"""Figure della Lezione 3 (Cinematica). Stesse regole della Lezione 2: ogni f_xx() restituisce un Fig
con parti nominate; lo stesso disegno serve al .pptx (tema chiaro) e alle animazioni (tema scuro).
Il numero nel nome è quello della slide originale (come le tracce L3-xx.png)."""
import os as _os
_R = _os.environ.get("COURSE_ROOT") or _os.path.dirname(_os.path.abspath(__file__))
while not _os.path.exists(_os.path.join(_R, ".course_root")) and _os.path.dirname(_R) != _R:
    _R = _os.path.dirname(_R)
import sys, os
sys.path.insert(0, _R + "/common")
import numpy as np
import figs as F
from figs import (Fig, p2, vec, tex, txt, label_along, ang_arc, ang_label, right_mark, dline, ang, proj, axes3d)
from manim import (VGroup, VMobject, Arrow, Line, DashedLine, Arc, Dot, Circle, Ellipse, Polygon, MathTex,
                   ORIGIN, UP, DOWN, LEFT, RIGHT, PI, Axes, ParametricFunction)

P = F.P
set_theme = F.set_theme

# ---------------------------------------------------------------- utilità
def axes2(o=p2(-2.6, -1.7), L=3.0, col=None):
    """terna obliqua 'da lavagna': Z in alto, Y a destra, X verso chi guarda."""
    col = col or P.fg
    o = np.asarray(o, float)
    ends = {"X": o + p2(-1.35, -1.0) * L / 3.0, "Y": o + p2(3.1, -0.65) * L / 3.0, "Z": o + p2(0, 3.3) * L / 3.0}
    g = VGroup()
    for n, e in ends.items():
        g.add(Line(o, e, color=col, stroke_width=2.5))
        d = (e - o) / np.linalg.norm(e - o)
        g.add(tex(n, e + 0.28 * d, col, 0.75))
    g.add(tex("O", o + p2(0.05, -0.36), col, 0.75))
    return g

class Arco:
    """traiettoria curvilinea generica: arco di circonferenza percorso da sinistra a destra."""
    def __init__(self, c=p2(1.4, -2.4), R=4.2, a0=142, a1=35):
        self.c, self.R, self.a0, self.a1 = np.asarray(c, float), R, np.radians(a0), np.radians(a1)
    def P(self, phi): return self.c + self.R * np.array([np.cos(phi), np.sin(phi), 0])
    def T(self, phi): return np.array([np.sin(phi), -np.cos(phi), 0])          # verso del moto
    def N(self, phi): return -np.array([np.cos(phi), np.sin(phi), 0])          # verso il centro
    def curve(self, col=None, dashed=True, w=3):
        a = Arc(radius=self.R, start_angle=self.a1, angle=self.a0 - self.a1, arc_center=self.c,
                color=col or P.muted, stroke_width=w)
        return DashedVMobject(a) if dashed else a

def DashedVMobject(m, n=60):
    from manim import DashedVMobject as D
    return D(m, num_dashes=n, dashed_ratio=0.55)

def dot(p, col=None, r=0.07):
    return Dot(np.asarray(p, float), color=col or P.fg, radius=r)

# ---------------------------------------------------------------- moto rettilineo (6, 9, 11)
def _rett(kind):
    f = Fig()
    O = p2(-2.2, -1.6)
    f["axes"] = axes2(O, 3.0)
    d = np.array([1.0, 0.32, 0]); d /= np.linalg.norm(d)
    Q = O + p2(-0.4, 1.9)
    f["traj"] = Line(Q - 0.6 * d, Q + 6.4 * d, color=P.muted, stroke_width=3)
    f["C"] = tex("C", Q + 6.4 * d + p2(0.3, 0.1), P.muted, 0.75)
    A, B = Q + 1.2 * d, Q + 3.6 * d          # il corpo si muove nel verso di d
    f["A"] = dot(A, P.fg); f["Al"] = tex("A", A + p2(-0.1, 0.38), P.fg, 0.7)
    f["B"] = dot(B, P.fg); f["Bl"] = tex("B", B + p2(-0.1, 0.38), P.fg, 0.7)
    if kind == "v":
        f["dx"] = Line(A, B, color=P.V, stroke_width=9).set_opacity(0.8)
        f["dxl"] = tex(r"\Delta x", (A + B) / 2 + p2(0.1, -0.4), P.V, 0.8)
        f["vm"] = vec(B, B + 1.5 * d, P.S, w=6, tip=0.22)
        f["vml"] = tex(r"\boldsymbol{v}_{\mathrm{media}}", B + 0.9 * d + p2(0.2, -0.45), P.S, 0.8)
    else:
        L0, L1 = (0.9, 1.7) if kind == "acc" else (1.7, 0.8)
        f["v0"] = vec(A, A + L0 * d, P.V, w=6, tip=0.22)
        f["v0l"] = tex(r"\boldsymbol{v}_0", A + 0.5 * L0 * d + p2(0.1, -0.42), P.V, 0.8)
        f["v"] = vec(B, B + L1 * d, P.S, w=6, tip=0.22)
        f["vl"] = tex(r"\boldsymbol{v}", B + 0.5 * L1 * d + p2(0.1, -0.42), P.S, 0.8)
    return f

