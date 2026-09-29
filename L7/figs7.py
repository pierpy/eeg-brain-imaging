"""Figure della Lezione 7 EEG: potenziali evento-correlati (dati SIMULATI)."""
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

P = F.P
PURP = "#8E7CC3"; GRN = "#6FCF97"
FS7 = 250
TE = np.arange(-0.2, 0.8, 1 / FS7)


def dec(v, n=2):
    s = f"{v:.{n}f}"
    return s if LANG == "en" else s.replace(".", ",")


def g(t, mu, sd, a):
    return a * np.exp(-0.5 * ((t - mu) / sd) ** 2)


COMPS = {"P1": (0.10, 0.02, 3.0), "N1": (0.17, 0.03, -5.0), "P2": (0.23, 0.03, 3.5), "N2": (0.28, 0.035, -3.0), "P3": (0.38, 0.09, 9.0)}


def erp(t=TE, scale=None, shift=0.0):
    scale = scale or {}
    return sum(g(t, mu + shift, sd, a * scale.get(k, 1.0)) for k, (mu, sd, a) in COMPS.items())


def noise_trials(n, t=TE, seed=0, uv=12.0):
    return np.array([periodic_eeg(len(t) / FS7, FS7, seed=seed + i, peaks=((10, 1, 0.8),), uv=uv)[1][:len(t)] for i in range(n)])


def wave_axes(O, W, H, t0=-0.2, t1=0.8, col=None, neg_up=False, ticks=(0, 200, 400, 600), sz=13):
    col = col or P.fg
    X = lambda tt: O + p2((tt - t0) / (t1 - t0) * W, 0)
    gr = VGroup(Line(X(t0), X(t1), color=col, stroke_width=1.5), Line(X(0) + p2(0, -H / 2), X(0) + p2(0, H / 2), color=col, stroke_width=1.5))
    for ms in ticks:
        gr.add(Line(X(ms / 1000), X(ms / 1000) + p2(0, -0.08), color=col, stroke_width=1.5), txt(f"{ms}", X(ms / 1000) + p2(0, -0.28), P.muted, sz))
    gr.add(txt("ms", X(t1) + p2(0.25, -0.28), P.muted, sz))
    return gr


def wave(t, x, O, W, h, col, sw=3, t0=-0.2, t1=0.8):
    m = (t >= t0) & (t <= t1)
    return VMobject(color=col, stroke_width=sw).set_points_as_corners([O + p2((a - t0) / (t1 - t0) * W, h * b) for a, b in zip(t[m], x[m])])


# ------------------------------------------------------------------ 3: la media fa emergere l'ERP
def f03_averaging(W=4.0):
    f = Fig()
    X = erp()[None, :] + noise_trials(64)
    for i in range(4):
        f[f"t{i}"] = wave(TE, X[i], p2(-6.0, 1.9 - 0.6 * i), W, 0.018, P.muted, 1.3)
    f["lt"] = txt(tr("single trials", "singoli trial"), p2(-4.0, 2.45), P.fg, 16, weight="BOLD")
    for k, n in enumerate((4, 16, 64)):
        O = p2(-0.4 + 0.0 * k, 1.6 - 1.35 * k)
        f[f"a{k}"] = wave(TE, X[:n].mean(0), O, W, 0.06, P.S, 2.5)
        f[f"x{k}"] = Line(O, O + p2(W, 0), color=P.aux, stroke_width=1)
        f[f"l{k}"] = txt(f"N = {n}", O + p2(W + 0.6, 0), P.S, 16, weight="BOLD")
    f["la"] = txt(tr("average", "media"), p2(1.6, 2.45), P.fg, 16, weight="BOLD")
    f["ar"] = Arrow(p2(-1.8, 0.8), p2(-0.7, 0.8), buff=0, color=P.fg, stroke_width=4, tip_length=0.18)
    return f


