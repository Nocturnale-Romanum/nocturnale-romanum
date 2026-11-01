# Nouveau cas R13 : « // » suivi d'une seule note jusqu'à la fin de la syllabe, un degré au-dessus de la note précédente.
# usage: audit_r13b.py <clone> <prs.tsv>
# Sortie : PR, ID, syllabe, gabc marteo (branche), et PROPOSED si dcrochu a « / » à cet endroit (signes rythmiques ignorés).
import re, subprocess, sys, unicodedata, difflib
clone, tsv = sys.argv[1:3]
L = 'abcdefghijklmnp'

def show(ref, path):
    r = subprocess.run(['git', '-C', clone, 'show', f'{ref}:{path}'], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None

def norm(txt):
    txt = re.sub(r'<[^>]*>', '', txt)
    txt = unicodedata.normalize('NFD', txt.lower())
    return ''.join(c for c in txt if c.isalpha())

def sylls(src):
    out = []
    for m in re.finditer(r'([^()]*)\(([^)]*)\)', src.split('%%\n')[-1]):
        segs = m.group(2).split('|')
        out.append(dict(raw=m.group(1).strip(), t=norm(m.group(1)), g=''.join(segs[0::2])))
    return out

def notes(g):
    g = re.sub(r'[a-np][xy#]', '', g)
    return [L.index(c.lower()) for c in re.findall(r'[a-npA-NP]', g)]

def unsign(g):
    return re.sub(r"_\d?|'\d?|\.", '', g)

def hits(g):
    for m in re.finditer(r'(?<!/)//(?!/)', g):
        before, after = notes(g[:m.start()]), notes(g[m.end():])
        if before and len(after) == 1 and after[0] == before[-1] + 1:
            yield m.start()

for line in open(tsv, encoding='utf-8'):
    num, br = line.split()
    if not br.startswith('merge-'):
        continue
    ID = br[6:]
    mb, dc = show(f'origin/{br}', f'gabc/{ID}_marteo.gabc'), show('origin/main', f'gabc/{ID}_dcrochu.gabc')
    if not mb:
        continue
    B = sylls(mb)
    D = sylls(dc) if dc else []
    al = {}
    for blk in difflib.SequenceMatcher(None, [s['t'] for s in B], [s['t'] for s in D], autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            al[blk.a + k] = blk.b + k
    for i, s in enumerate(B):
        for pos in hits(s['g']):
            reduced = s['g'][:pos] + '/' + s['g'][pos + 2:]
            prop = i in al and unsign(D[al[i]]['g']) == unsign(reduced)
            print(f"#{num}\t{ID}\t{'PROPOSED' if prop else 'officio'}\t{s['raw']}({s['g']})" + (f"\tD {D[al[i]]['g']}" if i in al else ''))
