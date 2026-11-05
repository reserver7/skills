#!/usr/bin/env python3
"""Install a curated AI environment. Python 3.11+, standard library only."""
import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import tomllib
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen
from release import validate_release_notes

ROOT = Path(__file__).resolve().parents[1]
BEGIN = "<!-- skills-environment:begin -->"
END = "<!-- skills-environment:end -->"


def run(*args, **kwargs):
    return subprocess.check_output(args, text=True, **kwargs).strip()


def load(path, default=None):
    return json.loads(path.read_text()) if path.exists() else default


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        path.chmod(0o600)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def write_text_atomic(path, value, mode=0o644):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, "w") as stream:
            stream.write(value)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def private_dir(path):
    path.mkdir(parents=True, exist_ok=True)
    path.chmod(0o700)
    return path


def private_tree(path):
    if path.is_symlink():
        return
    if path.is_dir():
        path.chmod(0o700)
        for child in path.iterdir():
            private_tree(child)
    elif path.exists():
        path.chmod(0o600)


def tree_modes(path):
    if path.is_symlink():
        return {".": stat.S_IMODE(path.lstat().st_mode)}
    if not path.is_dir():
        return {".": stat.S_IMODE(path.stat().st_mode)}
    result = {".": stat.S_IMODE(path.stat().st_mode)}
    for child in path.rglob("*"):
        if not child.is_symlink():
            result[str(child.relative_to(path))] = stat.S_IMODE(child.stat().st_mode)
    return result


def restore_modes(path, modes):
    for relative, mode in sorted(modes.items(), key=lambda item: item[0].count("/"), reverse=True):
        target = path if relative == "." else path / relative
        if target.exists() and not target.is_symlink():
            target.chmod(mode)


def private_copy(source, destination):
    modes = tree_modes(source)
    private_dir(destination.parent)
    if source.is_dir():
        shutil.copytree(source, destination, symlinks=True)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    private_tree(destination)
    return modes


def remote_json(url, accept):
    request = Request(url, headers={
        "Accept": accept,
        "User-Agent": "Grounded-setup",
    })
    try:
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read())
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        raise ValueError(f"Could not resolve official release metadata from {url}: {error}") from error


SEMVER_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:\+[0-9A-Za-z.-]+)?$")
SRI_RE = re.compile(r"^(?:sha512|sha384|sha256)-[A-Za-z0-9+/=]+(?:\s+(?:sha512|sha384|sha256)-[A-Za-z0-9+/=]+)*$")


def stable_version(value):
    match = SEMVER_RE.fullmatch(value or "")
    return tuple(int(part) for part in match.group(1, 2, 3)) if match else None


def github_repo(url):
    parsed = urlparse(url)
    parts = parsed.path.strip("/").removesuffix(".git").split("/")
    if parsed.scheme != "https" or parsed.netloc != "github.com" or parsed.query or parsed.fragment or len(parts) != 2:
        raise ValueError(f"Source URL must be an official HTTPS GitHub repository: {url}")
    if not all(re.fullmatch(r"[A-Za-z0-9_.-]+", part) for part in parts):
        raise ValueError(f"Invalid GitHub repository URL: {url}")
    return parts


def resolve_dependencies(manifest):
    resolved = {"resolved_at": datetime.now(timezone.utc).isoformat(), "sources": {}}
    for name, source in manifest["sources"].items():
        owner, repo = github_repo(source["url"])
        release_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
        release = remote_json(release_url, "application/vnd.github+json")
        if not isinstance(release, dict):
            raise ValueError(f"Malformed release metadata for {name} at {source['url']}")
        tag = release.get("tag_name")
        if release.get("draft") or release.get("prerelease") or not stable_version(tag.removeprefix("v") if isinstance(tag, str) else None):
            raise ValueError(f"No stable semantic-version release is available for {name} at {source['url']}")
        refs = subprocess.run(
            ["git", "ls-remote", "--exit-code", source["url"], f"refs/tags/{tag}", f"refs/tags/{tag}^{{}}"],
            capture_output=True, text=True,
        )
        if refs.returncode:
            raise ValueError(f"Could not resolve release tag {tag} for {name}: {refs.stderr.strip()}")
        tag_refs = {line.split("\t", 1)[1]: line.split("\t", 1)[0]
                    for line in refs.stdout.splitlines() if "\t" in line}
        commit = tag_refs.get(f"refs/tags/{tag}^{{}}") or tag_refs.get(f"refs/tags/{tag}")
        if not commit or not re.fullmatch(r"[0-9a-f]{40}", commit):
            raise ValueError(f"Release tag {tag} for {name} did not resolve to a full Git commit SHA")
        resolved["sources"][name] = {
            "url": source["url"], "tag": tag, "version": tag.removeprefix("v"),
            "commit": commit, "release_url": release.get("html_url", release_url),
        }

    package = manifest["openspec"]
    registry = package["registry"].rstrip("/")
    if registry != "https://registry.npmjs.org":
        raise ValueError(f"OpenSpec registry must be the official npm registry: {registry}")
    package_name = package["package"]
    if not re.fullmatch(r"@[a-z0-9-]+/[a-z0-9._-]+", package_name):
        raise ValueError(f"Invalid npm package name: {package_name}")
    metadata = remote_json(f"{registry}/{quote(package_name, safe='@')}", "application/vnd.npm.install-v1+json")
    versions = metadata.get("versions", {}) if isinstance(metadata, dict) else {}
    package_version = metadata.get("dist-tags", {}).get("latest") if isinstance(metadata, dict) else None
    parsed = stable_version(package_version)
    details = versions.get(package_version, {}) if package_version else {}
    integrity = details.get("dist", {}).get("integrity") if isinstance(details, dict) else None
    if not parsed or not isinstance(integrity, str) or not SRI_RE.fullmatch(integrity) or details.get("deprecated"):
        raise ValueError(f"npm latest for {package_name} is not a non-deprecated stable release with integrity metadata")
    resolved["openspec"] = {
        "package": package_name, "registry": registry, "version": package_version,
        "integrity": integrity,
    }
    return resolved


def print_resolved(resolved):
    print("Resolved stable dependencies:")
    for name, item in resolved["sources"].items():
        print(f"  {name}: {item['version']} ({item['commit']})")
    package = resolved["openspec"]
    print(f"  openspec: {package['version']} ({package['integrity']})")


