# Linting with `lintr`

Enforce code quality in R projects using the `lintr` package.

## Setup

Create a `.lintr` file at the project root (the directory containing `DESCRIPTION`) before running any lint checks. A template `.lintr` file is available as part of this skill — use it only if the repository does not already have a `.lintr` file. Never overwrite an existing `.lintr`. If adding to the package, append ^\.lintr$ to .Rbuildignore if it's not already there.

## Usage

Run lint checks **in Posit Assistant's live R session first** — use its built-in R tool to execute the call in your active console, then read the returned lints. This reuses installed packages and shows exactly what ran.

| Scope | Call |
|-------|------|
| Single file | `lintr::lint('R/fetch_records.R')` |
| Entire directory | `lintr::lint_dir('R/')` |
| Whole project/package | `lintr::lint_package()` |

**Terminal fallback only when no live session is available.** If you must run via the command line (e.g. outside Positron/RStudio), use `Rscript -e "..."`, or on Windows the bundled `scripts/run_r.ps1`:

```bash
Rscript -e "lintr::lint('R/fetch_records.R')"
```

```powershell
.\scripts\run_r.ps1 -e "lintr::lint('R/fetch_records.R')"
```

## Workflow

Run lint checks **after** formatting with `air`. Formatting fixes many style issues, so running lint second avoids false positives. Address all violations before finalizing changes.
