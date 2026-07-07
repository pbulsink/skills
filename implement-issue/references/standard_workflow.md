# Standard Development Workflow

This workflow applies to any feature, fix, or refactor task.

## Prerequisites

Before starting, ensure:
- All tests pass: `devtools::test(reporter = "check")`
- Packages are updated: `pak::pak()`

If tests fail, stop and ask before proceeding.

## Workflow Steps

1. **Plan** — identify affected source files; check if new exports are needed
2. **Test first** — write failing test, then implement: verify with `devtools::test(filter = "name", reporter = "check")`
3. **Implement** — minimal code to pass tests
4. **Refactor** — clean up while keeping tests green
5. **Document** — document any new or changed exports
6. **Verify**: Run full test suite, then `devtools::check(error_on = "warning")`. Resolve all warnings, errors, and NOTEs.
7. **News** — add bullet at top of `NEWS.md` (under dev heading):
   - User-facing changes only. 1 line, end with `.`
   - Present tense, positive framing, function names (backticks + `()`) near start
   - Issue/contributor before final period: `` * `fn()` now accepts ... (@user, #N). ``
   - Get username: `gh api user --jq .login`; issue number from branch name or `gh issue list`

## General

- R console: use `--quiet --vanilla`
- Always run `air format .` after generating code
- Comments explain *why*, not *what*