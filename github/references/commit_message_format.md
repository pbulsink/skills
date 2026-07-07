# GitHub CLI Workflows

## Repository ID Retrieval
To get the repository owner/name for the current project:

```powershell
$remote = git remote get-url origin

if ($remote -match '[:/]([^/]+)/([^/]+?)(?:\.git)?$') {
    "$($matches[1])/$($matches[2])"
}
```

## View Resources
```bash
gh issue view 123          # View issue #123
gh pr view 456            # View PR #456
gh issue list               # List issues
gh pr list                  # List pull requests
```

## Commit Message Format

Use conventional commits with the following format:

```
<type>: <description>

<body>

- Closes #N
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

### Examples

```bash
# Feature
feat: add `create_skill()`

Generates a new skill directory with a SKILL.md template.

- Closes #3

# Bug fix
fix: handle empty input in `process_data()`

Checks for empty data frames before processing and throws appropriate error.

- Fixes #12

# Documentation
docs: update README installation section

Adds example commands for Windows and Linux users.

# Refactor
refactor: simplify `fetch_records()` logic

Extracts pagination handling into separate helper function.
```