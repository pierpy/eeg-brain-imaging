"""Figure della Lezione 6 EEG: analisi spettrale e tempo-frequenza (dati SIMULATI)."""
import os as _os
_R = _os.environ.get("COURSE_ROOT") or _os.path.dirname(_os.path.abspath(__file__))
while not _os.path.exists(_os.path.join(_R, ".course_root")) and _os.path.dirname(_R) != _R:
    _R = _os.path.dirname(_R)
import sys
sys.path.insert(0, _R + "/common")
import numpy as np
from eegfigs import *
from manim import (VGroup, VMobject, Arrow, Line, DashedLine, DoubleArrow, Dot, Circle, Polygon, Rectangle,
                   RoundedRectangle, MathTex, ImageMobject, ORIGIN, UP, DOWN, LEFT, RIGHT, PI)
from scipy.signal import welch, butter, sosfiltfilt, hilbert, spectrogram

P = F.P
PURP = "#8E7CC3"; GRN = "#6FCF97"
FS6 = 250


def dec(v, n=2):
    s = f"{v:.{n}f}"
    return s if LANG == "en" else s.replace(".", ",")


# ------------------------------------------------------------------ utilità: immagini da matrici
def seq_cmap(v):
    """0..1 -> blu scuro, teal, giallo (tipo viridis)."""
    v = np.clip(v, 0, 1)[..., None]
    c0 = np.array([0.20, 0.10, 0.35]); c1 = np.array([0.13, 0.55, 0.55]); c2 = np.array([0.99, 0.85, 0.20])
    return np.where(v < 0.5, c0 * (1 - 2 * v) + c1 * 2 * v, c1 * (2 - 2 * v) + c2 * (2 * v - 1))


def mat_img(Z, W, H, c=ORIGIN, cmap="seq", vmin=None, vmax=None):
    """ImageMobject da una matrice (righe = frequenze dal basso verso l'alto)."""
    Z = np.asarray(Z, float)
    if cmap == "seq":
        vmin = np.nanmin(Z) if vmin is None else vmin; vmax = np.nanmax(Z) if vmax is None else vmax
        rgb = seq_cmap((Z - vmin) / (vmax - vmin + 1e-12))
    else:
        vmax = np.nanmax(np.abs(Z)) if vmax is None else vmax
        rgb = cmap_rdbu(Z / vmax)
    img = (np.dstack([rgb[::-1], np.ones(Z.shape)]) * 255).astype(np.uint8)
    m = ImageMobject(img)
    from manim import RESAMPLING_ALGORITHMS
    m.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    m.stretch_to_fit_width(W); m.stretch_to_fit_height(H); m.move_to(c)
    return m


def frame_axes(O, W, H, xt, yt, xl="", yl="", col=None, sz=13):
    """cornice con tacche: xt/yt = [(pos_rel 0..1, etichetta)]."""
    col = col or P.fg
    g = VGroup(Rectangle(width=W, height=H, color=col, stroke_width=1.5).move_to(O + p2(W / 2, H / 2)))
    for u, s in xt:
        g.add(Line(O + p2(u * W, 0), O + p2(u * W, -0.07), color=col, stroke_width=1.5), txt(s, O + p2(u * W, -0.25), P.muted, sz))
    for u, s in yt:
        g.add(Line(O + p2(0, u * H), O + p2(-0.07, u * H), color=col, stroke_width=1.5), txt(s, O + p2(-0.3, u * H), P.muted, sz))
    if xl: g.add(txt(xl, O + p2(W / 2, -0.55), P.muted, sz + 2))
    if yl: g.add(txt(yl, O + p2(-0.75, H / 2), P.muted, sz + 2).rotate(PI / 2))
    return g


# ------------------------------------------------------------------ 5: Fourier = somma di sinusoidi
COMP = [(2.0, 1.0, 0.3, P.C if hasattr(P, "C") else "#E0A030"), (10.0, 0.8, 1.1, None), (21.0, 0.35, 2.0, None)]


def fourier_parts(t):
    cols = [PURP, P.S, P.V]
    comps = [(f, a, ph, cols[k]) for k, (f, a, ph, _) in enumerate(COMP)]
    xs = [a * np.sin(2 * np.pi * f * t + ph) for f, a, ph, _ in comps]
    return comps, xs


