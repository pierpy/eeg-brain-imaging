"""Figure della Lezione 2 (Vettori) costruite con Manim.

Ogni funzione f_xx() restituisce un Fig: un dizionario ordinato di parti con nome
(così la presentazione animata può animarle una a una) che si assembla con .group().
Le stesse funzioni generano le immagini statiche del .pptx (tema chiaro) e le
animazioni manim-slides (tema scuro): il disegno è unico, cambia solo la palette.
"""
import re
import numpy as np
from manim import (VGroup, VMobject, Arrow, Line, DashedLine, Arc, Dot, Circle, Polygon,
                   MathTex, Text, CurvedArrow, ORIGIN, UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR, PI,
                   Axes, config)

# ----------------------------------------------------------------- palette
class Pal:
    def __init__(self, dark):
        self.dark = dark
        if dark:
            self.bg = "#16213A"; self.fg = "#E6EAF3"; self.muted = "#98A2B3"
            self.S = "#F07A3F"       # vettore protagonista / risultante (arancione)
            self.V = "#4FC3D6"       # vettori secondari (teal chiaro su fondo scuro)
            self.C = "#F5B041"       # componenti / vettori di appoggio (ambra)
            self.aux = "#7C8699"     # costruzioni ausiliarie
            self.fill = "#E4622B"
        else:
            self.bg = "#FFFFFF"; self.fg = "#16213A"; self.muted = "#6B7280"
            self.S = "#E4622B"; self.V = "#1F7A8C"; self.C = "#C2410C"
            self.aux = "#98A2B3"; self.fill = "#E4622B"

P = Pal(dark=True)

def set_theme(dark):
    global P
    P.__init__(dark)

# ----------------------------------------------------------------- helpers
class Fig(dict):
    def group(self):
        return VGroup(*self.values())

def p2(x, y):
    return np.array([x, y, 0.0])

def vec(a, b, col=None, w=6, tip=0.26):
    a, b = np.asarray(a, float), np.asarray(b, float)
    L = np.linalg.norm(b - a)
    return Arrow(a, b, buff=0, color=col or P.V, stroke_width=w,
                 max_tip_length_to_length_ratio=min(0.35, tip / max(L, 1e-6) * 1.0 + 0.0),
                 max_stroke_width_to_length_ratio=100, tip_length=tip)

def tex(s, pos=ORIGIN, col=None, sc=0.8):
    s = re.sub(r"(\\boldsymbol\{[A-Za-z]\})_", r"\1\\!_", s)
    return MathTex(s, color=col or P.fg).scale(sc).move_to(pos)

def txt(s, pos=ORIGIN, col=None, sz=26, slant="NORMAL"):
    return Text(s, font="Carlito", color=col or P.fg, font_size=sz, slant=slant).move_to(pos)