def f06_rett_v(): return _rett("v")
def f09_rett_acc(): return _rett("acc")
def f11_rett_dec(): return _rett("dec")

# ---------------------------------------------------------------- orari (12)
def f12_orari():
    f = Fig()
    ax = Axes(x_range=[0, 4.2, 1], y_range=[0, 5, 1], x_length=4.2, y_length=3.0,
              axis_config=dict(color=P.fg, stroke_width=2.5, include_ticks=False, tip_length=0.18))
    f["ax"] = ax
    f["t"] = tex("t", ax.c2p(4.2, 0) + p2(0.2, -0.2), P.fg, 0.8)
    f["x"] = tex("x", ax.c2p(0, 5) + p2(-0.25, 0.1), P.fg, 0.8)
    f["uni"] = ax.plot(lambda t: 0.8 + 0.75 * t, x_range=[0, 4], color=P.V, stroke_width=5)
    f["acc"] = ax.plot(lambda t: 0.8 + 0.2 * t + 0.22 * t * t, x_range=[0, 4], color=P.S, stroke_width=5)
    f["x0"] = tex("x_0", ax.c2p(0, 0.8) + p2(-0.35, 0), P.fg, 0.7)
    f["unil"] = tex(r"\text{uniforme}", ax.c2p(3.1, 2.4) + p2(0.8, -0.3), P.V, 0.62)
    f["accl"] = tex(r"\text{unif. accelerato}", ax.c2p(2.6, 4.6) + p2(-0.6, 0.1), P.S, 0.62)
    return f

# ---------------------------------------------------------------- moto curvilineo: spostamento (14)
ARC = Arco()
PA, PB = np.radians(118), np.radians(80)

def f14_spost(tri=True):
    f = Fig()
    O = p2(-2.6, -1.7)
    f["axes"] = axes2(O, 3.0)
    f["C"] = ARC.curve(); f["Cl"] = tex("C", ARC.P(ARC.a1) + p2(0.3, 0.0), P.muted, 0.75)
    A, B = ARC.P(PA), ARC.P(PB)
    f["r"] = vec(O, A, P.V, w=5, tip=0.2); f["rl"] = label_along(O, A, r"\boldsymbol{r}", P.V, 1, 0.3, 0.8, 0.6)
    f["r2"] = vec(O, B, P.V, w=5, tip=0.2); f["r2l"] = label_along(O, B, r"\boldsymbol{r}'", P.V, -1, 0.3, 0.8, 0.6)
    arc = Arc(radius=ARC.R, start_angle=PB, angle=PA - PB, arc_center=ARC.c, color=P.C, stroke_width=6)
    f["ds"] = arc; f["dsl"] = tex(r"\Delta s", ARC.P((PA + PB) / 2) + 0.35 * -ARC.N((PA + PB) / 2), P.C, 0.75)
    f["dr"] = vec(A, B, P.S, w=6, tip=0.22); f["drl"] = label_along(A, B, r"\Delta\boldsymbol{r}", P.S, -1, 0.32, 0.8)
    u = (B - A) / np.linalg.norm(B - A)
    f["vm"] = vec(B, B + 1.1 * u, P.S, w=5, tip=0.2)
    f["vml"] = tex(r"\boldsymbol{v}_{\mathrm{media}}", B + 1.0 * u + p2(0.3, 0.35), P.S, 0.7)
    f["Ad"] = dot(A); f["Al"] = tex("A", A + p2(-0.05, 0.35), P.fg, 0.7)
    f["Bd"] = dot(B); f["Bl"] = tex("B", B + p2(0.05, 0.35), P.fg, 0.7)
    if tri:
        q = p2(4.7, -1.7); k = 0.55
        f["t_r2"] = vec(q, q + k * (B - O), P.V, w=4, tip=0.16)
        f["t_mr"] = vec(q + k * (B - O), q + k * (B - A), P.muted, w=4, tip=0.16)
        f["t_dr"] = vec(q, q + k * (B - A), P.S, w=5, tip=0.18)
        f["t_r2l"] = label_along(q, q + k * (B - O), r"\boldsymbol{r}'", P.V, 1, 0.3, 0.7)
        f["t_mrl"] = label_along(q + k * (B - O), q + k * (B - A), r"-\boldsymbol{r}", P.muted, 1, 0.35, 0.7)
        f["t_drl"] = label_along(q, q + k * (B - A), r"\Delta\boldsymbol{r}", P.S, -1, 0.3, 0.7)
    return f