# ------------------------------------------------------------------ 5: jitter di latenza
def f05_jitter(W=4.4):
    f = Fig()
    rng = np.random.default_rng(3)
    for k, sd in enumerate((0.0, 0.06)):
        x0 = -5.6 + 5.8 * k
        lat = rng.normal(0, sd, 40)
        tr_ = np.array([g(TE, 0.35 + d, 0.05, 8.0) for d in lat])
        for i in range(8):
            f[f"s{k}{i}"] = wave(TE, tr_[i], p2(x0, 1.8 - 0.28 * i), W, 0.03, P.muted, 1.2)
        f[f"a{k}"] = wave(TE, tr_.mean(0), p2(x0, -1.9), W, 0.13, P.V if k == 0 else P.S, 3)
        f[f"z{k}"] = Line(p2(x0, -1.9), p2(x0 + W, -1.9), color=P.aux, stroke_width=1)
        f[f"l{k}"] = txt(tr("no jitter", "nessun jitter") if k == 0 else tr("latency jitter ±60 ms", "jitter di latenza ±60 ms"), p2(x0 + W / 2, 2.35), P.fg, 16, weight="BOLD")
        f[f"m{k}"] = txt(tr("average", "media"), p2(x0 - 0.7, -1.5), P.muted, 14)
    return f


# ------------------------------------------------------------------ 6: rapporto segnale/rumore
def f06_snr(W=5.0, Hh=2.6):
    f = Fig()
    O = p2(-W / 2, -1.4)
    f["ax"] = axes(O, W + 0.2, Hh + 0.3, tr("number of trials N", "numero di trial N"), tr("residual noise (µV)", "rumore residuo (µV)"))
    n = np.arange(1, 201)
    y = 12 / np.sqrt(n)
    f["c"] = VMobject(color=P.S, stroke_width=4).set_points_smoothly([O + p2(a / 200 * W, b / 12 * Hh) for a, b in zip(n, y)])
    for v in (1, 25, 50, 100, 200):
        f[f"x{v}"] = txt(str(v), O + p2(v / 200 * W, -0.25), P.muted, 13)
    for v in (30, 100):
        f[f"d{v}"] = DashedLine(O + p2(v / 200 * W, 0), O + p2(v / 200 * W, 12 / np.sqrt(v) / 12 * Hh), color=P.V, stroke_width=1.5)
        f[f"t{v}"] = txt(f"N={v}: {dec(12 / np.sqrt(v), 1)} µV", O + p2(v / 200 * W + 0.9, 12 / np.sqrt(v) / 12 * Hh + 0.3), P.V, 14)
    f["f"] = MathTex(r"\sigma_{\bar{x}} = \frac{\sigma}{\sqrt{N}}", color=P.fg).scale(0.9).move_to(O + p2(W * 0.75, Hh * 0.8))
    return f


# ------------------------------------------------------------------ 7: picchi ≠ componenti
def f07_components(W=5.0):
    f = Fig()
    t = TE
    c1 = g(t, 0.30, 0.05, 5.0); c2 = g(t, 0.43, 0.08, 4.0); c3 = g(t, 0.22, 0.04, -5.0)
    for k, (scale, lab) in enumerate(((1.0, tr("condition A", "condizione A")), (2.0, tr("condition B: only C2 larger", "condizione B: solo C2 più grande")))):
        x0 = -5.8 + 6.0 * k
        O = p2(x0, 0.9)
        comps = [(c1, P.V), (c2 * scale, P.S), (c3, PURP)]
        for j, (c, col) in enumerate(comps):
            f[f"c{k}{j}"] = wave(t, c, p2(x0, -1.3), W, 0.12, col, 2)
        s = c1 + c2 * scale + c3
        f[f"s{k}"] = wave(t, s, O, W, 0.12, P.fg, 3.5)
        pk = t[np.argmax(s)]
        f[f"p{k}"] = DashedLine(O + p2((pk + 0.2) / 1.0 * W, 0), O + p2((pk + 0.2) / 1.0 * W, 0.12 * s.max()), color=P.S, stroke_width=1.5)
        f[f"pl{k}"] = txt(tr(f"peak {int(pk * 1000)} ms", f"picco {int(pk * 1000)} ms"), O + p2((pk + 0.2) / 1.0 * W + 0.8, 0.12 * s.max() + 0.25), P.S, 14)
        f[f"l{k}"] = txt(lab, O + p2(W / 2, 2.7), P.fg, 16, weight="BOLD")
        f[f"z{k}"] = Line(O, O + p2(W, 0), color=P.aux, stroke_width=1)
    f["lc"] = txt(tr("latent components C1, C2, C3", "componenti latenti C1, C2, C3"), p2(0, -2.3), P.muted, 15)
    return f


