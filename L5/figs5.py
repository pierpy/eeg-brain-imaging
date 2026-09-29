"""Figure della Lezione 5 EEG: pre-elaborazione e ICA (dati SIMULATI)."""
import os as _os
_R = _os.environ.get("COURSE_ROOT") or _os.path.dirname(_os.path.abspath(__file__))
while not _os.path.exists(_os.path.join(_R, ".course_root")) and _os.path.dirname(_R) != _R:
    _R = _os.path.dirname(_R)
import sys
sys.path.insert(0, _R + "/common")
import numpy as np
from eegfigs import *
from manim import (VGroup, VMobject, Arrow, Line, DashedLine, DoubleArrow, Dot, Circle, Polygon, Rectangle,
                   RoundedRectangle, MathTex, ORIGIN, UP, DOWN, LEFT, RIGHT, PI)
from scipy.signal import butter, sosfilt, sosfiltfilt

P = F.P
PURP = "#8E7CC3"; GRN = "#6FCF97"
FS5 = 250


def box(c, w, h, lab, col, sz=16):
    return VGroup(RoundedRectangle(corner_radius=0.15, width=w, height=h, color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.18).move_to(c),
                  txt(lab, c, P.fg, sz))


# ------------------------------------------------------------------ 3: la pipeline
PIPE = [tr("import\n& check", "importa\ne controlla"), tr("filter\n(HP/LP)", "filtra\n(HP/LP)"), tr("bad\nchannels", "canali\ncattivi"),
        tr("re-reference", "ri-\nreferenzia"), "ICA", tr("epoch\n& baseline", "epoche\ne baseline"), tr("reject\n& report", "rigetta\ne documenta")]


def f03_pipeline(W=12.4):
    f = Fig()
    cols = [P.C, P.V, P.S, PURP, GRN, P.V, P.C]
    n = len(PIPE); step = W / n
    for k, lab in enumerate(PIPE):
        c = p2(-W / 2 + step * (k + 0.5), 0)
        f[f"b{k}"] = box(c, step - 0.4, 1.2, lab, cols[k], 16)
        if k < n - 1:
            f[f"a{k}"] = Arrow(c + p2((step - 0.4) / 2, 0), c + p2(step - (step - 0.4) / 2, 0), buff=0.02, color=P.fg, stroke_width=3, tip_length=0.13)
    return f


# ------------------------------------------------------------------ 5: filtri causali vs a fase zero
def erp_wave(t):
    return 5 * np.exp(-0.5 * ((t - 0.1) / 0.02) ** 2) - 7 * np.exp(-0.5 * ((t - 0.17) / 0.03) ** 2) + 9 * np.exp(-0.5 * ((t - 0.35) / 0.07) ** 2)


def filt_versions(fc=15.0):
    t = np.arange(-1.0, 2.0, 1 / FS5)
    x = erp_wave(t)
    sos = butter(4, fc, "lowpass", fs=FS5, output="sos")
    return t, x, sosfilt(sos, x), sosfiltfilt(sos, x)


def f05_causal(W=6.0, Hh=0.16):
    f = Fig()
    t, x, xc, xz = filt_versions(10.0)
    m = (t >= -0.1) & (t <= 0.7)
    O = p2(-W / 2, -0.4)
    X = lambda tt, y: O + p2((tt + 0.1) / 0.8 * W, Hh * y)
    f["z"] = Line(X(-0.1, 0), X(0.7, 0), color=P.aux, stroke_width=1.5)
    f["on"] = DashedLine(X(0, -1.5 / Hh * 0.1 - 6), X(0, 11), color=P.muted, stroke_width=1.5)
    f["x"] = VMobject(color=P.fg, stroke_width=2.5).set_points_as_corners([X(a, b) for a, b in zip(t[m], x[m])])
    f["c"] = VMobject(color=P.S, stroke_width=3.5).set_points_as_corners([X(a, b) for a, b in zip(t[m], xc[m])])
    f["zp"] = VMobject(color=P.V, stroke_width=3.5).set_points_as_corners([X(a, b) for a, b in zip(t[m], xz[m])])
    f["l0"] = txt(tr("original", "originale"), X(0.72, 9.0), P.fg, 15).align_to(X(0.72, 0), LEFT)
    f["l1"] = txt(tr("causal (one-pass): delayed", "causale (un passaggio): ritardato"), X(0.72, 6.0), P.S, 15).align_to(X(0.72, 0), LEFT)
    f["l2"] = txt(tr("zero-phase (filtfilt): no delay", "fase zero (filtfilt): nessun ritardo"), X(0.72, 3.0), P.V, 15).align_to(X(0.72, 0), LEFT)
    f["t0"] = txt("0 ms", X(0, -6.5), P.muted, 14)
    f["t1"] = txt("600 ms", X(0.6, -1.2), P.muted, 14)
    return f


