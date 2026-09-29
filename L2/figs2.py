"""Figure della Lezione 2 EEG: basi cellulari dell'EEG."""
import os as _os
_R = _os.environ.get("COURSE_ROOT") or _os.path.dirname(_os.path.abspath(__file__))
while not _os.path.exists(_os.path.join(_R, ".course_root")) and _os.path.dirname(_R) != _R:
    _R = _os.path.dirname(_R)
import sys
sys.path.insert(0, _R + "/common")
import numpy as np
from eegfigs import *
import neuro as N
from manim import (VGroup, VMobject, Arrow, Line, DashedLine, DoubleArrow, Dot, Circle, Ellipse, Polygon, Rectangle,
                   RoundedRectangle, Arc, ArcBetweenPoints, CurvedArrow, MathTex, ORIGIN, UP, DOWN, LEFT, RIGHT, PI)

P = F.P
PURP = "#8E7CC3"; GRN = "#6FCF97"
ION = {"Na": P.S, "K": P.V, "Cl": GRN, "Ca": P.C}


def ion_dot(p, kind, r=0.09):
    return Circle(radius=r, color=ION[kind], fill_color=ION[kind], fill_opacity=0.9, stroke_width=0).move_to(p)


# ------------------------------------------------------------------ 3: la domanda (cellula piramidale sotto lo scalpo)
def f03_question():
    f = Fig()
    f["scalp"] = ArcBetweenPoints(p2(-3.2, 1.6), p2(3.2, 1.6), angle=-0.5, color=P.muted, stroke_width=4)
    f["sl"] = txt(tr("scalp", "scalpo"), p2(3.6, 1.9), P.muted, 18)
    f["cell"] = pyramidal(p2(0, -1.4), 1.0)
    f["el"] = Circle(radius=0.12, color=P.fg, fill_color=P.bg, fill_opacity=1, stroke_width=2).move_to(p2(0, 2.02))
    # tracciato EEG: deflessione verso il basso = negativo
    t = np.linspace(0, 1, 200); x = -np.exp(-0.5 * ((t - 0.5) / 0.08) ** 2)
    f["tr"] = VMobject(color=P.S, stroke_width=3).set_points_smoothly([p2(1.2 + 1.8 * u, 2.9 + 0.6 * v) for u, v in zip(t, x)])
    f["base"] = DashedLine(p2(1.2, 2.9), p2(3.0, 2.9), color=P.aux, stroke_width=1.5)
    f["neg"] = txt(tr("negative deflection", "deflessione negativa"), p2(2.1, 3.4), P.S, 16)
    f["q"] = txt("?", p2(0.8, 0.9), P.C, 40, weight="BOLD")
    return f


