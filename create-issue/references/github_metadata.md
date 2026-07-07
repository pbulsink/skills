# GitHub Metadata

## Repository Owner/ID Information Lookup
To retrieve the repository ID (<OWNER>/<REPO>) for the current project, run this command in the project root:

```powershell
$remote = git remote get-url origin

if ($remote -match '[:/]([^/]+)/([^/]+?)(?:\.git)?$') {
    "$($matches[1])/$($matches[2])"
}
```

## Issue Type IDs
| Type | ID | Use for |
|---|---|---|
| Task | `IT_kwDOAB1wHM4AA6lT` | A specific piece of work |
| Bug | `IT_kwDOAB1wHM4AA6lV` | An unexpected problem or behavior |
| Feature | `IT_kwDOAB1wHM4AA6lY` | A request, idea, or new functionality |

## Lookup Query for Issue Types
To verify or update issue type IDs, run the following command, replacing `<OWNER>` and `<REPO>` with the appropriate values for the repository:

```bash
gh api graphql -f query='{ repository(owner: "<OWNER>", name: "<REPO>") { issueTypes(first: 20) { nodes { id name description } } } }'
```
