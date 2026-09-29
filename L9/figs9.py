"""Figure della Lezione 9 EEG: source imaging e connettività (modelli 2D SIMULATI)."""
import os as _os
_R = _os.environ.get("COURSE_ROOT") or _os.path.dirname(_os.path.abspath(__file__))
while not _os.path.exists(_os.path.join(_R, ".course_root")) and _os.path.dirname(_R) != _R:
    _R = _os.path.dirname(_R)
import sys
sys.path.insert(0, _R + "/common")
import numpy as np
from eegfigs import *
from manim import (VGroup, VMobject, Arrow, Line, DashedLine, Dot, Circle, Polygon, Rectangle, CurvedArrow,
                   RoundedRectangle, MathTex, ORIGIN, UP, DOWN, LEFT, RIGHT, PI, ImageMobject)
from scipy.signal import coherence, butter, sosfiltfilt, hilbert

P = F.P
PURP = "#8E7CC3"; GRN = "#6FCF97"


def dec(v, n=2):
    s = f"{v:.{n}f}"
    return s if LANG == "en" else s.replace(".", ",")


def hexc(rgb):
    r, g, b = (np.clip(np.asarray(rgb, float), 0, 1) * 255).astype(int)
    return "#%02x%02x%02x" % (r, g, b)


def heat(v):
    """0..1 → trasparente/giallo/rosso."""
    v = np.clip(v, 0, 1)
    return hexc(np.array([1.0, 0.95 - 0.75 * v, 0.3 - 0.3 * v]))


# ------------------------------------------------------------------ modello 2D: corteccia su un arco, sensori sul bordo
NS = 120; NE = 32
TH_S = np.linspace(-PI * 0.42, PI * 0.42, NS)     # sorgenti su un arco (angolo dal vertice)
R_CORTEX = 0.72; R_HEAD = 1.0


def src_pos():
    # corteccia "ondulata": raggio che varia (giri e solchi) → orientamenti diversi
    r = R_CORTEX + 0.05 * np.sin(9 * TH_S)
    return np.stack([r * np.sin(TH_S), r * np.cos(TH_S)], 1)


def src_ori():
    p = src_pos(); d = np.gradient(p, axis=0)
    n = np.stack([d[:, 1], -d[:, 0]], 1); n = n / np.linalg.norm(n, axis=1, keepdims=True)
    return n * np.sign((n * p).sum(1))[:, None]


TH_E = np.linspace(-PI * 0.5, PI * 0.5, NE)


def el_pos():
    return np.stack([R_HEAD * np.sin(TH_E), R_HEAD * np.cos(TH_E)], 1)


def leadfield():
    """potenziale 2D di un dipolo (∝ d·r/|r|², mezzo infinito) + fattore di sfocamento del cranio."""
    P_ = src_pos(); O = src_ori(); Epos = el_pos()
    L = np.zeros((NE, NS))
    for j in range(NS):
        d = Epos - P_[j]
        L[:, j] = (d @ O[j]) / (np.sum(d ** 2, 1) + 0.02)
    L = L - L.mean(0)
    return L


def inverse(L, y, method="mne", lam=0.05, C=None):
    G = L
    if method == "mne":
        W = np.eye(NS)
    elif method == "wmne":
        W = np.diag(1 / np.linalg.norm(L, axis=0) ** 2)
    else:
        W = np.eye(NS)
    if method == "lcmv":
        Ci = np.linalg.inv(C + 1e-3 * np.trace(C) / NE * np.eye(NE))
        out = []
        for i in range(NS):
            l = L[:, i]; w = Ci @ l / (l @ Ci @ l)
            out.append((w @ C @ w) / (w @ w))          # unit-noise-gain (NAI)
        out = np.array(out); out = out - np.median(out)
        return np.convolve(out, np.exp(-0.5 * (np.arange(-6, 7) / 2.0) ** 2), 'same')
    GW = G @ W @ G.T
    reg = lam * np.trace(GW) / NE
    K = W @ G.T @ np.linalg.inv(GW + reg * np.eye(NE))
    j = K @ y
    if method == "sloreta":
        R = K @ G
        j = j / np.sqrt(np.clip(np.diag(R), 1e-12, None))
    if method == "lcmv":
        Ci = np.linalg.inv(C + 1e-3 * np.trace(C) / NE * np.eye(NE))
        j = np.array([(L[:, i] @ Ci @ y) / (L[:, i] @ Ci @ L[:, i]) for i in range(NS)])
        pw = np.array([1 / (L[:, i] @ Ci @ L[:, i]) for i in range(NS)])
        return np.abs(j) * 0 + pw
    return j