# ------------------------------------------------------------------ 5: anatomia del neurone
def f05_neuron(W=9.0):
    f = Fig()
    soma = p2(-2.4, 0)
    f["soma"] = Circle(radius=0.45, color=P.fg, fill_color=P.V, fill_opacity=0.3, stroke_width=3).move_to(soma)
    rng = np.random.default_rng(3)
    dend = VGroup()
    for k in range(7):
        a = PI / 2 + (k - 3) * 0.42 + PI * 0.5 * (k % 2 == 0) * 0
        a = [2.2, 2.6, 3.0, 3.4, 3.8, 4.2, 1.8][k]
        d = np.array([np.cos(a), np.sin(a), 0])
        e = soma + 1.5 * d
        dend.add(Line(soma + 0.42 * d, e, color=P.fg, stroke_width=3))
        for s in (-0.5, 0.5):
            dend.add(Line(e, e + 0.6 * np.array([np.cos(a + s), np.sin(a + s), 0]), color=P.fg, stroke_width=2))
    f["dend"] = dend
    hill = soma + p2(0.45, 0)
    f["hill"] = Polygon(hill + p2(0, 0.18), hill + p2(0, -0.18), hill + p2(0.45, -0.07), hill + p2(0.45, 0.07), color=P.S, fill_color=P.S, fill_opacity=0.8, stroke_width=0)
    ax = VGroup()
    x = hill[0] + 0.45
    for k in range(5):
        ax.add(RoundedRectangle(corner_radius=0.1, width=0.95, height=0.3, color=P.C, fill_color=P.C, fill_opacity=0.35, stroke_width=2).move_to(p2(x + 0.55 + 1.1 * k, 0)))
    f["myelin"] = ax
    f["axon"] = Line(p2(x, 0), p2(x + 5.6, 0), color=P.fg, stroke_width=2.5)
    term = p2(x + 5.6, 0)
    f["term"] = VGroup(*[VGroup(Line(term, term + p2(0.5, 0.5 * s), color=P.fg, stroke_width=2), Dot(term + p2(0.5, 0.5 * s), radius=0.09, color=P.S)) for s in (-1, 0, 1)])
    f["l_d"] = txt(tr("dendrites (input)", "dendriti (input)"), soma + p2(-1.2, 2.25), P.fg, 18)
    f["l_s"] = txt(tr("soma", "soma"), soma + p2(-0.95, -0.75), P.fg, 18)
    f["l_h"] = txt(tr("axon hillock (trigger zone)", "monticolo assonale (zona trigger)"), hill + p2(1.4, -0.75), P.S, 18)
    f["l_m"] = txt(tr("myelinated axon (output)", "assone mielinizzato (output)"), p2(x + 2.8, 0.55), P.C, 18)
    f["l_t"] = txt(tr("synaptic terminals", "terminali sinaptici"), term + p2(0.3, -0.95), P.fg, 18)
    return f


# ------------------------------------------------------------------ 6: membrana (doppio strato) e canali
def f06_membrane(W=8.0):
    f = Fig()
    heads = VGroup(); tails = VGroup()
    xs = np.arange(-W / 2, W / 2 + 0.01, 0.32)
    for x in xs:
        if abs(x - 0.0) < 0.45 or abs(x - 2.2) < 0.45:
            continue
        for s in (1, -1):
            c = p2(x, 0.62 * s)
            heads.add(Circle(radius=0.13, color=P.C, fill_color=P.C, fill_opacity=0.9, stroke_width=0).move_to(c))
            tails.add(Line(c - p2(0.04, 0.13 * s), c - p2(0.04, 0.5 * s), color=P.muted, stroke_width=2),
                      Line(c + p2(0.04, -0.13 * s), c + p2(0.04, -0.5 * s), color=P.muted, stroke_width=2))
    f["tails"] = tails; f["heads"] = heads
    for k, (x, col, lab) in enumerate(((0.0, P.V, "K⁺"), (2.2, P.S, "Na⁺"))):
        f[f"ch{k}"] = VGroup(RoundedRectangle(corner_radius=0.15, width=0.34, height=1.6, color=col, fill_color=col, fill_opacity=0.5, stroke_width=2).move_to(p2(x - 0.22, 0)),
                             RoundedRectangle(corner_radius=0.15, width=0.34, height=1.6, color=col, fill_color=col, fill_opacity=0.5, stroke_width=2).move_to(p2(x + 0.22, 0)))
        f[f"cl{k}"] = txt(tr("channel ", "canale ") + lab, p2(x, -1.2), col, 16)
    f["out"] = txt(tr("outside", "esterno"), p2(-W / 2 + 0.6, 1.25), P.fg, 18)
    f["in"] = txt(tr("inside", "interno"), p2(-W / 2 + 0.6, -1.25), P.fg, 18)
    f["th"] = txt(tr("≈5 nm lipid bilayer = insulator → membrane acts as a capacitor (≈1 µF/cm²)", "doppio strato lipidico ≈5 nm = isolante → la membrana è un condensatore (≈1 µF/cm²)"), p2(0, -1.75), P.muted, 16)
    return f


# ------------------------------------------------------------------ 7: concentrazioni ioniche e potenziali di Nernst
IONS = [("K⁺", 140, 5, 1, "K"), ("Na⁺", 12, 145, 1, "Na"), ("Cl⁻", 10, 110, -1, "Cl"), ("Ca²⁺", 1e-4, 2, 2, "Ca")]


