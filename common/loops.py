"""Strumenti per slide "in movimento continuo" (segmenti in loop di manim-slides).

Uso tipico dentro construct(), alla FINE della costruzione di una slide:

    loop_start(self)                    # la slide di costruzione passa da sola al loop
    ph = ValueTracker(0.0)              # fase 0 -> 1 in un periodo
    m = always_redraw(lambda: build(ph.get_value()))   # build(0) == build(1) == stato attuale
    self.remove(<versione statica>); self.add(m)
    loop_play(self, ph, T=4.0)
    m.clear_updaters()

Il segmento in loop viene ripetuto finché il docente non preme "avanti".
Perché il loop non abbia scatti, lo stato a fase 1 deve coincidere con quello a fase 0.
"""
import numpy as np
from manim import ValueTracker, linear


def loop_start(self):
    """Chiude la parte "costruzione" della slide corrente (che avanza da sola) e apre un segmento in loop."""
    cfg = self._base_slide_config
    try:
        cfg.auto_next = True
    except Exception:
        object.__setattr__(cfg, "auto_next", True)
    self.next_slide(loop=True)


def loop_play(self, ph, T=4.0, *extra):
    """Porta la fase ph da 0 a 1 in T secondi (lineare), con eventuali altre animazioni in parallelo."""
    ph.set_value(0.0)
    self.play(ph.animate.set_value(1.0), *extra, run_time=T, rate_func=linear)


def tri(x):
    """Onda triangolare di periodo 2 con valori in [0, 1]: coordinata che rimbalza tra due pareti."""
    x = np.mod(x, 2.0)
    return np.where(x > 1.0, 2.0 - x, x)


class PeriodicGas:
    """Gas 2D (coordinate normalizzate in [0,1]^2) con moto ESATTAMENTE periodico di periodo T:
    le componenti di velocità normalizzate sono multipli di 2/T, quindi ogni molecola torna
    nella stessa posizione dopo T secondi (urti elastici con le pareti)."""

    def __init__(self, p, u, T):
        self.T = T
        p = np.clip(np.asarray(p, float), 0.0, 1.0)
        u = np.asarray(u, float)
        q = 2.0 / T
        k = np.round(u / q)
        k[k == 0] = np.where(u[k == 0] >= 0, 1, -1)
        self.u = k * q
        self.s0 = p.copy()                    # coordinata "srotolata": tri(s0) = p

    @classmethod
    def from_velocities(cls, p, v, W, H, T, speed=1.0):
        """p: posizioni normalizzate (N,2); v: velocità in unità di scena al secondo."""
        u = np.asarray(v, float) * speed / np.array([W, H])
        return cls(p, u, T)

    def pos(self, phase):
        """posizioni normalizzate alla fase phase in [0,1]."""
        return tri(self.s0 + self.u * phase * self.T)

    def vel_sign(self, phase):
        """segno della velocità effettiva (per disegnare frecce coerenti)."""
        s = np.mod(self.s0 + self.u * phase * self.T, 2.0)
        return np.where(s > 1.0, -1.0, 1.0) * np.sign(self.u)


def loop_gas(self, items, T=8.0):
    """Mette in loop (periodo T) uno o più gas già sulla scena.
    items: lista di (gas, W, H, mob_statico, builder); il gas ha attributi p (N,2 normalizzate) e v (N,2);
    builder() ridisegna il gas leggendo gas.p e gas.v (es. la lambda usata con always_redraw)."""
    from manim import always_redraw
    loop_start(self)
    ph = ValueTracker(0.0)
    lives = []
    for g, W, H, mob, b in items:
        pg = PeriodicGas.from_velocities(g.p, g.v, W, H, T)
        vabs = np.abs(pg.u) * np.array([W, H])

        def mk(g=g, pg=pg, vabs=vabs, b=b):
            def f():
                x = ph.get_value()
                g.p = pg.pos(x)
                g.v = vabs * pg.vel_sign(x)
                return b()
            return always_redraw(f)
        live = mk()
        if mob is not None:
            self.remove(mob)
        self.add(live)
        lives.append(live)
    loop_play(self, ph, T)
    for l in lives:
        l.clear_updaters()
    return lives


def loop_packets(self, streams, T=4.0, extra_live=()):
    """Loop di "pacchetti" (puntini) che scorrono lungo percorsi: flussi di energia, di fluido, di calore...
    streams: lista di (percorso VMobject, n_pacchetti, colore_o_funzione(prop)->colore, raggio).
    extra_live: altri mobject always_redraw già costruiti in funzione di una fase (verranno ignorati).
    Il moto è periodico: ogni pacchetto percorre l'intero percorso in T secondi."""
    from manim import always_redraw, Dot, VGroup
    loop_start(self)
    ph = ValueTracker(0.0)

    def build():
        g = VGroup()
        x = ph.get_value()
        for path, n, col, r in streams:
            for j in range(n):
                s = (x + j / n) % 1.0
                c = col(s) if callable(col) else col
                g.add(Dot(path.point_from_proportion(s), radius=r, color=c))
        return g
    live = always_redraw(build)
    self.add(live)
    loop_play(self, ph, T)
    live.clear_updaters()
    return live


def polyline(*pts):
    from manim import VMobject
    return VMobject().set_points_as_corners([np.asarray(p, float) for p in pts])