def f05_fourier(W=6.0):
    f = Fig()
    t = np.linspace(0, 1, 600)
    comps, xs = fourier_parts(t)
    O = p2(-W / 2, 1.6)
    f["sum"] = VMobject(color=P.fg, stroke_width=3).set_points_as_corners([O + p2(a * W, 0.45 * b) for a, b in zip(t, sum(xs))])
    f["ls"] = txt(tr("EEG segment (1 s)", "segmento EEG (1 s)"), O + p2(-1.0, 0), P.fg, 15, weight="BOLD")
    for k, ((fr, a, ph, col), x) in enumerate(zip(comps, xs)):
        y = 0.1 - 1.0 * k
        f[f"c{k}"] = VMobject(color=col, stroke_width=2.5).set_points_as_corners([p2(-W / 2 + u * W, y + 0.4 * v) for u, v in zip(t, x)])
        f[f"l{k}"] = txt(f"{fr:g} Hz", p2(-W / 2 - 1.0, y), col, 15, weight="BOLD")
        f[f"p{k}"] = txt("+" if k else "=", p2(-W / 2 - 0.3, y + 0.5), P.muted, 20)
    # spettro a barre
    Os = p2(W / 2 + 0.8, -2.0)
    f["sax"] = axes(Os, 2.8, 2.9, tr("freq. (Hz)", "freq. (Hz)"), tr("amplitude", "ampiezza"))
    for k, (fr, a, ph, col) in enumerate(comps):
        x = fr / 25 * 2.6
        f[f"b{k}"] = Line(Os + p2(x, 0), Os + p2(x, a * 2.4), color=col, stroke_width=7)
    return f


# ------------------------------------------------------------------ 6: risoluzione in frequenza
def two_peaks(T, fs=FS6, pad=4096):
    t = np.arange(0, T, 1 / fs)
    x = np.sin(2 * np.pi * 10 * t) + 0.8 * np.sin(2 * np.pi * 11 * t + 1)
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)), pad)) / len(x)
    fr = np.fft.rfftfreq(pad, 1 / fs)
    return fr, X / X.max()


def f06_resolution(W=4.2, Hh=2.0):
    f = Fig()
    for k, T in enumerate((0.5, 2.0)):
        fr, X = two_peaks(T)
        m = (fr >= 5) & (fr <= 16)
        O = p2(-5.0 + 5.6 * k, -1.0)
        f[f"ax{k}"] = axes(O, W + 0.2, Hh + 0.3, "Hz", "")
        f[f"s{k}"] = VMobject(color=P.V if k else P.S, stroke_width=3.5).set_points_smoothly([O + p2((a - 5) / 11 * W, Hh * b) for a, b in zip(fr[m], X[m])])
        for v in (10, 11):
            f[f"d{k}{v}"] = DashedLine(O + p2((v - 5) / 11 * W, 0), O + p2((v - 5) / 11 * W, Hh + 0.1), color=P.muted, stroke_width=1.2)
        f[f"t{k}"] = txt(f"T = {dec(T, 1)} s  →  Δf = {dec(1 / T, 1)} Hz", O + p2(W / 2, Hh + 0.6), P.V if k else P.S, 17, weight="BOLD")
        f[f"x{k}"] = VGroup(*[txt(str(v), O + p2((v - 5) / 11 * W, -0.25), P.muted, 13) for v in (5, 10, 11, 15)])
    f["n"] = txt(tr("10 Hz + 11 Hz: resolved only with T ≥ 1 s", "10 Hz + 11 Hz: separati solo con T ≥ 1 s"), p2(0.2, -2.0), P.fg, 16)
    return f


# ------------------------------------------------------------------ 7: leakage e finestre
def leak_spec(f0=10.3, T=1.0, win="rect", fs=FS6, pad=4096):
    t = np.arange(0, T, 1 / fs)
    x = np.sin(2 * np.pi * f0 * t)
    w = np.ones(len(t)) if win == "rect" else np.hanning(len(t))
    X = np.abs(np.fft.rfft(x * w, pad)); X = X / X.max()
    fr = np.fft.rfftfreq(pad, 1 / fs)
    return fr, 20 * np.log10(X + 1e-6)