# ------------------------------------------------------------------ 9: lo zoo delle componenti
ZOO = [(0.10, "P1", 1), (0.17, "N1", -1), (0.17, "N170", -1), (0.20, "MMN", -1), (0.25, "N2pc", -1), (0.35, "P3", 1), (0.40, "N400", -1), (0.60, "P600", 1), (0.08, "ERN", -1)]


def f09_zoo(W=11.0, h=0.2):
    f = Fig()
    t = np.arange(-0.2, 0.9, 1 / FS7)
    x = erp(t) + g(t, 0.60, 0.08, 2.5) + g(t, 0.42, 0.06, -2.0)
    O = p2(-W / 2, 0)
    X = lambda tt: O + p2((tt + 0.2) / 1.1 * W, 0)
    f["ax"] = VGroup(Line(X(-0.2), X(0.9), color=P.fg, stroke_width=1.5), Line(X(0) + p2(0, -1.4), X(0) + p2(0, 2.0), color=P.fg, stroke_width=1.5))
    for ms in (0, 200, 400, 600, 800):
        f[f"t{ms}"] = txt(str(ms), X(ms / 1000) + p2(0, -0.28), P.muted, 13)
    f["w"] = VMobject(color=P.V, stroke_width=3.5).set_points_as_corners([X(a) + p2(0, h * b) for a, b in zip(t, x)])
    labs = [(0.10, "P1", tr("visual sensory", "sensoriale visiva"), 1), (0.17, "N1 / N170", tr("attention / faces", "attenzione / volti"), -1),
            (0.22, "MMN", tr("auditory deviance", "devianza uditiva"), -2), (0.28, "N2 / N2pc", tr("conflict / spatial attention", "conflitto / attenzione spaziale"), -3),
            (0.38, "P3", tr("context update", "aggiornamento del contesto"), 2), (0.45, "N400", tr("semantic expectancy", "attesa semantica"), -1),
            (0.62, "P600", tr("syntactic reanalysis", "rianalisi sintattica"), 1)]
    for k, (tt, n, d, lv) in enumerate(labs):
        y = h * np.interp(tt, t, x)
        up = lv > 0
        yl = (1.3 + 0.7 * (lv - 1)) if up else (-0.9 - 0.7 * (-lv - 1))
        f[f"k{k}"] = VGroup(Line(X(tt) + p2(0, y), X(tt) + p2(0, yl - (0.15 if up else -0.15)), color=P.muted, stroke_width=1),
                           txt(n, X(tt) + p2(0, yl + (0.1 if up else -0.05)), P.S, 15, weight="BOLD"), txt(d, X(tt) + p2(0, yl + (-0.18 if up else -0.33)), P.muted, 12))
    return f


# ------------------------------------------------------------------ 11: oddball e P300
def oddball_erps(t=TE):
    std = erp(t, {"P3": 0.15, "N2": 0.5})
    dev = erp(t, {"P3": 1.1, "N2": 1.3})
    return std, dev


