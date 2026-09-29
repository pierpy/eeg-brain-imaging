"""Figure della Lezione 4 EEG: registrazione (elettrodi, 10-20, amplificatori, campionamento, filtri, artefatti)."""
import os as _os
_R = _os.environ.get("COURSE_ROOT") or _os.path.dirname(_os.path.abspath(__file__))
while not _os.path.exists(_os.path.join(_R, ".course_root")) and _os.path.dirname(_R) != _R:
    _R = _os.path.dirname(_R)
import sys
sys.path.insert(0, _R + "/common")
import numpy as np
from eegfigs import *
from manim import (VGroup, VMobject, Arrow, Line, DashedLine, DoubleArrow, Dot, Circle, Ellipse, Polygon, Rectangle,
                   RoundedRectangle, Arc, ArcBetweenPoints, CurvedArrow, MathTex, ORIGIN, UP, DOWN, LEFT, RIGHT, PI)

P = F.P
PURP = "#8E7CC3"; GRN = "#6FCF97"


def box(c, w, h, lab, col, sz=17):
    return VGroup(RoundedRectangle(corner_radius=0.15, width=w, height=h, color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.18).move_to(c),
                  txt(lab, c, P.fg, sz))


# ------------------------------------------------------------------ 3: catena di registrazione
CHAIN = [(tr("electrodes", "elettrodi"), "µV"), (tr("amplifier", "amplificatore"), "×1000–×100 000"), (tr("analog filters", "filtri analogici"), tr("anti-aliasing", "anti-aliasing")),
         ("ADC", tr("sampling + quantisation", "campionamento + quantizzazione")), (tr("computer", "computer"), tr("storage, triggers", "salvataggio, trigger"))]


def f03_chain(W=12.0):
    f = Fig()
    cols = [P.C, P.S, P.V, PURP, GRN]
    n = len(CHAIN); step = W / n
    for k, (a, b) in enumerate(CHAIN):
        c = p2(-W / 2 + step * (k + 0.5), 0.3)
        f[f"b{k}"] = box(c, step - 0.55, 1.1, a, cols[k], 19)
        f[f"s{k}"] = txt(b, c + p2(0, -0.95), P.muted, 15)
        if k < n - 1:
            f[f"a{k}"] = Arrow(c + p2((step - 0.55) / 2, 0), c + p2(step - (step - 0.55) / 2, 0), buff=0.02, color=P.fg, stroke_width=3, tip_length=0.15)
    return f


# ------------------------------------------------------------------ 6: sistema 10-20 (vista dall'alto e laterale)
def f06_1020(R=1.8):
    f = Fig()
    c = p2(-2.4, 0)
    f["head"] = head(c, R)
    for k, ring in enumerate((0.5, 1.0)):
        f[f"r{k}"] = Circle(radius=R * 0.85 * ring, color=P.aux, stroke_width=1.2).move_to(c)
    f["ml"] = DashedLine(c + p2(0, -R * 0.95), c + p2(0, R * 0.95), color=P.aux, stroke_width=1.2)
    f["cl"] = DashedLine(c + p2(-R * 0.95, 0), c + p2(R * 0.95, 0), color=P.aux, stroke_width=1.2)
    for n in NAMES:
        p = c + el2d(n, R)
        col = P.S if n.endswith("z") else (P.V if n[-1] in "13579" else P.C)
        f["e" + n] = VGroup(Circle(radius=0.2, color=col, fill_color=P.bg, fill_opacity=1, stroke_width=2.5).move_to(p), txt(n, p, P.fg, 13, weight="BOLD"))
    # vista laterale con percentuali
    s = p2(3.0, -0.3); rr = 1.7
    f["side"] = Arc(radius=rr, start_angle=0, angle=PI, color=P.fg, stroke_width=3).move_to(s + p2(0, rr / 2))
    f["nas"] = txt(tr("nasion", "nasion"), s + p2(-rr - 0.2, -0.3), P.muted, 15)
    f["ini"] = txt(tr("inion", "inion"), s + p2(rr + 0.2, -0.3), P.muted, 15)
    angs = [0.1, 0.3, 0.5, 0.7, 0.9]
    names = ["Fpz", "Fz", "Cz", "Pz", "Oz"]
    pcts = ["10%", "20%", "20%", "20%", "20%", "10%"]
    base = s + p2(0, 0)
    for k, (a, nm) in enumerate(zip(angs, names)):
        th = PI * (1 - a)
        p = base + rr * np.array([np.cos(th), np.sin(th), 0])
        f[f"s{k}"] = VGroup(Dot(p, radius=0.08, color=P.S), txt(nm, p + 0.35 * np.array([np.cos(th), np.sin(th), 0]), P.fg, 13))
    for k, (a0, a1) in enumerate(zip([0] + angs, angs + [1])):
        th = PI * (1 - (a0 + a1) / 2)
        f[f"p{k}"] = txt(pcts[k], base + (rr - 0.35) * np.array([np.cos(th), np.sin(th), 0]), P.muted, 12)
    f["lg"] = txt(tr("odd = left · even = right · z = midline", "dispari = sinistra · pari = destra · z = linea mediana"), p2(-2.4, -2.35), P.fg, 15)
    return f


