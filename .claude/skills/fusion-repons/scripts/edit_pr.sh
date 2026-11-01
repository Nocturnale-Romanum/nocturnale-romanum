#!/bin/bash
# edit_pr.sh <ID> : ajoute un commit à la branche merge-<ID> d'une PR existante.
# Applique $NR_WORK/edits/<ID>.txt (format apply_edits.py), commite avec $NR_WORK/edits/<ID>.commit,
# vérifie que seul gabc/<ID>_marteo.gabc change, puis pousse.
set -euo pipefail
. "$(dirname "$0")/env.sh"
ID=$1
cd "$NR_CLONE"
git fetch -q origin
git checkout -q -f --detach origin/main && git clean -fdq
git checkout -q -f -B merge-$ID origin/merge-$ID
N0=$(git ls-tree -r HEAD | wc -l)
python3 -I "$NR_SCRIPTS/apply_edits.py" "$NR_CLONE" "$ID" "$NR_WORK/edits/$ID.txt"
CH=$(git status --porcelain)
[ "$CH" = " M gabc/${ID}_marteo.gabc" ] || { echo "ARRÊT : état inattendu : $CH"; exit 1; }
cp "$NR_WORK/edits/$ID.commit" "$NR_WORK/edits/$ID.msg"
[ -n "${NR_COMMIT_TRAILER:-}" ] && printf '\n%s\n' "$NR_COMMIT_TRAILER" >> "$NR_WORK/edits/$ID.msg"
git commit -q -o "gabc/${ID}_marteo.gabc" -F "$NR_WORK/edits/$ID.msg"
[ "$(git diff --name-only origin/merge-$ID HEAD)" = "gabc/${ID}_marteo.gabc" ] || { echo "ARRÊT : fichiers inattendus"; exit 1; }
[ "$(git ls-tree -r HEAD | wc -l)" = "$N0" ] || { echo "ARRÊT : nombre de fichiers changé"; exit 1; }
[ "$(git diff --name-only origin/main...HEAD)" = "gabc/${ID}_marteo.gabc" ] || { echo "ARRÊT : la PR touche d'autres fichiers"; exit 1; }
git show --stat HEAD | tail -1
git push -q origin merge-$ID 2>&1 | grep -v "^remote:" || true
git checkout -q -f --detach origin/main