def f07_ions(W=8.0):
    f = Fig()
    O = p2(-W / 2 + 1.2, -1.8)
    Hmax = 3.2
    lp = lambda c: logpos(c, 1e-5, 1e3, Hmax)
    f["ax"] = Line(O, O + p2(0, Hmax + 0.2), color=P.fg, stroke_width=2)
    for c in (1e-4, 1e-2, 1, 1e2):
        f[f"t{c}"] = VGroup(Line(O + p2(-0.08, lp(c)), O + p2(0.08, lp(c)), color=P.fg, stroke_width=2), txt({1e-4: "0.1 µM", 1e-2: "10 µM", 1: "1 mM", 1e2: "100 mM"}[c], O + p2(-0.7, lp(c)), P.muted, 14))
    for k, (n, ci, co, z, key) in enumerate(IONS):
        x = O[0] + 0.9 + 1.55 * k
        f[f"bi{k}"] = Rectangle(width=0.5, height=lp(ci), stroke_width=0, fill_color=ION[key], fill_opacity=0.45).move_to(p2(x - 0.28, O[1] + lp(ci) / 2))
        f[f"bo{k}"] = Rectangle(width=0.5, height=lp(co), stroke_width=0, fill_color=ION[key], fill_opacity=0.95).move_to(p2(x + 0.28, O[1] + lp(co) / 2))
        f[f"n{k}"] = txt(n, p2(x, O[1] - 0.3), ION[key], 20, weight="BOLD")
        E_ = N.nernst(co, ci, z)
        f[f"e{k}"] = txt(f"E = {E_:+.0f} mV", p2(x, O[1] - 0.7), P.fg, 15)
    f["leg"] = txt(tr("pale = inside · solid = outside (log scale)", "chiaro = dentro · pieno = fuori (scala log)"), p2(0.5, O[1] + Hmax + 0.45), P.muted, 15)
    return f


# ------------------------------------------------------------------ 9-10: diffusione vs forza elettrica; Nernst
def f09_two_forces():
    f = Fig()
    f["mem"] = Line(p2(0, -1.6), p2(0, 1.6), color=P.C, stroke_width=8)
    rng = np.random.default_rng(1)
    for k in range(16):
        f[f"i{k}"] = ion_dot(p2(-rng.uniform(0.3, 2.6), rng.uniform(-1.4, 1.4)), "K")
    for k in range(4):
        f[f"o{k}"] = ion_dot(p2(rng.uniform(0.3, 2.6), rng.uniform(-1.4, 1.4)), "K")
    f["d"] = Arrow(p2(-0.9, 1.9), p2(0.9, 1.9), buff=0, color=P.V, stroke_width=5, tip_length=0.18)
    f["dl"] = txt(tr("diffusion (concentration)", "diffusione (concentrazione)"), p2(0, 2.3), P.V, 16)
    f["e"] = Arrow(p2(0.9, -1.9), p2(-0.9, -1.9), buff=0, color=P.S, stroke_width=5, tip_length=0.18)
    f["el"] = txt(tr("electric force (charge)", "forza elettrica (carica)"), p2(0, -2.3), P.S, 16)
    f["in"] = txt(tr("inside", "dentro"), p2(-1.5, 1.8), P.fg, 16); f["out"] = txt(tr("outside", "fuori"), p2(1.5, 1.8), P.fg, 16)
    return f


