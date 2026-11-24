#!/usr/bin/env python3
"""Show the Grounded versions recorded in the user's local setup."""

import argparse
import json
from pathlib import Path
import re

BEGIN = "<!-- skills-environment:begin -->"
END = "<!-- skills-environment:end -->"


def managed_block(text):
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        return None
    start = text.index(BEGIN)
    end = text.index(END)
    if start > end:
        return None
    return text[start:end + len(END)]


def print_installed_versions(home, host):
    policies = {"codex": ("Codex", ".codex/AGENTS.md"), "claude": ("Claude", ".claude/CLAUDE.md")}
    for label, relative in policies.values() if host == "both" else [policies[host]]:
        path = home / relative
        block = managed_block(path.read_text()) if path.is_file() else None
        match = re.search(r"(?m)^<!-- grounded-version: ([^ ]+) -->$", block or "")
        print(f"Applied {label} policy: {match[1] if match else 'not configured'}")

    path = home / ".local/share/skills-environment/installed.json"
    receipt = json.loads(path.read_text()) if path.is_file() else {}
    if not receipt:
        print("No shared installation receipt.")
        return

    print("Latest shared installation receipt:")
    for name, item in receipt.get("resolved", {}).get("sources", {}).items():
        print(f"  {name}: {item.get('version', 'unknown')} ({item.get('commit', 'unknown')[:12]})")
    for name, item in receipt.get("resolved", {}).get("tools", {}).items():
        print(f"  {name}: {item.get('version', 'unknown')} ({item.get('asset', 'unknown')})")
    if package := receipt.get("openspec"):
        print(f"  openspec: {package.get('version', 'unknown')}")


def main():
    parser = argparse.ArgumentParser(prog="grounded", description=__doc__)
    parser.add_argument("-v", "--version", action="store_true", help="Show installed versions (default)")
    parser.add_argument("--host", choices=("codex", "claude", "both"), default="both")
    parser.add_argument("--home", type=Path, default=Path.home())
    args = parser.parse_args()
    try:
        print_installed_versions(args.home.expanduser(), args.host)
    except (OSError, ValueError) as error:
        parser.exit(1, f"grounded: {error}\n")


if __name__ == "__main__":
    main()
