#!/usr/bin/env bash
# Phase 1, step 1: create the GitHub repository "student-info-system" and push.
# Requires git + GitHub CLI (https://cli.github.com), authenticated via `gh auth login`.
set -euo pipefail

gh repo create student-info-system --public --source=. --remote=origin --push \
  --description "Cloud-ready Student Information System (Python, JSON/XML)"

gh repo edit --add-topic python --add-topic student-management \
  --add-topic cli --add-topic docker --enable-issues

gh issue create --title "Add CSV import/export" --label enhancement \
  --body "Allow bulk import and export of student records."
gh issue create --title "Add REST API layer" --label enhancement \
  --body "Expose StudentService over HTTP for cloud deployment."
gh issue create --title "Add database backend" --label enhancement \
  --body "Implement StudentRepository for SQLite/PostgreSQL."

git push origin --tags
gh release create v1.1.0 --title "v1.1.0" --notes-file CHANGELOG.md
echo "Done. Enable branch protection on main and require the CI check."
