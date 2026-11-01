# Étude des décisions R5 ouvertes : classe chaque point par type de transformation NABC (marteo → dcrochu)
# Entrée : $NR_WORK/audit/open.json (voir list_prs.sh)
import json, re, collections
import os
N = os.environ.get('NR_WORK', '/tmp/nr-work').rstrip('/') + '/'
prs = json.load(open(N + 'audit/open.json', encoding='utf-8'))
G = r'(?:vi|pu|ta|gr|cl|pe|po|to|ci|sc|pf|sf|tr|st|ds|ts|tg|bv|tv|pr|pi|vs|or|sa|ql|qi|pt|oc|un)'
TOK = re.compile(r'(?P<sub>(?:su|pp)[tuvwxyz]\d)|(?P<ls>l[st][a-z]{1,4}\d)|(?P<h>h[a-np]{2})|(?P<g>' + G + r')(?P<mod>[SGM\-~>]*\d?)|(?P<o>[!/`|]|ob|cb)')

def parse(code):
    glyphs, mods, subs = [], [], []
    for m in TOK.finditer(code):
        if m.group('g'):
            glyphs.append(m.group('g'))
            mods.append(m.group('g') + m.group('mod'))
        elif m.group('sub'):
            subs.append(m.group('sub'))
    return glyphs, mods, subs

items = []
for p in prs:
    b = p['body'] or ''
    m = re.search(r'## Needs decision\n(.*?)(?:\n## |\Z)', b, re.S)
    if not m:
        continue
    for l in m.group(1).split('\n'):
        if l.startswith('- ') and re.search(r'\bR5\b(?! bis| ter)', l):
            items.append((p['number'], l))
cat = collections.defaultdict(list)
pairs = collections.Counter()
for n, l in items:
    mm = re.search(r'marteo ?`+ ?([^`]+?) ?`+.*?dcrochu ?(?:\(c\d\) )?`+ ?([^`]+?) ?`+', l)
    others = [r for r in re.findall(r'\bR\d+(?: bis| ter)?', l) if r != 'R5']
    tag = 'R5 seul' if not others else 'R5+' + '+'.join(sorted(set(others)))
    if not mm:
        cat[('?', tag)].append((n, l)); continue
    a, d = mm.group(1), mm.group(2)
    ga, ma, sa = parse(a.split('|')[-1] if '|' in a else a)
    gd, md, sd = parse(d.split('|')[-1] if '|' in d else d)
    if ga == gd and ma == md and sa != sd:
        k = 'subpunctis/prepunctis'
    elif ga == gd and ma != md:
        k = 'modificateur (S, M, -, ~, >, chiffre)'
    elif ga != gd:
        k = 'glyphe de base'
        pairs[(' '.join(ga), ' '.join(gd))] += 1
    else:
        k = 'autre (hauteur, espacement…)'
    cat[(k, tag)].append((n, l))
tot = collections.Counter()
for (k, tag), v in cat.items():
    tot[k] += len(v)
print('points R5 :', len(items), 'dans', len({n for n, _ in items}), 'PR')
for k, v in tot.most_common():
    print(f'{v:4d} {k}')
    for (k2, tag), w in sorted(cat.items(), key=lambda x: -len(x[1])):
        if k2 == k:
            print(f'       {len(w):3d} {tag}')
print('\nTransformations de glyphe les plus fréquentes :')
for (a, d), c in pairs.most_common(30):
    print(f'{c:3d}  {a}  →  {d}')
json.dump({f'{k}|{t}': v for (k, t), v in cat.items()}, open(N + 'audit/r5_cat.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
