# {Package Name} - Agent Guidelines

{One-sentence summary of package purpose derived from DESCRIPTION}

- **Package:** `{package}` v`{version}`
- **Authors:** `{primary author(s) with ORCID if available}`
- **Repository:** `{URL from DESCRIPTION}`
- **Bug Reports:** `{BugReports URL from DESCRIPTION}`

## Package Overview

{Full description text from DESCRIPTION, preserving bilingual content}

## Project Structure

### R/ (Source Code)
- `{filename}.R` - {short role annotation}
{... one line per file in R/, sorted alphabetically ...}

### .github/ (CI/CD and Workflows)
- **Workflows:** {list workflow basenames, e.g., R-CMD-check.yaml, test-coverage.yaml}
{If skills directory exists:}
- **Skills:** {[skill-name](skills/{skill-name}/SKILL.md), ...}
{If CONTRIBUTING.md exists:}
- [Contributing Guide](CONTRIBUTING.md)

### tests/testthat/ (Unit Tests)
- `test-{module}.R` - {brief description of what this test file covers}
{... one line per test file, grouped by the R module it tests ...}

{If vignettes exist:}
### vignettes/ (Documentation)
- `{vignette-file}` - {inferred or explicit purpose}

## Architecture Summary

{Intro sentence describing the package's architectural organization}

| File | Role | Key Functions |
|------|------|---------------|
| `{filename}.R` | {one-sentence responsibility} | `exported_fn()`, ... |
{... one row per non-trivial R file, sorted alphabetically ...}

**Dependencies:**
- **Imports:** {comma-separated list from DESCRIPTION Imports field}
- **Suggested (optional features):** {comma-separated list from DESCRIPTION Suggests field}

## Standard Workflow

This section describes the typical development and testing workflow for this package. Agents should follow these steps when making changes:

### 1. Understand the Code Path
- Read roxygen documentation in `R/*.R` to understand function purposes and signatures
- Trace data flow through the relevant module(s) identified in the architecture table
- Identify which files are affected by the proposed change

### 2. Make Changes
- Modify only the relevant file(s) in `R/`. Do not create new `.R` files unless adding a completely new capability that does not fit within existing modules.
- Follow existing naming conventions and code style (see loaded Kilo skills for R-specific guidance).
- Use `{error_handling_pattern}` for error messages (e.g., `cli::cli_abort()`) where present in the codebase.
- Preserve bilingual roxygen documentation (English + French) when modifying existing functions that include it.

### 3. Add Tests
{if tests/testthat/ exists:}
- Create or update tests in `tests/testthat/test-{module}.R`, matching the source file under test.
- Place new tests adjacent to existing tests for the same function, or at the end of the file if no tests exist yet.
- Run `{test_command}` to verify all tests pass.
- Ensure new exported functions have usage examples in roxygen `@examples` blocks.

{if suggested packages are used in tests:}
- Some test functionality requires suggested packages (e.g., {list}). These may not be installed locally; use `requireNamespace()` guards when testing optional features.

### 4. Update Documentation
- Regenerate man pages and NAMESPACE: `{document_command}` (typically `devtools::document()`)
- Update vignettes if the change affects user-facing behavior or examples.
- Run `{check_command}` to validate the package builds without errors, warnings, or notes.

### 5. Verify Build
- Full package check: `{check_command}` (typically `devtools::check()` or `R CMD CHECK`)
- Review test coverage for edited files; aim for high coverage on new code.
- Ensure no regressions in existing tests and that all file references remain valid.

## Testing Philosophy

{Generate from examining the package's test patterns:}
- Test outputs and behavior, not just function existence
- {Note any specific testing conventions observed, e.g., snapshot usage, fixture patterns}
- Failing tests are valuable — address failures rather than suppressing them

{If Kilo skills exist in .github/skills/:}
## Kilo Skills Integration

This project includes custom Kilo skills in `.github/skills/`:
- {[skill-name](.github/skills/{skill-name}/SKILL.md) - {brief description if discernible}}
{... one line per skill ...}

When working on this project, load these skills for domain-specific guidance alongside the general R and testing skills provided by Kilo.