# ------------------------------------------------------------------ 8: amplificatore differenziale e CMRR
def f08_diffamp(W=3.2):
    f = Fig()
    t = np.linspace(0, 0.4, 800)
    brainA = 0.6 * np.sin(2 * np.pi * 10 * t) * np.exp(-((t - 0.2) / 0.15) ** 2)
    noise = 1.2 * np.sin(2 * np.pi * 50 * t)
    ya, yb = 1.2, -1.2
    f["a"] = trace(t, brainA + noise, p2(-5.8, ya), W, 0.35, P.V, 2)
    f["b"] = trace(t, noise, p2(-5.8, yb), W, 0.35, P.V, 2)
    f["la"] = txt(tr("active: brain + 50 Hz", "attivo: cervello + 50 Hz"), p2(-4.2, ya + 0.75), P.fg, 15)
    f["lb"] = txt(tr("reference: 50 Hz", "riferimento: 50 Hz"), p2(-4.2, yb + 0.75), P.fg, 15)
    amp = p2(0.2, 0)
    f["amp"] = Polygon(amp + p2(-0.8, 1.0), amp + p2(-0.8, -1.0), amp + p2(0.8, 0), color=P.fg, stroke_width=3)
    f["pl"] = txt("+", amp + p2(-0.6, 0.5), P.fg, 22); f["mi"] = txt("−", amp + p2(-0.6, -0.5), P.fg, 22)
    f["wa"] = VMobject(color=P.fg, stroke_width=2).set_points_as_corners([p2(-2.4, ya), p2(-1.5, ya), p2(-1.5, 0.5), amp + p2(-0.8, 0.5)])
    f["wb"] = VMobject(color=P.fg, stroke_width=2).set_points_as_corners([p2(-2.4, yb), p2(-1.5, yb), p2(-1.5, -0.5), amp + p2(-0.8, -0.5)])
    f["out"] = trace(t, brainA * 1.0, amp + p2(1.3, 0), W, 0.6, P.S, 3)
    f["lo"] = txt(tr("output = difference: noise cancels", "uscita = differenza: il rumore si annulla"), amp + p2(1.3 + W / 2, -0.9), P.S, 15)
    f["cm"] = MathTex(r"\mathrm{CMRR} = 20\log_{10}\frac{A_{diff}}{A_{cm}} \gtrsim 100\ \mathrm{dB}", color=P.fg).scale(0.65).move_to(amp + p2(1.3 + W / 2, 1.4))
    return f