def head2d(c, R, f=None, col=None):
    col = col or P.fg
    g = VGroup(Arc(radius=R, start_angle=-0.1, angle=PI + 0.2, color=col, stroke_width=3).move_to(c + p2(0, R / 2 - 0.05)) if False else Circle(radius=R, color=col, stroke_width=3).move_to(c))
    g.add(Circle(radius=R * 0.93, color=P.aux, stroke_width=1.5).move_to(c))
    return g


def headc(c, R, col=None, sw=3):
    col = col or P.fg
    from manim import Arc
    return VGroup(Arc(radius=R, start_angle=-0.12, angle=PI + 0.24, color=col, stroke_width=sw, arc_center=c),
                  Line(c + p2(R * np.cos(-0.12), R * np.sin(-0.12)), c + p2(-R * np.cos(-0.12), R * np.sin(-0.12)), color=col, stroke_width=sw))


def cortex_mob(c, R, vals=None, col=None, sw=6):
    Ps = src_pos() * R + c[:2]
    if vals is None:
        return VMobject(color=col or P.muted, stroke_width=sw).set_points_smoothly([p2(*p) for p in Ps])
    v = np.abs(vals); v = (v - v.min()) / (v.max() - v.min() + 1e-12)
    g = VGroup()
    for i in range(NS - 1):
        g.add(Line(p2(*Ps[i]), p2(*Ps[i + 1]), color=heat(v[i]) if v[i] > 0.05 else P.muted, stroke_width=sw + 4 * v[i]))
    return g


def sensors_mob(c, R, y=None, r=0.07):
    Ep = el_pos() * R + c[:2]
    g = VGroup()
    vm = np.abs(y).max() if y is not None else 1
    for i, e in enumerate(Ep):
        col = hexc(cmap_rdbu(np.array(y[i] / vm))) if y is not None else P.bg
        g.add(Circle(radius=r, color=P.fg, stroke_width=1.5, fill_color=col, fill_opacity=1).move_to(p2(*e)))
    return g


# ------------------------------------------------------------------ 3: forward / inverse
def f03_forward(R=1.5):
    f = Fig()
    L = leadfield()
    j = np.exp(-0.5 * ((np.arange(NS) - 40) / 3) ** 2)
    y = L @ j
    for k, (lab, show_src, show_y) in enumerate(((tr("sources j", "sorgenti j"), True, False), (tr("scalp data y = L·j", "dati di scalpo y = L·j"), False, True))):
        c = p2(-3.2 + 6.4 * k, -0.3)
        f[f"h{k}"] = headc(c, R)
        f[f"c{k}"] = cortex_mob(c, R, j if show_src else None)
        f[f"e{k}"] = sensors_mob(c, R, y if show_y else None)
        f[f"l{k}"] = txt(lab, c + p2(0, -0.5), P.fg, 17, weight="BOLD")
    f["af"] = CurvedArrow(p2(-1.3, 1.3), p2(1.3, 1.3), angle=-PI / 3, color=P.V, stroke_width=4)
    f["lf"] = txt(tr("forward: unique", "diretto: unico"), p2(0, 2.15), P.V, 17, weight="BOLD")
    f["ai"] = CurvedArrow(p2(1.3, -0.2), p2(-1.3, -0.2), angle=-PI / 3, color=P.S, stroke_width=4)
    f["li"] = txt(tr("inverse: ill-posed", "inverso: mal posto"), p2(0, -1.15), P.S, 17, weight="BOLD")
    return f