def print_previous(registry):
    resolved = registry.get("resolved", {})
    if not resolved:
        return
    print("Previous successful setup:")
    if resolved.get("legacy"):
        print("  dependency receipt migrated from the legacy installation")
    for name, item in resolved.get("sources", {}).items():
        print(f"  {name}: {item.get('version', 'unknown')} ({item.get('commit', 'unknown')})")
    package = registry.get("openspec", {})
    if package:
        print(f"  openspec: {package.get('version', 'unknown')} ({package.get('integrity', 'unknown')})")


def hashes(folder):
    return {str(p.relative_to(folder)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(folder.rglob("*")) if p.is_file()}


def skill_name(path):
    text = path.read_text()
    match = re.search(r"(?m)^name:\s*['\"]?([a-z0-9-]+)", text)
    return match.group(1) if match else path.parent.name


def safe_component(value):
    if not re.fullmatch(r"[A-Za-z0-9._-]+", value):
        raise ValueError(f"Unsafe plugin path component: {value!r}")
    return value


def rule_text(path):
    if path.is_symlink():
        raise ValueError(f"Instruction file is a symlink; manage it explicitly: {path}")
    text = path.read_text() if path.exists() else ""
    if text.count(BEGIN) != text.count(END) or text.count(BEGIN) > 1:
        raise ValueError(f"Malformed managed block: {path}")
    if BEGIN in text and text.index(BEGIN) > text.index(END):
        raise ValueError(f"Reversed managed block: {path}")
    version = load(ROOT / "plugin.json")["version"]
    block = BEGIN + f"\n<!-- grounded-version: {version} -->\n" + (ROOT / "rules/development.md").read_text().rstrip() + "\n" + END
    if BEGIN in text:
        return text[:text.index(BEGIN)] + block + text[text.index(END) + len(END):]
    return text + ("\n\n" if text and not text.endswith("\n\n") else "") + block + "\n"


def managed_block(text):
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        return None
    start = text.index(BEGIN)
    end = text.index(END)
    if start > end:
        return None
    return text[start:end + len(END)]


def block_hash(text):
    block = managed_block(text)
    return hashlib.sha256(block.encode()).hexdigest() if block else None


def replace_managed_block(text, replacement):
    current = managed_block(text)
    if current:
        start = text.index(BEGIN)
        end = text.index(END) + len(END)
        return text[:start] + (replacement or "") + text[end:]
    if replacement:
        return text + ("\n\n" if text and not text.endswith("\n\n") else "") + replacement + "\n"
    return text


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
        files = {p / "SKILL.md" for p in root.iterdir() if (p / "SKILL.md").is_file()}
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


def native_conflicts(args, manifest, registry, backup):
    """Move known global skill duplicates aside and disable overlapping host plugins."""
    hosts = ["codex", "claude"] if args.host == "both" else [args.host]
    names = set(manifest["local_skills"] + manifest["incompatible_skills"])
    dependency_names = set()
    for source in manifest["sources"].values():
        names.update(source["skills"])
        dependency_names.update(source["skills"])
    roots = [args.home / ".agents/skills"]
    if "codex" in hosts:
        roots.append(args.home / ".codex/skills")
    if "claude" in hosts:
        roots.append(args.home / ".claude/skills")
    skills = []
    for root in roots:
        if root.is_dir():
            for path in root.iterdir():
                skill = path / "SKILL.md"
                if skill.is_file() and skill_name(skill) in names:
                    name = skill_name(skill)
                    expected = registry.get("skills", {}).get(str(path))
                    if name in dependency_names and expected is not None and hashes(path) == expected:
                        continue
                    skills.append(path)

    plugins = {"codex": [], "claude": []}
    codex_list = None
    if "codex" in hosts and shutil.which("codex"):
        try:
            codex_list = json.loads(run("codex", "plugin", "list", "--json"))
        except (subprocess.CalledProcessError, json.JSONDecodeError) as error:
            raise ValueError(f"Could not inspect Codex plugins safely: {error}") from error
        for plugin in codex_list.get("installed", []):
            plugin_id = plugin.get("pluginId", "")
            if plugin.get("enabled") and plugin.get("name") in manifest["incompatible_plugins"]:
                plugins["codex"].append(plugin)
    elif "codex" in hosts:
        codex = args.home / ".codex/config.toml"
        if codex.exists():
            settings = tomllib.loads(codex.read_text()).get("plugins", {})
            if any(v.get("enabled") and k.split("@")[0] in manifest["incompatible_plugins"]
                   for k, v in settings.items() if isinstance(v, dict)):
                raise ValueError("Install the Codex CLI to migrate overlapping plugins safely")

    if "claude" in hosts:
        settings = load(args.home / ".claude/settings.json", {})
        plugins["claude"] = [name for name, enabled in settings.get("enabledPlugins", {}).items()
                             if enabled and name.split("@")[0] in manifest["incompatible_plugins"]]
        if plugins["claude"] and not shutil.which("claude"):
            raise ValueError("Install the Claude CLI to disable overlapping plugins safely")

    print("Local duplicate skills to archive:", ", ".join(map(str, skills)) or "none")
    print("Codex plugins to remove:", ", ".join(p["pluginId"] for p in plugins["codex"]) or "none")
    print("Claude plugins to disable:", ", ".join(plugins["claude"]) or "none")
    if args.dry_run:
        return None
    if not skills and not plugins["codex"] and not plugins["claude"]:
        return None

    private_dir(backup.parent)
    private_dir(backup)
    saved_settings = []
    plugin_data = []
    moved = []
    removed_plugins = []
    disabled_plugins = []
    def save_metadata():
        write_json(backup / "migration.json", {
            "hosts": hosts,
            "archived_skills": [{"source": str(source), "backup": str(target), "modes": modes}
                                for source, target, modes in moved],
            "removed_codex_plugins": removed_plugins,
            "disabled_claude_plugins": disabled_plugins,
            "settings": saved_settings,
            "plugin_data": plugin_data,
        })
    for host, paths in {
        "codex": [args.home / ".codex/config.toml", args.home / ".codex/AGENTS.md"],
        "claude": [args.home / ".claude/settings.json", args.home / ".claude/CLAUDE.md"],
    }.items():
        if host in hosts:
            for index, source in enumerate(paths):
                if source.is_symlink():
                    raise ValueError(f"Refusing to back up host settings symlink: {source}")
                if source.is_file():
                    target = backup / "settings" / host / f"{index}-{source.name}"
                    modes = private_copy(source, target)
                    saved_settings.append({"source": str(source), "backup": str(target), "modes": modes})
    save_metadata()
    try:
        for plugin in plugins["codex"]:
            marketplace = safe_component(plugin.get("marketplaceName", ""))
            name = safe_component(plugin.get("name", ""))
            plugin_id = plugin.get("pluginId", "")
            if not re.fullmatch(r"[A-Za-z0-9._-]+@[A-Za-z0-9._-]+", plugin_id):
                raise ValueError(f"Unsafe Codex plugin identifier: {plugin_id!r}")
            for label, source, relative in [
                ("cache", args.home / ".codex/plugins/cache" / marketplace / name, Path(marketplace) / name),
                ("marketplace", args.home / ".codex/.tmp/marketplaces" / marketplace, Path(marketplace)),
            ]:
                if source.exists():
                    target = backup / "codex-plugin-data" / label / relative
                    modes = private_copy(source, target)
                    plugin_data.append({"source": str(source), "backup": str(target), "kind": label, "modes": modes})
                    save_metadata()
            removed_plugins.append(plugin_id)
            save_metadata()
            subprocess.run(["codex", "plugin", "remove", plugin_id, "--json"], check=True,
                           stdout=subprocess.DEVNULL)
        for plugin_id in plugins["claude"]:
            disabled_plugins.append(plugin_id)
            save_metadata()
            subprocess.run(["claude", "plugin", "disable", plugin_id, "--scope", "user"], check=True,
                           stdout=subprocess.DEVNULL)
        for index, source in enumerate(skills):
            target = backup / "skills" / f"{index}-{source.parent.name}-{source.name}"
            target.parent.mkdir(parents=True, exist_ok=True)
            modes = tree_modes(source)
            moved.append((source, target, modes))
            save_metadata()
            source.rename(target)
            private_tree(target)
        return backup
    except BaseException as error:
        try:
            restore_native_conflicts(backup, args)
        except (OSError, ValueError, subprocess.SubprocessError) as restore_error:
            raise ValueError(f"Conflict migration failed ({error}); recovery incomplete ({restore_error}); backup: {backup}") from error
        raise


def restore_native_conflicts(backup, args):
    if not backup or not Path(backup).exists():
        return
    backup = Path(backup)
    metadata = load(backup / "migration.json", {})
    errors = []
    allowed_skill_roots = [args.home / ".agents/skills", args.home / ".codex/skills", args.home / ".claude/skills"]
    for entry in metadata.get("archived_skills", []):
        source, saved = Path(entry["source"]), Path(entry["backup"])
        if not any(source.resolve(strict=False).is_relative_to(root.resolve(strict=False)) for root in allowed_skill_roots):
            errors.append(f"Refusing to restore skill outside host skill roots: {source}")
            continue
        if not saved.resolve(strict=False).is_relative_to(backup.resolve()):
            errors.append(f"Refusing to read backup outside transaction: {saved}")
            continue
        if saved.exists():
            if source.exists() or source.is_symlink():
                if source.is_dir() and not source.is_symlink() and saved.is_dir() and hashes(source) == hashes(saved):
                    continue
                print(f"Preserved existing skill path {source}; archived copy remains at {saved}")
                continue
            source.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(saved, source, symlinks=True) if saved.is_dir() else shutil.copy2(saved, source)
            restore_modes(source, entry.get("modes", {}))
    for plugin_id in metadata.get("disabled_claude_plugins", []):
        settings = load(args.home / ".claude/settings.json", {})
        if settings.get("enabledPlugins", {}).get(plugin_id, False):
            continue
        result = subprocess.run(["claude", "plugin", "enable", plugin_id, "--scope", "user"],
                                capture_output=True, text=True)
        if result.returncode:
            errors.append(f"Claude {plugin_id}: {result.stderr.strip()}")
    for plugin_id in metadata.get("removed_codex_plugins", []):
        if not re.fullmatch(r"[A-Za-z0-9._-]+@[A-Za-z0-9._-]+", plugin_id):
            errors.append(f"Unsafe Codex plugin identifier in backup: {plugin_id!r}")
            continue
        for entry in metadata.get("plugin_data", []):
            if entry.get("kind") != "marketplace":
                continue
            source, saved = Path(entry["source"]), Path(entry["backup"])
            marketplace_root = (args.home / ".codex/.tmp/marketplaces").resolve()
            if not source.resolve(strict=False).is_relative_to(marketplace_root):
                errors.append(f"Refusing to restore marketplace outside Codex cache: {source}")
                continue
            if not saved.resolve(strict=False).is_relative_to(backup.resolve()):
                errors.append(f"Refusing to read marketplace backup outside transaction: {saved}")
                continue
            if not source.exists() and saved.exists():
                shutil.copytree(saved, source, symlinks=True)
                restore_modes(source, entry.get("modes", {}))
        try:
            current = json.loads(run("codex", "plugin", "list", "--json"))
        except (subprocess.CalledProcessError, json.JSONDecodeError) as error:
            errors.append(f"Codex plugin list: {error}")
            continue
        installed = any(plugin.get("pluginId") == plugin_id for plugin in current.get("installed", []))
        if not installed:
            result = subprocess.run(["codex", "plugin", "add", plugin_id], capture_output=True, text=True)
            if result.returncode:
                errors.append(f"Codex {plugin_id}: {result.stderr.strip()}")
                continue
        for entry in metadata.get("plugin_data", []):
            source, saved = Path(entry["source"]), Path(entry["backup"])
            cache_root = (args.home / ".codex/plugins/cache").resolve()
            if entry.get("kind") != "cache" or not source.resolve(strict=False).is_relative_to(cache_root):
                continue
            if not saved.resolve(strict=False).is_relative_to(backup.resolve()):
                errors.append(f"Refusing to read plugin backup outside transaction: {saved}")
                continue
            if saved.exists():
                if source.exists():
                    shutil.rmtree(source)
                source.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(saved, source, symlinks=True)
                restore_modes(source, entry.get("modes", {}))
    if errors:
        raise ValueError("Could not fully restore native conflicts; use backup at " + str(backup) + ": " + "; ".join(errors))


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
    if manifest["schema"] != 2:
        raise ValueError("Unsupported manifest schema")
    plugin = load(ROOT / "plugin.json")
    claude = load(ROOT / ".claude-plugin/plugin.json")
    if plugin.get("version") != claude.get("version"):
        raise ValueError("Codex and Claude plugin versions differ; run setup/release.py bump")
    validate_release_notes(plugin)
    names = list(manifest["local_skills"])
    for source in manifest["sources"].values():
        github_repo(source["url"])
        if not source.get("skills") or any(not re.fullmatch(r"[a-z0-9-]+", name) for name in source["skills"]):
            raise ValueError("Each source must declare safe skill names")
        names.extend(source["skills"])
    package = manifest["openspec"]
    if package.get("registry") != "https://registry.npmjs.org" or not re.fullmatch(r"@[a-z0-9-]+/[a-z0-9._-]+", package.get("package", "")):
        raise ValueError("OpenSpec must use the official npm package and registry")
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


def fetch_source(state, name, source, resolved):
    commit = resolved["commit"]
    dest = state / "sources" / name / commit
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=dest.parent) as temp:
            work = Path(temp) / "repo"
            run("git", "init", "--quiet", str(work))
            run("git", "-C", str(work), "fetch", "--quiet", "--depth=1", source["url"], commit)
            run("git", "-C", str(work), "checkout", "--quiet", "--detach", "FETCH_HEAD")
            work.rename(dest)
    if run("git", "-C", str(dest), "rev-parse", "HEAD") != commit:
        raise ValueError(f"Source SHA mismatch: {dest}")
    if run("git", "-C", str(dest), "status", "--porcelain"):
        raise ValueError(f"Source cache has local modifications: {dest}")
    return dest