# ------------------------------------------------------------------ 11: aliasing
def f11_alias(W=8.0, Hh=1.2):
    f = Fig()
    f0, fs = 40.0, 50.0
    t = np.linspace(0, 0.3, 2000)
    x = np.sin(2 * np.pi * f0 * t)
    ts = np.arange(0, 0.3, 1 / fs)
    xs = np.sin(2 * np.pi * f0 * ts)
    O = p2(-W / 2, 0)
    X = lambda tt: O + p2(tt / 0.3 * W, 0)
    f["true"] = VMobject(color=P.V, stroke_width=2.5).set_points_smoothly([X(a) + p2(0, Hh * b) for a, b in zip(t, x)])
    f["samp"] = VGroup(*[Dot(X(a) + p2(0, Hh * b), radius=0.08, color=P.S) for a, b in zip(ts, xs)])
    ta = np.linspace(0, 0.3, 400)
    f["alias"] = VMobject(color=P.S, stroke_width=3).set_points_smoothly([X(a) + p2(0, Hh * np.sin(2 * np.pi * (f0 - fs) * a)) for a in ta])
    f["lt"] = txt(tr("true signal: 40 Hz", "segnale vero: 40 Hz"), O + p2(1.2, Hh + 0.4), P.V, 16)
    f["la"] = txt(tr("sampled at 50 Hz → looks like 10 Hz!", "campionato a 50 Hz → sembra 10 Hz!"), O + p2(W - 2.3, Hh + 0.4), P.S, 16)
    return f


# ------------------------------------------------------------------ 13: filtri
def f13_filters(W=6.0, Hh=2.8):
    f = Fig()
    fr = np.logspace(-2, np.log10(250), 400)
    O = p2(-W / 2, -Hh / 2)
    lx = lambda v: logpos(v, 0.01, 250, W)
    hp = lambda v, fc=0.1, n=2: 1 / np.sqrt(1 + (fc / v) ** (2 * n))
    lp = lambda v, fc=40, n=4: 1 / np.sqrt(1 + (v / fc) ** (2 * n))
    notch = lambda v: 1 - 0.97 * np.exp(-0.5 * ((v - 50) / 1.2) ** 2)
    f["ax"] = axes(O, W + 0.2, Hh + 0.3, tr("frequency (Hz, log)", "frequenza (Hz, log)"), tr("gain", "guadagno"))
    f["bp"] = VMobject(color=P.V, stroke_width=4).set_points_smoothly([O + p2(lx(v), Hh * hp(v) * lp(v)) for v in fr])
    f["nt"] = VMobject(color=P.S, stroke_width=2.5).set_points_smoothly([O + p2(lx(v), Hh * hp(v) * lp(v) * notch(v)) for v in fr if v > 20])
    for v, s in ((0.1, "0.1"), (1, "1"), (10, "10"), (50, "50"), (100, "100")):
        f[f"t{s}"] = VGroup(Line(O + p2(lx(v), -0.06), O + p2(lx(v), 0.06), color=P.fg, stroke_width=2), txt(s, O + p2(lx(v), -0.28), P.muted, 14))
    f["lhp"] = txt(tr("high-pass: removes drifts", "passa-alto: rimuove derive"), O + p2(lx(0.1) + 0.5, Hh + 0.3), P.V, 15)
    f["llp"] = txt(tr("low-pass: removes EMG, anti-alias", "passa-basso: rimuove EMG, anti-alias"), O + p2(lx(40) - 0.3, Hh + 0.75), P.V, 15)
    f["lnt"] = txt("notch 50 Hz", O + p2(lx(50) - 1.2, 0.9), P.S, 15)
    return f


