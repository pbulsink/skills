#!/usr/bin/env python3
"""
Keep .claude-plugin/marketplace.json consistent with the skills in this repository.

This repo is distributed as ONE plugin ("skills") that bundles many skills: every
immediate subfolder of the repo root containing a SKILL.md is one skill, and Claude Code
discovers them all because plugin.json sets "skills": ".". The marketplace therefore lists
a single entry named "skills" with source "./".

This script reconciles that single entry with reality:
  - ensures the "skills" entry exists (adds it if missing)
  - refreshes its description from README.md when present, else falls back to a default
  - keeps its version in sync with plugin.json's version
  - reports every skill folder found so you can confirm nothing was missed

Usage:
    sync_marketplace.py [--root PATH] [--dry-run]

Options:
    --root PATH   Repository root (default: the directory two levels above this script,
                  i.e. the repo that contains .claude-plugin/).
    --dry-run     Print what would change without writing anything.
"""

import argparse
import json
import re
import sys
from pathlib import Path


PLUGIN_NAME = "skills"  # must match plugin.json's name and the marketplace entry name
DEFAULT_DESCRIPTION = (
    "A collection of agent skills for R package development, GitHub workflows, "
    "code and plan review, and skill authoring."
)


def find_repo_root(start: Path) -> Path:
    """Walk up from `start` to the directory containing .claude-plugin/marketplace.json."""
    for candidate in [start, *start.parents]:
        if (candidate / ".claude-plugin" / "marketplace.json").is_file():
            return candidate
    raise SystemExit("Could not locate a repository root with .claude-plugin/marketplace.json")


def discover_skills(root: Path) -> list[str]:
    """Names of every immediate subfolder that contains a SKILL.md."""
    names = []
    for entry in sorted(root.iterdir()):
        if entry.is_dir() and not entry.name.startswith(".") and (entry / "SKILL.md").is_file():
            names.append(entry.name)
    return names


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None


def readme_description(root: Path) -> str | None:
    """First non-empty line of the README, used as a marketplace description when available."""
    readme = root / "README.md"
    if not readme.is_file():
        return None
    for line in readme.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if text and not text.startswith("#"):
            return text
    return None


def sync(root: Path, dry_run: bool) -> None:
    marketplace_path = root / ".claude-plugin" / "marketplace.json"
    plugin_path = root / ".claude-plugin" / "plugin.json"

    data = read_json(marketplace_path) or {}
    plugin = read_json(plugin_path) or {}

    skills = discover_skills(root)
    plugins = data.setdefault("plugins", [])
    entry = next((p for p in plugins if isinstance(p, dict) and p.get("name") == PLUGIN_NAME), None)

    changes: list[str] = []

    # Ensure the single "skills" entry exists.
    if entry is None:
        entry = {"name": PLUGIN_NAME, "source": "./"}
        plugins.append(entry)
        changes.append(f"+ added '{PLUGIN_NAME}' entry")

    # Keep source pointing at the repo root.
    if entry.get("source") != "./":
        entry["source"] = "./"
        changes.append("+ set source to './'")

    # Refresh description: prefer README, fall back to default.
    desc = readme_description(root) or DEFAULT_DESCRIPTION
    if entry.get("description") != desc:
        entry["description"] = desc
        changes.append("~ refreshed description")

    # Keep version in sync with plugin.json (only when the manifest sets one).
    pv = plugin.get("version")
    if pv and entry.get("version") != pv:
        entry["version"] = pv
        changes.append(f"~ synced version to {pv}")

    if dry_run:
        print("Dry run — no files written.")
        for c in changes:
            print(f"  {c}")
        if not changes:
            print("  marketplace.json is already in sync")
        print(f"\nDiscovered {len(skills)} skill folder(s):")
        for name in skills:
            print(f"  - {name}")
        return

    marketplace_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    if changes:
        for c in changes:
            print(f"  {c}")
    else:
        print("marketplace.json already in sync.")
    print(f"\nDiscovered {len(skills)} skill folder(s):")
    for name in skills:
        print(f"  - {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    default_root = Path(__file__).resolve().parent.parent.parent
    parser.add_argument("--root", type=Path, default=default_root)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = find_repo_root(args.root.resolve())
    sync(root, args.dry_run)


if __name__ == "__main__":
    main()
