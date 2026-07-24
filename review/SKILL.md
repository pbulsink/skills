---
name: review
description: >-
  Review code changes in git or GitHub repositories — catch logic bugs, design issues,
  style violations, test gaps, and missing documentation that CI cannot detect. Use when
  the user asks to review a PR, inspect diff changes, evaluate code quality, or get a
  second opinion on a pull request or branch comparison. Does not re-report CI failures
  for syntax, tests, linting, or formatting.
---

# Review Code Changes

Review diffs in git repositories (local branches and GitHub PRs). Catch what CI cannot: bugs, design issues, style violations, test gaps, and documentation drift. Frame all feedback as suggestions the reviewer can accept or reject.

## Don't duplicate CI

CI already reports failures directly. Do **not** comment on:

- R CMD Check errors
- Test suite failures
- Lint, formatting, or typecheck errors (`lintr`, `air`)

If every issue identified falls into one of these categories, post only `lgtm` (see [Output Format](#output-format)).

## Review workflow

Progress through the review in this order:

1. Fetch and read the full diff — use `git diff` for local branches or `gh pr diff` for PRs
2. Read surrounding context for changed functions/files; diffs alone hide intent
3. Evaluate each category below (bugs, style, tests, user-facing)
4. Post comments on specific lines using [Output Format](#output-format), or post `lgtm` if clean

## What to focus on

### 1. Bugs and correctness

Look for:

- Logic errors: off-by-one, wrong conditions, swapped arguments
- Unhandled error paths, unused parameters, missing presence checks for imported packages
- Inputs that lack validation in the function that uses them
- Documentation drift: usage descriptions that no longer match code behavior

### 2. Style compliance

Consult `references/r-style-guide.md` for the full set of naming conventions, API patterns, and formatting rules from `r-code`, `tdd-workflow`, and `document`. Only flag actual violations; recognize when existing code complies through a different mechanism (e.g., using an internal validator instead of inline checks).

When suggesting fixes, ensure the suggestion is valid R code (matched braces, correct syntax, proper pipe usage). Prefer prose comments over structured `suggestion` blocks unless the fix is trivially mechanical.

### 3. Test quality

- Tests should exercise real implementation logic, not duplicate it into assertions.
- Avoid mocking stable, pure functions within the package; flag tests that mock excessively and appear to test the mock rather than production code.
- New exported behavior in `R/{file}.R` should have a corresponding test in `tests/testthat/test-{file}.R`.

### 4. User-facing changes

- Features, bug fixes, and breaking changes need a NEWS.md entry. If a PR clearly alters user-visible behavior without one, flag it.
- NEWS descriptions are read by end users — rewrite implementation-style entries ("Add export handler that serializes…") into user-facing language ("Support exporting conversations as markdown").
- PR descriptions should explain **why**, not enumerate files. Skip file-by-file inventories.

## Gotchas

Domain-specific traps that agents commonly miss during review:

- **`library()` in package code**: Never use `library(dplyr)` inside `.R` source files — flag it and suggest namespace-qualified calls (`dplyr::filter()`) or `@importFrom`.
- **Eager validation**: Parameters validated at the top of a wrapper function break R's lazy evaluation. Flag this; validation should happen where each parameter is used.
- **Missing `call` propagation**: Internal validators that throw errors must accept and forward `call = rlang::caller_env()` so error messages include the calling function name.
- **Error class mismatch**: Tests for package errors via `.cli_abort()` must check both the message pattern and the error class string (e.g., `"empty_input"`). A test matching only the message is fragile.
- **Magrittr pipe (`%>%`)**: New code should use the base pipe (`|>`) unless maintaining existing `%>%` chains in a file that has not been migrated yet. Flag new instances of `%>%`.
- **Coverage gaps on edited files**: Any file changed in `R/{name}.R` must reach 100% test coverage (excluding `*package.R`, `aaa-shared_params.R`, and `import-standalone-*`). Check whether tests were added for the modified code.
- **roxygen2 drift after parameter rename**: If a function's parameters changed, its roxygen2 `@param` tags must match exactly — mismatched names are silent documentation bugs that only appear when users run `?function_name`.
- **New S3 methods without registration**: Adding a new S3 method requires both `@export` and an entry in `NAMESPACE`. Flag methods present in code but missing from exports.

## Posting comments

### GitHub PRs

When reviewing on GitHub, post line-specific comments using the `gh pr review --comment` command:

```bash
gh pr comment <number> --body-file - <<'EOF'
[comment text]
EOF
```

For line-specific inline comments, use:

```bash
gh api repos/{owner}/{repo}/pulls/{n}/comments \
  -f body="Comment text" \
  -f path="R/file.R" \
  -f line=42 \
  -f side="RIGHT"
```

### Local diffs

When reviewing local branches (no GitHub PR), summarize findings as a single block of review comments in the response. Use [Output Format](#output-format) for structure, but deliver them inline rather than via `gh`.

## Output format

Each review comment should follow this structure:

**[Category]: [One-line summary]**

Observation or concern with reference to specific code (file and line if applicable).

_Suggestion_ (optional): concrete fix or alternative approach.

Available categories:

| Category | Use for |
|----------|---------|
| `Logic` | Bugs, wrong conditions, off-by-one errors, unhandled paths |
| `Style` | Naming violations, pipe misuse, API pattern deviations |
| `Tests` | Missing tests, mock overuse, coverage gaps |
| `Documentation` | roxygen2 drift, missing examples, NEWS.md issues |
| `Design` | Architecture concerns, function size, abstraction leaks |

### When to post `lgtm`

Post only `lgtm` when the PR is **clean**: no logic bugs found, no style violations beyond what existing code demonstrates, new behavior has corresponding tests, and user-facing changes include NEWS.md entries. Do not add additional commentary in this case — `lgtm` signals a clean review to the reviewer.
