---
name: create-issue
trigger: create GitHub issues
description: This skill should be used when asked to create, file, or open a GitHub issue, or when planning new features or functions that need to be tracked for the package repository.
compatibility: Requires the `gh` CLI and an authenticated GitHub session.
---

# Create a GitHub issue

## Prerequisites
Verify authentication by running `gh auth status`. If not authenticated, instruct the user to authenticate before proceeding.

## Issue Construction

### 1. Determine Repository ID
Retrieve the repository node ID (i.e. <OWNER>/<REPO>) from `references/github_metadata.md` using:
```powershell
$remote = git remote get-url origin

if ($remote -match '[:/]([^/]+)/([^/]+?)(?:\.git)?$') {
    "$($matches[1])/$($matches[2])"
}
```

### 2. Select Issue Type and Title
Choose the most appropriate issue type based on the request. Use conventional commit prefixes for titles (e.g., `feat:`, `fix:`, `docs:`, `chore:`).

| Type | ID | Recommended Prefix |
|---|---|---|
| Feature | `IT_kwDOAB1wHM4AA6lY` | `feat:` |
| Bug | `IT_kwDOAB1wHM4AA6lV` | `fix:` |
| Task | `IT_kwDOAB1wHM4AA6lT` | `chore:` |

### 3. Prepare Issue Body
Construct a Markdown body file containing the following sections based on the issue type:

**Required for all types:**
- `## Summary`: A single user story sentence (e.g., `> As a [role], in order to [goal], I would like to [feature].`).

**Optional/Conditional Sections:**
- `## Details`: Contextual implementation details or package requirements.
- `## Proposed signature` (**Feature only**): The proposed R function signature and argument descriptions.
- `## Behavior` (**Feature and Bug**): Detailed expected behavior, edge cases (Features), or current broken behavior and reproduction steps (Bugs).
- `## References`: Links to external documentation, related code, or issue trackers.

### 4. Execution
Execute the creation using the helper script:
```bash
./scripts/gh_create_issue.sh <repoId> "<title>" /tmp/issue_body.md <typeId>
```
*Ensure the body content is written to a temporary file first.*

## Reference Material
For detailed GraphQL queries and ID lookups, consult `references/github_metadata.md`.
