# Get Repository ID

Extract the repository owner/name for GitHub API operations.

```powershell
$remote = git remote get-url origin

if ($remote -match '[:/]([^/]+)/([^/]+?)(?:\.git)?$') {
    "$($matches[1])/$($matches[2])"
}
```