# ------------------------------------------------------------------ 5: modelli di testa
def f05_headmodels(R=1.35):
    f = Fig()
    specs = [(tr("3-shell sphere", "sfera a 3 gusci"), "sph"), ("BEM", "bem"), ("FEM", "fem")]
    lay = [(1.0, "#E0B99A"), (0.93, "#D9D4C7"), (0.86, "#8FC7D9"), (0.82, "#C9A7B5")]
    for k, (lab, kind) in enumerate(specs):
        c = p2(-4.2 + 4.2 * k, 0.2)
        for j, (r, col) in enumerate(lay[:3] if kind == "sph" else lay):
            if kind == "sph":
                m = Circle(radius=R * r, color=P.fg, stroke_width=1.5, fill_color=col, fill_opacity=0.9)
            else:
                th = np.linspace(0, 2 * PI, 90)
                rr = R * r * (1 + 0.06 * np.sin(3 * th + j) + 0.04 * np.cos(5 * th) + (0.03 * np.sin(17 * th) if j == 3 else 0))
                rr = rr * np.where(np.sin(th) < 0, 0.92, 1.0)
                m = Polygon(*[p2(a * np.cos(t_), b * np.sin(t_)) for a, b, t_ in zip(rr, rr * 1.08, th)], color=P.fg, stroke_width=1.5, fill_color=col, fill_opacity=0.9)
            f[f"s{k}{j}"] = m.move_to(c)
        if kind == "fem":
            pts = [c + p2(R * 0.8 * np.cos(a), R * 0.85 * np.sin(a)) for a in np.linspace(0, 2 * PI, 13)]
            f[f"mesh{k}"] = VGroup(*[Line(c, p, color=P.fg, stroke_width=0.8, stroke_opacity=0.6) for p in pts],
                                   *[Circle(radius=R * s, color=P.fg, stroke_width=0.8, stroke_opacity=0.6).move_to(c) for s in (0.3, 0.55)])
        f[f"l{k}"] = txt(lab, c + p2(0, -R - 0.45), P.fg, 17, weight="BOLD")
    f["d0"] = txt(tr("analytic, fast", "analitico, veloce"), p2(-4.2, -2.05), P.muted, 14)
    f["d1"] = txt(tr("realistic surfaces (MRI)", "superfici realistiche (RM)"), p2(0, -2.05), P.muted, 14)
    f["d2"] = txt(tr("volumes, anisotropy, CSF", "volumi, anisotropia, liquor"), p2(4.2, -2.05), P.muted, 14)
    return f


# ------------------------------------------------------------------ 6: leadfield
def f06_leadfield(W=3.6, Hh=2.4, R=1.1):
    f = Fig()
    L = leadfield()
    vm = np.abs(L).max() * 0.6
    img = (np.dstack([cmap_rdbu(L / vm), np.ones(L.shape)]) * 255).astype(np.uint8)
    m = ImageMobject(img)
    from manim import RESAMPLING_ALGORITHMS
    m.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    m.stretch_to_fit_width(W); m.stretch_to_fit_height(Hh); m.move_to(p2(-3.0, 0))
    f["m"] = m
    f["fr"] = Rectangle(width=W, height=Hh, color=P.fg, stroke_width=1.5).move_to(p2(-3.0, 0))
    f["xl"] = txt(tr(f"{NS} sources", f"{NS} sorgenti"), p2(-3.0, -Hh / 2 - 0.3), P.muted, 14)
    f["yl"] = txt(tr(f"{NE} electrodes", f"{NE} elettrodi"), p2(-3.0 - W / 2 - 0.35, 0), P.muted, 14).rotate(PI / 2)
    col = 40
    f["hl"] = Rectangle(width=W / NS * 2, height=Hh, color=P.S, stroke_width=2.5).move_to(p2(-3.0 - W / 2 + W * (col + 0.5) / NS, 0))
    c = p2(2.6, 0)
    j = np.zeros(NS); j[col] = 1
    f["h"] = headc(c, R * 1.4)
    f["c"] = cortex_mob(c, R * 1.4, j)
    f["e"] = sensors_mob(c, R * 1.4, L[:, col])
    f["ar"] = Arrow(p2(-1.0, 0), p2(0.9, 0), buff=0, color=P.S, stroke_width=4, tip_length=0.18)
    f["lc"] = txt(tr("one column = scalp map of one source", "una colonna = mappa di scalpo di una sorgente"), c + p2(0, -0.55), P.fg, 15)
    return f