def f10_scale(H=4.4):
    """scala dei potenziali: E_K, E_Cl, V_riposo, E_Na, E_Ca."""
    f = Fig()
    v0, v1 = -100, 140
    y = lambda v: (v - v0) / (v1 - v0) * H - H / 2
    f["ax"] = Line(p2(0, y(v0)), p2(0, y(v1)), color=P.fg, stroke_width=3)
    for v in (-100, -50, 0, 50, 100):
        f[f"t{v}"] = VGroup(Line(p2(-0.1, y(v)), p2(0.1, y(v)), color=P.fg, stroke_width=2), txt(f"{v:+d}" if v else "0", p2(-0.55, y(v)), P.muted, 14))
    items = [("E(K⁺)", N.nernst(5, 140), P.V), ("E(Cl⁻)", N.nernst(110, 10, -1), GRN), (tr("V rest", "V riposo"), N.ghk(1, 0.05, 0.45), P.fg),
             ("E(Na⁺)", N.nernst(145, 12), P.S), ("E(Ca²⁺)", N.nernst(2, 1e-4, 2), P.C)]
    for k, (n, v, col) in enumerate(items):
        side = 1 if k % 2 == 0 else 1
        f[f"m{k}"] = VGroup(Line(p2(-0.2, y(v)), p2(0.35, y(v)), color=col, stroke_width=5),
                            txt(f"{n} ≈ {v:+.0f} mV", p2(1.6, y(v) + (0.22 if k == 1 else (-0.08 if k == 2 else (-0.1 if k == 0 else 0)))), col, 16))
    f["u"] = txt("mV", p2(0, y(v1) + 0.3), P.muted, 15)
    return f


# ------------------------------------------------------------------ 13: potenziale d'azione (HH)
def ap_data():
    t, V, m, h, n, gNa, gK = N.hh(lambda tt: 12.0 if 2 <= tt < 3 else 0.0, 14.0, 0.005)
    return t, V, gNa, gK


def f13_ap(W=6.4, Hh=3.2):
    f = Fig()
    t, V, gNa, gK = ap_data()
    O = p2(-W / 2, -Hh / 2)
    yv = lambda v: (v + 90) / 140 * Hh
    f["ax"] = axes(O, W, Hh + 0.3, "t (ms)", "V (mV)")
    xs = t / t[-1] * W
    f["V"] = VMobject(color=P.fg, stroke_width=3.5).set_points_as_corners([O + p2(a, yv(v)) for a, v in zip(xs[::4], V[::4])])
    f["gNa"] = VMobject(color=P.S, stroke_width=2.5).set_points_as_corners([O + p2(a, g / 40 * Hh * 0.6) for a, g in zip(xs[::4], gNa[::4])])
    f["gK"] = VMobject(color=P.V, stroke_width=2.5).set_points_as_corners([O + p2(a, g / 40 * Hh * 0.6) for a, g in zip(xs[::4], gK[::4])])
    f["thr"] = DashedLine(O + p2(0, yv(-55)), O + p2(W, yv(-55)), color=P.muted, stroke_width=1.5)
    f["thl"] = txt(tr("threshold ≈ −55 mV", "soglia ≈ −55 mV"), O + p2(W - 1.0, yv(-55) + 0.18), P.muted, 14)
    f["l0"] = txt(tr("0 mV", "0 mV"), O + p2(-0.45, yv(0)), P.muted, 14)
    f["lNa"] = txt("g(Na⁺)", O + p2(xs[np.argmax(gNa)] + 0.75, np.max(gNa) / 40 * Hh * 0.6 + 0.05), P.S, 16)
    f["lK"] = txt("g(K⁺)", O + p2(xs[np.argmax(gK)] + 0.6, np.max(gK) / 40 * Hh * 0.6 - 0.15), P.V, 16)
    # fasi
    ph = [(2.2, -65, "1"), (2.9, -50, "2"), (3.6, 30, "3"), (4.4, -20, "4"), (5.4, -76, "5"), (9, -66, "6")]
    for k, (tt, v, s) in enumerate(ph):
        f[f"p{k}"] = VGroup(Circle(radius=0.14, color=P.C, fill_color=P.C, fill_opacity=1, stroke_width=0), txt(s, ORIGIN, P.bg, 14, weight="BOLD")).move_to(O + p2(tt / t[-1] * W, yv(v) + 0.3))
    return f


