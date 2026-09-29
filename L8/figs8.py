"""Figure della Lezione 8 EEG: analisi spaziale e microstati (dati SIMULATI)."""
import os as _os
_R = _os.environ.get("COURSE_ROOT") or _os.path.dirname(_os.path.abspath(__file__))
while not _os.path.exists(_os.path.join(_R, ".course_root")) and _os.path.dirname(_R) != _R:
    _R = _os.path.dirname(_R)
import sys
sys.path.insert(0, _R + "/common")
import numpy as np
from eegfigs import *
from manim import (VGroup, VMobject, Arrow, Line, DashedLine, Dot, Circle, Polygon, Rectangle,
                   RoundedRectangle, MathTex, ORIGIN, UP, DOWN, LEFT, RIGHT, PI)

P = F.P
PURP = "#8E7CC3"; GRN = "#6FCF97"
FS8 = 250
MS_COL = ["#E07A5F", "#3D9BA8", "#8E7CC3", "#E0A030"]   # A, B, C, D


def dec(v, n=2):
    s = f"{v:.{n}f}"
    return s if LANG == "en" else s.replace(".", ",")


def box(c, w, h, lab, col, sz=16):
    return VGroup(RoundedRectangle(corner_radius=0.15, width=w, height=h, color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.18).move_to(c),
                  txt(lab, c, P.fg, sz))


# ------------------------------------------------------------------ modelli dei 4 microstati canonici
MS_DIP = [([0.0, 0.0, 0.35], [-0.75, 0.75, 0.0]),     # A: diagonale sinistra-posteriore / destra-frontale
          ([0.0, 0.0, 0.35], [0.75, 0.75, 0.0]),      # B: diagonale opposta
          ([0.0, 0.0, 0.35], [0.0, 1.0, 0.0]),        # C: antero-posteriore
          ([0.0, 0.25, 0.3], [0.0, 0.15, 1.0])]       # D: fronto-centrale


def template_maps(n=121):
    return [dipole_map(p, m, n=n, blur=0.15) for p, m in MS_DIP]


def template_vec(names=None):
    names = names or NAMES
    E_ = np.array([el3d(k) for k in names])
    out = []
    for p, m in MS_DIP:
        v = dipole_pot(E_, np.array(p), np.array(m)); v = v - v.mean(); out.append(v / np.linalg.norm(v))
    return np.array(out)          # 4 x nch


def simulate(dur=4.0, fs=FS8, seed=3, snr=25.0):
    """EEG a microstati: segmenti 50–150 ms, mappa fissa, polarità che oscilla ad alfa."""
    rng = np.random.default_rng(seed)
    T = template_vec()
    n = int(dur * fs); t = np.arange(n) / fs
    lab = np.zeros(n, int); k = rng.integers(4); i = 0
    while i < n:
        L = int(rng.uniform(0.05, 0.15) * fs)
        lab[i:i + L] = k; i += L
        k = rng.choice([j for j in range(4) if j != k])
    s = np.sin(2 * np.pi * 10 * t + 0.3) * (1 + 0.3 * np.sin(2 * np.pi * 0.7 * t))
    X = (T[lab].T * s) * 30
    X = X + rng.normal(size=X.shape) * 30 / snr
    X = X - X.mean(0)
    return t, X, lab


def gfp(X):
    return X.std(0)


