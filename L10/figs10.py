"""Figure della Lezione 10 EEG: decoding / MVPA e applicazioni (dati SIMULATI)."""
import os as _os
_R = _os.environ.get("COURSE_ROOT") or _os.path.dirname(_os.path.abspath(__file__))
while not _os.path.exists(_os.path.join(_R, ".course_root")) and _os.path.dirname(_R) != _R:
    _R = _os.path.dirname(_R)
import sys
sys.path.insert(0, _R + "/common")
import numpy as np
from eegfigs import *
from manim import (VGroup, VMobject, Arrow, Line, DashedLine, Dot, Circle, Polygon, Rectangle,
                   RoundedRectangle, MathTex, ORIGIN, UP, DOWN, LEFT, RIGHT, PI, ImageMobject)

P = F.P
PURP = "#8E7CC3"; GRN = "#6FCF97"


def dec(v, n=2):
    s = f"{v:.{n}f}"
    return s if LANG == "en" else s.replace(".", ",")


def box(c, w, h, lab, col, sz=16):
    return VGroup(RoundedRectangle(corner_radius=0.15, width=w, height=h, color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.18).move_to(c),
                  txt(lab, c, P.fg, sz))


# ------------------------------------------------------------------ dati simulati: due classi, pattern spaziale che evolve nel tempo
NCH = 19
TD = np.arange(-0.2, 0.8, 0.01)


def patterns():
    E_ = np.array([el3d(n) for n in NAMES])
    a1 = dipole_pot(E_, np.array([0.0, -0.5, 0.5]), np.array([0, -0.4, 1.0]))           # parieto-occipitale (precoce)
    a2 = dipole_pot(E_, np.array([0.2, 0.1, 0.55]), np.array([0.5, 0.2, 0.9]))           # centrale (tardivo)
    return a1 / np.abs(a1).max(), a2 / np.abs(a2).max()


def sim_trials(n=200, seed=0, snr=0.6):
    """X: trial × canali × tempo; y ∈ {0,1}. Effetto precoce (a1, 150–250 ms) e tardivo (a2, 350–600 ms)."""
    rng = np.random.default_rng(seed)
    a1, a2 = patterns()
    y = np.repeat([0, 1], n // 2)
    e1 = np.exp(-0.5 * ((TD - 0.2) / 0.04) ** 2); e2 = np.exp(-0.5 * ((TD - 0.47) / 0.1) ** 2)
    sig = np.outer(a1, e1) + np.outer(a2, e2)
    noise_mix = rng.normal(size=(NCH, NCH)) * 0.4 + np.eye(NCH)
    X = np.array([(2 * yy - 1) * snr * sig + noise_mix @ rng.normal(size=(NCH, len(TD))) for yy in y])
    return X, y


def lda_fit(Xtr, ytr, shrink=0.2):
    m0, m1 = Xtr[ytr == 0].mean(0), Xtr[ytr == 1].mean(0)
    S = np.cov(Xtr.T)
    S = (1 - shrink) * S + shrink * np.trace(S) / S.shape[0] * np.eye(S.shape[0])
    w = np.linalg.solve(S, m1 - m0); b = -w @ (m0 + m1) / 2
    return w, b


def time_decoding(X, y, k=5, seed=0):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(y)); folds = np.array_split(idx, k)
    acc = np.zeros(len(TD))
    for ti in range(len(TD)):
        c = 0
        for f in folds:
            tr = np.setdiff1d(idx, f)
            w, b = lda_fit(X[tr, :, ti], y[tr])
            c += np.sum(((X[f, :, ti] @ w + b) > 0) == y[f])
        acc[ti] = c / len(y)
    return acc


def gen_matrix(X, y, seed=0):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(y)); half = len(y) // 2
    tr, te = idx[:half], idx[half:]
    G = np.zeros((len(TD), len(TD)))
    for i in range(len(TD)):
        w, b = lda_fit(X[tr, :, i], y[tr])
        for j in range(len(TD)):
            G[i, j] = np.mean(((X[te, :, j] @ w + b) > 0) == y[te])
    return G