def f14_fI(W=6.0):
    f = Fig()
    cols = [P.muted, P.V, P.S]
    for k, I in enumerate((2.0, 6.5, 15.0)):
        t, V, *_ = N.hh(lambda tt, I=I: I if tt > 5 else 0.0, 80.0, 0.01)
        O = p2(-W / 2, 1.3 - 1.35 * k)
        xs = t / t[-1] * W
        f[f"v{k}"] = VMobject(color=cols[k], stroke_width=2.5).set_points_as_corners([O + p2(a, (v + 70) / 120 * 1.0) for a, v in zip(xs[::10], V[::10])])
        nsp = int(np.sum((V[1:] > 0) & (V[:-1] <= 0)))
        f[f"l{k}"] = txt(f"I = {I:g} µA/cm²  →  {nsp} spike", O + p2(W + 1.4, 0.35), cols[k], 16)
    f["note"] = txt(tr("below threshold: no spike · above: more current = more spikes, not bigger spikes",
                       "sotto soglia: niente spike · sopra: più corrente = più spike, non spike più grandi"), p2(0.9, -2.9), P.muted, 15)
    return f


# ------------------------------------------------------------------ 15: conduzione continua e saltatoria
def f15_conduction(W=8.0):
    f = Fig()
    for k, (y, lab, myel) in enumerate(((0.9, tr("unmyelinated: continuous, ≈0.5–2 m/s", "amielinico: continua, ≈0.5–2 m/s"), False),
                                        (-1.1, tr("myelinated: saltatory, up to ≈120 m/s", "mielinizzato: saltatoria, fino a ≈120 m/s"), True))):
        f[f"ax{k}"] = Line(p2(-W / 2, y), p2(W / 2, y), color=P.fg, stroke_width=3)
        if myel:
            for j in range(6):
                f[f"my{j}"] = RoundedRectangle(corner_radius=0.1, width=1.05, height=0.36, color=P.C, fill_color=P.C, fill_opacity=0.35, stroke_width=2).move_to(p2(-W / 2 + 0.7 + 1.3 * j, y))
        f[f"l{k}"] = txt(lab, p2(0, y + 0.55), P.S if myel else P.V, 18)
    return f


# ------------------------------------------------------------------ 17: sinapsi chimica
def f17_synapse():
    f = Fig()
    f["pre"] = VMobject(color=P.fg, stroke_width=3, fill_color=P.V, fill_opacity=0.15).set_points_smoothly(
        [p2(-0.6, 2.4), p2(-1.5, 1.2), p2(-1.4, 0.3), p2(0, 0.2), p2(1.4, 0.3), p2(1.5, 1.2), p2(0.6, 2.4)])
    f["post"] = VMobject(color=P.fg, stroke_width=3, fill_color=P.S, fill_opacity=0.12).set_points_smoothly(
        [p2(-2.0, -1.8), p2(-1.8, -0.35), p2(0, -0.25), p2(1.8, -0.35), p2(2.0, -1.8)])
    rng = np.random.default_rng(2)
    for k in range(7):
        c = p2(rng.uniform(-0.9, 0.9), rng.uniform(0.7, 1.6))
        f[f"v{k}"] = Circle(radius=0.17, color=P.C, fill_color=P.C, fill_opacity=0.3, stroke_width=2).move_to(c)
    for k, x in enumerate((-1.0, -0.35, 0.35, 1.0)):
        f[f"r{k}"] = RoundedRectangle(corner_radius=0.05, width=0.22, height=0.3, color=P.S, fill_color=P.S, fill_opacity=0.8, stroke_width=0).move_to(p2(x, -0.3))
    for k, x in enumerate((-1.25, 1.25)):
        f[f"ca{k}"] = RoundedRectangle(corner_radius=0.05, width=0.22, height=0.3, color=P.C, fill_color=P.C, fill_opacity=0.9, stroke_width=0).move_to(p2(x, 0.28))
    f["lpre"] = txt(tr("presynaptic terminal", "terminale presinaptico"), p2(0, 2.75), P.fg, 16)
    f["lpost"] = txt(tr("postsynaptic membrane", "membrana postsinaptica"), p2(0, -2.15), P.fg, 16)
    f["lca"] = txt(tr("Ca²⁺ channels", "canali Ca²⁺"), p2(2.3, 0.5), P.C, 15)
    f["lr"] = txt(tr("receptors", "recettori"), p2(2.4, -0.55), P.S, 15)
    f["lv"] = txt(tr("vesicles", "vescicole"), p2(-2.1, 1.3), P.C, 15)
    return f


