"""Rende le figure di una lezione EEG (tema chiaro, sfondo trasparente) in PNG, nella lingua EEG_LANG.
Uso: EEG_LANG=it python render_static.py <dir_lezione> <modulo_figs> [nomi...]"""
import os as _os
_R = _os.environ.get("COURSE_ROOT") or _os.path.dirname(_os.path.abspath(__file__))
while not _os.path.exists(_os.path.join(_R, ".course_root")) and _os.path.dirname(_R) != _R:
    _R = _os.path.dirname(_R)
import sys, os, json, importlib
from manim import config, Scene, tempconfig
LD, MOD = sys.argv[1], sys.argv[2]
sys.path.insert(0, LD); sys.path.insert(0, _R + "/common")
figs = importlib.import_module(MOD)
figs.set_theme(dark=False)
lang = os.environ.get("EEG_LANG", "en")
OUT = os.path.join(LD, f"figpng_{lang}")
os.makedirs(OUT, exist_ok=True)
NAMES = [n for n in dir(figs) if n.startswith("f") and n[1:3].isdigit()]
PXU = 240
todo = sys.argv[3:] or NAMES
for name in todo:
    build = getattr(figs, name)
    g = build().group()
    w, h = g.width + 0.3, g.height + 0.3
    pw, ph = int(w * PXU) // 2 * 2, int(h * PXU) // 2 * 2

    class S(Scene):
        def construct(self):
            self.add(*[m for m in build().values()])
            c = g.get_center()
            for m in self.mobjects: m.shift(-c)

    with tempconfig(dict(frame_width=w, frame_height=h, pixel_width=pw, pixel_height=ph,
                         transparent=True, save_last_frame=True, write_to_movie=False,
                         format="png", output_file=name, media_dir="/tmp/eeg_static",
                         disable_caching=True, verbosity="WARNING", progress_bar="none")):
        sc = S(); sc.render()
        src = sc.renderer.file_writer.image_file_path
    os.replace(src, os.path.join(OUT, name + ".png"))
    print(name, pw, ph)