def prepare_openspec(state, package):
    prefix = state / "npm-versions" / package["version"]
    installed_path = prefix / "node_modules" / "@fission-ai" / "openspec" / "package.json"
    lock_path = prefix / "package-lock.json"
    if prefix.exists():
        installed = load(installed_path, {})
        lock = load(lock_path, {})
        entry = lock.get("packages", {}).get("node_modules/@fission-ai/openspec", {})
        if installed.get("version") != package["version"] or entry.get("integrity") != package["integrity"]:
            raise ValueError(f"Cached OpenSpec version/integrity mismatch: {prefix}")
        return {**package, "cache": str(prefix.relative_to(state)),
                "lock_sha256": hashlib.sha256(lock_path.read_bytes()).hexdigest()}

    prefix.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=prefix.parent) as temp:
        staged = Path(temp) / "package"
        staged.mkdir()
        subprocess.run([
            "npm", "install", "--prefix", str(staged), "--no-audit", "--no-fund",
            "--registry", package["registry"], f"{package['package']}@{package['version']}",
        ], check=True)
        installed = load(staged / "node_modules/@fission-ai/openspec/package.json", {})
        lock_path = staged / "package-lock.json"
        lock = load(lock_path, {})
        entry = lock.get("packages", {}).get("node_modules/@fission-ai/openspec", {})
        if installed.get("version") != package["version"] or entry.get("integrity") != package["integrity"]:
            raise ValueError(f"Installed OpenSpec did not match resolved version/integrity: {package['version']}")
        staged.rename(prefix)
    return {**package, "cache": str(prefix.relative_to(state)),
            "lock_sha256": hashlib.sha256((prefix / "package-lock.json").read_bytes()).hexdigest()}


