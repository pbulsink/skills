---
name: maintain-plugin
description: This skill should be used when adding a new skill to this repository, removing one, or otherwise changing which skills exist, so that .claude-plugin/marketplace.json and the README stay in sync with the skills on disk. Triggers on requests like "add a skill", "register this skill in the marketplace", "I added a new skill, update the docs", or "remove a skill from the plugin". Keeps the Claude Code plugin manifest consistent as the collection of skills grows over time.
---

# Maintain Plugin

Keep the Claude Code plugin for this repository consistent with the skills that actually exist on disk. The repo is distributed as **one plugin** ("skills") that bundles many skills: every immediate subfolder of the repo root containing a `SKILL.md` is one skill, and Claude Code discovers them all because `plugin.json` sets `"skills": "."`. The marketplace therefore lists a single entry named `skills` with `source: "./"`, and each skill must also be documented in `README.md`.

## When to use this skill

- A new skill folder (with a `SKILL.md`) has been added.
- A skill has been renamed or removed.
- The user asks to "register", "publish", or "add" a skill to the plugin/marketplace.
- After any change, to verify the manifest and README match reality.

## Repository layout (source of truth)

```
<repo-root>/
├── .claude-plugin/
│   ├── plugin.json          # plugin manifest — name, version, author, skills: "."
│   └── marketplace.json     # lists every skill as a plugins[] entry with source "./"
├── <skill-name>/SKILL.md     # one folder per skill (this is what gets discovered)
├── README.md                # human-facing catalog of the skills
└── AGENTS.md
```

Because `plugin.json` sets `"skills": "."`, Claude Code discovers every top-level `<name>/SKILL.md` automatically — adding a skill folder is enough for the plugin to load it. The files that need upkeep are **marketplace.json** (machine-readable; keep its single entry and version in sync) and **README.md** (human-readable catalog).

## Workflow

### 1. Add or remove the skill folder

- To add: create `<repo-root>/<skill-name>/SKILL.md` with valid YAML front-matter (`name`, `description`; optionally `trigger`). The folder name must equal the front-matter `name`.
- To remove: delete the whole `<skill-name>/` directory.

### 2. Sync marketplace.json (deterministic)

Run the bundled script to reconcile `marketplace.json` with the repo. It ensures the single `skills` entry exists, keeps its `source` at `./`, refreshes its description from the README, and syncs its version with `plugin.json`. It also prints every skill folder it discovered so you can confirm nothing was missed:

```bash
python3 maintain-plugin/scripts/sync_marketplace.py            # apply changes
python3 maintain-plugin/scripts/sync_marketplace.py --dry-run   # preview only
```

The script locates the repo root by walking up to the directory containing `.claude-plugin/marketplace.json`, so it works from any working directory. The entry it maintains looks like:

```json
{ "name": "skills", "source": "./", "description": "...", "version": "1.0.0" }
```

### 3. Update README.md (manual)

The script does not touch `README.md`. Edit it by hand to keep the human-facing catalog accurate:

- Add a row for each new skill in the appropriate category table under **Available Skills** (`| [name](<name>/SKILL.md) | \`trigger\` | description |`).
- Remove rows for deleted skills.
- If a new category of skill appears, add a `### <Category>` heading with its own table.

Keep descriptions in the README consistent with each skill's front-matter `description`.

### 4. Validate

If the `claude` CLI is available, validate the marketplace:

```bash
claude plugin validate .
```

Otherwise confirm both JSON files parse and that every `<name>/SKILL.md` has a matching entry in `marketplace.json`:

```bash
python3 -c "import json; json.load(open('.claude-plugin/marketplace.json')); print('ok')"
```

## Rules to preserve

- **One plugin, many skills — one marketplace entry.** Do not create a separate `plugin.json` per skill or add a marketplace entry per skill. This repo is a single plugin whose `skills: "."` discovers every top-level `<name>/SKILL.md`; the marketplace lists exactly one entry named `skills`. Only split into multiple plugins if the user explicitly wants that.
- **Entry name == manifest name.** The install id is `skills@<marketplace>`; keep the plugin.json `name`, the marketplace entry `name`, and the marketplace `name` consistent. Plugin names are immutable once published — renaming breaks existing installs.
- **Keep versions in sync.** When bumping `.claude-plugin/plugin.json`'s `version`, also bump the matching entry's `version` in `marketplace.json` (the script does this for you).

## Resources

### scripts/
- `sync_marketplace.py` — Keeps the single `skills` marketplace entry in sync with the repo (ensures it exists, fixes source, refreshes description from README, syncs version) and lists every discovered skill folder. Supports `--dry-run` and `--root PATH`.
