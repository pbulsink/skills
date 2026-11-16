---
name: r-code
trigger: write R functions
description: This skill should be used when writing new R functions, designing APIs, or reviewing/modifying existing R code. Covers naming conventions, function design patterns, input validation, error handling, and common pitfalls.
compatibility: Requires R and the `devtools` package for testing, `air` formatter for code formatting. Prefer Posit Assistant's live R/Python session to run code; fall back to PowerShell/Rscript only when no live session is available.
---

# R code

This skill covers how to design and write R functions — including naming conventions, signatures, API conventions, input validation, error handling, and common pitfalls. For documenting functions, use the `document` skill. For tests, use the `tdd-workflow` skill, ensuring coverage is as complete as possible using the `test-coverage` skill. Once satisfied with the function of the code (see the `tdd-workflow` skill), verify that the code passes R CMD Check without errors, warnings, or notes. Address any issues before finalizing the code. If an R CMD Check note or warning cannot be resolved without changes outside the scope of the current task (e.g., it originates from a dependency or existing code), document it explicitly and flag it for developer review rather than suppressing it silently.

## Running R code

When you need to execute R code (tests, documentation, linting, coverage, etc.), **prefer Posit Assistant's live R/Python session** over spawning a new terminal process. Posit Assistant is built into Positron and RStudio with out-of-the-box access to your active console — it can run code in that session directly and see the objects you already have loaded.

1. **First choice: run in the live session.** Use Posit Assistant's built-in runtime integration (its R/Python tools, e.g. `run_r_code` / `execute_python`) to execute the code in your active console. This reuses installed packages and any objects already in scope, shows the exact code being run, and avoids writing throwaway scripts.
2. **Fallback: terminal only when no live session is available.** If there is no active R/Python session (e.g. you are running outside Positron/RStudio, or a tool call that needs a fresh isolated process), fall back to the command line — `Rscript -e "..."`, or the bundled `scripts/run_r.ps1` on Windows.

Do not hardcode absolute R paths in terminal fallbacks; locate R dynamically (see `references/powershell_commands.md`).

> **Note:** Some tasks intrinsically require a *separate* R process — for example, screenshot capture (`app-screenshot`) drives an app via `shinytest2::AppDriver`, which must launch its own fresh R process. Use the terminal/subprocess route for those; do not run them in your interactive session.

## Reference Material

- `references/powershell_commands.md` - Terminal/PowerShell fallback commands for running R (only when no live session is available)
- `references/error_classes.md` - Package-specific error classes
- `references/linting.md` - Using `lintr` for code quality checks and `.lintr` configuration

## Templates

| File | Purpose |
|------|---------|
| `templates/.lintr` | Default linting rules — share only if the repository has no existing `.lintr` file |

## Naming conventions

### Functions

Functions use `snake_case` and should be **verbs or verb phrases** that describe what the function does:

```r
fetch_records()
build_summary()
validate_input()
```

A function name should be descriptive enough to make its purpose clear without a comment. Prefer clarity over brevity — don't abbreviate unless there is a widely understood convention (e.g. `df` for data frame, `dir` for directory).

Internal helpers use a dot prefix:

```r
.parse_response()
.validate_columns()
```

### Parameters

Parameters use `snake_case` and should generally be **nouns**, occasionally adjectives. The same rule applies: clarity over brevity.

```r
# Good
fetch_records(file_path, page_size, overwrite)

# Bad — unclear abbreviations
fetch_records(fp, ps, ow)
```

## File organization

1. If modifying or extending existing functionality: place code in the existing file(s). Do not create new `.R` files.
2. If adding a completely new capability:
  a. Place the exported function in `R/{function_name}.R` (e.g. `fetch_records()` -> `R/fetch_records.R`).
  b. Place helpers used only by that function in the same file.
  c. Place helpers shared across multiple functions in `R/utils.R` or `R/utils-{topic}.R` (e.g. `R/utils-parsing.R`).

## Coding style

- Always run `air format .` after generating code, then run lint checks to catch any remaining issues.
- Use the base pipe operator (`|>`) not the magrittr pipe (`%>%`).
- Use `\() ...` for single-line anonymous functions. For all other cases, use `function() {...}`.

## Linting

Enforce code quality with `lintr`. Run lint checks after formatting with `air`. Address all violations before finalizing changes. See `references/linting.md` for full details on usage and `.lintr` configuration. If the repository has no `.lintr` file, share the template from `templates/.lintr` — never overwrite an existing `.lintr`.

## Function design

**Functional core, imperative shell** — pure, testable functions that accept data and return data form the core. The imperative shell orchestrates program flow, manages state, and calls the functional core.

Functions should be **small and single-purpose**. Each function should operate at a **single level of abstraction**: it either orchestrates calls to other functions, or performs a direct operation on data, but does not mix the two.

```r
# Orchestrator — delegates to focused helpers
build_report <- function(data, output_path) {
  data <- .clean_data(data)
  summary <- .compute_summary(data)
  .write_report(summary, output_path)
}

# Worker — performs one direct operation
.clean_data <- function(data) {
  data |>
    dplyr::filter(!is.na(value)) |>
    dplyr::mutate(value = round(value, 2))
}
```

