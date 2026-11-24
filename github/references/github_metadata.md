# GitHub Metadata

## Repository Owner/ID Information Lookup
To retrieve the repository's owner/name (<OWNER>/<REPO>) for the current project, run this command in the project root:

```powershell
$remote = git remote get-url origin

if ($remote -match '[:/]([^/]+)/([^/]+?)(?:\.git)?$') {
    "$($matches[1])/$($matches[2])"
}
```

## Repository Node ID (required for issue creation)
`gh_create_issue.sh` requires the repository's **GraphQL node ID** (base64), not `owner/name`. Passing `<OWNER>/<REPO>` fails with "Could not resolve to a node with the global id". Look it up with:

```bash
gh api graphql -f query='{ repository(owner: "<OWNER>", name: "<REPO>") { id } }' --jq '.data.repository.id'
```

## Issue Type IDs (per-repository!)
Issue type IDs are **not universal** — every repository has its own set. The values below are examples only; a mismatch fails with "Issue type cannot be found in this organization". Always run the lookup query before creating an issue:

| Example Type | Example ID | Use for |
|---|---|---|
| Task | `IT_kwDOAB1wHM4AA6lT` | A specific piece of work |
| Bug | `IT_kwDOAB1wHM4AA6lV` | An unexpected problem or behavior |
| Feature | `IT_kwDOAB1wHM4AA6lY` | A request, idea, or new functionality |

## Lookup Query for Issue Types and Repo ID
To get the repository node ID *and* its issue type IDs in one call, run the following command, replacing `<OWNER>` and `<REPO>` with the appropriate values:

```bash
gh api graphql -f query='{ repository(owner: "<OWNER>", name: "<REPO>") { id issueTypes(first: 20) { nodes { id name } } } }' --jq '.data.repository | .id, (.issueTypes.nodes[] | "\(.name): \(.id)")'
```