def prepare(state, manifest, stage, resolved):
    for name in manifest["local_skills"]:
        shutil.copytree(ROOT / "skills" / name, stage / name)
    for name, source in manifest["sources"].items():
        upstream = fetch_source(state, name, source, resolved["sources"][name])
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
    return prepare_openspec(state, resolved["openspec"])


def migrate_legacy_registry(state, manifest, registry, host, require_cache=True):
    if not registry or registry.get("schema") == 2:
        return registry
    legacy = state / "npm"
    package = load(legacy / "node_modules/@fission-ai/openspec/package.json", {})
    lock_path = legacy / "package-lock.json"
    lock = load(lock_path, {})
    entry = lock.get("packages", {}).get("node_modules/@fission-ai/openspec", {})
    version, integrity = package.get("version"), entry.get("integrity")
    cache_valid = (stable_version(version) and isinstance(integrity, str)
                   and SRI_RE.fullmatch(integrity) and lock_path.is_file())
    if not cache_valid and require_cache:
        raise ValueError("Existing installation uses a legacy receipt without a verifiable OpenSpec cache; no host files changed. Keep its backup and resolve the old cache before setup.")
    migrated = json.loads(json.dumps(registry))
    migrated.update({
        "schema": 2,
        "resolved": {"legacy": True, "sources": {}},
    })
    if cache_valid:
        migrated["openspec"] = {"package": manifest["openspec"]["package"], "registry": manifest["openspec"]["registry"],
                                 "version": version, "integrity": integrity, "cache": "npm",
                                 "lock_sha256": hashlib.sha256(lock_path.read_bytes()).hexdigest()}
    else:
        migrated.pop("openspec", None)
    hosts = set(migrated.get("hosts", []))
    for raw_path in migrated.get("skills", {}):
        path = Path(raw_path)
        home = state.parents[2]
        if path.parent == home / ".agents/skills":
            hosts.add("codex")
        elif path.parent == home / ".claude/skills":
            hosts.add("claude")
    if not hosts:
        hosts.update(["codex", "claude"] if host == "both" else [host])
    migrated["hosts"] = sorted(hosts)
    policies = migrated.setdefault("policy_blocks", {})
    home = state.parents[2]
    for name, relative in (("codex", ".codex/AGENTS.md"), ("claude", ".claude/CLAUDE.md")):
        path = home / relative
        if name in hosts and path.is_file() and not path.is_symlink():
            digest = block_hash(path.read_text())
            if digest:
                policies[str(path)] = digest
    return migrated


def install_plan(args, manifest, registry):
    hosts = ["codex", "claude"] if args.host == "both" else [args.host]
    errors = conflicts(args.home, manifest, registry, hosts)
    destinations = [args.home / (".agents/skills" if h == "codex" else ".claude/skills") for h in hosts]
    instructions = [args.home / (".codex/AGENTS.md" if h == "codex" else ".claude/CLAUDE.md") for h in hosts]
    source_names = [n for s in manifest["sources"].values() for n in s["skills"]]
    names = source_names if args.native_plugin else manifest["local_skills"] + source_names
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
    return hosts, destinations, instructions, names, stale, blocks