# ------------------------------------------------------------------ 8: canali cattivi
def bad_signals(dur=4.0, fs=FS5):
    t = np.arange(0, dur, 1 / fs)
    chans = []
    for k, n in enumerate(["Fz", "FC1", "C3", "Cz", "C4", "CP2", "Pz", "Oz"]):
        x = periodic_eeg(dur, fs, seed=40 + k, peaks=((10, 1, 0.8),), uv=18)[1]
        if n == "C3":
            x = 0.03 * x
        if n == "C4":
            x = x + 10 * np.random.default_rng(3).normal(size=len(t))
        if n == "CP2":
            x = x + 35 * np.sin(2 * np.pi * t / dur) + 15 * np.sin(2 * np.pi * 2 * t / dur)
        chans.append((n, x))
    return t, chans


def f08_badch(W=6.8):
    f = Fig()
    t, chans = bad_signals()
    labs = {"C3": tr("flat", "piatto"), "C4": tr("noisy", "rumoroso"), "CP2": tr("drifting", "in deriva")}
    for k, (n, x) in enumerate(chans):
        y = 2.1 - 0.6 * k
        bad = n in labs
        f[f"n{k}"] = txt(n, p2(-W / 2 - 0.45, y), P.S if bad else P.muted, 15, weight="BOLD" if bad else "NORMAL")
        f[f"x{k}"] = trace(t, x, p2(-W / 2, y), W, 0.006, P.S if bad else P.V, 1.4)
        if bad:
            f[f"l{k}"] = txt(labs[n], p2(W / 2 + 0.75, y), P.S, 15, weight="BOLD")
    return f


# ------------------------------------------------------------------ 9: interpolazione a spline sferiche
def bad_topos():
    vals = []
    for n in NAMES:
        e = el3d(n)
        vals.append(float(dipole_pot(e[None, :], np.array([0.0, -0.35, 0.55]), np.array([0, -0.3, 1.0]))[0]))
    vals = np.array(vals); vals /= np.abs(vals).max()
    bad = vals.copy(); ib = NAMES.index("C4"); bad[ib] = -2.5
    good = vals.copy()
    others = [i for i in range(len(NAMES)) if i != ib]
    Eb = el3d("C4"); d = np.array([np.arccos(np.clip(el3d(NAMES[i]) @ Eb, -1, 1)) for i in others])
    w = 1 / d ** 3; good[ib] = (w @ vals[others]) / w.sum()
    return bad, good


def f09_interp(R=1.3):
    f = Fig()
    bad, good = bad_topos()
    for k, (v, lab) in enumerate(((bad, tr("C4 broken", "C4 guasto")), (good, tr("C4 interpolated", "C4 interpolato")))):
        c = p2(-1.8 + 3.6 * k, 0)
        V, m = interp_map(v, n=161, p=2.5)
        f[f"m{k}"], f[f"o{k}"] = topomap(V, m, c, R, vmax=1.0, elec=True)
        f[f"l{k}"] = txt(lab, c + p2(0, -R - 0.4), P.S if k == 0 else P.V, 17, weight="BOLD")
    f["a"] = Arrow(p2(-0.35, 0), p2(0.35, 0), buff=0, color=P.fg, stroke_width=4, tip_length=0.18)
    return f


# ------------------------------------------------------------------ 12: epoche
EVENTS = [0.8, 2.3, 3.7, 5.2]


def cont_signal(dur=6.5, fs=FS5, seed=7):
    t = np.arange(0, dur, 1 / fs)
    x = periodic_eeg(dur, fs, seed=seed, peaks=((10, 1, 0.9),), uv=14)[1]
    for e in EVENTS:
        x = x + np.where(t >= e, erp_wave(t - e), 0)
    return t, x


