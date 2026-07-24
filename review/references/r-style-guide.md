# R Style Quick-Reference for Code Review

Condensed conventions from `r-code`, `tdd-workflow`, and `document` skills. Load when reviewing PRs that touch `.R` files.

## Naming

| Item | Convention | Example |
|------|-----------|---------|
| Exported functions | `snake_case`, verb or phrase | `fetch_records()`, `build_summary()` |
| Internal helpers | `snake_case` with dot prefix | `.parse_response()`, `.validate_columns()` |
| Parameters | `snake_case`, usually nouns | `file_path`, `page_size`, `overwrite` |

Flag: exported functions using `camelCase` or `dot.case`; internal helpers missing the leading dot.

## Pipe & Function Syntax

- Use base pipe `|>`, not magrittr `%>%`.
- Single-line anonymous functions use `\() ...`; multi-line uses `function() { }`.

## API Patterns

- **Enums**: default to character vector, resolve with `rlang::arg_match()`.
- **Optional params**: use `NULL` as default; check with `is.null()`.
- **Return values**: return tibbles (`tibble::as_tibble()`), not bare data frames.
- **S3 objects**: build named list + set class explicitly.
- **Validators**: accept and forward `call = rlang::caller_env()` for error context.

## Validation & Error Handling

- Validate at the point of use (preserve lazy evaluation). Do not eagerly check all params in a top-level wrapper.
- Use `cli::cli_abort()` with `{.fn name}` and `{.arg param}` formatting. Include an error class string.
- Flag tests for package errors: must include the package prefix string as well as the error class.

## Documentation (roxygen2)

- Exported functions need: full sentence-case title, description paragraph, `@export`, `@examples`.
- Internal helpers: brief title, `@keywords internal`, no `@examples`.
- New exports must appear in `_pkgdown.yml` reference section if it exists.
- After doc changes: run `air format . && devtools::document(roclets = c('rd', 'collate', 'namespace'))`.

## Tests (testthat)

- Test files mirror source: `tests/testthat/test-{name}.R` for `R/{name}.R`.
- One concept per test. Self-contained setup. Runnable in isolation.
- Every new `test_that()` includes an issue reference: e.g., `( #42 )`. Use `#noissue` if none verifiable.
- Target 100% coverage on every edited source file; exclude only `R/*-package.R`, `R/aaa-shared_params.R`, and `R/import-standalone-*.R`.
- Snapshot tests: never accept a diff without reviewing the full `.md` snapshot change first.

## Dependencies

- Prefer existing imports from DESCRIPTION over base R equivalents (`purrr::map()` over `lapply()`).
- Never use `library()` inside package code — always namespace (`dplyr::filter()` or `@importFrom`).
- Adding a new dependency requires explicit discussion, not silent inclusion.
