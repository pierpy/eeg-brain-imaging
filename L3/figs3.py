"""Figure della Lezione 3 EEG: dai neuroni allo scalpo (scale, dipoli, conduzione di volume, ritmi)."""
import os as _os
_R = _os.environ.get("COURSE_ROOT") or _os.path.dirname(_os.path.abspath(__file__))
while not _os.path.exists(_os.path.join(_R, ".course_root")) and _os.path.dirname(_R) != _R:
    _R = _os.path.dirname(_R)
import sys
sys.path.insert(0, _R + "/common")
import numpy as np
from eegfigs import *
from manim import (VGroup, VMobject, Arrow, Line, DashedLine, DoubleArrow, Dot, Circle, Ellipse, Polygon, Rectangle,
                   RoundedRectangle, Arc, ArcBetweenPoints, CurvedArrow, MathTex, ImageMobject, ORIGIN, UP, DOWN, LEFT, RIGHT, PI)
from manim import RESAMPLING_ALGORITHMS

P = F.P
PURP = "#8E7CC3"; GRN = "#6FCF97"


# ------------------------------------------------------------------ 4: scale micro/meso/macro
def f04_scales(W=3.4):
    f = Fig()
    rng = np.random.default_rng(2)
    t = np.linspace(0, 1, 1000)
    sp = 0.08 * rng.normal(size=1000)
    for c in rng.uniform(0.05, 0.95, 9):
        sp += np.where(np.abs(t - c) < 0.004, -np.sin(np.pi * (t - c + 0.004) / 0.004) * 1.2, 0)
    lfp = 0.5 * np.sin(2 * np.pi * 7 * t) + 0.25 * np.sin(2 * np.pi * 23 * t + 1) + 0.1 * rng.normal(size=1000)
    _, e = eeg(1.0, 1000, seed=4)
    e = e / np.abs(e).max()
    cols = [P.C, P.V, P.S]
    labs = [(tr("Microscopic", "Microscopica"), tr("single neurons · µm · spikes ~1 ms", "singoli neuroni · µm · spike ~1 ms")),
            (tr("Mesoscopic", "Mesoscopica"), tr("local networks · mm · LFP ~10 ms", "reti locali · mm · LFP ~10 ms")),
            (tr("Macroscopic", "Macroscopica"), tr("large-scale networks · cm · EEG ~100 ms", "reti su larga scala · cm · EEG ~100 ms"))]
    for k, (x, col) in enumerate(zip((sp, lfp, e), cols)):
        O = p2(-W * 1.5 - 0.6 + k * (W + 0.6), 0)
        f[f"b{k}"] = RoundedRectangle(corner_radius=0.15, width=W + 0.3, height=3.3, color=col, stroke_width=2).move_to(O + p2(W / 2, 0.1))
        f[f"x{k}"] = trace(t, x, O + p2(0, -0.2), W, 0.55, col, 2)
        f[f"t{k}"] = txt(labs[k][0], O + p2(W / 2, 1.35), col, 20, weight="BOLD")
        f[f"d{k}"] = txt(labs[k][1], O + p2(W / 2, -1.25), P.fg, 15)
        if k < 2:
            f[f"a{k}"] = Arrow(O + p2(W + 0.1, 0.1), O + p2(W + 0.5, 0.1), buff=0, color=P.muted, stroke_width=3, tip_length=0.14)
    return f


# ------------------------------------------------------------------ 5: sincronia -> ampiezza
def f05_sync(W=5.0):
    f = Fig()
    t = np.linspace(0, 1, 500)
    rng = np.random.default_rng(1)
    ph = rng.uniform(0, 2 * np.pi, 8)
    for c, (phs, lab, col) in enumerate(((ph, tr("not synchronised", "non sincronizzati"), P.V), (np.zeros(8), tr("synchronised", "sincronizzati"), P.S))):
        x0 = -W - 0.5 + c * (W + 1.0)
        f[f"t{c}"] = txt(lab, p2(x0 + W / 2, 2.25), col, 20, weight="BOLD")
        for k in range(8):
            f[f"n{c}{k}"] = trace(t, np.sin(2 * np.pi * 8 * t + phs[k]), p2(x0, 1.8 - 0.3 * k), W, 0.1, P.muted, 1.5)
        s = np.sum(np.sin(2 * np.pi * 8 * t[:, None] + phs[None, :]), 1)
        f[f"s{c}"] = trace(t, s, p2(x0, -1.6), W, 0.09, col, 3.5)
        f[f"S{c}"] = txt(tr("summed EEG", "EEG somma"), p2(x0 + W / 2, -2.5), col, 16)
    return f


