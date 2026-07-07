#!/bin/bash
# Usage: ./gh_create_issue.sh <repoId> <title> <bodyFile> <typeId>

REPO_ID=$1
TITLE=$2
BODY_FILE=$3
TYPE_ID=$4

if [[ -z "$REPO_ID" || -z "$TITLE" || -z "$BODY_FILE" || -z "$TYPE_ID" ]]; then
    echo "Usage: $0 <repoId> <title> <bodyFile> <typeId>"
    exit 1
fi

# Determine Repo Owner and Name from git remote
REMOTE_URL=$(git remote get-url origin)
if [[ -z "$REMOTE_URL" ]]; then
    echo "Error: Not a git repository or no 'origin' remote found."
    exit 1
fi

# Extract owner/name using regex (handles both https and ssh formats)
# This matches the pattern after the last slash before .git or end of string
if [[ $REMOTE_URL =~ [^/]+/[^/?]+.git$ ]]; then
    CLEAN_URL="${REMOTE_URL%.git}"
else
    CLEAN_URL="$REMOTE_URL"
fi

# Extract owner and name: format is "owner/name"
REPO_PATH=$(echo "$CLEAN_URL" | grep -oE '[^/]+/[^/]+$')

if [[ -z "$REPO_PATH" ]]; then
    echo "Error: Could not parse owner/repo from remote URL: $REMOTE_URL"
    exit 1
fi

gh api graphql \
  -f query='mutation($repoId:ID!, $title:String!, $body:String!, $typeId:ID!) {
    createIssue(input:{repositoryId:$repoId, title:$title, body:$body, issueTypeId:$typeId}) {
      issue { url }
    }
  }' \
  -f repoId="$REPO_ID" \
  -f title="$TITLE" \
  -f body="$(cat "$BODY_FILE")" \
  -f typeId="$TYPE_ID"
