from base import *
import figs7 as F7
from s7a import wv, wax, dec


class B7_Misure(Base):
    start_num = 15

    def construct(self):
        TE = F7.TE
        # ---------------------------------------------------------- 15 sezione
        self.new(first=True); section_title(self, 3, tr("Measuring ERPs", "Misurare gli ERP"))

        # ---------------------------------------------------------- 16 misure: finestra che scorre
        self.new(tr("Measurement (1)", "Misura (1)"), tr("Amplitude and latency measures", "Misure di ampiezza e latenza"))
        t = np.arange(-0.2, 0.8, 1 / 1000)
        x = F7.erp(t)
        Om = np.array([-6.2, -1.4, 0]); Wm = 7.2; hm = 0.24
        X = lambda tt, y=0: Om + np.array([(tt + 0.2) * Wm, hm * y, 0])
        wave = VMobject(color=FG, stroke_width=3.5).set_points_as_corners([X(a, b) for a, b in zip(t, x)])
        self.play(FadeIn(wax(Om, Wm, 3.6)), Create(wave))
        cT = ValueTracker(0.40)

        def meas():
            c = cT.get_value(); a0, a1 = c - 0.1, c + 0.1
            m = (t >= a0) & (t <= a1)
            mu = x[m].mean()
            g = VGroup(Polygon(*([X(a, b) for a, b in zip(t[m], x[m])] + [X(a1), X(a0)]), stroke_width=0, fill_color=TEAL, fill_opacity=0.35),
                       Line(X(a0, mu), X(a1, mu), color=TEAL, stroke_width=4),
                       T(tr(f"mean {int(a0 * 1000)}–{int(a1 * 1000)} ms = **{dec(mu, 1)} µV**", f"media {int(a0 * 1000)}–{int(a1 * 1000)} ms = **{dec(mu, 1)} µV**"), 19, TEAL).move_to(np.array([-2.6, 2.05, 0])))
            return g
        mz = always_redraw(meas)
        mw = (t >= 0.3) & (t <= 0.5)
        ip = np.argmax(x * mw)
        cs = np.cumsum(np.clip(x * mw, 0, None)); i50 = np.searchsorted(cs, cs[-1] / 2)
        pk = VGroup(Dot(X(t[ip], x[ip]), radius=0.09, color=ACC), T(tr("peak", "picco"), 16, ACC).move_to(X(t[ip], x[ip]) + np.array([0.6, 0.25, 0])))
        fa = VGroup(DashedLine(X(t[i50]), X(t[i50], x[i50]), color=PURP, stroke_width=2.5), T(tr("50 % area latency", "latenza al 50 % dell'area"), 15, PURP).move_to(X(t[i50]) + np.array([1.2, -0.55, 0])))
        self.play(FadeIn(mz), FadeIn(pk), FadeIn(fa))
        bl = bullets([tr("*Mean amplitude*: robust, ++unbiased++ by trial number — preferred.", "*Ampiezza media*: robusta, ++non distorta++ dal numero di trial — preferita."),
                      tr("*Peak*: noisy, ++biased++ upward with few trials.", "*Picco*: rumoroso, ++distorto++ verso l'alto con pochi trial."),
                      tr("*Latency*: fractional area/peak + ++jackknifing++ (Kiesel et al., 2008).", "*Latenza*: frazione d'area/picco + ++jackknife++ (Kiesel et al., 2008)."),
                      tr("~Choose the window a priori!~", "~Scegliere la finestra a priori!~")], 16, n=30, gap=0.26).move_to(np.array([4.6, -0.4, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.35)
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: cT.set_value(0.40 + 0.22 * np.sin(2 * np.pi * ph.get_value())))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); mz.clear_updaters()

        # ---------------------------------------------------------- 17 onde differenza e topografie
        self.new(tr("Measurement (2)", "Misura (2)"), tr("Difference waves, topographies — and circularity", "Onde differenza, topografie — e circolarità"))
        std, dev = F7.oddball_erps()
        O1 = np.array([-6.2, 0.9, 0]); O2 = np.array([-6.2, -1.7, 0]); Wd = 5.4
        self.play(FadeIn(wax(O1, Wd, 2.6)), Create(wv(TE, std, O1, Wd, 0.13, TEAL, 2.5)), Create(wv(TE, dev, O1, Wd, 0.13, ACC, 2.5)),
                  FadeIn(T(tr("rare / standard", "raro / standard"), 16).move_to(O1 + np.array([Wd / 2, 1.6, 0]))))
        self.play(FadeIn(wax(O2, Wd, 1.8)), Create(wv(TE, dev - std, O2, Wd, 0.13, FG, 3.5)), FadeIn(T(tr("difference wave", "onda differenza"), 16).move_to(O2 + np.array([Wd / 2, 1.3, 0]))))
        maps = Group()
        for k, (lab, pos, mom) in enumerate((("170 ms", [0, 0.1, 0.7], [0, 0.8, -0.6]), ("380 ms", [0, -0.45, 0.55], [0, -0.3, 1.0]))):
            c = np.array([0.8 + 2.6 * k, 0.7, 0])
            V, m = E.dipole_map(pos, mom, n=121, blur=0.2)
            img, out = E.topomap(V, m, c, 1.1)
            maps.add(Group(img, out, T(lab, 16).move_to(c + np.array([0, -1.4, 0]))))
        self.play(FadeIn(maps))
        bl = bullets([tr("⚠ Picking window/electrodes ++after seeing the effect++ = double dipping.", "⚠ Scegliere finestra/elettrodi ++dopo aver visto l'effetto++ = double dipping."),
                      tr("Use ++a priori++ windows, a ++collapsed localiser++ or mass-univariate tests (Luck & Gaspelin, 2017).", "Usare finestre ++a priori++, un ++localizzatore collassato++ o test mass-univariati (Luck & Gaspelin, 2017).")], 16, n=48, gap=0.26).move_to(np.array([2.1, -2.2, 0]))
        self.play(FadeIn(bl))

        # ---------------------------------------------------------- 18 sezione
        self.new(); section_title(self, 4, tr("Statistics for ERPs", "Statistica per gli ERP"))

        # ---------------------------------------------------------- 19 permutazioni a cluster: la distribuzione nulla si costruisce
        self.new(tr("Statistics (1)", "Statistica (1)"), tr("Cluster-based permutation tests", "Test di permutazione a cluster"))
        rng = np.random.default_rng(11)
        tt = np.arange(-0.2, 0.8, 1 / 100); nS = 20
        eff = F7.g(tt, 0.38, 0.07, 1.2) + F7.g(tt, 0.17, 0.02, 0.6)
        from scipy.ndimage import gaussian_filter1d
        D = np.array([eff + gaussian_filter1d(rng.normal(size=len(tt)), 2) * 1.8 for _ in range(nS)])   # differenze per soggetto
        tstat = lambda M: M.mean(0) / (M.std(0, ddof=1) / np.sqrt(len(M)))
        thr = 2.09

        def clmass(tv):
            ms, i = [], 0
            while i < len(tv):
                if tv[i] > thr:
                    j = i
                    while j < len(tv) and tv[j] > thr: j += 1
                    ms.append((i, j, tv[i:j].sum())); i = j
                else:
                    i += 1
            return ms
        tobs = tstat(D); cobs = clmass(tobs); mobs = max(m for _, _, m in cobs)
        NP = 300
        flips = rng.choice([-1, 1], size=(NP, nS))
        tperm = [tstat(D * f_[:, None]) for f_ in flips]
        mperm = np.array([max([m for _, _, m in clmass(tp)] + [0]) for tp in tperm])
        Ot = np.array([-6.2, -0.6, 0]); Wt = 6.4; ht = 0.2
        X = lambda a, y: Ot + np.array([(a + 0.2) * Wt, ht * y, 0])
        obs = VMobject(color=FG, stroke_width=3.5).set_points_as_corners([X(a, b) for a, b in zip(tt, tobs)])
        shade = VGroup(*[Polygon(*([X(a, b) for a, b in zip(tt[i:j], tobs[i:j])] + [X(tt[j - 1], thr), X(tt[i], thr)]), stroke_width=0, fill_color=ACC, fill_opacity=0.5) for i, j, m in cobs])
        th = DashedLine(X(-0.2, thr), X(0.8, thr), color=MUT, stroke_width=1.5)
        self.play(FadeIn(wax(Ot, Wt, 3.6)), Create(obs), Create(th), FadeIn(T("t = 2.09", 14, MUT).move_to(X(0.8, thr) + np.array([0.45, 0.2, 0]))))
        self.play(FadeIn(shade), FadeIn(T(tr(f"observed cluster mass Σt = **{dec(mobs, 1)}**", f"massa del cluster osservato Σt = **{dec(mobs, 1)}**"), 18, ACC).move_to(np.array([-3.0, 2.05, 0]))))
        Ob = np.array([1.2, -1.8, 0]); Wb = 5.0; Hb = 2.6
        xmax = max(mobs, mperm.max()) * 1.05
        bins = np.linspace(0, xmax, 26)
        hmax = np.histogram(mperm, bins)[0].max()
        kT = ValueTracker(1)

        def perm():
            k = max(int(kT.get_value()), 1)
            h, _ = np.histogram(mperm[:k], bins)
            wb = Wb / 25
            g = VGroup(*[Rectangle(width=wb * 0.9, height=max(v / hmax * Hb, 0.003), stroke_width=0, fill_color=MUT, fill_opacity=0.9).move_to(Ob + np.array([wb * (i + 0.5), 0, 0]), aligned_edge=DOWN) for i, v in enumerate(h)])
            g.add(VMobject(color=TEAL, stroke_width=2, stroke_opacity=0.8).set_points_as_corners([X(a, b) for a, b in zip(tt, tperm[k - 1])]))
            p = (np.sum(mperm[:k] >= mobs) + 1) / (k + 1)
            g.add(T(tr(f"permutation **{k}** · p = **{dec(p, 3)}**", f"permutazione **{k}** · p = **{dec(p, 3)}**"), 18, TEAL).move_to(Ob + np.array([Wb / 2, Hb + 0.45, 0])))
            return g
        axb = VGroup(Line(Ob, Ob + np.array([Wb + 0.1, 0, 0]), color=FG, stroke_width=1.5), T(tr("max cluster mass (null)", "massa max dei cluster (nulla)"), 14, MUT).move_to(Ob + np.array([Wb / 2, -0.3, 0])),
                     Arrow(Ob + np.array([mobs / xmax * Wb, 1.3, 0]), Ob + np.array([mobs / xmax * Wb, 0.05, 0]), buff=0, color=ACC, stroke_width=5, tip_length=0.16))
        pz = always_redraw(perm)
        self.play(FadeIn(axb), FadeIn(pz))
        cap = T(tr("Sign-flip the subjects' differences, recompute the largest cluster, repeat: the observed cluster is compared with this ++max-cluster++ distribution (Maris & Oostenveld, 2007).", "Invertire a caso il segno delle differenze dei soggetti, ricalcolare il cluster massimo, ripetere: il cluster osservato si confronta con questa distribuzione del ++massimo++ (Maris & Oostenveld, 2007)."), 16, n=120).move_to(np.array([0, -3.05, 0]))
        self.play(FadeIn(cap))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: kT.set_value(1 + (NP - 1) * ph.get_value()))
        self.add(drv); loop_play(self, ph, 12.0); drv.clear_updaters(); pz.clear_updaters()

        # ---------------------------------------------------------- 20 sovrapposizione e deconvoluzione
        self.new(tr("Statistics (2)", "Statistica (2)"), tr("Beyond averages: single trials and regression", "Oltre le medie: singolo trial e regressione"))
        t2 = np.arange(-0.2, 1.4, 1 / 250)
        rs = lambda tt_: F7.erp(tt_, {"P3": 0.6})
        rr = lambda tt_: F7.g(tt_, 0.05, 0.04, -4.0) + F7.g(tt_, 0.25, 0.1, 5.0)
        soaT = ValueTracker(0.8)
        Oo = np.array([-6.2, -0.4, 0]); Wo = 7.2; ho = 0.14
        Xo = lambda a, y=0: Oo + np.array([(a + 0.2) / 1.6 * Wo, ho * y, 0])

        def ovl():
            soa = soaT.get_value()
            a = rs(t2); b = rr(t2 - soa)
            g = VGroup(VMobject(color=TEAL, stroke_width=2.5).set_points_as_corners([Xo(u, v) for u, v in zip(t2, a)]),
                       VMobject(color=PURP, stroke_width=2.5).set_points_as_corners([Xo(u, v) for u, v in zip(t2, b)]),
                       VMobject(color=FG, stroke_width=4).set_points_as_corners([Xo(u, v - 9) for u, v in zip(t2, a + b)]),
                       DashedLine(Xo(soa, -14), Xo(soa, 10), color=PURP, stroke_width=1.5),
                       T(tr(f"response at **{int(soa * 1000)} ms**", f"risposta a **{int(soa * 1000)} ms**"), 18, PURP).move_to(Xo(soa, 11.5)))
            return g
        axo = VGroup(Line(Xo(-0.2), Xo(1.4), color=MUT, stroke_width=1.2), Line(Xo(-0.2, -9), Xo(1.4, -9), color=MUT, stroke_width=1.2), DashedLine(Xo(0, -14), Xo(0, 10), color=TEAL, stroke_width=1.5),
                     T(tr("stimulus", "stimolo"), 16, TEAL).move_to(Xo(0, 11.5)), T(tr("recorded = sum", "registrato = somma"), 16, FG).move_to(Xo(1.15, -6.5)))
        oz = always_redraw(ovl)
        self.play(FadeIn(axo), FadeIn(oz))
        bl = bullets([tr("Fast events ++overlap++: the average of one is contaminated by the other.", "Eventi rapidi si ++sovrappongono++: la media dell'uno è contaminata dall'altro."),
                      tr("*Deconvolution* / rERP: estimate each response by ++regression++ (Smith & Kutas, 2015; Ehinger & Dimigen, 2019).", "*Deconvoluzione* / rERP: stimare ogni risposta per ++regressione++ (Smith & Kutas, 2015; Ehinger & Dimigen, 2019)."),
                      tr("*Hierarchical GLM* (LIMO) and *mixed models*: use ++all trials++ and continuous predictors.", "*GLM gerarchico* (LIMO) e *modelli misti*: usano ++tutti i trial++ e predittori continui.")], 16, n=34, gap=0.28).move_to(np.array([4.4, -0.4, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.4)
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: soaT.set_value(0.55 + 0.35 * np.cos(2 * np.pi * ph.get_value())))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); oz.clear_updaters()

        # ---------------------------------------------------------- 21 sezione
        self.new(); section_title(self, 5, tr("ERPs in practice", "ERP in pratica"))

        # ---------------------------------------------------------- 22 MATLAB
        self.new(tr("In MATLAB", "In MATLAB"), tr("ERPs, difference waves and a permutation test", "ERP, onde differenza e un test di permutazione"))
        code = ["A = pop_loadset('sub-01_std.set');  B = pop_loadset('sub-01_dev.set');",
                "ch = find(strcmpi({A.chanlocs.labels}, 'Pz'));  t = A.times;          % ms",
                "erpA = mean(A.data(ch,:,:), 3);  erpB = mean(B.data(ch,:,:), 3);    % averages",
                "dw   = erpB - erpA;                                                  % difference wave",
                "win  = t >= 300 & t <= 500;                                          % a priori window",
                "mA = squeeze(mean(A.data(ch,win,:), 2));  mB = squeeze(mean(B.data(ch,win,:), 2));",
                "obs = mean(mB) - mean(mA);                                           % mean-amplitude effect",
                "all = [mA; mB];  nA = numel(mA);  nPerm = 5000;  null = zeros(nPerm,1);",
                "for p = 1:nPerm",
                "    idx = randperm(numel(all));",
                "    null(p) = mean(all(idx(nA+1:end))) - mean(all(idx(1:nA)));",
                "end",
                "pval = (sum(abs(null) >= abs(obs)) + 1) / (nPerm + 1);",
                "plot(t, erpA, t, erpB, t, dw, 'k', 'LineWidth', 2);",
                "xlabel('time (ms)'); ylabel('\\muV'); legend('standard','deviant','difference');"]
        cl = code_lines(code, 15)
        if cl.width > 12.6: cl.scale_to_fit_width(12.6)
        cc_ = card(cl, CARD, pad=0.25).move_to(np.array([0, -0.45, 0]))
        self.play(FadeIn(cc_[0]))
        self.play(LaggedStart(*[FadeIn(x_, shift=RIGHT * 0.1) for x_ in cl], lag_ratio=0.12), run_time=3.0)

        # ---------------------------------------------------------- 23 buona pratica
        self.new(tr("Good practice", "Buona pratica"), tr("Reporting ERP studies", "Documentare uno studio ERP"))
        g = rows_mob([tr("Trials per condition ++after rejection++; data quality (SME).", "Trial per condizione ++dopo il rigetto++; qualità dei dati (SME)."),
                      tr("Reference, filters (type, cut-off, order), baseline window.", "Riferimento, filtri (tipo, taglio, ordine), finestra di baseline."),
                      tr("Measurement windows and electrodes ++justified a priori++.", "Finestre di misura ed elettrodi ++motivati a priori++."),
                      tr("Show ++waveforms and topographies++, not only bar plots.", "Mostrare ++forme d'onda e topografie++, non solo istogrammi."),
                      tr("Share data (BIDS) and code; pre-register when possible (Keil et al., 2014).", "Condividere dati (BIDS) e codice; pre-registrare quando possibile (Keil et al., 2014).")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 24 domande
        self.new(tr("Check your understanding", "Verifica"), tr("Three questions", "Tre domande"))
        g = rows_mob([tr("With 40 trials the residual noise is 2 µV. How many trials to reach 1 µV?", "Con 40 trial il rumore residuo è 2 µV. Quanti trial servono per 1 µV?"),
                      tr("Patients show a smaller, wider P3. Give an explanation that is not \"less P3\".", "I pazienti mostrano una P3 più piccola e larga. Dai una spiegazione diversa da \"meno P3\"."),
                      tr("You pick the 50-ms window where conditions differ most, then test it. What is wrong?", "Scegli la finestra di 50 ms dove le condizioni differiscono di più, poi la testi. Che cosa non va?")], 21, n=84, h=1.05, gap=0.35, col=ACC).shift(DOWN * 0.3)
        for r_ in g: self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.7)

        # ---------------------------------------------------------- 25 messaggi chiave
        self.new(tr("Take-home messages", "Messaggi chiave"), tr("Take-home messages", "Messaggi chiave"))
        g = rows_mob([tr("Averaging: noise ∝ ++1/√N++; assumes a constant, time-locked signal.", "Media: rumore ∝ ++1/√N++; presuppone un segnale costante e agganciato."),
                      tr("++Peaks ≠ components++: use difference waves and topographies.", "++Picchi ≠ componenti++: usare onde differenza e topografie."),
                      tr("Components index ++specific processes++ (P1/N1, N170, MMN, P3, N400, ERN, N2pc).", "Le componenti indicano ++processi specifici++ (P1/N1, N170, MMN, P3, N400, ERN, N2pc)."),
                      tr("Prefer ++mean amplitude++; windows ++a priori++.", "Preferire l'++ampiezza media++; finestre ++a priori++."),
                      tr("++Cluster permutation++ or single-trial models for inference.", "++Permutazioni a cluster++ o modelli a singolo trial per l'inferenza.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 26 letture
        self.new(tr("Suggested reading", "Letture consigliate"), tr("Suggested reading", "Letture consigliate"))
        refs_slide(self, ["Luck (2014) *An Introduction to the Event-Related Potential Technique*, MIT Press.", "Kappenman & Luck (2012) *Oxford Handbook of ERP Components*, OUP.",
                          "Sutton et al. (1965) *Science* 150:1187–1188.", "Polich (2007) *Clin Neurophysiol* 118:2128–2148.",
                          "Kutas & Federmeier (2011) *Annu Rev Psychol* 62:621–647.", "Näätänen et al. (2007) *Clin Neurophysiol* 118:2544–2590.",
                          "Luck & Hillyard (1994) *Psychophysiology* 31:291–308.", "Gehring et al. (1993) *Psychol Sci* 4:385–390.",
                          "Luck & Gaspelin (2017) *Psychophysiology* 54:146–157.", "Groppe, Urbach & Kutas (2011) *Psychophysiology* 48:1711–1725.",
                          "Maris & Oostenveld (2007) *J Neurosci Methods* 164:177–190.", "Luck et al. (2021) *Psychophysiology* 58:e13793."], 17)
        self.end()
