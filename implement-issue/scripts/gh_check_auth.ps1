# Check GitHub CLI Authentication

Verify that the gh CLI is authenticated before performing GitHub operations.

```powershell
gh auth status
```

If not authenticated, stop and instruct the user to authenticate with `gh auth login` before proceeding.