def apply_install(args, manifest, state, registry, resolved, stage, openspec, plan, native_backup=None):
    hosts, destinations, instructions, names, stale, blocks = plan
    private_dir(state / "backups")
    backup = private_dir(state / "backups" / str(time.time_ns()))
    old_registry = json.loads(json.dumps(registry))
    targets = []
    for index, dest in enumerate(stale):
        previous = backup / f"obsolete-{index}-{dest.name}"
        targets.append({"kind": "skill", "target": str(dest), "backup": str(previous) if dest.exists() else None,
                        "existed": dest.exists(), "modes": tree_modes(dest) if dest.exists() else {},
                        "expected_after": None})
    for host_index, base in enumerate(destinations):
        for skill_index, name in enumerate(names):
            dest = base / name
            previous = backup / f"{host_index}-{name}"
            targets.append({"kind": "skill", "target": str(dest), "backup": str(previous) if dest.exists() else None,
                            "existed": dest.exists(), "modes": tree_modes(dest) if dest.exists() else {},
                            "expected_after": hashes(stage / name)})
    for index, path in enumerate(instructions):
        previous = backup / f"instructions-{index}.md"
        existed = path.exists()
        modes = tree_modes(path) if existed else {}
        if existed:
            private_copy(path, previous)
        targets.append({"kind": "policy", "target": str(path), "backup": str(previous) if existed else None,
                        "existed": existed, "modes": modes,
                        "expected_after": block_hash(blocks[path])})
    transaction = {"previous_registry": old_registry, "targets": targets,
                   "native_backup": str(native_backup) if native_backup else None}
    write_json(backup / "transaction.json", transaction)
    pending_path = state / "pending.json"
    pending = load(pending_path, {})
    pending.update({"status": "installing", "resolved": resolved, "openspec": openspec,
                    "backup": str(backup), "native_backup": str(native_backup) if native_backup else None})
    write_json(pending_path, pending)

    saved = []
    try:
        for entry in targets:
            dest = Path(entry["target"])
            previous = Path(entry["backup"]) if entry["backup"] else None
            existed = entry["existed"]
            if entry["kind"] == "skill":
                saved.append((dest, previous, existed, True, entry["modes"]))
                if previous and existed:
                    previous.parent.mkdir(parents=True, exist_ok=True)
                    dest.rename(previous)
                    private_tree(previous)
                if entry["expected_after"] is None:
                    registry.setdefault("skills", {}).pop(str(dest), None)
                    continue
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(stage / dest.name, dest)
                registry.setdefault("skills", {})[str(dest)] = hashes(dest)
            else:
                path = dest
                if existed:
                    saved_path = previous
                    saved.append((path, saved_path, True, False, entry["modes"]))
                else:
                    saved.append((path, None, False, False, {}))
                path.parent.mkdir(parents=True, exist_ok=True)
                write_text_atomic(path, blocks[path], entry["modes"].get(".", 0o644) if existed else 0o644)

        registry.update({
            "schema": 2,
            "manifest_sha256": hashlib.sha256((ROOT / "manifest.json").read_bytes()).hexdigest(),
            "repository": str(ROOT),
            "mode": "native-plugin" if args.native_plugin else "standalone",
            "hosts": hosts,
            "installed_at": datetime.now(timezone.utc).isoformat(),
            "resolved": resolved,
            "openspec": openspec,
            "previous_backup": str(backup),
            "native_backup": str(native_backup) if native_backup else old_registry.get("native_backup"),
            "policy_blocks": {str(path): block_hash(blocks[path]) for path in instructions},
        })
        write_json(state / "installed.json", registry)
        pending_path.unlink(missing_ok=True)
    except BaseException as error:
        rollback_errors = []
        for dest, previous, existed, directory, modes in reversed(saved):
            try:
                previous_exists = bool(previous and previous.exists())
                if existed and previous_exists:
                    if dest.exists() or dest.is_symlink():
                        if directory and not dest.is_symlink():
                            shutil.rmtree(dest)
                        else:
                            dest.unlink()
                    if directory:
                        shutil.copytree(previous, dest, symlinks=True)
                    else:
                        shutil.copy2(previous, dest)
                    restore_modes(dest, modes)
                elif existed:
                    if not dest.exists() and not dest.is_symlink():
                        rollback_errors.append(f"{dest}: original item and backup are both missing")
                elif dest.exists() or dest.is_symlink():
                    if directory and not dest.is_symlink():
                        shutil.rmtree(dest)
                    else:
                        dest.unlink()
            except OSError as restore_error:
                rollback_errors.append(f"{dest}: {restore_error}")
        registry.clear()
        registry.update(old_registry)
        try:
            write_json(state / "installed.json", old_registry)
        except OSError as restore_error:
            rollback_errors.append(f"installed receipt: {restore_error}")
        if rollback_errors:
            pending.update({"status": "recovery_required", "errors": rollback_errors})
            write_json(pending_path, pending)
            raise ValueError(f"Install failed ({error}); rollback incomplete; affected items: {'; '.join(rollback_errors)}; backup: {backup}") from error
        pending_path.unlink(missing_ok=True)
        raise
    print("Installed. Backups:", backup)
    print("Restart Codex/Claude. Run doctor from inside each project before development.")


def install(args, manifest, state, registry, resolved=None, stage=None, openspec=None, native_backup=None):
    registry = migrate_legacy_registry(state, manifest, registry, args.host)
    plan = install_plan(args, manifest, registry)
    hosts, _, instructions, names, _, _ = plan
    resolved = resolved or resolve_dependencies(manifest)
    print("Hosts:", ", ".join(hosts))
    print("Skills:", ", ".join(names))
    print("Instruction files:", ", ".join(str(p) for p in instructions))
    print_resolved(resolved)
    if args.dry_run:
        print("Dry run: no downloads, installs or host/state writes.")
        return
    for tool in ["git", "node", "npm"]:
        if not shutil.which(tool):
            raise ValueError(f"Install prerequisite first: {tool}")
    version = tuple(int(x) for x in run("node", "--version").lstrip("v").split(".")[:3])
    if version < (20, 19, 0):
        raise ValueError("Node.js >=20.19.0 is required")
    state.mkdir(parents=True, exist_ok=True)
    if stage is not None:
        openspec = openspec or prepare_openspec(state, resolved["openspec"])
        return apply_install(args, manifest, state, registry, resolved, stage, openspec, plan, native_backup)
    with tempfile.TemporaryDirectory(dir=state) as temp:
        stage = Path(temp) / "skills"
        stage.mkdir()
        openspec = prepare(state, manifest, stage, resolved)
        return apply_install(args, manifest, state, registry, resolved, stage, openspec, plan, native_backup)