# ------------------------------------------------------------------ 7: problema mal posto
def f07_illposed(R=1.35):
    f = Fig()
    L = leadfield()
    j1 = np.exp(-0.5 * ((np.arange(NS) - 60) / 4) ** 2)
    y = L @ j1
    # soluzione alternativa: minima norma + componente nel nullo
    Lp = np.linalg.pinv(L)
    Nsp = np.eye(NS) - Lp @ L
    rng = np.random.default_rng(2)
    z = Nsp @ rng.normal(size=NS) * 3
    j2 = Lp @ y + z
    for k, (j, lab) in enumerate(((j1, tr("one deep focal source", "una sorgente focale")), (j2, tr("a very different pattern", "una configurazione molto diversa")))):
        c = p2(-3.0 + 6.0 * k, 0.1)
        f[f"h{k}"] = headc(c, R)
        f[f"c{k}"] = cortex_mob(c, R, j)
        f[f"e{k}"] = sensors_mob(c, R, L @ j)
        f[f"l{k}"] = txt(lab, c + p2(0, -0.5), P.fg, 16, weight="BOLD")
    f["eq"] = txt("=", p2(0, 0.1), P.fg, 40)
    f["t"] = txt(tr(f"identical scalp data: {NE} equations, {NS} unknowns", f"dati di scalpo identici: {NE} equazioni, {NS} incognite"), p2(0, 1.9), P.S, 17, weight="BOLD")
    return f


# ------------------------------------------------------------------ 10: confronto dei metodi inversi
def f10_methods(R=1.05):
    f = Fig()
    L = leadfield()
    rng = np.random.default_rng(5)
    src = 55
    t = np.arange(400) / 250
    s = np.sin(2 * np.pi * 10 * t)
    J = np.zeros((NS, len(t))); J[src] = s
    Y = L @ J + rng.normal(size=(NE, len(t))) * np.abs(L[:, src]).max() * 0.08
    C = Y @ Y.T / len(t)
    y = L[:, src]
    res = [(tr("true source", "sorgente vera"), np.exp(-0.5 * ((np.arange(NS) - src) / 2.5) ** 2)), ("MNE", inverse(L, y, "mne")), (tr("depth-weighted MNE", "MNE pesato"), inverse(L, y, "wmne")),
           ("sLORETA", inverse(L, y, "sloreta")), (tr("LCMV beamformer", "beamformer LCMV"), inverse(L, None, "lcmv", C=C))]
    for k, (lab, j) in enumerate(res):
        c = p2(-5.2 + 2.6 * k, 0.1)
        f[f"h{k}"] = headc(c, R, sw=2.5)
        f[f"c{k}"] = cortex_mob(c, R, j, sw=5)
        f[f"l{k}"] = txt(lab, c + p2(0, -0.45), P.fg, 14, weight="BOLD")
    return f


# ------------------------------------------------------------------ 11: regolarizzazione
def f11_lambda(R=1.05):
    f = Fig()
    L = leadfield(); rng = np.random.default_rng(3)
    y = L[:, 55] + rng.normal(size=NE) * np.abs(L[:, 55]).max() * 0.15
    for k, lam in enumerate((1e-4, 0.05, 2.0)):
        c = p2(-3.6 + 3.6 * k, 0.1)
        j = inverse(L, y, "sloreta", lam=lam)
        f[f"h{k}"] = headc(c, R, sw=2.5)
        f[f"c{k}"] = cortex_mob(c, R, j, sw=5)
        lab = [tr("λ too small: fits noise", "λ troppo piccolo: segue il rumore"), tr("λ adequate", "λ adeguato"), tr("λ too large: over-smooth", "λ troppo grande: troppo liscio")][k]
        f[f"l{k}"] = txt(lab, c + p2(0, -0.45), [P.S, P.V, P.S][k], 14, weight="BOLD")
    return f


