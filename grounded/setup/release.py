#!/usr/bin/env python3
"""Synchronize Grounded plugin versions and build a tag-validated release ZIP."""
import argparse
import json
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"


def manifests(root):
    paths = [root / "plugin.json", root / ".claude-plugin/plugin.json"]
    values = [json.loads(path.read_text()) for path in paths]
    if any(value.get("name") != "grounded" for value in values):
        raise ValueError("Both plugin manifests must name grounded")
    return list(zip(paths, values))


def bump(root, version):
    if not re.fullmatch(VERSION, version):
        raise ValueError("Version must be MAJOR.MINOR.PATCH without leading zeros")
    entries = manifests(root)
    for path, data in entries:
        data["version"] = version
        path.write_text(json.dumps(data, indent=2) + "\n")


def package(root, tag, output):
    entries = manifests(root)
    version = entries[0][1].get("version", "")
    if not re.fullmatch(VERSION, version):
        raise ValueError("Canonical plugin version must be MAJOR.MINOR.PATCH")
    if any(data.get("version") != version for _, data in entries):
        raise ValueError("Codex and Claude plugin versions differ; run release.py bump")
    if tag != f"skills-v{version}":
        raise ValueError(f"Tag {tag!r} does not match plugin version; expected skills-v{version}")
    if output.resolve().is_relative_to(root.resolve()):
        raise ValueError("Write the release ZIP outside the plugin directory")
    files = [path for path in sorted(root.rglob("*"))
             if path.is_file() and "__pycache__" not in path.parts
             and path.suffix != ".pyc" and path.name != ".DS_Store"]
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(root))
        license_file = root.parent / "LICENSE"
        if license_file.is_file() and not (root / "LICENSE").exists():
            archive.write(license_file, "LICENSE")
    return version


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("bump").add_argument("version")
    build = sub.add_parser("package")
    build.add_argument("--tag", required=True)
    build.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "bump":
        bump(ROOT, args.version)
        print("Codex and Claude versions synchronized:", args.version)
    else:
        version = package(ROOT, args.tag, args.output)
        print(f"Grounded {version}: {args.output}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, zipfile.BadZipFile) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