def setup(args, manifest, state, registry):
    for tool in ["git", "node", "npm"]:
        if not shutil.which(tool):
            raise ValueError(f"Install prerequisite first: {tool}")
    version = tuple(int(x) for x in run("node", "--version").lstrip("v").split(".")[:3])
    if version < (20, 19, 0):
        raise ValueError("Node.js >=20.19.0 is required")
    backup = args.home / ".local/share/grounded/migration-backups" / str(time.time_ns())
    args.native_plugin = True
    if args.dry_run:
        resolved = resolve_dependencies(manifest)
        print_resolved(resolved)
        native_conflicts(args, manifest, registry, backup)
        print("Grounded dependencies and shared rules will be installed; no downloads, installs or host/state writes.")
        return
    state.mkdir(parents=True, exist_ok=True)
    lock_path = state / "install.lock"
    with lock_path.open("w") as lock:
        lock_path.chmod(0o600)
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if (state / "pending.json").exists():
            raise ValueError(f"A prior setup is pending recovery. Run restore --host {args.host} --dry-run and inspect its backup before continuing.")
        resolved = resolve_dependencies(manifest)
        print_resolved(resolved)
        current_registry = load(state / "installed.json", {})
        current_registry = migrate_legacy_registry(state, manifest, current_registry, args.host)
        print_previous(current_registry)
        with tempfile.TemporaryDirectory(dir=state) as temp:
            stage = Path(temp) / "skills"
            stage.mkdir()
            openspec = prepare(state, manifest, stage, resolved)
            pending_path = state / "pending.json"
            write_json(pending_path, {"status": "prepared", "resolved": resolved, "openspec": openspec,
                                      "previous": current_registry, "native_backup": str(backup)})
            snapshot = None
            try:
                snapshot = native_conflicts(args, manifest, current_registry, backup)
                install(args, manifest, state, load(state / "installed.json", {}), resolved,
                        stage, openspec, snapshot)
            except BaseException as error:
                if snapshot:
                    try:
                        restore_native_conflicts(snapshot, args)
                    except (OSError, ValueError, subprocess.SubprocessError) as restore_error:
                        pending = load(pending_path, {})
                        pending.update({"status": "recovery_required", "error": str(restore_error),
                                        "native_backup": str(snapshot)})
                        write_json(pending_path, pending)
                        raise ValueError(f"Setup failed ({error}); automatic recovery was incomplete ({restore_error}); backup: {snapshot}") from error
                elif "recovery incomplete" in str(error).lower():
                    pending = load(pending_path, {})
                    pending.update({"status": "recovery_required", "error": str(error),
                                    "native_backup": str(backup)})
                    write_json(pending_path, pending)
                if not load(pending_path, {}).get("status") == "recovery_required":
                    pending_path.unlink(missing_ok=True)
                raise
    print("Grounded setup complete. Existing overlapping skills and plugin data are backed up at:", snapshot or "none")


def configure(args, state):
    print("Grounded policy version:", load(ROOT / "plugin.json")["version"])
    hosts = ["codex", "claude"] if args.host == "both" else [args.host]
    paths = [args.home / (".codex/AGENTS.md" if host == "codex" else ".claude/CLAUDE.md") for host in hosts]
    blocks = {path: rule_text(path) for path in paths}
    changes = {path: content for path, content in blocks.items()
               if not path.exists() or path.read_text() != content}
    for path in changes:
        print("Configure policy:", path)
    if args.dry_run:
        print("Dry run: no instruction files changed")
        return
    if not changes:
        print("Shared policy is already current")
        return
    backup = private_dir(state / "backups" / str(time.time_ns()))
    saved = []
    try:
        for index, (path, content) in enumerate(changes.items()):
            path.parent.mkdir(parents=True, exist_ok=True)
            previous = backup / f"instructions-{index}.md"
            existed = path.exists()
            modes = tree_modes(path) if existed else {}
            if existed:
                private_copy(path, previous)
            saved.append((path, previous, existed, modes))
            path.write_text(content)
    except BaseException:
        for path, previous, existed, modes in reversed(saved):
            if existed:
                shutil.copy2(previous, path)
                restore_modes(path, modes)
            elif path.exists():
                path.unlink()
        raise
    print("Shared policy configured. Backups:", backup)
    print("Start a new Codex/Claude conversation to load the updated instructions.")


def doctor(args, manifest, state, registry):
    hosts = ["codex", "claude"] if args.host == "both" else [args.host]
    errors = conflicts(args.home, manifest, registry, hosts)
    source_names = [n for s in manifest["sources"].values() for n in s["skills"]]
    names = source_names if registry.get("mode") == "native-plugin" else manifest["local_skills"] + source_names
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
    package_receipt = registry.get("openspec", {})
    prefix = state / package_receipt.get("cache", "")
    package = load(prefix / "node_modules/@fission-ai/openspec/package.json", {})
    lock_path = prefix / "package-lock.json"
    lock = load(lock_path, {})
    entry = lock.get("packages", {}).get("node_modules/@fission-ai/openspec", {})
    if (package.get("version") != package_receipt.get("version")
            or entry.get("integrity") != package_receipt.get("integrity")
            or not lock_path.is_file()
            or hashlib.sha256(lock_path.read_bytes()).hexdigest() != package_receipt.get("lock_sha256")):
        raise ValueError("Receipt OpenSpec cache is missing or failed version/integrity verification")
    print("Managed skills, policy, resolved dependency receipt and known overlap checks: passed")
    print("Project-specific prose, nonstandard skill/plugin paths and actual agent behavior still require review.")


def inside(path, roots):
    candidate = path.resolve(strict=False)
    return any(candidate.is_relative_to(root.resolve(strict=False)) for root in roots)


def managed_policy_path(path, home):
    return path in {home / ".codex/AGENTS.md", home / ".claude/CLAUDE.md"}


