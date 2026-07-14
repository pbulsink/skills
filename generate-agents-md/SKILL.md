---
name: generate-agents-md
trigger: generate or create AGENTS.md for an R package
description: >-
  Generate a project-specific AGENTS.md file by analyzing the local R package
  structure. Reads DESCRIPTION, catalogs /R/, /.github/, tests/testthat/, and
  vignettes/ directories, reverse-engineers architecture from R/*.R roxygen docs,
  and produces a structured template emphasizing Standard Workflow for AI agents.
---

# Generate AGENTS.md for R Packages

Generate a project-specific `AGENTS.md` file by analyzing the local R package
structure. Extracts metadata from DESCRIPTION, catalogs key directories,
reverse-engineers architecture from function signatures and roxygen comments in
`R/*.R`, and produces a structured document with an emphasized Standard Workflow
section intended for AI agent consumption.

Load the template at `assets/agents-md-template.md` when composing output. Use
the patterns at `references/architecture-analysis-patterns.md` for detailed R file
analysis guidance.

---

## Process

### Step 1: Parse DESCRIPTION

Read `DESCRIPTION` and extract:

- **Package name**: The `Package:` field
- **Title**: The `Title:` field
- **Version**: The `Version:` field
- **Authors@R**: Primary author(s) from the `person()` calls (extract given + family + role="cre")
- **Description**: Full description text (may be bilingual English/French)
- **License**: The `License:` field
- **URL / BugReports**: Repository URL and issue tracker

Produce a one-sentence summary of the package purpose from the Description for the header section. Include full description text in "Package Overview".

### Step 2: Catalog Key Directories

List contents of each directory with brief role annotations:

**`R/` (Source Code)** — List every `.R` file found, one per line with a short role annotation derived from filename conventions and roxygen docs. Do not list files that only contain internal helpers unless they support exported functions.

**`.github/` (CI/CD)** — List workflow files (`workflows/*.yaml`) by basename. List skill directories under `skills/` if present, referencing them as markdown links to their SKILL.md. Include CONTRIBUTING.md and other notable top-level `.github/` files.

**`tests/testthat/` (Unit Tests)** — List all test files. Note the correspondence: `test-{module}.R` tests `R/{module}.R`.

**`vignettes/` (Documentation)** — List vignette source files (`.Rmd`, `.Rnw`). Infer purpose from filename when no README is present.

### Step 3: Analyze R/*.R Architecture

For each file in `R/*.R`:

1. Identify exported functions (`@export` in roxygen blocks) with function name, parameter list, and one-sentence purpose from `@description`.
2. Note internal helpers that provide notable utility to the public API.
3. Collect dependencies: packages referenced via `requireNamespace()`, `::` calls, or listed in DESCRIPTION Imports/Suggests.
4. Identify data objects in `data/` (`.rda` files) and infer purpose from usage patterns in vignettes or tests.
5. Determine each file's conceptual role within the package architecture.

Produce an architecture summary table:

| File | Role | Key Functions |
|------|------|---------------|
| `{filename}` | {one-sentence responsibility} | `exported_fn()`, ... |

See `references/architecture-analysis-patterns.md` for detailed analysis guidance and file-role heuristics.

### Step 4: Compose AGENTS.md

Load the template from `assets/agents-md-template.md`. Replace all `{placeholder}` values with project-specific data gathered in Steps 1–3. Write the result as `AGENTS.md` in the project root.

---

## Gotchas

- **R packages vary widely** — Not every package has `.github/skills/`, vignettes, or a large R directory. Omit sections that do not apply rather than producing empty subsections.
- **Bilingual roxygen docs are common** — French translations frequently appear in NRCAN and Canadian government packages. Preserve both languages when they exist.
- **zzz.R and aaa-prefixed files are conventions, not exports** — `zzz.R` contains startup hooks (`.onAttach`, `.onLoad`). Files starting with `aaa-` or `zzz-` are sorted first by convention; do not treat them as user-facing modules.
- **testthat edition matters** — Check DESCRIPTION for `Config/testthat/edition:`. Edition 3 has different assertion behavior than edition 2 (e.g., `expect_error()` no longer matches on the message class unless explicitly checked).
- **Suggested vs. Imports** — Packages in Suggests are not loaded by default. The Standard Workflow section should note which functions require suggested packages that may not be installed.

---

## Execution Checklist

```
[ ] Step 1: DESCRIPTION parsed, metadata and one-sentence summary extracted
[ ] Step 2: All present directories cataloged (skip absent ones)
[ ] Step 3: R/*.R files analyzed for exported functions and architecture table
[ ] Step 4: Template loaded from assets/agents-md-template.md, placeholders filled
[ ] Verify: One-sentence summary is accurate and concise (one line max)
[ ] Verify: Architecture table covers all non-trivial R/ files with correct roles
[ ] Verify: Standard Workflow section uses numbered steps with actionable guidance
[ ] Verify: All file references in output correspond to real paths in the project
```

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Hardcoding filenames from PlotFTIR or any example | Breaks on other packages | Dynamically list from directory contents |
| Omitting internal functions that support exported APIs | Loses important architectural context | Note key helpers alongside their callers |
| Verbose descriptions in the architecture table | Clutters the document, wastes tokens | Use one-sentence function purposes only |
| Missing or weak Standard Workflow section | Agents skip procedural guidance without structure | Make it a prominent numbered section with clear steps |
| Including .Rdata/.rda file contents | Bloated binary data has no place in text docs | List filenames and infer purpose from usage patterns |