# ------------------------------------------------------------------ 18: EPSP e IPSP
def f18_epsp_ipsp(W=6.0):
    f = Fig()
    t = np.linspace(0, 60, 600)
    for k, (s, col, lab, e) in enumerate(((1, P.S, "EPSP", tr("glutamate (AMPA): Na⁺ in → depolarization", "glutammato (AMPA): entra Na⁺ → depolarizzazione")),
                                          (-1, P.V, "IPSP", tr("GABA-A: Cl⁻ in → hyperpolarization", "GABA-A: entra Cl⁻ → iperpolarizzazione")))):
        O = p2(-W / 2, 0.9 - 2.1 * k)
        v = s * N.alpha_psp(t, 5, 6.0, 1.0)
        f[f"b{k}"] = DashedLine(O, O + p2(W, 0), color=P.aux, stroke_width=1.5)
        f[f"v{k}"] = VMobject(color=col, stroke_width=3.5).set_points_smoothly([O + p2(a / 60 * W, 0.8 * b) for a, b in zip(t[::6], v[::6])])
        f[f"l{k}"] = txt(lab, O + p2(-0.6, 0.35 * s), col, 20, weight="BOLD")
        f[f"e{k}"] = txt(e, O + p2(W / 2 + 0.4, -0.45 * s + (0.1 if s > 0 else 0)), P.fg, 15)
    f["sc"] = VGroup(Line(p2(W / 2 - 1.0, -2.35), p2(W / 2, -2.35), color=P.fg, stroke_width=3), txt("10 ms", p2(W / 2 - 0.5, -2.6), P.muted, 14))
    return f


# ------------------------------------------------------------------ 19-20: sommazione temporale e spaziale
def summation(rate_hz, T=200.0, dt=0.1, tau=15.0, w=8.0):
    """potenziale al monticolo (mV): EPSP a salto con decadimento tau, spike e reset a soglia -55 mV."""
    t = np.arange(0, T, dt)
    V = np.full(len(t), -70.0); isi = 1000.0 / rate_hz
    arr = set(np.round(np.arange(10, T, isi) / dt).astype(int)); sp = []
    for k in range(1, len(t)):
        V[k] = V[k - 1] - dt * (V[k - 1] + 70.0) / tau + (w if k in arr else 0.0)
        if V[k] >= -55.0:
            sp.append(k); V[k] = -75.0
    return t, V, sp


def f19_temporal(W=6.0):
    f = Fig()
    for k, (r, col) in enumerate(((25, P.V), (90, P.S))):
        t, V, sp = summation(r)
        O = p2(-W / 2, 0.8 - 2.2 * k)
        y = lambda v: (v + 72) / 22 * 1.4
        f[f"th{k}"] = DashedLine(O + p2(0, y(-55)), O + p2(W, y(-55)), color=P.muted, stroke_width=1.5)
        f[f"v{k}"] = VMobject(color=col, stroke_width=3).set_points_as_corners([O + p2(a / t[-1] * W, y(v)) for a, v in zip(t[::2], V[::2])])
        for j, i in enumerate(sp[:12]):
            x = t[i] / t[-1] * W
            f[f"s{k}_{j}"] = Line(O + p2(x, y(-55)), O + p2(x, y(-55) + 0.9), color=col, stroke_width=3)
        f[f"l{k}"] = txt(f"{r} Hz", O + p2(-0.55, 0.5), col, 18, weight="BOLD")
    f["thl"] = txt(tr("threshold", "soglia"), p2(W / 2 + 0.6, 0.8 + (15 / 22) * 1.4), P.muted, 14)
    return f


