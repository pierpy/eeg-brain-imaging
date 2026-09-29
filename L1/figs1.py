"""Figure della Lezione 1 EEG: storia e che cosa misura l'EEG."""
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


def f05_resolution():
    return f_resolution(7.0, 4.6)


# ------------------------------------------------------------------ EEG diretto vs BOLD ritardato
def hrf(t):
    """funzione di risposta emodinamica canonica (doppia gamma, SPM)."""
    from scipy.stats import gamma
    return gamma.pdf(t, 6) - gamma.pdf(t, 16) / 6


def f06_eeg_vs_bold(W=7.0):
    f = Fig()
    t = np.linspace(0, 20, 2001)
    stim = ((t > 2) & (t < 2.5)).astype(float)
    # risposta neurale (evocato breve) e BOLD
    neur = np.exp(-0.5 * ((t - 2.35) / 0.12) ** 2) - 0.6 * np.exp(-0.5 * ((t - 2.7) / 0.15) ** 2)
    dt = t[1] - t[0]
    bold = np.convolve(stim, hrf(t))[:len(t)] * dt
    bold /= bold.max()
    ys = [1.7, 0.2, -1.5]
    lab = [tr("stimulus", "stimolo"), tr("neural response → EEG (ms)", "risposta neurale → EEG (ms)"), tr("BOLD (fMRI): peak after ~5 s", "BOLD (fMRI): picco dopo ~5 s")]
    cols = [P.muted, P.S, P.V]
    for k, (y, sig) in enumerate(zip(ys, (stim, neur, bold))):
        O = p2(-W / 2, y - 0.4)
        f[f"b{k}"] = Line(O, O + p2(W, 0), color=P.aux, stroke_width=1.5)
        f[f"s{k}"] = trace(t, sig, O, W, 0.7, cols[k], 3)
        f[f"l{k}"] = txt(lab[k], O + p2(0, 0.95), cols[k], 20).align_to(O + p2(W, 0), RIGHT)
    for s_ in (0, 5, 10, 15, 20):
        f[f"t{s_}"] = txt(f"{s_} s", p2(-W / 2 + s_ / 20 * W, -2.25), P.muted, 16)
    return f


# ------------------------------------------------------------------ Galvani (schema)
def f08_galvani():
    f = Fig()
    f["mus"] = Ellipse(width=3.2, height=1.1, color=P.S, stroke_width=3, fill_color=P.S, fill_opacity=0.25).move_to(p2(0.4, -0.9))
    f["tend"] = Line(p2(2.0, -0.9), p2(2.8, -0.9), color=P.fg, stroke_width=4)
    f["nerve"] = VMobject(color=P.C, stroke_width=4).set_points_smoothly([p2(-2.6, 1.6), p2(-1.9, 0.9), p2(-1.3, 0.1), p2(-0.7, -0.55)])
    f["arc"] = ArcBetweenPoints(p2(-2.0, 1.05), p2(1.2, -0.45), angle=-1.9, color=P.fg, stroke_width=5)
    f["cu"] = txt(tr("copper", "rame"), p2(-1.2, 2.0), P.fg, 18); f["zn"] = txt(tr("zinc", "zinco"), p2(2.1, 0.8), P.fg, 18)
    f["ln"] = txt(tr("nerve", "nervo"), p2(-2.6, 0.5), P.C, 18)
    f["lm"] = txt(tr("muscle", "muscolo"), p2(0.4, -1.75), P.S, 18)
    return f