def label_along(a, b, s, col, side=1, off=0.32, sc=0.8, t=0.5):
    """etichetta al punto t del segmento a->b, spostata a sinistra (side=1) o a destra (-1)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = b - a; n = np.array([-d[1], d[0], 0]); n /= np.linalg.norm(n)
    return tex(s, a + t * d + side * off * n, col, sc)

def ang_arc(center, r, a0, a1, col=None, w=3):
    return Arc(radius=r, start_angle=a0, angle=a1 - a0, arc_center=np.asarray(center, float),
               color=col or P.fg, stroke_width=w)

def ang_label(center, r, a0, a1, s, col=None, sc=0.7):
    m = (a0 + a1) / 2
    return tex(s, np.asarray(center, float) + r * np.array([np.cos(m), np.sin(m), 0]), col or P.fg, sc)

def right_mark(corner, u1, u2, s=0.2, col=None):
    c = np.asarray(corner, float); u1 = np.asarray(u1, float); u2 = np.asarray(u2, float)
    u1 = u1 / np.linalg.norm(u1); u2 = u2 / np.linalg.norm(u2)
    return VMobject(color=col or P.fg, stroke_width=2.5).set_points_as_corners(
        [c + s * u1, c + s * (u1 + u2), c + s * u2])

def dline(a, b, col=None, w=2.5, dash=0.12):
    return DashedLine(np.asarray(a, float), np.asarray(b, float), color=col or P.aux,
                      stroke_width=w, dash_length=dash)

def ang(v):
    return np.arctan2(v[1], v[0])

# proiezione ortografica per le figure 3D (azimut/elevazione in gradi)
def proj(x, y, z, az=28, el=22, s=1.0):
    a, e = np.radians(az), np.radians(el)
    right = np.array([-np.sin(a), np.cos(a), 0])
    up = np.array([-np.cos(a) * np.sin(e), -np.sin(a) * np.sin(e), np.cos(e)])
    v = np.array([x, y, z], float)
    return s * np.array([v @ right, v @ up, 0.0])

def axes3d(o=ORIGIN, L=2.6, az=28, el=22, col=None, labels=True, w=3):
    col = col or P.fg
    o = np.asarray(o, float)
    g = VGroup()
    for (d, n) in [((L, 0, 0), "X"), ((0, L, 0), "Y"), ((0, 0, L), "Z")]:
        end = o + proj(*d, az=az, el=el)
        g.add(Arrow(o, end, buff=0, color=col, stroke_width=w, tip_length=0.2,
                    max_tip_length_to_length_ratio=0.1))
        if labels:
            dd = end - o; dd /= np.linalg.norm(dd)
            g.add(tex(n, end + 0.3 * dd, col, 0.8))
    return g

# ----------------------------------------------------------------- figure
def f05_axis():
    f = Fig()
    f["line"] = Arrow(p2(-4, 0), p2(4, 0), buff=0, color=P.fg, stroke_width=4, tip_length=0.28,
                      max_tip_length_to_length_ratio=0.05)
    f["O"] = Dot(p2(-0.5, 0), color=P.S, radius=0.09)
    f["Olab"] = tex("O", p2(-0.5, 0.45), P.S, 0.95)
    f["plus"] = tex("+", p2(3.5, -0.45), P.fg, 1.0)
    f["minus"] = tex("-", p2(-3.5, -0.45), P.muted, 1.0)
    return f

def f06_dir2d(az=28, el=22):
    f = Fig()
    f["axes"] = axes3d(L=2.8, az=az, el=el)
    th = np.radians(50)
    d = proj(2.6 * np.cos(th), 2.6 * np.sin(th), 0, az, el)
    f["D"] = dline(ORIGIN, d, P.S, w=4)
    f["Dtip"] = Arrow(d * 0.9, d, buff=0, color=P.S, stroke_width=4, tip_length=0.2,
                      max_tip_length_to_length_ratio=1)
    f["Dlab"] = tex("D", d + 0.3 * d / np.linalg.norm(d), P.S, 0.9)
    pts = [proj(0.9 * np.cos(t), 0.9 * np.sin(t), 0, az, el) for t in np.linspace(0, th, 30)]
    f["arc"] = VMobject(color=P.V, stroke_width=3).set_points_smoothly(pts)
    m = proj(1.25 * np.cos(th / 2), 1.25 * np.sin(th / 2), 0, az, el)
    f["th"] = tex(r"\theta", m, P.V, 0.9)
    return f

def f07_dir3d(az=28, el=22):
    f = Fig()
    f["axes"] = axes3d(L=2.8, az=az, el=el)
    th, ph, R = np.radians(55), np.radians(30), 2.6
    x, y, z = R * np.cos(ph) * np.cos(th), R * np.cos(ph) * np.sin(th), R * np.sin(ph)
    D, Dp = proj(x, y, z, az, el), proj(x, y, 0, az, el)
    f["D"] = vec(ORIGIN, D, P.S, w=5, tip=0.22)
    f["Dlab"] = tex("D", D + 0.3 * D / np.linalg.norm(D), P.S, 0.9)
    f["Dp"] = dline(ORIGIN, Dp, P.V, w=3.5)
    f["Dplab"] = tex("D'", Dp + 0.35 * Dp / np.linalg.norm(Dp), P.V, 0.9)
    f["drop"] = dline(D, Dp, P.aux, w=2)
    pts = [proj(0.8 * np.cos(t), 0.8 * np.sin(t), 0, az, el) for t in np.linspace(0, th, 30)]
    f["tharc"] = VMobject(color=P.V, stroke_width=3).set_points_smoothly(pts)
    f["th"] = tex(r"\theta", proj(1.15 * np.cos(th / 2), 1.15 * np.sin(th / 2), 0, az, el), P.V, 0.9)
    r = 1.3
    pts = [proj(r * np.cos(p) * np.cos(th), r * np.cos(p) * np.sin(th), r * np.sin(p), az, el)
           for p in np.linspace(0, ph, 20)]
    f["pharc"] = VMobject(color=P.C, stroke_width=3).set_points_smoothly(pts)
    r = 1.95
    f["ph"] = tex(r"\phi", proj(r * np.cos(ph / 2) * np.cos(th), r * np.cos(ph / 2) * np.sin(th),
                                r * np.sin(ph / 2), az, el), P.C, 0.9)
    return f

def f08_vec():
    f = Fig()
    a, b = p2(-2.6, -0.9), p2(2.4, 1.1)
    u = (b - a) / np.linalg.norm(b - a)
    f["line"] = dline(a - 1.2 * u, b + 1.4 * u, P.aux, w=2)
    f["dirtxt"] = txt("direzione", b + 1.4 * u + p2(0.1, 0.35), P.muted, 22)
    f["V"] = vec(a, b, P.S, w=8)
    f["Vlab"] = label_along(a, b, r"\boldsymbol{V}", P.S, 1, 0.45, 1.0)
    f["tail"] = Dot(a, color=P.fg, radius=0.07)
    f["tailtxt"] = txt("origine", a + p2(0.1, -0.42), P.muted, 22)
    f["headtxt"] = txt("verso", b + p2(0.35, -0.45), P.muted, 22)
    f["modtxt"] = txt("lunghezza \u221d modulo", (a + b) / 2 + p2(0.55, -0.62), P.muted, 22)
    f["u"] = vec(a + p2(0.0, -1.3), a + p2(0, -1.3) + 1.0 * u, P.V, w=6, tip=0.22)
    f["ulab"] = tex(r"\boldsymbol{u}", a + p2(0, -1.3) + 0.5 * u + p2(0.18, -0.32), P.V, 0.9)
    return f

# --- somma sul piano: geometria comune
V1 = p2(3.2, 0); TH = np.radians(55); V2 = 2.3 * p2(np.cos(TH), np.sin(TH))

def f10_sum_tri(o=p2(-2.4, -1.0)):
    f = Fig()
    a, b, c = o, o + V1, o + V1 + V2
    f["V1"] = vec(a, b, P.V); f["V1l"] = label_along(a, b, r"\boldsymbol{V}_1", P.V, -1)
    f["V2"] = vec(b, c, P.V); f["V2l"] = label_along(b, c, r"\boldsymbol{V}_2", P.V, -1)
    f["S"] = vec(a, c, P.S, w=7); f["Sl"] = label_along(a, c, r"\boldsymbol{S}", P.S, 1, 0.35, 1.0)
    return f

def f11_parallelogram(o=p2(-2.4, -1.0)):
    f = f10_sum_tri(o)
    a, b, c, d = o, o + V1, o + V1 + V2, o + V2
    f["V2b"] = DashedLine(a, d, color=P.V, stroke_width=4, dash_length=0.15)
    f["V1b"] = DashedLine(d, c, color=P.V, stroke_width=4, dash_length=0.15)
    return f

def f12_commut(o=p2(-2.4, -1.0)):
    f = Fig()
    a, d, c = o, o + V2, o + V1 + V2
    f["V2"] = vec(a, d, P.V); f["V2l"] = label_along(a, d, r"\boldsymbol{V}_2", P.V, 1)
    f["V1"] = vec(d, c, P.V); f["V1l"] = label_along(d, c, r"\boldsymbol{V}_1", P.V, 1)
    f["S"] = vec(a, c, P.S, w=7); f["Sl"] = label_along(a, c, r"\boldsymbol{S}", P.S, -1, 0.35, 1.0)
    return f

def f14_trig_plot():
    f = Fig()
    ax = Axes(x_range=[0, 2 * PI + 0.3, PI / 2], y_range=[-1.3, 1.3, 1], x_length=7.5, y_length=3.4,
              axis_config=dict(color=P.fg, stroke_width=2.5, include_tip=True, tip_length=0.2),
              tips=True)
    f["ax"] = ax
    labs = [(PI / 2, r"\tfrac{\pi}{2}"), (PI, r"\pi"), (3 * PI / 2, r"\tfrac{3\pi}{2}"), (2 * PI, r"2\pi")]
    g = VGroup(*[tex(s, ax.c2p(x, 0) + p2(0, -0.38), P.fg, 0.62) for x, s in labs])
    g.add(tex("1", ax.c2p(0, 1) + p2(-0.3, 0), P.fg, 0.6), tex("-1", ax.c2p(0, -1) + p2(-0.35, 0), P.fg, 0.6))
    f["ticks"] = g
    f["sin"] = ax.plot(np.sin, x_range=[0, 2 * PI], color=P.S, stroke_width=5)
    f["cos"] = ax.plot(np.cos, x_range=[0, 2 * PI], color=P.V, stroke_width=5)
    f["sinl"] = tex(r"\mathrm{sen}\,x", ax.c2p(1.2, 1.25), P.S, 0.75)
    f["cosl"] = tex(r"\cos x", ax.c2p(5.9, 1.25), P.V, 0.75)
    return f

def unit_circle(x_deg=40, R=2.4, show_tan=True):
    f = Fig()
    x = np.radians(x_deg)
    O = ORIGIN; C = p2(R * np.cos(x), 0); D = p2(R * np.cos(x), R * np.sin(x))
    A = p2(R, 0); B = p2(R, R * np.tan(x))
    f["axx"] = Arrow(p2(-R - 0.5, 0), p2(R + 0.7, 0), buff=0, color=P.fg, stroke_width=2.5, tip_length=0.18,
                     max_tip_length_to_length_ratio=0.1)
    f["axy"] = Arrow(p2(0, -R - 0.4), p2(0, R + 0.6), buff=0, color=P.fg, stroke_width=2.5, tip_length=0.18,
                     max_tip_length_to_length_ratio=0.1)
    f["X"] = tex("X", p2(R + 0.95, 0), P.fg, 0.7); f["Y"] = tex("Y", p2(0, R + 0.85), P.fg, 0.7)
    f["circ"] = Circle(radius=R, color=P.muted, stroke_width=2.5)
    f["tri"] = Polygon(O, C, D, color=P.fill, fill_opacity=0.28, stroke_width=0)
    f["OD"] = Line(O, D, color=P.fg, stroke_width=4)
    f["OC"] = Line(O, C, color=P.V, stroke_width=6)
    f["DC"] = Line(C, D, color=P.S, stroke_width=6)
    f["xarc"] = ang_arc(O, 0.55, 0, x, P.fg); f["x"] = tex("x", p2(0.8 * np.cos(x / 2), 0.8 * np.sin(x / 2)), P.fg, 0.7)
    if show_tan:
        f["AB"] = Line(A, B, color=P.C, stroke_width=6)
        f["OB"] = dline(D, B, P.aux)
        f["Bl"] = tex("B", B + p2(0.25, 0.1), P.fg, 0.65)
        f["tanl"] = tex(r"\tan x", (A + B) / 2 + p2(0.55, 0), P.C, 0.6)
    f["Ol"] = tex("O", p2(-0.25, -0.28), P.fg, 0.65)
    f["Cl"] = tex("C", C + p2(-0.15, -0.3), P.fg, 0.65)
    f["Dl"] = tex("D", D + p2(-0.1, 0.3), P.fg, 0.65)
    f["Al"] = tex("A", A + p2(0.22, -0.28), P.fg, 0.65)
    f["sinl"] = tex(r"\mathrm{sen}\,x", p2(C[0] - 0.5, 0.33 * D[1]), P.S, 0.6)
    f["cosl"] = tex(r"\cos x", (O + C) / 2 + p2(0, -0.32), P.V, 0.6)
    f["r1"] = tex("r=1", (O + D) / 2 + p2(-0.35, 0.3), P.fg, 0.6)
    return f

def f17_values(R=2.2):
    f = Fig()
    f["axx"] = Arrow(p2(-R - 0.5, 0), p2(R + 0.7, 0), buff=0, color=P.fg, stroke_width=2.5, tip_length=0.18,
                     max_tip_length_to_length_ratio=0.1)
    f["axy"] = Arrow(p2(0, -R - 0.5), p2(0, R + 0.7), buff=0, color=P.fg, stroke_width=2.5, tip_length=0.18,
                     max_tip_length_to_length_ratio=0.1)
    f["circ"] = Circle(radius=R, color=P.muted, stroke_width=2.5)
    pts = [(0, r"x=0,\ 2\pi", p2(R + 0.15, 0.4), (0, 1)), (PI / 2, r"x=\tfrac{\pi}{2}", p2(0.95, R + 0.3), (1, 0)),
           (PI, r"x=\pi", p2(-R - 0.1, 0.4), (0, -1)), (3 * PI / 2, r"x=\tfrac{3}{2}\pi", p2(1.0, -R - 0.3), (-1, 0))]
    for i, (a, s, lp, _) in enumerate(pts):
        f[f"d{i}"] = Dot(p2(R * np.cos(a), R * np.sin(a)), color=P.S, radius=0.1)
        f[f"l{i}"] = tex(s, lp, P.S, 0.62)
    return f

# --- triangolo di Carnot (slide 18-20)
def f18_carnot(o=p2(-3.4, -1.4), full=True):
    f = Fig()
    Cc, Oo, Bb = o, o + V1, o + V1 + V2
    Aa = p2(Bb[0], Oo[1])
    f["ext"] = dline(Oo, Aa, P.aux)
    f["AB"] = dline(Aa, Bb, P.aux)
    f["V1"] = vec(Cc, Oo, P.V); f["V1l"] = label_along(Cc, Oo, r"\boldsymbol{V}_1", P.V, -1)
    f["V2"] = vec(Oo, Bb, P.V); f["V2l"] = label_along(Oo, Bb, r"\boldsymbol{V}_2", P.V, -1, 0.34, 0.8, 0.45)
    f["S"] = vec(Cc, Bb, P.S, w=7); f["Sl"] = label_along(Cc, Bb, r"\boldsymbol{S}", P.S, 1, 0.35, 1.0)
    f["tharc"] = ang_arc(Oo, 0.45, 0, TH, P.fg)
    f["th"] = ang_label(Oo, 0.75, 0, TH, r"\theta", P.fg)
    aS = ang(Bb - Cc)
    f["alarc"] = ang_arc(Cc, 0.9, 0, aS, P.fg); f["al"] = ang_label(Cc, 1.2, 0, aS, r"\alpha", P.fg)
    f["bearc"] = ang_arc(Bb, 0.6, aS + PI, TH + PI, P.fg)
    f["be"] = ang_label(Bb, 0.9, aS + PI, TH + PI, r"\beta", P.fg)
    f["ra"] = right_mark(Aa, LEFT, UP, 0.18, P.aux)
    for n, pt, d in [("C", Cc, p2(-0.3, -0.1)), ("O", Oo, p2(0, -0.35)), ("A", Aa, p2(0.25, -0.3)), ("B", Bb, p2(0.25, 0.2))]:
        f["L" + n] = tex(n, pt + d, P.fg, 0.75)
    if full:
        f["v2c"] = tex(r"V_2\cos\theta", (Oo + Aa) / 2 + p2(0.05, -0.8), P.C, 0.7)
        f["v2s"] = tex(r"V_2\,\mathrm{sen}\,\theta", (Aa + Bb) / 2 + p2(0.95, 0), P.C, 0.7)
    return f

def f21_sines(o=p2(-2.6, -1.2)):
    f = Fig()
    Cc, Oo, Bb = o, o + V1, o + V1 + V2
    f["V1"] = vec(Cc, Oo, P.V); f["V1l"] = label_along(Cc, Oo, r"\boldsymbol{V}_1", P.V, -1)
    f["V2"] = vec(Oo, Bb, P.V); f["V2l"] = label_along(Oo, Bb, r"\boldsymbol{V}_2", P.V, -1, 0.34, 0.8, 0.55)
    f["S"] = vec(Cc, Bb, P.S, w=7); f["Sl"] = label_along(Cc, Bb, r"\boldsymbol{S}", P.S, 1, 0.35, 1.0)
    aS = ang(Bb - Cc)
    f["alarc"] = ang_arc(Cc, 0.9, 0, aS, P.fg); f["al"] = ang_label(Cc, 1.2, 0, aS, r"\alpha", P.fg)
    f["bearc"] = ang_arc(Bb, 0.6, aS + PI, TH + PI, P.fg); f["be"] = ang_label(Bb, 0.9, aS + PI, TH + PI, r"\beta", P.fg)
    f["gaarc"] = ang_arc(Oo, 0.45, TH, PI, P.C); f["ga"] = ang_label(Oo, 0.75, TH, PI, r"\gamma", P.C)
    return f

def f22_perp(o=p2(-2.4, -1.0)):
    f = Fig()
    v1, v2 = p2(3.6, 0), p2(0, 2.0)
    a, b, c = o, o + v1, o + v1 + v2
    f["V1"] = vec(a, b, P.V); f["V1l"] = label_along(a, b, r"\boldsymbol{V}_1", P.V, -1)
    f["V2"] = vec(b, c, P.V); f["V2l"] = label_along(b, c, r"\boldsymbol{V}_2", P.V, -1)
    f["S"] = vec(a, c, P.S, w=7); f["Sl"] = label_along(a, c, r"\boldsymbol{S}", P.S, 1, 0.35, 1.0)
    f["ra"] = right_mark(b, LEFT, UP, 0.22, P.fg)
    f["ext"] = dline(b, b + p2(1.0, 0), P.aux)
    f["th"] = tex(r"\theta=\pi/2", b + p2(0.95, 0.35), P.fg, 0.65)
    aS = ang(c - a)
    f["alarc"] = ang_arc(a, 1.0, 0, aS, P.fg); f["al"] = ang_label(a, 1.3, 0, aS, r"\alpha", P.fg)
    return f

def f23_diff(o=p2(-3.2, 1.0)):
    f = Fig()
    a, b = o, o + V1
    c = b - V2
    f["V1"] = vec(a, b, P.V); f["V1l"] = label_along(a, b, r"\boldsymbol{V}_1", P.V, 1)
    f["mV2"] = vec(b, c, P.C); f["mV2l"] = label_along(b, c, r"-\boldsymbol{V}_2", P.C, 1, 0.55)
    f["D"] = vec(a, c, P.S, w=7); f["Dl"] = label_along(a, c, r"\boldsymbol{D}", P.S, 1, 0.4, 1.0)
    q = o + p2(4.3, -1.7)
    f["V2"] = vec(q, q + V2, P.V); f["V2l"] = label_along(q, q + V2, r"\boldsymbol{V}_2", P.V, -1)
    return f

def f24_anticomm(o=p2(-3.2, 1.0)):
    f = Fig()
    # V2 - V1 = V2 + (-V1): parto da V2, poi -V1
    a = o + p2(0.4, -2.2)
    b = a + V2
    c = b - V1
    f["V2"] = vec(a, b, P.V); f["V2l"] = label_along(a, b, r"\boldsymbol{V}_2", P.V, -1)
    f["mV1"] = vec(b, c, P.C); f["mV1l"] = label_along(b, c, r"-\boldsymbol{V}_1", P.C, -1, 0.35)
    f["mD"] = vec(a, c, P.S, w=7); f["mDl"] = label_along(a, c, r"-\boldsymbol{D}", P.S, -1, 0.5, 1.0)
    q = a + p2(-3.4, 1.9)
    f["D"] = vec(q, q - (c - a), P.muted, w=5); f["Dl"] = label_along(q, q - (c - a), r"\boldsymbol{D}", P.muted, -1, 0.4)
    return f

def f27_components(o=p2(-2.6, -1.3)):
    f = Fig()
    V = p2(4.4, 2.0)
    a, b, x = o, o + V, o + p2(V[0], 0)
    f["Vx"] = vec(a, x, P.V); f["Vxl"] = label_along(a, x, r"\boldsymbol{V}_x", P.V, -1)
    f["Vy"] = vec(x, b, P.V); f["Vyl"] = label_along(x, b, r"\boldsymbol{V}_y", P.V, -1)
    f["V"] = vec(a, b, P.S, w=7); f["Vl"] = label_along(a, b, r"\boldsymbol{V}", P.S, 1, 0.35, 1.0)
    f["ra"] = right_mark(x, LEFT, UP, 0.22, P.fg)
    aV = ang(V)
    f["alarc"] = ang_arc(a, 1.0, 0, aV, P.fg); f["al"] = ang_label(a, 1.3, 0, aV, r"\alpha", P.fg)
    return f

def f28_projection(o=p2(-3.6, -1.4)):
    f = Fig()
    d = np.array([np.cos(np.radians(8)), np.sin(np.radians(8)), 0])
    al = np.radians(27); ta = np.radians(8) + al
    V = 4.4 * np.array([np.cos(ta), np.sin(ta), 0])
    pr = (V @ d) * d
    f["axis"] = Arrow(o - 0.5 * d, o + 7.0 * d, buff=0, color=P.muted, stroke_width=3, tip_length=0.2,
                      max_tip_length_to_length_ratio=0.1)
    f["Dlab"] = tex("D", o + 7.2 * d + p2(0, 0.35), P.muted, 0.8)
    f["V"] = vec(o, o + V, P.S, w=7); f["Vl"] = label_along(o, o + V, r"\boldsymbol{V}", P.S, 1, 0.35, 1.0)
    f["drop"] = dline(o + V, o + pr, P.aux)
    f["VD"] = vec(o, o + pr, P.V, w=7)
    f["VDl"] = tex(r"V_D = V\cos\alpha", o + 0.5 * pr + p2(0.1, -0.5), P.V, 0.8)
    f["ra"] = right_mark(o + pr, -d, (V - pr), 0.2, P.fg)
    f["alarc"] = ang_arc(o, 1.3, np.radians(8), ta, P.fg); f["al"] = ang_label(o, 1.6, np.radians(8), ta, r"\alpha", P.fg)
    f["O"] = tex("O", o + p2(-0.15, -0.35), P.fg, 0.75)
    return f

def f29_pos3d(az=28, el=22):
    f = Fig()
    f["axes"] = axes3d(L=3.0, az=az, el=el)
    x, y, z = 1.6, 2.0, 2.2
    Pp = proj(x, y, z, az, el)
    f["Px"] = vec(ORIGIN, proj(x, 0, 0, az, el), P.V, w=5, tip=0.2)
    f["Py"] = vec(ORIGIN, proj(0, y, 0, az, el), P.V, w=5, tip=0.2)
    f["Pz"] = vec(ORIGIN, proj(0, 0, z, az, el), P.V, w=5, tip=0.2)
    f["Pxl"] = tex(r"\boldsymbol{P}_x", proj(x, 0, 0, az, el) + p2(0.35, -0.2), P.V, 0.75)
    f["Pyl"] = tex(r"\boldsymbol{P}_y", proj(0, y, 0, az, el) + p2(0.0, -0.38), P.V, 0.75)
    f["Pzl"] = tex(r"\boldsymbol{P}_z", proj(0, 0, z, az, el) + p2(-0.4, 0), P.V, 0.75)
    box = VGroup()
    for a, b in [((x, 0, 0), (x, y, 0)), ((0, y, 0), (x, y, 0)), ((x, y, 0), (x, y, z)),
                 ((0, 0, z), (x, 0, z)), ((0, 0, z), (0, y, z)), ((x, 0, z), (x, y, z)), ((0, y, z), (x, y, z)),
                 ((x, 0, 0), (x, 0, z)), ((0, y, 0), (0, y, z))]:
        box.add(dline(proj(*a, az=az, el=el), proj(*b, az=az, el=el), P.aux, w=1.8, dash=0.1))
    f["box"] = box
    f["P"] = vec(ORIGIN, Pp, P.S, w=7, tip=0.24)
    f["Pl"] = tex(r"\boldsymbol{P}", Pp + p2(0.25, 0.3), P.S, 0.95)
    f["dot"] = Dot(Pp, color=P.S, radius=0.08)
    f["O"] = tex("O", p2(-0.3, -0.25), P.fg, 0.75)
    return f

MANY = [p2(2.3, 0), p2(1.1, 1.4), p2(-0.4, 1.5), p2(-2.4, 0)]

def f31_sum_many(o=p2(-1.8, -2.0)):
    f = Fig()
    pts = [o]
    for v in MANY:
        pts.append(pts[-1] + v)
    sides = [1, 1, 1, 1]
    for i in range(4):
        f[f"V{i+1}"] = vec(pts[i], pts[i + 1], P.V)
        f[f"V{i+1}l"] = label_along(pts[i], pts[i + 1], rf"\boldsymbol{{V}}_{i+1}", P.V, -1)
    for i in range(1, 4):
        f[f"S{i}"] = vec(o, pts[i + 1], P.S, w=6)
        f[f"S{i}l"] = label_along(o, pts[i + 1], rf"\boldsymbol{{S}}_{i}", P.S, 1 if i < 3 else -1, 0.35, 0.85, 0.55)
    return f

def f32_diff_many(o=p2(-1.2, -0.4)):
    f = Fig()
    v1, v2, v3 = p2(1.5, 2.0), p2(3.0, 0), p2(-0.6, 2.8)
    a = o; b = a + v1; c = b - v2; d = c - v3
    f["V1"] = vec(a, b, P.V); f["V1l"] = label_along(a, b, r"\boldsymbol{V}_1", P.V, -1)
    f["mV2"] = vec(b, c, P.C); f["mV2l"] = label_along(b, c, r"-\boldsymbol{V}_2", P.C, -1, 0.35)
    f["D1"] = vec(a, c, P.S, w=6); f["D1l"] = label_along(a, c, r"\boldsymbol{D}_1", P.S, -1, 0.35)
    f["mV3"] = vec(c, d, P.C); f["mV3l"] = label_along(c, d, r"-\boldsymbol{V}_3", P.C, -1, 0.5)
    f["D2"] = vec(a, d, P.S, w=6); f["D2l"] = label_along(a, d, r"\boldsymbol{D}_2", P.S, 1, 0.35)
    q = p2(2.6, 2.0)
    f["V2"] = vec(q, q + v2 * 0.75, P.muted, w=4); f["V2l"] = label_along(q, q + v2 * .75, r"\boldsymbol{V}_2", P.muted, 1)
    q = p2(3.6, -1.6)
    f["V3"] = vec(q, q + v3 * 0.9, P.muted, w=4); f["V3l"] = label_along(q, q + v3 * .9, r"\boldsymbol{V}_3", P.muted, -1)
    return f

def f34_dot(o=p2(-3.2, -1.2), th_deg=28):
    f = Fig()
    th = np.radians(th_deg)
    A = p2(5.2, 0); B = 3.8 * p2(np.cos(th), np.sin(th))
    f["ext"] = dline(o + A, o + A + p2(1.2, 0), P.aux)
    f["A"] = vec(o, o + A, P.S, w=7); f["Al"] = tex(r"\boldsymbol{A}", o + A + p2(-0.2, -0.45), P.S, 1.0)
    f["B"] = vec(o, o + B, P.V, w=7); f["Bl"] = label_along(o, o + B, r"\boldsymbol{B}", P.V, 1, 0.35, 1.0)
    f["drop"] = dline(o + B, o + p2(B[0], 0), P.aux)
    f["BA"] = Line(o, o + p2(B[0], 0), color=P.C, stroke_width=10).set_opacity(0.85)
    f["BAl"] = tex(r"B_A = B\cos\theta", o + p2(B[0] / 2, -0.55), P.C, 0.8)
    f["ra"] = right_mark(o + p2(B[0], 0), LEFT, UP, 0.2, P.fg)
    f["tharc"] = ang_arc(o, 1.1, 0, th, P.fg); f["th"] = ang_label(o, 1.42, 0, th, r"\theta", P.fg)
    return f

def f37_cross(az=28, el=35, anti=False, th_deg=60, a_deg=55):
    f = Fig()
    f["axes"] = axes3d(o=ORIGIN, L=2.2, az=az, el=el, col=P.muted)
    f["O"] = tex("O", p2(-0.35, 0.05), P.muted, 0.7)
    o3 = np.array([1.2, 1.2, 0.0])
    th = np.radians(th_deg); a0 = np.radians(a_deg)
    a3 = 3.0 * np.array([np.cos(a0), np.sin(a0), 0])
    b3 = 2.2 * np.array([np.cos(a0 + th), np.sin(a0 + th), 0])
    def P3(v): return proj(*(o3 + v), az=az, el=el)
    O3 = P3(np.zeros(3))
    def away(v, d=0.38):
        w = P3(v) - O3; return P3(v) + d * w / np.linalg.norm(w)
    f["para"] = Polygon(O3, P3(a3), P3(a3 + b3), P3(b3), color=P.V, fill_opacity=0.16, stroke_width=0)
    f["pe1"] = dline(P3(a3), P3(a3 + b3), P.aux, w=2); f["pe2"] = dline(P3(b3), P3(a3 + b3), P.aux, w=2)
    if not anti:
        ah = a3 / np.linalg.norm(a3); foot = (b3 @ ah) * ah; top = b3
        f["h"] = dline(P3(top), P3(foot), P.C, w=3.5)
        f["hl"] = tex(r"B\,\mathrm{sen}\,\theta", P3(0.62 * a3 + 0.5 * b3), P.C, 0.65)
    else:
        bh = b3 / np.linalg.norm(b3); foot = (a3 @ bh) * bh; top = a3
        f["h"] = dline(P3(top), P3(foot), P.C, w=3.5)
        f["hl"] = tex(r"A\,\mathrm{sen}\,\theta", P3(0.55 * a3 + 0.62 * b3), P.C, 0.65)
    f["A"] = vec(O3, P3(a3), P.V, w=6, tip=0.22); f["Al"] = tex(r"\boldsymbol{A}", away(a3), P.V, 0.9)
    f["B"] = vec(O3, P3(b3), P.V, w=6, tip=0.22); f["Bl"] = tex(r"\boldsymbol{B}", away(b3), P.V, 0.9)
    pts = [P3(0.8 * np.array([np.cos(t), np.sin(t), 0])) for t in np.linspace(a0, a0 + th, 20)]
    f["tharc"] = VMobject(color=P.fg, stroke_width=3).set_points_smoothly(pts)
    f["th"] = tex(r"\theta", P3(1.15 * np.array([np.cos(a0 + th / 2), np.sin(a0 + th / 2), 0])), P.fg, 0.7)
    s = -1 if anti else 1
    nv = s * np.array([0, 0, 2.3])
    f["V"] = vec(O3, P3(nv), P.S, w=7, tip=0.26)
    f["Vl"] = tex(r"-\boldsymbol{V}" if anti else r"\boldsymbol{V}", P3(nv) + p2(-0.45, -0.1 * s), P.S, 1.0)
    # rotazione "a vite" attorno a V: da A verso B (o da B verso A)
    ts = np.linspace(a0, a0 + np.radians(300), 40) if not anti else np.linspace(a0 + th, a0 + th - np.radians(300), 40)
    zc = 1.0 * s
    pts = [P3(np.array([0.42 * np.cos(t), 0.42 * np.sin(t), zc])) for t in ts]
    rot = VMobject(color=P.C, stroke_width=4).set_points_smoothly(pts[:-3])
    rot.add(Arrow(pts[-5], pts[-1], buff=0, color=P.C, stroke_width=4, tip_length=0.18, max_tip_length_to_length_ratio=1))
    f["rot"] = rot
    return f

def f25_supp(R=2.2, th_deg=55):
    """cos(pi - theta) = -cos(theta): simmetria rispetto all'asse Y."""
    f = Fig()
    th = np.radians(th_deg)
    f["axx"] = Arrow(p2(-R - 0.5, 0), p2(R + 0.7, 0), buff=0, color=P.fg, stroke_width=2.5, tip_length=0.18,
                     max_tip_length_to_length_ratio=0.1)
    f["axy"] = Arrow(p2(0, -0.6), p2(0, R + 0.6), buff=0, color=P.fg, stroke_width=2.5, tip_length=0.18,
                     max_tip_length_to_length_ratio=0.1)
    f["circ"] = Arc(radius=R, start_angle=-0.15, angle=PI + 0.3, color=P.muted, stroke_width=2.5)
    A = R * p2(np.cos(th), np.sin(th)); B = R * p2(-np.cos(th), np.sin(th))
    f["rA"] = Line(ORIGIN, A, color=P.V, stroke_width=4); f["rB"] = Line(ORIGIN, B, color=P.S, stroke_width=4)
    f["dA"] = dline(A, p2(A[0], 0)); f["dB"] = dline(B, p2(B[0], 0))
    f["cA"] = Line(ORIGIN, p2(A[0], 0), color=P.V, stroke_width=7)
    f["cB"] = Line(ORIGIN, p2(B[0], 0), color=P.S, stroke_width=7)
    f["aA"] = ang_arc(ORIGIN, 0.55, 0, th, P.V); f["lA"] = ang_label(ORIGIN, 0.85, 0, th, r"\theta", P.V)
    f["aB"] = ang_arc(ORIGIN, 0.4, 0, PI - th, P.S); f["lB"] = ang_label(ORIGIN, 1.15, th, PI - th * 0.6, r"\pi-\theta", P.S, 0.65)
    f["tA"] = tex(r"\cos\theta", p2(A[0] / 2, -0.4), P.V, 0.65)
    f["tB"] = tex(r"-\cos\theta", p2(B[0] / 2, -0.4), P.S, 0.65)
    return f