# ------------------------------------------------------------------ 3: encoding vs decoding
def f03_encdec(W=12.0):
    f = Fig()
    f["s"] = box(p2(-4.3, 0), 2.6, 1.2, tr("stimulus /\nmental state", "stimolo /\nstato mentale"), P.C, 17)
    f["b"] = box(p2(0, 0), 2.6, 1.2, tr("brain\nactivity", "attività\ncerebrale"), P.V, 17)
    f["e"] = box(p2(4.3, 0), 2.6, 1.2, tr("EEG\n(ch × time)", "EEG\n(canali × tempo)"), P.S, 17)
    f["a1"] = Arrow(p2(-2.95, 0.25), p2(-1.35, 0.25), buff=0, color=P.fg, stroke_width=3, tip_length=0.15)
    f["a2"] = Arrow(p2(1.35, 0.25), p2(2.95, 0.25), buff=0, color=P.fg, stroke_width=3, tip_length=0.15)
    f["enc"] = VGroup(Arrow(p2(-4.3, 1.1), p2(4.3, 1.1), buff=0, color=P.V, stroke_width=4, tip_length=0.2), txt(tr("ENCODING: how does the stimulus shape the signal? (ERP, GLM)", "ENCODING: come lo stimolo modella il segnale? (ERP, GLM)"), p2(0, 1.5), P.V, 16, weight="BOLD"))
    f["dec"] = VGroup(Arrow(p2(4.3, -1.1), p2(-4.3, -1.1), buff=0, color=P.S, stroke_width=4, tip_length=0.2), txt(tr("DECODING: can we read the stimulus from the signal? (MVPA)", "DECODING: possiamo leggere lo stimolo dal segnale? (MVPA)"), p2(0, -1.5), P.S, 16, weight="BOLD"))
    return f


# ------------------------------------------------------------------ 5: classificatore lineare 2D
def f05_lda(R=1.9):
    f = Fig()
    rng = np.random.default_rng(3)
    C = np.array([[1.0, 0.8], [0.8, 1.0]]) * 0.25
    A = rng.multivariate_normal([-0.35, 0.35], C, 60); B = rng.multivariate_normal([0.35, -0.35], C, 60)
    c = p2(-2.6, 0)
    f["ax"] = VGroup(Line(c + p2(-R, -R), c + p2(R, -R), color=P.fg, stroke_width=1.5), Line(c + p2(-R, -R), c + p2(-R, R), color=P.fg, stroke_width=1.5),
                     txt(tr("channel 1 (µV)", "canale 1 (µV)"), c + p2(0, -R - 0.3), P.muted, 14), txt(tr("channel 2", "canale 2"), c + p2(-R - 0.35, 0), P.muted, 14).rotate(PI / 2))
    sc = R / 1.6
    f["A"] = VGroup(*[Dot(c + p2(*(a * sc)), radius=0.045, color=P.V) for a in A])
    f["B"] = VGroup(*[Dot(c + p2(*(b * sc)), radius=0.045, color=P.S) for b in B])
    X = np.vstack([A, B]); y = np.r_[np.zeros(60), np.ones(60)]
    w, b = lda_fit(X, y.astype(int), 0.05)
    d = np.array([-w[1], w[0]]); d /= np.linalg.norm(d); p0 = -b * w / (w @ w)
    f["h"] = DashedLine(c + p2(*((p0 - 1.9 * d) * sc)), c + p2(*((p0 + 1.9 * d) * sc)), color=P.fg, stroke_width=3)
    wn = w / np.linalg.norm(w)
    f["w"] = Arrow(c + p2(*(p0 * sc)), c + p2(*((p0 + 0.9 * wn) * sc)), buff=0, color=P.C, stroke_width=5, tip_length=0.18)
    f["wl"] = txt("w", c + p2(*((p0 + 1.05 * wn) * sc)), P.C, 20, weight="BOLD")
    # proiezioni
    pa = A @ w + b; pb = B @ w + b
    O = p2(1.2, -1.2)
    bins = np.linspace(-6, 6, 25); wb = 4.6 / 24
    ha, _ = np.histogram(pa, bins); hb, _ = np.histogram(pb, bins); hm = max(ha.max(), hb.max())
    f["ha"] = VGroup(*[Rectangle(width=wb * 0.9, height=max(v / hm * 2.0, 0.003), stroke_width=0, fill_color=P.V, fill_opacity=0.6).move_to(O + p2(wb * (i + 0.5), 0), aligned_edge=DOWN) for i, v in enumerate(ha)])
    f["hb"] = VGroup(*[Rectangle(width=wb * 0.9, height=max(v / hm * 2.0, 0.003), stroke_width=0, fill_color=P.S, fill_opacity=0.6).move_to(O + p2(wb * (i + 0.5), 0), aligned_edge=DOWN) for i, v in enumerate(hb)])
    f["hx"] = Line(O, O + p2(4.6, 0), color=P.fg, stroke_width=1.5)
    f["h0"] = DashedLine(O + p2(2.3, 0), O + p2(2.3, 2.2), color=P.fg, stroke_width=2)
    f["ht"] = txt(tr("projection on w: y = wᵀx + b", "proiezione su w: y = wᵀx + b"), O + p2(2.3, 2.5), P.fg, 15)
    return f


