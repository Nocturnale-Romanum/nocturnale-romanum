#!/bin/bash
# pending_comments.sh [depuis] : commentaires (généraux et en ligne) postés sur les PR ouvertes depuis une date ISO
# (défaut : 30 jours), hors comptes de bots, avec le dernier commit de la branche pour repérer ceux qui n'ont pas été traités.
set -euo pipefail
. "$(dirname "$0")/env.sh"
SINCE=${1:-$(date -u -d '30 days ago' +%Y-%m-%dT%H:%M:%SZ)}
gh pr list --repo "$NR_REPO" --state open --limit 1000 --json number --jq '.[].number' | sort > "$NR_WORK/audit/open_numbers.txt"
{
  gh api --paginate "repos/$NR_REPO/issues/comments?since=$SINCE&per_page=100" \
    --jq '.[]|"\(.issue_url|split("/")|last)\t\(.created_at)\t\(.user.login)\tC\t\(.body|gsub("\n";" ")|.[0:300])"'
  gh api --paginate "repos/$NR_REPO/pulls/comments?since=$SINCE&per_page=100" \
    --jq '.[]|"\(.pull_request_url|split("/")|last)\t\(.created_at)\t\(.user.login)\tL \(.path):\(.line)\t\(.body|gsub("\n";" ")|.[0:300])"'
} | sort -k1,1n -k2,2 | while IFS=$'\t' read -r n d who kind body; do
  grep -qx "$n" "$NR_WORK/audit/open_numbers.txt" || continue
  last=$(gh pr view "$n" --repo "$NR_REPO" --json commits --jq '[.commits[].committedDate]|max')
  flag=""; [[ "$d" > "$last" ]] && flag="  <-- postérieur au dernier commit"
  printf '#%s %s %s %s%s\n    %s\n' "$n" "$d" "$who" "$kind" "$flag" "$body"
done