# ---------------------------------------------------------------- secante -> tangente (15)
def f15_tangente(n=3):
    f = Fig()
    A = p2(-3.0, -1.5)
    def curve(s):   # curva generica concava verso il basso
        return A + p2(s, 0.95 * s - 0.11 * s * s)
    pts = [curve(s) for s in np.linspace(-0.6, 6.2, 60)]
    f["C"] = VMobject(color=P.muted, stroke_width=3).set_points_smoothly(pts)
    tdir = p2(1, 0.95); tdir /= np.linalg.norm(tdir)
    f["T"] = dline(A - 0.7 * tdir, A + 4.6 * tdir, P.aux, w=2)
    f["Tl"] = tex("T", A + 4.75 * tdir + p2(-0.15, 0.2), P.aux, 0.75)
    ss = [5.4, 3.6, 2.0][:n]
    names = ["B", "B'", "B''"]
    for i, s in enumerate(ss):
        B = curve(s); u = (B - A) / np.linalg.norm(B - A)
        f[f"dr{i}"] = vec(A, B, P.C, w=4, tip=0.17)
        f[f"vm{i}"] = vec(B, B + 0.9 * u, P.S, w=4, tip=0.17)
        f[f"B{i}"] = dot(B); f[f"Bl{i}"] = tex(names[i], B + p2(0.1, -0.35), P.fg, 0.65)
    f["drl"] = label_along(A, curve(5.4), r"\Delta\boldsymbol{r}", P.C, -1, 0.3, 0.75, 0.55)
    f["vml"] = tex(r"\boldsymbol{v}_{\mathrm{media}}", curve(5.4) + 0.9 * (curve(5.4) - A) / np.linalg.norm(curve(5.4) - A) + p2(0.2, 0.35), P.S, 0.7)
    f["v"] = vec(A, A + 1.6 * tdir, P.V, w=7, tip=0.24)
    f["vl"] = tex(r"\boldsymbol{v}", A + 0.8 * tdir + p2(-0.3, 0.25), P.V, 0.85)
    f["uT"] = vec(A + p2(-0.9, 0.2), A + p2(-0.9, 0.2) + 0.7 * tdir, P.V, w=4, tip=0.16)
    f["uTl"] = tex(r"\boldsymbol{u}_T", A + p2(-1.05, 0.95), P.V, 0.7)
    f["A"] = dot(A); f["Al"] = tex("A", A + p2(0.1, -0.35), P.fg, 0.7)
    return f