def f07_leakage(W=5.0, Hh=2.6):
    f = Fig()
    O = p2(-W / 2 - 0.3, -1.5)
    f["ax"] = axes(O, W + 0.2, Hh + 0.3, tr("frequency (Hz)", "frequenza (Hz)"), tr("power (dB)", "potenza (dB)"))
    yy = lambda d: (np.maximum(d, -80) + 80) / 80 * Hh
    for k, (w, col, lab) in enumerate((("rect", P.S, tr("rectangular window", "finestra rettangolare")), ("hann", P.V, tr("Hann window", "finestra di Hann")))):
        fr, D = leak_spec(win=w)
        m = (fr >= 0) & (fr <= 30)
        f[f"s{k}"] = VMobject(color=col, stroke_width=3).set_points_as_corners([O + p2(a / 30 * W, yy(b)) for a, b in zip(fr[m], D[m])])
        f[f"l{k}"] = txt(lab, O + p2(W + 1.6, Hh - 0.4 - 0.5 * k), col, 16, weight="BOLD")
    for v in (0, 10, 20, 30):
        f[f"x{v}"] = txt(str(v), O + p2(v / 30 * W, -0.25), P.muted, 13)
    for d in (0, -40, -80):
        f[f"y{d}"] = txt(str(d), O + p2(-0.35, yy(d)), P.muted, 13)
    return f


# ------------------------------------------------------------------ 9: Welch
def rest_signal(dur=60.0, fs=FS6, seed=4):
    return eeg(dur, fs, seed=seed, alpha=1.3, beta=0.5, theta=0.3, delta=0.3, uv=25)


def f09_welch(W=5.2, Hh=2.8):
    f = Fig()
    t, x = rest_signal()
    fr1 = np.fft.rfftfreq(len(x), 1 / FS6); P1 = 2 * np.abs(np.fft.rfft(x)) ** 2 / (len(x) * FS6)
    fr2, P2 = welch(x, FS6, nperseg=2 * FS6)
    O = p2(-W / 2, -1.5)
    f["ax"] = axes(O, W + 0.2, Hh + 0.3, tr("frequency (Hz)", "frequenza (Hz)"), tr("power (log)", "potenza (log)"))
    lo, hi = np.log10(P2[(fr2 > 1) & (fr2 < 40)].min()) - 1.2, np.log10(P1[(fr1 > 1) & (fr1 < 40)].max())
    yy = lambda v: (np.log10(v) - lo) / (hi - lo) * Hh
    m1 = (fr1 >= 1) & (fr1 <= 40); m2 = (fr2 >= 1) & (fr2 <= 40)
    f["p1"] = VMobject(color=P.muted, stroke_width=1).set_points_as_corners([O + p2((a - 1) / 39 * W, max(yy(b), 0)) for a, b in zip(fr1[m1][::2], P1[m1][::2])])
    f["p2"] = VMobject(color=P.S, stroke_width=4).set_points_smoothly([O + p2((a - 1) / 39 * W, yy(b)) for a, b in zip(fr2[m2], P2[m2])])
    f["l1"] = txt(tr("single periodogram (60 s)", "periodogramma unico (60 s)"), O + p2(W * 0.7, Hh + 0.1), P.muted, 15)
    f["l2"] = txt(tr("Welch: 2-s segments, 50 % overlap", "Welch: segmenti di 2 s, 50 % sovrapposti"), O + p2(W * 0.7, Hh - 0.35), P.S, 15, weight="BOLD")
    for v in (1, 10, 20, 30, 40):
        f[f"x{v}"] = txt(str(v), O + p2((v - 1) / 39 * W, -0.25), P.muted, 13)
    return f


