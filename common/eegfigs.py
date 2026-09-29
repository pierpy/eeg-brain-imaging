"""Libreria di figure e segnali per il corso EEG (Brain Imaging – Methods and Applications).
Tutto ciò che è "dato" è SIMULATO con modelli fisiologicamente plausibili (dichiararlo sulle slide).
Le figure sono oggetti manim (Fig = dict di mobject) usabili sia nelle scene sia per i PNG statici."""
import os as _os
_R = _os.environ.get("COURSE_ROOT") or _os.path.dirname(_os.path.abspath(__file__))
while not _os.path.exists(_os.path.join(_R, ".course_root")) and _os.path.dirname(_R) != _R:
    _R = _os.path.dirname(_R)
import os, sys
sys.path.insert(0, _R + "/common"); sys.path.insert(0, _R + "/common")
import numpy as np
from manim import (VGroup, VMobject, Arrow, Line, DashedLine, DoubleArrow, Dot, Circle, Ellipse, Polygon, Rectangle,
                   RoundedRectangle, ArcBetweenPoints, Arc, MathTex, Text, ImageMobject, ORIGIN, UP, DOWN, LEFT, RIGHT, PI,
                   interpolate_color, ManimColor)
import figs as F
from figs import Fig, p2, vec, tex

P = F.P
set_theme = F.set_theme
from manim import Group as _Group
Fig.group = lambda self: _Group(*self.values())   # le figure EEG possono contenere immagini (topografie)
LANG = os.environ.get("EEG_LANG", "en")


def tr(en, it):
    """testo nella lingua corrente (EEG_LANG=en|it)."""
    return it if LANG == "it" else en


def txt(s, pos=ORIGIN, col=None, sz=24, weight="NORMAL", slant="NORMAL"):
    return Text(s, font="Carlito", color=col or P.fg, font_size=sz * 4, weight=weight, slant=slant).scale(0.25).move_to(pos)


# ================================================================== segnali simulati
FS = 250.0


