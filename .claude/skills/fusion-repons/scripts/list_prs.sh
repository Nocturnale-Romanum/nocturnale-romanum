#!/bin/bash
# list_prs.sh : met à jour $NR_WORK/audit/prs.tsv (numéro, branche) et $NR_WORK/audit/open.json (numéro, brouillon, description)
# pour toutes les PR ouvertes, puis rafraîchit le clone. Entrées des scripts d'audit.
set -euo pipefail
. "$(dirname "$0")/env.sh"
git -C "$NR_CLONE" fetch -q origin
gh pr list --repo "$NR_REPO" --state open --limit 1000 --json number,headRefName \
  --jq '.[]|"\(.number)\t\(.headRefName)"' > "$NR_WORK/audit/prs.tsv"
gh pr list --repo "$NR_REPO" --state open --limit 1000 --json number,isDraft,body > "$NR_WORK/audit/open.json"
echo "$(wc -l < "$NR_WORK/audit/prs.tsv") PR ouvertes"
# Contrôle permanent : chaque PR de fusion ne touche qu'un fichier
gh pr list --repo "$NR_REPO" --state open --limit 1000 --json number,headRefName,files \
  --jq '.[]|select(.headRefName|startswith("merge-"))|select((.files|length)!=1)|"ATTENTION : #\(.number) touche \(.files|length) fichiers"'