# ------------------------------------------------------------------ 11: periodico vs aperiodico
def f11_fooof(W=4.4, Hh=2.6):
    f = Fig()
    fr = np.linspace(1, 40, 300)
    ap = 2.2 - 1.5 * np.log10(fr)
    pk = 0.9 * np.exp(-0.5 * ((fr - 10) / 1.3) ** 2) + 0.3 * np.exp(-0.5 * ((fr - 20) / 2.5) ** 2)
    L = ap + pk
    lx = lambda v: logpos(v, 1, 40, W)
    for k in range(2):
        O = p2(-5.0 + 5.6 * k, -1.4)
        f[f"ax{k}"] = axes(O, W + 0.2, Hh + 0.3, tr("frequency (Hz, log)", "frequenza (Hz, log)"), tr("log power", "log potenza") if k == 0 else tr("log power − aperiodic", "log potenza − aperiodica"))
        for v in (1, 4, 10, 20, 40):
            f[f"x{k}{v}"] = txt(str(v), O + p2(lx(v), -0.25), P.muted, 13)
    O0 = p2(-5.0, -1.4); O1 = p2(0.6, -1.4)
    yy0 = lambda v: (v + 0.4) / 3.0 * Hh
    f["s"] = VMobject(color=P.V, stroke_width=3.5).set_points_smoothly([O0 + p2(lx(a), yy0(b)) for a, b in zip(fr, L)])
    f["ap"] = DashedLine(O0 + p2(lx(1), yy0(ap[0])), O0 + p2(lx(40), yy0(ap[-1])), color=P.S, stroke_width=3)
    f["la"] = txt(tr("aperiodic 1/fᵡ (slope χ, offset)", "aperiodica 1/fᵡ (pendenza χ, offset)"), O0 + p2(W / 2 + 0.3, Hh + 0.2), P.S, 15)
    yy1 = lambda v: v / 1.1 * Hh
    f["pk"] = VMobject(color=P.V, stroke_width=3.5).set_points_smoothly([O1 + p2(lx(a), yy1(b)) for a, b in zip(fr, pk)])
    f["lp"] = txt(tr("periodic peaks: centre, power, width", "picchi periodici: centro, potenza, larghezza"), O1 + p2(W / 2 + 0.3, Hh + 0.2), P.V, 15)
    return f


# ------------------------------------------------------------------ 14: STFT e compromesso tempo-frequenza
def test_signal(fs=FS6, dur=4.0):
    t = np.arange(0, dur, 1 / fs)
    x = np.sin(2 * np.pi * (4 * t + 3.0 * t ** 2))                          # chirp 4 -> 28 Hz
    x = x + 1.2 * np.exp(-0.5 * ((t - 1.0) / 0.05) ** 2) * np.sin(2 * np.pi * 30 * t)   # breve burst a 30 Hz
    x = x + 0.8 * (t > 2.8) * (t < 3.6) * np.sin(2 * np.pi * 10 * t)       # alfa sostenuto
    return t, x


def stft_map(win, fs=FS6):
    t, x = test_signal()
    fr, tt, S = spectrogram(x, fs, window="hann", nperseg=int(win * fs), noverlap=int(win * fs) - 2, nfft=512)
    m = fr <= 40
    A = np.sqrt(S[m]); return fr[m], tt, A / A.max()


def f14_stft(W=4.6, Hh=2.4):
    f = Fig()
    t, x = test_signal()
    f["x"] = trace(t, x, p2(-W - 0.6, 1.9), 2 * W + 1.2, 0.3, P.fg, 1.3)
    for k, win in enumerate((0.125, 1.0)):
        fr, tt, S = stft_map(win)
        O = p2(-5.2 + 5.8 * k, -1.8)
        f[f"m{k}"] = mat_img(S, W, Hh, O + p2(W / 2, Hh / 2), vmin=0, vmax=0.8)
        f[f"a{k}"] = frame_axes(O, W, Hh, [(0, "0"), (0.5, "2"), (1, "4 s")], [(0, "0"), (0.5, "20"), (1, "40 Hz")])
        f[f"t{k}"] = txt(tr(f"window {dec(win * 1000, 0)} ms: " + ("sharp in time" if k == 0 else "sharp in frequency"),
                            f"finestra {dec(win * 1000, 0)} ms: " + ("nitida nel tempo" if k == 0 else "nitida in frequenza")), O + p2(W / 2, Hh + 0.3), P.S if k == 0 else P.V, 16, weight="BOLD")
    return f


