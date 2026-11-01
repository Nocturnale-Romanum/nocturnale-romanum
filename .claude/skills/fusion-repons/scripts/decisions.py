# Extrait les points « Needs decision » des PR ouvertes, les classe par règle citée et par motif
# Entrée : $NR_WORK/audit/open.json (voir list_prs.sh)
import json, re, collections
import os
N = os.environ.get('NR_WORK', '/tmp/nr-work').rstrip('/') + '/'
prs = json.load(open(N + 'audit/open.json', encoding='utf-8'))
items = []
for p in prs:
    b = p['body'] or ''
    m = re.search(r'## Needs decision\n(.*?)(?:\n## |\Z)', b, re.S)
    if not m:
        continue
    for l in m.group(1).split('\n'):
        if l.startswith('- '):
            items.append((p['number'], l))
print('items', len(items), 'PRs', len({n for n, _ in items}))
rules = collections.Counter()
for n, l in items:
    for r in set(re.findall(r'\bR\d+(?: bis| ter)?', l)):
        rules[r] += 1
print(rules.most_common())
MOTIFS = {
    'flat/bémol': r'\bflat|B flat|bémol',
    'virga<->punctum': r'virga.{0,40}punctum|punctum.{0,40}virga',
    'quilisma': r'quilisma',
    'oriscus': r'oriscus',
    'liquescence': r'liquesc',
    'bar (R18)': r'\bbar\b|bars\b',
    'ob/cb': r'\bob\b|\bcb\b|bracket',
    'tractulus/virga NABC': r'tractulus|\bta\b.{0,20}\bvi\b|\bvi\b.{0,20}\bta\b',
    'glyph NABC change': r'glyph',
    'episema NABC': r'episema',
    'lsX letters (non lsc)': r'\bls[a-z]{1,3}\d',
    'melody': r'melod',
    'spelling/text': r'spelling|R8\b',
    'syllabification': r'syllab|R2\b',
    'mode cadence': r'cadence',
    'pes quassus / sa': r'\bpq\b|quassus|salicus',
    'stropha': r'stropha',
    'gregall': r'gregall',
}
cnt = collections.Counter(); ex = collections.defaultdict(list)
for n, l in items:
    for k, rx in MOTIFS.items():
        if re.search(rx, l, re.I):
            cnt[k] += 1
            ex[k].append(n)
for k, v in cnt.most_common():
    print(f'{v:4d} {k}: PRs {sorted(set(ex[k]))[:12]}')
open(N + 'audit/decisions.txt', 'w', encoding='utf-8').write('\n'.join(f'#{n}\t{l}' for n, l in items))
