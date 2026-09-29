"""Mattoni comuni delle presentazioni manim-slides del corso EEG (bilingue: EEG_LANG=en|it)."""
import os as _os
_R = _os.environ.get("COURSE_ROOT") or _os.path.dirname(_os.path.abspath(__file__))
while not _os.path.exists(_os.path.join(_R, ".course_root")) and _os.path.dirname(_R) != _R:
    _R = _os.path.dirname(_R)
import re, sys, os
sys.path.insert(0, _R + "/common"); sys.path.insert(0, _R + "/common"); sys.path.insert(0, _R + "/common"); sys.path.insert(0, _R + "/common")
import numpy as np
from manim import *
from manim_slides import Slide
import figs
figs.set_theme(dark=True)
P = figs.P
import eegfigs as E

config.background_color = P.bg
FOOTER = "Brain Imaging · EEG"
LANG = os.environ.get("EEG_LANG", "en")
def tr(en, it):
    return it if LANG == "it" else en
def set_footer(s):
    global FOOTER
    FOOTER = s
BODY = "Carlito"; SERIF_F = "Caladea"
ACC, TEAL, AMB, FG, MUT = P.S, P.V, P.C, P.fg, P.muted
CARD = "#223057"; CARD2 = "#3A2A2E"

# ------------------------------------------------ markup -> Pango
def md(s):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    rules = [
        (r"_\{(.+?)\}", r"<sub>\1</sub>"), (r"\^\{(.+?)\}", r"<sup>\1</sup>"),
        (r"_([A-Za-z0-9])", r"<sub>\1</sub>"), (r"\^([A-Za-z0-9])", r"<sup>\1</sup>"),
        (r"\*\*(.+?)\*\*", r"<b>\1</b>"),
        (r"\*(.+?)\*", rf'<span foreground="{ACC}"><i>\1</i></span>'),
        (r"~(.+?)~", rf'<span foreground="{TEAL}"><b>\1</b></span>'),
        (r"\+\+(.+?)\+\+", r"<u>\1</u>"),
        (r"!(.+?)!", rf'<span font_family="{SERIF_F}"><b><i>\1</i></b></span>'),
        (r"\$(.+?)\$", rf'<span font_family="{SERIF_F}"><i>\1</i></span>'),
    ]
    for a, b in rules:
        s = re.sub(a, b, s)
    return s

def wrap(markup, n):
    """a capo automatico su una stringa Pango, contando solo i caratteri visibili."""
    toks = re.findall(r"<[^>]+>|[^<\s]+|\s+", markup)
    out, line = [], 0
    for t in toks:
        if t.startswith("<"):
            out.append(t); continue
        if t.isspace():
            out.append(" "); line += 1; continue
        vis = len(re.sub(r"&\w+;", "x", t))
        prev = next((x for x in reversed(out) if not x.startswith("<")), " ")
        if line + vis > n and line > 0 and prev == " ":
            while out and out[-1] == " ":
                out.pop()
            out.append("\n"); line = 0
        out.append(t); line += vis
    return "".join(out)

K = 4  # si rende il testo 4 volte più grande e lo si riscala: evita la crenatura irregolare di Pango a corpi piccoli
def T(s, size=28, col=FG, n=60, font=BODY, **kw):
    k = max(1.0, min(K, 3800 / (size * n)))   # MarkupText va a capo da sé oltre una certa larghezza: limito il fattore
    return MarkupText(wrap(md(s), n), font=font, font_size=size * k, color=col, line_spacing=0.9, **kw).scale(1 / k)

def TX(s, font=BODY, font_size=28, **kw):
    k = max(1.0, min(K, 3800 / (font_size * max(len(s), 1))))
    return Text(s, font=font, font_size=font_size * k, **kw).scale(1 / k)

def M(s, col=FG, sc=1.0):
    return MathTex(s, color=col).scale(sc)

def card(mob, col=CARD, pad=0.32, r=0.16):
    box = RoundedRectangle(corner_radius=r, width=mob.width + 2 * pad, height=mob.height + 2 * pad,
                           fill_color=col, fill_opacity=1, stroke_width=0).move_to(mob)
    return VGroup(box, mob)

def fcard(tex, col=CARD, sc=1.0, tcol=FG):
    return card(M(tex, tcol, sc), col)