# ---------------------------------------------------------------- componenti della velocità (18)
def f18_vcomp():
    f = Fig()
    O = p2(-2.6, -1.7)
    f["axes"] = axes2(O, 3.0)
    f["C"] = ARC.curve(); f["Cl"] = tex("C", ARC.P(ARC.a1) + p2(0.3, 0.0), P.muted, 0.75)
    ph = np.radians(108); A = ARC.P(ph); B = ARC.P(ph - 0.12)
    f["r"] = vec(O, A, P.V, w=5, tip=0.2); f["rl"] = label_along(O, A, r"\boldsymbol{r}", P.V, 1, 0.3, 0.8, 0.55)
    f["r2"] = vec(O, B, P.V, w=4, tip=0.2); f["r2l"] = label_along(O, B, r"\boldsymbol{r}'", P.V, -1, 0.3, 0.75, 0.6)
    f["drl"] = tex(r"d\boldsymbol{r}\;(ds)", A + p2(0.3, 0.55), P.C, 0.7)
    t = ARC.T(ph)
    f["v"] = vec(A, A + 1.5 * t, P.S, w=7, tip=0.24); f["vl"] = tex(r"\boldsymbol{v}", A + 1.5 * t + p2(0.25, 0.25), P.S, 0.85)
    # componenti sugli assi (lunghezze indicative)
    ex, ey, ez = p2(-1.35, -1.0) / 3, p2(3.1, -0.65) / 3, p2(0, 3.3) / 3
    f["vx"] = vec(O, O + 1.0 * ex * 2.2, P.C, w=5, tip=0.18); f["vxl"] = tex("v_x", O + ex * 2.2 + p2(-0.1, 0.3), P.C, 0.7)
    f["vy"] = vec(O, O + 1.0 * ey * 1.8, P.C, w=5, tip=0.18); f["vyl"] = tex("v_y", O + ey * 1.8 + p2(0, -0.35), P.C, 0.7)
    f["vz"] = vec(O, O + 1.0 * ez * 1.2, P.C, w=5, tip=0.18); f["vzl"] = tex("v_z", O + ez * 1.2 + p2(-0.35, 0), P.C, 0.7)
    f["Ad"] = dot(A)
    return f

# ---------------------------------------------------------------- accelerazione media e istantanea (20, 21)
def f20_amed(phA=np.radians(122), phB=np.radians(78), side=True, inst=False):
    f = Fig()
    O = p2(-2.6, -1.7)
    f["axes"] = axes2(O, 3.0)
    f["C"] = ARC.curve(); f["Cl"] = tex("C", ARC.P(ARC.a1) + p2(0.3, 0.0), P.muted, 0.75)
    A, B = ARC.P(phA), ARC.P(phB)
    f["r"] = vec(O, A, P.V, w=4, tip=0.18); f["rl"] = label_along(O, A, r"\boldsymbol{r}", P.V, 1, 0.3, 0.75, 0.55)
    f["r2"] = vec(O, B, P.V, w=4, tip=0.18); f["r2l"] = label_along(O, B, r"\boldsymbol{r}'", P.V, -1, 0.3, 0.75, 0.55)
    vA, vB = 1.5 * ARC.T(phA), 1.5 * ARC.T(phB)
    f["vA"] = vec(A, A + vA, P.S, w=6, tip=0.22); f["vAl"] = tex(r"\boldsymbol{v}", A + vA + p2(0.1, 0.3), P.S, 0.8)
    f["vB"] = vec(B, B + vB, P.S, w=6, tip=0.22); f["vBl"] = tex(r"\boldsymbol{v}'", B + vB + p2(0.35, 0.05), P.S, 0.8)
    dv = vB - vA
    lab = r"\boldsymbol{a}" if inst else r"\boldsymbol{a}_{\mathrm{med}}"
    base = A if inst else (A + B) / 2 + 0.25 * ARC.N((phA + phB) / 2)
    f["a"] = vec(base, base + 1.0 * dv / np.linalg.norm(dv), P.C, w=6, tip=0.22)
    f["al"] = tex(lab, base + 1.0 * dv / np.linalg.norm(dv) + p2(0.45, -0.1), P.C, 0.8)
    f["Ad"] = dot(A); f["Bd"] = dot(B)
    if side:
        q = p2(4.7, 1.6)
        f["t_v"] = vec(q, q + vA, P.S, w=4, tip=0.18); f["t_vl"] = label_along(q, q + vA, r"\boldsymbol{v}", P.S, 1, 0.3, 0.7)
        f["t_v2"] = vec(q, q + vB, P.S, w=4, tip=0.18); f["t_v2l"] = label_along(q, q + vB, r"\boldsymbol{v}'", P.S, -1, 0.3, 0.7)
        f["t_dv"] = vec(q + vA, q + vB, P.C, w=5, tip=0.18)
        f["t_dvl"] = label_along(q + vA, q + vB, r"d\boldsymbol{v}" if inst else r"\Delta\boldsymbol{v}", P.C, 1, 0.35, 0.75)
    return f

def f21_ainst(): return f20_amed(np.radians(110), np.radians(102), True, True)