# ------------------------------------------------------------------ 5: GFP
def f05_gfp(W=9.0):
    f = Fig()
    t, X, lab = simulate(1.0)
    O = p2(-W / 2, 0.8)
    f["b"] = VGroup(*[trace(t, x, O, W, 0.02, P.muted, 1) for x in X])
    g = gfp(X)
    O2 = p2(-W / 2, -1.7)
    f["g"] = trace(t, g, O2, W, 0.08, P.S, 3)
    from scipy.signal import find_peaks
    pk, _ = find_peaks(g)
    f["p"] = VGroup(*[Dot(O2 + p2(t[i] / t[-1] * W, 0.08 * g[i]), radius=0.05, color=P.V) for i in pk])
    f["lb"] = txt(tr("butterfly plot (all channels)", "butterfly plot (tutti i canali)"), O + p2(-1.3, 0.9), P.muted, 15)
    f["lg"] = txt(tr("GFP", "GFP"), O2 + p2(-0.5, 0.4), P.S, 17, weight="BOLD")
    f["lp"] = txt(tr("dots = GFP peaks (highest SNR)", "punti = picchi di GFP (SNR massimo)"), O2 + p2(W / 2, -0.35), P.V, 14)
    return f


# ------------------------------------------------------------------ 6: dissimilarità globale
def f06_gmd(R=1.0):
    f = Fig()
    maps = template_maps()
    specs = [(maps[2], 1.0, tr("map u", "mappa u")), (maps[2], 2.0, tr("u × 2: same shape", "u × 2: stessa forma")), (maps[0], 1.0, tr("map v: other shape", "mappa v: altra forma"))]
    for k, ((V, m), sc, lab) in enumerate(specs):
        c = p2(-3.6 + 3.6 * k, 0.3)
        f[f"m{k}"], f[f"o{k}"] = topomap(V * sc, m, c, R * (0.8 + 0.2 * sc), vmax=np.abs(maps[2][0][maps[2][1]]).max() * 1.4)
        f[f"l{k}"] = txt(lab, c + p2(0, -1.55), P.fg, 15, weight="BOLD")
    f["g1"] = txt("GMD = 0", p2(-1.8, 1.7), P.V, 17, weight="BOLD")
    f["g2"] = txt("GMD ≈ 1.4", p2(1.8, 1.7), P.S, 17, weight="BOLD")
    return f


# ------------------------------------------------------------------ 7: stati quasi-stabili
def f07_sequence(W=11.0, R=0.42):
    f = Fig()
    t, X, lab = simulate(0.8, seed=5)
    g = gfp(X)
    O = p2(-W / 2, 0.3)
    # segmenti colorati sotto la GFP
    i = 0; k = 0
    tmaps = template_maps(81)
    while i < len(lab):
        j = i
        while j < len(lab) and lab[j] == lab[i]: j += 1
        x0 = O + p2(t[i] / t[-1] * W, 0); x1 = O + p2(t[j - 1] / t[-1] * W, 0)
        f[f"s{k}"] = Rectangle(width=max(x1[0] - x0[0], 0.02), height=1.5, stroke_width=0, fill_color=MS_COL[lab[i]], fill_opacity=0.3).move_to((x0 + x1) / 2 + p2(0, 0.75))
        c = (x0 + x1) / 2 + p2(0, -0.8)
        V, m = tmaps[lab[i]]
        f[f"m{k}"], f[f"o{k}"] = topomap(V, m, c, R)
        f[f"l{k}"] = txt("ABCD"[lab[i]], c + p2(0, -0.6), MS_COL[lab[i]], 15, weight="BOLD")
        i = j; k += 1
    f["g"] = trace(t, g, O, W, 0.14, P.fg, 2.5)
    f["t"] = txt(tr("quasi-stable maps (≈ 60–120 ms) with rapid transitions", "mappe quasi stabili (≈ 60–120 ms) con transizioni rapide"), O + p2(W / 2, 1.9), P.fg, 16)
    return f


# ------------------------------------------------------------------ 9: pipeline dei microstati
PIPE8 = [tr("multichannel\nEEG", "EEG\nmulticanale"), tr("GFP\npeaks", "picchi\nGFP"), tr("spatial\nclustering", "clustering\nspaziale"), tr("templates\nA–D", "template\nA–D"),
         tr("back-\nfitting", "back-\nfitting"), tr("metrics &\nstatistics", "metriche e\nstatistica")]