# ------------------------------------------------------------------ 6: cross-validation
def f06_cv(W=10.0, k=5):
    f = Fig()
    for r in range(k):
        y = 1.3 - 0.55 * r
        for c in range(k):
            test = c == r
            f[f"b{r}{c}"] = Rectangle(width=W / k - 0.08, height=0.4, stroke_width=0, fill_color=P.S if test else P.V, fill_opacity=0.85 if test else 0.35).move_to(p2(-W / 2 + W / k * (c + 0.5), y))
        f[f"l{r}"] = txt(tr(f"fold {r + 1}", f"fold {r + 1}"), p2(-W / 2 - 0.6, y), P.muted, 14)
    f["lt"] = VGroup(txt(tr("train", "addestramento"), p2(-2.5, -1.7), P.V, 16, weight="BOLD"), txt("test", p2(-0.8, -1.7), P.S, 16, weight="BOLD"),
                     txt(tr("→ accuracy averaged over folds", "→ accuratezza media sui fold"), p2(2.2, -1.7), P.fg, 15))
    return f


# ------------------------------------------------------------------ 7: overfitting
def f07_overfit(W=4.6, Hh=2.4):
    f = Fig()
    O = p2(-W / 2, -1.3)
    f["ax"] = axes(O, W + 0.2, Hh + 0.2, tr("model complexity / features", "complessità del modello / feature"), tr("accuracy", "accuratezza"))
    x = np.linspace(0, 1, 100)
    tr_ = 0.55 + 0.44 * (1 - np.exp(-4 * x)); te = 0.56 + 0.3 * np.exp(-((x - 0.35) / 0.3) ** 2) + 0.04 * (1 - x)
    f["tr"] = VMobject(color=P.V, stroke_width=3.5).set_points_smoothly([O + p2(a * W, (b - 0.45) / 0.6 * Hh) for a, b in zip(x, tr_)])
    f["te"] = VMobject(color=P.S, stroke_width=3.5).set_points_smoothly([O + p2(a * W, (b - 0.45) / 0.6 * Hh) for a, b in zip(x, te)])
    f["lt"] = txt(tr("training", "addestramento"), O + p2(W * 0.85, (0.99 - 0.45) / 0.6 * Hh + 0.25), P.V, 15, weight="BOLD")
    f["le"] = txt(tr("test (cross-validated)", "test (cross-validation)"), O + p2(W * 0.8, (te[-1] - 0.45) / 0.6 * Hh - 0.3), P.S, 15, weight="BOLD")
    f["ch"] = DashedLine(O + p2(0, (0.5 - 0.45) / 0.6 * Hh), O + p2(W, (0.5 - 0.45) / 0.6 * Hh), color=P.muted, stroke_width=1.5)
    f["cl"] = txt(tr("chance 50 %", "caso 50 %"), O + p2(W + 0.55, (0.5 - 0.45) / 0.6 * Hh), P.muted, 13)
    return f