# ------------------------------------------------------------------ 6: input in strato IV vs strato I
def f06_layers():
    f = Fig()
    for c, (sink_top, lab, pol) in enumerate(((False, tr("input to layer IV (basal)", "input allo strato IV (basale)"), "+"),
                                               (True, tr("input to layer I (apical)", "input allo strato I (apicale)"), "−"))):
        x0 = -2.6 + 5.2 * c
        f[f"surf{c}"] = Line(p2(x0 - 1.8, 2.0), p2(x0 + 1.8, 2.0), color=P.muted, stroke_width=4)
        for k in range(3):
            f[f"p{c}{k}"] = pyramidal(p2(x0 - 0.9 + 0.9 * k, -1.2), 0.95, sw=2.5)
        ys = 0.9 if sink_top else -1.1
        yo = -1.1 if sink_top else 0.9
        f[f"sink{c}"] = VGroup(Circle(radius=0.2, color=P.V, fill_color=P.V, fill_opacity=0.9, stroke_width=0), txt("−", ORIGIN, P.bg, 20, weight="BOLD")).move_to(p2(x0 + 1.5, ys))
        f[f"src{c}"] = VGroup(Circle(radius=0.2, color=P.S, fill_color=P.S, fill_opacity=0.9, stroke_width=0), txt("+", ORIGIN, P.bg, 20, weight="BOLD")).move_to(p2(x0 + 1.5, yo))
        f[f"inp{c}"] = Arrow(p2(x0 - 2.0, ys - 0.25 if not sink_top else ys), p2(x0 - 1.2, ys), buff=0, color=P.C, stroke_width=4, tip_length=0.16)
        f[f"lab{c}"] = txt(lab, p2(x0, -2.45), P.fg, 17)
        f[f"el{c}"] = VGroup(Circle(radius=0.14, color=P.fg, fill_color=P.bg, fill_opacity=1, stroke_width=2).move_to(p2(x0, 2.3)),
                             txt(tr("surface: ", "superficie: ") + pol, p2(x0 + 1.2, 2.45), P.S if pol == "+" else P.V, 17, weight="BOLD"))
    return f


# ------------------------------------------------------------------ 7: campo del dipolo (immagine del potenziale + linee)
def dipole_plane_img(n=260, d=0.5, W=6.0, H=4.0):
    xs = np.linspace(-W / 2, W / 2, n); ys = np.linspace(-H / 2, H / 2, int(n * H / W))
    X, Y = np.meshgrid(xs, ys[::-1])
    r1 = np.hypot(X, Y - d / 2) + 0.08; r2 = np.hypot(X, Y + d / 2) + 0.08
    V = 1 / r1 - 1 / r2
    vm = 0.6 * np.abs(V).max() * 0.35
    rgb = cmap_rdbu(np.tanh(V / vm))
    return (np.dstack([rgb, np.ones_like(V) * 0.95]) * 255).astype(np.uint8)


def f07_dipole(W=6.0, H=4.0):
    f = Fig()
    img = ImageMobject(dipole_plane_img(W=W, H=H)); img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"]); img.height = H
    f["img"] = img
    d = 0.5
    # linee di corrente (dal + al −): archi
    for k, s in enumerate((0.5, 0.9, 1.4, 2.0)):
        for sg in (-1, 1):
            f[f"l{k}{sg}"] = ArcBetweenPoints(p2(0, d / 2), p2(0, -d / 2), angle=sg * (2.4 + 0.15 * k), color=P.fg, stroke_width=1.5, stroke_opacity=0.7).scale(1 + 0.9 * k, about_point=ORIGIN)
    f["p"] = Arrow(p2(0, -0.45), p2(0, 0.45), buff=0, color=P.fg, stroke_width=7, tip_length=0.2)
    f["pl"] = MathTex(r"\vec p = I\,\vec d", color=P.fg).scale(0.8).move_to(p2(2.0, 1.4))
    f["frame"] = Rectangle(width=W, height=H, color=P.muted, stroke_width=2)
    return f


