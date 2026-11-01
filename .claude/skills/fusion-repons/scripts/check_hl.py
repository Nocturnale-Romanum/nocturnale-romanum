"""Refuse une version qui ajoute des hauteurs NABC au-dessus de hl (hm, hn, hp) par rapport à l'ancienne."""
import re, sys

def high(path):
    body = open(path, encoding="utf-8").read().split("%%")[-1]
    n = 0
    for grp in re.findall(r"\(([^)]*)\)", body):
        parts = grp.split("|")
        for nabc in parts[1::2]:
            # lecture gauche-droite sans chevauchement : « clhhpihj » donne hh, hj (et non « hp »)
            n += sum(h in "mnp" for h in re.findall(r"h([a-np])", nabc))
    return n

old, new = high(sys.argv[1]), high(sys.argv[2])
import os
if new > old + int(os.environ.get("HL_EXTRA", "0")):
    sys.exit(f"ARRÊT : hauteurs au-dessus de hl ajoutées ({old} -> {new})")
print(f"hl ok ({old} -> {new})")
