# Variables communes aux scripts de fusion (à sourcer : . env.sh)
#   NR_REPO    dépôt GitHub (défaut : Nocturnale-Romanum/nocturnale-romanum)
#   NR_WORK    espace de travail jetable : final/, edits/, bodies/, audit/ (défaut : $TMPDIR/nr-work)
#   NR_CLONE   clone git dédié aux branches de PR, distinct de la copie de travail de l'utilisateur
#              (défaut : $NR_WORK/clone ; créé au besoin)
#   NR_COMMIT_TRAILER, NR_PR_FOOTER   lignes d'attribution ajoutées aux commits et aux PR (facultatives)
NR_REPO=${NR_REPO:-Nocturnale-Romanum/nocturnale-romanum}
NR_WORK=${NR_WORK:-${TMPDIR:-/tmp}/nr-work}
NR_CLONE=${NR_CLONE:-$NR_WORK/clone}
NR_SCRIPTS=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export NR_REPO NR_WORK NR_CLONE NR_SCRIPTS
mkdir -p "$NR_WORK/final" "$NR_WORK/edits" "$NR_WORK/bodies" "$NR_WORK/audit"
[ -d "$NR_CLONE/.git" ] || git clone -q "https://github.com/$NR_REPO.git" "$NR_CLONE"
