# Audit R24 sur les PR ouvertes.
# usage: audit_r24.py <clone> <prs.tsv>  (lignes : numéro<TAB>branche)
# Pour chaque PR merge-ID : compare _marteo de la branche, _marteo de main et _dcrochu de main.
#  MISSING : syllabe sans NABC chez marteo (branche), dans une section synthétique (ob…cb) de marteo,
#            alors que la syllabe alignée de dcrochu a du NABC et les mêmes hauteurs de notes.
#  OUTSIDE : syllabe sans NABC dans main, avec NABC dans la branche, hors section synthétique.
import re, subprocess, sys, unicodedata, difflib

clone, tsv = sys.argv[1:3]

def show(ref, path):
    r = subprocess.run(['git', '-C', clone, 'show', f'{ref}:{path}'], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None

def body(src):
    parts = src.split('%%\n')
    return parts[-1] if len(parts) > 1 else src

def norm(txt):
    txt = re.sub(r'<[^>]*>', '', txt)
    txt = unicodedata.normalize('NFD', txt.lower())
    txt = ''.join(c for c in txt if c.isalpha())
    return txt.replace('æ', 'ae').replace('œ', 'oe')

def sylls(src):
    out = []
    for m in re.finditer(r'([^()]*)\(([^)]*)\)', body(src)):
        txt, content = m.group(1), m.group(2)
        segs = content.split('|')
        gabc = ''.join(segs[0::2])
        nabc = '|'.join(segs[1::2])
        out.append(dict(raw=txt.strip(), t=norm(txt), gabc=gabc, nabc=nabc, has=bool(nabc.strip())))
    return out

def pitches(g):
    g = re.sub(r'[a-np][xy#]', '', g)
    return re.sub(r'[^a-npA-NP]', '', g).lower()

def synth(sy):
    flags, inside = [], False
    for s in sy:
        if re.match(r'^[/`]*ob', s['nabc']):
            inside = True
        flags.append(inside)
        if re.search(r'cb$', s['nabc']):
            inside = False
    return flags

def align(a, b):
    ta = [s['t'] for s in a]
    tb = [s['t'] for s in b]
    m = {}
    for blk in difflib.SequenceMatcher(None, ta, tb, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            m[blk.a + k] = blk.b + k
    return m

for line in open(tsv, encoding='utf-8'):
    num, br = line.split()
    if not br.startswith('merge-'):
        continue
    ID = br[6:]
    mb = show(f'origin/{br}', f'gabc/{ID}_marteo.gabc')
    mm = show('origin/main', f'gabc/{ID}_marteo.gabc')
    dc = show('origin/main', f'gabc/{ID}_dcrochu.gabc')
    if not (mb and mm and dc):
        print(f'#{num} {ID}: fichier manquant'); continue
    B, M, D = sylls(mb), sylls(mm), sylls(dc)
    if not any(s['has'] for s in M):
        continue  # R22 : marteo sans NABC
    fl = synth(B)
    bd = align(B, D)
    bm = align(B, M)
    for i, s in enumerate(B):
        if not s['t']:
            continue
        if fl[i] and not s['has'] and i in bd:
            d = D[bd[i]]
            if d['has']:
                same = pitches(s['gabc']) == pitches(d['gabc'])
                print(f"#{num} {ID}\tMISSING{'' if same else '-MELODY'}\t{s['raw']}({s['gabc']})\tdcrochu {d['raw']}({d['gabc']}|{d['nabc']})")
        if not fl[i] and s['has'] and i in bm and not M[bm[i]]['has']:
            print(f"#{num} {ID}\tOUTSIDE\t{s['raw']}({s['gabc']}|{s['nabc']})")
