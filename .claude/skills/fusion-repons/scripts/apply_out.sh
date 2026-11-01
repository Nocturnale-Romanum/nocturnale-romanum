#!/bin/bash
# apply_out.sh : applique les sorties d'agents de $NR_WORK/out/ (voir ../agents/brief_decisions.md) :
#   <ID>.txt + <ID>.commit  -> commit sur la branche merge-<ID> (edit_pr.sh)
#   <PR>.body.md            -> nouvelle description de la PR ; passage en « ready » s'il ne reste aucune décision
set -uo pipefail
. "$(dirname "$0")/env.sh"
cd "$NR_WORK"
for f in out/*.txt; do
  [ -e "$f" ] || continue
  ID=$(basename "$f" .txt)
  cp "out/$ID.txt" "edits/$ID.txt"
  cp "out/$ID.commit" "edits/$ID.commit"
  echo "$ID: $(bash "$NR_SCRIPTS/edit_pr.sh" "$ID" 2>&1 | tail -1)"
done
for f in out/*.body.md; do
  [ -e "$f" ] || continue
  PR=$(basename "$f" .body.md)
  [ -n "${NR_PR_FOOTER:-}" ] && ! grep -qF "$NR_PR_FOOTER" "$f" && printf '\n%s\n' "$NR_PR_FOOTER" >> "$f"
  gh api -X PATCH "repos/$NR_REPO/pulls/$PR" -F "body=@$f" --jq .number >/dev/null || { echo "#$PR : échec de la description"; continue; }
  nd=$(awk '/^## Needs decision/{f=1;next} /^## /{f=0} f' "$f" | grep -c '^- ' || true)
  dr=$(gh pr view "$PR" --repo "$NR_REPO" --json isDraft --jq .isDraft)
  if [ "$nd" = 0 ] && [ "$dr" = true ]; then gh pr ready "$PR" --repo "$NR_REPO" >/dev/null && echo "#$PR : ready"; fi
done