# ------------------------------------------------------------------ 15: wavelet di Morlet
def morlet(fc, n, t):
    s = n / (2 * np.pi * fc)
    return np.exp(2j * np.pi * fc * t) * np.exp(-t ** 2 / (2 * s ** 2)), s


def f15_morlet(W=3.4):
    f = Fig()
    t = np.linspace(-0.6, 0.6, 1200)
    for k, fc in enumerate((4, 10, 30)):
        w, s = morlet(fc, 6, t)
        c = p2(-4.4 + 4.4 * k, 0.4)
        f[f"r{k}"] = VMobject(color=P.V, stroke_width=2.5).set_points_as_corners([c + p2(a / 1.2 * W, 1.0 * b) for a, b in zip(t, w.real)])
        f[f"e{k}"] = VMobject(color=P.S, stroke_width=2).set_points_as_corners([c + p2(a / 1.2 * W, 1.0 * abs(b)) for a, b in zip(t, w)])
        f[f"l{k}"] = txt(f"{fc} Hz · 6 " + tr("cycles", "cicli"), c + p2(0, -1.35), P.fg, 16, weight="BOLD")
        f[f"s{k}"] = txt(f"σ_t = {dec(s * 1000, 0)} ms   σ_f = {dec(1 / (2 * np.pi * s), 1)} Hz", c + p2(0, -1.75), P.muted, 14)
    return f


# ------------------------------------------------------------------ 17: mappa tempo-frequenza (ERD/ERS)
TF_T = np.linspace(-0.5, 1.5, 200)
TF_F = np.logspace(np.log10(2), np.log10(40), 80)


def tf_model():
    T_, F_ = np.meshgrid(TF_T, TF_F)
    g = lambda t0, st, f0, sf, a: a * np.exp(-0.5 * ((T_ - t0) / st) ** 2 - 0.5 * ((np.log(F_) - np.log(f0)) / sf) ** 2)
    Z = g(0.25, 0.12, 5.0, 0.25, 2.5)                     # theta ERS precoce
    Z += g(0.75, 0.35, 10.5, 0.12, -3.0)                 # alfa ERD
    Z += g(0.6, 0.3, 20.0, 0.15, -2.0)                   # beta ERD
    Z += g(1.25, 0.15, 20.0, 0.15, 1.8)                  # beta rebound
    Z += g(0.15, 0.05, 35.0, 0.1, 1.5)                   # gamma breve
    Z *= (T_ > -0.05) | (np.abs(Z) < 0)                  # niente prima dello stimolo
    rng = np.random.default_rng(1)
    from scipy.ndimage import gaussian_filter
    Z += gaussian_filter(rng.normal(size=Z.shape), 2) * 0.8
    return Z


def f17_tfmap(W=6.4, Hh=3.4):
    f = Fig()
    Z = tf_model()
    O = p2(-W / 2, -Hh / 2)
    f["m"] = mat_img(Z, W, Hh, ORIGIN, cmap="div", vmax=3.0)
    fy = lambda v: logpos(v, 2, 40, 1.0)
    f["a"] = frame_axes(O, W, Hh, [((v + 0.5) / 2.0, s) for v, s in ((-0.5, "−0.5"), (0, "0"), (0.5, "0.5"), (1.0, "1"), (1.5, "1.5 s"))],
                        [(fy(v), str(v)) for v in (2, 4, 10, 20, 40)], tr("time (s)", "tempo (s)"), "Hz")
    f["z"] = DashedLine(O + p2(0.25 * W, 0), O + p2(0.25 * W, Hh), color=P.fg, stroke_width=2)
    labs = [(0.25, 5, "theta ERS", 0.1), (0.75, 10.5, "alpha ERD", 0.0), (1.25, 20, tr("beta rebound", "rebound beta"), 0.0), (0.15, 35 * 0.72, "gamma", 0.5)]
    for k, (tt, fq, s, dx) in enumerate(labs):
        f[f"l{k}"] = txt(s, O + p2((tt + 0.5) / 2 * W + dx, fy(fq) * Hh + 0.33), P.fg, 14, weight="BOLD")
    # barra colori
    cb = np.linspace(-1, 1, 100)[:, None] * np.ones((1, 5))
    f["cb"] = mat_img(cb, 0.22, Hh * 0.8, O + p2(W + 0.45, Hh / 2), cmap="div", vmax=1.0)
    f["cbt"] = VGroup(txt("+3 dB", O + p2(W + 0.45, Hh * 0.9 + 0.2), P.muted, 13), txt("−3 dB", O + p2(W + 0.45, Hh * 0.1 - 0.2), P.muted, 13))
    return f


