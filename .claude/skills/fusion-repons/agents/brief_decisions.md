# Consignes : application d'un lot de décisions aux PR ouvertes (Nocturnale Romanum)

> **Modèle.** Ce brief est celui des lots R5 du 01/11/2026, déjà appliqués. Pour un nouveau lot (nouvelle règle générale, décisions renseignées dans les PR…), remplace la section « Lots » et la liste reçue ; garde le reste (sortie, contrôles).

Variables : `$NR_CLONE` (clone git dédié) et `$NR_WORK` (espace de travail), définies par `scripts/env.sh` du skill ; le coordinateur te donne leurs valeurs.

Tu reçois une liste de PR ouvertes (`$NR_WORK/work/<lot>.md`) avec, pour chacune, ses points « Needs decision » qui citent R5. Pour chaque point, tu décides s'il relève d'un des lots ci-dessous et, si oui, tu prépares la modification. **Tu ne modifies aucun fichier du dépôt, tu ne commites rien, tu ne pousses rien, tu n'édites aucune PR** : un script applique ensuite tes fichiers.

Lis d'abord la règle R5 dans `guidelines/fusion-repons.html` (lis-le via `git -C $NR_CLONE show origin/main:guidelines/fusion-repons.html`) (paragraphe « Lots de décisions R5 »), ainsi que R5 bis (hauteurs), R5 ter (teneur), R3 bis (altérations) et R15 (formes des notes carrées).

## Lots (décisions de Thomas, 01/11/2026)

« Section synthétique » = dans le `_marteo` **de la branche de la PR**, la syllabe est après un `ob` pas encore fermé par un `cb` (le `cb` ferme la section sur la syllabe qui le porte). Pour le savoir, lis le fichier : `git -C $NR_CLONE show origin/merge-<ID>:gabc/<ID>_marteo.gabc`. « Verset » = après `<sp>V/</sp>`.

| Lot | Transformation de dcrochu | Décision |
|---|---|---|
| R5-1 | épisème NABC **ajouté** (`cl`→`cl-`, `ql-`, `ci-`, `vi-`, `pe-1`, `to-`…) | section synthétique : **adopter** + case « - [ ] … (R5, episema added in a synthetic section): check » dans To check. Hors crochets : rester en décision |
| R5-2 | virga → tractulus (`vi`→`ta`), mêmes notes | verset synthétique : **adopter sans signaler** (garde la hauteur de teneur de marteo, ex. `vihh`→`tahh`, R5 ter). Ailleurs : rester en décision |
| R5-3 | `pe` ↔ `peS` (ajout ou retrait du S) | comme R5-2 |
| R5-4 | virga + pes → scandicus (`vi-/pehi` → `scM1`, `scG-1`…), mêmes notes | **adopter** partout ; hauteurs de marteo gardées si dcrochu les retire ou les baisse (R5 bis) |
| R5-6 | clivis + prépunctis → `sf-` (`cl-ppt2`, `cl-pp2` → `sf-`) | **adopter** partout, NABC seulement : le bémol, le regroupement gabc ou l'espacement liés au bémol restent en décision ou refusés comme avant |
| R5-9 | deux clivis → porrectus flexus (`clcl` → `pf`) | **adopter** partout (avec la lettre/l'espacement de dcrochu qui n'ont de sens qu'avec ce neume) |

Restent en décision (ne rien changer) : épisème **retiré**, `tr-1`→`tr-3`, pes avec prépunctis → deux tractulus, et **tout point où la transformation est liée à un changement mélodique, de forme des notes carrées (R15), de liquescence, de groupement (R12) ou d'altération**, sauf R5-6 qui s'adopte pour sa partie NABC seule. Un point qui mélange un lot adoptable et autre chose : adopte seulement la partie du lot si elle est séparable sans ambiguïté, sinon laisse-le entier en décision. Au moindre doute : décision (on ne change rien).

## Sortie, pour chaque PR où tu adoptes au moins une chose

1. `$NR_WORK/out/<ID>.txt` : édits au format `OLD:`/`NEW:` (sous-chaîne exacte et **unique** du `_marteo` de la **branche** `origin/merge-<ID>`, avec assez de contexte ; `OLDALL:` si le même passage revient à l'identique, par ex. dans une reprise — R25). Vérifie par un script (`data.count(old) == 1`) sur le fichier de la branche.
2. `$NR_WORK/out/<ID>.commit` : message en anglais, titre `<ID>: Adopt dcrochu's NABC glyphs (R5 batches)`, puis une puce par syllabe.
3. `$NR_WORK/out/<PR>.body.md` : la **description complète mise à jour** de la PR (récupère-la avec `gh pr view <PR> --repo Nocturnale-Romanum/nocturnale-romanum --json body --jq .body`) : retire de « Needs decision » les points adoptés (ou réécris-les s'il n'en reste qu'une partie), ajoute une ligne au tableau « Backported » par point adopté (règle : `R5 (batch R5-n, Thomas's decision, 01/11)`), ajoute les cases R5-1 dans « To check ». Si « Needs decision » devient vide, écris exactement `None.`. Ne change rien d'autre à la description.

Si `python3 -c` ou les heredocs Python sont refusés, écris tes scripts dans `$NR_WORK/work/r5_agentN/` puis `python3 -I fichier.py`.

À la fin, réponds par un résumé très court : par PR, le nombre de points adoptés par lot et s'il reste des décisions ; puis les cas douteux.