# ------------------------------------------------------------------ 8: mappe di dipoli radiali/tangenziali/profondi
DIPS = [([0.0, 0.0, 0.8], [0, 0, 1], tr("radial, superficial", "radiale, superficiale")),
        ([0.0, 0.0, 0.8], [0, 1, 0], tr("tangential", "tangenziale")),
        ([0.0, 0.0, 0.45], [0, 0, 1], tr("radial, deep", "radiale, profondo"))]


def f08_maps(R=1.1):
    f = Fig()
    for k, (pos, mom, lab) in enumerate(DIPS):
        V, m = dipole_map(pos, mom, n=161, blur=0.15)
        c = p2(-3.0 + 3.0 * k, 0.2)
        f[f"m{k}"], f[f"o{k}"] = topomap(V, m, c, R)
        f[f"l{k}"] = txt(lab, c + p2(0, -R - 0.4), P.fg, 17)
    return f


# ------------------------------------------------------------------ 10: strati della testa e conducibilità
LAYERS = [(tr("scalp", "scalpo"), 0.43, 1.0, "#E0B99A"), (tr("skull", "cranio"), 0.01, 0.93, "#D9D4C7"),
          (tr("CSF", "liquor"), 1.79, 0.87, "#8FC7D9"), (tr("brain (grey matter)", "cervello (sostanza grigia)"), 0.33, 0.84, "#C9A7B5")]


def f10_head(R=2.0):
    f = Fig()
    for k, (n, s, r, col) in enumerate(LAYERS):
        f[f"c{k}"] = Circle(radius=R * r, color=col, fill_color=col, fill_opacity=0.9 if k < 3 else 0.7, stroke_color=P.fg, stroke_width=1.5)
        a = np.radians(35 - 18 * k)
        e = R * (r - 0.03) * np.array([np.cos(a), np.sin(a), 0])
        lab = f"{n}: σ ≈ {s:g} S/m"
        f[f"t{k}"] = VGroup(Line(e, p2(R + 0.6, 1.3 - 0.75 * k), color=P.fg, stroke_width=1.5),
                            txt(lab, p2(R + 0.7, 1.3 - 0.75 * k), P.fg, 17).align_to(p2(R + 0.7, 0), LEFT))
    return f


# ------------------------------------------------------------------ 11: lead field V = L j
def f11_leadfield():
    f = Fig()
    rng = np.random.default_rng(3)
    nE, nS = 8, 14
    Lm = VGroup()
    for i in range(nE):
        for j in range(nS):
            v = np.tanh(rng.normal())
            Lm.add(Rectangle(width=0.22, height=0.22, stroke_width=0.5, stroke_color=P.bg, fill_color=rgb_to_hex_(cmap_rdbu(np.array(v))), fill_opacity=1).move_to(p2(-1.6 + 0.22 * j, 0.8 - 0.22 * i)))
    f["L"] = Lm
    f["V"] = VGroup(*[Rectangle(width=0.22, height=0.22, stroke_width=0.5, stroke_color=P.bg, fill_color=P.V, fill_opacity=0.3 + 0.08 * i).move_to(p2(-3.2, 0.8 - 0.22 * i)) for i in range(nE)])
    f["j"] = VGroup(*[Rectangle(width=0.22, height=0.22, stroke_width=0.5, stroke_color=P.bg, fill_color=P.S, fill_opacity=0.9 if i in (4, 5) else 0.1).move_to(p2(2.0, 1.45 - 0.22 * i)) for i in range(nS)])
    f["eq"] = txt("=", p2(-2.6, 0.03), P.fg, 36); f["dot"] = txt("·", p2(1.6, 0.03), P.fg, 36)
    f["lV"] = txt(tr("V: electrodes", "V: elettrodi"), p2(-3.2, -1.3), P.V, 16)
    f["lL"] = txt(tr("L: lead field (head model)", "L: lead field (modello di testa)"), p2(-0.1, -1.3), P.fg, 16)
    f["lj"] = txt(tr("j: sources", "j: sorgenti"), p2(2.0, -1.9), P.S, 16)
    return f


