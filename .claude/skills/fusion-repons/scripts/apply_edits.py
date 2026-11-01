"""Applique à gabc/<ID>_marteo.gabc des remplacements exacts.

Fichier d'édits : paires de lignes « OLD: … » / « NEW: … » (OLD doit apparaître une seule fois),
ou « OLDALL: … » / « NEW: … » (toutes les occurrences, au moins une). Octets préservés.
"""
import sys

wt, gid, edits = sys.argv[1:4]
path = f"{wt}/gabc/{gid}_marteo.gabc"
data = open(path, encoding="utf-8", newline="").read()
lines = [l.rstrip("\n") for l in open(edits, encoding="utf-8")]
i = 0
while i < len(lines):
    l = lines[i]
    if l.startswith("OLDFIRST: "):
        old = l.split(": ", 1)[1]
        new = lines[i + 1][5:]
        assert old in data, f"introuvable : {old!r}"
        data = data.replace(old, new, 1)
        print(f"ok (1re de {data.count(old) + 1}) {old!r} -> {new!r}")
        i += 2
    elif l.startswith("OLD: ") or l.startswith("OLDALL: "):
        allmode = l.startswith("OLDALL: ")
        old = l.split(": ", 1)[1]
        new = lines[i + 1]
        assert new.startswith("NEW:"), f"ligne {i + 2} : NEW attendu"
        new = new[5:] if new.startswith("NEW: ") else ""
        n = data.count(old)
        if allmode:
            assert n >= 1, f"introuvable : {old!r}"
            data = data.replace(old, new)
        else:
            assert n == 1, f"{n} occurrences de {old!r}"
            data = data.replace(old, new, 1)
        print(f"ok ({n}) {old!r} -> {new!r}")
        i += 2
    else:
        i += 1
open(path, "w", encoding="utf-8", newline="").write(data)
