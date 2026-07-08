# Commit Message Format

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