# ------------------------------------------------------------------ 14: conduzione di volume e connettività spuria
def f14_vc(R=1.4):
    f = Fig()
    c = p2(-3.6, 0)
    L = leadfield()
    j = np.zeros(NS); j[60] = 1
    f["h"] = headc(c, R)
    f["c"] = cortex_mob(c, R, j)
    f["e"] = sensors_mob(c, R, L @ j)
    Ep = el_pos() * R + c[:2]
    for i, col in ((12, P.V), (19, P.C)):
        f[f"k{i}"] = Circle(radius=0.14, color=col, stroke_width=4).move_to(p2(*Ep[i]))
    t = np.linspace(0, 1, 400)
    s = np.sin(2 * np.pi * 6 * t) * (1 + 0.3 * np.sin(2 * np.pi * t))
    f["s1"] = VMobject(color=P.V, stroke_width=2.5).set_points_as_corners([p2(-1.2 + 4.8 * a, 1.0 + 0.5 * b) for a, b in zip(t, s * L[12, 60] / np.abs(L[:, 60]).max())])
    f["s2"] = VMobject(color=P.C, stroke_width=2.5).set_points_as_corners([p2(-1.2 + 4.8 * a, -0.6 + 0.5 * b) for a, b in zip(t, s * L[19, 60] / np.abs(L[:, 60]).max())])
    f["t"] = txt(tr("one source → two electrodes: correlated at ZERO lag", "una sorgente → due elettrodi: correlati a ritardo ZERO"), p2(1.2, -1.3), P.S, 16, weight="BOLD")
    return f


# ------------------------------------------------------------------ 16: fasi: zero-lag vs sfasate
def f16_phase(R=1.2):
    f = Fig()
    rng = np.random.default_rng(7)
    specs = [(0.0, 0.25, tr("zero-lag (volume conduction)", "ritardo zero (conduzione di volume)")), (PI / 2.5, 0.35, tr("consistent non-zero lag", "ritardo costante non nullo")), (0.0, 3.0, tr("random phase", "fase casuale"))]
    for k, (mu, sd, lab) in enumerate(specs):
        c = p2(-4.3 + 4.3 * k, 0.2)
        phall = rng.normal(mu, sd * 0.6 if k == 0 else sd, 2000) if sd < 2 else rng.uniform(-PI, PI, 2000)
        ph = phall[:60]
        ph = np.where(k == 0, np.where(rng.uniform(size=60) < 0.5, ph, ph + PI) * 0 + ph, ph)
        f[f"c{k}"] = VGroup(Circle(radius=R, color=P.aux, stroke_width=1.5).move_to(c), Line(c + p2(-R, 0), c + p2(R, 0), color=P.aux, stroke_width=1), Line(c + p2(0, -R), c + p2(0, R), color=P.aux, stroke_width=1))
        f[f"v{k}"] = VGroup(*[Line(c, c + R * np.array([np.cos(a), np.sin(a), 0]), color=P.V, stroke_width=1.3, stroke_opacity=0.6) for a in ph])
        z = np.exp(1j * phall)
        plv = abs(z.mean())
        wpli = abs(np.mean(np.sin(phall))) / (np.mean(np.abs(np.sin(phall))) + 1e-9)
        f[f"t{k}"] = VGroup(txt(lab, c + p2(0, -R - 0.35), P.fg, 14, weight="BOLD"),
                            txt(f"PLV = {dec(plv)}   wPLI = {dec(wpli)}", c + p2(0, -R - 0.75), P.S, 14))
    return f


# ------------------------------------------------------------------ 17: Granger
def granger_sim(n=3000, seed=1):
    rng = np.random.default_rng(seed)
    x = np.zeros(n); y = np.zeros(n)
    for t in range(2, n):
        x[t] = 0.55 * x[t - 1] - 0.3 * x[t - 2] + rng.normal()
        y[t] = 0.5 * y[t - 1] + 0.6 * x[t - 2] + rng.normal()
    return x, y


