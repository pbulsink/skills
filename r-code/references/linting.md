# Linting with `lintr`

Enforce code quality in R projects using the `lintr` package.

## Setup

Create a `.lintr` file at the project root (the directory containing `DESCRIPTION`) before running any lint checks. A template `.lintr` file is available as part of this skill — use it only if the repository does not already have a `.lintr` file. Never overwrite an existing `.lintr`.

## Usage

| Scope | Function | How to run |
|-------|----------|------------|
| Single file | `lintr::lint()` | `Rscript -e "lintr::lint('R/fetch_records.R')"` |
| Entire directory | `lintr::lint_dir()` | `Rscript -e "lintr::lint_dir('R/')"` |
| Whole project/package | `lintr::lint_package()` | `Rscript -e "lintr::lint_package()"` |

Use the bundled `scripts/run_r.ps1` script to execute R commands:

```powershell
.\scripts\run_r.ps1 -e "lintr::lint('R/fetch_records.R')"
```

## Workflow

Run lint checks **after** formatting with `air`. Formatting fixes many style issues, so running lint second avoids false positives. Address all violations before finalizing changes.
