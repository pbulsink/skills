---
name: document
trigger: document functions
description: This skill should be used when documentation for R package functions is requested or required.
compatibility: Requires R and the `devtools` package.
---

# Document Functions

Implement Roxygen2 documentation following these procedural standards.

## Core Documentation Workflow

1.  **Apply Roxygen2 Tags**: Use `@param`, `@returns`, and `@seealso` as appropriate. Refer to `references/roxygen2_syntax.md` for detailed type notation and parameter formatting.
2.  **Manage Parameter Inheritance**: Place function-specific `@param` definitions before any `@inheritParams` lines. Use `@inheritParams .shared-params` when using shared parameters defined in `R/aaa-shared_params.R`.
3.  **Handle Internal Functions**: Use abbreviated documentation for unexported helpers (no `@export`, include `@keywords internal`). Still include title & @description, and describe all parameters. Avoid adding `@examples` to internal functions.
4.  **Group Related Functions**: For S3 methods or related exported variants, use the `@rdname` tag to group them under a single help page. Refer to `references/s3_methods.md` for implementation details.
5.  **Format**: After updating documentation, format code:
    ```bash
    air format .
    ```
6.  **Regenerate Docs**: generate automatic Roxygen files by calling `devtools::document()` after edits and formatting. **Run it in Posit Assistant's live R session** (its built-in R tool) so it reuses your active console — fall back to the terminal only when no live session is available:
    ```r
    devtools::document(roclets = c('rd', 'collate', 'namespace'))
    ```
    Terminal fallback:
    ```bash
    Rscript -e "devtools::document(roclets = c('rd', 'collate', 'namespace'))"
    ```

## Exported vs. Internal Functions

### Exported Functions (Public API)
- Use a full title in sentence case.
- Provide a descriptive paragraph providing context and details.
- Include `@export` to make the function available to users.
- Always include an `@examples` section for user guidance.

### Internal Functions (Private Helpers)
- Use a brief title in sentence case.
- Omit the description paragraph only if the name and parameter names do not clearly communicate behavior.
- Include `@keywords internal` to prevent exporting.
- Avoid adding `@examples`.

## Specialized Workflows

### S3 Methods
Follow specific grouping rules for S3 methods using `@rdname`, as detailed in `references/s3_methods.md`.

### Package Documentation (`pkgdown`)
If a `_pkgdown.yml` file exists and contains a `reference` section, add any new non-internal topics to the reference index. Verify completeness by running:
```bash
pkgdown::check_pkgdown()
```
