# Étude des décisions R15 ouvertes (formes des notes carrées) : classement par type de changement gabc
# Entrée : $NR_WORK/audit/open.json (voir list_prs.sh)
import json, re, collections
import os
N = os.environ.get('NR_WORK', '/tmp/nr-work').rstrip('/') + '/'
prs = json.load(open(N + 'audit/open.json', encoding='utf-8'))
items = []
for p in prs:
    b = p['body'] or ''
    m = re.search(r'## Needs decision\n(.*?)(?:\n## |\Z)', b, re.S)
    if m:
        items += [(p['number'], l) for l in m.group(1).split('\n') if l.startswith('- ') and re.search(r'\bR15\b', l)]

def shapes(g):
    """Liste (hauteur, forme) des notes carrées, signes rythmiques ignorés."""
    g = re.sub(r"_\d?|'\d?|\.|[/!@ ]|[0-9]", '', g)
    g = re.sub(r'([a-np])[xy#]', '', g)
    out = []
    for m in re.finditer(r'([a-npA-NP])([vVwoOs~<>]*)', g):
        c = m.group(1)
        f = m.group(2)
        out.append((c.lower(), ('I' if c.isupper() else '') + ''.join(sorted(set(f)))))
    return out

NAMES = {'v': 'virga', 'V': 'virga', 'w': 'quilisma', 'o': 'oriscus', 'O': 'oriscus', 's': 'stropha', '~': 'liquescence', '<': 'liquescence', '>': 'liquescence', 'I': 'inclinatum'}
cnt = collections.Counter(); ex = collections.defaultdict(list); melodic = 0
for n, l in items:
    mm = re.search(r'marteo ?`+ ?([^`|]+?)(?:\|[^`]*)? ?`+.*?dcrochu ?(?:\(c\d\) )?`+ ?([^`|]+?)(?:\|[^`]*)? ?`+', l)
    if not mm:
        k = 'non analysé'
    else:
        a, d = shapes(mm.group(1)), shapes(mm.group(2))
        if [x for x, _ in a] != [x for x, _ in d]:
            k = 'hauteurs changées (mélodie)'
        else:
            ch = []
            for (h, f1), (_, f2) in zip(a, d):
                for c in sorted(set(f1) ^ set(f2)):
                    nm = NAMES.get(c, c)
                    ch.append(nm + (' ajouté' if c in f2 else ' retiré'))
            k = ', '.join(sorted(set(ch))) or 'identique hors signes (regroupement…)'
    cnt[k] += 1; ex[k].append(n)
print('points R15 :', len(items), 'dans', len({n for n, _ in items}), 'PR')
for k, v in cnt.most_common():
    print(f'{v:3d}  {k:45s} #' + ' #'.join(str(x) for x in sorted(set(ex[k]))[:10]))