# ------------------------------------------------------------------ Berger: alfa a occhi chiusi / aperti
def f11_berger(W=7.5):
    f = Fig()
    t = np.arange(0, 6, 1 / 250)
    rng = np.random.default_rng(3)
    x = 0.6 * pink(len(t), 5)
    a = np.sin(2 * np.pi * 10.2 * t + 0.4) * (1.0 + 0.25 * np.sin(2 * np.pi * 0.4 * t))
    env = np.where(t < 3, 1.0, 0.12 + 0.88 * np.exp(-(t - 3) / 0.15))
    x = x + 2.2 * a * env + 0.5 * np.sin(2 * np.pi * 21 * t) * (t > 3)
    O = p2(-W / 2, 0)
    f["tr"] = trace(t, x, O, W, 0.28, P.V, 2.5)
    f["div"] = DashedLine(O + p2(W / 2, -1.2), O + p2(W / 2, 1.2), color=P.muted, stroke_width=2)
    f["ec"] = txt(tr("eyes closed: alpha ~10 Hz", "occhi chiusi: alfa ~10 Hz"), O + p2(W / 4, 1.4), P.V, 20)
    f["eo"] = txt(tr("eyes open: alpha blocked", "occhi aperti: alfa bloccato"), O + p2(3 * W / 4, 1.4), P.S, 20)
    f["sb"] = VGroup(Line(O + p2(0, -1.3), O + p2(W / 6, -1.3), color=P.fg, stroke_width=3), txt("1 s", O + p2(W / 12, -1.55), P.muted, 16))
    return f