def f11_oddball(W=5.0):
    f = Fig()
    # sequenza di stimoli
    seq = "SSSSDSSSSSDSSSDSSS"
    for i, c in enumerate(seq):
        f[f"q{i}"] = Rectangle(width=0.28, height=0.28, stroke_width=0, fill_color=P.S if c == "D" else P.aux, fill_opacity=1).move_to(p2(-6.0 + 0.36 * i, 2.1))
    f["ql"] = txt(tr("80 % standard · 20 % rare target", "80 % standard · 20 % target raro"), p2(-2.9, 1.6), P.muted, 15)
    std, dev = oddball_erps()
    O = p2(-W / 2 + 1.0, -1.2)
    f["ax"] = wave_axes(O, W, 3.0)
    f["s"] = wave(TE, std, O, W, 0.18, P.V, 3)
    f["d"] = wave(TE, dev, O, W, 0.18, P.S, 3.5)
    f["ls"] = txt("standard", O + p2(W + 0.8, 0.35), P.V, 15, weight="BOLD")
    f["ld"] = txt(tr("rare target", "target raro"), O + p2(W * 0.62, 0.18 * dev.max() + 0.3), P.S, 15, weight="BOLD")
    f["p3"] = txt("P3 (Pz)", O + p2((0.38 + 0.2) * W - 0.9, 0.18 * dev.max() - 0.1), P.S, 16, weight="BOLD")
    return f


# ------------------------------------------------------------------ 12: N400
def f12_n400(W=5.2):
    f = Fig()
    t = TE
    base = erp(t, {"P3": 0.35})
    inc = base + g(t, 0.40, 0.08, -6.0)
    O = p2(-W / 2, -0.9)
    f["ax"] = wave_axes(O, W, 3.0)
    f["c"] = wave(t, base, O, W, 0.2, P.V, 3)
    f["i"] = wave(t, inc, O, W, 0.2, P.S, 3.5)
    f["s1"] = txt(tr("\"I take my coffee with cream and sugar\"", "\"Prendo il caffè con latte e zucchero\""), p2(0, 2.3), P.V, 16)
    f["s2"] = txt(tr("\"I take my coffee with cream and socks\"", "\"Prendo il caffè con latte e calzini\""), p2(0, 1.85), P.S, 16)
    f["n4"] = txt("N400", O + p2((0.40 + 0.2) * W + 0.6, 0.2 * inc.min()), P.S, 16, weight="BOLD")
    f["neg"] = txt(tr("(negative plotted down)", "(negativo in basso)"), O + p2(W - 0.8, -1.55), P.muted, 12)
    return f


# ------------------------------------------------------------------ 14: N2pc
def f14_n2pc(W=4.4):
    f = Fig()
    c = p2(-4.3, 0.2); R = 1.4
    f["head"] = head(c, R)
    for n, col in (("P7", P.V), ("P8", P.S)):
        f["e" + n] = VGroup(Circle(radius=0.2, color=col, stroke_width=3, fill_color=P.bg, fill_opacity=1).move_to(c + el2d(n, R)), txt(n, c + el2d(n, R), P.fg, 12, weight="BOLD"))
    # display
    d = p2(-4.3, 2.75)
    f["fix"] = txt("+", d, P.fg, 20)
    f["tg"] = Circle(radius=0.14, color=P.S, fill_color=P.S, fill_opacity=1).move_to(d + p2(-0.7, 0))
    f["dis"] = Circle(radius=0.14, color=P.aux, fill_color=P.aux, fill_opacity=1).move_to(d + p2(0.7, 0))
    f["dl"] = txt(tr("target in the LEFT visual field", "target nel campo visivo SINISTRO"), d + p2(0, -0.45), P.muted, 13)
    t = TE
    ipsi = erp(t, {"P3": 0.4}); contra = ipsi + g(t, 0.25, 0.045, -2.5)
    O = p2(-1.2, 0.6)
    f["ax"] = wave_axes(O, W, 2.4)
    f["ip"] = wave(t, ipsi, O, W, 0.13, P.V, 2.5)
    f["co"] = wave(t, contra, O, W, 0.13, P.S, 3)
    f["li"] = txt(tr("ipsilateral (P7)", "ipsilaterale (P7)"), O + p2(W + 1.0, 0.6), P.V, 14, weight="BOLD")
    f["lc"] = txt(tr("contralateral (P8)", "controlaterale (P8)"), O + p2(W + 1.1, 0.2), P.S, 14, weight="BOLD")
    O2 = p2(-1.2, -1.9)
    f["ax2"] = wave_axes(O2, W, 1.6)
    f["df"] = wave(t, contra - ipsi, O2, W, 0.2, P.S, 3.5)
    f["ld"] = txt(tr("contra − ipsi = N2pc", "contro − ipsi = N2pc"), O2 + p2(W + 1.5, 0.3), P.S, 15, weight="BOLD")
    return f