def f20_spatial():
    f = Fig()
    soma = p2(0, -0.6)
    f["cell"] = pyramidal(soma, 1.2)
    syn = [(p2(-0.5, 1.45), P.S, "+"), (p2(0.45, 1.3), P.S, "+"), (p2(0.55, -1.0), P.V, "−")]
    for k, (p, col, s) in enumerate(syn):
        f[f"s{k}"] = VGroup(Circle(radius=0.16, color=col, fill_color=col, fill_opacity=0.9, stroke_width=0), txt(s, ORIGIN, P.bg, 18, weight="BOLD")).move_to(p)
    f["hill"] = Circle(radius=0.12, color=P.C, fill_color=P.C, fill_opacity=1, stroke_width=0).move_to(soma + p2(0, -0.35))
    f["hl"] = txt(tr("axon hillock: Σ inputs ≥ threshold?", "monticolo: Σ input ≥ soglia?"), soma + p2(0.2, -1.55), P.C, 16)
    return f


# ------------------------------------------------------------------ 22: PSP vs spike: durata e decadimento del campo
def f22_decay(W=5.5):
    f = Fig()
    O = p2(-W / 2, -1.6)
    f["ax"] = axes(O, W, 3.3, tr("distance r", "distanza r"), tr("field amplitude", "ampiezza del campo"))
    r = np.linspace(0.35, 3.0, 100)
    d = (0.35 / r) ** 2; q = (0.35 / r) ** 3
    f["d"] = VMobject(color=P.S, stroke_width=4).set_points_smoothly([O + p2(x / 3.0 * W, 3.0 * v) for x, v in zip(r, d)])
    f["q"] = VMobject(color=P.V, stroke_width=4).set_points_smoothly([O + p2(x / 3.0 * W, 3.0 * v) for x, v in zip(r, q)])
    f["ld"] = txt(tr("PSP: dipole ∝ 1/r²", "PSP: dipolo ∝ 1/r²"), O + p2(3.6, 1.7), P.S, 17)
    f["lq"] = txt(tr("spike: quadrupole ∝ 1/r³", "spike: quadrupolo ∝ 1/r³"), O + p2(3.6, 1.2), P.V, 17)
    return f


# ------------------------------------------------------------------ 23: pozzo e sorgente di corrente
def f23_sinksource(deep=False):
    f = Fig()
    soma = p2(0, -1.0)
    f["cell"] = pyramidal(soma, 1.3)
    f["surf"] = Line(p2(-2.4, 1.7), p2(2.4, 1.7), color=P.muted, stroke_width=4)
    f["sl"] = txt(tr("cortical surface", "superficie corticale"), p2(1.6, 2.0), P.muted, 15)
    top = soma + p2(0, 1.6 * 1.3)
    sink = top if not deep else soma
    src = soma + p2(0, 0.2) if not deep else top
    f["sink"] = VGroup(Circle(radius=0.22, color=P.V, fill_color=P.V, fill_opacity=0.9, stroke_width=0), txt("−", ORIGIN, P.bg, 22, weight="BOLD")).move_to(sink + p2(-0.55, 0))
    f["src"] = VGroup(Circle(radius=0.22, color=P.S, fill_color=P.S, fill_opacity=0.9, stroke_width=0), txt("+", ORIGIN, P.bg, 22, weight="BOLD")).move_to(src + p2(-0.55, 0))
    # linee di corrente extracellulari (dal source al sink, fuori dalla cellula)
    for k, w in enumerate((0.9, 1.5, 2.1)):
        for s in (-1, 1):
            a = src + p2(0.25 * s, 0); b = sink + p2(0.25 * s, 0)
            f[f"c{k}{s}"] = ArcBetweenPoints(a, b, angle=(1 if s > 0 else -1) * (1.3 + 0.45 * k) * (1 if not deep else -1), color=P.C, stroke_width=2, stroke_opacity=0.8)
    return f