# ------------------------------------------------------------------ 9: metriche
def f09_metrics(R=1.2):
    f = Fig()
    cm = np.array([[40, 10], [15, 35]])
    c0 = p2(-4.2, 0.1); s = 1.1
    labs = [["TN", "FP"], ["FN", "TP"]]
    for i in range(2):
        for j in range(2):
            good = i == j
            f[f"c{i}{j}"] = VGroup(Rectangle(width=s, height=s, stroke_width=1.5, stroke_color=P.fg, fill_color=P.V if good else P.S, fill_opacity=0.35).move_to(c0 + p2((j - 0.5) * s, (0.5 - i) * s)),
                                   txt(f"{labs[i][j]}\n{cm[i, j]}", c0 + p2((j - 0.5) * s, (0.5 - i) * s), P.fg, 16, weight="BOLD"))
    f["tl"] = txt(tr("predicted", "predetto"), c0 + p2(0, s + 0.35), P.muted, 14)
    f["yl"] = txt(tr("true", "vero"), c0 + p2(-s - 0.45, 0), P.muted, 14).rotate(PI / 2)
    # ROC
    O = p2(-0.6, -1.3); Wr = 2.6
    f["rax"] = axes(O, Wr + 0.2, Wr + 0.2, tr("false-positive rate", "tasso falsi positivi"), tr("hit rate", "tasso di hit"))
    for k, (dp, col) in enumerate(((0.0, P.muted), (1.0, P.V), (2.0, P.S))):
        from scipy.stats import norm
        th = np.linspace(-4, 6, 100)
        fa = 1 - norm.cdf(th); hr = 1 - norm.cdf(th - dp)
        f[f"r{k}"] = VMobject(color=col, stroke_width=3).set_points_smoothly([O + p2(a * Wr, b * Wr) for a, b in zip(fa[::-1], hr[::-1])])
        auc = norm.cdf(dp / np.sqrt(2))
        f[f"a{k}"] = txt(f"d′={dec(dp, 0)} AUC={dec(auc)}", O + p2(Wr + 1.2, 0.35 + 0.45 * k), col, 13, weight="BOLD")
    f["mt"] = VGroup(txt(tr("accuracy = (TP+TN)/N = 0.75", "accuratezza = (TP+TN)/N = 0,75"), p2(-4.2, -1.55), P.fg, 14),
                     txt(tr("balanced acc. = (TPR+TNR)/2", "acc. bilanciata = (TPR+TNR)/2"), p2(-4.2, -1.95), P.fg, 14))
    return f


# ------------------------------------------------------------------ 10: pesi vs pattern (Haufe 2014)
def f10_haufe(R=1.1):
    f = Fig()
    X, y = sim_trials(400, seed=4)
    ti = np.argmin(np.abs(TD - 0.2))
    Xt = X[:, :, ti]
    w, b = lda_fit(Xt, y, 0.1)
    Cx = np.cov(Xt.T); a = Cx @ w
    a1, _ = patterns()
    for k, (v, lab, col) in enumerate(((w, tr("classifier weights w", "pesi del classificatore w"), P.S), (a, tr("activation pattern A = Σₓw", "pattern di attivazione A = Σₓw"), P.V), (a1, tr("true source map", "mappa vera della sorgente"), P.fg))):
        c = p2(-3.6 + 3.6 * k, 0.2)
        V, m = interp_map(v / np.abs(v).max(), n=121, p=2.5)
        f[f"m{k}"], f[f"o{k}"] = topomap(V, m, c, R, vmax=1.0, elec=True)
        f[f"l{k}"] = txt(lab, c + p2(0, -R - 0.4), col, 15, weight="BOLD")
    return f


# ------------------------------------------------------------------ 11: decoding nel tempo
def f11_timedec(W=6.0, Hh=2.6):
    f = Fig()
    X, y = sim_trials(400, seed=1)
    from scipy.ndimage import gaussian_filter1d
    acc = gaussian_filter1d(time_decoding(X, y), 1.2)
    O = p2(-W / 2, -1.3)
    f["ax"] = axes(O, W + 0.2, Hh + 0.2, tr("time (ms)", "tempo (ms)"), tr("accuracy", "accuratezza"))
    Y = lambda v: (v - 0.4) / 0.6 * Hh
    X_ = lambda t: (t + 0.2) / 1.0 * W
    f["ch"] = DashedLine(O + p2(0, Y(0.5)), O + p2(W, Y(0.5)), color=P.muted, stroke_width=1.5)
    f["z"] = DashedLine(O + p2(X_(0), 0), O + p2(X_(0), Hh), color=P.muted, stroke_width=1.5)
    f["c"] = VMobject(color=P.S, stroke_width=3.5).set_points_smoothly([O + p2(X_(t), Y(a)) for t, a in zip(TD, acc)])
    for ms in (0, 200, 400, 600):
        f[f"t{ms}"] = txt(str(ms), O + p2(X_(ms / 1000), -0.25), P.muted, 13)
    f["cl"] = txt(tr("chance", "caso"), O + p2(W + 0.4, Y(0.5)), P.muted, 13)
    return f


