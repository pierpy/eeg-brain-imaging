from base import *
import figs7 as F7


def dec(v, n=2):
    s = f"{v:.{n}f}"
    return s if LANG == "en" else s.replace(".", ",")


def wv(t, x, O, W, h, col, sw=3, t0=-0.2, t1=0.8):
    m = (t >= t0) & (t <= t1)
    return VMobject(color=col, stroke_width=sw).set_points_as_corners([O + np.array([(a - t0) / (t1 - t0) * W, h * b, 0]) for a, b in zip(t[m], x[m])])


def wax(O, W, H, t0=-0.2, t1=0.8, ticks=(0, 200, 400, 600), sz=13):
    X = lambda tt: O + np.array([(tt - t0) / (t1 - t0) * W, 0, 0])
    g = VGroup(Line(X(t0), X(t1), color=MUT, stroke_width=1.5), Line(X(0) + np.array([0, -H / 2, 0]), X(0) + np.array([0, H / 2, 0]), color=MUT, stroke_width=1.5))
    for ms in ticks:
        g.add(T(str(ms), sz, MUT).move_to(X(ms / 1000) + np.array([0, -0.25, 0])))
    g.add(T("ms", sz, MUT).move_to(X(t1) + np.array([0.3, -0.25, 0])))
    return g