def pink(n, seed=0, alpha=1.0):
    """rumore 1/f^alpha a media nulla e varianza unitaria."""
    rng = np.random.default_rng(seed)
    X = rng.normal(size=n // 2 + 1) + 1j * rng.normal(size=n // 2 + 1)
    f = np.arange(n // 2 + 1); f[0] = 1
    X /= f ** (alpha / 2)
    x = np.fft.irfft(X, n)
    return (x - x.mean()) / x.std()


def burst(t, f0, amp, seed=0, n_bursts=None, dur=(0.6, 2.0)):
    """oscillazione a fuso (burst) a frequenza f0 con inviluppo gaussiano."""
    rng = np.random.default_rng(seed)
    T = t[-1] - t[0]
    n = n_bursts or max(1, int(T / 1.5))
    y = np.zeros_like(t)
    for _ in range(n):
        c = rng.uniform(t[0], t[-1]); w = rng.uniform(*dur) / 2.5
        ph = rng.uniform(0, 2 * np.pi); fj = f0 + rng.normal(0, 0.3)
        y += amp * np.exp(-0.5 * ((t - c) / w) ** 2) * np.sin(2 * np.pi * fj * t + ph)
    return y


def eeg(dur=4.0, fs=FS, seed=0, alpha=1.0, beta=0.3, theta=0.3, delta=0.2, gamma=0.0, noise=1.0, uv=30.0):
    """EEG sintetico (µV): rumore 1/f + ritmi a fusi. Restituisce (t, x)."""
    t = np.arange(0, dur, 1 / fs)
    x = noise * pink(len(t), seed)
    x += burst(t, 10.0, 2.5 * alpha, seed + 1)
    x += burst(t, 20.0, 1.2 * beta, seed + 2, dur=(0.3, 0.8))
    x += burst(t, 6.0, 2.0 * theta, seed + 3)
    x += burst(t, 2.0, 3.0 * delta, seed + 4, dur=(1.0, 3.0))
    x += burst(t, 40.0, 0.8 * gamma, seed + 5, dur=(0.1, 0.3))
    return t, x / np.std(x) * uv / 2.5


def trace(t, x, O, w, h_per_uv, col=None, sw=2.5, t0=None, t1=None):
    """polilinea del segnale x(t) con origine O, larghezza w (su [t0,t1]), scala verticale h_per_uv."""
    t0 = t[0] if t0 is None else t0; t1 = t[-1] if t1 is None else t1
    m = (t >= t0) & (t <= t1)
    xs = (t[m] - t0) / (t1 - t0) * w
    pts = [np.asarray(O, float) + p2(a, b * h_per_uv) for a, b in zip(xs, x[m])]
    return VMobject(color=col or P.V, stroke_width=sw).set_points_as_corners(pts)


# ================================================================== testa ed elettrodi (sistema 10-20)
# coordinate polari stile EEGLAB: theta (gradi, 0 = naso, positivo verso destra), r (0.5 = 90° dal vertice)
E1020 = {"Fp1": (-18, .511), "Fp2": (18, .511), "F7": (-54, .511), "F3": (-39, .333), "Fz": (0, .256), "F4": (39, .333),
         "F8": (54, .511), "T7": (-90, .511), "C3": (-90, .256), "Cz": (0, 0), "C4": (90, .256), "T8": (90, .511),
         "P7": (-126, .511), "P3": (-141, .333), "Pz": (180, .256), "P4": (141, .333), "P8": (126, .511),
         "O1": (-162, .511), "O2": (162, .511)}
NAMES = list(E1020)


def el2d(name, R=1.0, edge=0.85):
    """posizione 2D (vista dall'alto, naso in su) su una testa di raggio R."""
    th, r = E1020[name]
    rr = r / 0.511 * edge * R
    return np.array([rr * np.sin(np.radians(th)), rr * np.cos(np.radians(th)), 0.0])


def el3d(name):
    """posizione 3D su sfera unitaria (z = vertice, y = naso, x = destra)."""
    th, r = E1020[name]
    phi = np.radians(r / 0.5 * 90.0)
    return np.array([np.sin(phi) * np.sin(np.radians(th)), np.sin(phi) * np.cos(np.radians(th)), np.cos(phi)])


def head(c=ORIGIN, R=1.0, col=None, sw=3):
    c = np.asarray(c, float); col = col or P.fg
    g = VGroup(Circle(radius=R, color=col, stroke_width=sw).move_to(c))
    g.add(VMobject(color=col, stroke_width=sw).set_points_as_corners([c + p2(-0.12 * R, 0.99 * R), c + p2(0, 1.13 * R), c + p2(0.12 * R, 0.99 * R)]))
    for s in (-1, 1):
        g.add(Ellipse(width=0.12 * R, height=0.34 * R, color=col, stroke_width=sw).move_to(c + p2(s * 1.04 * R, 0)))
    return g


def electrodes(c=ORIGIN, R=1.0, names=None, col=None, r=0.07, labels=False, lsz=14):
    c = np.asarray(c, float); g = VGroup()
    for n in (names or NAMES):
        p = c + el2d(n, R)
        g.add(Circle(radius=r * R, color=col or P.fg, stroke_width=2, fill_color=P.bg, fill_opacity=1).move_to(p))
        if labels:
            g.add(txt(n, p + p2(0, -0.16 * R), P.muted, lsz))
    return g


# ------------------------------------------------------------------ colormap e topografie
def cmap_rdbu(v):
    """v in [-1,1] -> RGB (blu-bianco-rosso, stile RdBu_r)."""
    v = np.clip(v, -1, 1)
    neg = np.array([33, 102, 172]) / 255; mid = np.array([247, 247, 247]) / 255; pos = np.array([178, 24, 43]) / 255
    a = np.abs(v)[..., None]
    return np.where(v[..., None] < 0, mid * (1 - a) + neg * a, mid * (1 - a) + pos * a)


def dipole_pot(xyz, pos, mom):
    """potenziale di un dipolo di corrente in mezzo omogeneo infinito (unità arbitrarie)."""
    d = xyz - pos
    r3 = np.linalg.norm(d, axis=-1) ** 3 + 1e-9
    return (d @ mom) / r3


def sphere_grid(n=161):
    """griglia 2D (proiezione azimutale equidistante) -> punti 3D sulla sfera unitaria e maschera."""
    u = np.linspace(-1, 1, n); X, Y = np.meshgrid(u, -u)
    rho = np.hypot(X, Y); mask = rho <= 1.0
    phi = rho / 0.85 * (np.pi / 2)            # bordo della testa (0.85) = 90° dal vertice
    phi = np.minimum(phi, 0.62 * np.pi)
    az = np.arctan2(X, Y)
    xyz = np.stack([np.sin(phi) * np.sin(az), np.sin(phi) * np.cos(az), np.cos(phi)], -1)
    return xyz, mask


def dipole_map(pos, mom, n=161, blur=0.0):
    """mappa di potenziale di scalpo (griglia n×n) per uno o più dipoli.
    blur > 0 simula lo sfocamento del cranio (media pesata su una calotta)."""
    xyz, mask = sphere_grid(n)
    V = np.zeros(xyz.shape[:2])
    pos = np.atleast_2d(pos); mom = np.atleast_2d(mom)
    for p_, m_ in zip(pos, mom):
        V += dipole_pot(xyz, np.asarray(p_, float), np.asarray(m_, float))
    if blur > 0:
        from scipy.ndimage import gaussian_filter
        V = gaussian_filter(V, blur * n / 10)
    return V, mask


def topo_img(V, mask, vmax=None, alpha_out=0.0):
    """RGBA uint8 da una mappa: fuori dalla testa trasparente."""
    vmax = vmax or 0.75 * np.nanmax(np.abs(V[mask]))
    rgb = cmap_rdbu(V / vmax)
    a = np.where(mask, 1.0, alpha_out)
    return (np.dstack([rgb, a]) * 255).astype(np.uint8)


def interp_map(values, names=None, n=161, p=2.0):
    """interpolazione (inverse distance weighting su sfera) di valori agli elettrodi -> griglia."""
    names = names or NAMES
    xyz, mask = sphere_grid(n)
    E = np.array([el3d(k) for k in names])
    d = np.arccos(np.clip(xyz @ E.T, -1, 1)) + 1e-4
    w = 1 / d ** p
    V = (w @ np.asarray(values, float)) / w.sum(-1)
    return V, mask


def topomap(V, mask, c=ORIGIN, R=1.0, vmax=None, outline=True, elec=False, col=None):
    """ImageMobject della mappa + contorno testa (Group di mobject: restituisce (img, outline))."""
    img = ImageMobject(topo_img(V, mask, vmax))
    from manim import RESAMPLING_ALGORITHMS
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    img.height = 2 * R
    img.move_to(c)
    out = VGroup()
    if outline:
        out.add(head(c, R, col))
    if elec:
        out.add(electrodes(c, R, r=0.045))
    return img, out


# ================================================================== neuroni e dipoli
def pyramidal(c=ORIGIN, s=1.0, col=None, sw=3):
    """neurone piramidale schematico: soma triangolare, dendrite apicale con ciuffo, dendriti basali, assone."""
    c = np.asarray(c, float); col = col or P.fg
    g = VGroup()
    g.add(Polygon(c + p2(-0.22, -0.18) * s, c + p2(0.22, -0.18) * s, c + p2(0, 0.25) * s, color=col, stroke_width=sw,
                  fill_color=col, fill_opacity=0.25))
    top = c + p2(0, 1.6) * s
    g.add(Line(c + p2(0, 0.25) * s, top, color=col, stroke_width=sw))
    for a in (-1, -0.45, 0.45, 1):
        g.add(Line(top, top + p2(0.45 * a, 0.35 + 0.15 * (1 - abs(a))) * s, color=col, stroke_width=sw - 0.5))
    for a in (-1, 1):
        g.add(Line(c + p2(0.18 * a, -0.15) * s, c + p2(0.6 * a, -0.45) * s, color=col, stroke_width=sw - 0.5))
    g.add(Line(c + p2(0, -0.18) * s, c + p2(0, -1.0) * s, color=col, stroke_width=sw - 1))
    return g


def stellate(c=ORIGIN, s=1.0, col=None, sw=2.5, n=7, seed=2):
    c = np.asarray(c, float); col = col or P.fg; rng = np.random.default_rng(seed)
    g = VGroup(Dot(c, radius=0.13 * s, color=col))
    for k in range(n):
        a = 2 * np.pi * k / n + rng.uniform(-0.3, 0.3); L = rng.uniform(0.4, 0.65) * s
        g.add(Line(c, c + L * np.array([np.cos(a), np.sin(a), 0]), color=col, stroke_width=sw))
    return g


# ================================================================== grafici generici
def axes(O, lx, ly, xl="", yl="", col=None, sc=0.6, tick=True):
    col = col or P.fg
    g = VGroup(Arrow(O, O + p2(lx, 0), buff=0, color=col, stroke_width=2.5, tip_length=0.14, max_tip_length_to_length_ratio=0.1),
               Arrow(O, O + p2(0, ly), buff=0, color=col, stroke_width=2.5, tip_length=0.14, max_tip_length_to_length_ratio=0.1))
    if xl: g.add(txt(xl, O + p2(lx, -0.6), P.muted, 18).align_to(O + p2(lx, 0), RIGHT))
    if yl: g.add(txt(yl, O + p2(0.1, ly + 0.2), P.muted, 18).align_to(O, LEFT))
    return g


def logpos(v, v0, v1, L):
    return (np.log10(v) - np.log10(v0)) / (np.log10(v1) - np.log10(v0)) * L


# metodi di imaging: (nome, t_min[s], t_max[s], s_min[mm], s_max[mm], invasivo)
METHODS = [("EEG / MEG", 1e-3, 1e2, 20, 100, False), ("fNIRS", 0.3, 5e2, 9.5, 18, False),
           ("fMRI", 1.5, 1e3, 1, 4.5, False), ("PET", 60, 1e4, 4.8, 8.5, False),
           ("ECoG", 1e-3, 0.8, 1, 8, True), ("LFP", 1e-3, 1e1, 0.1, 0.8, True), ("Single unit", 1e-4, 1e0, 0.012, 0.08, True)]


def f_resolution(W=7.0, Hh=4.6):
    """mappa risoluzione spaziale vs temporale dei metodi (scala log)."""
    f = Fig()
    O = p2(-W / 2, -Hh / 2)
    t0, t1, s0, s1 = 1e-4, 1e4, 1e-2, 1e3
    f["ax"] = axes(O, W, Hh, tr("temporal resolution (s)", "risoluzione temporale (s)"), tr("spatial resolution (mm)", "risoluzione spaziale (mm)"))
    for v in (1e-3, 1e-1, 1e1, 1e3):
        x = logpos(v, t0, t1, W)
        f[f"tx{v}"] = txt({1e-3: "1 ms", 1e-1: "100 ms", 1e1: "10 s", 1e3: "15 min"}[v], O + p2(x, -0.2), P.muted, 15)
    for v in (1e-1, 1e0, 1e1, 1e2):
        y = logpos(v, s0, s1, Hh)
        f[f"ty{v}"] = txt({1e-1: "0.1 mm", 1e0: "1 mm", 1e1: "1 cm", 1e2: "10 cm"}[v], O + p2(-0.45, y), P.muted, 15)
    cols = {"EEG / MEG": P.S, "fMRI": P.V, "PET": "#8E7CC3", "fNIRS": "#6FCF97", "ECoG": P.muted, "LFP": P.muted, "Single unit": P.muted}
    for n, a, b, c_, d, inv in METHODS:
        x0, x1 = logpos(a, t0, t1, W), logpos(b, t0, t1, W)
        y0, y1 = logpos(c_, s0, s1, Hh), logpos(d, s0, s1, Hh)
        col = cols[n]
        f[n] = RoundedRectangle(corner_radius=0.12, width=x1 - x0, height=y1 - y0, color=col, stroke_width=2,
                                fill_color=col, fill_opacity=0.15 if inv else 0.35).move_to(O + p2((x0 + x1) / 2, (y0 + y1) / 2))
        f[n + "l"] = txt(n, O + p2((x0 + x1) / 2, (y0 + y1) / 2), col if inv else P.fg, 16 if n in ("PET",) else 18, weight="BOLD")
    return f


# ================================================================== segnali periodici (per animazioni in loop)
def periodic_eeg(D=4.0, fs=FS, seed=0, peaks=((10.0, 1.0, 1.0),), slope=1.0, uv=30.0):
    """EEG sintetico ESATTAMENTE periodico di periodo D (sintesi in frequenza con fasi casuali):
    spettro 1/f^slope + picchi gaussiani (f0, larghezza Hz, ampiezza relativa)."""
    n = int(round(D * fs))
    f = np.fft.rfftfreq(n, 1 / fs)
    rng = np.random.default_rng(seed)
    amp = 1.0 / np.maximum(f, 0.5) ** (slope / 2)
    for f0, bw, a in peaks:
        amp = amp + a * 3.0 * np.exp(-0.5 * ((f - f0) / bw) ** 2)
    amp[0] = 0; amp[f > 70] *= np.exp(-(f[f > 70] - 70) / 5)
    X = amp * np.exp(1j * rng.uniform(0, 2 * np.pi, len(f)))
    x = np.fft.irfft(X, n)
    t = np.arange(n) / fs
    return t, x / np.std(x) * uv / 2.5


def window_trace(t, x, start, win, O, w, h_per_uv, col=None, sw=2.5):
    """finestra [start, start+win) di un segnale periodico (con avvolgimento): per EEG che scorre."""
    D = t[-1] + (t[1] - t[0]); fs = 1 / (t[1] - t[0])
    k0 = int(round((start % D) * fs)); nw = int(round(win * fs))
    idx = (k0 + np.arange(nw)) % len(x)
    xs = np.arange(nw) / nw * w
    pts = [np.asarray(O, float) + p2(a, b * h_per_uv) for a, b in zip(xs, x[idx])]
    return VMobject(color=col or P.V, stroke_width=sw).set_points_as_corners(pts)