def f12_epochs(W=11.0):
    f = Fig()
    t, x = cont_signal()
    O = p2(-W / 2, 1.3)
    X = lambda tt: O + p2(tt / 6.5 * W, 0)
    f["x"] = trace(t, x, O, W, 0.03, P.V, 1.6)
    for k, e in enumerate(EVENTS):
        f[f"e{k}"] = VGroup(Line(X(e) + p2(0, -0.8), X(e) + p2(0, 0.9), color=P.S, stroke_width=2.5), txt(f"S{k + 1}", X(e) + p2(0, 1.1), P.S, 14, weight="BOLD"))
        f[f"w{k}"] = Rectangle(width=W / 6.5, height=1.6, stroke_width=0, fill_color=P.C, fill_opacity=0.15).move_to(X(e + 0.3))
    # epoche impilate
    for k, e in enumerate(EVENTS):
        m = (t >= e - 0.2) & (t < e + 0.8)
        y = -0.6 - 0.55 * k
        f[f"p{k}"] = trace(t[m] - e, x[m], p2(-2.0, y), 4.0, 0.012, P.V, 1.5, -0.2, 0.8)
    m = t < 0
    f["ax"] = DashedLine(p2(-2.0 + 0.8, -0.25), p2(-2.0 + 0.8, -2.45), color=P.S, stroke_width=1.8)
    f["lb"] = txt(tr("−200 … +800 ms around each event", "−200 … +800 ms attorno a ogni evento"), p2(4.3, -1.4), P.fg, 16)
    f["bl"] = Rectangle(width=0.8, height=2.2, stroke_width=0, fill_color=P.aux, fill_opacity=0.25).move_to(p2(-1.6, -1.42))
    f["blt"] = txt("baseline", p2(-1.6, -2.75), P.muted, 14)
    return f


# ------------------------------------------------------------------ 14: rigetto delle epoche
def f14_reject(W=5.0):
    f = Fig()
    thr = 100.0; hs = 0.006
    for k in range(5):
        t = np.arange(-0.2, 0.8, 1 / FS5)
        x = periodic_eeg(1.0, FS5, seed=60 + k, peaks=((10, 1, 0.8),), uv=25)[1] + erp_wave(t)
        if k == 2:
            x = x + 160 * np.exp(-0.5 * ((t - 0.3) / 0.08) ** 2)
        y = 1.8 - 0.95 * k
        bad = k == 2
        f[f"x{k}"] = trace(t, x, p2(-W / 2, y), W, hs, P.S if bad else P.V, 2)
        f[f"u{k}"] = DashedLine(p2(-W / 2, y + thr * hs), p2(W / 2, y + thr * hs), color=P.muted, stroke_width=1.2, dash_length=0.06)
        f[f"d{k}"] = DashedLine(p2(-W / 2, y - thr * hs), p2(W / 2, y - thr * hs), color=P.muted, stroke_width=1.2, dash_length=0.06)
        f[f"k{k}"] = txt("✗" if bad else "✓", p2(W / 2 + 0.4, y), P.S if bad else P.V, 22, weight="BOLD")
    f["th"] = txt("±100 µV", p2(-W / 2 - 0.65, 1.8 + thr * hs), P.muted, 14)
    return f


# ------------------------------------------------------------------ 16-18: ICA
def sources(n=2000, seed=0):
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 4, n)
    s1 = np.sign(np.sin(2 * np.pi * 1.1 * t)) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.23 * t))   # "voce" 1: sub-gaussiana
    s2 = np.sin(2 * np.pi * 3.3 * t) ** 3                                                      # "voce" 2
    return t, np.vstack([s1, s2])


MIX = np.array([[0.8, 0.55], [0.35, 0.9]])