# ------------------------------------------------------------------ 16: misure
def f16_measures(W=6.0):
    f = Fig()
    t = np.arange(-0.2, 0.8, 1 / 1000)
    x = erp(t, {"P3": 1.0})
    O = p2(-W / 2, -1.2)
    X = lambda tt, y=0: O + p2((tt + 0.2) / 1.0 * W, 0.22 * y)
    f["ax"] = wave_axes(O, W, 3.2)
    m = (t >= 0.30) & (t <= 0.50)
    f["area"] = Polygon(*([X(a, b) for a, b in zip(t[m], x[m])] + [X(0.50), X(0.30)]), stroke_width=0, fill_color=P.V, fill_opacity=0.3)
    f["w"] = VMobject(color=P.fg, stroke_width=3).set_points_as_corners([X(a, b) for a, b in zip(t, x)])
    ip = np.argmax(x * m)
    f["pk"] = VGroup(Dot(X(t[ip], x[ip]), radius=0.08, color=P.S), txt(tr("peak amplitude / latency", "ampiezza / latenza di picco"), X(t[ip], x[ip]) + p2(1.7, 0.2), P.S, 14, weight="BOLD"))
    cs = np.cumsum(np.clip(x * m, 0, None)); i50 = np.searchsorted(cs, cs[-1] / 2)
    f["fa"] = VGroup(DashedLine(X(t[i50]), X(t[i50], x[i50]), color=PURP, stroke_width=2.5), txt(tr("50 % area latency", "latenza al 50 % dell'area"), X(t[i50]) + p2(0.2, -0.45), PURP, 14, weight="BOLD"))
    f["mw"] = txt(tr("mean amplitude 300–500 ms", "ampiezza media 300–500 ms"), X(0.62, 5.5) + p2(1.2, 0), P.V, 14, weight="BOLD")
    return f


# ------------------------------------------------------------------ 17: onde differenza e topografie
def f17_diffwave(W=4.6, R=1.1):
    f = Fig()
    std, dev = oddball_erps()
    O = p2(-6.0, 0.5)
    f["ax"] = wave_axes(O, W, 2.6)
    f["s"] = wave(TE, std, O, W, 0.13, P.V, 2.5)
    f["d"] = wave(TE, dev, O, W, 0.13, P.S, 2.5)
    O2 = p2(-6.0, -1.8)
    f["ax2"] = wave_axes(O2, W, 1.8)
    f["df"] = wave(TE, dev - std, O2, W, 0.13, P.fg, 3.5)
    f["l1"] = txt(tr("rare / standard", "raro / standard"), O + p2(W / 2, 1.6), P.fg, 15, weight="BOLD")
    f["l2"] = txt(tr("difference wave", "onda differenza"), O2 + p2(W / 2, 1.2), P.fg, 15, weight="BOLD")
    for k, (tt, lab) in enumerate(((0.17, "170 ms"), (0.38, "380 ms"))):
        c = p2(1.4 + 2.8 * k, 0.2)
        pos = [0, 0.1, 0.7] if k == 0 else [0, -0.45, 0.55]
        mom = [0, 0.8, -0.6] if k == 0 else [0, -0.3, 1.0]
        V, m = dipole_map(pos, mom, n=141, blur=0.2)
        f[f"m{k}"], f[f"o{k}"] = topomap(V, m, c, R)
        f[f"t{k}"] = txt(lab, c + p2(0, -R - 0.35), P.fg, 16, weight="BOLD")
    return f


