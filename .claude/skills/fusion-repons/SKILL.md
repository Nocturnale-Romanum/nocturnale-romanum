---
name: fusion-repons
description: Fusionner les propositions de dcrochu dans les fichiers gabc/<ID>_marteo.gabc de Nocturnale Romanum (une PR par répons), exécuter les décisions renseignées par marteo ou Thomas dans les PR, ajouter une règle aux guidelines et l'appliquer aux PR ouvertes, auditer les PR ouvertes. À utiliser dès qu'il est question de fusion de répons, de PR merge-<ID>, de décisions « Needs decision », de guidelines/fusion-repons, de dcrochu ou de marteo.
---

# Fusion des répons (Nocturnale Romanum)

Chaque répons existe en deux versions : `gabc/<ID>_marteo.gabc` (marteo, arbitre, compte GitHub **xmarteo**) et `gabc/<ID>_dcrochu.gabc` (propositions de dcrochu). Le travail consiste à reporter dans `_marteo` les propositions de dcrochu que les règles permettent d'adopter, **une PR par répons**, et à laisser à un humain ce que les règles ne tranchent pas.

## Sources de vérité

1. **`guidelines/fusion-repons.html`** (et son PDF), sur `main` : toutes les règles (R1 à R25 au 01/11/2026), leurs exceptions et les décisions consignées. **À lire en entier avant tout travail**, et à relire à chaque reprise : les règles évoluent. Ne jamais les recopier ailleurs (ni ici, ni dans une PR) : y renvoyer.
2. **Les PR** `merge-<ID>` : leur description (format ci-dessous) et leurs **commentaires** (décisions de marteo et de Thomas).
3. L'historique git des deux fichiers (`git log -- gabc/<ID>_dcrochu.gabc`), qui donne la base R20 et les justifications de dcrochu.

## Mise en place

```bash
. .claude/skills/fusion-repons/scripts/env.sh   # définit NR_REPO, NR_WORK, NR_CLONE, NR_SCRIPTS ; crée le clone au besoin
```

- Les branches de PR se construisent dans **`$NR_CLONE`, un clone dédié**, jamais dans la copie de travail de l'utilisateur (elle peut être synchronisée par OneDrive ou autre, `.git` compris : un `git add` y aurait des effets imprévus).
- `gh` doit être authentifié avec un compte qui peut pousser sur le dépôt.
- Attribution facultative : `NR_COMMIT_TRAILER` (ex. `Co-Authored-By: …`) et `NR_PR_FOOTER` sont ajoutés aux commits et aux PR.
- Python : `python3 -I` ; si l'environnement refuse `python3 -c` ou les heredocs, écrire les scripts dans des fichiers.

## Invariants (à vérifier à chaque commit)

- Une PR de fusion ne modifie **qu'un seul fichier**, `gabc/<ID>_marteo.gabc`. Les scripts `make_pr.sh` et `edit_pr.sh` le contrôlent (fichier unique, nombre de fichiers du dépôt inchangé) ; `list_prs.sh` signale toute PR ouverte qui touche plusieurs fichiers.
- Commits, titres et descriptions de PR **en anglais** ; guidelines **entièrement en français**.
- Seuls `guidelines/fusion-repons.html` et `.pdf` se modifient directement sur `main` (autorisation de Thomas, 29/10/2026). Tout autre changement passe par une PR.
- Le PDF se régénère après chaque modification du HTML : `google-chrome --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=guidelines/fusion-repons.pdf file://$PWD/guidelines/fusion-repons.html`.
- Une PR est **prête** s'il n'y a aucune « Needs decision », **brouillon** sinon. Les PR du sanctoral (ID à quatre chiffres) portent l'étiquette `sanctoral`.

## Format d'une description de PR