def f22_acomp():
    f = f20_amed(np.radians(110), np.radians(102), False, True)
    O = p2(-2.6, -1.7)
    ex, ey, ez = p2(-1.35, -1.0) / 3, p2(3.1, -0.65) / 3, p2(0, 3.3) / 3
    f["ax"] = vec(O, O + ex * 1.6, P.C, w=4, tip=0.16); f["axl"] = tex("a_x", O + ex * 1.6 + p2(-0.1, 0.3), P.C, 0.7)
    f["ay"] = vec(O, O + ey * 0.9, P.C, w=4, tip=0.16); f["ayl"] = tex("a_y", O + ey * 0.9 + p2(0.05, -0.35), P.C, 0.7)
    f["az"] = vec(O, O + ez * 0.5, P.C, w=4, tip=0.14); f["azl"] = tex("a_z", O + ez * 0.5 + p2(-0.4, 0), P.C, 0.7)
    return f

# ---------------------------------------------------------------- componenti tangenziale e normale (26, 27, 34)
def f26_aTaN(versori=False, ph=np.radians(98)):
    f = Fig()
    arc = Arco(c=p2(0, -3.2), R=4.2, a0=140, a1=40)
    f["C"] = arc.curve(); f["Cl"] = tex("C", arc.P(arc.a1) + p2(0.3, -0.1), P.muted, 0.75)
    Pp = arc.P(ph); t, n = arc.T(ph), arc.N(ph)
    aT, aN = 1.6 * t, 1.3 * n
    f["aT"] = vec(Pp, Pp + aT, P.V, w=6, tip=0.22); f["aTl"] = tex(r"\boldsymbol{a}_T", Pp + aT + 0.3 * t + p2(0, 0.2), P.V, 0.85)
    f["aN"] = vec(Pp, Pp + aN, P.V, w=6, tip=0.22); f["aNl"] = tex(r"\boldsymbol{a}_N", Pp + aN + p2(-0.45, -0.05), P.V, 0.85)
    f["d1"] = dline(Pp + aT, Pp + aT + aN); f["d2"] = dline(Pp + aN, Pp + aT + aN)
    f["a"] = vec(Pp, Pp + aT + aN, P.S, w=7, tip=0.24); f["al"] = tex(r"\boldsymbol{a}", Pp + aT + aN + p2(0.3, -0.15), P.S, 0.9)
    f["ra"] = right_mark(Pp, t, n, 0.2, P.fg)
    if versori:
        f["uT"] = vec(Pp - 0.9 * n, Pp - 0.9 * n + 0.7 * t, P.C, w=4, tip=0.16)
        f["uTl"] = tex(r"\boldsymbol{u}_T", Pp - 0.9 * n + 0.8 * t + p2(0.1, 0.25), P.C, 0.7)
        f["uN"] = vec(Pp - 0.9 * n, Pp - 0.9 * n + 0.7 * n, P.C, w=4, tip=0.16)
        f["uNl"] = tex(r"\boldsymbol{u}_N", Pp - 0.9 * n + p2(-0.45, -0.35), P.C, 0.7)
    f["P"] = dot(Pp, P.S, 0.09)
    return f

def f27_versori(): return f26_aTaN(True)

# ---------------------------------------------------------------- raggio di curvatura (28)
def f28_curvatura():
    f = Fig()
    def y(x): return 0.9 * np.sin(1.25 * x) + 0.12 * x
    pts = [p2(x, y(x)) for x in np.linspace(-3.4, 3.4, 120)]
    f["C"] = VMobject(color=P.fg, stroke_width=4).set_points_smoothly(pts)
    f["Cl"] = tex("C", p2(3.6, y(3.4) + 0.1), P.fg, 0.75)
    def osc(x0):
        h = 1e-3
        y1 = (y(x0 + h) - y(x0 - h)) / (2 * h); y2 = (y(x0 + h) - 2 * y(x0) + y(x0 - h)) / h ** 2
        R = (1 + y1 ** 2) ** 1.5 / abs(y2)
        n = np.array([-y1, 1, 0]) / np.sqrt(1 + y1 ** 2) * np.sign(y2)
        return p2(x0, y(x0)), R, n
    x1 = np.pi / 2 / 1.25; x2 = -np.pi / 2 / 1.25 + 0.05
    for k, x0, col in [(1, x1, P.V), (2, x2, P.S)]:
        Pp, R, n = osc(x0)
        c = Pp + R * n
        R2 = R if k == 1 else R * 1.9    # secondo punto: curvatura minore (raggio maggiore) per il confronto
        c = Pp + R2 * n
        f[f"circ{k}"] = Circle(radius=R2, color=col, fill_opacity=0.18, stroke_width=3).move_to(c)
        f[f"rad{k}"] = vec(c, Pp, col, w=4, tip=0.16)
        f[f"Rl{k}"] = tex(f"R_{k}", c + 0.5 * (Pp - c) + p2(0.3, 0.1), col, 0.75)
        f[f"P{k}"] = dot(Pp, col, 0.08); f[f"Pl{k}"] = tex(f"P_{k}", Pp - 0.4 * n, col, 0.75)
    return f

