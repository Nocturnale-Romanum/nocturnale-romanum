# Nocturnale Romanum

Dépôt des pièces grégoriennes de l'office nocturne (GABC/NABC pour Gregorio).

- `gabc/<ID>_marteo.gabc` : version de référence de marteo (compte GitHub **xmarteo**, arbitre) ; `gabc/<ID>_dcrochu.gabc` : propositions de dcrochu. `gabc/ORAL2.gabc` : alléluias pascals standard des huit modes.
- Fusion des propositions de dcrochu, décisions dans les PR, audits : skill **`fusion-repons`** (`.claude/skills/fusion-repons/SKILL.md`). Les règles sont dans `guidelines/fusion-repons.html` (et `.pdf`), seule référence.
- Une PR de fusion (`merge-<ID>`) ne modifie que `gabc/<ID>_marteo.gabc`. Vérifier à chaque commit que seuls les fichiers concernés sont ajoutés.
- Commits et PR en anglais ; guidelines en français.
- Seuls `guidelines/fusion-repons.html` et `.pdf` se modifient directement sur `main` ; tout le reste passe par une PR.