def rgb_to_hex_(rgb):
    r, g, b = (np.clip(np.asarray(rgb), 0, 1) * 255).astype(int)
    return f"#{r:02X}{g:02X}{b:02X}"


# ------------------------------------------------------------------ 13: montaggio monopolare vs bipolare
def f13_montage(W=4.2):
    f = Fig()
    c = p2(-4.2, 0); R = 1.3
    f["head"] = head(c, R)
    V, m = dipole_map([0.1, 0.0, 0.75], [0, 0.5, 1], n=121, blur=0.2)
    f["img"], f["o"] = topomap(V, m, c, R)
    names = ["F3", "C3", "P3"]
    for k, nm in enumerate(names):
        f[f"e{k}"] = VGroup(Circle(radius=0.1, color=P.fg, fill_color=P.bg, fill_opacity=1).move_to(c + el2d(nm, R)), txt(nm, c + el2d(nm, R) + p2(-0.3, 0), "#16213A", 14))
    t, x = periodic_eeg(2.0, seed=5, peaks=((10, 1, 1.5),), uv=30)
    amps = {"F3": 0.6, "C3": 1.0, "P3": 0.8}
    common = 0.5 * periodic_eeg(2.0, seed=9, peaks=((1.5, 0.5, 2),), uv=30)[1]
    sig = {n: amps[n] * x + common for n in names}
    for k, nm in enumerate(names):
        f[f"u{k}"] = VGroup(txt(nm + "−A1", p2(-1.5, 1.5 - 0.6 * k), P.muted, 14), trace(t, sig[nm], p2(-0.8, 1.5 - 0.6 * k), W, 0.006, P.V, 1.8))
    for k, (a, b) in enumerate((("F3", "C3"), ("C3", "P3"))):
        f[f"b{k}"] = VGroup(txt(a + "−" + b, p2(-1.5, -0.7 - 0.6 * k), P.muted, 14), trace(t, sig[a] - sig[b], p2(-0.8, -0.7 - 0.6 * k), W, 0.006, P.S, 1.8))
    f["tu"] = txt(tr("referential (unipolar)", "referenziale (monopolare)"), p2(1.3, 2.05), P.V, 17, weight="BOLD")
    f["tb"] = txt(tr("bipolar", "bipolare"), p2(1.3, -0.15), P.S, 17, weight="BOLD")
    return f


# ------------------------------------------------------------------ 15: spettro 1/f + picchi
def psd(x, fs=250, nper=500):
    from scipy.signal import welch
    return welch(x, fs, nperseg=nper)


def f15_spectrum(W=6.0, Hh=3.6):
    f = Fig()
    t, x = periodic_eeg(60.0, seed=3, peaks=((10, 1.0, 1.4), (20, 2.0, 0.25)), slope=1.6)
    fr, pw = psd(x)
    m = (fr >= 1) & (fr <= 45)
    fr, pw = fr[m], pw[m]
    O = p2(-W / 2, -Hh / 2)
    lx = lambda v: logpos(v, 1, 45, W); ly = lambda v: (np.log10(v) - np.log10(pw.min())) / (np.log10(pw.max()) - np.log10(pw.min())) * Hh
    f["ax"] = axes(O, W + 0.2, Hh + 0.2, tr("frequency (Hz, log)", "frequenza (Hz, log)"), tr("power (log)", "potenza (log)"))
    f["psd"] = VMobject(color=P.V, stroke_width=3.5).set_points_smoothly([O + p2(lx(a), ly(b)) for a, b in zip(fr, pw)])
    # aperiodico 1/f
    i1, i2 = np.argmin(np.abs(fr - 2)), np.argmin(np.abs(fr - 40))
    sl = (np.log10(pw[i2]) - np.log10(pw[i1])) / (np.log10(fr[i2]) - np.log10(fr[i1]))
    fit_ = lambda v: pw[i1] * (v / fr[i1]) ** sl
    f["ap"] = DashedLine(O + p2(lx(1.2), ly(fit_(1.2))), O + p2(lx(44), ly(fit_(44))), color=P.muted, stroke_width=2.5)
    f["apl"] = txt(tr("aperiodic 1/f component", "componente aperiodica 1/f"), O + p2(lx(6), ly(fit_(6)) - 0.45), P.muted, 15)
    f["pk"] = txt(tr("alpha peak", "picco alfa"), O + p2(lx(10), ly(pw[np.argmin(np.abs(fr - 10))]) + 0.3), P.S, 16)
    for v in (1, 4, 8, 13, 30):
        f[f"t{v}"] = VGroup(Line(O + p2(lx(v), -0.06), O + p2(lx(v), 0.06), color=P.fg, stroke_width=2), txt(str(v), O + p2(lx(v), -0.25), P.muted, 14))
    return f