# ------------------------------------------------------------------ 18: evocato vs indotto
def trials_ev_ind(n=30, fs=FS6, seed=3, jitter=False):
    rng = np.random.default_rng(seed)
    t = np.arange(-0.2, 0.8, 1 / fs)
    X = []
    for i in range(n):
        ph = rng.uniform(0, 2 * np.pi) if jitter else 0.0
        lat = rng.normal(0, 0.03) if jitter else 0.0
        X.append(np.exp(-0.5 * ((t - 0.2 - lat) / 0.06) ** 2) * np.sin(2 * np.pi * 20 * (t - 0.2) + ph) + 0.35 * rng.normal(size=len(t)))
    return t, np.array(X)


def f18_evoked_induced(W=4.2):
    f = Fig()
    for k, jit in enumerate((False, True)):
        t, X = trials_ev_ind(jitter=jit)
        x0 = -5.5 + 6.0 * k
        f[f"h{k}"] = txt(tr("evoked (phase-locked)", "evocato (agganciato in fase)") if k == 0 else tr("induced (not phase-locked)", "indotto (non agganciato in fase)"), p2(x0 + W / 2, 2.3), P.S if k == 0 else P.V, 17, weight="BOLD")
        for i in range(5):
            f[f"t{k}{i}"] = trace(t, X[i], p2(x0, 1.7 - 0.42 * i), W, 0.17, P.muted, 1.2)
        f[f"av{k}"] = trace(t, X.mean(0), p2(x0, -0.9), W, 0.5, P.S if k == 0 else P.V, 3)
        f[f"la{k}"] = txt(tr("average of trials", "media dei trial"), p2(x0 + W / 2, -0.35), P.fg, 14)
        env = np.abs(hilbert(X, axis=1)) ** 2
        pw = env.mean(0); pw = pw / pw.max()
        f[f"pw{k}"] = VMobject(color=AMB if False else P.C, stroke_width=3).set_points_as_corners([p2(x0 + (a + 0.2) / 1.0 * W, -2.5 + 0.9 * b) for a, b in zip(t, pw)])
        f[f"lp{k}"] = txt(tr("average of power (TF)", "media della potenza (TF)"), p2(x0 + W / 2, -1.45), P.fg, 14)
    return f


# ------------------------------------------------------------------ 20: ITPC
def f20_itpc(R=1.3):
    f = Fig()
    rng = np.random.default_rng(6)
    for k, (kap, lab) in enumerate(((0.0, tr("random phases", "fasi casuali")), (3.0, tr("phase-locked", "agganciate in fase")))):
        c = p2(-2.2 + 4.4 * k, 0)
        ph = rng.uniform(-np.pi, np.pi, 40) if kap == 0 else rng.vonmises(0.8, kap, 40)
        f[f"c{k}"] = Circle(radius=R, color=P.aux, stroke_width=2).move_to(c)
        f[f"v{k}"] = VGroup(*[Line(c, c + R * np.array([np.cos(a), np.sin(a), 0]), color=P.V, stroke_width=1.5, stroke_opacity=0.6) for a in ph])
        m = np.mean(np.exp(1j * ph))
        f[f"r{k}"] = Arrow(c, c + R * np.array([m.real, m.imag, 0]), buff=0, color=P.S, stroke_width=6, tip_length=0.2, max_tip_length_to_length_ratio=0.5)
        f[f"l{k}"] = txt(f"{lab}: ITPC = {dec(abs(m))}", c + p2(0, -R - 0.4), P.fg, 16, weight="BOLD")
    return f


# ------------------------------------------------------------------ 21: Hilbert: ampiezza e fase
def alpha_band(dur=2.0, fs=FS6):
    t, x = periodic_eeg(dur, fs, seed=12, peaks=((10, 0.8, 2.0),), uv=20)
    sos = butter(4, [8, 12], "bandpass", fs=fs, output="sos")
    xb = sosfiltfilt(sos, x)
    a = hilbert(xb)
    return t, x, xb, np.abs(a), np.angle(a)


