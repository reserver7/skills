#!/usr/bin/env python3
"""Install a curated AI environment. Python 3.11+, standard library only."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib

ROOT = Path(__file__).resolve().parents[1]
BEGIN = "<!-- skills-environment:begin -->"
END = "<!-- skills-environment:end -->"


def run(*args, **kwargs):
    return subprocess.check_output(args, text=True, **kwargs).strip()


def load(path, default=None):
    return json.loads(path.read_text()) if path.exists() else default


def hashes(folder):
    return {str(p.relative_to(folder)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(folder.rglob("*")) if p.is_file()}


def skill_name(path):
    text = path.read_text()
    match = re.search(r"(?m)^name:\s*['\"]?([a-z0-9-]+)", text)
    return match.group(1) if match else path.parent.name


def rule_text(path):
    if path.is_symlink():
        raise ValueError(f"Instruction file is a symlink; manage it explicitly: {path}")
    text = path.read_text() if path.exists() else ""
    if text.count(BEGIN) != text.count(END) or text.count(BEGIN) > 1:
        raise ValueError(f"Malformed managed block: {path}")
    if BEGIN in text and text.index(BEGIN) > text.index(END):
        raise ValueError(f"Reversed managed block: {path}")
    block = BEGIN + "\n" + (ROOT / "rules/development.md").read_text().rstrip() + "\n" + END
    if BEGIN in text:
        return text[:text.index(BEGIN)] + block + text[text.index(END) + len(END):]
    return text + ("\n\n" if text and not text.endswith("\n\n") else "") + block + "\n"


def conflicts(home, manifest, registry, hosts):
    errors = []
    desired = set(manifest["local_skills"])
    for source in manifest["sources"].values():
        desired.update(source["skills"])
    banned = desired | set(manifest["incompatible_skills"])
    roots = [home / ".agents/skills"]
    if "codex" in hosts:
        roots.append(home / ".codex/skills")
    if "claude" in hosts:
        roots.append(home / ".claude/skills")
    for root in roots:
        if not root.exists():
            continue
        # Include linked top-level skill folders without recursively following arbitrary links.
        files = set(root.rglob("SKILL.md"))
        files.update(p / "SKILL.md" for p in root.iterdir() if (p / "SKILL.md").is_file())
        for file in files:
            if skill_name(file) not in banned:
                continue
            key = str(file.parent)
            if key not in registry.get("skills", {}):
                errors.append(f"Unmanaged overlapping skill: {file}")
    plugin_settings = []
    codex = home / ".codex/config.toml"
    if "codex" in hosts and codex.exists():
        data = tomllib.loads(codex.read_text())
        plugin_settings.extend((k, v.get("enabled", False)) for k, v in data.get("plugins", {}).items() if isinstance(v, dict))
    claude = home / ".claude/settings.json"
    if "claude" in hosts and claude.exists():
        plugin_settings.extend(load(claude, {}).get("enabledPlugins", {}).items())
    for name, enabled in plugin_settings:
        if enabled and name.split("@")[0] in manifest["incompatible_plugins"]:
            errors.append(f"Enabled overlapping plugin: {name}; disable it in that host first")
    return errors


def project_conflicts(project, manifest, hosts):
    errors = []
    for ancestor in [project, *project.parents]:
        if "claude" in hosts:
            for relative in [".claude/settings.json", ".claude/settings.local.json"]:
                path = ancestor / relative
                for name, enabled in load(path, {}).get("enabledPlugins", {}).items():
                    if enabled and name.split("@")[0] in manifest["incompatible_plugins"]:
                        errors.append(f"Overlapping project plugin {name}: {path}")
        if "codex" in hosts:
            path = ancestor / ".codex/config.toml"
            data = tomllib.loads(path.read_text()) if path.exists() else {}
            for name, config in data.get("plugins", {}).items():
                if isinstance(config, dict) and config.get("enabled") and name.split("@")[0] in manifest["incompatible_plugins"]:
                    errors.append(f"Overlapping project plugin {name}: {path}")
        if (ancestor / ".git").exists():
            break
    return errors


def validate_repo(manifest):
    if manifest["schema"] != 1:
        raise ValueError("Unsupported manifest schema")
    names = list(manifest["local_skills"])
    for source in manifest["sources"].values():
        if not re.fullmatch(r"[0-9a-f]{40}", source["commit"]):
            raise ValueError("Sources must use full Git commit pins")
        if not source["url"].startswith("https://github.com/"):
            raise ValueError("Source URL must be an explicit HTTPS GitHub repository")
        names.extend(source["skills"])
    if len(names) != len(set(names)):
        raise ValueError("Duplicate skill name in manifest")
    for name in names:
        if not re.fullmatch(r"[a-z0-9-]+", name):
            raise ValueError(f"Unsafe skill name: {name}")
    for name in manifest["local_skills"]:
        path = ROOT / "skills" / name / "SKILL.md"
        if skill_name(path) != name:
            raise ValueError(f"Skill name mismatch: {path}")
        if len(path.read_bytes()) > 6000:
            raise ValueError(f"Local skill exceeds the 6KB instruction budget: {path}")
        if "disable-model-invocation: true" not in path.read_text():
            raise ValueError(f"Optional local skill must be explicit-only: {path}")
    if len((ROOT / "rules/development.md").read_bytes()) > 6500:
        raise ValueError("Default policy exceeds the 6.5KB budget")


def fetch_source(state, name, source):
    dest = state / "sources" / name / source["commit"]
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=dest.parent) as temp:
            work = Path(temp) / "repo"
            run("git", "init", "--quiet", str(work))
            run("git", "-C", str(work), "fetch", "--quiet", "--depth=1", source["url"], source["commit"])
            run("git", "-C", str(work), "checkout", "--quiet", "--detach", "FETCH_HEAD")
            work.rename(dest)
    if run("git", "-C", str(dest), "rev-parse", "HEAD") != source["commit"]:
        raise ValueError(f"Source pin mismatch: {dest}")
    if run("git", "-C", str(dest), "status", "--porcelain"):
        raise ValueError(f"Source cache has local modifications: {dest}")
    return dest


def prepare(state, manifest, stage):
    for name in manifest["local_skills"]:
        shutil.copytree(ROOT / "skills" / name, stage / name)
        shutil.copy2(ROOT / "LICENSE", stage / name / "LICENSE.review-skills")
    for name, source in manifest["sources"].items():
        upstream = fetch_source(state, name, source)
        for skill in source["skills"]:
            target = stage / skill
            shutil.copytree(upstream / "skills" / skill, target)
            for license_file in upstream.glob("LICENSE*"):
                if license_file.is_file():
                    shutil.copy2(license_file, target / license_file.name)
            body = target / "SKILL.md"
            text = body.read_text()
            # Standalone skill installation has no superpowers plugin namespace.
            text = text.replace("superpowers:", "")
            body.write_text(text)
            if skill == "requesting-code-review":
                shutil.copy2(ROOT / "setup/adapters/requesting-code-review.md", body)
    for path in stage.glob("*/SKILL.md"):
        # CLI/IDE Codex and Claude share bodies, not invocation-control metadata.
        agents = path.parent / "agents"
        agents.mkdir(exist_ok=True)
        (agents / "openai.yaml").write_text("policy:\n  allow_implicit_invocation: false\n" if path.parent.name in manifest["local_skills"] else "policy:\n  allow_implicit_invocation: true\n")


def install(args, manifest, state, registry):
    hosts = ["codex", "claude"] if args.host == "both" else [args.host]
    errors = conflicts(args.home, manifest, registry, hosts)
    destinations = [args.home / (".agents/skills" if h == "codex" else ".claude/skills") for h in hosts]
    instructions = [args.home / (".codex/AGENTS.md" if h == "codex" else ".claude/CLAUDE.md") for h in hosts]
    names = manifest["local_skills"] + [n for s in manifest["sources"].values() for n in s["skills"]]
    stale = [Path(p) for p in registry.get("skills", {})
             if Path(p).parent in destinations and Path(p).name not in names]
    for dest in stale:
        if dest.is_symlink() or (dest.exists() and hashes(dest) != registry["skills"][str(dest)]):
            errors.append(f"Edited obsolete managed skill; preserve/resolve before update: {dest}")
    for base in destinations:
        for name in names:
            dest = base / name
            previous = registry.get("skills", {}).get(str(dest))
            if dest.is_symlink():
                errors.append(f"Refusing to replace symlink: {dest}")
            elif dest.exists() and (previous is None or hashes(dest) != previous):
                errors.append(f"Unmanaged or edited destination: {dest}")
    blocks = {p: rule_text(p) for p in instructions}
    if errors:
        raise ValueError("\n".join(sorted(set(errors))))
    print("Hosts:", ", ".join(hosts))
    print("Skills:", ", ".join(names))
    print("Instruction files:", ", ".join(str(p) for p in instructions))
    if args.dry_run:
        print("Dry run: no downloads, installs or writes. Source contents are not checked.")
        return
    for tool in ["git", "node", "npm"]:
        if not shutil.which(tool):
            raise ValueError(f"Install prerequisite first: {tool}")
    version = tuple(int(x) for x in run("node", "--version").lstrip("v").split(".")[:3])
    if version < (20, 19, 0):
        raise ValueError("Node.js >=20.19.0 is required")
    state.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=state) as temp:
        stage = Path(temp) / "skills"
        stage.mkdir()
        prepare(state, manifest, stage)
        npm = state / "npm"
        package = manifest["openspec"]
        installed = load(npm / "node_modules/@fission-ai/openspec/package.json", {})
        if installed.get("version") != package["version"]:
            subprocess.run(["npm", "install", "--prefix", str(npm), "--no-audit", "--no-fund", f"{package['package']}@{package['version']}"], check=True)
        backup = state / "backups" / str(time.time_ns())
        backup.mkdir(parents=True)
        saved = []
        old_registry = json.loads(json.dumps(registry))
        try:
            for index, dest in enumerate(stale):
                previous = backup / f"obsolete-{index}-{dest.name}"
                existed = dest.exists()
                if existed:
                    dest.rename(previous)
                saved.append((dest, previous, existed, True))
                registry["skills"].pop(str(dest))
            for index, base in enumerate(destinations):
                base.mkdir(parents=True, exist_ok=True)
                for name in names:
                    dest = base / name
                    previous = backup / f"{index}-{name}"
                    existed = dest.exists()
                    if existed:
                        dest.rename(previous)
                    saved.append((dest, previous, existed, True))
                    shutil.copytree(stage / name, dest)
                    registry.setdefault("skills", {})[str(dest)] = hashes(dest)
            for index, (path, content) in enumerate(blocks.items()):
                path.parent.mkdir(parents=True, exist_ok=True)
                previous = backup / f"instructions-{index}.md"
                existed = path.exists()
                if existed:
                    shutil.copy2(path, previous)
                saved.append((path, previous, existed, False))
                path.write_text(content)
            registry["manifest_sha256"] = hashlib.sha256((ROOT / "manifest.json").read_bytes()).hexdigest()
            registry["repository"] = str(ROOT)
            temporary = state / "installed.tmp"
            temporary.write_text(json.dumps(registry, indent=2) + "\n")
            temporary.replace(state / "installed.json")
        except BaseException:
            for dest, previous, existed, directory in reversed(saved):
                if directory and dest.exists():
                    shutil.rmtree(dest)
                elif not directory and dest.exists():
                    dest.unlink()
                if existed:
                    if directory:
                        previous.rename(dest)
                    else:
                        shutil.copy2(previous, dest)
            registry.clear()
            registry.update(old_registry)
            raise
    print("Installed. Backups:", backup)
    print("Restart Codex/Claude. Run doctor from inside each project before development.")


def doctor(args, manifest, state, registry):
    hosts = ["codex", "claude"] if args.host == "both" else [args.host]
    errors = conflicts(args.home, manifest, registry, hosts)
    names = manifest["local_skills"] + [n for s in manifest["sources"].values() for n in s["skills"]]
    for host in hosts:
        base = args.home / (".agents/skills" if host == "codex" else ".claude/skills")
        for name in names:
            if str(base / name) not in registry.get("skills", {}):
                errors.append(f"Missing managed installation: {base / name}")
    for path, expected in registry.get("skills", {}).items():
        if not Path(path).is_dir() or hashes(Path(path)) != expected:
            errors.append(f"Missing or changed managed skill: {path}")
    for host in hosts:
        path = args.home / (".codex/AGENTS.md" if host == "codex" else ".claude/CLAUDE.md")
        if not path.exists() or path.read_text() != rule_text(path):
            errors.append(f"Missing or stale managed policy: {path}")
    if registry.get("manifest_sha256") != hashlib.sha256((ROOT / "manifest.json").read_bytes()).hexdigest():
        errors.append("Environment not installed with this manifest; run install")
    project = args.project.resolve() if args.project else Path.cwd()
    errors.extend(project_conflicts(project, manifest, hosts))
    for ancestor in [project, *project.parents]:
        for relative in [".agents/skills", ".codex/skills", ".claude/skills"]:
            directory = ancestor / relative
            if directory.exists() and not directory.is_relative_to(args.home / ".agents") and not directory.is_relative_to(args.home / ".claude"):
                for file in directory.rglob("SKILL.md"):
                    if skill_name(file) in set(manifest["incompatible_skills"]) | {n for s in manifest["sources"].values() for n in s["skills"]} | set(manifest["local_skills"]):
                        errors.append(f"Project/ancestor overlapping skill: {file}")
        if (ancestor / ".git").exists():
            break
    print("Repository structure: valid")
    if errors:
        raise ValueError("\n".join(sorted(set(errors))))
    package = load(state / "npm/node_modules/@fission-ai/openspec/package.json", {})
    if package.get("version") != manifest["openspec"]["version"]:
        raise ValueError("Pinned OpenSpec is missing or has a different version")
    print("Managed skills, policy, pins and known overlap checks: passed")
    print("Project-specific prose, nonstandard skill/plugin paths and actual agent behavior still require review.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["install", "doctor", "check", "openspec"])
    parser.add_argument("--host", choices=["codex", "claude", "both"], default="both")
    parser.add_argument("--home", type=Path, default=Path.home(), help="Installation home (default: current user's home)")
    parser.add_argument("--project", type=Path, help="Project path for doctor or OpenSpec")
    parser.add_argument("--dry-run", action="store_true", help="Install preflight only; no writes/downloads")
    args, extra = parser.parse_known_args()
    if extra and args.command != "openspec":
        parser.error("Unexpected arguments: " + " ".join(extra))
    args.home = args.home.expanduser().resolve()
    if args.command in {"install", "doctor", "openspec"} and args.home == Path.home().resolve():
        defaults = {"CODEX_HOME": args.home / ".codex", "CLAUDE_CONFIG_DIR": args.home / ".claude"}
        relevant = list(defaults) if args.host == "both" else ["CODEX_HOME" if args.host == "codex" else "CLAUDE_CONFIG_DIR"]
        custom = [name for name in relevant if os.environ.get(name)
                  and Path(os.environ[name]).expanduser().resolve() != defaults[name]]
        if custom:
            raise ValueError("Custom host directories are not supported by this setup: " + ", ".join(custom))
    manifest = load(ROOT / "manifest.json")
    validate_repo(manifest)
    state = args.home / ".local/share/skills-environment"
    registry = load(state / "installed.json", {})
    if args.command == "check":
        print("Repository manifest, names and instruction budgets: valid (no runtime validation)")
    elif args.command == "install":
        if args.dry_run:
            install(args, manifest, state, registry)
        else:
            state.mkdir(parents=True, exist_ok=True)
            with (state / "install.lock").open("w") as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                install(args, manifest, state, load(state / "installed.json", {}))
    elif args.command == "doctor":
        doctor(args, manifest, state, registry)
    else:
        binary = state / "npm/node_modules/.bin/openspec"
        if not binary.exists():
            raise ValueError("Run install first; pinned OpenSpec binary is missing")
        extra = extra[1:] if extra[:1] == ["--"] else extra
        subprocess.run([str(binary), *extra], cwd=args.project, check=True)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