# ------------------------------------------------------------------ 18: alfa posteriore e mu centrale (topografie)
def smooth_map(centers, width=0.35, n=141):
    xyz, mask = sphere_grid(n)
    V = np.zeros(xyz.shape[:2])
    for c in centers:
        c = np.asarray(c, float); c /= np.linalg.norm(c)
        V += np.exp(-np.sum((xyz - c) ** 2, -1) / width ** 2)
    return V, mask


def f18_alpha_mu(R=1.2):
    f = Fig()
    occ = [[-0.35, -0.85, 0.35], [0.35, -0.85, 0.35]]
    cen = [[-0.8, 0.0, 0.6], [0.8, 0.0, 0.6]]
    for k, (cs, lab) in enumerate(((occ, tr("alpha: posterior, eyes closed", "alfa: posteriore, occhi chiusi")), (cen, tr("mu: sensorimotor, at rest", "mu: sensomotorio, a riposo")))):
        V, m = smooth_map(cs, 0.45)
        c = p2(-1.7 + 3.4 * k, 0.2)
        f[f"m{k}"], f[f"o{k}"] = topomap(V, m, c, R, vmax=1.0)
        f[f"l{k}"] = txt(lab, c + p2(0, -R - 0.4), P.fg, 16)
    return f


# ------------------------------------------------------------------ 21: ampiezza vs frequenza
def f21_ampfreq(W=5.5, Hh=3.2):
    f = Fig()
    O = p2(-W / 2, -Hh / 2)
    f["ax"] = axes(O, W, Hh, tr("frequency", "frequenza"), tr("amplitude", "ampiezza"))
    pts = [(2, "δ", 100), (6, "θ", 60), (10, "α", 50), (20, "β", 20), (40, "γ", 8)]
    cols = [PURP, P.V, P.S, P.C, GRN]
    for k, (fr, n, a) in enumerate(pts):
        x = logpos(fr, 1, 60, W); y = a / 110 * Hh
        f[f"d{k}"] = Dot(O + p2(x, y), radius=0.12, color=cols[k])
        f[f"l{k}"] = txt(n, O + p2(x + 0.25, y + 0.25), cols[k], 22, weight="BOLD")
    f["c"] = VMobject(color=P.muted, stroke_width=2).set_points_smoothly([O + p2(logpos(fr, 1, 60, W), 100 * (2 / fr) ** 0.72 / 110 * Hh) for fr in np.linspace(1.7, 50, 50)])
    f["n"] = txt(tr("larger networks → slower and larger rhythms", "reti più grandi → ritmi più lenti e più ampi"), O + p2(W / 2, -0.95), P.muted, 15)
    return f


