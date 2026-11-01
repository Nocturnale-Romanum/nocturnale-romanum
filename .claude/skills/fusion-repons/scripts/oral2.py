# Compare les alléluias pascals (T.P.) des PR ouvertes avec les alléluias standard de gabc/ORAL2.gabc.
# usage: oral2.py <clone> <prs.tsv>
# Pour chaque pièce : mode d'ORAL2 reconnu (mêmes intervalles), puis, syllabe par syllabe,
# M = _marteo de la branche, D = _dcrochu de main, O = ORAL2 transposé à la hauteur de la pièce.
import re, subprocess, sys, difflib

clone, tsv = sys.argv[1:3]
L = 'abcdefghijklmnp'

def show(ref, path):
    r = subprocess.run(['git', '-C', clone, 'show', f'{ref}:{path}'], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None

def sylls(s):
    out = []
    for m in re.finditer(r'([^()]*)\(([^)]*)\)', s):
        segs = m.group(2).split('|')
        out.append(((re.sub(r'<[^>]*>|[{}]', '', m.group(1)).split() or [''])[-1], m.group(2), ''.join(segs[0::2])))
    return out

def steps(gabc):
    g = re.sub(r'([a-np])[xy#]', '', gabc.lower())
    return [L.index(c) for c in re.sub(r'[^a-np]', '', g)]

def shift(gabc, k):
    def f(m):
        c = m.group(0)
        i = L.index(c.lower()) + k
        if not 0 <= i < len(L):
            return '?'
        return L[i] if c.islower() else L[i].upper()
    return re.sub(r'(?<![a-np])[a-npA-NP]', f, gabc) if False else re.sub(r'[a-npA-NP]', f, gabc)

# ORAL2 : un alléluia par mode
oral = {}
src = show('origin/main', 'gabc/ORAL2.gabc').split('%%\n')[-1]
for line in src.split('\n'):
    m = re.search(r'alt:([IVX]+)\.', line)
    if not m:
        continue
    sy = [s for s in sylls(line) if s[0].lower().startswith(('al', 'le', 'lú', 'ia'))]
    oral[m.group(1)] = sy[:4]

def tp(src):
    body = src.split('%%\n')[-1]
    i = body.find('T.P.')
    if i < 0:
        return None
    sy = [s for s in sylls(body[i:]) if s[0]][:4]
    return sy if len(sy) == 4 and sy[0][0].lower().startswith('al') else None

def seq(sy):
    return [n for s in sy for n in steps(s[2])]

for line in open(tsv, encoding='utf-8'):
    num, br = line.split()
    if not br.startswith('merge-'):
        continue
    ID = br[6:]
    mb = show(f'origin/{br}', f'gabc/{ID}_marteo.gabc')
    dc = show('origin/main', f'gabc/{ID}_dcrochu.gabc')
    if not mb:
        continue
    M = tp(mb)
    if not M:
        continue
    D = tp(dc) if dc else None
    ms = seq(M)
    best = None
    for mode, O in oral.items():
        os_ = seq(O)
        if not os_ or not ms:
            continue
        k = ms[0] - os_[0]
        r = difflib.SequenceMatcher(None, ms, [x + k for x in os_]).ratio()
        if not best or r > best[0]:
            best = (r, mode, k, O)
    r, mode, k, O = best
    print(f'=== #{num} {ID}  mode {mode}  match {r:.2f}  shift {k:+d}')
    for i in range(4):
        print(f'  M {M[i][0]}({M[i][1]})')
        print(f'  D {D[i][0]}({D[i][1]})' if D else '  D -')
        o = O[i][1].split('|')
        o[0::2] = [shift(x, k) for x in o[0::2]]
        print(f'  O {O[i][0]}({"|".join(o)})')
