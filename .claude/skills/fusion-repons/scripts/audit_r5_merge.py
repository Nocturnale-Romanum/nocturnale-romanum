# Audit R5 (hauteur d'un neume issu d'une fusion) : dans le _marteo des branches de PR ouvertes, syllabes où plusieurs
# glyphes NABC deviennent moins de glyphes (vi/pe -> scM1, clcl -> pf, cl-ppt2 -> sf-…), comparées à la base de la PR.
# On ne compare que les glyphes qui changent (retirés / ajoutés). BAD : un glyphe ajouté n'a pas la hauteur
# minimale des glyphes retirés (défaut hf), qu'il soit plus haut ou plus bas. Le nouveau neume
# doit prendre cette hauteur minimale, jamais celle du dernier neume (décision de marteo, 10/11/2026).
# Candidats à relire : faux positifs fréquents (changement de mélodie, neume déplacé ou retiré, hausse R5 bis
# d'un autre glyphe de la même syllabe).
# usage: audit_r5_merge.py <clone> <prs.tsv>   (prs.tsv : sortie de list_prs.sh)
# sortie (TSV) : statut, PR, ID, syllabe, avant, après, glyphes avant, glyphes après, hauteur min, hauteurs après, notes identiques
import re, sys, subprocess, difflib
clone, tsv = sys.argv[1], sys.argv[2]
GLY = set('vi pu ta gr cl pe po to ci sc pf sf tr st ds ts tg bv tv pr pi vs or sa ql qi pq ni oc un'.split())
def git(*a):
    r = subprocess.run(['git','-C',clone]+list(a), capture_output=True)
    return r.stdout.decode('utf-8','replace') if r.returncode==0 else None
def sylls(txt):
    body = txt.split('%%')[-1]
    out = []
    for m in re.finditer(r'([^()]*)\(([^()]*)\)', body):
        parts = m.group(2).split('|')
        out.append((m.group(1).strip(), parts[0::2], parts[1::2]))
    return out
def glyphs(n):
    """liste de (glyphe complet, base, hauteur) ; ignore ob/cb, lettres, pp/su, espacements"""
    res=[]; i=0
    while i < len(n):
        c=n[i]
        if c in '/`!@ ': i+=1; continue
        two=n[i:i+2]
        if two in ('ob','cb'):
            i+=2; m=re.match(r'h[a-np]',n[i:]); i+= m.end() if m else 0; continue
        if two in ('ls','lt'):
            m=re.match(r'l[st][a-z]+\d',n[i:]); i+= m.end() if m else 2; continue
        if two in ('pp','su'):
            m=re.match(r'(pp|su)[a-z]?\d+',n[i:]); i+= m.end() if m else 2; continue
        if two in GLY:
            m=re.match(r'([a-z]{2})([SGM\-><~]*\d?)(h([a-np]))?',n[i:])
            res.append((m.group(0), m.group(1), m.group(4) or 'f')); i+=m.end(); continue
        i+=1
    return res
rows=[]
for line in open(tsv, encoding='utf-8'):
    num, br = line.split('\t')[:2]; br=br.strip()
    if not br.startswith('merge-'): continue
    ID=br[6:]; f=f'gabc/{ID}_marteo.gabc'
    base=git('merge-base','origin/main',f'origin/{br}')
    if not base: continue
    a=git('show',f'{base.strip()}:{f}'); b=git('show',f'origin/{br}:{f}')
    if a is None or b is None: continue
    A=sylls(a); B=sylls(b)
    sm=difflib.SequenceMatcher(None,[s[0] for s in A],[s[0] for s in B],autojunk=False)
    pairs=[]
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='equal' or (op=='replace' and i2-i1==j2-j1):
            pairs += list(zip(range(i1,i2),range(j1,j2)))
    for i,j in pairs:
        ta,ga,na=A[i]; tb,gb,nb=B[j]
        sa=''.join(na); sb=''.join(nb)
        if sa==sb: continue
        oa=glyphs(sa); ob=glyphs(sb)
        if len(oa)>=2 and 0<len(ob)<len(oa):
            from collections import Counter
            ca=Counter(g for g,_,_ in oa); cb=Counter(g for g,_,_ in ob)
            rem=[x for x in oa if (ca-cb)[x[0]]>0]; add=[x for x in ob if (cb-ca)[x[0]]>0]
            if not rem or not add: continue
            hmin=min(h for *_,h in rem)
            hs=[h for *_,h in add]
            flag = 'BAD' if any(h!=hmin for h in hs) else 'ok'
            notes_same = ''.join(ga).replace('_','').replace('.','').replace("'",'') == ''.join(gb).replace('_','').replace('.','').replace("'",'')
            rows.append((flag,num,ID,tb,'|'.join(x for p in zip(ga,na) for x in p),'|'.join(x for p in zip(gb,nb) for x in p),
                         ' '.join(g for g,_,_ in oa),' '.join(g for g,_,_ in ob),hmin,''.join(hs),notes_same))
for r in sorted(rows,key=lambda r:(r[0],int(r[1]))):
    print('\t'.join(map(str,r)))