def restore_install(args, state, registry):
    pending_path = state / "pending.json"
    pending = load(pending_path, {})
    if pending.get("status") == "uninstalling" or (
        pending.get("status") == "recovery_required" and pending.get("backup")
        and (Path(pending["backup"]) / "installed.json").is_file()
        and not (Path(pending["backup"]) / "transaction.json").is_file()
    ):
        raise ValueError(f"An uninstall is incomplete. Resume it with uninstall --host {args.host}; inspect {pending.get('backup', pending_path)}")
    backup_value = pending.get("backup") if pending.get("status") in {"installing", "restoring", "recovery_required"} else None
    recovering_pending = bool(backup_value)
    if pending.get("status") == "prepared" or (pending.get("status") == "recovery_required" and not backup_value):
        native_value = pending.get("native_backup")
        native_root = args.home / ".local/share/grounded/migration-backups"
        native = Path(native_value).resolve() if native_value else None
        if not native or not inside(native, [native_root]):
            raise ValueError(f"Pending setup state requires manual recovery; inspect {pending_path} and its recorded backup")
        print("Pending native conflict migration:", native)
        if args.dry_run:
            print("Dry run: no plugin or skill state changed" if not (native / "migration.json").is_file()
                  else "Dry run: restore the recorded native conflict state")
            return
        if (native / "migration.json").is_file():
            restore_native_conflicts(native, args)
        pending_path.unlink(missing_ok=True)
        print("Pending native state cleared. Backup retained:", native if native.exists() else "none")
        return
    backup_value = backup_value or registry.get("previous_backup")
    if not backup_value:
        raise ValueError("No previous installation snapshot is recorded")
    backup = Path(backup_value).resolve()
    if not inside(backup, [state / "backups"]):
        raise ValueError(f"Refusing to read restore snapshot outside managed backups: {backup}")
    transaction = load(backup / "transaction.json")
    if not isinstance(transaction, dict):
        raise ValueError(f"Restore snapshot is missing or invalid: {backup}")
    previous = transaction.get("previous_registry", {})
    targets = transaction.get("targets", [])
    errors, skipped, actions = [], [], []
    skill_roots = [args.home / ".agents/skills", args.home / ".codex/skills", args.home / ".claude/skills"]
    for entry in targets:
        target = Path(entry["target"])
        if entry["kind"] == "skill":
            if not inside(target, skill_roots):
                errors.append(f"Refusing to alter skill outside managed host roots: {target}")
                continue
            expected = entry.get("expected_after")
            if expected is None:
                if target.exists() or target.is_symlink():
                    skipped.append(f"Preserved new/unmanaged path: {target}")
                elif entry.get("existed"):
                    saved_path = Path(entry["backup"]) if entry.get("backup") else None
                    if not saved_path or not inside(saved_path, [backup]) or not saved_path.exists():
                        errors.append(f"Required skill backup is missing or outside transaction: {saved_path}")
                    else:
                        actions.append(("restore-skill", entry, target))
                continue
            saved_path = Path(entry["backup"]) if entry.get("backup") else None
            if entry.get("existed") and (not saved_path or not inside(saved_path, [backup]) or not saved_path.exists()):
                errors.append(f"Required skill backup is missing or outside transaction: {saved_path}")
                continue
            if (entry.get("existed") and target.is_dir() and not target.is_symlink()
                    and saved_path and hashes(target) == hashes(saved_path)):
                continue
            if not target.exists() and not target.is_symlink() and entry.get("existed") and recovering_pending:
                actions.append(("restore-skill", entry, target))
                continue
            if target.is_symlink() or not target.is_dir() or hashes(target) != expected:
                skipped.append(f"Preserved changed managed skill: {target}")
                continue
            actions.append(("restore-skill", entry, target))
        elif entry["kind"] == "policy":
            if not managed_policy_path(target, args.home):
                errors.append(f"Refusing to alter unrecognized policy path: {target}")
                continue
            if target.is_symlink():
                skipped.append(f"Preserved symlink policy path: {target}")
                continue
            saved_path = Path(entry["backup"]) if entry.get("backup") else None
            if entry.get("existed") and (not saved_path or not inside(saved_path, [backup]) or not saved_path.is_file()):
                errors.append(f"Required policy backup is missing or outside transaction: {saved_path}")
                continue
            current_text = target.read_text() if target.is_file() else ""
            old_text = saved_path.read_text() if saved_path and saved_path.is_file() else ""
            old_block = managed_block(old_text)
            if old_block and managed_block(current_text) == old_block:
                continue
            if block_hash(current_text) != entry.get("expected_after"):
                skipped.append(f"Preserved edited managed policy block: {target}")
                continue
            actions.append(("restore-policy", entry, target))
        else:
            errors.append(f"Unknown restore target type: {entry.get('kind')}")
    if errors:
        raise ValueError("Restore preflight failed: " + "; ".join(errors))
    print("Restore target:", "previous installation" if previous else "pre-install state")
    for _, _, path in actions:
        print("Restore:", path)
    for message in skipped:
        print(message)
    native_backup = transaction.get("native_backup") or registry.get("native_backup")
    if args.dry_run:
        print("Dry run: no files or plugin state changed; retained snapshot:", backup)
        return
    write_json(pending_path, {"status": "restoring", "backup": str(backup), "previous": previous})
    completed = []
    try:
        for kind, entry, target in actions:
            saved = Path(entry["backup"]) if entry.get("backup") else None
            if saved and not inside(saved, [backup]):
                raise ValueError(f"Refusing to read restore file outside transaction: {saved}")
            if kind == "restore-skill":
                if target.exists():
                    shutil.rmtree(target)
                if entry.get("existed"):
                    if not saved or not saved.exists():
                        raise ValueError(f"Required skill backup is missing: {saved}")
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(saved, target, symlinks=True)
                    restore_modes(target, entry.get("modes", {}))
            else:
                old_text = saved.read_text() if saved and saved.is_file() else ""
                old_block = managed_block(old_text)
                current_text = target.read_text() if target.exists() else ""
                updated = replace_managed_block(current_text, old_block)
                if updated.strip() or entry.get("existed"):
                    target.parent.mkdir(parents=True, exist_ok=True)
                    write_text_atomic(target, updated, entry.get("modes", {}).get(".", 0o644))
                    if entry.get("existed"):
                        restore_modes(target, entry.get("modes", {}))
                else:
                    target.unlink(missing_ok=True)
            completed.append(str(target))
        if native_backup:
            restore_native_conflicts(native_backup, args)
        write_json(state / "installed.json", previous)
        pending_path.unlink(missing_ok=True)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        write_json(pending_path, {"status": "recovery_required", "backup": str(backup),
                                  "completed": completed, "error": str(error)})
        raise ValueError(f"Restore incomplete: {error}; completed: {', '.join(completed) or 'none'}; backup: {backup}") from error
    print("Restore complete. Backups retained:", backup)