class A7_Media(Base):
    start_num = 1

    def construct(self):
        TE = F7.TE
        # ---------------------------------------------------------- 1 copertina
        self.new(first=True); self.num = 1
        hc = np.array([5.7, -2.35, 0]); Rh = 0.95
        sigs = [E.periodic_eeg(4.0, seed=s, peaks=((10.0, 1.0, 1.0), (20.0, 2.0, 0.3)), uv=20) for s in (71, 72, 73)]
        Os = [np.array([2.0, -1.75 - 0.6 * k, 0]) for k in range(3)]
        cols = [TEAL, ACC, AMB]

        def vis():
            hd = VGroup(E.head(hc, Rh), E.electrodes(hc, Rh, r=0.04))
            tr0 = VGroup(*[E.window_trace(t, x, 0.0, 1.5, O, 2.6, 0.012, c, 1.8) for (t, x), O, c in zip(sigs, Os, cols)])
            self.play(FadeIn(hd), Create(tr0), run_time=1.2)
            self.tr0 = tr0
        copertina(self, tr("Lecture 7", "Lezione 7"), tr("Event-related potentials:\nfrom averages to components", "Potenziali evento-correlati:\ndalla media alle componenti"), vis)
        scroll_many(self, sigs, Os, 2.6, 0.012, 1.5, cols, 4.0, 1.8, old=self.tr0)

        # ---------------------------------------------------------- 2 obiettivi
        self.new(tr("Lecture 7", "Lezione 7"), tr("Today: the brain's response to an event", "Oggi: la risposta del cervello a un evento"))
        g = rows_mob([tr("*Averaging*: why it works, what it assumes, how many trials.", "*Media*: perché funziona, cosa assume, quanti trial."),
                      tr("++Peaks are not components++: the superposition problem.", "++I picchi non sono componenti++: il problema della sovrapposizione."),
                      tr("The ERP *component zoo*: P1/N1, N170, MMN, P3, N400, ERN, N2pc.", "Lo *zoo delle componenti*: P1/N1, N170, MMN, P3, N400, ERN, N2pc."),
                      tr("*Measuring* amplitudes and latencies without fooling ourselves.", "*Misurare* ampiezze e latenze senza ingannarsi."),
                      tr("*Statistics*: mass-univariate, cluster permutation, single-trial models.", "*Statistica*: mass-univariata, permutazioni a cluster, modelli a singolo trial.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 3 la media che emerge
        self.new(tr("What is an ERP?", "Che cos'è un ERP?"), tr("Averaging lifts a small response out of the EEG", "La media fa emergere una piccola risposta dall'EEG"))
        EP = F7.erp()[None, :] + F7.noise_trials(100, seed=300, uv=14)
        Ot = np.array([-6.2, 1.2, 0]); Wt = 5.6
        Oa = np.array([0.8, 0.1, 0]); Wa = 5.6; ha = 0.08
        nT = ValueTracker(1)

        def avg():
            n = max(int(nT.get_value()), 1)
            return VGroup(wv(TE, EP[n - 1], Ot, Wt, 0.03, MUT, 1.5), wv(TE, np.clip(EP[:n].mean(0), -22, 22), Oa, Wa, ha, ACC, 3.5),
                          T(tr(f"N = **{n}** trials · residual noise ≈ **{dec(14 / 2.5 * 1.0 / np.sqrt(n) * 2.5, 1)} µV**", f"N = **{n}** trial · rumore residuo ≈ **{dec(14 / np.sqrt(n), 1)} µV**"), 20, AMB).move_to(np.array([0, 2.05, 0])))
        ax1 = VGroup(wax(Ot, Wt, 1.8), T(tr("current trial", "trial corrente"), 16, MUT).move_to(Ot + np.array([Wt / 2, 1.2, 0])))
        ax2 = VGroup(wax(Oa, Wa, 3.0), T(tr("running average", "media progressiva"), 16, ACC).move_to(Oa + np.array([1.2, 1.45, 0])))
        az = always_redraw(avg)
        self.play(FadeIn(ax1), FadeIn(ax2), FadeIn(az))
        bl = bullets([tr("ERP ≈ 1–10 µV, ongoing EEG ≈ 20–50 µV.", "ERP ≈ 1–10 µV, EEG di fondo ≈ 20–50 µV."),
                      tr("++Time-locked++ activity stays, the rest cancels.", "L'attività ++agganciata nel tempo++ resta, il resto si annulla.")], 17, n=44, gap=0.22).move_to(np.array([-3.4, -1.4, 0]))
        mt = metaphor(tr("a ++long exposure++ at night: moving cars vanish, the street lamp appears.", "una ++lunga esposizione++ di notte: le auto spariscono, il lampione appare."), 16).move_to(np.array([0, -3.05, 0]))
        self.play(FadeIn(bl), FadeIn(mt))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: nT.set_value(1 + 99 * ph.get_value() ** 2))
        self.add(drv); loop_play(self, ph, 10.0); drv.clear_updaters(); az.clear_updaters()

        # ---------------------------------------------------------- 4 sezione
        self.new(); section_title(self, 1, tr("From trials to ERPs", "Dai trial agli ERP"))

        # ---------------------------------------------------------- 5 jitter di latenza
        self.new(tr("Averaging (1)", "Media (1)"), tr("What averaging assumes — and latency jitter", "Che cosa assume la media — e il jitter di latenza"))
        fm = fcard(r"x_k(t) = s(t) + n_k(t)", CARD2, 0.8).move_to(np.array([-3.6, 1.8, 0]))
        self.play(FadeIn(fm))
        bl = bullets([tr("Same signal s(t) in every trial.", "Stesso segnale s(t) in ogni trial."),
                      tr("Noise with ++zero mean++, independent of the event.", "Rumore a ++media nulla++, indipendente dall'evento."),
                      tr("If latency ++jitters++, the average is ++smaller and wider++.", "Se la latenza ++varia++, la media è ++più piccola e più larga++."),
                      tr("Remedies: response-locking, Woody filter, single-trial methods.", "Rimedi: aggancio alla risposta, filtro di Woody, metodi a singolo trial.")], 17, n=36, gap=0.26).move_to(np.array([-3.6, -0.6, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.4)
        rng = np.random.default_rng(3); z = rng.normal(size=60)
        sdT = ValueTracker(0.0)
        Oj = np.array([0.8, 0, 0]); Wj = 5.6

        def jit():
            sd = sdT.get_value()
            tr_ = np.array([F7.g(TE, 0.35 + sd * zz, 0.05, 8.0) for zz in z])
            g = VGroup(*[wv(TE, tr_[i], Oj + np.array([0, 2.0 - 0.28 * i, 0]), Wj, 0.03, MUT, 1.2) for i in range(8)])
            g.add(wv(TE, tr_.mean(0), Oj + np.array([0, -2.2, 0]), Wj, 0.16, ACC if sd > 0.02 else TEAL, 3.5))
            g.add(T(tr(f"latency jitter σ = **{int(sd * 1000)} ms**", f"jitter di latenza σ = **{int(sd * 1000)} ms**"), 19, AMB).move_to(Oj + np.array([Wj / 2, -0.6, 0])))
            return g
        axj = VGroup(Line(Oj + np.array([0, -2.2, 0]), Oj + np.array([Wj, -2.2, 0]), color=MUT, stroke_width=1.2), T(tr("average", "media"), 15, MUT).move_to(Oj + np.array([-0.55, -1.8, 0])))
        jz = always_redraw(jit)
        self.play(FadeIn(axj), FadeIn(jz))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: sdT.set_value(0.04 * (1 - np.cos(2 * np.pi * ph.get_value()))))
        self.add(drv); loop_play(self, ph, 6.0); drv.clear_updaters(); jz.clear_updaters()

        # ---------------------------------------------------------- 6 SNR e numero di trial
        self.new(tr("Averaging (2)", "Media (2)"), tr("How many trials? Noise falls with √N", "Quanti trial? Il rumore cala con √N"))
        Os_ = np.array([-6.2, -2.3, 0]); Ws = 5.4; Hs = 3.4
        n = np.arange(1, 101)
        cur = VMobject(color=ACC, stroke_width=4).set_points_smoothly([Os_ + np.array([a / 100 * Ws, 12 / np.sqrt(a) / 12 * Hs, 0]) for a in n])
        axs = VGroup(E.axes(Os_, Ws + 0.2, Hs + 0.2, tr("trials N", "trial N"), tr("residual noise (µV)", "rumore residuo (µV)")), *[T(str(v), 13, MUT).move_to(Os_ + np.array([v / 100 * Ws, -0.25, 0])) for v in (1, 25, 50, 100)])
        Oa = np.array([0.9, -0.2, 0]); Wa = 5.4
        nT = ValueTracker(1)

        def snr():
            k = max(int(nT.get_value()), 1)
            y = 12 / np.sqrt(k) / 12 * Hs
            return VGroup(Dot(Os_ + np.array([k / 100 * Ws, y, 0]), radius=0.1, color=AMB), DashedLine(Os_ + np.array([k / 100 * Ws, 0, 0]), Os_ + np.array([k / 100 * Ws, y, 0]), color=AMB, stroke_width=1.5),
                          wv(TE, np.clip(EP[:k].mean(0), -14, 14), Oa, Wa, 0.08, ACC, 3), T(f"N = **{k}** → **{dec(12 / np.sqrt(k), 1)} µV**", 20, AMB).move_to(Oa + np.array([Wa / 2, 2.1, 0])))
        fm = fcard(r"\sigma_{\bar x}=\frac{\sigma}{\sqrt{N}}", CARD2, 0.8).move_to(np.array([-2.0, 1.2, 0]))
        sz = always_redraw(snr)
        self.play(Create(axs), Create(cur), FadeIn(fm), FadeIn(wax(Oa, Wa, 2.6)), FadeIn(sz))
        bl = bullets([tr("To ++halve++ the noise: ++4×++ the trials.", "Per ++dimezzare++ il rumore: ++4×++ i trial."),
                      tr("P3 ≈ 30–40 trials; N2pc, MMN, ERN often ++100+++.", "P3 ≈ 30–40 trial; N2pc, MMN, ERN spesso ++100+++."),
                      tr("Report data quality: *SME* (Luck et al., 2021).", "Riportare la qualità: *SME* (Luck et al., 2021).")], 16, n=48, gap=0.2).move_to(np.array([3.6, -2.7, 0]))
        self.play(FadeIn(bl))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: nT.set_value(1 + 99 * ph.get_value() ** 2))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); sz.clear_updaters()

        # ---------------------------------------------------------- 7 picchi ≠ componenti
        self.new(tr("Averaging (3)", "Media (3)"), tr("Peaks are not components", "I picchi non sono componenti"))
        c1 = F7.g(TE, 0.30, 0.05, 5.0); c2 = F7.g(TE, 0.43, 0.08, 4.0); c3 = F7.g(TE, 0.22, 0.04, -5.0)
        kT = ValueTracker(1.0)
        Oc = np.array([-6.0, 0.4, 0]); Wc = 7.0; hc_ = 0.17
        Ol = np.array([-6.0, -2.3, 0])

        def comp():
            k = kT.get_value(); s = c1 + k * c2 + c3
            pk = TE[np.argmax(s)]
            X = lambda tt: Oc + np.array([(tt + 0.2) * Wc, 0, 0])
            return VGroup(wv(TE, s, Oc, Wc, hc_, FG, 4), wv(TE, c1, Ol, Wc, 0.12, TEAL, 2.5), wv(TE, k * c2, Ol, Wc, 0.12, ACC, 3), wv(TE, c3, Ol, Wc, 0.12, PURP, 2.5),
                          DashedLine(X(pk), X(pk) + np.array([0, hc_ * s.max(), 0]), color=AMB, stroke_width=2),
                          T(tr(f"peak at **{int(round(pk * 1000))} ms**", f"picco a **{int(round(pk * 1000))} ms**"), 19, AMB).move_to(X(pk) + np.array([1.3, hc_ * s.max() + 0.3, 0])),
                          T(f"C2 × {dec(k, 1)}", 17, ACC).move_to(Ol + np.array([Wc + 0.7, 0.3, 0])))
        axc = VGroup(wax(Oc, Wc, 1.2), Line(Ol, Ol + np.array([Wc, 0, 0]), color=MUT, stroke_width=1.2),
                     T(tr("observed ERP = sum", "ERP osservato = somma"), 16, FG).move_to(Oc + np.array([1.4, 1.75, 0])),
                     T(tr("latent components C1, C2, C3", "componenti latenti C1, C2, C3"), 16, MUT).move_to(Ol + np.array([1.8, 1.2, 0])))
        cz = always_redraw(comp)
        self.play(FadeIn(axc), FadeIn(cz))
        bl = bullets([tr("Only C2 changes — the ++peak moves++.", "Cambia solo C2 — il ++picco si sposta++."),
                      tr("Peak latency ≠ timing of a process.", "Latenza del picco ≠ tempo di un processo."),
                      tr("Isolate components with ++difference waves++ and ++topographies++ (Luck, 2014).", "Isolare le componenti con ++onde differenza++ e ++topografie++ (Luck, 2014).")], 16, n=26, gap=0.28).move_to(np.array([4.8, 0.0, 0]))
        self.play(FadeIn(bl))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: kT.set_value(1.5 - 0.5 * np.cos(2 * np.pi * ph.get_value())))
        self.add(drv); loop_play(self, ph, 6.0); drv.clear_updaters(); cz.clear_updaters()

        # ---------------------------------------------------------- 8 sezione
        self.new(); section_title(self, 2, tr("The ERP component zoo", "Lo zoo delle componenti ERP"))

        # ---------------------------------------------------------- 9 zoo: un cursore percorre il tempo
        self.new(tr("Components (1)", "Componenti (1)"), tr("A timeline of classic ERP components", "Una linea del tempo delle componenti classiche"))
        f = F7.f09_zoo(12.0); fit(f, 0.95, np.array([0, -0.2, 0]))
        self.play(Create(f["ax"]), *[FadeIn(f[k]) for k in f if k.startswith("t")], run_time=0.8)
        self.play(Create(f["w"]), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(f[f"k{k}"]) for k in range(7)], lag_ratio=0.2), run_time=2.0)
        x0 = f["ax"][0].get_start()[0]; x1 = f["ax"][0].get_end()[0]; y0 = f["ax"][0].get_start()[1]
        loop_start(self)
        ph = ValueTracker(0.0)
        cur = always_redraw(lambda: Line(np.array([x0 + (x1 - x0) * ph.get_value(), y0 - 2.4, 0]), np.array([x0 + (x1 - x0) * ph.get_value(), y0 + 2.4, 0]), color=AMB, stroke_width=3, stroke_opacity=0.8))
        self.add(cur); loop_play(self, ph, 8.0); cur.clear_updaters()

        # ---------------------------------------------------------- 10 componenti precoci
        self.new(tr("Components (2)", "Componenti (2)"), tr("Early components: senses, attention, prediction", "Componenti precoci: sensi, attenzione, predizione"))
        kinds = [("P1 / N1 (80–200 ms)", tr("sensory responses; ++larger for attended++ locations (Hillyard et al., 1973; Mangun & Hillyard, 1991).", "risposte sensoriali; ++più grandi per le posizioni attese++ (Hillyard et al., 1973; Mangun & Hillyard, 1991).")),
                 ("N170 (≈ 170 ms)", tr("occipito-temporal, ++larger for faces++ (Bentin et al., 1996).", "occipito-temporale, ++più grande per i volti++ (Bentin et al., 1996).")),
                 ("MMN (150–250 ms)", tr("negativity to a ++deviant++ sound, even without attention (Näätänen et al., 2007).", "negatività a un suono ++deviante++, anche senza attenzione (Näätänen et al., 2007)."))]
        cs = VGroup()
        for k, (h_, d_) in enumerate(kinds):
            box = RoundedRectangle(corner_radius=0.14, width=4.0, height=2.5, fill_color=CARD if k % 2 == 0 else CARD2, fill_opacity=1, stroke_width=0)
            tx = VGroup(TX(h_, font=BODY, font_size=20, color=TEAL, weight=BOLD), T(d_, 17, n=36)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            tx.move_to(box).align_to(box, UP).shift(DOWN * 0.25)
            cs.add(VGroup(box, tx))
        cs.arrange(RIGHT, buff=0.25).move_to(np.array([0, 0.7, 0]))
        for c_ in cs: self.play(FadeIn(c_, shift=UP * 0.15), run_time=0.45)
        # MMN: sequenza di toni che scorre
        rng = np.random.default_rng(9); seq = (rng.uniform(size=40) < 0.15)
        y_s = -1.55
        def tones(u):
            g = VGroup()
            for i, dv in enumerate(seq):
                x = -6.0 + 0.45 * i - u * 0.45 * 20
                x = (x + 6.0) % (0.45 * 40) - 6.0
                if -6.2 < x < 6.2:
                    g.add(Rectangle(width=0.28, height=0.28 if not dv else 0.5, stroke_width=0, fill_color=ACC if dv else MUT, fill_opacity=1).move_to(np.array([x, y_s, 0])))
            return g
        t0 = tones(0.0)
        lab = T(tr("auditory sequence: standard ■ · deviant ▮ → MMN", "sequenza uditiva: standard ■ · deviante ▮ → MMN"), 16, MUT).move_to(np.array([0, -2.15, 0]))
        cap = T(tr("Early components show how ++attention++ and ++predictions++ gate sensory processing.", "Le componenti precoci mostrano come ++attenzione++ e ++predizioni++ regolano l'elaborazione sensoriale."), 17, n=110).move_to(np.array([0, -2.85, 0]))
        self.play(FadeIn(t0), FadeIn(lab), FadeIn(cap))
        loop_start(self)
        ph = ValueTracker(0.0)
        tz = always_redraw(lambda: tones(ph.get_value()))
        self.remove(t0); self.add(tz); loop_play(self, ph, 8.0); tz.clear_updaters()

        # ---------------------------------------------------------- 11 P3 oddball
        self.new(tr("Components (3)", "Componenti (3)"), tr("The P3 and the oddball paradigm", "La P3 e il paradigma oddball"))
        std, dev = F7.oddball_erps()
        Op = np.array([-6.0, -0.8, 0]); Wp = 6.4
        self.play(FadeIn(wax(Op, Wp, 3.6)))
        self.play(Create(wv(TE, std, Op, Wp, 0.18, TEAL, 3)), FadeIn(T("standard", 16, TEAL).move_to(Op + np.array([Wp + 0.2, 0.45, 0]))))
        self.play(Create(wv(TE, dev, Op, Wp, 0.18, ACC, 3.5)), FadeIn(T(tr("rare target", "target raro"), 16, ACC).move_to(Op + np.array([0.58 * Wp, 0.18 * dev.max() + 0.3, 0]))),
                  FadeIn(T("P3 (Pz)", 18, ACC).move_to(Op + np.array([0.28 * Wp, 0.18 * dev.max(), 0]))))
        bl = bullets([tr("Rare targets → large ++parietal positivity++ 300–600 ms.", "Target rari → grande ++positività parietale++ 300–600 ms."),
                      tr("Amplitude ∝ ++improbability++ × ++relevance++; latency ∝ ++evaluation time++.", "Ampiezza ∝ ++improbabilità++ × ++rilevanza++; latenza ∝ ++tempo di valutazione++."),
                      tr("*P3a* (novelty) vs *P3b* (targets) (Polich, 2007).", "*P3a* (novità) vs *P3b* (target) (Polich, 2007)."),
                      tr("Basis of the ++P300 speller++ (Farwell & Donchin, 1988).", "Base del ++P300 speller++ (Farwell & Donchin, 1988).")], 16, n=38, gap=0.26).move_to(np.array([3.9, -0.5, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.35)
        seq = (np.random.default_rng(2).uniform(size=36) < 0.2)

        def stream(u):
            g = VGroup()
            for i, dv in enumerate(seq):
                x = (0.45 * i - u * 0.45 * 36) % (0.45 * 36) - 6.2
                if x < 6.2:
                    g.add(Rectangle(width=0.3, height=0.3, stroke_width=0, fill_color=ACC if dv else MUT, fill_opacity=1).move_to(np.array([x, 2.0, 0])))
            return g
        s0 = stream(0.0)
        self.play(FadeIn(s0))
        loop_start(self)
        ph = ValueTracker(0.0)
        sz_ = always_redraw(lambda: stream(ph.get_value()))
        self.remove(s0); self.add(sz_); loop_play(self, ph, 10.0); sz_.clear_updaters()

        # ---------------------------------------------------------- 12 N400
        self.new(tr("Components (4)", "Componenti (4)"), tr("Language: N400 and P600", "Linguaggio: N400 e P600"))
        base = F7.erp(TE, {"P3": 0.35}); inc = base + F7.g(TE, 0.40, 0.08, -6.0)
        On = np.array([-6.0, -1.3, 0]); Wn = 6.2
        s1 = T(tr("I take my coffee with cream and ~sugar~", "Prendo il caffè con latte e ~zucchero~"), 24).move_to(np.array([-2.3, 2.0, 0]))
        s2 = T(tr("I take my coffee with cream and *socks*", "Prendo il caffè con latte e *calzini*"), 24).move_to(np.array([-2.3, 2.0, 0]))
        self.play(FadeIn(s1, shift=RIGHT * 0.2), run_time=1.2)
        self.play(FadeIn(wax(On, Wn, 3.2)), Create(wv(TE, base, On, Wn, 0.2, TEAL, 3)))
        self.next_slide()
        self.play(FadeOut(s1), FadeIn(s2))
        self.play(Create(wv(TE, inc, On, Wn, 0.2, ACC, 3.5)), FadeIn(T("N400", 20, ACC).move_to(On + np.array([0.6 * Wn + 0.6, 0.2 * inc.min(), 0]))))
        bl = bullets([tr("*N400*: centro-parietal negativity ≈ 250–500 ms, ++larger for unexpected words++ (Kutas & Hillyard, 1980).", "*N400*: negatività centro-parietale ≈ 250–500 ms, ++più grande per parole inattese++ (Kutas & Hillyard, 1980)."),
                      tr("Graded by ++cloze probability++: meaning and prediction.", "Graduata dalla ++probabilità cloze++: significato e predizione."),
                      tr("*P600*: syntactic violations and reanalysis (Osterhout & Holcomb, 1992).", "*P600*: violazioni sintattiche e rianalisi (Osterhout & Holcomb, 1992).")], 16, n=38, gap=0.26).move_to(np.array([3.9, -0.8, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.4)

        # ---------------------------------------------------------- 13 azione ed errore
        self.new(tr("Components (5)", "Componenti (5)"), tr("Preparing and monitoring actions", "Preparare e monitorare le azioni"))
        kinds = [("CNV", tr("slow negativity between warning and imperative stimulus: ++anticipation++ (Walter et al., 1964).", "negatività lenta tra avviso e stimolo imperativo: ++anticipazione++ (Walter et al., 1964).")),
                 (tr("Readiness potential / LRP", "Potenziale di prontezza / LRP"), tr("builds up before movements; the ++lateralized++ part (C3/C4) shows ++which hand++.", "cresce prima dei movimenti; la parte ++lateralizzata++ (C3/C4) mostra ++quale mano++.")),
                 ("ERN / Pe", tr("fronto-central negativity ++50–100 ms after an error++, then Pe (awareness) (Gehring et al., 1993).", "negatività fronto-centrale ++50–100 ms dopo un errore++, poi Pe (consapevolezza) (Gehring et al., 1993)."))]
        cs = VGroup()
        for k, (h_, d_) in enumerate(kinds):
            box = RoundedRectangle(corner_radius=0.14, width=4.0, height=2.6, fill_color=CARD if k % 2 == 0 else CARD2, fill_opacity=1, stroke_width=0)
            tx = VGroup(TX(h_, font=BODY, font_size=20, color=TEAL, weight=BOLD), T(d_, 17, n=36)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            tx.move_to(box).align_to(box, UP).shift(DOWN * 0.25)
            cs.add(VGroup(box, tx))
        cs.arrange(RIGHT, buff=0.25).move_to(np.array([0, 0.6, 0]))
        for c_ in cs: self.play(FadeIn(c_, shift=UP * 0.15), run_time=0.45)
        # ERN agganciata alla risposta
        tr_ = np.arange(-0.2, 0.6, 1 / 250)
        corr = F7.g(tr_, 0.06, 0.03, -1.0) + F7.g(tr_, 0.25, 0.08, 2.0)
        err = F7.g(tr_, 0.07, 0.03, -7.0) + F7.g(tr_, 0.28, 0.1, 5.0)
        Oe = np.array([-3.0, -2.2, 0]); We = 6.0
        self.play(FadeIn(wax(Oe, We, 1.6, -0.2, 0.6, (0, 200, 400))), Create(wv(tr_, corr, Oe, We, 0.09, TEAL, 3, -0.2, 0.6)), Create(wv(tr_, err, Oe, We, 0.09, ACC, 3.5, -0.2, 0.6)),
                  FadeIn(T(tr("response-locked: correct / ++error++ (ERN)", "agganciata alla risposta: corretta / ++errore++ (ERN)"), 16).move_to(Oe + np.array([We / 2, 0.85, 0]))))

        # ---------------------------------------------------------- 14 N2pc: il target cambia lato
        self.new(tr("Components (6)", "Componenti (6)"), tr("N2pc: tracking spatial attention with a subtraction", "N2pc: l'attenzione spaziale per sottrazione"))
        hc = np.array([-4.4, -0.6, 0]); Rh = 1.7
        sideT = ValueTracker(0.0)
        ipsi = F7.erp(TE, {"P3": 0.4}); contra = ipsi + F7.g(TE, 0.25, 0.045, -2.5)
        Ow = np.array([-1.6, 0.9, 0]); Ww = 5.2
        Od = np.array([-1.6, -1.9, 0])

        def n2():
            left = sideT.get_value() < 0.5
            d = np.array([-4.4, 2.0, 0])
            g = VGroup(T("+", 22).move_to(d), Circle(radius=0.16, color=ACC, fill_color=ACC, fill_opacity=1).move_to(d + np.array([-0.8 if left else 0.8, 0, 0])),
                       Circle(radius=0.16, color=MUT, fill_color=MUT, fill_opacity=1).move_to(d + np.array([0.8 if left else -0.8, 0, 0])))
            for n_ in ("P7", "P8"):
                contra_ = (n_ == "P8") == left
                g.add(Circle(radius=0.26, color=ACC if contra_ else TEAL, stroke_width=4, fill_color=config.background_color, fill_opacity=1).move_to(hc + E.el2d(n_, Rh)), T(n_, 13).move_to(hc + E.el2d(n_, Rh)))
            g.add(T(tr("target LEFT → contralateral = P8", "target SINISTRA → controlaterale = P8") if left else tr("target RIGHT → contralateral = P7", "target DESTRA → controlaterale = P7"), 16, AMB).move_to(d + np.array([0, -0.5, 0])))
            return g
        self.play(Create(E.head(hc, Rh)), FadeIn(wax(Ow, Ww, 2.4)), FadeIn(wax(Od, Ww, 1.6)))
        nz = always_redraw(n2)
        self.play(FadeIn(nz), Create(wv(TE, ipsi, Ow, Ww, 0.13, TEAL, 2.5)), Create(wv(TE, contra, Ow, Ww, 0.13, ACC, 3)),
                  FadeIn(T(tr("ipsi", "ipsi"), 15, TEAL).move_to(Ow + np.array([Ww + 0.4, 0.4, 0]))), FadeIn(T(tr("contra", "contro"), 15, ACC).move_to(Ow + np.array([Ww + 0.45, 0.0, 0]))))
        self.play(Create(wv(TE, contra - ipsi, Od, Ww, 0.2, ACC, 3.5)), FadeIn(T(tr("contra − ipsi = N2pc", "contro − ipsi = N2pc"), 16, ACC).move_to(Od + np.array([Ww / 2, 0.9, 0]))))
        bl = bullets([tr("Negativity ++contralateral++ to the attended item, 200–300 ms (Luck & Hillyard, 1994).", "Negatività ++controlaterale++ all'oggetto atteso, 200–300 ms (Luck & Hillyard, 1994)."),
                      tr("The subtraction removes all ++non-lateralised++ activity.", "La sottrazione toglie tutta l'attività ++non lateralizzata++.")], 15, n=30, gap=0.25).move_to(np.array([5.2, -0.5, 0]))
        self.play(FadeIn(bl))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: sideT.set_value(ph.get_value()))
        self.add(drv); loop_play(self, ph, 6.0); drv.clear_updaters(); nz.clear_updaters()
        self.end()