# ------------------------------------------------------------------ 12: generalizzazione temporale
def f12_tgm(W=3.4):
    f = Fig()
    X, y = sim_trials(200, seed=2, snr=0.8)
    G = gen_matrix(X, y)
    v = np.clip((G - 0.5) / 0.4, -1, 1)
    img = (np.dstack([cmap_rdbu(v[::-1]), np.ones(G.shape)]) * 255).astype(np.uint8)
    m = ImageMobject(img)
    from manim import RESAMPLING_ALGORITHMS
    m.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    m.stretch_to_fit_width(W); m.stretch_to_fit_height(W); m.move_to(p2(-2.4, 0))
    f["m"] = m
    O = p2(-2.4 - W / 2, -W / 2)
    f["fr"] = Rectangle(width=W, height=W, color=P.fg, stroke_width=1.5).move_to(p2(-2.4, 0))
    f["d"] = DashedLine(O, O + p2(W, W), color=P.fg, stroke_width=1.2)
    for ms in (0, 400):
        u = (ms / 1000 + 0.2) / 1.0 * W
        f[f"x{ms}"] = txt(str(ms), O + p2(u, -0.25), P.muted, 13); f[f"y{ms}"] = txt(str(ms), O + p2(-0.35, u), P.muted, 13)
    f["xl"] = txt(tr("testing time (ms)", "tempo di test (ms)"), O + p2(W / 2, -0.6), P.muted, 14)
    f["yl"] = txt(tr("training time (ms)", "tempo di addestramento (ms)"), O + p2(-0.75, W / 2), P.muted, 14).rotate(PI / 2)
    # schemi di King & Dehaene
    for k, (lab, kind) in enumerate(((tr("transient chain", "catena transitoria"), "diag"), (tr("sustained code", "codice sostenuto"), "square"))):
        c = p2(2.0 + 2.3 * k, 0.4); s = 1.6
        g = VGroup(Rectangle(width=s, height=s, color=P.fg, stroke_width=1.5).move_to(c))
        if kind == "diag":
            g.add(Line(c + p2(-s / 2, -s / 2), c + p2(s / 2, s / 2), color=P.S, stroke_width=10))
        else:
            g.add(Rectangle(width=s * 0.6, height=s * 0.6, stroke_width=0, fill_color=P.S, fill_opacity=0.8).move_to(c + p2(0.15, 0.15)))
        f[f"k{k}"] = VGroup(g, txt(lab, c + p2(0, -s / 2 - 0.3), P.fg, 14, weight="BOLD"))
    f["kt"] = txt(tr("King & Dehaene (2014)", "King & Dehaene (2014)"), p2(3.15, -1.2), P.muted, 13)
    return f


# ------------------------------------------------------------------ 15: BCI
def f15_bci(W=12.4):
    f = Fig()
    steps = [(tr("EEG\nacquisition", "acquisizione\nEEG"), P.C), (tr("pre-\nprocessing", "pre-\nelaborazione"), P.V), (tr("feature\nextraction", "estrazione\nfeature"), P.S),
             (tr("classifier", "classificatore"), PURP), (tr("device\ncommand", "comando\ndispositivo"), GRN)]
    n = len(steps); step = W / n
    for k, (lab, col) in enumerate(steps):
        c = p2(-W / 2 + step * (k + 0.5), 0.5)
        f[f"b{k}"] = box(c, step - 0.5, 1.2, lab, col, 16)
        if k < n - 1:
            f[f"a{k}"] = Arrow(c + p2((step - 0.5) / 2, 0), c + p2(step - (step - 0.5) / 2, 0), buff=0.02, color=P.fg, stroke_width=3, tip_length=0.13)
    f["fb"] = CurvedArrowSafe(p2(W / 2 - step / 2, -0.2), p2(-W / 2 + step / 2, -0.2))
    f["fl"] = txt(tr("feedback to the user (closed loop)", "feedback all'utente (circuito chiuso)"), p2(0, -1.55), P.S, 16, weight="BOLD")
    return f


def CurvedArrowSafe(a, b):
    from manim import CurvedArrow
    return CurvedArrow(a, b, angle=-PI / 4, color=P.S, stroke_width=3.5)


