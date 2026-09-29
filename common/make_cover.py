import os as _os
_R = _os.environ.get("COURSE_ROOT") or _os.path.dirname(_os.path.abspath(__file__))
while not _os.path.exists(_os.path.join(_R, ".course_root")) and _os.path.dirname(_R) != _R:
    _R = _os.path.dirname(_R)
import sys; sys.path.insert(0, _R + "/common")
import numpy as np
from manim import *
import eegfigs as E
E.set_theme(dark=True)
class Cov(Scene):
    def construct(self):
        cols = [E.P.V, E.P.S, E.P.V, E.P.C, E.P.V, E.P.S]
        for k in range(6):
            t, x = E.eeg(3, seed=20 + k, alpha=1.3 if k > 2 else 0.6)
            self.add(E.trace(t, x, np.array([-4.2, 1.6 - 0.62 * k, 0]), 5.2, 0.006, cols[k], 2.2).set_stroke(opacity=0.9))
        V, m = E.dipole_map([0.1, -0.35, 0.55], [0, -0.3, 1], blur=0.25)
        img, out = E.topomap(V, m, np.array([2.4, -0.1, 0]), 1.45, elec=True)
        self.add(img, out)
with tempconfig(dict(frame_width=9.0, frame_height=5.6, pixel_width=1800, pixel_height=1120, transparent=True, save_last_frame=True,
                     write_to_movie=False, format="png", output_file="cover_eeg", media_dir="/tmp/eeg_cov", disable_caching=True, verbosity="WARNING")):
    s = Cov(); s.render(); import shutil; shutil.copy(s.renderer.file_writer.image_file_path, _R + "/common/cover_eeg.png")