Name functions well enough that their purpose is obvious from the call site. When reading the orchestrator above, each step is self-documenting — no comments needed.

**Simplify control flow** — prefer guard clauses and returning early over complex if/else structures.

**Pure conditionals** — the expression inside a conditional check should not cause side effects. Extract the pure check from the impure action into separate functions if needed.

## General API design patterns

**Enum-like arguments** — declare choices as the default vector; resolve with `rlang::arg_match()` at the top of the function:

```r
summarize_data <- function(x, method = c("mean", "median")) {
  method <- rlang::arg_match(method)
  # method is now guaranteed to be "mean" or "median"
}
```

**`NULL` as "not provided"** — use `NULL` as the default for optional arguments where there is no sensible scalar fallback; check with `is.null()`:

```r
fetch_records <- function(x, output_column = NULL) {
  if (!is.null(output_column)) { ... }
}
```

**S3 object construction** — build as a named list, set class explicitly:

```r
.new_summary <- function(values, method) {
  out <- list(values = values, method = method)
  class(out) <- c(paste0("summary_", method), "data_summary")
  out
}
```

**`call` propagation in internal validators** — helpers that validate arguments and may throw errors should accept and forward `call`:

```r
.check_non_empty <- function(x, call = rlang::caller_env()) {
  if (length(x) == 0L) {
    .pkg_abort("Input {.arg x} cannot be empty.", "empty_input", call = call)
  }
}

process_data <- function(x, call = rlang::caller_env()) {
  .check_non_empty(x, call = call)
  ...
}
```

**Return tibbles, not data frames:**

```r
summarize_data <- function(x) {
  result |> tibble::as_tibble()
}
```

## Input validation

Validate each input parameter in the function that directly uses it. Provide cli::cli_abort() errors with informative messages and appropriate error classes if parameter values are invalid. This ensures that users get clear feedback when they call the function incorrectly, and allows them to handle specific error classes if needed.

Existing validators such as those for spectra format and intensity type are available in the package. Always use these existing validators when the parameter type or structure they check matches what you need to validate, rather than re-implementing equivalent checks with `cli::cli_abort()` directly.

**Validate in the function that uses the parameter**, not in a caller that passes it through. This preserves R's lazy evaluation — if a parameter is never used on a code path, it is never evaluated or validated.

```r
# Good — validation happens where the parameter is used
build_report <- function(data, title, page_size) {
  data <- .clean_data(data)
  summary <- .compute_summary(data, page_size)
  .write_report(summary, title)
}

.compute_summary <- function(data, page_size, call = rlang::caller_env()) {
  page_size <- stbl::to_int_scalar(page_size, call = call)
  ...
}

.write_report <- function(summary, title, call = rlang::caller_env()) {
  title <- stbl::to_chr_scalar(title, call = call)
  ...
}
```

```r
# Bad — validates everything eagerly, breaking lazy evaluation
build_report <- function(data, title, page_size) {
  title <- stbl::to_chr_scalar(title)
  page_size <- stbl::to_int_scalar(page_size)
  ...
}
```

## Internal vs. exported functions

Export a function when:
- Users will call it directly
- Other packages may want to extend it
- It is a stable, intentional part of the API

Keep a function internal when:
- It is an implementation detail that may change
- It is only used within the package
- Exporting it would clutter the user-facing API

Internal helpers use a dot prefix (e.g. `.parse_response()`).

## Error handling

Always provide informative error messages with `cli::cli_abort()`.

Include the name of the calling function (using `{.fn func_name}`) and a description of why the input is invalid in every `cli::cli_abort()` message. Example: `cli::cli_abort("{.fn fetch_records}: {.arg page_size} must be a positive integer, not {.val {page_size}}.")`.

Any code lines must contain only ASCII characters - if writing messages (especially in french) to users be sure to properly escape any non-ASCII characters (e.g. `\u00e9` for `é`) to avoid R CMD Check notes. A table of escaped characters is available in the reference folder of this skill.

## Common package mistakes

```r
# Never use library() inside package code
library(dplyr)          # Wrong
dplyr::filter(...)      # Right
# or `@importFrom dplyr filter` if used extensively

# Never modify global state without restoring it
options(my_option = TRUE)                    # Wrong
withr::local_options(list(my_option = TRUE)) # Right

# Use system.file() for package data, not hardcoded paths
read.csv("/home/user/data.csv")                         # Wrong
system.file("extdata", "data.csv", package = "mypkg")   # Right
```

## Dependencies

### Use existing imports first

Packages already in `Imports` in `DESCRIPTION` should be preferred over base R equivalents: `purrr::map()` over `lapply()`, `rlang::is_*()` predicates over `is.*()`, and `withr::local_*()` over manual `on.exit()` state management. The preference for purrr, rlang, and withr only applies when those packages are already listed under `Imports` in `DESCRIPTION`. If they are not present, treat them as new dependencies requiring explicit discussion before use.

### When to add a new dependency

Add a dependency when it provides significant functionality that would be complex or brittle to reimplement — date parsing, web requests, complex string manipulation. Stick with base R or existing imports when the solution is straightforward.

**Adding a new dependency requires explicit discussion with the developer.**