# ------------------------------------------------------------------ 25: anello talamo-corticale
def f25_loop():
    f = Fig()
    cx = p2(0, 1.6); tc = p2(-1.4, -1.2); trn = p2(1.4, -1.2)
    f["ctx"] = RoundedRectangle(corner_radius=0.2, width=3.4, height=0.8, color=P.S, fill_color=P.S, fill_opacity=0.25, stroke_width=2).move_to(cx)
    f["ctxl"] = txt(tr("cortex (pyramidal cells)", "corteccia (piramidali)"), cx, P.fg, 16)
    f["tc"] = VGroup(Circle(radius=0.5, color=P.V, fill_color=P.V, fill_opacity=0.3, stroke_width=2), txt("TC", ORIGIN, P.fg, 20, weight="BOLD")).move_to(tc)
    f["trn"] = VGroup(Circle(radius=0.5, color=PURP, fill_color=PURP, fill_opacity=0.3, stroke_width=2), txt("TRN", ORIGIN, P.fg, 18, weight="BOLD")).move_to(trn)
    f["a1"] = CurvedArrow(tc + p2(-0.2, 0.5), cx + p2(-1.2, -0.42), angle=-0.4, color=P.V, stroke_width=3, tip_length=0.18)
    f["a2"] = CurvedArrow(cx + p2(1.2, -0.42), trn + p2(0.2, 0.5), angle=-0.4, color=P.S, stroke_width=3, tip_length=0.18)
    f["a3"] = CurvedArrow(trn + p2(-0.5, -0.1), tc + p2(0.5, -0.1), angle=-0.6, color=PURP, stroke_width=3, tip_length=0.18)
    f["a4"] = CurvedArrow(tc + p2(0.5, 0.15), trn + p2(-0.5, 0.15), angle=-0.6, color=P.V, stroke_width=3, tip_length=0.18)
    f["l3"] = txt(tr("GABA (inhibition)", "GABA (inibizione)"), p2(0, -2.2), PURP, 15)
    f["l4"] = txt(tr("glutamate", "glutammato"), p2(0, -0.35), P.V, 15)
    f["sens"] = Arrow(tc + p2(-1.8, -0.6), tc + p2(-0.5, -0.15), buff=0, color=P.muted, stroke_width=3, tip_length=0.15)
    f["sl"] = txt(tr("sensory input", "input sensoriale"), tc + p2(-1.9, -0.9), P.muted, 14)
    return f


def tc_modes(T=600.0, dt=0.1):
    """tracciati schematici di un neurone TC: tonico (veglia) e burst (sonno)."""
    t = np.arange(0, T, dt)
    ton = -60 + 1.5 * np.sin(2 * np.pi * t / 90)
    for t0 in np.arange(20, T, 33):
        ton += 70 * np.exp(-0.5 * ((t - t0) / 0.5) ** 2)
    bur = -72 + 0 * t
    for c in (80, 330, 580):
        lts = 18 * np.exp(-0.5 * ((t - c - 15) / 12) ** 2)
        bur += lts
        for j in range(5):
            bur += 55 * np.exp(-0.5 * ((t - c - 5 - 3.5 * j) / 0.45) ** 2)
    return t, ton, bur


def f25_modes(W=6.0):
    f = Fig()
    t, ton, bur = tc_modes()
    for k, (v, col, lab) in enumerate(((ton, P.C, tr("tonic mode (wake, depolarized): relays input", "modo tonico (veglia, depolarizzato): trasmette l'input")),
                                       (bur, PURP, tr("burst mode (sleep, hyperpolarized): Ca²⁺ LTS + spike burst", "modo burst (sonno, iperpolarizzato): LTS Ca²⁺ + burst di spike")))):
        O = p2(-W / 2, 0.9 - 2.0 * k)
        f[f"v{k}"] = VMobject(color=col, stroke_width=2).set_points_as_corners([O + p2(a / t[-1] * W, (b + 72) / 90 * 1.4) for a, b in zip(t[::3], v[::3])])
        f[f"l{k}"] = txt(lab, O + p2(W / 2, -0.35), col, 16)
    f["sc"] = VGroup(Line(p2(W / 2 - 1.0, -2.3), p2(W / 2, -2.3), color=P.fg, stroke_width=3), txt("100 ms", p2(W / 2 - 0.5, -2.55), P.muted, 14))
    return f