# ------------------------------------------------------------------ ordini di grandezza (scala log)
def f15_magnitudes(W=7.0):
    f = Fig()
    items = [(tr("scalp EEG", "EEG di scalpo"), 50e-6, P.S), (tr("ECoG (cortex surface)", "ECoG (superficie corticale)"), 500e-6, P.C),
             (tr("ECG (heart, on the skin)", "ECG (cuore, sulla pelle)"), 1e-3, "#8E7CC3"), (tr("action potential (inside the cell)", "potenziale d'azione (intracellulare)"), 100e-3, P.V),
             (tr("AA battery", "pila stilo"), 1.5, P.muted)]
    v0, v1 = 1e-6, 10
    for k, (n, v, col) in enumerate(items):
        y = 1.6 - k * 0.8
        L = logpos(v, v0, v1, W - 3.0)
        f[f"b{k}"] = Rectangle(width=max(L, 0.05), height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(p2(-W / 2 + 3.0 + L / 2, y))
        f[f"n{k}"] = txt(n, p2(-W / 2 + 2.85, y), P.fg, 18).align_to(p2(-W / 2 + 2.85, y), RIGHT)
        val = {50e-6: "10–100 µV", 500e-6: "0.1–1 mV", 1e-3: "~1 mV", 100e-3: "~100 mV", 1.5: "1.5 V"}[v]
        f[f"v{k}"] = txt(val, p2(-W / 2 + 3.0 + L + 0.75, y), col, 18)
    f["ax"] = Line(p2(-W / 2 + 3.0, -2.0), p2(W / 2 + 0.3, -2.0), color=P.muted, stroke_width=2)
    for v, s in ((1e-6, "1 µV"), (1e-3, "1 mV"), (1, "1 V")):
        x = -W / 2 + 3.0 + logpos(v, v0, v1, W - 3.0)
        f[f"t{s}"] = VGroup(Line(p2(x, -2.08), p2(x, -1.92), color=P.muted, stroke_width=2), txt(s, p2(x, -2.3), P.muted, 16))
    f["note"] = txt(tr("log scale: each tick = ×1000", "scala log: ogni tacca = ×1000"), p2(1.2, -2.7), P.muted, 16)
    return f


# ------------------------------------------------------------------ analogia idraulica
def f16_water():
    f = Fig()
    # serbatoio alto (potenziale) -> tubo con strozzatura (resistenza) -> serbatoio basso
    f["t1"] = Rectangle(width=1.4, height=2.2, color=P.fg, stroke_width=3).move_to(p2(-3.0, 0.6))
    f["w1"] = Rectangle(width=1.36, height=1.8, stroke_width=0, fill_color=P.V, fill_opacity=0.55).move_to(p2(-3.0, 0.4))
    f["t2"] = Rectangle(width=1.4, height=2.2, color=P.fg, stroke_width=3).move_to(p2(3.0, -0.4))
    f["w2"] = Rectangle(width=1.36, height=0.6, stroke_width=0, fill_color=P.V, fill_opacity=0.55).move_to(p2(3.0, -1.2))
    pipe = [p2(-2.3, -0.3), p2(-0.7, -0.3), p2(-0.4, -0.45), p2(0.4, -0.45), p2(0.7, -0.3), p2(2.3, -0.3)]
    pipe2 = [p + p2(0, -0.5) for p in [p2(-2.3, -0.3), p2(-0.7, -0.3), p2(-0.4, -0.15), p2(0.4, -0.15), p2(0.7, -0.3), p2(2.3, -0.3)]]
    f["p1"] = VMobject(color=P.fg, stroke_width=3).set_points_as_corners(pipe)
    f["p2"] = VMobject(color=P.fg, stroke_width=3).set_points_as_corners(pipe2)
    f["dv"] = DoubleArrow(p2(-4.0, 1.3), p2(-4.0, -1.5), buff=0, color=P.S, stroke_width=4, tip_length=0.18)
    f["V"] = txt(tr("voltage V\n= water pressure", "tensione V\n= pressione"), p2(-5.3, -0.1), P.S, 18)
    f["I"] = txt(tr("current I = flow", "corrente I = portata"), p2(-1.5, -1.3), P.V, 18)
    f["R"] = txt(tr("resistance R\n= narrowing", "resistenza R\n= strozzatura"), p2(0.0, 0.55), P.C, 18)
    f["ohm"] = MathTex(r"V = R\,I", color=P.fg).scale(1.1).move_to(p2(2.6, 1.4))
    return f


# ------------------------------------------------------------------ differenza di potenziale: attivo - riferimento
def f17_diff():
    f = Fig()
    c = p2(-1.6, 0); R = 1.6
    f["head"] = head(c, R)
    a = c + el2d("C3", R); r_ = c + p2(1.04 * R, -0.35)   # riferimento sul mastoide/orecchio
    f["ea"] = Circle(radius=0.11, color=P.S, fill_color=P.S, fill_opacity=1).move_to(a)
    f["er"] = Circle(radius=0.11, color=P.muted, fill_color=P.muted, fill_opacity=1).move_to(r_)
    f["la"] = txt(tr("active", "attivo"), a + p2(-0.2, -0.35), P.S, 18)
    f["lr"] = txt(tr("reference", "riferimento"), r_ + p2(0.9, -0.45), P.muted, 18)
    amp = p2(2.6, 0.2)
    f["amp"] = Polygon(amp + p2(-0.5, 0.55), amp + p2(-0.5, -0.55), amp + p2(0.45, 0), color=P.fg, stroke_width=3)
    f["pl"] = txt("+", amp + p2(-0.35, 0.25), P.fg, 20); f["mi"] = txt("−", amp + p2(-0.35, -0.25), P.fg, 20)
    f["wa"] = VMobject(color=P.S, stroke_width=2.5).set_points_as_corners([a, a + p2(0.3, 1.3), p2(1.4, 1.3), p2(1.4, 0.45), amp + p2(-0.5, 0.25)])
    f["wr"] = VMobject(color=P.muted, stroke_width=2.5).set_points_as_corners([r_, p2(1.2, -0.35 + 0), p2(1.2, -0.05), amp + p2(-0.5, -0.25)])
    f["out"] = Arrow(amp + p2(0.45, 0), amp + p2(1.3, 0), buff=0, color=P.fg, stroke_width=3, tip_length=0.16)
    f["eq"] = MathTex(tr(r"V(t) = \varphi_{\mathrm{active}}(t) - \varphi_{\mathrm{ref}}(t)", r"V(t) = \varphi_{\mathrm{attivo}}(t) - \varphi_{\mathrm{rif}}(t)"), color=P.fg).scale(0.8).move_to(p2(2.2, -1.6))
    return f


# ------------------------------------------------------------------ spike vs PSP: somma temporale
def spikes_vs_psp(n=40, dur=0.4, fs=4000, seed=1, jitter=0.12):
    """n neuroni con un evento ciascuno a tempi casuali (jitter s): somma di spike (1 ms) vs PSP (~20 ms)."""
    rng = np.random.default_rng(seed)
    t = np.arange(0, dur, 1 / fs)
    t0 = 0.15 + rng.normal(0, jitter / 3, n)
    sp = np.zeros((n, len(t))); ps = np.zeros((n, len(t)))
    for i, c in enumerate(t0):
        u = t - c
        sp[i] = np.where(np.abs(u) < 0.002, np.sin(np.pi * (u + 0.002) / 0.002) * np.exp(-np.abs(u) / 0.0006), 0)   # bifasico ~1 ms
        ps[i] = np.where(u > 0, (np.exp(-u / 0.020) - np.exp(-u / 0.004)), 0)
    return t, sp, ps


def f18_summation(W=6.0):
    f = Fig()
    t, sp, ps = spikes_vs_psp(12)
    for k in range(5):
        f[f"s{k}"] = trace(t, sp[k], p2(-W - 0.4, 1.5 - 0.42 * k), W, 0.3, P.S, 2.5)
        f[f"p{k}"] = trace(t, ps[k] / ps.max(), p2(0.6, 1.5 - 0.42 * k), W, 0.3, P.V, 2)
    ssum = sp.sum(0); psum = ps.sum(0)
    f["ss"] = trace(t, ssum / np.abs(psum).max() * 6, p2(-W - 0.4, -1.6), W, 0.25, P.S, 3)
    f["ps"] = trace(t, psum / np.abs(psum).max() * 6, p2(0.6, -1.6), W, 0.25, P.V, 3)
    f["ts"] = txt(tr("action potentials (~1 ms)", "potenziali d'azione (~1 ms)"), p2(-W / 2 - 0.4, 2.2), P.S, 20)
    f["tp"] = txt(tr("postsynaptic potentials (10–100 ms)", "potenziali postsinaptici (10–100 ms)"), p2(W / 2 + 0.6, 2.2), P.V, 20)
    f["sig"] = txt("Σ", p2(-W - 0.8, -1.6), P.fg, 30); f["sig2"] = txt("Σ", p2(0.2, -1.6), P.fg, 30)
    return f


def f19_sync(W=6.0):
    """N sorgenti sincrone vs asincrone: ampiezza ∝ N vs ∝ √N."""
    f = Fig()
    Ns = np.array([1, 10, 100, 1000, 10000])
    O = p2(-W / 2, -1.6)
    f["ax"] = axes(O, W, 3.4, tr("number of neurons N", "numero di neuroni N"), tr("summed amplitude", "ampiezza somma"))
    xs = [logpos(n, 1, 1e4, W - 0.4) for n in Ns]
    ys = lambda v: logpos(v, 1, 1e4, 3.0)
    f["sync"] = VMobject(color=P.S, stroke_width=4).set_points_as_corners([O + p2(x, ys(n)) for x, n in zip(xs, Ns)])
    f["asy"] = VMobject(color=P.V, stroke_width=4).set_points_as_corners([O + p2(x, ys(np.sqrt(n))) for x, n in zip(xs, Ns)])
    f["ls"] = txt(tr("synchronous ∝ N", "sincroni ∝ N"), O + p2(W - 1.3, 3.25), P.S, 20)
    f["la"] = txt(tr("asynchronous ∝ √N", "asincroni ∝ √N"), O + p2(W - 1.3, 0.8), P.V, 20)
    for x, n in zip(xs, Ns):
        f[f"t{n}"] = txt(f"{n:,}".replace(",", " "), O + p2(x, -0.25), P.muted, 15)
    return f


# ------------------------------------------------------------------ campo aperto vs chiuso
def f20_fields():
    f = Fig()
    for k in range(5):
        f[f"p{k}"] = pyramidal(p2(-4.3 + 0.55 * k, -0.6), 0.55)
    f["st"] = stellate(p2(2.6, 0.0), 1.2, n=9)
    f["lo"] = txt(tr("open field: aligned pyramidal cells\n→ dipoles add up", "campo aperto: piramidali allineate\n→ i dipoli si sommano"), p2(-3.2, -1.9), P.S, 18)
    f["lc"] = txt(tr("closed field: radial dendrites\n→ fields cancel out", "campo chiuso: dendriti radiali\n→ i campi si annullano"), p2(2.6, -1.9), P.V, 18)
    f["ar"] = VGroup(*[Arrow(p2(-4.3 + 0.55 * k, -0.3), p2(-4.3 + 0.55 * k, 0.6), buff=0, color=P.S, stroke_width=4, tip_length=0.15) for k in range(5)])
    return f


# ------------------------------------------------------------------ giro e solco: dipoli radiali e tangenziali
def f21_gyrus(W=7.0):
    f = Fig()
    xs = np.linspace(-W / 2, W / 2, 300)
    surf = lambda x: 0.9 * np.cos(2 * np.pi * x / 3.2)
    f["skull"] = Line(p2(-W / 2, 1.9), p2(W / 2, 1.9), color=P.muted, stroke_width=8)
    f["sk"] = txt(tr("skull / scalp", "cranio / scalpo"), p2(W / 2 - 1.0, 2.25), P.muted, 16)
    f["cx"] = VMobject(color=P.fg, stroke_width=3).set_points_smoothly([p2(x, surf(x)) for x in xs])
    # dipoli perpendicolari alla superficie corticale
    for k, x in enumerate(np.linspace(-W / 2 + 0.3, W / 2 - 0.3, 13)):
        y = surf(x); dy = -0.9 * 2 * np.pi / 3.2 * np.sin(2 * np.pi * x / 3.2)
        n = np.array([-dy, 1.0, 0]); n /= np.linalg.norm(n)
        radial = abs(n[0]) < 0.35
        col = P.S if radial else P.V
        f[f"d{k}"] = Arrow(p2(x, y) - 0.65 * n, p2(x, y) - 0.05 * n, buff=0, color=col, stroke_width=5, tip_length=0.15)
    f["lr"] = txt(tr("radial (gyral crown): seen well by EEG", "radiali (cresta del giro): ben visti dall'EEG"), p2(0, -2.15), P.S, 18)
    f["lt"] = txt(tr("tangential (sulcal wall): weaker in EEG, strong in MEG", "tangenziali (parete del solco): deboli in EEG, forti in MEG"), p2(0, -2.6), P.V, 18)
    return f


# ------------------------------------------------------------------ problema diretto / inverso
def f23_fwdinv():
    f = Fig()
    f["h1"] = head(p2(-3.4, 0), 1.2)
    f["d1"] = Arrow(p2(-3.5, -0.3), p2(-3.3, 0.45), buff=0, color=P.S, stroke_width=6, tip_length=0.18)
    V, m = dipole_map([0.05, 0.1, 0.55], [0.3, 0.2, 1.0], blur=0.2)
    f["img"], f["out"] = topomap(V, m, p2(3.4, 0), 1.2)
    f["fw"] = Arrow(p2(-1.8, 0.45), p2(1.8, 0.45), buff=0, color=P.V, stroke_width=4, tip_length=0.2)
    f["iv"] = Arrow(p2(1.8, -0.45), p2(-1.8, -0.45), buff=0, color=P.C, stroke_width=4, tip_length=0.2)
    f["lf"] = txt(tr("forward problem: unique solution", "problema diretto: soluzione unica"), p2(0, 0.85), P.V, 18)
    f["li"] = txt(tr("inverse problem: infinitely many solutions", "problema inverso: infinite soluzioni"), p2(0, -0.85), P.C, 18)
    return f


# ------------------------------------------------------------------ canali -> topografie
def multichannel(n=8, dur=2.0, seed=10):
    t = np.arange(0, dur, 1 / 250)
    rng = np.random.default_rng(seed)
    # due sorgenti comuni (alfa occipitale, lento frontale) + rumore
    s1 = burst(t, 10, 1.0, seed, n_bursts=3); s2 = burst(t, 3, 1.0, seed + 1, n_bursts=2, dur=(1, 2))
    X = []
    for k, nm in enumerate(NAMES):
        e = el3d(nm)
        w1 = max(0, -e[1]) ** 1.5; w2 = max(0, e[1]) ** 1.5
        X.append(2.2 * w1 * s1 + 1.8 * w2 * s2 + 0.18 * pink(len(t), seed + 10 + k))
    return t, np.array(X)


def f24_channels(W=5.4):
    f = Fig()
    t, X = multichannel()
    show = ["Fp1", "Fz", "C3", "Cz", "P3", "Pz", "O1", "O2"]
    for k, nm in enumerate(show):
        i = NAMES.index(nm)
        y = 2.0 - 0.55 * k
        f[f"n{k}"] = txt(nm, p2(-W - 1.0, y), P.muted, 16)
        f[f"x{k}"] = trace(t, X[i], p2(-W - 0.6, y), W, 0.18, P.V, 1.8)
    for j, tt in enumerate((0.4, 0.9, 1.4)):
        x = -W - 0.6 + tt / t[-1] * W
        f[f"cur{j}"] = DashedLine(p2(x, 2.3), p2(x, -2.0), color=P.S, stroke_width=2)
        i0 = int(tt * 250)
        V, m = interp_map(X[:, i0])
        img, out = topomap(V, m, p2(1.2 + 1.5 * j, 0.1), 0.65)
        f[f"m{j}"] = img; f[f"o{j}"] = out
        f[f"mt{j}"] = txt(f"t = {int(tt * 1000)} ms", p2(1.2 + 1.5 * j, -0.85), P.muted, 15)
    return f


# ------------------------------------------------------------------ ritmi
BANDS = [("δ delta", 2.0, "0.5–4 Hz", tr("deep sleep", "sonno profondo")),
         ("θ theta", 6.0, "4–8 Hz", tr("drowsiness, memory", "sonnolenza, memoria")),
         ("α alpha", 10.0, "8–13 Hz", tr("relaxed wake, eyes closed", "veglia rilassata, occhi chiusi")),
         ("β beta", 20.0, "13–30 Hz", tr("active thinking, motor", "attività mentale, motoria")),
         ("γ gamma", 40.0, "30–80 Hz", tr("local processing, binding", "elaborazione locale"))]
BCOL = ["#8E7CC3", None, None, None, None]


def f26_rhythms(W=6.0):
    f = Fig()
    t = np.arange(0, 1.0, 1 / 1000)
    cols = ["#8E7CC3", P.V, P.S, P.C, "#6FCF97"]
    for k, (n, fr, rg, st) in enumerate(BANDS):
        y = 2.0 - 1.0 * k
        f[f"n{k}"] = txt(n, p2(-W / 2 - 1.2, y + 0.12), cols[k], 22, weight="BOLD")
        f[f"r{k}"] = txt(rg, p2(-W / 2 - 1.2, y - 0.22), P.muted, 16)
        amp = [1.0, 0.8, 0.7, 0.35, 0.2][k]
        x = amp * np.sin(2 * np.pi * fr * t)
        f[f"x{k}"] = trace(t, x, p2(-W / 2 + 0.2, y), W, 0.38, cols[k], 2.5)
        f[f"s{k}"] = txt(st, p2(W / 2 + 1.9, y), P.fg, 17)
    f["sb"] = VGroup(Line(p2(-W / 2 + 0.2, -2.55), p2(-W / 2 + 0.2 + W * 0.25, -2.55), color=P.fg, stroke_width=3), txt("250 ms", p2(-W / 2 + 0.2 + W * 0.125, -2.8), P.muted, 15))
    return f