def f09_pipeline(W=12.4):
    f = Fig()
    cols = [P.C, P.S, P.V, PURP, GRN, P.C]
    n = len(PIPE8); step = W / n
    for k, lab in enumerate(PIPE8):
        c = p2(-W / 2 + step * (k + 0.5), 0)
        f[f"b{k}"] = box(c, step - 0.45, 1.25, lab, cols[k], 16)
        if k < n - 1:
            f[f"a{k}"] = Arrow(c + p2((step - 0.45) / 2, 0), c + p2(step - (step - 0.45) / 2, 0), buff=0.02, color=P.fg, stroke_width=3, tip_length=0.13)
    return f


# ------------------------------------------------------------------ 10: k-means vs k-means modificato
def f10_kmeans(R=1.6):
    f = Fig()
    rng = np.random.default_rng(4)
    a = np.array([np.cos(0.5), np.sin(0.5)]); b = np.array([np.cos(2.2), np.sin(2.2)])
    pts = []
    for v, col in ((a, MS_COL[0]), (b, MS_COL[1])):
        for s in (1, -1):
            for _ in range(40):
                pts.append((s * v * rng.uniform(0.5, 1.0) + rng.normal(0, 0.08, 2), col, s))
    for k, (lab, mode) in enumerate(((tr("classic k-means: 4 clusters", "k-means classico: 4 cluster"), 0), (tr("modified k-means: polarity ignored", "k-means modificato: polarità ignorata"), 1))):
        c = p2(-3.0 + 6.0 * k, 0)
        f[f"ax{k}"] = VGroup(Line(c + p2(-R, 0), c + p2(R, 0), color=P.aux, stroke_width=1.5), Line(c + p2(0, -R), c + p2(0, R), color=P.aux, stroke_width=1.5),
                            txt("ch1", c + p2(R + 0.25, 0), P.muted, 13), txt("ch2", c + p2(0, R + 0.2), P.muted, 13))
        dots = VGroup()
        for p_, col, s in pts:
            cc = col if mode == 1 else (col if s > 0 else (MS_COL[2] if col == MS_COL[0] else MS_COL[3]))
            dots.add(Dot(c + p2(*(p_ * R)), radius=0.035, color=cc))
        f[f"d{k}"] = dots
        if mode == 1:
            for v, col in ((a, MS_COL[0]), (b, MS_COL[1])):
                f[f"ln{k}{col}"] = DashedLine(c + p2(*(-v * R * 1.05)), c + p2(*(v * R * 1.05)), color=col, stroke_width=2)
        f[f"l{k}"] = txt(lab, c + p2(0, -R - 0.4), P.fg, 15, weight="BOLD")
    return f


# ------------------------------------------------------------------ 12: criteri per scegliere k
def f12_criteria(W=3.2, Hh=2.0):
    f = Fig()
    ks = np.arange(2, 11)
    gev = 0.82 - 0.35 * np.exp(-(ks - 2) / 1.3); gev[2:] = gev[2:] + 0.0
    cv = 22 - 12 * (1 - np.exp(-(ks - 2) / 1.0)) + 0.9 * np.maximum(ks - 4, 0) ** 1.3
    kl = np.array([0.02, 0.05, 0.16, 0.04, 0.03, 0.05, 0.02, 0.03, 0.01])
    for j, (y, lab, best) in enumerate(((gev, tr("GEV (explained variance)", "GEV (varianza spiegata)"), None), (cv, tr("cross-validation (min)", "cross-validation (min)"), np.argmin(cv)), (kl, tr("Krzanowski–Lai (max)", "Krzanowski–Lai (max)"), np.argmax(kl)))):
        O = p2(-5.6 + 4.0 * j, -1.0)
        f[f"ax{j}"] = axes(O, W + 0.2, Hh + 0.2, "k", "")
        yy = (y - y.min()) / (y.max() - y.min()) * Hh * 0.9 + 0.05
        f[f"c{j}"] = VMobject(color=P.V, stroke_width=3).set_points_as_corners([O + p2((k - 2) / 8 * W, v) for k, v in zip(ks, yy)])
        f[f"p{j}"] = VGroup(*[Dot(O + p2((k - 2) / 8 * W, v), radius=0.05, color=P.V) for k, v in zip(ks, yy)])
        if best is not None:
            f[f"b{j}"] = Circle(radius=0.14, color=P.S, stroke_width=3).move_to(O + p2((ks[best] - 2) / 8 * W, yy[best]))
        f[f"l{j}"] = txt(lab, O + p2(W / 2, Hh + 0.45), P.fg, 15, weight="BOLD")
        f[f"x{j}"] = VGroup(*[txt(str(k), O + p2((k - 2) / 8 * W, -0.25), P.muted, 12) for k in (2, 4, 6, 8, 10)])
    return f