def f16_cocktail(W=3.2):
    f = Fig()
    t, S = sources(800)
    X = MIX @ S
    cols = [P.S, P.V]
    for k in range(2):
        y = 0.9 - 1.8 * k
        f[f"s{k}"] = trace(t, S[k], p2(-6.0, y), W, 0.45, cols[k], 2)
        f[f"x{k}"] = trace(t, X[k], p2(-0.5 * W + 0.9, y), W, 0.38, P.fg, 2)
        f[f"r{k}"] = trace(t, S[k], p2(3.4, y), W * 0.75, 0.45, cols[k], 2)
    f["ls"] = txt(tr("sources (brain, eyes…)", "sorgenti (cervello, occhi…)"), p2(-6.0 + W / 2, 1.9), P.fg, 16, weight="BOLD")
    f["lx"] = txt(tr("electrodes = mixtures", "elettrodi = miscele"), p2(0.9, 1.9), P.fg, 16, weight="BOLD")
    f["lr"] = txt(tr("ICA: recovered", "ICA: recuperate"), p2(3.4 + W * 0.375, 1.9), P.fg, 16, weight="BOLD")
    f["a1"] = Arrow(p2(-2.65, 0), p2(-1.0, 0), buff=0, color=P.fg, stroke_width=4, tip_length=0.18)
    f["m1"] = MathTex(r"\mathbf{A}", color=P.fg).scale(0.8).move_to(p2(-1.8, 0.35))
    f["a2"] = Arrow(p2(2.0 + 0.25, 0), p2(3.25, 0), buff=0, color=P.fg, stroke_width=4, tip_length=0.18)
    f["m2"] = MathTex(r"\mathbf{W}", color=P.fg).scale(0.8).move_to(p2(2.75, 0.35))
    return f


def f17_scatter(R=1.4):
    f = Fig()
    t, S = sources(1500, 1)
    rng = np.random.default_rng(2)
    S = np.vstack([rng.uniform(-1, 1, 700), rng.uniform(-1, 1, 700)])
    X = MIX @ S
    for k, (D, lab) in enumerate(((X, tr("mixtures x₁, x₂", "miscele x₁, x₂")), (S, tr("unmixed = independent", "separate = indipendenti")))):
        c = p2(-2.3 + 4.6 * k, 0)
        f[f"ax{k}"] = VGroup(Line(c + p2(-R, 0), c + p2(R, 0), color=P.aux, stroke_width=1.5), Line(c + p2(0, -R), c + p2(0, R), color=P.aux, stroke_width=1.5))
        sc = R / 1.5
        f[f"p{k}"] = VGroup(*[Dot(c + p2(a * sc, b * sc), radius=0.018, color=P.V if k else P.S) for a, b in zip(D[0], D[1])])
        f[f"l{k}"] = txt(lab, c + p2(0, -R - 0.35), P.fg, 16)
    f["ar"] = Arrow(p2(-0.55, 0), p2(0.55, 0), buff=0, color=P.fg, stroke_width=4, tip_length=0.18)
    f["w"] = MathTex(r"\mathbf{W}", color=P.fg).scale(0.8).move_to(p2(0, 0.4))
    return f


def f18_clt(W=2.6, Hh=1.5):
    f = Fig()
    rng = np.random.default_rng(5)
    labs = [tr("1 source", "1 sorgente"), tr("sum of 2", "somma di 2"), tr("sum of 10", "somma di 10")]
    for k, nsum in enumerate((1, 2, 10)):
        x = rng.uniform(-1, 1, (nsum, 40000)).sum(0) / np.sqrt(nsum)
        h, e = np.histogram(x, 30, density=True)
        O = p2(-4.6 + 3.3 * k, -0.8)
        wb = W / 30
        f[f"h{k}"] = VGroup(*[Rectangle(width=wb * 0.9, height=max(hh / h.max() * Hh, 0.005), stroke_width=0, fill_color=P.V if k < 2 else P.S, fill_opacity=0.85)
                              .move_to(O + p2(wb * (i + 0.5), 0), aligned_edge=DOWN) for i, hh in enumerate(h)])
        kurt = np.mean((x - x.mean()) ** 4) / np.var(x) ** 2 - 3
        f[f"l{k}"] = txt(labs[k], O + p2(W / 2, -0.3), P.fg, 16, weight="BOLD")
        f[f"k{k}"] = txt(tr(f"excess kurtosis ≈ {kurt:+.1f}", f"curtosi in eccesso ≈ {kurt:+.1f}").replace(".", "." if LANG == "en" else ","), O + p2(W / 2, -0.65), P.muted, 14)
    f["ar"] = Arrow(p2(-5.0, 1.35), p2(3.9, 1.35), buff=0, color=P.muted, stroke_width=3, tip_length=0.16)
    f["at"] = txt(tr("mixing → more Gaussian (central limit theorem)", "mescolare → più gaussiano (teorema del limite centrale)"), p2(-0.5, 1.7), P.muted, 16)
    return f