# ------------------------------------------------------------------ 20: permutazioni a cluster
def cluster_data(seed=5):
    rng = np.random.default_rng(seed)
    t = np.arange(-0.2, 0.8, 1 / 100)
    eff = g(t, 0.38, 0.07, 3.2) + g(t, 0.17, 0.02, 1.6)
    tv = eff + np.convolve(rng.normal(size=len(t)), np.ones(5) / 2.2, "same") * 0.6
    return t, tv


def f20_cluster(W=6.0, Hh=2.6):
    f = Fig()
    t, tv = cluster_data()
    O = p2(-6.2, -0.6)
    X = lambda tt, y: O + p2((tt + 0.2) / 1.0 * W, y / 4.0 * Hh / 2)
    f["ax"] = wave_axes(O, W, Hh + 0.6)
    thr = 2.1
    f["th"] = DashedLine(X(-0.2, thr), X(0.8, thr), color=P.muted, stroke_width=1.5)
    f["tt"] = txt("t = 2.1 (p < .05)", X(0.8, thr) + p2(0.2, 0.25), P.muted, 13)
    above = tv > thr
    k = 0; i = 0; masses = []
    while i < len(t):
        if above[i]:
            j = i
            while j < len(t) and above[j]: j += 1
            pts = [X(a, b) for a, b in zip(t[i:j], tv[i:j])] + [X(t[j - 1], thr), X(t[i], thr)]
            f[f"cl{k}"] = Polygon(*pts, stroke_width=0, fill_color=P.S, fill_opacity=0.45)
            masses.append(tv[i:j].sum())
            f[f"cs{k}"] = txt(f"Σt = {dec(tv[i:j].sum(), 1)}", X((t[i] + t[j - 1]) / 2, tv[i:j].max()) + p2(0, 0.3), P.S, 14, weight="BOLD")
            k += 1; i = j
        else:
            i += 1
    f["w"] = VMobject(color=P.fg, stroke_width=3).set_points_as_corners([X(a, b) for a, b in zip(t, tv)])
    f["yl"] = txt(tr("t value", "valore t"), O + p2(0.45, Hh / 2 + 0.3), P.muted, 14)
    # distribuzione nulla
    rng = np.random.default_rng(1)
    null = np.abs(rng.gumbel(8, 3.5, 2000))
    h, e = np.histogram(null, 30, range=(0, 40))
    Ob = p2(1.4, -1.4); wb = 4.4 / 30
    f["hb"] = VGroup(*[Rectangle(width=wb * 0.9, height=v / h.max() * 2.2, stroke_width=0, fill_color=P.aux, fill_opacity=0.9).move_to(Ob + p2(wb * (i + 0.5), 0), aligned_edge=DOWN) for i, v in enumerate(h)])
    f["hax"] = Line(Ob, Ob + p2(4.5, 0), color=P.fg, stroke_width=1.5)
    f["hl"] = txt(tr("max cluster mass under permutation", "massa max dei cluster sotto permutazione"), Ob + p2(2.2, 2.55), P.fg, 14)
    q95 = np.quantile(null, 0.95)
    f["q"] = DashedLine(Ob + p2(q95 / 40 * 4.4, 0), Ob + p2(q95 / 40 * 4.4, 2.3), color=P.muted, stroke_width=1.5)
    xo = min(max(masses), 39) / 40 * 4.4
    f["obs"] = VGroup(Arrow(Ob + p2(xo, 1.4), Ob + p2(xo, 0.05), buff=0, color=P.S, stroke_width=5, tip_length=0.18), txt(tr("observed", "osservata"), Ob + p2(xo, 1.65), P.S, 14, weight="BOLD"))
    return f