# ------------------------------------------------------------------ 13: i quattro template
def f13_templates(R=1.1):
    f = Fig()
    maps = template_maps()
    desc = [tr("left-right orientation", "orientamento sinistra-destra"), tr("right-left orientation", "orientamento destra-sinistra"), tr("anterior-posterior", "antero-posteriore"), tr("fronto-central maximum", "massimo fronto-centrale")]
    for k, (V, m) in enumerate(maps):
        c = p2(-4.5 + 3.0 * k, 0.2)
        f[f"m{k}"], f[f"o{k}"] = topomap(V, m, c, R)
        f[f"l{k}"] = txt("ABCD"[k], c + p2(0, R + 0.4), MS_COL[k], 26, weight="BOLD")
        f[f"d{k}"] = txt(desc[k], c + p2(0, -R - 0.35), P.muted, 14)
    return f


# ------------------------------------------------------------------ 15: backfitting
def backfit(X, T=None):
    T = template_vec() if T is None else T
    Xn = X / (np.linalg.norm(X, axis=0) + 1e-12)
    C = np.abs(T @ Xn)
    lab = C.argmax(0).copy()
    g = X.std(0); ok = g > 0.35 * np.percentile(g, 95)
    last = lab[np.argmax(ok)]
    for i in range(len(lab)):            # campioni a bassa GFP: si eredita l'ultima etichetta affidabile
        if ok[i]: last = lab[i]
        else: lab[i] = last
    i = 0                                 # segmenti < 20 ms assorbiti dal precedente
    while i < len(lab):
        j = i
        while j < len(lab) and lab[j] == lab[i]: j += 1
        if j - i < 5 and i > 0: lab[i:j] = lab[i - 1]
        i = j
    return lab, C.max(0)


def f15_backfit(W=11.0):
    f = Fig()
    t, X, lab_true = simulate(1.0, seed=8)
    lab, corr = backfit(X)
    g = gfp(X)
    O = p2(-W / 2, 0.0)
    i = 0; k = 0
    while i < len(lab):
        j = i
        while j < len(lab) and lab[j] == lab[i]: j += 1
        x0 = O + p2(t[i] / t[-1] * W, 0); x1 = O + p2(t[j - 1] / t[-1] * W, 0)
        f[f"s{k}"] = Rectangle(width=max(x1[0] - x0[0], 0.01), height=0.14 * g.max() * 1.05, stroke_width=0, fill_color=MS_COL[lab[i]], fill_opacity=0.55).move_to((x0 + x1) / 2 + p2(0, 0.07 * g.max() * 1.05))
        if (j - i) > 6:
            f[f"t{k}"] = txt("ABCD"[lab[i]], (x0 + x1) / 2 + p2(0, -0.3), MS_COL[lab[i]], 14, weight="BOLD")
        i = j; k += 1
    f["g"] = trace(t, g, O, W, 0.14, P.fg, 2.5)
    f["lb"] = txt(tr("each sample labelled with the best-correlating template (winner-takes-all, polarity ignored)", "ogni campione etichettato con il template più correlato (winner-takes-all, polarità ignorata)"), O + p2(W / 2, 0.14 * g.max() + 0.45), P.fg, 15)
    return f