# ---------------------------------------------------------------- variazione del versore tangente (31)
def f31_duT():
    f = Fig()
    arc = Arco(c=p2(-0.6, -3.6), R=4.6, a0=152, a1=40)
    f["C"] = arc.curve(); f["Cl"] = tex("C", arc.P(arc.a1) + p2(0.3, 0.0), P.muted, 0.75)
    ph1, ph2 = np.radians(140), np.radians(114)
    A, B = arc.P(ph1), arc.P(ph2); t1, t2 = arc.T(ph1), arc.T(ph2)
    L = 1.3
    f["T1"] = dline(A - 1.2 * t1, A + 2.2 * t1, P.aux, w=2); f["T2"] = dline(B - 1.2 * t2, B + 2.2 * t2, P.aux, w=2)
    f["u1"] = vec(A, A + L * t1, P.V, w=6, tip=0.22); f["u1l"] = tex(r"\boldsymbol{u}_T", A + L * t1 + p2(-0.1, 0.35), P.V, 0.8)
    f["u2"] = vec(B, B + L * t2, P.S, w=6, tip=0.22); f["u2l"] = tex(r"\boldsymbol{u}_T'", B + L * t2 + p2(0.1, 0.42), P.S, 0.8)
    # riferimento orizzontale (parallelo all'asse X) in ciascun punto
    a1, a2 = ang(t1), ang(t2)
    f["h1"] = dline(A, A + p2(1.6, 0), P.aux, w=1.8); f["h2"] = dline(B, B + p2(1.6, 0), P.aux, w=1.8)
    f["al1"] = ang_arc(A, 0.8, 0, a1, P.V); f["al1l"] = ang_label(A, 1.1, 0, a1, r"\alpha", P.V)
    f["al2"] = ang_arc(B, 1.1, 0, a2, P.S); f["al2l"] = ang_label(B, 1.45, 0, a2, r"\alpha'", P.S)
    f["Xr"] = Arrow(p2(-4.4, -2.4), p2(-2.9, -2.4), buff=0, color=P.muted, stroke_width=2.5, tip_length=0.16, max_tip_length_to_length_ratio=0.2)
    f["Xl"] = tex(r"X", p2(-2.65, -2.4), P.muted, 0.7)
    # triangolo dei versori
    q = p2(3.2, 1.2)
    f["t1"] = vec(q, q + L * t1, P.V, w=4, tip=0.18); f["t2"] = vec(q, q + L * t2, P.S, w=4, tip=0.18)
    f["tdu"] = vec(q + L * t1, q + L * t2, P.C, w=5, tip=0.16)
    f["tdul"] = tex(r"d\boldsymbol{u}_T", q + L * (t1 + t2) / 2 + p2(0.45, 0.25), P.C, 0.7)
    f["tdal"] = ang_arc(q, 0.6, a2, a1, P.fg); f["tdall"] = ang_label(q, 0.9, a2, a1, r"d\alpha", P.fg, 0.6)
    return f

