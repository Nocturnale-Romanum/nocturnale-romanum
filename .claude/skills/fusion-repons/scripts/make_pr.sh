#!/bin/bash
# make_pr.sh <ID> : crée la branche merge-<ID> depuis origin/main dans $NR_CLONE, applique $NR_WORK/final/<ID>.md,
# commite, vérifie qu'un seul fichier change, pousse et ouvre la PR (brouillon s'il y a des décisions).
# Format de final/<ID>.md : voir ../agents/brief_lot.md (sections EDITS, COMMIT, PR, NOTES ; ## SKIP ; ## HOLD).
set -euo pipefail
. "$(dirname "$0")/env.sh"
ID=$1
F=$NR_WORK/final/$ID.md
if grep -q '^## SKIP' "$F"; then echo "SKIP $ID : $(grep -A2 '^## SKIP' "$F" | tail -n +2 | tr '\n' ' ')"; exit 0; fi
if grep -q '^## HOLD' "$F"; then echo "HOLD $ID : $(grep '^## HOLD' "$F")"; exit 0; fi
if gh pr list --repo "$NR_REPO" --state all --head merge-$ID --json number -q '.[].number' | grep -q .; then echo "ARRÊT : une PR existe déjà pour $ID"; exit 1; fi
cd "$NR_CLONE"
git fetch -q origin
git checkout -q -f --detach origin/main && git clean -fdq
git branch -q -D merge-$ID 2>/dev/null || true
git switch -q -c merge-$ID origin/main
N0=$(git ls-tree -r HEAD | wc -l)
cp gabc/${ID}_marteo.gabc "$NR_WORK/final/$ID.before"
awk '/^## EDITS/{f=1;next} /^## /{f=0} f' "$F" > "$NR_WORK/final/$ID.edits"
python3 -I "$NR_SCRIPTS/apply_edits.py" "$NR_CLONE" "$ID" "$NR_WORK/final/$ID.edits"
HL_EXTRA=${HL_EXTRA:-0} python3 -I "$NR_SCRIPTS/check_hl.py" "$NR_WORK/final/$ID.before" gabc/${ID}_marteo.gabc
CH=$(git status --porcelain)
[ "$CH" = " M gabc/${ID}_marteo.gabc" ] || { echo "ARRÊT : état inattendu avant commit :"; echo "$CH"; git checkout -q -f --detach origin/main; exit 1; }
awk '/^## COMMIT/{f=1;next} /^## PR/{f=0} f' "$F" | sed -e '/./,$!d' > "$NR_WORK/final/$ID.commit"
[ -n "${NR_COMMIT_TRAILER:-}" ] && printf '\n%s\n' "$NR_COMMIT_TRAILER" >> "$NR_WORK/final/$ID.commit"
git commit -q -o "gabc/${ID}_marteo.gabc" -F "$NR_WORK/final/$ID.commit"
[ "$(git diff --name-only origin/main HEAD)" = "gabc/${ID}_marteo.gabc" ] || { echo "ARRÊT : fichiers inattendus"; exit 1; }
[ "$(git ls-tree -r HEAD | wc -l)" = "$N0" ] || { echo "ARRÊT : nombre de fichiers changé"; exit 1; }
git show --stat HEAD | tail -1
awk '/^## PR/{f=1;next} /^## NOTES/{f=0} f' "$F" > "$NR_WORK/final/$ID.pr"
[ -n "${NR_PR_FOOTER:-}" ] && printf '\n%s\n' "$NR_PR_FOOTER" >> "$NR_WORK/final/$ID.pr"
git push -q -u origin merge-$ID 2>&1 | grep -v "^remote:" || true
ND=$(awk '/^## Needs decision/{f=1;next} /^## /{f=0} f' "$NR_WORK/final/$ID.pr" | grep -v '^\s*$' | grep -vx 'None\.' || true)
DRAFT=""; [ -n "$ND" ] && DRAFT="--draft"
gh pr create --repo "$NR_REPO" --base main --head merge-$ID $DRAFT \
  --title "$(head -1 "$NR_WORK/final/$ID.commit")" --body-file "$NR_WORK/final/$ID.pr"
# Les PR du sanctoral (ID à quatre chiffres) portent l'étiquette « sanctoral », prioritaire
if [[ $ID =~ ^[0-9]{4} ]]; then
  N=$(gh pr list --repo "$NR_REPO" --head merge-$ID --json number -q '.[0].number')
  gh api -X POST repos/$NR_REPO/issues/$N/labels -f "labels[]=sanctoral" -q '.[0].name' >/dev/null
fi
echo "statut : ${DRAFT:-prête}"
git checkout -q -f --detach origin/main