def uninstall(args, state, registry, manifest):
    pending_path = state / "pending.json"
    pending = load(pending_path, {})
    existing_backup = None
    if pending.get("status") in {"uninstalling", "recovery_required"} and pending.get("backup"):
        candidate = Path(pending["backup"]).resolve()
        if inside(candidate, [state / "backups"]) and (candidate / "installed.json").is_file():
            registry = load(candidate / "installed.json", registry)
            existing_backup = candidate
        else:
            raise ValueError(f"Pending operation is not a resumable uninstall; recover it first using {pending.get('backup')}")
    elif pending:
        raise ValueError(f"A different operation is pending recovery; use restore --host {args.host} --dry-run first")
    registry = migrate_legacy_registry(state, manifest, registry, args.host, require_cache=False)
    if not registry:
        print("Grounded has no recorded installation to uninstall")
        return
    skill_roots = [args.home / ".agents/skills", args.home / ".codex/skills", args.home / ".claude/skills"]
    actions, preserved = [], []
    for raw_path, expected in registry.get("skills", {}).items():
        path = Path(raw_path)
        if not inside(path, skill_roots):
            preserved.append(f"Unrecognized managed path preserved: {path}")
        elif not path.exists() and not path.is_symlink():
            continue
        elif path.is_dir() and not path.is_symlink() and hashes(path) == expected:
            actions.append(("skill", path))
        else:
            preserved.append(f"Edited or missing managed skill preserved: {path}")
    for raw_path, expected in registry.get("policy_blocks", {}).items():
        path = Path(raw_path)
        if not managed_policy_path(path, args.home):
            preserved.append(f"Unrecognized policy path preserved: {path}")
            continue
        text = path.read_text() if path.is_file() and not path.is_symlink() else ""
        if path.is_symlink():
            preserved.append(f"Symlink policy path preserved: {path}")
        elif not path.exists():
            continue
        elif block_hash(text) == expected:
            actions.append(("policy", path))
        else:
            preserved.append(f"Edited managed policy block preserved: {path}")
    print("Uninstall:")
    for _, path in actions:
        print("  ", path)
    for message in preserved:
        print(message)
    native_backup = registry.get("native_backup")
    if args.dry_run:
        print("Dry run: no host/state changes; backups retained")
        return
    backup = existing_backup or private_dir(state / "backups" / f"uninstall-{time.time_ns()}")
    if not existing_backup:
        write_json(backup / "installed.json", registry)
    write_json(pending_path, {"status": "uninstalling", "backup": str(backup)})
    errors = []
    for kind, path in actions:
        try:
            if kind == "skill":
                shutil.rmtree(path)
            else:
                text = path.read_text()
                updated = replace_managed_block(text, None)
                if updated.strip():
                    write_text_atomic(path, updated, stat.S_IMODE(path.stat().st_mode))
                else:
                    path.unlink(missing_ok=True)
        except OSError as error:
            errors.append(f"{path}: {error}")
    if native_backup:
        try:
            restore_native_conflicts(native_backup, args)
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            errors.append(f"native plugin/skill recovery: {error}")
    write_json(backup / "result.json", {"preserved": preserved, "errors": errors,
                                         "removed": [str(path) for _, path in actions if not any(str(path) in item for item in errors)]})
    if errors:
        write_json(pending_path, {"status": "recovery_required", "backup": str(backup), "errors": errors})
        raise ValueError("Uninstall incomplete: " + "; ".join(errors) + f"; backup: {backup}")
    (state / "installed.json").unlink(missing_ok=True)
    pending_path.unlink(missing_ok=True)
    print("Uninstall complete. Preserved paths are listed above. Backups retained:", backup)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["setup", "install", "configure", "doctor", "restore", "uninstall", "check", "openspec"])
    parser.add_argument("--host", choices=["codex", "claude", "both"], default="both")
    parser.add_argument("--home", type=Path, default=Path.home(), help="Installation home (default: current user's home)")
    parser.add_argument("--project", type=Path, help="Project path for doctor or OpenSpec")
    parser.add_argument("--dry-run", action="store_true", help="Preview installation or configuration; no writes/downloads")
    args, extra = parser.parse_known_args()
    if extra and args.command != "openspec":
        parser.error("Unexpected arguments: " + " ".join(extra))
    args.home = args.home.expanduser().resolve()
    if args.command in {"setup", "install", "configure", "doctor", "restore", "uninstall", "openspec"} and args.home == Path.home().resolve():
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
    elif args.command in {"setup", "install", "configure", "restore", "uninstall"}:
        def apply_configuration():
            if args.command == "setup":
                setup(args, manifest, state, registry)
            elif args.command == "configure":
                configure(args, state)
            elif args.command == "restore":
                restore_install(args, state, load(state / "installed.json", {}))
            elif args.command == "uninstall":
                uninstall(args, state, load(state / "installed.json", {}), manifest)
            else:
                if (state / "pending.json").exists():
                    raise ValueError(f"A prior setup is pending recovery. Run restore --host {args.host} --dry-run first.")
                args.native_plugin = False
                install(args, manifest, state, load(state / "installed.json", {}))
        if args.dry_run:
            apply_configuration()
        elif args.command == "setup":
            apply_configuration()
        else:
            state.mkdir(parents=True, exist_ok=True)
            with (state / "install.lock").open("w") as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                apply_configuration()
    elif args.command == "doctor":
        doctor(args, manifest, state, registry)
    else:
        receipt = registry.get("openspec", {})
        prefix = (state / receipt.get("cache", "")).resolve()
        if not inside(prefix, [state / "npm-versions", state / "npm"]):
            raise ValueError("Run install first; resolved OpenSpec cache is missing from the receipt")
        lock_path = prefix / "package-lock.json"
        lock = load(lock_path, {})
        package = load(prefix / "node_modules/@fission-ai/openspec/package.json", {})
        integrity = lock.get("packages", {}).get("node_modules/@fission-ai/openspec", {}).get("integrity")
        if (package.get("version") != receipt.get("version") or integrity != receipt.get("integrity")
                or not lock_path.is_file()
                or hashlib.sha256(lock_path.read_bytes()).hexdigest() != receipt.get("lock_sha256")):
            raise ValueError("OpenSpec cache failed receipt verification")
        binary = prefix / "node_modules/.bin/openspec"
        if not binary.exists():
            raise ValueError("Resolved OpenSpec executable is missing")
        extra = extra[1:] if extra[:1] == ["--"] else extra
        subprocess.run([str(binary), *extra], cwd=args.project, check=True)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
