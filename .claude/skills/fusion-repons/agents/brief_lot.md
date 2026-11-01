# Consignes : fusion des propositions de dcrochu dans `ID_marteo.gabc` (Nocturnale Romanum)

Tu prépares, pour chaque répons de ton lot, un fichier `final/<ID>.md` qui décrit les modifications à apporter à `gabc/<ID>_marteo.gabc`. **Tu ne modifies aucun fichier du dépôt, tu ne commites rien, tu ne pousses rien, tu n'ouvres aucune PR** : un script s'en charge ensuite à partir de ton fichier.

Répertoires (chemins absolus) :
- Variables : `$NR_CLONE` (clone git dédié) et `$NR_WORK` (espace de travail), définies par `scripts/env.sh` du skill ; le coordinateur te donne leurs valeurs.
- Dépôt (clone git, lecture seule) : `$NR_CLONE`. **N'utilise jamais l'arbre de travail** (il change pendant que d'autres scripts tournent) : lis tout via `git -C $NR_CLONE show origin/main:gabc/<fichier>` et `git -C $NR_CLONE log origin/main -- gabc/<fichier>`. Pas de `checkout`, `switch`, `reset`, `fetch`, `commit`, `push`.
- Règles : `guidelines/fusion-repons.html` (lis-le via `git -C $NR_CLONE show origin/main:guidelines/fusion-repons.html`) (**à lire en entier avant de commencer** ; règles R1 à R25, avec leurs exceptions et les décisions consignées).
- Ton espace de travail : `$NR_WORK/work/<lot>/` (scripts, extraits). Si le shell refuse `python3 -c` ou les heredocs Python, écris tes scripts dans des fichiers puis lance `python3 -I fichier.py`.
- Sortie : `$NR_WORK/final/<ID>.md`, un par répons.

## Méthode, pour chaque répons

1. **Base R20.** Repère le premier commit de dcrochu sur `<ID>_dcrochu.gabc` (`git log --reverse --format='%h %ad %an %s' --date=short origin/main -- gabc/<ID>_dcrochu.gabc`). La base B est `_marteo` à ce commit (`git show <commit>:gabc/<ID>_marteo.gabc`). Si `_marteo` n'existait pas encore, ou si l'historique de `_marteo` montre que marteo est parti de dcrochu (« dcrochu as of… », « Backported dcrochu… »), la base B est `_dcrochu` au moment où marteo l'a repris. D = `_dcrochu` actuel, M = `_marteo` actuel. **Si marteo a déjà fait un report des propositions de dcrochu** (commit « Backported… », « Modifications intégrées », « NABC addivi »…, même pour une pièce hors des 212), ses choix de ce report font foi : la base B est `_dcrochu` à la date de ce report, et on ne revient pas sur ce qu'il a alors écarté ou modifié. Seules les divergences **D ≠ B** sont des propositions de dcrochu ; ce qui est D ≠ M mais D = B est un changement de marteo, qu'on garde. Les messages de commit de dcrochu (`git log origin/main -- gabc/<ID>_dcrochu.gabc`) donnent souvent la justification (R3 cas 5). Dans `_dcrochu`, un second en-tête est parfois collé : ne lis le corps qu'après le **dernier** `%%`.
2. Aligne syllabe par syllabe (texte, gabc, nabc) et applique les règles des guidelines à chaque proposition : **adoptée** (Backported), **refusée** (Refused), ou **renvoyée à un humain** (Needs decision : on garde alors la version de marteo dans le fichier).
3. Points d'attention (erreurs déjà commises) :
   - Plafond `hl` (R5 bis) : une hausse de dcrochu est plafonnée à `hl` si les notes carrées ne dépassent pas `k`. Si les notes carrées du neume montent au-dessus de `k`, on prend la valeur de dcrochu même au-dessus de `hl` (ex. `sahn` sur des notes jusqu'à m) ; une hauteur de marteo déjà au-dessus de `hl` reste telle quelle. Dans ce cas, écris `HL_EXTRA: <nombre de hauteurs > hl ajoutées>` dans NOTES.
   - R13 : `//` → `/` après un punctum seul (épisème compris), **même si marteo l'avait refusé auparavant** ; second cas : `//` → `/` quand l'espacement est suivi d'une seule note jusqu'à la fin de la syllabe, un degré au-dessus de la note précédente, **seulement si dcrochu le propose** (pas d'office).
   - R7 : modifications de `lsc` adoptées (et signalées). Autres lettres (`lsi`, `lse`, `lsl`, `lsal`, `lst`, `lt…`) : **ajout ou suppression adoptés**, avec une case « check on the manuscript » dans To check ; **changement de lettre ou de position** (y compris une lettre déplacée d'une syllabe à l'autre) → humain. Si dcrochu change aussi le neume qui porte la lettre, la lettre suit la décision sur le neume. Une `lse` ajoutée par dcrochu dans la reprise finale (fin de fichier) est **refusée**.
   - R5 : glyphe de base, modificateurs, **subpunctis/prepunctis** (`sut2` → `suu2`…) → humain. Vérifie les équivalences (`vi>` = `cl~`).
   - R8 : mots du texte → toujours marteo (Refused) ; accents et ponctuation → dcrochu, signalés.
   - R21 : si les deux versions sont complètement différentes (autre source pour toute la pièce), garde marteo en bloc et ne traite que les parties communes (Gloria Patri…).
   - R2 : syllabation de dcrochu, sauf les exceptions du tableau ; préfixe *trans-* entier, signaler toute coupe *tran/s…*.
   - R11 : alléluia pascal standard : `gabc/ORAL2.gabc` (alléluias standard des 8 modes) arbitre chaque proposition de dcrochu (adopter si ORAL2 lui donne raison, garder marteo sinon, humain si ORAL2 ne donne raison à aucun) ; on ne recopie jamais ORAL2. Un alléluia qui ne correspond à aucun mode d'ORAL2 suit les règles communes.
   - R24 : dans une section synthétique de marteo (NABC encadré par `ob` … `cb`, verset ou répons), reprendre le NABC de dcrochu sur les syllabes sans neumes chez marteo entourées de syllabes neumées, si la mélodie de la syllabe est la même ; sauf versions complètement différentes (R21) et NABC simplement décalé d'une syllabe (décision).
   - R12 : tout changement de groupement gabc refusé. R16 : reprise après le verset, forme de marteo.
   - R19 : si le répons est une « fille » d'un autre (copie avec variantes), dis-le dans NOTES. Si la mère a une PR encore ouverte (`gh pr list --repo Nocturnale-Romanum/nocturnale-romanum --state all --head merge-<IDmère>`), rédige quand même le fichier complet, mais **ajoute en première ligne** `## HOLD <IDmère> #<PR>` : la PR de la fille attendra la fusion de la mère.
   - Remplacements en masse à compléter au passage (R8) : `X@Yo`/`X!Yo` → `XYO1`, *san/ctus* → *sanc/tus*, strophas abrégées développées (R14).
4. **S'il n'y a aucun édit à faire** dans `_marteo` (rien à adopter, même s'il y a des refus ou des décisions), écris un fichier qui commence par `## SKIP` suivi d'une ligne d'explication ; s'il y a des décisions humaines, décris-les précisément sur cette ligne (syllabe, marteo vs dcrochu, règle). On n'ouvre pas de PR sans diff. **R23** : les réductions R13 et les syllabations non conformes aux exceptions de R2 (quó/ni/am, po/te…, í/de/o, dis/per, sic/ut, di/gnis, a/gnus, sanc/tus, trans- entier) se corrigent **d'office, même sans aucune proposition de dcrochu** : elles justifient à elles seules une PR (pas de SKIP dans ce cas). Les autres corrections d'office (R5 ter, R14, remplacements en masse) ne sont faites que s'il y a déjà une PR ; sinon, signale-les sur la ligne SKIP.
   - R8, coquilles : une lettre manquante ou en trop est adoptée et signalée seulement si c'est **certainement** une coquille ; au moindre doute, et pour toute variante de graphie (oboedientia/obedientia, Genetricis/Genitricis, pœ/pæ…), Needs decision.

## Format de `final/<ID>.md` (respecte exactement les titres)

```
## EDITS
OLD: <texte exact, présent une seule fois dans l'actuel gabc/<ID>_marteo.gabc>
NEW: <remplacement>
WHY: <règle, en une ligne>
OLDALL: <texte exact remplacé partout (au moins une occurrence)>
NEW: <remplacement>
WHY: …

## COMMIT
<ID>: <titre en anglais, ≤ 72 caractères, ex. "Backported dcrochu's changes except …">

- <puces en anglais, une par groupe de modifications>
- Refused: …
- Kept for decision: …

## PR
<description en anglais, au format ci-dessous>

## NOTES
<remarques en français pour le coordinateur : doutes, cas limites>
```

Chaque `OLD:` doit être une sous-chaîne **exacte et unique** de `_marteo` actuel (prends assez de contexte, ex. la syllabe précédente). Vérifie-le avec un petit script (`data.count(old) == 1`). Les édits s'appliquent dans l'ordre. N'utilise pas `OLD:` qui chevauche un autre édit.

Section PR (en anglais), modèle :

```
Merge of dcrochu's proposal into `gabc/<ID>_marteo.gabc` (*<incipit>*), following `guidelines/fusion-repons.pdf`. Only `<ID>_marteo.gabc` is changed; the selection on the website is left to marteo.

<un paragraphe : base R20 (date, commit), ce que dcrochu a changé depuis>

## Backported

| Syllable | Before (marteo) | After | Rule |
|---|---|---|---|
| … | `…` | `…` | R… |

Marteo's rhythmic signs are kept everywhere (R1).

## Refused

- **SYLlable**: … (R…).   (ou « None. »)

## Needs decision

- **SYLlable**: marteo `…` (kept), dcrochu `…`: … (R…).   (ou exactement « None. » s'il n'y en a aucune)

## To check

- [ ] … (éléments adoptés « et signalés » : lsc, accents/ponctuation, R3 cas 1/5, plafonds hl, découpages R10…)   (ou « None. »)
```

La PR sera ouverte en brouillon s'il y a au moins une « Needs decision », prête sinon. Dans les tableaux Markdown, échappe les `|` du code (`\|`).

À la fin, réponds par un résumé très court : pour chaque ID, « PR prête », « brouillon (N décisions) » ou « SKIP », et les doutes principaux.

## Règles ajoutées le 01/11 (soir)
- R5 : `to` → `toM1` proposé par dcrochu : **refusé** (garder marteo).
- R17 : dcrochu avance l'`ob` d'un verset synthétique pour y inclure des syllabes du début du verset que marteo a laissées sans neumes : **adopter** avec ses neumes.
- R25 : une correction adoptée sur un passage du répons est **reportée d'office** sur le même passage dans les reprises (repetenda, reprise finale), si le passage y est identique avant correction ; la `lse` ajoutée en reprise finale reste refusée.
- R8 : coquille de marteo dans le NABC ou l'espacement gabc : corrigée selon dcrochu et signalée **seulement si tu es très confiant** ; au moindre doute, Needs decision.
- Bémols (R3 bis), salicus retiré, quilisma ajouté en tête de groupe (R15) : restent des décisions humaines.
- R15 : oriscus ajouté sous or/vs/pr/pi, quilisma sous ql/qi, NABC de marteo inchangé : adopter + case To check ; punctum ↔ virga et liquescences : humain.
