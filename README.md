# Skills

Kilo skills extend the agent's capabilities with specialized knowledge, workflows, and conventions. Each skill defines its trigger, scope, and dependencies in a YAML front-matter block at the top of `SKILL.md`.

## Available Skills

### R Package Development

| Skill | Trigger | Description |
|---|---|---|
| [r-code](r-code/SKILL.md) | `write R functions` | Writing new R functions, designing APIs, reviewing or modifying existing code. Covers naming conventions, function signatures, input validation, error handling, and common pitfalls. Requires R + devtools. |
| [document](document/SKILL.md) | `document functions` | Roxygen2 documentation for R package functions. Requires R + devtools. |
| [tdd-workflow](tdd-workflow/SKILL.md) | `write or review tests` | Test-driven development with testthat. Covers TDD workflow, test organization, coverage targets, and common patterns. Requires R + testthat. |
| [vignette](vignette/SKILL.md) | `create vignettes` | Workflow-focused package vignettes for users familiar with R but new to the package. Requires R + usethis. |
| [generate-agents-md](generate-agents-md/SKILL.md) | `generate AGENTS.md` | Generate a project-specific AGENTS.md by analyzing an R package's DESCRIPTION, directory structure, and R/*.R roxygen docs. Produces structured documentation with Standard Workflow emphasis. Requires no external tools — pure file analysis. |

### GitHub Operations

| Skill | Trigger | Description |
|---|---|---|
| [github](github/SKILL.md) | `use GitHub CLI for repository operations` | Authentication verification, repository identification, issue management (creation, viewing, commenting), pull request creation and review via `gh` CLI. Requires gh + auth. |
| [implement-issue](implement-issue/SKILL.md) | `implement GitHub issue` | End-to-end implementation of a specific GitHub issue: reads the issue, creates a branch, implements changes using other skills (tdd-workflow, r-code, document), commits, pushes, and opens a PR. Requires gh + auth. |

### Skill Development

| Skill | Trigger | Description |
|---|---|---|
| [skill-creator](skill-creator/SKILL.md) | `create or update skill` | Guide for creating or updating skills. Extends Kilo's capabilities with new knowledge, workflows, or tool integrations. |

## Agent Guidelines

This repository includes a generic [AGENTS.md](AGENTS.md) file with general behavioral guidelines for Kilo sessions. Copy it to the root of your project and customize it with project-specific rules, conventions, and preferences.

## How Skills Work

Each skill directory contains:

- **SKILL.md** — The skill definition (YAML front-matter + instructions). Kilo loads this when the trigger matches a user request.
- **references/** — Supporting files (metadata, templates, scripts) referenced by the skill.
- **scripts/** — Helper scripts (e.g., shell or PowerShell utilities used during execution).

### Trigger Matching

Kilo matches user requests to skills using the `trigger` field in front-matter. Multiple skills may be loaded for a single request if their triggers apply. The system resolves dependencies automatically — for example, implementing an issue via `implement-issue` will also load `tdd-workflow`, `r-code`, and `document`.

## Adding a New Skill

1. Create a new directory: `mkdir <skill-name>`
2. Add `SKILL.md` with YAML front-matter (`name`, `trigger`, `description`) followed by instructions.
3. Optionally add `references/` for supporting files and `scripts/` for executables.

See the [skill-creator](skill-creator/SKILL.md) skill for detailed guidance on designing effective skills.