def bullets(items, size=28, n=56, gap=0.28, width=None):
    """items: stringhe o (stringa, livello). Restituisce VGroup di righe con pallino."""
    rows = VGroup()
    for it in items:
        s, lvl = (it, 0) if isinstance(it, str) else it
        t = T(s, size, n=n - 4 * lvl)
        if lvl >= 0:
            mark = Dot(radius=0.06, color=ACC) if lvl == 0 else Line(ORIGIN, RIGHT * 0.16, color=TEAL, stroke_width=3)
            mark.next_to(t, LEFT, buff=0.22).align_to(t, UP).shift(DOWN * 0.15)
            row = VGroup(mark, t)
        else:
            row = VGroup(t)
        row.shift(RIGHT * 0.45 * max(lvl, 0))
        rows.add(row)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=gap)
    return rows

# ------------------------------------------------ classe base
class Base(Slide):
    start_num = 1
    skip_reversing = True   # niente animazioni "all'indietro": rendering più rapido
    def setup(self):
        super().setup()
        self.num = self.start_num - 1
        self.hdr = VGroup()

    def header(self, tag, title):
        tg = TX(tag.upper(), font=BODY, font_size=18, color=TEAL, weight=BOLD)
        tg.to_corner(UL, buff=0.5)
        tl = TX(title, font=SERIF_F, font_size=42, color=FG, weight=BOLD).next_to(tg, DOWN, aligned_edge=LEFT, buff=0.14)
        return VGroup(tg, tl)

    def footer(self):
        f = TX(FOOTER, font=BODY, font_size=14, color=MUT).to_corner(DL, buff=0.3)
        n = TX(str(self.num), font=BODY, font_size=14, color=MUT).to_corner(DR, buff=0.3)
        return VGroup(f, n)

    def new(self, tag=None, title=None, first=False):
        """chiude la slide precedente e apre la successiva con intestazione."""
        self.num += 1
        if not first:
            self.next_slide()
            ms = [m for m in self.mobjects if isinstance(m, ImageMobject) or m.family_members_with_points()]
            for m in list(self.mobjects):
                if m not in ms: self.remove(m)
            if ms:
                self.play(*[FadeOut(m) for m in ms], run_time=0.5)
        g = VGroup()
        if title:
            g = self.header(tag, title)
            self.play(FadeIn(g, shift=RIGHT * 0.2), FadeIn(self.footer()), run_time=0.6)
        return g

    def remove(self, *mobs):
        """rimuove anche i sotto-oggetti aggiunti singolarmente alla scena (es. con LaggedStart(Create(...)))."""
        fam = []
        for m in mobs:
            fam += m.get_family()
        return super().remove(*fam)

    def step(self):
        self.next_slide()

    # utilità per disegnare una Fig con animazioni sensate
    def draw(self, parts, rt=0.8, lag=0.15):
        anims = []
        for m in parts:
            if isinstance(m, Arrow):
                anims.append(GrowArrow(m))
            elif isinstance(m, (MathTex, Tex, Text, MarkupText)):
                anims.append(Write(m))
            else:
                anims.append(Create(m))
        self.play(LaggedStart(*anims, lag_ratio=lag), run_time=rt * max(1, len(anims) ** 0.5))

    def end(self):
        self.next_slide()
        self.wait(0.1)