# ------------------------------------------------------------------ 15: artefatti
def artifact_signals(dur=6.0, fs=250):
    t = np.arange(0, dur, 1 / fs)
    base = lambda s: periodic_eeg(dur, fs, seed=s, peaks=((10, 1, 1.0),), uv=15)[1]
    blink = 150 * np.exp(-0.5 * ((t - 1.0) / 0.08) ** 2) + 140 * np.exp(-0.5 * ((t - 4.2) / 0.09) ** 2)
    sacc = 60 * (np.tanh((t - 2.5) / 0.01) - np.tanh((t - 3.3) / 0.01)) / 2
    rng = np.random.default_rng(2)
    emg = np.convolve(rng.normal(size=len(t)), np.ones(3) / 3, "same") * 25 * ((t > 3.6) & (t < 4.8))
    ecg = np.zeros_like(t)
    for c in np.arange(0.3, dur, 0.85):
        ecg += 50 * np.exp(-0.5 * ((t - c) / 0.012) ** 2) - 6 * np.exp(-0.5 * ((t - c - 0.25) / 0.06) ** 2)
    line = 20 * np.sin(2 * np.pi * 50 * t)
    pop = np.where(t > 5.0, -120 * np.exp(-(t - 5.0) / 0.3), 0)
    chans = [("Fp1", base(1) + blink + 0.3 * sacc), ("F8", base(2) + 0.4 * blink + sacc), ("T7", base(3) + emg), ("C3", base(4) + ecg),
             ("P3", base(5) + line), ("O1", base(6) + pop)]
    return t, chans


def f15_artifacts(W=7.4):
    f = Fig()
    t, chans = artifact_signals()
    for k, (n, x) in enumerate(chans):
        y = 2.1 - 0.85 * k
        f[f"n{k}"] = txt(n, p2(-W / 2 - 0.5, y), P.muted, 15)
        f[f"x{k}"] = trace(t, x, p2(-W / 2, y), W, 0.0045, P.V, 1.6)
    labs = [(1.0, 0, tr("blink", "ammiccamento"), P.S), (2.9, 1, tr("saccade", "saccade"), P.S), (4.2, 2, "EMG", P.S), (0.3, 3, "ECG", P.S), (0.6, 4, "50 Hz", P.S), (5.0, 5, tr("electrode pop", "pop dell'elettrodo"), P.S)]
    for j, (tt, k, s, col) in enumerate(labs):
        f[f"l{j}"] = txt(s, p2(-W / 2 + tt / 6.0 * W + 0.5, 2.1 - 0.85 * k + 0.4), col, 14, weight="BOLD")
    f["sb"] = VGroup(Line(p2(-W / 2, -2.8), p2(-W / 2 + W / 6, -2.8), color=P.fg, stroke_width=3), txt("1 s", p2(-W / 2 + W / 12, -3.05), P.muted, 14))
    return f


def f18_linenoise(W=5.5, Hh=3.0):
    f = Fig()
    t, x = periodic_eeg(20.0, seed=3, peaks=((10, 1, 1.2),), slope=2.2)
    x = x + 25 * np.sin(2 * np.pi * 50 * t) + 6 * np.sin(2 * np.pi * 100 * t)
    from scipy.signal import welch
    fr, pw = welch(x, 250, nperseg=1000)
    m = (fr >= 1) & (fr <= 120)
    fr, pw = fr[m], pw[m]
    O = p2(-W / 2, -Hh / 2)
    ly = lambda v: (np.log10(v) - np.log10(pw.min())) / (np.log10(pw.max()) - np.log10(pw.min())) * Hh
    f["ax"] = axes(O, W + 0.2, Hh + 0.2, tr("frequency (Hz)", "frequenza (Hz)"), tr("power (log)", "potenza (log)"))
    f["p"] = VMobject(color=P.V, stroke_width=3).set_points_as_corners([O + p2(a / 120 * W, ly(b)) for a, b in zip(fr, pw)])
    f["l50"] = txt("50 Hz", O + p2(50 / 120 * W + 0.45, ly(pw[np.argmin(np.abs(fr - 50))]) - 0.1), P.S, 16)
    f["l100"] = txt(tr("100 Hz (harmonic)", "100 Hz (armonica)"), O + p2(100 / 120 * W - 0.2, ly(pw[np.argmin(np.abs(fr - 100))]) + 0.35), P.S, 14)
    for v in (0, 25, 50, 75, 100):
        f[f"t{v}"] = txt(str(v), O + p2(v / 120 * W, -0.25), P.muted, 14)
    return f