def f18_granger(W=6.0):
    f = Fig()
    x, y = granger_sim()
    t = np.arange(120)
    f["x"] = VMobject(color=P.V, stroke_width=2.5).set_points_as_corners([p2(-6.0 + a / 120 * W, 1.2 + 0.22 * b) for a, b in zip(t, x[500:620])])
    f["y"] = VMobject(color=P.S, stroke_width=2.5).set_points_as_corners([p2(-6.0 + a / 120 * W, -0.6 + 0.22 * b) for a, b in zip(t, y[500:620])])
    f["lx"] = txt("X", p2(-6.35, 1.2), P.V, 20, weight="BOLD"); f["ly"] = txt("Y", p2(-6.35, -0.6), P.S, 20, weight="BOLD")
    # varianza residua con e senza il passato di X
    def ar_res(target, preds, p=4):
        n = len(target); rows = []
        for t_ in range(p, n):
            rows.append(np.concatenate([pr[t_ - p:t_][::-1] for pr in preds]))
        A = np.array(rows); b = target[p:]
        coef, *_ = np.linalg.lstsq(A, b, rcond=None)
        return np.var(b - A @ coef)
    gxy = np.log(ar_res(y, [y]) / ar_res(y, [y, x])); gyx = np.log(ar_res(x, [x]) / ar_res(x, [x, y]))
    f["b1"] = Rectangle(width=0.9, height=gxy * 2.2, stroke_width=0, fill_color=P.S, fill_opacity=0.9).move_to(p2(2.2, -1.2), aligned_edge=DOWN)
    f["b2"] = Rectangle(width=0.9, height=max(gyx * 2.2, 0.02), stroke_width=0, fill_color=P.V, fill_opacity=0.9).move_to(p2(3.8, -1.2), aligned_edge=DOWN)
    f["ax"] = Line(p2(1.4, -1.2), p2(4.6, -1.2), color=P.fg, stroke_width=2)
    f["t1"] = txt("X → Y", p2(2.2, -1.5), P.S, 16, weight="BOLD"); f["t2"] = txt("Y → X", p2(3.8, -1.5), P.V, 16, weight="BOLD")
    f["v1"] = txt(dec(gxy), p2(2.2, -1.2 + gxy * 2.2 + 0.25), P.S, 14); f["v2"] = txt(dec(gyx), p2(3.8, -1.2 + max(gyx * 2.2, 0.02) + 0.25), P.V, 14)
    f["tt"] = txt(tr("Granger causality (log variance ratio)", "causalità di Granger (log rapporto di varianze)"), p2(3.0, 1.9), P.fg, 15, weight="BOLD")
    return f


# ------------------------------------------------------------------ 19: grafo
def f19_graph(R=1.7):
    f = Fig()
    c = p2(-3.2, 0)
    f["h"] = head(c, R)
    rng = np.random.default_rng(3)
    names = NAMES
    pos = {n: c + el2d(n, R) for n in names}
    A = np.zeros((len(names), len(names)))
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            d = np.linalg.norm(pos[names[i]] - pos[names[j]])
            if rng.uniform() < 0.9 * np.exp(-d / 0.9) + (0.06 if names[i][0] != names[j][0] else 0):
                A[i, j] = A[j, i] = 1
    deg = A.sum(0)
    edges = VGroup()
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            if A[i, j]:
                edges.add(Line(pos[names[i]], pos[names[j]], color=P.V, stroke_width=1.8, stroke_opacity=0.7))
    f["ed"] = edges
    f["nd"] = VGroup(*[Dot(pos[n], radius=0.07 + 0.025 * deg[i], color=P.S) for i, n in enumerate(names)])
    items = [(tr("degree", "grado"), tr("number of links of a node (hubs)", "numero di connessioni di un nodo (hub)")),
             (tr("clustering", "clustering"), tr("how connected the neighbours are", "quanto sono connessi i vicini")),
             (tr("path length", "lunghezza dei cammini"), tr("steps between nodes (integration)", "passi tra i nodi (integrazione)")),
             (tr("small-world", "small-world"), tr("high clustering + short paths", "alto clustering + cammini brevi")),
             (tr("modularity", "modularità"), tr("communities of densely linked nodes", "comunità di nodi densamente collegati"))]
    for k, (a, b) in enumerate(items):
        f[f"i{k}"] = VGroup(txt(a, p2(0.4, 1.6 - 0.75 * k), P.S, 16, weight="BOLD").align_to(p2(0.4, 0), LEFT),
                            txt(b, p2(0.4, 1.3 - 0.75 * k), P.fg, 14).align_to(p2(0.4, 0), LEFT))
    return f