# ------------------------------------------------------------------ 16: P300 speller e SSVEP
def f16_paradigms(R=1.0):
    f = Fig()
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789_"
    c0 = p2(-4.2, 0.4); s = 0.42
    for i in range(6):
        for j in range(6):
            hl = i == 2
            f[f"g{i}{j}"] = VGroup(Rectangle(width=s, height=s, stroke_width=0, fill_color=P.S if hl else P.bg, fill_opacity=0.5 if hl else 0).move_to(c0 + p2((j - 2.5) * s, (2.5 - i) * s)),
                                   txt(chars[i * 6 + j], c0 + p2((j - 2.5) * s, (2.5 - i) * s), P.fg, 15, weight="BOLD"))
    f["pl"] = txt(tr("P300 speller: flashing rows/columns", "P300 speller: righe/colonne che lampeggiano"), c0 + p2(0, -1.6), P.fg, 15, weight="BOLD")
    # SSVEP: spettro
    O = p2(1.0, -1.1); Wd = 4.4; Hh = 2.2
    fr = np.linspace(4, 40, 400)
    sp = 1 / fr ** 0.8 * 3 + 2.2 * np.exp(-0.5 * ((fr - 12) / 0.25) ** 2) + 0.9 * np.exp(-0.5 * ((fr - 24) / 0.25) ** 2)
    f["sax"] = axes(O, Wd + 0.2, Hh + 0.2, "Hz", "")
    f["sp"] = VMobject(color=P.V, stroke_width=3).set_points_smoothly([O + p2((a - 4) / 36 * Wd, b / sp.max() * Hh) for a, b in zip(fr, sp)])
    f["s1"] = txt("12 Hz", O + p2((12 - 4) / 36 * Wd, Hh + 0.2), P.S, 14, weight="BOLD"); f["s2"] = txt("24 Hz", O + p2((24 - 4) / 36 * Wd, 0.9 / sp.max() * Hh + 0.55), P.S, 14)
    f["sl"] = txt(tr("SSVEP: target flickering at 12 Hz", "SSVEP: target che lampeggia a 12 Hz"), O + p2(Wd / 2, -0.55), P.fg, 15, weight="BOLD")
    return f


# ------------------------------------------------------------------ 18: EEG-fMRI
def f18_eegfmri(W=10.0):
    f = Fig()
    t = np.linspace(0, 60, 1200)
    rng = np.random.default_rng(4)
    alpha = 1 + 0.6 * np.sin(2 * np.pi * t / 24) + 0.2 * np.convolve(rng.normal(size=1200), np.ones(40) / 40, "same") * 5
    th = np.arange(0, 30, 0.05)
    hrf = th ** 5 * np.exp(-th) / 120 - 0.1 * th ** 15 * np.exp(-th) / 1.3e12
    reg = np.convolve(alpha - alpha.mean(), hrf)[:1200] * 0.05
    bold = -reg + 0.08 * np.convolve(rng.normal(size=1200), np.ones(60) / 60, "same") * 5
    O1 = p2(-W / 2, 1.2); O2 = p2(-W / 2, -0.3); O3 = p2(-W / 2, -1.7)
    f["a"] = VMobject(color=P.V, stroke_width=3).set_points_as_corners([O1 + p2(a / 60 * W, 0.5 * (b - 1)) for a, b in zip(t, alpha)])
    f["r"] = VMobject(color=P.S, stroke_width=3).set_points_as_corners([O2 + p2(a / 60 * W, 1.2 * b / np.abs(reg).max() * 0.5) for a, b in zip(t, reg)])
    f["b"] = VMobject(color=P.C, stroke_width=3).set_points_as_corners([O3 + p2(a / 60 * W, 0.6 * b / np.abs(bold).max()) for a, b in zip(t, bold)])
    f["la"] = txt(tr("EEG alpha power", "potenza alfa EEG"), O1 + p2(-1.3, 0), P.V, 15, weight="BOLD")
    f["lr"] = txt(tr("⊗ HRF = regressor", "⊗ HRF = regressore"), O2 + p2(-1.3, 0), P.S, 15, weight="BOLD")
    f["lb"] = txt(tr("occipital BOLD (anti-correlated)", "BOLD occipitale (anticorrelato)"), O3 + p2(-1.6, 0), P.C, 15, weight="BOLD")
    return f
