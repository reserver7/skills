"""Run a disposable Codex scenario against the current Grounded checkout."""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from manage import ROOT, rule_text


def completed_items(events):
    with events.open() as stream:
        for line in stream:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "item.completed":
                yield event.get("item", {})


def skill_path_evidence(items, workspace, inventory):
    """Record path mentions in execution requests and their observed status."""
    paths = {}
    for item in items:
        kind = item.get("type")
        if kind == "command_execution":
            request = item.get("command", "")
            output = item.get("aggregated_output") or ""
            status = "command_succeeded" if item.get("exit_code") == 0 else "command_failed_or_unknown"
        elif kind == "mcp_tool_call" and "context_mode" in item.get("server", "").replace("-", "_"):
            request = json.dumps(item.get("arguments") or {})
            output = "\n".join(
                part.get("text", "") for part in (item.get("result") or {}).get("content", [])
                if part.get("type") == "text"
            )
            status = "tool_completed" if item.get("status") == "completed" and not item.get("error") else "tool_failed_or_unknown"
        else:
            continue
        for match in re.findall(r"[^\s'\";|&<>\\]+/SKILL\.md", request):
            path = Path(match).expanduser()
            path = (workspace / path).resolve()
            if path.parent.name not in inventory:
                continue
            evidence = "path_mention"
            if re.search(r"\b(?:cat|head|tail|sed|less|more|open|read_text)\b[^;&|\n]*"
                         + re.escape(match), request):
                evidence = "read_attempt"
            if path.is_file() and path.stat().st_size:
                body = path.read_text(errors="replace").strip()
                if body and body in output:
                    evidence = "body_visible"
            paths.setdefault(path, set()).add((status, evidence))
    expected = (workspace / ".agents" / "skills").resolve()
    evidence = []
    for path in sorted(paths):
        expected_hash = inventory.get(path.parent.name, {}).get("files", {}).get("SKILL.md")
        if not expected_hash:
            continue
        matches = path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == expected_hash
        evidence.append({"path": str(path), "fixture_copy": path.is_relative_to(expected),
                         "matches_prepared_hash": matches,
                         "request_statuses": sorted({status for status, _ in paths[path]}),
                         "evidence_types": sorted({kind for _, kind in paths[path]})})
    return evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    parser.add_argument("prompt")
    parser.add_argument("--write", action="store_true", help="Allow edits to the disposable fixture")
    parser.add_argument("--host-config", action="store_true", help="Load host MCP servers and hooks")
    parser.add_argument("--installed-skills", type=Path, default=Path.home() / ".agents" / "skills",
                        help="Directory containing the installed external skill collection")
    args = parser.parse_args()
    run = Path(tempfile.mkdtemp(prefix="grounded-local-"))
    workspace = run / "workspace"
    shutil.copytree(args.fixture, workspace, ignore=shutil.ignore_patterns(".git"), symlinks=True)
    if any(path.is_symlink() for path in workspace.rglob("*")):
        parser.error("Use a fixture without symlinks")
    subprocess.run(["git", "init", "--quiet", str(workspace)], check=True)
    instructions = workspace / "AGENTS.md"
    host_mcp_context = (
        "Host MCP configuration is enabled for this run; use only available tools relevant to the task."
        if args.host_config else
        "This run uses --ignore-user-config, so host MCP servers including Context7 and context-mode are unavailable. "
        "Do not claim they were used. Use exact official artifact fallback for versioned APIs; if unavailable, stop dependent work."
    )
    instructions.write_text(
        "## Validation execution context\n\n"
        "This is a fresh isolated `codex exec --ephemeral` task; no interrupted session exists to restore. Network is available for read-only official documentation and exact-version artifact lookups. Fetch artifacts to a temporary directory only if needed; do not install packages or change dependencies. Do not call `ctx_resume`.\n\n"
        + host_mcp_context + "\n\n"
        + rule_text(instructions) + (
        "\n## Validation fixture skill source\n\n"
        "For managed skills, read the selected instructions from "
        "`.agents/skills/<name>/SKILL.md` in this workspace. "
        "Use that path even when the host lists a matching global copy. Do not enumerate the skill directory; open only matched paths. "
        "Report missing fixture instructions.\n"
        )
    )
    manifest = json.loads((ROOT / "manifest.json").read_text())
    names = manifest["local_skills"] + [
        name for source in manifest["sources"].values() for name in source["skills"]
    ]
    inventory = {}
    for name in names:
        source = (ROOT / "skills" / name if name in manifest["local_skills"]
                  else args.installed_skills / name)
        target = workspace / ".agents" / "skills" / name
        shutil.copytree(source, target)
        inventory[name] = {
            "source": str(source.resolve()),
            "files": {
                str(file.relative_to(target)): hashlib.sha256(file.read_bytes()).hexdigest()
                for file in sorted(target.rglob("*")) if file.is_file()
            },
        }
    subprocess.run(["git", "-C", str(workspace), "add", "-A"], check=True)
    # OpenSpec can be ignored by host Git settings but is part of the fixture contract.
    if (workspace / "openspec").is_dir():
        subprocess.run(["git", "-C", str(workspace), "add", "--force", "--all", "--", "openspec"], check=True)
    subprocess.run([
        "git", "-C", str(workspace), "-c", "user.name=Grounded Eval",
        "-c", "user.email=grounded-eval@invalid", "commit", "--quiet",
        "-m", "fixture baseline",
    ], check=True)
    baseline = subprocess.check_output(
        ["git", "-C", str(workspace), "rev-parse", "HEAD"], text=True
    ).strip()
    policy_path = ROOT / "rules" / "development.md"
    effective_prompt = (
        "Validation context: this is a fresh isolated task with no interrupted session; read AGENTS.md first and do not call ctx_resume. "
        "Network is available for read-only official documentation and exact-version artifact lookups; use a temporary directory if needed, without installing packages or changing dependencies. "
        + host_mcp_context + "\n\n"
        + args.prompt
    )
    (run / "inputs.json").write_text(json.dumps({
        "instructions_sha256": hashlib.sha256(instructions.read_bytes()).hexdigest(),
        "policy_sha256": hashlib.sha256(policy_path.read_bytes()).hexdigest(),
        "policy_bytes": policy_path.stat().st_size,
        "fresh_ephemeral_task": True,
        "skills": inventory,
        "baseline": baseline,
        "host_config": args.host_config,
        "host_mcp_context": host_mcp_context,
        "prompt": args.prompt,
        "effective_prompt": effective_prompt,
    }, indent=2) + "\n")
    print(run, flush=True)
    command = [
        "codex", "exec", "--ephemeral", "--skip-git-repo-check", "--json",
        "-m", "gpt-6-luna", "-c", 'model_reasoning_effort="medium"',
        "-s", "workspace-write" if args.write else "read-only",
        "-C", str(workspace), effective_prompt,
    ]
    if not args.host_config:
        command.insert(2, "--ignore-user-config")
    stderr_log = run / "stderr.log"
    with (run / "events.jsonl").open("w") as events, stderr_log.open("w") as stderr:
        result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=events, stderr=stderr)
    subprocess.run(["git", "-C", str(workspace), "add", "--intent-to-add", "--all"], check=True)
    if (workspace / "openspec").is_dir():
        subprocess.run([
            "git", "-C", str(workspace), "add", "--force", "--intent-to-add", "--all", "--", "openspec",
        ], check=True)
    status = subprocess.run(
        ["git", "-C", str(workspace), "status", "--short"],
        check=True, capture_output=True, text=True,
    ).stdout
    with (run / "changes.diff").open("wb") as changes:
        subprocess.run(
            ["git", "-C", str(workspace), "diff", "--binary", baseline, "--"],
            stdout=changes, check=True,
        )
    diff_check = subprocess.run(
        ["git", "-C", str(workspace), "diff", "--check", baseline, "--"],
        check=False, capture_output=True, text=True,
    )
    diff_stat = subprocess.run(
        ["git", "-C", str(workspace), "diff", "--stat", baseline, "--"],
        check=True, capture_output=True, text=True,
    ).stdout
    items = list(completed_items(run / "events.jsonl"))
    skill_evidence = skill_path_evidence(items, workspace, inventory)
    mismatched_skills = [
        entry for entry in skill_evidence
        if Path(entry["path"]).parent.name in inventory
        and not (entry["fixture_copy"] and entry["matches_prepared_hash"])
        and "body_visible" in entry["evidence_types"]
    ]
    (run / "outcome.json").write_text(json.dumps({
        "codex_exit_code": result.returncode,
        "stderr_log": stderr_log.name,
        "tool_argument_error_count": stderr_log.read_text(errors="replace").count(
            "failed to parse function arguments:"
        ),
        "fresh_session_resume_calls": sum(
            item.get("type") == "mcp_tool_call" and item.get("tool") == "ctx_resume"
            for item in items
        ),
        "tool_call_statuses": [
            {key: item.get(key) for key in ("type", "server", "tool", "status", "exit_code")}
            for item in items if item.get("type") in {"mcp_tool_call", "collab_tool_call"}
        ],
        "skill_path_evidence": skill_evidence,
        "mismatched_skill_paths": mismatched_skills,
        "status": status,
        "diff_check_exit_code": diff_check.returncode,
        "diff_check_output": diff_check.stdout + diff_check.stderr,
        "diff_stat": diff_stat,
    }, indent=2) + "\n")
    raise SystemExit(result.returncode or int(bool(mismatched_skills)))


if __name__ == "__main__":
    main()
