import os as _os
_R = _os.environ.get("COURSE_ROOT") or _os.path.dirname(_os.path.abspath(__file__))
while not _os.path.exists(_os.path.join(_R, ".course_root")) and _os.path.dirname(_R) != _R:
    _R = _os.path.dirname(_R)
import sys
sys.path.insert(0, _R + "/common"); sys.path.insert(0, _R + "/L10")
from base_eeg import *
sys.path.insert(0, _R + "/L10")
set_footer(tr("Brain Imaging · EEG · Lecture 10 · Decoding and applications", "Brain Imaging · EEG · Lezione 10 · Decoding e applicazioni"))