# ------------------------------------------------------------------ 20: galleria di componenti
IC_DEFS = [("eye", tr("eye (blink)", "occhio (ammiccamento)"), ([0.0, 0.7, 0.05], [0, 1.0, 0.3]), 0.15),
           ("muscle", tr("muscle (temporal)", "muscolo (temporale)"), ([0.68, 0.05, 0.2], [1.0, 0, 0.3]), 0.1),
           ("heart", tr("heart (ECG)", "cuore (ECG)"), ([[-1.6, -0.5, -1.2], [1.6, -0.5, -1.2]], [[0.2, 0, 1.0], [0.2, 0, -1.0]]), 0.3),
           ("line", tr("line noise / channel", "rete / canale"), ([-0.35, -0.2, 0.72], [-0.35, -0.2, 0.72]), 0.05),
           ("brain", tr("brain (posterior alpha)", "cervello (alfa posteriore)"), ([0.0, -0.5, 0.45], [0, -0.5, 1.0]), 0.2)]


def ic_timecourse(kind, dur=3.0, fs=FS5):
    t = np.arange(0, dur, 1 / fs)
    rng = np.random.default_rng(8)
    if kind == "eye":
        x = sum(150 * np.exp(-0.5 * ((t - c) / 0.08) ** 2) for c in (0.6, 2.1)) + 3 * rng.normal(size=len(t))
    elif kind == "muscle":
        x = np.convolve(rng.normal(size=len(t)), [0.3, 1, 0.3], "same") * 20 * (0.4 + (t > 1.2) * (t < 2.4))
    elif kind == "heart":
        x = sum(60 * np.exp(-0.5 * ((t - c) / 0.012) ** 2) - 8 * np.exp(-0.5 * ((t - c - 0.25) / 0.05) ** 2) for c in np.arange(0.2, dur, 0.8))
    elif kind == "line":
        x = 20 * np.sin(2 * np.pi * 50 * t) + 4 * rng.normal(size=len(t))
    else:
        x = periodic_eeg(dur, fs, seed=9, peaks=((10, 0.8, 2.0),), uv=30)[1]
    return t, x


def f20_ics(R=0.8):
    f = Fig()
    for k, (kind, lab, (pos, mom), blur) in enumerate(IC_DEFS):
        c = p2(-5.2 + 2.6 * k, 0.9)
        V, m = dipole_map(pos, mom, n=121, blur=blur)
        f[f"m{k}"], f[f"o{k}"] = topomap(V, m, c, R)
        t, x = ic_timecourse(kind)
        x = x / np.abs(x).max()
        f[f"x{k}"] = trace(t, x, c + p2(-1.05, -1.5), 2.1, 0.4, P.V if kind == "brain" else P.S, 1.4)
        f[f"l{k}"] = txt(lab, c + p2(0, -2.25), P.fg, 14, weight="BOLD")
    return f


# ------------------------------------------------------------------ 22: ricostruzione senza componenti artefattuali
def blink_mix(dur=4.0, fs=FS5):
    t = np.arange(0, dur, 1 / fs)
    blink = sum(150 * np.exp(-0.5 * ((t - c) / 0.08) ** 2) for c in (0.7, 2.4, 3.5))
    names = ["Fp1", "Fz", "Cz", "Pz"]; w = [1.0, 0.55, 0.25, 0.08]
    brain = [periodic_eeg(dur, fs, seed=70 + k, peaks=((10, 1, 0.5 + 0.3 * k),), uv=18)[1] for k in range(4)]
    return t, names, brain, [b + wk * blink for b, wk in zip(brain, w)]


def f22_backproj(W=4.6):
    f = Fig()
    t, names, brain, raw = blink_mix()
    for side, (D, lab, col) in enumerate(((raw, tr("raw", "grezzo"), P.S), (brain, tr("cleaned (eye IC removed)", "pulito (IC oculare rimossa)"), P.V))):
        x0 = -5.6 + 6.2 * side
        f[f"t{side}"] = txt(lab, p2(x0 + W / 2, 2.0), col, 17, weight="BOLD")
        for k, (n, x) in enumerate(zip(names, D)):
            y = 1.2 - 0.95 * k
            if side == 0:
                f[f"n{k}"] = txt(n, p2(x0 - 0.45, y), P.muted, 15)
            f[f"x{side}{k}"] = trace(t, x, p2(x0, y), W, 0.0045, col, 1.5)
    f["ar"] = Arrow(p2(-0.8, -0.2), p2(0.4, -0.2), buff=0, color=P.fg, stroke_width=4, tip_length=0.18)
    return f