# ------------------------------------------------------------------ 22: continuum di vigilanza
def stage_signals(fs=250, dur=4.0):
    t = np.arange(0, dur, 1 / fs)
    out = []
    out.append(periodic_eeg(dur, seed=1, peaks=((20, 4, 0.8), (10, 1, 0.3)), slope=0.6, uv=12)[1])     # attento: beta, basso voltaggio
    out.append(periodic_eeg(dur, seed=2, peaks=((10, 0.6, 3.0),), slope=0.8, uv=35)[1])                 # rilassato: alfa
    out.append(periodic_eeg(dur, seed=3, peaks=((6, 1.5, 1.8), (9, 0.8, 0.8)), slope=1.0, uv=25)[1])    # sonnolenza: theta
    x = periodic_eeg(dur, seed=4, peaks=((6, 2, 0.8),), slope=1.3, uv=25)[1]
    x += 45 * np.exp(-0.5 * ((t - 1.2) / 0.08) ** 2) * np.sin(2 * np.pi * 13 * t) * (1 - 0 * t)          # fuso
    x += -80 * np.exp(-0.5 * ((t - 2.8) / 0.18) ** 2) + 50 * np.exp(-0.5 * ((t - 3.2) / 0.2) ** 2)      # complesso K
    out.append(x)                                                                                        # N2
    out.append(periodic_eeg(dur, seed=5, peaks=((1.0, 0.4, 4.0),), slope=2.0, uv=90)[1])               # N3: delta
    return t, out


def f22_vigilance(W=7.0):
    f = Fig()
    t, S = stage_signals()
    labs = [tr("alert (eyes open): low-voltage beta", "vigile (occhi aperti): beta a basso voltaggio"), tr("relaxed wake (eyes closed): alpha", "veglia rilassata (occhi chiusi): alfa"),
            tr("drowsy (N1): alpha drops out, theta", "sonnolenza (N1): l'alfa scompare, theta"), tr("N2: sleep spindles, K-complexes", "N2: fusi del sonno, complessi K"), tr("N3: slow waves (delta)", "N3: onde lente (delta)")]
    cols = [P.C, P.S, P.V, PURP, "#4A5A8A" if not P.dark else "#9FB0E0"]
    for k in range(5):
        O = p2(-W / 2, 2.0 - 1.0 * k)
        f[f"x{k}"] = trace(t, S[k], O, W, 0.006, cols[k], 1.8)
        f[f"l{k}"] = txt(labs[k], O + p2(W + 0.3, 0), cols[k], 15).align_to(O + p2(W + 0.3, 0), LEFT)
    f["sb"] = VGroup(Line(p2(-W / 2, -2.55), p2(-W / 2 + W / 4, -2.55), color=P.fg, stroke_width=3), txt("1 s", p2(-W / 2 + W / 8, -2.8), P.muted, 14),
                     Line(p2(-W / 2 - 0.2, -2.3), p2(-W / 2 - 0.2, -2.3 + 50 * 0.006), color=P.fg, stroke_width=3), txt("50 µV", p2(-W / 2 - 0.65, -2.2), P.muted, 14))
    return f


# ------------------------------------------------------------------ 23: ipnogramma
def f23_hypnogram(W=8.0, Hh=2.8):
    f = Fig()
    st = ["W", "REM", "N1", "N2", "N3"]
    # sequenza schematica di 8 ore (in minuti)
    seq = [(0, 0), (15, 2), (25, 3), (45, 4), (80, 3), (90, 1), (100, 3), (130, 4), (160, 3), (180, 1), (205, 3), (240, 4), (255, 3), (275, 1),
           (305, 3), (340, 2), (350, 3), (380, 1), (420, 3), (450, 1), (470, 0), (480, 0)]
    y = lambda s: Hh - s / 4 * Hh
    O = p2(-W / 2, -Hh / 2)
    pts = []
    for (t0, s), (t1, _) in zip(seq[:-1], seq[1:]):
        pts += [O + p2(t0 / 480 * W, y(s)), O + p2(t1 / 480 * W, y(s))]
    f["h"] = VMobject(color=P.V, stroke_width=3).set_points_as_corners(pts)
    for k, n in enumerate(st):
        f[f"s{k}"] = txt(n, O + p2(-0.5, y(k)), P.S if n == "REM" else P.fg, 16)
    for hh in range(0, 9, 2):
        f[f"t{hh}"] = txt(f"{hh} h", O + p2(hh / 8 * W, -0.35), P.muted, 14)
    f["n"] = txt(tr("N3 dominates early night, REM late night · cycles ≈ 90 min", "N3 prevale a inizio notte, REM a fine notte · cicli ≈ 90 min"), O + p2(W / 2, -0.8), P.muted, 15)
    return f
