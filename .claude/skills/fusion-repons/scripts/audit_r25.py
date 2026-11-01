# Audit R25 : correction adoptée dans le répons (main → branche) mais pas reportée sur le même passage d'une reprise.
# usage: audit_r25.py <clone> <prs.tsv>
import re, subprocess, sys, unicodedata, difflib
clone, tsv = sys.argv[1:3]

def show(ref, path):
    r = subprocess.run(['git', '-C', clone, 'show', f'{ref}:{path}'], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None

def norm(txt):
    txt = re.sub(r'<[^>]*>', '', txt)
    txt = unicodedata.normalize('NFD', txt.lower())
    return ''.join(c for c in txt if c.isalpha())

def sylls(src):
    out, rep = [], False
    for m in re.finditer(r'([^()]*)\(([^)]*)\)', src.split('%%\n')[-1]):
        raw = m.group(1)
        if '<sp>+</sp>' in raw:
            rep = True
        elif '<sp>V/</sp>' in raw:
            rep = False
        out.append(dict(raw=raw.strip(), t=norm(raw), c=m.group(2), rep=rep))
    return out

for line in open(tsv, encoding='utf-8'):
    num, br = line.split()
    if not br.startswith('merge-'):
        continue
    ID = br[6:]
    a, b = show('origin/main', f'gabc/{ID}_marteo.gabc'), show(f'origin/{br}', f'gabc/{ID}_marteo.gabc')
    if not (a and b):
        continue
    A, B = sylls(a), sylls(b)
    m = {}
    for blk in difflib.SequenceMatcher(None, [s['t'] for s in A], [s['t'] for s in B], autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            m[blk.a + k] = blk.b + k
    for i, j in m.items():
        if not A[i]['t'] or A[i]['c'] == B[j]['c']:
            continue
        old, new = A[i]['c'], B[j]['c']
        prev_t = B[j - 1]['t'] if j else ''
        for k, s in enumerate(B):
            if k <= j or s['t'] != B[j]['t'] or s['c'] != old:
                continue
            if B[k - 1]['t'] != prev_t and not (k + 1 < len(B) and j + 1 < len(B) and B[k + 1]['t'] == B[j + 1]['t']):
                continue
            ctx = lambda x: ' '.join(f"{B[q]['raw']}({B[q]['c']})" for q in range(max(0, x - 2), min(len(B), x + 3)))
            print(f"#{num}\t{ID}\t({old}) -> ({new})\n   CHG: {ctx(j)}\n   REP: {ctx(k)}")