def f21_hilbert(W=9.0):
    f = Fig()
    t, x, xb, amp, ph = alpha_band()
    O = p2(-W / 2, 1.6)
    f["x"] = trace(t, x, O, W, 0.03, P.muted, 1.4)
    f["lx"] = txt(tr("raw", "grezzo"), O + p2(-0.8, 0), P.muted, 15)
    O2 = p2(-W / 2, 0.0)
    f["b"] = trace(t, xb, O2, W, 0.045, P.V, 2.2)
    f["e"] = trace(t, amp, O2, W, 0.045, P.S, 3)
    f["lb"] = txt("8–12 Hz", O2 + p2(-0.8, 0.15), P.V, 15, weight="BOLD")
    f["le"] = txt(tr("amplitude |z(t)|", "ampiezza |z(t)|"), O2 + p2(W + 1.0, 0.6), P.S, 15, weight="BOLD")
    O3 = p2(-W / 2, -1.8)
    f["p"] = trace(t, ph, O3, W, 0.25, P.C, 2)
    f["lp"] = txt(tr("phase ∠z(t)", "fase ∠z(t)"), O3 + p2(W + 0.9, 0), P.C, 15, weight="BOLD")
    f["pi"] = VGroup(txt("+π", O3 + p2(-0.35, 0.25 * np.pi), P.muted, 13), txt("−π", O3 + p2(-0.35, -0.25 * np.pi), P.muted, 13))
    return f


# ------------------------------------------------------------------ 22: accoppiamento fase-ampiezza
def pac_signal(dur=2.0, fs=500):
    t = np.arange(0, dur, 1 / fs)
    th = np.sin(2 * np.pi * 6 * t)
    gam = (0.2 + 0.8 * (1 + th) / 2) * 0.35 * np.sin(2 * np.pi * 60 * t)
    return t, th, gam, th + gam


def f22_pac(W=6.0):
    f = Fig()
    t, th, gam, x = pac_signal()
    O = p2(-W / 2 - 1.8, 1.2)
    f["x"] = trace(t, x, O, W, 0.6, P.fg, 1.5)
    f["lx"] = txt(tr("signal", "segnale"), O + p2(-0.8, 0), P.muted, 15)
    f["th"] = trace(t, th, O + p2(0, -1.5), W, 0.4, P.V, 2.5)
    f["lt"] = txt(tr("theta phase", "fase theta"), O + p2(-0.9, -1.5), P.V, 15, weight="BOLD")
    f["g"] = trace(t, gam, O + p2(0, -2.8), W, 1.0, P.S, 1.5)
    f["lg"] = txt(tr("gamma amplitude", "ampiezza gamma"), O + p2(-1.0, -2.8), P.S, 15, weight="BOLD")
    # istogramma ampiezza per fase
    Ob = p2(W / 2 - 0.5, -2.0)
    bins = np.linspace(-np.pi, np.pi, 19)
    phase = np.angle(hilbert(th)); am = np.abs(hilbert(gam))
    hb = np.array([am[(phase >= a) & (phase < b)].mean() for a, b in zip(bins[:-1], bins[1:])]); hb /= hb.sum()
    wb = 2.6 / 18
    f["hb"] = VGroup(*[Rectangle(width=wb * 0.9, height=v / hb.max() * 2.0, stroke_width=0, fill_color=P.S, fill_opacity=0.85).move_to(Ob + p2(wb * (i + 0.5), 0), aligned_edge=DOWN) for i, v in enumerate(hb)])
    f["hax"] = Line(Ob, Ob + p2(2.6, 0), color=P.fg, stroke_width=2)
    f["hl"] = VGroup(txt("−π", Ob + p2(0, -0.25), P.muted, 13), txt("0", Ob + p2(1.3, -0.25), P.muted, 13), txt("+π", Ob + p2(2.6, -0.25), P.muted, 13))
    f["ht"] = txt(tr("gamma amplitude by theta phase", "ampiezza gamma per fase theta"), Ob + p2(1.3, 2.4), P.fg, 15)
    return f
