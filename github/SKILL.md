---
name: github
trigger: use GitHub or git tools for repository operations
description: This skill should be used when interacting with GitHub repositories via the gh CLI (remote actions like issue/PR management) and standard git CLI (local actions like status checks, staging files, committing history). Includes safe commit patterns to prevent corruption during simultaneous agent work. Requires git and an authenticated gh session for remote operations.
compatibility: Requires `git` for local repository operations and the `gh` CLI for authentication verification, issue/PR management.
---

# GitHub CLI Workflows

All GitHub operations require:
1. **Authentication**: Verify with `gh auth status`
2. **Repository Identification**: Extract owner/name from git remote (see `references/github_metadata.md`)

## Prerequisites (Always First)

### 1. Authentication Check
```bash
gh auth status
```

If not authenticated, instruct the user to run `gh auth login` before proceeding.

### 2. Repository ID Retrieval
Issue creation via `gh_create_issue.sh` takes the repository's **GraphQL node ID** (base64), *not* `owner/name`. See `references/github_metadata.md` for the lookup command and issue type IDs.

## Issue Management

### Create an Issue

#### Determine Repository ID
Retrieve the repository node ID from `references/github_metadata.md`:

```bash
gh api graphql -f query='{ repository(owner: "<OWNER>", name: "<REPO>") { id } }' --jq '.data.repository.id'
```

Passing `<OWNER>/<REPO>` here fails with "Could not resolve to a node with the global id".

#### Select Issue Type and Title
Choose the most appropriate issue type based on the request. Use conventional commit prefixes for titles (e.g., `feat:`, `fix:`, `docs:`, `chore:`). Issue type IDs are **per-repository**, not universal — the table in `references/github_metadata.md` shows example values only. Always verify the target repo's actual IDs with the lookup query there before creating an issue; a mismatch fails with "Issue type cannot be found in this organization".

#### Construct Issue Body
Build a Markdown body file containing:

**Required for all types:**
- `## Summary`: A single user story sentence (e.g., `> As a [role], in order to [goal], I would like to [feature].`)

**Conditional sections:**
- **Issues requiring fixes (bugs):**
  - `## Behavior`: Current broken behavior and reproduction steps
  - `## Details`: Implementation context

- **Issues for new feature implementations:**
  - `## Proposed signature`: The proposed R function signature and argument descriptions
  - `## Behavior`: Expected behavior, edge cases
  - `## Details`: Package requirements and implementation notes

**Optional sections (all types):**
- `## References`: Links to external documentation or related code

#### Execute Issue Creation
```bash
./scripts/gh_create_issue.sh <repoNodeID> "<title>" /tmp/issue_body.md <issueTypeID>
```

- `<repoNodeID>`: the repository's GraphQL node ID (base64), from the lookup above.
- *Ensure the body content is written to a temporary file first.* On Windows, quote absolute paths that contain spaces.

**Reference**: For detailed GraphQL queries and ID lookups, consult `references/github_metadata.md`.

### View/Read Issues
```bash
gh issue view <number>    # View specific issue
gh issue list             # List all issues
```

### Comment on Issues
```bash
gh issue comment <number> --body "comment text"
```

## Pull Request Management

### Create a PR

#### Prerequisites Check
1. **Verify `gh` CLI is installed**: `gh --version`
2. **Check authentication**: `gh auth status`
3. **Verify clean working directory**: `git status`

If uncommitted changes exist, ask the user whether to commit, stash, or discard them.

#### Gather Context
1. **Identify current branch**: `git branch --show-current`
2. **Find base branch**: `git remote show origin | grep "HEAD branch"`
3. **Analyze commits**: `git log origin/main..HEAD --oneline`
4. **Review diff**: `git diff origin/main..HEAD --stat`

#### Issue Implementation Workflow
When implementing a specific GitHub issue:

1. **Read the issue**: `gh issue view <number>`
2. **Verify authentication and repository ID**
3. **Check/create branch** using pattern `fix-{number}-{description}`:
   - If on `main`: use `usethis::pr_init("fix-{number}-{description}")` or fall back to `git checkout -b fix-{number}-{description}`
   - If a matching branch already exists, check it out instead
4. **Run development workflow**:
   - Follow `tdd-workflow` for test-first development
   - Follow `r-code` for function design and implementation
   - Use `document` skill when new exports require documentation
   - Use `vignette` skill when user-facing workflows need vignettes
5. **Verify implementation**:
    - Run tests: `devtools::test()`
    - All commit checks must pass before PR submission
6. **Commit and push changes** — follow an **edit → stage loop**, never `git add -A`:

    After each file change, stage it immediately:
    ```bash
    git status --short                              # Confirm only your files changed
    git diff --name-only                            # Verify the staged path matches
    git add R/foo.R                                 # Stage the specific file you edited
    ```

    **Why this pattern**: `git add -A` stages everything in the working tree, including files modified by other concurrent agents. The edit→stage loop ensures commits contain only your changes and never corrupt another agent's work. Commit when all planned edits are staged:

    ```bash
    git commit -m "fix: resolve issue with foo (#42)"
    git push -u origin HEAD
    ```

#### Create the Pull Request

**IMPORTANT**: Read and use the PR template at `.github/pull_request_template.md`. The PR body format must strictly match the template structure.

1. Write PR body to temporary file (to avoid shell escaping issues)
2. Create PR:
   ```bash
   gh pr create --title "PR_TITLE" --body-file /tmp/pr-body.md --base main
   ```
3. For draft PRs: add `--draft` flag

#### PR Review Checklist (Pre-Submission)

**Code Quality**
- [ ] Full diff reviewed for correctness
- [ ] Consistency with project structure, style, and conventions
- [ ] Edge-case handling verified
- [ ] Error paths properly handled

**Testing**
- [ ] Appropriate tests added or updated
- [ ] Test suite passes (`devtools::test()`)
- [ ] Tests cover modified code paths
- [ ] GitHub Actions status checks pass
- [ ] Code coverage maintained or improved (check Codecov reports)

**Documentation**
- [ ] User-facing behavior documented
- [ ] API documentation complete
- [ ] Vignettes updated when workflows changed
- [ ] Release notes/NEWS.md updated for user-facing changes

**Metadata & Process**
- [ ] PR description complete and accurate
- [ ] Linked issue references correct (e.g., `Closes #123`)
- [ ] Labels applied appropriately
- [ ] Required reviewers added
- [ ] All status checks passing

### Manage PRs
```bash
gh pr edit --add-reviewer USERNAME    # Add reviewer
gh pr edit --add-label "bug"          # Add label
gh pr review                          # Submit review (approve, request changes, or comment)
```

**Important**: The agent should never merge or close a PR. Instead:
- For merge recommendation: File a review with "Approve" status and add a comment explaining why the PR is ready to merge
- For closure recommendation: File a review with "Comment" status explaining the reasons for closing (e.g., outdated, superseded, or no longer needed)

## Reference Material
- GitHub CLI documentation: https://cli.github.com/manual
- GitHub Issues API: https://docs.github.com/en/rest/issues
- GitHub Pull Requests API: https://docs.github.com/en/rest/pulls
- Repository metadata queries: `references/github_metadata.md`
- Issue implementation workflow: `implement-issue` skill (for detailed development steps)
- TDD workflow: `tdd-workflow` skill
- R code guidelines: `r-code` skill
- Documentation: `document` skill
- Vignettes: `vignette` skill
