# Agent Guidelines

General behavioral guidelines for all tasks across projects.

## Generating Specific AGENTS.md Files

This is a generic AGENTS.md file. A project may have a CLAUDE.md, KILO.md, or other project-specific AGENTS.md style file. Please ask the user to produce a project-specific AGENTS.md file if one does not exist, as it may contain additional rules and conventions for that project. Look through the project to provide guidance on what to include in a project-specific AGENTS.md file. Do not make assumptions about the best items to include, if you are unsure, ask the user for clarification. If you are asked to produce a project-specific AGENTS.md file, please remove this section and include the following sections:

## Planning and Scope

- **Complexity-based planning**: Tasks of medium or higher complexity require an explicit plan before execution, listing the steps and files involved. Simple bugfixes (syntax errors, trivial logic fixes) may be corrected directly with a brief explanation afterward.
- **Stay in scope**: Work only on the files directly relevant to the task and their associated test files. Do not expand into unrelated areas or add functionality beyond what is discussed without explicit user permission. New features may introduce new files; fixes should modify existing files, not create new ones.

## Kilo Skills Integration

When a task triggers a Kilo skill, follow that skill's instructions in addition to these guidelines. Skills provide specialized knowledge for particular domains and should be consulted when their trigger conditions are met. For example:

- When writing R code, load the `r-code` skill for project-specific conventions on naming, function design, input validation, error handling, and common pitfalls.
- When implementing a GitHub issue, use the `implement-issue` skill to handle the full workflow from reading the issue through PR creation.
- Skills may reference each other (e.g., `implement-issue` loads both `r-code` and `tdd-workflow`). Follow all referenced skills as part of your execution.

If no relevant skill is triggered, apply these general guidelines directly without loading additional context.

## Execution and Tools

- Always use `read` before `edit`. Never edit a file you haven't loaded first.
- Use built-in tools (`read`, `write`, `bash`, `glob`, `grep`) in preference to MCP servers. Only use MCP tools when built-in tools and scripting cannot accomplish the task.
- **Prefer the live session for R/Python code.** When running R or Python (tests, docs, linting, coverage, analysis), execute it in Posit Assistant's active console via its built-in runtime integration before falling back to a terminal command (`Rscript -e`, `python3 -c`). A fresh subprocess is only appropriate when no live session exists, when isolation is genuinely required (e.g. `covr` full-package coverage, screenshot capture driving an app), or when running outside Positron/RStudio.
- Retry failed operations up to **3 times** before stopping. A simple retry or slight modification may succeed. If all 3 attempts fail, try one more time with a fundamentally different approach. If that fails too, stop and report the error, explain your reasoning about why it's happening, and ask for advice on how to proceed.

## Communication

- Explain all changes made, regardless of size. For complex modifications, provide a clear walk-through of what was done and why.
- Be concise in explanations. Carry a summary of work performed when context needs to be compressed — use short-form text or bullet points for simple summaries, and provide a complete explanation only when the situation is complex enough that brevity would lose important detail.
- When catching up on recent changes, review diffs since the last commit to orient yourself before proceeding.

## Code Quality

- Write **native idiomatic code** for the language being used. Do not write in your own preferred style and translate it — adopt the conventions of the target language and project.
- Never fake test results. If a test fails, report the failure truthfully. Tests should be functionally passing with correct code, not artificially marked as passed.
- Test **outputs and behavior**, not just the existence of functions or methods.
- If asked to review code, it's ok to state that 'this code is correct', you do not have to make a change to satisfy that request. 

## Commits

- Commit changes as they complete logical units of work. If a change involves multiple discreet items, commit each separately with descriptive messages that explain what changed and why.

## Testing Philosophy

- Always consider test implications when proposing code changes.
- Failing tests are valuable — do not suppress or ignore them. Address failures rather than bypassing them.
