"""Nel .pptx di manim-slides: le slide con auto_next avanzano da sole alla fine del video
(così la slide in loop successiva parte senza clic). Uso: pptx_autonext.py file.pptx dir_manim Scene1 Scene2 ..."""
import sys, json, zipfile, re, subprocess, os
pp, md, scenes = sys.argv[1], sys.argv[2], sys.argv[3:]
cfg = []
for s in scenes:
    d = json.load(open(os.path.join(md, "slides_small", s + ".json")))
    for x in d["slides"]:
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                    os.path.join(md, x["file"])], capture_output=True, text=True).stdout or 0)
        cfg.append((x.get("auto_next", False), dur))
zi = zipfile.ZipFile(pp)
names = zi.namelist()
nslides = len([n for n in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)])
assert nslides == len(cfg), (nslides, len(cfg))
tmp = pp + ".tmp"
zo = zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED)
nmod = 0
for it in zi.infolist():
    b = zi.read(it.filename)
    m = re.fullmatch(r"ppt/slides/slide(\d+)\.xml", it.filename)
    if m:
        k = int(m.group(1)) - 1
        auto, dur = cfg[k]
        if auto:
            x = b.decode("utf8")
            x = re.sub(r"<p:transition[^>]*/>|<p:transition.*?</p:transition>", "", x, flags=re.S)
            tr = f'<p:transition advClick="1" advTm="{int(dur * 1000) + 100}"/>'
            if "</p:clrMapOvr>" in x:
                x = x.replace("</p:clrMapOvr>", "</p:clrMapOvr>" + tr, 1)
            else:
                x = x.replace("</p:cSld>", "</p:cSld>" + tr, 1)
            b = x.encode("utf8"); nmod += 1
    zo.writestr(it, b)
zo.close(); os.replace(tmp, pp)
print("auto-avanzamento su", nmod, "slide")