# ---------------------------------------------------------------- arco ds e raggio di curvatura (32)
def f32_ds():
    f = Fig()
    c = p2(-1.4, -2.6); R = 4.4
    a1, a2 = np.radians(64), np.radians(48)
    f["C"] = DashedVMobject(Arc(radius=R, start_angle=np.radians(30), angle=np.radians(70), arc_center=c, color=P.muted, stroke_width=3))
    A, B = c + R * p2(np.cos(a1), np.sin(a1)), c + R * p2(np.cos(a2), np.sin(a2))
    f["rA"] = Line(c, A, color=P.V, stroke_width=3); f["rB"] = Line(c, B, color=P.V, stroke_width=3)
    f["rhol"] = label_along(c, A, r"\rho", P.V, 1, 0.3, 0.9, 0.5)
    f["ds"] = Arc(radius=R, start_angle=a2, angle=a1 - a2, arc_center=c, color=P.S, stroke_width=8)
    f["dsl"] = tex("ds", c + (R - 0.45) * p2(np.cos((a1 + a2) / 2), np.sin((a1 + a2) / 2)), P.S, 0.85)
    f["da"] = ang_arc(c, 1.1, a2, a1, P.fg); f["dal"] = ang_label(c, 1.5, a2, a1, r"d\alpha", P.fg, 0.75)
    f["c"] = dot(c)
    tA = p2(np.sin(a1), -np.cos(a1)); tB = p2(np.sin(a2), -np.cos(a2))
    f["uA"] = vec(A, A + 1.1 * tA, P.C, w=5, tip=0.18); f["uAl"] = tex(r"\boldsymbol{u}_T", A + 1.1 * tA + p2(0.1, 0.38), P.C, 0.7)
    f["uB"] = vec(B, B + 1.1 * tB, P.C, w=5, tip=0.18); f["uBl"] = tex(r"\boldsymbol{u}_T'", B + 1.1 * tB + p2(0.45, 0.05), P.C, 0.7)
    return f

# ---------------------------------------------------------------- moto circolare (37, 39, 40, 45)
def circ3(az=28, el=22, R=2.3):
    return [proj(R * np.cos(t), R * np.sin(t), 0, az, el) for t in np.linspace(0, 2 * PI, 90)]

def f37_arco(az=28, el=22, R=2.8, thA=np.radians(55), thB=np.radians(115)):
    f = Fig()
    f["axes"] = axes3d(L=3.6, az=az, el=el, col=P.muted)
    f["O"] = tex("O", p2(-0.35, 0.12), P.muted, 0.7)
    f["circ"] = VMobject(color=P.fg, stroke_width=3).set_points_smoothly(circ3(az, el, R))
    A = proj(R * np.cos(thA), R * np.sin(thA), 0, az, el); B = proj(R * np.cos(thB), R * np.sin(thB), 0, az, el)
    f["RA"] = vec(ORIGIN, A, P.V, w=5, tip=0.2); f["RAl"] = label_along(ORIGIN, A, "R", P.V, -1, 0.3, 0.8, 0.6)
    f["RB"] = vec(ORIGIN, B, P.V, w=4, tip=0.2)
    pts = [proj(R * np.cos(t), R * np.sin(t), 0, az, el) for t in np.linspace(thA, thB, 30)]
    f["s"] = VMobject(color=P.S, stroke_width=7).set_points_smoothly(pts)
    m = proj((R + 0.35) * np.cos((thA + thB) / 2), (R + 0.35) * np.sin((thA + thB) / 2), 0, az, el)
    f["sl"] = tex("s", m, P.S, 0.85)
    f["chord"] = vec(A, B, P.C, w=4, tip=0.16); f["chl"] = label_along(A, B, r"\boldsymbol{r}", P.C, 1, 0.28, 0.75)
    pts = [proj(0.7 * np.cos(t), 0.7 * np.sin(t), 0, az, el) for t in np.linspace(thA, thB, 20)]
    f["th"] = VMobject(color=P.fg, stroke_width=3).set_points_smoothly(pts)
    f["thl"] = tex(r"\theta", proj(1.35 * np.cos((thA + thB) / 2), 1.35 * np.sin((thA + thB) / 2), 0, az, el), P.fg, 0.8)
    f["A"] = dot(A, P.S); f["Al"] = tex("A", A + p2(0.3, -0.05), P.fg, 0.7)
    f["B"] = dot(B, P.S); f["Bl"] = tex("B", B + p2(0.05, 0.32), P.fg, 0.7)
    return f