```
Merge of dcrochu's proposal into `gabc/<ID>_marteo.gabc` (*<incipit>*), following `guidelines/fusion-repons.pdf`. …
<paragraphe : base R20, ce que dcrochu a changé depuis>

## Backported      (tableau | Syllable | Before (marteo) | After | Rule |, puis « Marteo's rhythmic signs are kept everywhere (R1). »)
## Refused         (puces, ou « None. »)
## Needs decision  (puces « **SYL**: marteo `…` (kept), dcrochu `…`: … (Rn). », ou exactement « None. »)
## To check        (cases à cocher pour ce qui est adopté « et signalé », ou « None. »)
```

Quand une décision est exécutée, **mettre à jour la description** : déplacer le point de « Needs decision » vers « Backported » ou « Refused » (avec la règle ou « marteo's decision »), écrire `None.` si la section se vide, ajouter les cases à cocher prévues par la règle, puis passer la PR en prête. Une description qui contredit le fichier est une erreur (cf. #121, où le refus restait affiché alors que la correction était faite).

## Tâches

### A. Fusionner de nouveaux répons

1. Lister les répons à traiter (ceux qui ont `_marteo` et `_dcrochu`, hors liste des fusions déjà faites par marteo et hors exclusions des guidelines).
2. Par lots de 5, déléguer à des agents avec `agents/brief_lot.md` : chaque agent écrit `$NR_WORK/final/<ID>.md` (sections EDITS, COMMIT, PR, NOTES ; `## SKIP` si aucun édit, `## HOLD <mère> #<PR>` pour une fille dont la mère n'est pas fusionnée).
3. Pour chaque fichier : `scripts/make_pr.sh <ID>` (applique, vérifie le plafond de hauteurs `hl`, commite, pousse, ouvre la PR, pose l'étiquette). `HL_EXTRA=n` si l'agent a justifié des hauteurs au-dessus de `hl` (voir NOTES).
4. Relire les NOTES des agents : doutes, cas limites, corrections hors fusion à consigner.

### B. Exécuter les décisions renseignées dans les PR

1. `scripts/pending_comments.sh <date ISO>` : commentaires postés depuis la date, marqués quand ils sont postérieurs au dernier commit de la branche. Lire aussi les commentaires **en ligne** (inclus) et les reviews.
2. Formules consacrées de marteo : « rebase » / « merge automatically » / « rebase and close » → `gh pr merge <n> --rebase` après exécution ; « leave in review » / « leave the PR open » → `gh pr ready <n>` sans fusionner ; « ignore this for now » → ne rien faire.
3. Pour chaque décision : écrire `$NR_WORK/edits/<ID>.txt` (format de `apply_edits.py` : `OLD:`/`OLDALL:`/`OLDFIRST:` + `NEW:`, sous-chaîne exacte et unique du fichier **de la branche**) et `<ID>.commit`, puis `scripts/edit_pr.sh <ID>`. Recopier exactement le gabc/NABC donné par marteo quand il en donne un.
4. Mettre à jour la description (voir plus haut), répondre en commentaire (« Done: … »), fusionner ou passer en prête selon la consigne.
5. **Toute décision qui énonce un principe général** (« new rule », « in general… ») : l'ajouter aux guidelines, puis l'appliquer aux autres PR ouvertes (tâche C). Ne jamais oublier un commentaire : relancer `pending_comments.sh` à la fin.

### C. Nouvelle règle → guidelines → PR ouvertes

1. Rédiger la règle dans le HTML (en français, avec la date et l'auteur de la décision, un exemple et le numéro de PR), régénérer le PDF, commiter **les deux fichiers seulement** sur `main`.
2. Mettre à jour `agents/brief_lot.md` (section « Points d'attention »).
3. Repérer les PR concernées : audit par script (voir E) ou recensement des « Needs decision » (`scripts/decisions.py`).
4. Appliquer : directement pour quelques PR, ou par agents avec `agents/brief_decisions.md` (sorties dans `$NR_WORK/out/`, appliquées par `scripts/apply_out.sh`), en 4 lots d'environ 25 PR.
5. Une règle peut aussi rendre fausse une décision déjà prise dans une PR (ex. réduction `//` → `/` refusée avant la règle) : la reprendre, fichier **et** description.

### D. Pièces filles (R19)

Une fille (copie d'une autre pièce avec variantes) attend la fusion de sa mère. Ensuite : reporter dans la fille, passage par passage, ce qui a été **réellement fusionné** dans la mère (diff de `_marteo` de la mère avant/après les commits de fusion, plus les décisions de marteo en commentaire), puis traiter les propositions propres à la fille. La PR de la fille renvoie à celle de la mère.

### E. Audits des PR ouvertes

`scripts/list_prs.sh` (met à jour `$NR_WORK/audit/prs.tsv` et `open.json`), puis :

| Script | Contrôle |
|---|---|
| `audit_r13.py <clone> <prs.tsv>` | `//` restant après un punctum seul (R13, appliqué d'office par R23) |
| `audit_r13b.py` | `//` suivi d'une seule note finale un degré plus haut (second cas de R13 : seulement si dcrochu le propose) |
| `audit_r24.py` | syllabes sans NABC dans une section synthétique (`ob`…`cb`) où dcrochu en a (R24), et NABC ajouté hors section |
| `audit_r25.py` | correction adoptée dans le répons mais pas reportée dans une reprise (R25) |
| `oral2.py` | alléluias pascals comparés aux alléluias standard de `gabc/ORAL2.gabc` (R11) |
| `decisions.py`, `r5_study.py`, `r15_study.py` | recensement et classement des « Needs decision » (pour proposer des règles par lots) |

Chaque audit produit des **candidats** : les relire un par un avant d'agir (faux positifs fréquents : NABC simplement réaligné, mélodie différente, reprise qui n'est pas le même passage).

## Leçons apprises (session du 29/10 au 01/11/2026)

- **Les agents « corrigent » trop.** Leur rappeler que tout ce qui n'est pas couvert par une règle reste en « Needs decision » avec la version de marteo dans le fichier. Erreurs déjà commises : remplacement en masse des oriscus de salicus (interdit), report de marteo ignoré (si marteo a déjà fait un report « Backported… », ses choix de ce report font foi), SKIP alors qu'une correction d'office s'imposait (R23).
- **Base R20.** Seules les divergences entre dcrochu actuel et la base (marteo à la date du premier commit de dcrochu, ou dcrochu à la date du dernier report de marteo) sont des propositions. Un écart marteo ≠ dcrochu où dcrochu = base est un choix de marteo, à garder.
- **Un commentaire oublié** (#97, traité un jour en retard) : toujours relancer `pending_comments.sh` avant de rendre la main.
- **Corrections à reporter dans les reprises** (R25) : une correction faite dans le corps du répons vaut aussi pour ses repetenda identiques. Dcrochu l'oublie souvent.
- **Exceptions de marteo ≠ règles.** Une exception accordée sur une PR (« exceptionally, accept… ») ne devient une règle que si Thomas ou marteo la formulent comme telle.
- **Ne pas décider par analogie** une question que les règles laissent ouverte : poser la question (ex. R24 est née d'une telle question).
- **Hauteurs NABC** : plafond `hl` (R5 bis) vérifié par `check_hl.py` ; la lecture des hauteurs se fait de gauche à droite sans chevauchement (`clhhpihj` = `hh`, `hj`).
- **Vocabulaire NABC** : `pf` = *porrectus flexus* (pas pes flexus), `sf` = scandicus flexus, `vs` = virga strata, `pq` = pes quassus, `sa` = salicus, `ql`/`qi` = quilisma, `or` = oriscus, `pi` = pressus, `ob`/`cb` = crochets ouvrant/fermant une section de neumes synthétiques.
- **Outils de l'environnement** : certains environnements bloquent Grep/Glob natifs ou `python3 -c` ; écrire les scripts dans des fichiers. Sous zsh, `$i:g` est un modificateur : écrire `${i}`.
- **Conservation** : le travail doit vivre dans le dépôt (PR, guidelines, ce skill), pas dans un dossier temporaire ni dans une conversation (effacée après 30 jours par défaut).
