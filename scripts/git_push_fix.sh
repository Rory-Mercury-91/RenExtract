#!/usr/bin/env bash
set -e

# Add and commit
git add -A
if git diff --cached --quiet; then
  echo "No staged changes to commit"
else
  git commit -m "v1.2.23-Fix: ports configurable; hotkey default 45000; safer cleanup and tests"
fi

# Create or update tag
if git rev-parse "v1.2.23-Fix" >/dev/null 2>&1; then
  echo "Tag v1.2.23-Fix exists, forcing update"
  git tag -f v1.2.23-Fix -m "v1.2.23-Fix: configurable ports and safer port cleanup"
else
  git tag v1.2.23-Fix -m "v1.2.23-Fix: configurable ports and safer port cleanup"
fi

# Push branch and tags
branch=$(git rev-parse --abbrev-ref HEAD)
echo "Pushing branch $branch to origin"
git push origin "$branch"

echo "Pushing tags"
git push origin --tags

echo "Done"
