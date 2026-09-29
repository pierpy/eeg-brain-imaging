from base import *
import figs10 as F10
from s10a import dec, cards_row, TD
from scipy.stats import norm
from scipy.ndimage import gaussian_filter1d


class B10_Applicazioni(Base):
    start_num = 8

    def construct(self):
        # ---------------------------------------------------------- 8 sezione
        self.new(first=True); section_title(self, 2, tr("Evaluating and interpreting", "Valutare e interpretare"))

        # ---------------------------------------------------------- 9 metriche: d' che cresce, ROC e distribuzioni
        self.new(tr("Evaluation (1)", "Valutazione (1)"), tr("Performance metrics and chance level", "Metriche di prestazione e livello del caso"))
        dT = ValueTracker(0.5)
        Od = np.array([-6.2, -0.4, 0]); Wd = 5.4; Hd = 2.0
        Or = np.array([0.6, -1.8, 0]); Wr = 2.8
        xs = np.linspace(-4, 6, 200)

        def met():
            dp = dT.get_value(); thr = dp / 2
            g = VGroup()
            for mu, col in ((0, TEAL), (dp, ACC)):
                g.add(VMobject(color=col, stroke_width=3).set_points_smoothly([Od + np.array([(x + 4) / 10 * Wd, norm.pdf(x - mu) / 0.4 * Hd, 0]) for x in xs]))
            g.add(DashedLine(Od + np.array([(thr + 4) / 10 * Wd, 0, 0]), Od + np.array([(thr + 4) / 10 * Wd, Hd + 0.1, 0]), color=FG, stroke_width=2))
            th = np.linspace(-5, 7, 120); fa = 1 - norm.cdf(th); hr = 1 - norm.cdf(th - dp)
            g.add(VMobject(color=ACC, stroke_width=3.5).set_points_smoothly([Or + np.array([a * Wr, b * Wr, 0]) for a, b in zip(fa[::-1], hr[::-1])]))
            g.add(Dot(Or + np.array([(1 - norm.cdf(thr)) * Wr, (1 - norm.cdf(thr - dp)) * Wr, 0]), radius=0.08, color=AMB))
            auc = norm.cdf(dp / np.sqrt(2)); acc = (norm.cdf(thr) + 1 - norm.cdf(thr - dp)) / 2
            g.add(T(f"d′ = **{dec(dp, 1)}** · AUC = **{dec(auc)}** · " + tr(f"accuracy = **{int(100 * acc)} %**", f"accuratezza = **{int(100 * acc)} %**"), 20, AMB).move_to(np.array([-1.0, 2.0, 0])))
            return g
        axm = VGroup(Line(Od, Od + np.array([Wd, 0, 0]), color=MUT, stroke_width=1.5), T(tr("classifier output", "uscita del classificatore"), 14, MUT).move_to(Od + np.array([Wd / 2, -0.3, 0])),
                     E.axes(Or, Wr + 0.2, Wr + 0.2, tr("false alarms", "falsi allarmi"), tr("hits", "hit")), Line(Or, Or + np.array([Wr, Wr, 0]), color=MUT, stroke_width=1.2))
        mz = always_redraw(met)
        self.play(FadeIn(axm), FadeIn(mz))
        bl = bullets([tr("*Balanced accuracy* for unbalanced classes.", "*Accuratezza bilanciata* per classi sbilanciate."),
                      tr("*d′*, *AUC*: threshold-free.", "*d′*, *AUC*: indipendenti dalla soglia."),
                      tr("⚠ Chance ≠ 50 % with few trials → ++permutation++ (Combrisson & Jerbi, 2015).", "⚠ Caso ≠ 50 % con pochi trial → ++permutazioni++ (Combrisson & Jerbi, 2015).")], 15, n=30, gap=0.28).move_to(np.array([5.0, -0.5, 0]))
        self.play(FadeIn(bl))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: dT.set_value(1.25 - 1.0 * np.cos(2 * np.pi * ph.get_value())))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); mz.clear_updaters()

        # ---------------------------------------------------------- 10 Haufe
        self.new(tr("Evaluation (2)", "Valutazione (2)"), tr("Weights are not patterns", "I pesi non sono pattern"))
        f = F10.f10_haufe(1.25); fit(f, 1.0, np.array([0, 0.7, 0]))
        for k in range(3):
            self.play(FadeIn(f[f"m{k}"]), FadeIn(f[f"o{k}"]), FadeIn(f[f"l{k}"]), run_time=0.8)
        fm = fcard(r"\mathbf{A}=\boldsymbol{\Sigma}_x\,\mathbf{W}\,\boldsymbol{\Sigma}_{\hat s}^{-1}", CARD2, 0.8).move_to(np.array([0, -1.5, 0]))
        cap = T(tr("Weights also ++cancel noise++: interpret the ++activation pattern++, not w (Haufe et al., 2014).", "I pesi ++cancellano anche il rumore++: interpretare il ++pattern di attivazione++, non w (Haufe et al., 2014)."), 17, n=110).move_to(np.array([0, -2.7, 0]))
        self.play(FadeIn(fm), FadeIn(cap))

        # ---------------------------------------------------------- 11 decoding nel tempo: la curva si costruisce
        self.new(tr("Time-resolved decoding (1)", "Decoding nel tempo (1)"), tr("When does the brain know?", "Quando il cervello \"sa\"?"))
        X, y = F10.sim_trials(400, seed=1)
        acc = gaussian_filter1d(F10.time_decoding(X, y), 1.2)
        W_ = 7.0; H_ = 3.2; O_ = np.array([-6.2, -1.9, 0])
        Xp = lambda t: (t + 0.2) / 1.0 * W_; Yp = lambda v: (v - 0.4) / 0.6 * H_
        ax = VGroup(E.axes(O_, W_ + 0.2, H_ + 0.2, tr("time (ms)", "tempo (ms)"), tr("accuracy", "accuratezza")),
                    DashedLine(O_ + np.array([0, Yp(0.5), 0]), O_ + np.array([W_, Yp(0.5), 0]), color=MUT, stroke_width=1.5),
                    DashedLine(O_ + np.array([Xp(0), 0, 0]), O_ + np.array([Xp(0), H_, 0]), color=MUT, stroke_width=1.5),
                    *[T(str(ms), 13, MUT).move_to(O_ + np.array([Xp(ms / 1000), -0.25, 0])) for ms in (0, 200, 400, 600)])
        self.play(FadeIn(ax))
        a1, a2 = F10.patterns()
        tT = ValueTracker(0.0)
        cm = np.array([4.4, 1.3, 0]); R = 1.05

        def td():
            u = tT.get_value(); i = int(u * (len(TD) - 1))
            g = VGroup(VMobject(color=ACC, stroke_width=3.5).set_points_as_corners([O_ + np.array([Xp(t), Yp(a), 0]) for t, a in zip(TD[:i + 1], acc[:i + 1])] + ([O_ + np.array([Xp(TD[0]) + 1e-3, Yp(acc[0]), 0])] if i == 0 else [])))
            g.add(Dot(O_ + np.array([Xp(TD[i]), Yp(acc[i]), 0]), radius=0.08, color=AMB))
            g.add(T(f"t = **{int(TD[i] * 1000)} ms** · " + tr(f"acc. **{int(100 * acc[i])} %**", f"acc. **{int(100 * acc[i])} %**"), 19, AMB).move_to(O_ + np.array([W_ / 2, H_ + 0.4, 0])))
            return g
        tz = always_redraw(td)
        def pat():
            i = int(tT.get_value() * (len(TD) - 1)); t = TD[i]
            v = a1 * np.exp(-0.5 * ((t - 0.2) / 0.04) ** 2) + a2 * np.exp(-0.5 * ((t - 0.47) / 0.1) ** 2)
            V, m = E.interp_map(v + 1e-6, n=81, p=2.5)
            img, out = E.topomap(V, m, cm, R, vmax=1.0)
            return Group(img, out)
        pz = redraw(pat)
        self.play(FadeIn(tz), FadeIn(pz), FadeIn(T(tr("class difference", "differenza tra classi"), 15, MUT).move_to(cm + np.array([0, -1.35, 0]))))
        bl = bullets([tr("Classify ++at every time point++.", "Classificare ++a ogni istante++."),
                      tr("Shows ++when++ information is present.", "Mostra ++quando++ l'informazione c'è."),
                      tr("Group test: cluster permutation.", "Test di gruppo: permutazioni a cluster."),
                      tr("⚠ Filters can shift onsets (Van Driel et al., 2021).", "⚠ I filtri possono spostare l'onset (Van Driel et al., 2021).")], 15, n=30, gap=0.24).move_to(np.array([4.5, -1.6, 0]))
        self.play(FadeIn(bl))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: tT.set_value(ph.get_value()))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); tz.clear_updaters(); pz.clear_updaters()

        # ---------------------------------------------------------- 12 generalizzazione temporale: la matrice si riempie
        self.new(tr("Time-resolved decoding (2)", "Decoding nel tempo (2)"), tr("Temporal generalisation", "Generalizzazione temporale"))
        X, y = F10.sim_trials(200, seed=2, snr=0.8)
        G = F10.gen_matrix(X, y)
        Wm = 4.4; cm = np.array([-3.4, -0.3, 0])
        rT = ValueTracker(1.0)
        v = np.clip((G - 0.5) / 0.4, -1, 1)
        from manim import RESAMPLING_ALGORITHMS

        def tgm():
            n = max(int(rT.get_value() * len(TD)), 1)
            vv = np.full_like(v, 0.0); vv[:n] = v[:n]
            img = (np.dstack([E.cmap_rdbu(vv[::-1]), np.ones(v.shape)]) * 255).astype(np.uint8)
            m = ImageMobject(img); m.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
            m.stretch_to_fit_width(Wm); m.stretch_to_fit_height(Wm); m.move_to(cm)
            yl = cm[1] - Wm / 2 + n / len(TD) * Wm
            return Group(m, Line(np.array([cm[0] - Wm / 2, yl, 0]), np.array([cm[0] + Wm / 2, yl, 0]), color=AMB, stroke_width=3))
        O = cm - np.array([Wm / 2, Wm / 2, 0])
        frm = VGroup(Rectangle(width=Wm, height=Wm, color=FG, stroke_width=1.5).move_to(cm), DashedLine(O, O + np.array([Wm, Wm, 0]), color=FG, stroke_width=1.2),
                     T(tr("testing time", "tempo di test"), 15, MUT).move_to(cm + np.array([0, -Wm / 2 - 0.3, 0])), T(tr("training time", "tempo di addestramento"), 15, MUT).rotate(PI / 2).move_to(cm + np.array([-Wm / 2 - 0.3, 0, 0])))
        gz = redraw(tgm)
        self.play(FadeIn(gz), FadeIn(frm))
        f = F10.f12_tgm(3.4)
        kk = VGroup(f["k0"], f["k1"], f["kt"]).move_to(np.array([3.6, 1.0, 0]))
        bl = bullets([tr("Train at t, ++test at every t′++ (King & Dehaene, 2014).", "Addestrare a t, ++testare a ogni t′++ (King & Dehaene, 2014)."),
                      tr("++Diagonal++ = transient chain; ++square++ = sustained code.", "++Diagonale++ = catena transitoria; ++quadrato++ = codice sostenuto."),
                      tr("Here: early transient + late sustained code.", "Qui: codice precoce transitorio + tardivo sostenuto.")], 15, n=36, gap=0.25).move_to(np.array([3.6, -1.7, 0]))
        self.play(FadeIn(kk), FadeIn(bl))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: rT.set_value(ph.get_value()))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); gz.clear_updaters()

        # ---------------------------------------------------------- 13 sezione
        self.new(); section_title(self, 3, tr("Applications", "Applicazioni"))

        # ---------------------------------------------------------- 14 BCI: impulso lungo il circuito
        self.new(tr("Applications (1)", "Applicazioni (1)"), tr("Brain–computer interfaces", "Interfacce cervello–computer"))
        f = F10.f15_bci(12.8); fit(f, 1.0, np.array([0, 1.1, 0]))
        self.play(*[FadeIn(f[k]) for k in f], run_time=1.2)
        cs = cards_row([("P300 speller", tr("rare flashes of the attended row/column evoke a ++P3++.", "i lampi rari della riga/colonna attesa evocano una ++P3++.")),
                        ("SSVEP", tr("targets flicker at ++different frequencies++.", "i target lampeggiano a ++frequenze diverse++.")),
                        (tr("Motor imagery", "Immaginazione motoria"), tr("imagined movement → ++mu/beta ERD++.", "movimento immaginato → ++ERD mu/beta++.")),
                        (tr("Uses", "Usi"), tr("++ALS/locked-in++, stroke rehab, neurofeedback.", "++SLA/locked-in++, riabilitazione, neurofeedback."))], 3.0, 1.8, -2.1, 15, 26)
        for c_ in cs: self.play(FadeIn(c_, shift=UP * 0.15), run_time=0.35)
        loop_start(self)
        ph = ValueTracker(0.0)
        pulse = always_redraw(lambda: Dot(f["b0"][0].get_center() + (f["b4"][0].get_center() - f["b0"][0].get_center()) * min(ph.get_value() * 1.5, 1.0), radius=0.13, color=AMB) if ph.get_value() < 0.667
                              else Dot(f["fb"].point_from_proportion((ph.get_value() - 0.667) * 3 * 0.999), radius=0.13, color=ACC))
        self.add(pulse); loop_play(self, ph, 6.0); pulse.clear_updaters()

        # ---------------------------------------------------------- 15 P300 speller e SSVEP dal vivo
        self.new(tr("Applications (2)", "Applicazioni (2)"), tr("P300 speller and SSVEP", "P300 speller e SSVEP"))
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789_"
        c0 = np.array([-3.8, 0.4, 0]); s = 0.55
        grid = VGroup(*[Text(chars[i * 6 + j], font=BODY, font_size=24, color=FG, weight=BOLD).move_to(c0 + np.array([(j - 2.5) * s, (2.5 - i) * s, 0])) for i in range(6) for j in range(6)])
        self.play(FadeIn(grid))
        seq = [("r", 2), ("c", 4), ("r", 0), ("c", 1), ("r", 5), ("c", 3), ("r", 3), ("c", 0), ("r", 1), ("c", 5), ("r", 4), ("c", 2)]
        fT = ValueTracker(0.0)

        def flash():
            k = min(int(fT.get_value() * len(seq)), len(seq) - 1); kind, idx = seq[k]
            if kind == "r":
                return Rectangle(width=6 * s, height=s * 0.9, stroke_width=0, fill_color=AMB, fill_opacity=0.55).move_to(c0 + np.array([0, (2.5 - idx) * s, 0]))
            return Rectangle(width=s * 0.9, height=6 * s, stroke_width=0, fill_color=AMB, fill_opacity=0.55).move_to(c0 + np.array([(idx - 2.5) * s, 0, 0]))
        fl = always_redraw(flash)
        tgt = Circle(radius=0.26, color=ACC, stroke_width=4).move_to(c0 + np.array([(4 - 2.5) * s, (2.5 - 2) * s, 0]))
        lp = T(tr("target \"Q\": its row/column flash → P3", "target \"Q\": la sua riga/colonna lampeggia → P3"), 16, ACC).move_to(c0 + np.array([0, -2.0, 0]))
        self.add(fl); self.play(Create(tgt), FadeIn(lp))
        # SSVEP: quadrato che lampeggia e spettro
        Os = np.array([0.8, -1.4, 0]); Ws = 4.8; Hs = 2.4
        fr = np.linspace(4, 40, 300)
        sp = 1 / fr ** 0.8 * 3 + 2.2 * np.exp(-0.5 * ((fr - 12) / 0.3) ** 2) + 0.9 * np.exp(-0.5 * ((fr - 24) / 0.3) ** 2)
        spec = VGroup(E.axes(Os, Ws + 0.2, Hs + 0.2, "Hz", ""), VMobject(color=TEAL, stroke_width=3).set_points_smoothly([Os + np.array([(a - 4) / 36 * Ws, b / sp.max() * Hs, 0]) for a, b in zip(fr, sp)]),
                      T("12 Hz", 14, ACC).move_to(Os + np.array([(12 - 4) / 36 * Ws, Hs + 0.2, 0])), T("24 Hz", 14, ACC).move_to(Os + np.array([(24 - 4) / 36 * Ws, 0.9 / sp.max() * Hs + 0.6, 0])))
        self.play(FadeIn(spec))
        sq = always_redraw(lambda: Square(0.8, stroke_width=2, stroke_color=FG, fill_color=FG, fill_opacity=0.9 if np.sin(2 * np.pi * 12 * fT.get_value() * 0.5) > 0 else 0.05).move_to(np.array([5.8, 1.4, 0])))
        self.add(sq)
        ls = T(tr("SSVEP: flicker at 12 Hz → peaks at 12, 24 Hz", "SSVEP: lampeggio a 12 Hz → picchi a 12, 24 Hz"), 15, TEAL).move_to(np.array([3.2, 2.0, 0]))
        cap = T(tr("Performance: ++information transfer rate++ (bits/min) = accuracy × classes × speed (Wolpaw et al., 2002).", "Prestazioni: ++tasso di trasferimento d'informazione++ (bit/min) = accuratezza × classi × velocità (Wolpaw et al., 2002)."), 15, n=120).move_to(np.array([0, -3.1, 0]))
        self.play(FadeIn(ls), FadeIn(cap))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: fT.set_value(ph.get_value() * 0.9999))
        self.add(drv); loop_play(self, ph, 6.0); drv.clear_updaters(); fl.clear_updaters(); sq.clear_updaters()

        # ---------------------------------------------------------- 16 clinica
        self.new(tr("Applications (3)", "Applicazioni (3)"), tr("Clinical EEG", "EEG clinico"))
        cs = cards_row([(tr("Epilepsy", "Epilessia"), tr("spikes, seizures, ++presurgical source imaging++ (Brodbeck et al., 2011).", "spike, crisi, ++source imaging prechirurgico++ (Brodbeck et al., 2011).")),
                        (tr("Sleep", "Sonno"), tr("stages, apnoea, ++automatic scoring++.", "stadi, apnee, ++stadiazione automatica++.")),
                        (tr("Consciousness", "Coscienza"), tr("++covert command following++ by decoding (Claassen et al., 2019).", "++risposta nascosta ai comandi++ con il decoding (Claassen et al., 2019).")),
                        (tr("Anaesthesia & dementia", "Anestesia e demenza"), tr("depth monitors; ++slowing++ in dementia.", "monitor di profondità; ++rallentamento++ nella demenza."))], 3.0, 2.6, 0.9, 15, 26)
        for c_ in cs: self.play(FadeIn(c_, shift=UP * 0.15), run_time=0.4)
        D = 4.0; fs = 250; t = np.arange(0, D, 1 / fs)
        x = E.periodic_eeg(D, fs, seed=90, peaks=((10, 1, 0.8),), uv=15)[1]
        for c in (0.9, 2.6):
            x = x + 60 * np.exp(-0.5 * ((t - c) / 0.015) ** 2) - 25 * np.exp(-0.5 * ((t - c - 0.12) / 0.06) ** 2)
        Ot = np.array([-6.0, -1.9, 0])
        tr0 = E.window_trace(t, x, 0, 2.0, Ot, 12.0, 0.012, TEAL, 1.8)
        lab = T(tr("interictal spike-and-wave (simulated)", "complesso punta-onda intercritico (simulato)"), 15, MUT).move_to(np.array([0, -1.0, 0]))
        cap = T(tr("EEG is ++cheap, portable, bedside++, ms-precise: ideal for monitoring and screening.", "L'EEG è ++economico, portatile, al letto del paziente++, preciso al ms: ideale per monitoraggio e screening."), 16, n=110).move_to(np.array([0, -3.0, 0]))
        self.play(Create(tr0), FadeIn(lab), FadeIn(cap))
        scroll_many(self, [(t, x)], [Ot], 12.0, 0.012, 2.0, [TEAL], 4.0, 1.8, old=tr0)

        # ---------------------------------------------------------- 17 EEG-fMRI
        self.new(tr("Applications (4)", "Applicazioni (4)"), tr("Multimodal imaging: EEG–fMRI", "Imaging multimodale: EEG–fMRI"))
        rng = np.random.default_rng(4)
        tt = np.arange(0, 120, 0.1)
        alpha = 1 + 0.5 * np.sin(2 * np.pi * tt / 30) + 0.3 * np.sin(2 * np.pi * tt / 12 + 1) + 0.1 * np.sin(2 * np.pi * tt / 60)
        th = np.arange(0, 30, 0.1)
        hrf = th ** 5 * np.exp(-th) / 120 - 0.1 * th ** 15 * np.exp(-th) / 1.3e12
        reg = np.convolve(np.tile(alpha - alpha.mean(), 2), hrf)[len(tt):2 * len(tt)]; reg /= np.abs(reg).max()
        bold = -reg + 0.15 * np.sin(2 * np.pi * tt / 5)
        sigs = [(tt, alpha - 1), (tt, reg), (tt, bold)]
        Os = [np.array([-6.0, 1.3, 0]), np.array([-6.0, 0.0, 0]), np.array([-6.0, -1.3, 0])]
        cols = [TEAL, ACC, AMB]
        labs = VGroup(T(tr("EEG alpha power", "potenza alfa EEG"), 15, TEAL).move_to(Os[0] + np.array([1.2, 0.7, 0])), T(tr("⊗ HRF → regressor", "⊗ HRF → regressore"), 15, ACC).move_to(Os[1] + np.array([1.2, 0.6, 0])),
                      T(tr("occipital BOLD (anti-correlated)", "BOLD occipitale (anticorrelato)"), 15, AMB).move_to(Os[2] + np.array([1.8, 0.6, 0])))
        tr0 = VGroup(*[E.window_trace(a, b, 0, 40.0, O, 7.0, 0.5, c, 2.5) for (a, b), O, c in zip(sigs, Os, cols)])
        self.play(FadeIn(labs), Create(tr0))
        bl = bullets([tr("EEG = ++when++ (ms), fMRI = ++where++ (mm).", "EEG = ++quando++ (ms), fMRI = ++dove++ (mm)."),
                      tr("*EEG-informed fMRI*: alpha ↔ ++negative++ occipital BOLD (Goldman et al., 2002; Laufs et al., 2003).", "*fMRI informata dall'EEG*: alfa ↔ BOLD occipitale ++negativo++ (Goldman et al., 2002; Laufs et al., 2003)."),
                      tr("Artifacts: ++gradient++, ++ballistocardiogram++ (Allen et al., 1998, 2000).", "Artefatti: ++gradiente++, ++balistocardiogramma++ (Allen et al., 1998, 2000)."),
                      tr("Also EEG+TMS, EEG+fNIRS, EEG+eye tracking.", "Anche EEG+TMS, EEG+fNIRS, EEG+eye tracking.")], 15, n=34, gap=0.26).move_to(np.array([4.4, -0.2, 0]))
        self.play(FadeIn(bl))
        scroll_many(self, sigs, Os, 7.0, 0.5, 40.0, cols, 10.0, 2.5, old=tr0)

        # ---------------------------------------------------------- 18 sezione
        self.new(); section_title(self, 4, tr("In practice and wrap-up", "In pratica e sintesi"))

        # ---------------------------------------------------------- 19 MATLAB
        self.new(tr("In MATLAB", "In MATLAB"), tr("Time-resolved decoding with cross-validation", "Decoding nel tempo con cross-validation"))
        code = ["X = cat(3, A.data, B.data);  X = permute(X, [3 1 2]);        % trials x channels x time",
                "y = [zeros(size(A.data,3),1); ones(size(B.data,3),1)];",
                "cv = cvpartition(y, 'KFold', 5);  nT = size(X,3);  acc = zeros(1,nT);",
                "for t = 1:nT",
                "    Xt = X(:,:,t);  c = 0;",
                "    for k = 1:cv.NumTestSets",
                "        tr = training(cv,k);  te = test(cv,k);",
                "        mdl = fitcdiscr(Xt(tr,:), y(tr), 'DiscrimType','linear', 'Gamma',0.2);",
                "        c = c + sum(predict(mdl, Xt(te,:)) == y(te));",
                "    end",
                "    acc(t) = c / numel(y);",
                "end",
                "w = mdl.Coeffs(1,2).Linear;                                   % weights",
                "Apat = cov(Xt) * w;                                           % activation pattern",
                "plot(A.times, acc); yline(0.5, '--'); xlabel('time (ms)'); ylabel('accuracy');",
                "% chance: repeat with y(randperm(numel(y))) 1000 times -> null distribution"]
        cl = code_lines(code, 15)
        if cl.width > 12.6: cl.scale_to_fit_width(12.6)
        cc_ = card(cl, CARD, pad=0.25).move_to(np.array([0, -0.45, 0]))
        self.play(FadeIn(cc_[0]))
        self.play(LaggedStart(*[FadeIn(x_, shift=RIGHT * 0.1) for x_ in cl], lag_ratio=0.12), run_time=3.0)

        # ---------------------------------------------------------- 20 etica
        self.new(tr("Ethics", "Etica"), tr("Neural data are personal data", "I dati neurali sono dati personali"))
        g = rows_mob([tr("Decoding reads ++information++, not \"thoughts\": limited, task-specific.", "Il decoding legge ++informazione++, non \"pensieri\": limitato, specifico del compito."),
                      tr("EEG is ++health/biometric data++ (GDPR): consent, anonymisation.", "L'EEG è un ++dato sanitario/biometrico++ (GDPR): consenso, anonimizzazione."),
                      tr("++Mental privacy++ and ++cognitive liberty++ (Ienca & Andorno, 2017; Yuste et al., 2017).", "++Privacy mentale++ e ++libertà cognitiva++ (Ienca & Andorno, 2017; Yuste et al., 2017)."),
                      tr("Report limits honestly: avoid ++hype++.", "Riportare onestamente i limiti: evitare l'++hype++.")], 20).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.2), run_time=2.0)

        # ---------------------------------------------------------- 21 sintesi del corso: il percorso si illumina
        self.new(tr("Course wrap-up", "Sintesi del corso"), tr("Ten lectures in one slide", "Dieci lezioni in una slide"))
        items = [tr("History & what EEG measures", "Storia e cosa misura l'EEG"), tr("Cellular bases", "Basi cellulari"), tr("From neurons to scalp", "Dai neuroni allo scalpo"),
                 tr("Recording", "Registrazione"), tr("Preprocessing & ICA", "Pre-elaborazione e ICA"), tr("Spectra & time-frequency", "Spettri e tempo-frequenza"),
                 tr("ERPs", "ERP"), tr("Spatial analysis & microstates", "Analisi spaziale e microstati"), tr("Sources & connectivity", "Sorgenti e connettività"), tr("Decoding & applications", "Decoding e applicazioni")]
        boxes = VGroup()
        for k, it in enumerate(items):
            col, row = k // 5, k % 5
            b = RoundedRectangle(corner_radius=0.12, width=5.8, height=0.62, fill_color=CARD if col == 0 else CARD2, fill_opacity=1, stroke_width=0)
            lb = VGroup(TX(f"{k + 1}", font=SERIF_F, font_size=24, color=ACC, weight=BOLD), T(it, 18)).arrange(RIGHT, buff=0.3)
            lb.move_to(b).align_to(b, LEFT).shift(RIGHT * 0.3)
            boxes.add(VGroup(b, lb).move_to(np.array([-3.1 + 6.2 * col, 1.3 - 0.75 * row, 0])))
        self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.15) for b_ in boxes], lag_ratio=0.1), run_time=2.0)
        cap = T(tr("~Physics~ → ~recording~ → ~cleaning~ → ~time, frequency, space~ → ~sources, networks~ → ~prediction~", "~Fisica~ → ~registrazione~ → ~pulizia~ → ~tempo, frequenza, spazio~ → ~sorgenti, reti~ → ~predizione~"), 18, n=120).move_to(np.array([0, -2.6, 0]))
        self.play(FadeIn(cap))
        loop_start(self)
        ph = ValueTracker(0.0)
        hl = always_redraw(lambda: SurroundingRectangle(boxes[min(int(ph.get_value() * 10), 9)], color=AMB, stroke_width=5, buff=0.06, corner_radius=0.14))
        self.add(hl); loop_play(self, ph, 10.0); hl.clear_updaters()

        # ---------------------------------------------------------- 22 domande
        self.new(tr("Check your understanding", "Verifica"), tr("Three questions", "Tre domande"))
        g = rows_mob([tr("10 best channels selected on all data, then cross-validation: 95 %. What went wrong?", "10 canali migliori scelti su tutti i dati, poi cross-validation: 95 %. Che cosa non va?"),
                      tr("Large classifier weight at Fp1: does Fp1 carry the effect?", "Peso grande del classificatore in Fp1: Fp1 contiene l'effetto?"),
                      tr("The temporal generalisation matrix is a thin diagonal: meaning?", "La matrice di generalizzazione temporale è una sottile diagonale: significato?")], 21, n=84, h=1.05, gap=0.35, col=ACC).shift(DOWN * 0.3)
        for r_ in g: self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.7)

        # ---------------------------------------------------------- 23 messaggi chiave
        self.new(tr("Take-home messages", "Messaggi chiave"), tr("Take-home messages", "Messaggi chiave"))
        g = rows_mob([tr("Decoding: \"++is the information there, and when?++\"", "Decoding: \"++l'informazione c'è, e quando?++\""),
                      tr("++Cross-validate++, regularise, avoid ++leakage++; permutation for chance.", "++Cross-validation++, regolarizzazione, niente ++leakage++; permutazioni per il caso."),
                      tr("Interpret ++patterns++, not weights.", "Interpretare i ++pattern++, non i pesi."),
                      tr("Temporal generalisation reveals the ++dynamics of codes++.", "La generalizzazione temporale rivela la ++dinamica dei codici++."),
                      tr("EEG powers ++BCIs, clinical monitoring, multimodal imaging++ — ethically.", "L'EEG alimenta ++BCI, monitoraggio clinico, imaging multimodale++ — con etica.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 24 letture
        self.new(tr("Suggested reading", "Letture consigliate"), tr("Suggested reading", "Letture consigliate"))
        refs_slide(self, ["Grootswagers, Wardle & Carlson (2017) *J Cogn Neurosci* 29:677–697.", "King & Dehaene (2014) *Trends Cogn Sci* 18:203–210.",
                          "Haufe et al. (2014) *NeuroImage* 87:96–110.", "Blankertz et al. (2011) *NeuroImage* 56:814–825.",
                          "Varoquaux et al. (2017) *NeuroImage* 145:166–179.", "Combrisson & Jerbi (2015) *J Neurosci Methods* 250:126–136.",
                          "Wolpaw et al. (2002) *Clin Neurophysiol* 113:767–791.", "Lotte et al. (2018) *J Neural Eng* 15:031005.",
                          "Laufs et al. (2003) *NeuroImage* 19:1463–1476.", "Claassen et al. (2019) *N Engl J Med* 380:2497–2505.",
                          "Treder (2020) *Front Neurosci* 14:289.", "Yuste et al. (2017) *Nature* 551:159–163."], 17)
        self.end()