def copertina(self, lez, title, visual=None):
    """copertina del corso EEG; visual: funzione che anima un motivo a destra."""
    c1 = TX(tr("MSC IN COMPUTATIONAL COGNITIVE SCIENCE", "CDS MAGISTRALE IN COMPUTATIONAL COGNITIVE SCIENCE"), font=BODY, font_size=20, color=MUT, weight=BOLD).to_corner(UL, buff=0.8)
    c2 = TX("Brain Imaging – Methods and Applications", font=BODY, font_size=30, color=FG).next_to(c1, DOWN, aligned_edge=LEFT, buff=0.18)
    c3 = TX(tr("Module: Electroencephalography (EEG)", "Modulo: Elettroencefalografia (EEG)"), font=BODY, font_size=28, color=FG).next_to(c2, DOWN, aligned_edge=LEFT, buff=0.15)
    l2 = TX(lez, font=BODY, font_size=30, color=ACC, weight=BOLD).next_to(c3, DOWN, aligned_edge=LEFT, buff=0.9)
    ti = VGroup(*[TX(x, font=SERIF_F, font_size=64, color=FG, weight=BOLD) for x in title.split("\n")]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(l2, DOWN, aligned_edge=LEFT, buff=0.15)
    yr = VGroup(TX("Pierpaolo Croce", font=BODY, font_size=30, color=FG, weight=BOLD), TX(tr("A.Y. 2026-2027", "A.A. 2026-2027"), font=BODY, font_size=24, color=MUT)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DL, buff=0.8)
    self.play(FadeIn(VGroup(c1, c2, c3), shift=UP * 0.2), run_time=0.8)
    self.play(FadeIn(l2), Write(ti), FadeIn(yr), run_time=1.2)
    if visual:
        visual()


def licenza(self):
    pass


def fitlive(build, k, cen, ref):
    """always_redraw di una Fig: scala k attorno all'origine e centra il riferimento ref in cen."""
    c0 = ref.group().get_center()
    return always_redraw(lambda: build().group().scale(k, about_point=ORIGIN).shift(cen - k * c0))

def fit(f, k, cen, ref=None):
    c0 = (ref or f).group().get_center()
    for m in f.values():
        m.scale(k, about_point=ORIGIN).shift(cen - k * c0)
    return f

def xform(f, k, cen):
    c0 = f.group().get_center(); sh = cen - k * c0
    return (lambda p: k * np.asarray(p, float) + sh)

def bar(h, col, base, w=0.45, op=0.85):
    return Rectangle(width=w, height=max(h, 0.005), fill_color=col, fill_opacity=op, stroke_width=0).move_to(base, aligned_edge=DOWN)


# ---- movimento continuo (loop)
import sys as _s; _s.path.insert(0, _R + "/common")
from loops import *


def redraw(func):
    """come always_redraw, ma funziona anche con Group che contengono ImageMobject (topografie)."""
    g = Group(*func().submobjects)

    def upd(m):
        new = func()
        m.remove(*m.submobjects)
        m.add(*new.submobjects)
    g.add_updater(upd)
    return g


# ---- mattoni comuni delle scene EEG
PURP = "#8E7CC3"; GRN = "#6FCF97"


def rows_mob(items, size=21, n=70, w=12.2, h=0.78, gap=0.16, col=TEAL):
    g = VGroup()
    for i, s in enumerate(items):
        box = RoundedRectangle(corner_radius=0.12, width=w, height=h, fill_color=CARD if i % 2 == 0 else CARD2, fill_opacity=1, stroke_width=0)
        b = VGroup(Circle(0.21, color=col, fill_opacity=1, stroke_width=0), TX(str(i + 1), font=BODY, font_size=17, color=WHITE, weight=BOLD))
        r = VGroup(b, T(s, size, n=n)).arrange(RIGHT, buff=0.3).move_to(box).align_to(box, LEFT).shift(RIGHT * 0.2)
        g.add(VGroup(box, r))
    g.arrange(DOWN, buff=gap)
    return g


def metaphor(s, size=19, n=100):
    return card(T("~" + tr("Metaphor", "Metafora") + "~  " + s, size, n=n), CARD2)


def section_title(self, n, title):
    num = TX(f"{n:02d}", font=SERIF_F, font_size=110, color=ACC, weight=BOLD).to_edge(LEFT, buff=1.0).shift(UP * 0.6)
    ti = TX(title, font=SERIF_F, font_size=52, color=FG, weight=BOLD).next_to(num, DOWN, aligned_edge=LEFT, buff=0.3)
    self.play(FadeIn(num, shift=RIGHT * 0.3), Write(ti), run_time=1.2)


def refs_slide(self, refs, size=18):
    rb = bullets(refs, size, n=110, gap=0.18).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
    self.play(LaggedStart(*[FadeIn(r_) for r_ in rb], lag_ratio=0.1), run_time=2)


def scroll_many(self, sigs, Os, W, h, win, cols, T_, sw=2.0, old=None, extra=()):
    """più tracce periodiche che scorrono insieme (loop senza scatti); sigs: [(t, x)]."""
    D = sigs[0][0][-1] + (sigs[0][0][1] - sigs[0][0][0])
    loop_start(self)
    ph = ValueTracker(0.0)
    live = always_redraw(lambda: VGroup(*[E.window_trace(t, x, ph.get_value() * D, win, O, W, h, c, sw) for (t, x), O, c in zip(sigs, Os, cols)]))
    if old is not None:
        self.remove(old)
    self.add(live)
    loop_play(self, ph, T_, *extra)
    live.clear_updaters()
    return live


def code_lines(code, size=15, col=None, buff=0.1):
    """righe di codice monospazio con indentazione preservata (Text non conta gli spazi iniziali)."""
    col = col or FG
    ref = Text("M" * 20, font="DejaVu Sans Mono", font_size=size)
    cw = ref.width / 20
    g = VGroup(*[Text(c.strip() or ".", font="DejaVu Sans Mono", font_size=size, color=col) for c in code])
    g.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    for c, m in zip(code, g):
        m.shift(RIGHT * cw * (len(c) - len(c.lstrip(" "))))
    return g
