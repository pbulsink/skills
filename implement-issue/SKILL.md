---
name: implement-issue
trigger: implement GitHub issue
description: This skill should be used when asked to implement, work on, or fix a specific GitHub issue number. Wraps the standard development workflow with GitHub-specific setup (issue reading, branch creation) and completion steps (commit, push, PR creation).
compatibility: Requires the `gh` CLI and an authenticated GitHub session.
---

# Implement a GitHub Issue

This skill wraps the Standard Workflow defined in `references/standard_workflow.md`. Run the steps below before and after that workflow. Refer to `scripts/` for PowerShell utilities that assist with GitHub operations.

## Bundled Scripts

| Script | Purpose |
|--------|---------|
| `scripts/gh_check_auth.ps1` | Verify `gh` CLI authentication status |
| `scripts/gh_get_repo_id.ps1` | Extract repository owner/name from git remote |

Use these scripts when you need to verify authentication or retrieve repository information during the implementation process.

## Before the Standard Workflow

**A. Verify authentication:**

Run `scripts/gh_check_auth.ps1` or manually execute:
```powershell
gh auth status
```

If not authenticated, stop and ask the user to authenticate before continuing. If the issue is already closed or has a linked merged PR, stop and inform the user before proceeding. Ask whether to continue anyway.

**B. Read the issue in full:**

```bash
gh issue view {number}
```

**C. Check/create the branch:**

- If on `main`: use `usethis::pr_init("fix-{number}-{description}")` or fall back to `git checkout -b fix-{number}-{description}`
- If currently on a branch that is not `main` and does not match `fix-{number}-*`, stop and ask the user whether to switch to `main` and create a new branch or continue on the current branch.
- Branch format: `fix-{number}-{description}` with three segments separated by hyphens; within description, use snake_case
- Example: `fix-42-validate_input`
- If a matching branch already exists locally or on remote, check it out instead of creating

## Run the Standard Workflow from `references/standard_workflow.md`

Steps 1–9 represent the core development loop. During implementation:

1. **Plan**: Identify affected source files; check if new exports are needed
2. **Test first**: Write failing test, then implement; verify with `devtools::test(filter = "name")`
3. **Implement**: Minimal code to pass tests
4. **Refactor**: Clean up while keeping tests green

**Important**: Before committing changes, perform an independent review as if another agent is reviewing your work:
- Verify all test cases are correct and complete
- Confirm code follows `r-code` conventions (naming, signatures, validation)
- Check that new or modified functions have proper documentation
- Ensure error handling covers edge cases
- Validate that the implementation matches issue requirements

## After the Standard Workflow

**D. Final verification before PR submission:**

1. Run full test suite: `devtools::test(reporter = "check")`
2. Verify all commit checks pass (GitHub Actions status)
3. Confirm code coverage metrics are acceptable
4. If vignettes or documentation were updated, verify they render correctly

**E. Commit and push:**

1. Review commits already on this branch: `git log main..HEAD --oneline`
2. Stage and commit all changes:
   ```bash
   git add -A
   git commit -m "{short imperative summary}"
   ```
3. Push the branch: `git push -u origin HEAD`

**F. Open the PR:**

1. Create PR: `gh pr create --fill`
2. If auto-filled content is incomplete or omits issue number, use explicit `--title` and `--body`
3. Verify PR description links to the issue (e.g., "Closes #{number}")
4. Ensure all required reviewers are added

**G. After status checks pass:**

1. Review the PR as if performed by an independent agent
2. If all criteria met, file a review with "Approve" status and comment explaining readiness for merge
3. If issues remain, file a review with "Request Changes" status and document required fixes

**Important**: The agent should never merge or close a PR. All merge/closure decisions rest with repository maintainers.

## Skills Reference

- **Core development**: Follow `tdd-workflow` for test-first development and `r-code` for R function guidelines
- **Documentation**: Use `document` skill when adding or modifying exported functions requires roxygen documentation
- **Vignettes**: Use `vignette` skill when user-facing workflows, examples, or conceptual guides need updating

## Error Handling

### Common Issues

1. **No commits ahead of main**: Branch has no changes to submit
   - Ask if the user meant to work on a different branch

2. **Branch not pushed**: Remote doesn't have the branch
   - Push first: `git push -u origin HEAD`

3. **PR already exists**: A PR for this branch already exists
   - Show existing PR: `gh pr view`
   - Ask if they want to update it instead

4. **Merge conflicts**: Branch conflicts with base
   - Guide user through resolving conflicts or rebasing

5. **After PR is created and checks pass**:
   - File a review with "Approve" status if all criteria met
   - Add comment explaining why the PR is ready for merge
