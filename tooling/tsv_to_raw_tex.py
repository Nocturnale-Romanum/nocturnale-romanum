
feasts = open("feasts.tsv").readlines()
feasts = [x.split("\t") for x in feasts]
feasts = [[x.strip() for x in l] for l in feasts]
pieces = open("pieces.tsv").readlines()
pieces = [x.split("\t") for x in pieces]
pieces = [[x.strip() for x in l] for l in pieces]
out=open("code.tex", "w")
for [fcode, ftitle, lhead, rhead, level, date, oldrank, newrank] in feasts:
  fpieces = [x for x in pieces if x[-1] == fcode]
  out.write("\\feast{"+fcode+"}{"+ftitle+"}{"+lhead+"}{"+rhead+"}{"+level+"}{"+date+"}{"+oldrank+"}{"+newrank+"}{}{}\n")
  for [incipit, opart, pcode, fcode] in fpieces:
    letter={"re":"R","or":"T","an":"A","hy":"H","ps":"P","in":"I"}[opart]
    out.write("\\gscore{"+pcode+"}{"+letter+"}{}{"+incipit+"}\n")
out.close()