# ------------------------------------------------------------------ 16: metriche
def ms_metrics(lab, fs=FS8):
    runs, rl = [], []
    i = 0
    while i < len(lab):
        j = i
        while j < len(lab) and lab[j] == lab[i]: j += 1
        runs.append(j - i); rl.append(lab[i]); i = j
    runs = np.array(runs); rl = np.array(rl)
    dur = np.array([runs[rl == k].mean() / fs * 1000 for k in range(4)])
    occ = np.array([(rl == k).sum() / (len(lab) / fs) for k in range(4)])
    cov = np.array([(lab == k).mean() * 100 for k in range(4)])
    Tm = np.zeros((4, 4))
    for a, b in zip(rl[:-1], rl[1:]): Tm[a, b] += 1
    Tm = Tm / Tm.sum(1, keepdims=True)
    return dur, occ, cov, Tm


def f16_metrics(W=2.2, Hh=1.8):
    f = Fig()
    t, X, _ = simulate(60.0, seed=2)
    lab, _ = backfit(X)
    dur, occ, cov, Tm = ms_metrics(lab)
    for j, (vals, lab_, unit) in enumerate(((dur, tr("mean duration", "durata media"), "ms"), (occ, tr("occurrence", "occorrenza"), "/s"), (cov, tr("coverage", "copertura"), "%"))):
        O = p2(-6.0 + 3.0 * j, -1.0)
        vm = vals.max() * 1.15
        for k in range(4):
            f[f"b{j}{k}"] = Rectangle(width=0.35, height=vals[k] / vm * Hh, stroke_width=0, fill_color=MS_COL[k], fill_opacity=0.9).move_to(O + p2(0.35 + 0.5 * k, 0), aligned_edge=DOWN)
            f[f"t{j}{k}"] = txt("ABCD"[k], O + p2(0.35 + 0.5 * k, -0.25), MS_COL[k], 13, weight="BOLD")
        f[f"a{j}"] = Line(O, O + p2(W, 0), color=P.fg, stroke_width=1.5)
        f[f"l{j}"] = txt(f"{lab_} ({unit})", O + p2(W / 2, Hh + 0.35), P.fg, 15, weight="BOLD")
        f[f"v{j}"] = txt(f"≈ {dec(vals.mean(), 0 if unit != '/s' else 1)} {unit}", O + p2(W / 2, Hh + 0.05), P.muted, 13)
    # matrice di transizione
    c0 = p2(3.9, -0.1); s = 0.45
    for a in range(4):
        for b in range(4):
            v = Tm[a, b]
            col = cmap_rdbu(np.array(v / 0.6))
            f[f"q{a}{b}"] = Rectangle(width=s, height=s, stroke_width=1, stroke_color=P.bg, fill_color="#%02x%02x%02x" % tuple((np.clip(col, 0, 1) * 255).astype(int)), fill_opacity=1).move_to(c0 + p2((b - 1.5) * s, (1.5 - a) * s))
            f[f"n{a}{b}"] = txt(dec(v, 2) if a != b else "–", c0 + p2((b - 1.5) * s, (1.5 - a) * s), P.fg, 11)
        f[f"ra{a}"] = txt("ABCD"[a], c0 + p2(-2.35 * s, (1.5 - a) * s), MS_COL[a], 13, weight="BOLD")
        f[f"ca{a}"] = txt("ABCD"[a], c0 + p2((a - 1.5) * s, 2.35 * s), MS_COL[a], 13, weight="BOLD")
    f["tl"] = txt(tr("transition probabilities (from → to)", "probabilità di transizione (da → a)"), c0 + p2(0, 3.0 * s + 0.2), P.fg, 15, weight="BOLD")
    return f
