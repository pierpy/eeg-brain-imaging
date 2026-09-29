"""Rimuove i <a:pPr> duplicati che pptxgenjs scrive per ogni run: resta solo il primo di ogni paragrafo."""
import sys, zipfile, re, shutil, os
src = sys.argv[1]; tmp = src + ".tmp"
PPR = re.compile(r"<a:pPr\b[^>]*/>|<a:pPr\b[^>]*>.*?</a:pPr>", re.S)
def fix_p(m):
    p = m.group(0); seen = [False]
    def keep(mm):
        if seen[0]: return ""
        seen[0] = True; return mm.group(0)
    return PPR.sub(keep, p)
with zipfile.ZipFile(src) as zi, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
    for it in zi.infolist():
        data = zi.read(it.filename)
        if it.filename.startswith("ppt/slides/slide") and it.filename.endswith(".xml"):
            s = data.decode("utf8")
            s = re.sub(r"<a:p>.*?</a:p>", fix_p, s, flags=re.S)
            data = s.encode("utf8")
        zo.writestr(it, data)
shutil.move(tmp, src)
