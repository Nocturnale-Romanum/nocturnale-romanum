# Audit R13/R23 : « // » restant après un punctum seul (épisème ou bémol compris) dans le _marteo des branches de PR ouvertes.
# usage: audit_r13.py <clone> <prs.tsv>   (prs.tsv : sortie de list_prs.sh)
import re, subprocess, sys
clone, tsv = sys.argv[1:3]
# un groupe = début de la syllabe ou après un « / » simple ; punctum seul = une note, avec bémol, épisème ou point éventuels
PUNCTUM = re.compile(r"(?:^|(?<=[^/]/))((?:[a-np][xy#])?[a-np][_.'0-9]*)//(?!/)")
for line in open(tsv, encoding='utf-8'):
    num, br = line.split()
    if not br.startswith('merge-'):
        continue
    ID = br[6:]
    r = subprocess.run(['git', '-C', clone, 'show', f'origin/{br}:gabc/{ID}_marteo.gabc'], capture_output=True, text=True)
    src = r.stdout.split('%%\n')[-1]
    for m in re.finditer(r'([^()]*)\(([^)|]*)', src):
        if PUNCTUM.search(m.group(2)):
            print(f"#{num} {ID}\t{m.group(1).strip()}({m.group(2)})")