def f39_omega(az=28, el=22, R=2.3, th=np.radians(60), cross=False):
    f = Fig()
    f["axes"] = axes3d(L=3.0, az=az, el=el, col=P.muted)
    f["O"] = tex("O", p2(-0.3, -0.25), P.muted, 0.7)
    f["circ"] = VMobject(color=P.fg, stroke_width=3).set_points_smoothly(circ3(az, el, R))
    Pp = proj(R * np.cos(th), R * np.sin(th), 0, az, el)
    f["r"] = vec(ORIGIN, Pp, P.V, w=6, tip=0.22); f["rl"] = label_along(ORIGIN, Pp, r"\boldsymbol{r}", P.V, -1, 0.3, 0.85)
    t3 = np.array([-np.sin(th), np.cos(th), 0])
    V = Pp + proj(*(1.4 * t3), az=az, el=el)
    f["v"] = vec(Pp, V, P.S, w=6, tip=0.22); f["vl"] = tex(r"\boldsymbol{v}", V + p2(0.25, 0.2), P.S, 0.85)
    W = proj(0, 0, 2.2, az, el)
    f["w"] = vec(ORIGIN, W, P.C, w=7, tip=0.24); f["wl"] = tex(r"\boldsymbol{\omega}", W + p2(-0.35, 0), P.C, 0.9)
    pts = [proj(0.45 * np.cos(t), 0.45 * np.sin(t), 1.2, az, el) for t in np.linspace(0, np.radians(290), 40)]
    rot = VMobject(color=P.C, stroke_width=3.5).set_points_smoothly(pts[:-3])
    rot.add(Arrow(pts[-5], pts[-1], buff=0, color=P.C, stroke_width=3.5, tip_length=0.16, max_tip_length_to_length_ratio=1))
    f["rot"] = rot
    f["P"] = dot(Pp, P.S)
    return f

def f45_centripeta(R=2.4, n=6):
    f = Fig()
    f["circ"] = Circle(radius=R, color=P.fg, stroke_width=3)
    f["c"] = dot(ORIGIN)
    for k in range(n):
        th = 2 * PI * k / n + 0.3
        Pp = R * p2(np.cos(th), np.sin(th)); t = p2(-np.sin(th), np.cos(th))
        f[f"v{k}"] = vec(Pp, Pp + 1.1 * t, P.S, w=5, tip=0.18)
        f[f"a{k}"] = vec(Pp, Pp - 0.95 * Pp / R, P.V, w=5, tip=0.18)
        f[f"p{k}"] = dot(Pp)
    f["vl"] = tex(r"\boldsymbol{v}", R * p2(np.cos(0.3), np.sin(0.3)) + 1.1 * p2(-np.sin(0.3), np.cos(0.3)) + p2(0.3, 0.1), P.S, 0.85)
    f["al"] = tex(r"\boldsymbol{a}_N", R * p2(np.cos(0.3), np.sin(0.3)) * 0.55 + p2(0.1, -0.3), P.V, 0.8)
    return f

# ---------------------------------------------------------------- moto con a costante: parabola (25)
def f25_parabola(n=7):
    f = Fig()
    g = 0.55; v0 = p2(1.2, 1.9); r0 = p2(-3.2, -1.6)
    def r(t): return r0 + v0 * t + 0.5 * p2(0, -g) * t * t
    T = 2 * v0[1] / g
    pts = [r(t) for t in np.linspace(0, T, 80)]
    f["traj"] = VMobject(color=P.muted, stroke_width=3).set_points_smoothly(pts)
    f["ground"] = Line(r0 + p2(-0.5, 0), r(T) + p2(0.6, 0), color=P.fg, stroke_width=2.5)
    f["v0"] = vec(r0, r0 + 0.75 * v0, P.V, w=6, tip=0.22); f["v0l"] = tex(r"\boldsymbol{v}_0", r0 + 0.75 * v0 + p2(-0.35, 0.1), P.V, 0.85)
    f["r0"] = dot(r0); f["r0l"] = tex(r"\boldsymbol{r}_0", r0 + p2(0, -0.35), P.fg, 0.75)
    for k, t in enumerate(np.linspace(T * 0.2, T * 0.85, 4)):
        p = r(t); v = v0 + p2(0, -g) * t
        f[f"vv{k}"] = vec(p, p + 0.55 * v, P.S, w=4, tip=0.16)
        f[f"aa{k}"] = vec(p, p + p2(0, -0.8), P.C, w=4, tip=0.16)
        f[f"d{k}"] = dot(p)
    f["al"] = tex(r"\boldsymbol{a}", r(T * 0.2) + p2(0.3, -0.6), P.C, 0.8)
    f["vl"] = tex(r"\boldsymbol{v}", r(T * 0.2) + 0.55 * (v0 + p2(0, -g) * T * 0.2) + p2(0.25, 0.1), P.S, 0.8)
    return f
