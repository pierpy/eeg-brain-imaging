from base import *
import figs6 as F6
from scipy.signal import welch


def curve(pts, col, sw=3, smooth=False):
    m = VMobject(color=col, stroke_width=sw)
    return m.set_points_smoothly(pts) if smooth else m.set_points_as_corners(pts)


class A6_Fourier(Base):
    start_num = 1

    def construct(self):
        # ---------------------------------------------------------- 1 copertina
        self.new(first=True); self.num = 1
        hc = np.array([5.7, -2.35, 0]); Rh = 0.95
        sigs = [E.periodic_eeg(4.0, seed=s, peaks=((f0, 1.0, 1.2), (20.0, 2.0, 0.3)), uv=20) for s, f0 in ((61, 10.0), (62, 6.0), (63, 12.0))]
        Os = [np.array([2.0, -1.75 - 0.6 * k, 0]) for k in range(3)]
        cols = [TEAL, ACC, AMB]

        def vis():
            hd = VGroup(E.head(hc, Rh), E.electrodes(hc, Rh, r=0.04))
            tr0 = VGroup(*[E.window_trace(t, x, 0.0, 1.5, O, 2.6, 0.012, c, 1.8) for (t, x), O, c in zip(sigs, Os, cols)])
            self.play(FadeIn(hd), Create(tr0), run_time=1.2)
            self.tr0 = tr0
        copertina(self, tr("Lecture 6", "Lezione 6"), tr("Spectral and\ntime-frequency analysis", "Analisi spettrale\ne tempo-frequenza"), vis)
        scroll_many(self, sigs, Os, 2.6, 0.012, 1.5, cols, 4.0, 1.8, old=self.tr0)

        # ---------------------------------------------------------- 2 obiettivi
        self.new(tr("Lecture 6", "Lezione 6"), tr("Today: rhythms as numbers", "Oggi: i ritmi diventano numeri"))
        g = rows_mob([tr("The ++Fourier transform++: resolution, Nyquist, leakage, windows.", "La ++trasformata di Fourier++: risoluzione, Nyquist, leakage, finestre."),
                      tr("*Power spectrum* estimation: Welch, multitaper, 1/f vs peaks.", "Stima dello *spettro di potenza*: Welch, multitaper, 1/f vs picchi."),
                      tr("*Time-frequency* analysis: STFT, Morlet wavelets, baseline, ERD/ERS.", "Analisi *tempo-frequenza*: STFT, wavelet di Morlet, baseline, ERD/ERS."),
                      tr("*Evoked* vs *induced* activity; ++phase++ and ITPC.", "Attività *evocata* vs *indotta*; ++fase++ e ITPC."),
                      tr("++Cross-frequency coupling++ and common pitfalls.", "++Accoppiamento tra frequenze++ e trappole comuni.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 3 il prisma: EEG -> bande
        self.new(tr("Why frequency?", "Perché la frequenza?"), tr("The EEG speaks in rhythms", "L'EEG parla per ritmi"))
        D = 2.0; fs = 250; t = np.arange(0, D, 1 / fs)
        bands = [(2.0, 1.0, PURP, "δ 2 Hz"), (6.0, 0.7, AMB, "θ 6 Hz"), (10.0, 1.1, ACC, "α 10 Hz"), (20.0, 0.45, TEAL, "β 20 Hz")]
        comps = [a * np.sin(2 * np.pi * f * t + k) for k, (f, a, c, n) in enumerate(bands)]
        xin = sum(comps)
        pc = np.array([-2.3, 0.35, 0])
        prism = Polygon(pc + np.array([-0.55, -0.7, 0]), pc + np.array([0.55, -0.7, 0]), pc + np.array([0, 0.75, 0]), color=FG, stroke_width=3, fill_color=FG, fill_opacity=0.12)
        Oi = np.array([-6.4, 0.35, 0]); Wi = 3.4
        Oo = [np.array([-1.2, 1.65 - 0.85 * k, 0]) for k in range(4)]; Wo = 3.0
        rays = VGroup(*[Line(pc + np.array([0.3, 0, 0]), O_ + np.array([-0.1, 0, 0]), color=c, stroke_width=2, stroke_opacity=0.6) for O_, (f, a, c, n) in zip(Oo, bands)])
        labs = VGroup(*[T(n, 16, c).move_to(O_ + np.array([Wo + 0.6, 0, 0])) for O_, (f, a, c, n) in zip(Oo, bands)])
        sigs = [(t, xin)] + [(t, x) for x in comps]
        Os = [Oi] + Oo; cols = [FG] + [c for f, a, c, n in bands]; Ws = [Wi] + [Wo] * 4; hs = [0.28] + [0.28] * 4
        win = 1.0

        def live(u):
            return VGroup(*[E.window_trace(tt, x, u * D, win, O_, W_, h, c, 2) for (tt, x), O_, W_, h, c in zip(sigs, Os, Ws, hs, cols)])
        l0 = live(0.0)
        self.play(Create(l0[0]), run_time=1.0)
        self.play(DrawBorderThenFill(prism), run_time=0.8)
        self.play(Create(rays), *[Create(x) for x in l0[1:]], FadeIn(labs), run_time=1.5)
        bl = bullets([tr("Oscillations = ++synchronised populations++ (Lecture 3).", "Oscillazioni = ++popolazioni sincronizzate++ (Lezione 3)."),
                      tr("Bands have different ++generators and functions++.", "Le bande hanno ++generatori e funzioni++ diversi."),
                      tr("Spectra ++summarise++ long recordings.", "Gli spettri ++riassumono++ registrazioni lunghe."),
                      tr("TF shows ++when++ rhythms change.", "Il TF mostra ++quando++ cambiano i ritmi.")], 17, n=26, gap=0.28).move_to(np.array([4.9, 0.3, 0]))
        mt = metaphor(tr("a ++prism++ splits white light into colours; Fourier splits the EEG into rhythms.", "un ++prisma++ scompone la luce bianca nei colori; Fourier scompone l'EEG nei ritmi."), 17).move_to(np.array([0, -2.95, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.4)
        self.play(FadeIn(mt))
        loop_start(self)
        ph = ValueTracker(0.0)
        lz = always_redraw(lambda: live(ph.get_value()))
        self.remove(l0); self.add(lz); loop_play(self, ph, 6.0); lz.clear_updaters()

        # ---------------------------------------------------------- 4 sezione
        self.new(); section_title(self, 1, tr("From time to frequency", "Dal tempo alla frequenza"))

        # ---------------------------------------------------------- 5 Fourier: epicicli che disegnano il segnale
        self.new(tr("Fourier (1)", "Fourier (1)"), tr("Any signal is a sum of sinusoids", "Ogni segnale è una somma di sinusoidi"))
        comp = [(2, 1.0, 0.3, PURP), (10, 0.8, 1.1, ACC), (21, 0.35, 2.0, TEAL)]
        sc = 0.55; cen = np.array([-5.0, 0.2, 0]); Wtr = 5.0; x0 = -3.2
        uT = ValueTracker(0.0)   # tempo in secondi (periodo 1 s)
        tt_ = np.linspace(0, 1, 400)
        ysig = lambda tt: sum(a * np.sin(2 * np.pi * f * tt + p) for f, a, p, c in comp)

        def epi():
            u = uT.get_value()
            g = VGroup(); p = cen.copy()
            for f, a, ph0, c in comp:
                ang = 2 * np.pi * f * u + ph0
                q = p + sc * a * np.array([np.cos(ang), np.sin(ang), 0])
                g.add(Circle(radius=sc * a, color=c, stroke_width=1.5, stroke_opacity=0.6).move_to(p), Line(p, q, color=c, stroke_width=3.5))
                p = q
            # traccia: il passato scorre verso destra
            past = [np.array([x0 + (1 - s) * 0 + s * Wtr, cen[1] + sc * ysig(u - s), 0]) for s in np.linspace(0, 1, 300)]
            g.add(DashedLine(p, np.array([x0, p[1], 0]), color=MUT, stroke_width=1.5))
            g.add(VMobject(color=FG, stroke_width=3).set_points_as_corners(past))
            g.add(Dot(np.array([x0, p[1], 0]), radius=0.06, color=FG))
            return g
        ez = always_redraw(epi)
        # spettro a barre
        Os_ = np.array([3.0, -1.5, 0])
        sax = E.axes(Os_, 3.3, 2.6, "Hz", tr("amplitude", "ampiezza"))
        bars = VGroup(*[VGroup(Line(Os_ + np.array([f / 25 * 3.0, 0, 0]), Os_ + np.array([f / 25 * 3.0, a * 2.2, 0]), color=c, stroke_width=8), T(f"{f}", 14, c).move_to(Os_ + np.array([f / 25 * 3.0, -0.25, 0]))) for f, a, p, c in comp])
        self.play(FadeIn(ez), run_time=1.0)
        self.play(Create(sax), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.2), run_time=1.2)
        fm = fcard(r"X(f)=\sum_n x(n)\,e^{-i2\pi f n/f_s}", CARD2, 0.75).move_to(np.array([4.4, 1.9, 0]))
        cap = T(tr("amplitude |X(f)| and phase ∠X(f) of each rotating arm; power = |X(f)|²", "ampiezza |X(f)| e fase ∠X(f) di ogni braccio rotante; potenza = |X(f)|²"), 17, n=100).move_to(np.array([0, -2.75, 0]))
        self.play(FadeIn(fm), FadeIn(cap))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: uT.set_value(ph.get_value()))
        self.add(drv); loop_play(self, ph, 10.0); drv.clear_updaters(); ez.clear_updaters()

        # ---------------------------------------------------------- 6 risoluzione: finestra che si allunga
        self.new(tr("Fourier (2)", "Fourier (2)"), tr("Frequency resolution: Δf = 1/T", "Risoluzione in frequenza: Δf = 1/T"))
        TT = ValueTracker(0.5)
        Ot = np.array([-6.3, 1.25, 0]); Wt_ = 12.6
        tfull = np.arange(0, 3.0, 1 / 250)
        xfull = np.sin(2 * np.pi * 10 * tfull) + 0.8 * np.sin(2 * np.pi * 11 * tfull + 1)
        sig = E.trace(tfull, xfull, Ot, Wt_, 0.28, MUT, 1.3)
        Osp = np.array([-3.0, -2.4, 0]); Wsp = 6.0; Hsp = 2.4

        def res():
            T_ = TT.get_value()
            fr, X = F6.two_peaks(T_)
            m = (fr >= 5) & (fr <= 16)
            g = VGroup(Rectangle(width=T_ / 3.0 * Wt_, height=0.9, stroke_width=0, fill_color=AMB, fill_opacity=0.2).move_to(Ot + np.array([T_ / 3.0 * Wt_ / 2, 0, 0])))
            g.add(E.trace(tfull[tfull < T_], xfull[tfull < T_], Ot, T_ / 3.0 * Wt_, 0.28, TEAL, 2.2, 0, T_))
            g.add(curve([Osp + np.array([(a - 5) / 11 * Wsp, Hsp * b, 0]) for a, b in zip(fr[m], X[m])], ACC, 3.5, True))
            g.add(T(f"T = **{dec(T_, 2)} s**  →  Δf = **{dec(1 / T_, 2)} Hz**", 22, AMB).move_to(np.array([0, 0.25, 0])))
            return g
        axs = VGroup(E.axes(Osp, Wsp + 0.2, Hsp + 0.3, "Hz", ""), *[DashedLine(Osp + np.array([(v - 5) / 11 * Wsp, 0, 0]), Osp + np.array([(v - 5) / 11 * Wsp, Hsp + 0.1, 0]), color=MUT, stroke_width=1.2) for v in (10, 11)],
                     *[T(str(v), 13, MUT).move_to(Osp + np.array([(v - 5) / 11 * Wsp, -0.25, 0])) for v in (5, 10, 11, 15)])
        rz = always_redraw(res)
        self.play(Create(sig), Create(axs), FadeIn(rz), run_time=1.2)
        bl = bullets([tr("Longer windows → ++finer++ resolution.", "Finestre più lunghe → risoluzione ++più fine++."),
                      tr("f_{s} sets only the ++maximum++ frequency (f_{s}/2).", "f_{s} fissa solo la frequenza ++massima++ (f_{s}/2)."),
                      tr("Zero-padding ++smooths++, it does not resolve.", "Lo zero-padding ++liscia++, non risolve.")], 17, n=30, gap=0.28).move_to(np.array([5.0, -1.3, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.4)
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: TT.set_value(0.4 * (3.0 / 0.4) ** (0.5 - 0.5 * np.cos(2 * np.pi * ph.get_value()))))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); rz.clear_updaters()

        # ---------------------------------------------------------- 7 leakage: stem DFT rettangolare vs Hann
        self.new(tr("Fourier (3)", "Fourier (3)"), tr("Spectral leakage and tapers", "Leakage spettrale e finestre"))
        f0T = ValueTracker(10.0)
        N = 250; tn = np.arange(N) / 250.0
        Wb = 5.2; Hb = 2.6
        Ops = [np.array([-6.2, -1.6, 0]), np.array([0.6, -1.6, 0])]
        yy = lambda d: (max(d, -60) + 60) / 60 * Hb

        def stems():
            f0 = f0T.get_value()
            x = np.sin(2 * np.pi * f0 * tn)
            g = VGroup()
            for k, (w, col) in enumerate(((np.ones(N), ACC), (np.hanning(N), TEAL))):
                X = np.abs(np.fft.rfft(x * w)); X = X / X.max(); D_ = 20 * np.log10(X + 1e-9)
                O_ = Ops[k]
                for fk in range(0, 21):
                    xx = O_ + np.array([fk / 20 * Wb, 0, 0])
                    g.add(Line(xx, xx + np.array([0, yy(D_[fk]), 0]), color=col, stroke_width=4), Dot(xx + np.array([0, yy(D_[fk]), 0]), radius=0.05, color=col))
            g.add(T(tr(f"sine at **{dec(f0, 2)} Hz**, T = 1 s (bins every 1 Hz)", f"sinusoide a **{dec(f0, 2)} Hz**, T = 1 s (bin ogni 1 Hz)"), 20, AMB).move_to(np.array([0, 1.95, 0])))
            return g
        axl = VGroup()
        for k, lab in enumerate((tr("rectangular window", "finestra rettangolare"), tr("Hann window", "finestra di Hann"))):
            O_ = Ops[k]
            axl.add(Line(O_, O_ + np.array([Wb + 0.2, 0, 0]), color=MUT, stroke_width=1.5), T(lab, 17, ACC if k == 0 else TEAL).move_to(O_ + np.array([Wb / 2, Hb + 0.4, 0])),
                    *[T(str(v), 13, MUT).move_to(O_ + np.array([v / 20 * Wb, -0.25, 0])) for v in (0, 10, 20)],
                    T("0 dB", 12, MUT).move_to(O_ + np.array([-0.4, Hb, 0])), T("−60", 12, MUT).move_to(O_ + np.array([-0.4, 0.05, 0])))
        sz = always_redraw(stems)
        self.play(FadeIn(axl), FadeIn(sz), run_time=1.0)
        cap = T(tr("Off-bin frequencies ++leak++ into all bins with a hard cut; a ++taper++ keeps the energy close to the true frequency.", "Le frequenze tra un bin e l'altro ++si disperdono++ su tutti i bin con un taglio netto; una ++finestra++ tiene l'energia vicino alla frequenza vera."), 17, n=110).move_to(np.array([0, -2.45, 0]))
        mt = metaphor(tr("a ++hard photo frame++ creates false edges; a soft vignette does not.", "una ++cornice netta++ crea falsi bordi; una sfumatura morbida no."), 16).move_to(np.array([0, -3.15, 0]))
        self.play(FadeIn(cap), FadeIn(mt))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: f0T.set_value(10.5 - 0.5 * np.cos(2 * np.pi * ph.get_value())))
        self.add(drv); loop_play(self, ph, 6.0); drv.clear_updaters(); sz.clear_updaters()

        # ---------------------------------------------------------- 8 sezione
        self.new(); section_title(self, 2, tr("Estimating the power spectrum", "Stimare lo spettro di potenza"))

        # ---------------------------------------------------------- 9 Welch: segmenti che si accumulano nella media
        self.new(tr("Spectrum (1)", "Spettro (1)"), tr("Welch's method: average to reduce variance", "Metodo di Welch: mediare per ridurre la varianza"))
        t, x = F6.rest_signal(60.0)
        seg = 500; step = 250; starts = np.arange(0, len(x) - seg + 1, step)
        hw = np.hanning(seg)
        fr = np.fft.rfftfreq(seg, 1 / 250)
        PS = np.array([np.abs(np.fft.rfft(x[s:s + seg] * hw)) ** 2 for s in starts])
        m = (fr >= 1) & (fr <= 40)
        cum = np.cumsum(PS, 0) / np.arange(1, len(PS) + 1)[:, None]
        lo, hi = np.log10(PS[:, m].min()) + 1.5, np.log10(PS[:, m].max())
        Ow = np.array([-6.3, 1.55, 0]); Ww = 12.6
        top = E.trace(t, x, Ow, Ww, 0.012, MUT, 0.8)
        Osp = np.array([-5.8, -2.6, 0]); Wsp = 6.8; Hsp = 3.0
        yy = lambda v: np.clip((np.log10(v) - lo) / (hi - lo), 0, 1.05) * Hsp
        kT = ValueTracker(0)

        def wl():
            k = int(kT.get_value())
            s0 = starts[k] / 250.0
            g = VGroup(Rectangle(width=2.0 / 60 * Ww, height=0.8, stroke_width=0, fill_color=AMB, fill_opacity=0.3).move_to(Ow + np.array([(s0 + 1.0) / 60 * Ww, 0, 0])))
            g.add(curve([Osp + np.array([(a - 1) / 39 * Wsp, yy(b), 0]) for a, b in zip(fr[m], PS[k][m])], MUT, 1.5))
            g.add(curve([Osp + np.array([(a - 1) / 39 * Wsp, yy(b), 0]) for a, b in zip(fr[m], cum[k][m])], ACC, 4))
            g.add(T(tr(f"average of **{k + 1}** segments", f"media di **{k + 1}** segmenti"), 20, ACC).move_to(Osp + np.array([Wsp / 2, Hsp + 0.35, 0])))
            return g
        axw = VGroup(E.axes(Osp, Wsp + 0.2, Hsp + 0.2, tr("frequency (Hz)", "frequenza (Hz)"), ""), *[T(str(v), 13, MUT).move_to(Osp + np.array([(v - 1) / 39 * Wsp, -0.25, 0])) for v in (1, 10, 20, 30, 40)])
        wz = always_redraw(wl)
        self.play(Create(top), Create(axw), FadeIn(wz), run_time=1.2)
        bl = bullets([tr("One periodogram is ++noisy++, whatever the length.", "Un periodogramma è ++rumoroso++, qualunque sia la durata."),
                      tr("*Welch*: overlapping tapered segments, ++average++ their power.", "*Welch*: segmenti sovrapposti e finestrati, ++mediarne++ la potenza."),
                      tr("Shorter segments: more averages, ++coarser++ Δf.", "Segmenti più corti: più medie, Δf ++più grossolana++."),
                      tr("MATLAB: pwelch(x, hann(2*fs), fs, [], fs)", "MATLAB: pwelch(x, hann(2*fs), fs, [], fs)")], 16, n=32, gap=0.26).move_to(np.array([4.4, -0.9, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.4)
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: kT.set_value(min(int(ph.get_value() * len(starts)), len(starts) - 1)))
        self.add(drv); loop_play(self, ph, 10.0); drv.clear_updaters(); wz.clear_updaters()

        # ---------------------------------------------------------- 10 multitaper e unità
        self.new(tr("Spectrum (2)", "Spettro (2)"), tr("Multitaper and units", "Multitaper e unità di misura"))
        kinds = [(tr("Multitaper", "Multitaper"), tr("several orthogonal ++Slepian++ tapers on the same data, averaged: low variance, controlled smoothing ±W (Thomson, 1982).", "più finestre ++Slepian++ ortogonali sugli stessi dati, mediate: bassa varianza, smoothing controllato ±W (Thomson, 1982).")),
                 (tr("Absolute power", "Potenza assoluta"), tr("µV²/Hz or µV² per band; depends on skull, impedance, reference.", "µV²/Hz o µV² per banda; dipende da cranio, impedenza, riferimento.")),
                 (tr("Relative power", "Potenza relativa"), tr("band / total: removes global scaling, but bands become ++interdependent++.", "banda / totale: toglie la scala globale, ma le bande diventano ++interdipendenti++.")),
                 (tr("Log / dB", "Log / dB"), tr("power is ++skewed++: log10 or 10·log10(P/P_{ref}) is closer to Gaussian.", "la potenza è ++asimmetrica++: log10 o 10·log10(P/P_{rif}) è più vicino alla gaussiana."))]
        cs = VGroup()
        for k, (h_, d_) in enumerate(kinds):
            box = RoundedRectangle(corner_radius=0.14, width=3.0, height=2.9, fill_color=CARD if k % 2 == 0 else CARD2, fill_opacity=1, stroke_width=0)
            tx = VGroup(TX(h_, font=BODY, font_size=20, color=TEAL, weight=BOLD), T(d_, 16, n=28)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            tx.move_to(box).align_to(box, UP).shift(DOWN * 0.25)
            cs.add(VGroup(box, tx))
        cs.arrange(RIGHT, buff=0.2).move_to(np.array([0, 0.55, 0]))
        for c_ in cs: self.play(FadeIn(c_, shift=UP * 0.15), run_time=0.4)
        nt = card(T(tr("Report: method, segment length, overlap, taper, Δf, units. ~Plot spectra on log axes.~", "Riportare: metodo, lunghezza dei segmenti, sovrapposizione, finestra, Δf, unità. ~Spettri su assi log.~"), 18, n=110)).move_to(np.array([0, -2.3, 0]))
        self.play(FadeIn(nt))

        # ---------------------------------------------------------- 11 picchi su fondo 1/f (parametri che cambiano)
        self.new(tr("Spectrum (3)", "Spettro (3)"), tr("Peaks on a 1/f background", "Picchi su un fondo 1/f"))
        fr = np.linspace(1, 40, 250)
        Wf = 5.2; Hf = 2.6
        lx = lambda v: E.logpos(v, 1, 40, Wf)
        O1 = np.array([-6.2, -1.5, 0]); O2 = np.array([0.8, -1.5, 0])
        chiT = ValueTracker(1.5); aT = ValueTracker(0.9)

        def spec():
            chi = chiT.get_value(); a = aT.get_value()
            ap = 2.2 - chi * np.log10(fr)
            pk = a * np.exp(-0.5 * ((fr - 10) / 1.3) ** 2) + 0.3 * np.exp(-0.5 * ((fr - 20) / 2.5) ** 2)
            y1 = lambda v: (v + 0.8) / 3.4 * Hf; y2 = lambda v: v / 1.5 * Hf
            g = VGroup(curve([O1 + np.array([lx(f), y1(v), 0]) for f, v in zip(fr, ap + pk)], TEAL, 3.5, True),
                       DashedLine(O1 + np.array([lx(1), y1(ap[0]), 0]), O1 + np.array([lx(40), y1(ap[-1]), 0]), color=ACC, stroke_width=3),
                       curve([O2 + np.array([lx(f), y2(v), 0]) for f, v in zip(fr, pk)], TEAL, 3.5, True))
            g.add(T(f"χ = **{dec(chi, 2)}**", 20, ACC).move_to(O1 + np.array([Wf * 0.75, Hf + 0.35, 0])))
            g.add(T(tr(f"alpha peak = **{dec(a, 2)}**", f"picco alfa = **{dec(a, 2)}**"), 20, TEAL).move_to(O2 + np.array([Wf * 0.7, Hf + 0.35, 0])))
            return g
        axf = VGroup(E.axes(O1, Wf + 0.2, Hf + 0.2, tr("Hz (log)", "Hz (log)"), tr("log power", "log potenza")), E.axes(O2, Wf + 0.2, Hf + 0.2, tr("Hz (log)", "Hz (log)"), tr("minus aperiodic", "meno aperiodica")),
                     *[T(str(v), 13, MUT).move_to(O_ + np.array([lx(v), -0.25, 0])) for O_ in (O1, O2) for v in (1, 4, 10, 20, 40)])
        sz = always_redraw(spec)
        self.play(Create(axf), FadeIn(sz), run_time=1.2)
        cap = T(tr("\"Band power\" changes can come from ++peaks++ or from the ++slope/offset++: separate them (specparam/FOOOF, Donoghue et al., 2020).", "I cambiamenti di \"potenza di banda\" possono venire dai ++picchi++ o da ++pendenza/offset++: separarli (specparam/FOOOF, Donoghue et al., 2020)."), 17, n=110).move_to(np.array([0, -2.75, 0]))
        self.play(FadeIn(cap))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: (chiT.set_value(1.5 + 0.35 * np.sin(2 * np.pi * ph.get_value())), aT.set_value(0.9 + 0.5 * np.cos(2 * np.pi * ph.get_value()))))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); sz.clear_updaters()

        # ---------------------------------------------------------- 12 potenza di banda e IAF (persone diverse)
        self.new(tr("Spectrum (4)", "Spettro (4)"), tr("Band power and individual frequencies", "Potenza di banda e frequenze individuali"))
        fr = np.linspace(2, 20, 300)
        Wa = 7.0; Ha = 3.0; Oa = np.array([-6.2, -2.0, 0])
        iafT = ValueTracker(10.0)
        xf = lambda v: (v - 2) / 18 * Wa

        def iaf():
            p = iafT.get_value()
            L = 1.0 - 0.8 * np.log10(fr) + 1.4 * np.exp(-0.5 * ((fr - p) / 1.1) ** 2)
            y = lambda v: (v + 0.3) / 2.6 * Ha
            g = VGroup()
            g.add(Rectangle(width=xf(13) - xf(8), height=Ha, stroke_width=0, fill_color=MUT, fill_opacity=0.18).move_to(Oa + np.array([(xf(8) + xf(13)) / 2, Ha / 2, 0])))
            g.add(Rectangle(width=xf(p + 2) - xf(p - 2), height=Ha, stroke_width=2, stroke_color=ACC, fill_color=ACC, fill_opacity=0.12).move_to(Oa + np.array([(xf(p - 2) + xf(p + 2)) / 2, Ha / 2, 0])))
            g.add(curve([Oa + np.array([xf(f), y(v), 0]) for f, v in zip(fr, L)], TEAL, 3.5, True))
            g.add(DashedLine(Oa + np.array([xf(p), 0, 0]), Oa + np.array([xf(p), Ha, 0]), color=ACC, stroke_width=2))
            g.add(T(f"IAF = **{dec(p, 1)} Hz**", 20, ACC).move_to(Oa + np.array([xf(p), Ha + 0.3, 0])))
            return g
        axa = VGroup(E.axes(Oa, Wa + 0.2, Ha + 0.2, "Hz", ""), *[T(str(v), 13, MUT).move_to(Oa + np.array([xf(v), -0.25, 0])) for v in (2, 4, 8, 13, 20)],
                     T(tr("grey: fixed 8–13 Hz · orange: IAF ± 2 Hz", "grigio: fisso 8–13 Hz · arancio: IAF ± 2 Hz"), 15, MUT).move_to(Oa + np.array([Wa / 2, -0.65, 0])))
        iz = always_redraw(iaf)
        self.play(Create(axa), FadeIn(iz))
        fm = fcard(r"P_{band}=\sum_{f\in band}P(f)\,\Delta f", CARD2, 0.75).move_to(np.array([4.2, 1.35, 0]))
        bl = bullets([tr("Fixed bands are ++conventions++: IAF ≈ 8–12 Hz, lower with age.", "Le bande fisse sono ++convenzioni++: IAF ≈ 8–12 Hz, più bassa con l'età."),
                      tr("Use ++individually adjusted++ bands (Klimesch, 1999; Corcoran et al., 2018).", "Usare bande ++adattate all'individuo++ (Klimesch, 1999; Corcoran et al., 2018)."),
                      tr("Ratios (θ/β, α asymmetry) are ++fragile++.", "I rapporti (θ/β, asimmetria α) sono ++fragili++.")], 16, n=34, gap=0.26).move_to(np.array([4.3, -0.9, 0]))
        self.play(FadeIn(fm))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.4)
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: iafT.set_value(10.0 - 1.6 * np.sin(2 * np.pi * ph.get_value())))
        self.add(drv); loop_play(self, ph, 6.0); drv.clear_updaters(); iz.clear_updaters()
        self.end()


def dec(v, n=2):
    s = f"{v:.{n}f}"
    return s if LANG == "en" else s.replace(".", ",")
