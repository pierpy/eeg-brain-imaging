from base import *
import figs5 as F5


def uni_sources(n=900, seed=2):
    rng = np.random.default_rng(seed)
    return rng.uniform(-np.sqrt(3), np.sqrt(3), (2, n))


class B5_ICA(Base):
    start_num = 14

    def construct(self):
        # ---------------------------------------------------------- 14 sezione
        self.new(first=True); section_title(self, 4, tr("Independent Component Analysis", "Analisi delle componenti indipendenti"))

        # ---------------------------------------------------------- 15 cocktail party (dal vivo)
        self.new(tr("ICA (1)", "ICA (1)"), tr("The cocktail-party problem", "Il problema del cocktail party"))
        D = 4.0; fs = 250; t = np.arange(0, D, 1 / fs)
        s1 = np.sign(np.sin(2 * np.pi * 1.0 * t + 0.3)) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.25 * t))
        s2 = np.sin(2 * np.pi * 3.0 * t) ** 3
        S = np.vstack([s1, s2]); X = F5.MIX @ S
        Wt = 2.8; ys = [1.0, -0.6]
        cols3 = [[ACC, TEAL], [FG, FG], [ACC, TEAL]]
        xs = [-6.3, -1.4, 3.5]
        sigs = [(t, S[0]), (t, S[1]), (t, X[0]), (t, X[1]), (t, S[0]), (t, S[1])]
        Os = [np.array([xs[c], ys[k], 0]) for c in range(3) for k in range(2)]
        cols = [cols3[c][k] for c in range(3) for k in range(2)]
        hh = [0.42, 0.42, 0.34, 0.34, 0.42, 0.42]
        labs = VGroup(T(tr("~sources~ (brain, eyes…)", "~sorgenti~ (cervello, occhi…)"), 18), T(tr("~electrodes~ = mixtures", "~elettrodi~ = miscele"), 18), T(tr("~ICA~: recovered", "~ICA~: recuperate"), 18))
        for c in range(3): labs[c].move_to(np.array([xs[c] + Wt / 2, 1.95, 0]))
        tr0 = VGroup(*[E.window_trace(tt, x, 0.0, 2.0, O, Wt, h, c, 2) for (tt, x), O, c, h in zip(sigs, Os, cols, hh)])
        arA = VGroup(Arrow(np.array([-3.35, 0.2, 0]), np.array([-1.6, 0.2, 0]), buff=0, color=FG, stroke_width=4, tip_length=0.2), M(r"\mathbf{A}", FG, 0.9).move_to(np.array([-2.45, 0.6, 0])))
        arW = VGroup(Arrow(np.array([1.55, 0.2, 0]), np.array([3.3, 0.2, 0]), buff=0, color=FG, stroke_width=4, tip_length=0.2), M(r"\mathbf{W}", FG, 0.9).move_to(np.array([2.45, 0.6, 0])))
        self.play(FadeIn(labs[0]), Create(tr0[0]), Create(tr0[1]), run_time=1.0)
        self.play(GrowArrow(arA[0]), FadeIn(arA[1]), FadeIn(labs[1]), Create(tr0[2]), Create(tr0[3]), run_time=1.0)
        self.play(GrowArrow(arW[0]), FadeIn(arW[1]), FadeIn(labs[2]), Create(tr0[4]), Create(tr0[5]), run_time=1.0)
        bl = bullets([tr("Several people talk at once; each microphone records a ++different mixture++. Recover each voice without knowing the room?", "Più persone parlano insieme; ogni microfono registra una ++miscela diversa++. Recuperare ogni voce senza conoscere la stanza?"),
                      tr("EEG: electrodes = microphones; brain, eyes, muscles, heart = speakers; volume conduction = ++instantaneous linear mixing++.", "EEG: elettrodi = microfoni; cervello, occhi, muscoli, cuore = oratori; conduzione di volume = ++miscelazione lineare istantanea++."),
                      tr("ICA is ++blind++: it uses only the statistics of the data (Bell & Sejnowski, 1995; Makeig et al., 1996).", "L'ICA è ++cieca++: usa solo la statistica dei dati (Bell & Sejnowski, 1995; Makeig et al., 1996).")], 17, n=100, gap=0.2).move_to(np.array([0, -2.3, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.45)
        loop_start(self)
        ph = ValueTracker(0.0)
        live = always_redraw(lambda: VGroup(*[E.window_trace(tt, x, ph.get_value() * D, 2.0, O, Wt, h, c, 2) for (tt, x), O, c, h in zip(sigs, Os, cols, hh)]))
        self.remove(tr0); self.add(live); loop_play(self, ph, 4.0); live.clear_updaters()

        # ---------------------------------------------------------- 16 modello: la nuvola che si "raddrizza"
        self.new(tr("ICA (2)", "ICA (2)"), tr("The model and its assumptions", "Il modello e le sue ipotesi"))
        fm = fcard(r"\mathbf{x}(t) = \mathbf{A}\,\mathbf{s}(t) \qquad \hat{\mathbf{s}}(t) = \mathbf{W}\,\mathbf{x}(t),\ \ \mathbf{W}\approx\mathbf{A}^{-1}", CARD2, 0.72).move_to(np.array([-3.2, 1.85, 0]))
        self.play(FadeIn(fm))
        Su = uni_sources(500)
        cc = np.array([-3.2, -0.75, 0]); sc = 0.62
        tauT = ValueTracker(0.0)
        Ainv = np.linalg.inv(F5.MIX)

        def cloud():
            tau = tauT.get_value()
            Mx = (1 - tau) * np.eye(2) + tau * Ainv
            P_ = Mx @ (F5.MIX @ Su)
            col = interpolate_color(ManimColor(ACC), ManimColor(TEAL), tau)
            g = VGroup(*[Dot(cc + np.array([a * sc, b * sc, 0]), radius=0.022, color=col) for a, b in zip(P_[0], P_[1])])
            g.add(T(tr("mixtures x₁, x₂", "miscele x₁, x₂") if tau < 0.5 else tr("unmixed = independent", "separate = indipendenti"), 18, col).move_to(cc + np.array([0, -2.05, 0])))
            return g
        axc = VGroup(Line(cc + np.array([-2.0, 0, 0]), cc + np.array([2.0, 0, 0]), color=MUT, stroke_width=1.5), Line(cc + np.array([0, -1.7, 0]), cc + np.array([0, 1.7, 0]), color=MUT, stroke_width=1.5))
        cz = always_redraw(cloud)
        self.play(Create(axc), FadeIn(cz))
        bl = bullets([tr("*Columns of A*: scalp maps of the components.", "*Colonne di A*: mappe di scalpo delle componenti."),
                      tr("*Rows of W*: spatial filters that extract them.", "*Righe di W*: filtri spaziali che le estraggono."),
                      tr("~Assumptions~: sources ++independent++ and ++non-Gaussian++; mixing ++linear, instantaneous, stationary++; sources ≤ channels (rank).", "~Ipotesi~: sorgenti ++indipendenti++ e ++non gaussiane++; miscelazione ++lineare, istantanea, stazionaria++; sorgenti ≤ canali (rango)."),
                      tr("Order, sign and scale are ++arbitrary++.", "Ordine, segno e scala sono ++arbitrari++.")], 17, n=40, gap=0.28).move_to(np.array([3.6, -0.2, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.45)
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: tauT.set_value(0.5 - 0.5 * np.cos(2 * np.pi * ph.get_value())))
        self.add(drv); loop_play(self, ph, 6.0); drv.clear_updaters(); cz.clear_updaters()

        # ---------------------------------------------------------- 17 non gaussianità: proiezione che ruota, istogramma e curtosi
        self.new(tr("ICA (3)", "ICA (3)"), tr("Why non-Gaussianity reveals the sources", "Perché la non gaussianità rivela le sorgenti"))
        Su = uni_sources(4000, 5)
        th0 = np.radians(30)
        R0 = np.array([[np.cos(th0), -np.sin(th0)], [np.sin(th0), np.cos(th0)]])
        Z = R0 @ Su   # dati sbiancati = rotazione delle sorgenti
        ths = np.linspace(0, np.pi, 361)
        kur = np.array([np.mean((np.cos(a) * Z[0] + np.sin(a) * Z[1]) ** 4) - 3 for a in ths])
        thT = ValueTracker(0.0)
        cs = np.array([-4.9, 0.1, 0]); ssc = 0.55
        dots = VGroup(*[Dot(cs + np.array([a * ssc, b * ssc, 0]), radius=0.015, color=MUT) for a, b in zip(Z[0][:700], Z[1][:700])])
        lsc = T(tr("whitened data", "dati sbiancati"), 16, MUT).move_to(cs + np.array([0, -1.55, 0]))
        Oh = np.array([-2.6, -1.0, 0]); Wh = 3.4; Hh = 2.2
        Ok = np.array([1.6, -1.0, 0]); Wk = 4.6; Hk = 2.2
        yk = lambda k: (k + 1.3) / 1.4 * Hk

        def live():
            a = thT.get_value(); u = np.array([np.cos(a), np.sin(a), 0])
            y = np.cos(a) * Z[0] + np.sin(a) * Z[1]
            h, e = np.histogram(y, 28, range=(-2.6, 2.6), density=True)
            wb = Wh / 28
            g = VGroup(Line(cs - 1.5 * u, cs + 1.5 * u, color=AMB, stroke_width=4))
            kk = float(np.interp(a, ths, kur))
            col = ACC if kk < -0.95 else TEAL
            g.add(VGroup(*[Rectangle(width=wb * 0.9, height=max(v / 0.45 * Hh * 0.8, 0.005), stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(Oh + np.array([wb * (i + 0.5), 0, 0]), aligned_edge=DOWN) for i, v in enumerate(h)]))
            g.add(Dot(Ok + np.array([a / np.pi * Wk, yk(kk), 0]), radius=0.09, color=AMB))
            g.add(T(tr(f"projection angle **{np.degrees(a):.0f}°** → excess kurtosis **{kk:+.2f}**", f"angolo di proiezione **{np.degrees(a):.0f}°** → curtosi in eccesso **{kk:+.2f}**").replace(".", "." if LANG == "en" else ","), 19, AMB).move_to(np.array([0.2, 1.95, 0])))
            return g
        kc = VMobject(color=TEAL, stroke_width=3).set_points_smoothly([Ok + np.array([a / np.pi * Wk, yk(k), 0]) for a, k in zip(ths[::6], kur[::6])])
        axk = VGroup(Line(Ok, Ok + np.array([Wk, 0, 0]), color=MUT, stroke_width=1.5), Line(Ok, Ok + np.array([0, Hk, 0]), color=MUT, stroke_width=1.5),
                     DashedLine(Ok + np.array([0, yk(0), 0]), Ok + np.array([Wk, yk(0), 0]), color=MUT, stroke_width=1.2),
                     T("0°", 13, MUT).move_to(Ok + np.array([0, -0.25, 0])), T("180°", 13, MUT).move_to(Ok + np.array([Wk, -0.25, 0])),
                     T(tr("kurtosis vs angle: minima = sources", "curtosi vs angolo: minimi = sorgenti"), 15, MUT).move_to(Ok + np.array([Wk / 2, -0.6, 0])),
                     T(tr("histogram of the projection", "istogramma della proiezione"), 15, MUT).move_to(Oh + np.array([Wh / 2, -0.6, 0])),
                     Line(Oh, Oh + np.array([Wh, 0, 0]), color=MUT, stroke_width=1.5))
        lv = always_redraw(live)
        self.play(FadeIn(dots), FadeIn(lsc), FadeIn(axk), Create(kc), FadeIn(lv), run_time=1.5)
        bl = T(tr("A mixture is ++more Gaussian++ than its sources (central limit theorem): rotate until the output is ++least Gaussian++.", "Una miscela è ++più gaussiana++ delle sue sorgenti (limite centrale): ruotare finché l'uscita è ++meno gaussiana++."), 17, n=110).move_to(np.array([0, -2.3, 0]))
        mt = metaphor(tr("a ++smoothie++ tastes \"average\": to recognise the fruits, look for the most distinctive flavours.", "un ++frullato++ ha un sapore \"medio\": per riconoscere i frutti, cerca i sapori più distintivi."), 15, n=130).move_to(np.array([0, -3.05, 0]))
        self.play(FadeIn(bl), FadeIn(mt))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: thT.set_value(np.pi * ph.get_value() * 0.9999))
        self.add(drv); loop_play(self, ph, 10.0); drv.clear_updaters(); lv.clear_updaters()

        # ---------------------------------------------------------- 18 algoritmi
        self.new(tr("ICA (4)", "ICA (4)"), tr("Algorithms and practical recipes", "Algoritmi e ricette pratiche"))
        algs = [("Infomax / ext.", tr("max. information flow; EEGLAB runica (Bell & Sejnowski, 1995; Lee et al., 1999)", "max. flusso d'informazione; runica di EEGLAB (Bell & Sejnowski, 1995; Lee et al., 1999)")),
                ("FastICA", tr("negentropy, fixed-point; fast, less stable (Hyvärinen, 1999)", "negentropia, punto fisso; veloce, meno stabile (Hyvärinen, 1999)")),
                ("AMICA", tr("adaptive mixtures; best separation, slower (Delorme et al., 2012)", "miscele adattive; migliore separazione, più lento (Delorme et al., 2012)")),
                ("SOBI", tr("second-order, temporal correlations (Belouchrani et al., 1997)", "secondo ordine, correlazioni temporali (Belouchrani et al., 1997)"))]
        cs_ = VGroup()
        for k, (h_, d_) in enumerate(algs):
            box = RoundedRectangle(corner_radius=0.14, width=3.0, height=2.1, fill_color=CARD if k % 2 == 0 else CARD2, fill_opacity=1, stroke_width=0)
            tx = VGroup(TX(h_, font=BODY, font_size=20, color=TEAL, weight=BOLD), T(d_, 15, n=30)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            tx.move_to(box).align_to(box, UP).shift(DOWN * 0.22)
            cs_.add(VGroup(box, tx))
        cs_.arrange(RIGHT, buff=0.2).move_to(np.array([0, 1.15, 0]))
        for c_ in cs_: self.play(FadeIn(c_, shift=UP * 0.15), run_time=0.4)
        g = rows_mob([tr("Train ICA on a ++1-Hz high-passed copy++, apply the weights to the 0.1-Hz data (Winkler et al., 2015).", "Addestrare l'ICA su una ++copia filtrata a 1 Hz++, applicare i pesi ai dati a 0,1 Hz (Winkler et al., 2015)."),
                      tr("Enough data: ++≈ 20–30 × N²++ samples; remove gross, non-stereotyped artifacts first.", "Dati sufficienti: ++≈ 20–30 × N²++ campioni; togliere prima gli artefatti grossolani non stereotipati."),
                      tr("Number of components = ++data rank++ (after reference and interpolation).", "Numero di componenti = ++rango dei dati++ (dopo riferimento e interpolazione).")], 18, n=96, h=0.72, gap=0.14, col=ACC).move_to(np.array([0, -1.75, 0]))
        for r_ in g: self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.5)

        # ---------------------------------------------------------- 19 galleria di componenti (andamenti che scorrono)
        self.new(tr("ICA (5)", "ICA (5)"), tr("Reading components: map, time course, spectrum", "Leggere le componenti: mappa, andamento, spettro"))
        maps = Group(); labs = VGroup(); sigs = []; Os = []; cols = []
        for k, (kind, lab, (pos, mom), blur) in enumerate(F5.IC_DEFS):
            c = np.array([-5.2 + 2.6 * k, 1.05, 0])
            V, mk = E.dipole_map(pos, mom, n=121, blur=blur)
            img, out = E.topomap(V, mk, c, 0.8)
            maps.add(Group(img, out))
            labs.add(T(lab, 15, FG).move_to(c + np.array([0, -1.1, 0])))
            tt, x = F5.ic_timecourse(kind, 3.0)
            sigs.append((tt, x / np.abs(x).max())); Os.append(c + np.array([-1.1, -1.75, 0])); cols.append(TEAL if kind == "brain" else ACC)
        tr0 = VGroup(*[E.window_trace(tt, x, 0.0, 1.5, O, 2.2, 0.36, c, 1.4) for (tt, x), O, c in zip(sigs, Os, cols)])
        for k in range(5):
            self.play(FadeIn(maps[k]), FadeIn(labs[k]), Create(tr0[k]), run_time=0.5)
        bl = bullets([tr("*Brain*: smooth ++dipolar++ map, 1/f spectrum with peaks. *Eye*: frontal map, blinks/saccades, low frequencies.", "*Cervello*: mappa ++dipolare++ liscia, spettro 1/f con picchi. *Occhio*: mappa frontale, ammiccamenti/saccadi, basse frequenze."),
                      tr("*Muscle*: focal at the edge, ++broadband > 20 Hz++. *Heart*: broad gradient, regular beats. *Channel/line*: one electrode or 50 Hz.", "*Muscolo*: focale al bordo, ++banda larga > 20 Hz++. *Cuore*: gradiente ampio, battiti regolari. *Canale/rete*: un elettrodo o 50 Hz."),
                      tr("Guide: Chaumon, Bishop & Busch (2015).", "Guida: Chaumon, Bishop & Busch (2015).")], 16, n=110, gap=0.14).move_to(np.array([0, -2.75, 0]))
        self.play(FadeIn(bl))
        scroll_many(self, sigs, Os, 2.2, 0.36, 1.5, cols, 3.0, 1.4, old=tr0)

        # ---------------------------------------------------------- 20 ICLabel
        self.new(tr("ICA (6)", "ICA (6)"), tr("ICLabel: automatic component classification", "ICLabel: classificazione automatica delle componenti"))
        cls = [("Brain", 0.02), ("Muscle", 0.01), ("Eye", 0.95), ("Heart", 0.00), ("Line Noise", 0.00), ("Channel Noise", 0.01), ("Other", 0.01)]
        hdr = T(tr("~Example: IC 1 (blink)~", "~Esempio: IC 1 (ammiccamento)~"), 19).move_to(np.array([-3.6, 1.85, 0]))
        rows_ = VGroup(); bars_ = VGroup()
        for k, (c_, p_) in enumerate(cls):
            y = 1.2 - 0.52 * k
            rows_.add(VGroup(T(c_, 16).move_to(np.array([-5.3, y, 0])), T((f"{p_:.2f}").replace(".", "." if LANG == "en" else ","), 15, MUT).move_to(np.array([-0.9, y, 0]))))
            bars_.add(Rectangle(width=max(3.0 * p_, 0.03), height=0.28, stroke_width=0, fill_color=ACC if p_ > 0.5 else TEAL, fill_opacity=1).move_to(np.array([-4.2, y, 0]), aligned_edge=LEFT))
        self.play(FadeIn(hdr), FadeIn(rows_))
        self.play(LaggedStart(*[GrowFromEdge(b_, LEFT) for b_ in bars_], lag_ratio=0.1), run_time=1.5)
        bl = bullets([tr("A neural network trained on thousands of expert-labelled ICs → ++7 class probabilities++ (Pion-Tonachini et al., 2019).", "Una rete neurale addestrata su migliaia di IC etichettate → ++7 probabilità di classe++ (Pion-Tonachini et al., 2019)."),
                      tr("Typical rule: flag *Eye* and *Muscle* ICs with p > 0.8–0.9.", "Regola tipica: marcare le IC *Oculari* e *Muscolari* con p > 0,8–0,9."),
                      tr("A ++help, not an oracle++: check maps, spectra, time courses.", "Un ++aiuto, non un oracolo++: controllare mappe, spettri, andamenti."),
                      tr("Report algorithm, rank, number of ICs removed and criterion.", "Riportare algoritmo, rango, numero di IC rimosse e criterio.")], 17, n=40, gap=0.3).move_to(np.array([3.7, -0.3, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.4)

        # ---------------------------------------------------------- 21 retro-proiezione (grezzo vs pulito, dal vivo)
        self.new(tr("ICA (7)", "ICA (7)"), tr("Removing artifacts: back-projection", "Rimuovere gli artefatti: retro-proiezione"))
        t, names, brain, raw = F5.blink_mix(4.0)
        Wr = 4.8; ys = [1.35 - 0.75 * k for k in range(4)]
        Os = [np.array([-5.9, y, 0]) for y in ys] + [np.array([1.3, y, 0]) for y in ys]
        sigs = [(t, x) for x in raw] + [(t, x) for x in brain]
        cols = [ACC] * 4 + [TEAL] * 4
        nm = VGroup(*[T(n, 15, MUT).move_to(np.array([-6.35, y, 0])) for n, y in zip(names, ys)])
        hd = VGroup(T(tr("~raw~", "~grezzo~"), 19).move_to(np.array([-5.9 + Wr / 2, 2.05, 0])), T(tr("~cleaned~ (eye IC removed)", "~pulito~ (IC oculare rimossa)"), 19).move_to(np.array([1.3 + Wr / 2, 2.05, 0])))
        ar = Arrow(np.array([-0.8, 0.2, 0]), np.array([0.9, 0.2, 0]), buff=0, color=FG, stroke_width=4, tip_length=0.2)
        tr0 = VGroup(*[E.window_trace(tt, x, 0.0, 2.0, O, Wr, 0.0035, c, 1.5) for (tt, x), O, c in zip(sigs, Os, cols)])
        self.play(FadeIn(nm), FadeIn(hd[0]), LaggedStart(*[Create(x) for x in tr0[:4]], lag_ratio=0.1), run_time=1.2)
        self.play(GrowArrow(ar), FadeIn(hd[1]), LaggedStart(*[Create(x) for x in tr0[4:]], lag_ratio=0.1), run_time=1.2)
        fm = fcard(r"\mathbf{x}_{clean}(t) = \sum_{k\,\notin\,\mathrm{artifacts}} \mathbf{a}_k\, s_k(t)", CARD2, 0.75).move_to(np.array([0, -2.0, 0]))
        bl = T(tr("Zero the artifact ICs and ++re-mix++ the rest: all trials kept. ⚠ Remove ++only clear++ artifacts: poorly separated ICs contain brain signal.", "Azzerare le IC artefattuali e ++ri-miscelare++ il resto: si tengono tutti i trial. ⚠ Rimuovere ++solo artefatti chiari++: IC mal separate contengono segnale cerebrale."), 16, n=120).move_to(np.array([0, -3.05, 0]))
        self.play(FadeIn(fm), FadeIn(bl))
        scroll_many(self, sigs, Os, Wr, 0.0035, 2.0, cols, 4.0, 1.5, old=tr0)

        # ---------------------------------------------------------- 22 sezione
        self.new(); section_title(self, 5, tr("Pipelines in practice", "Pipeline in pratica"))

        # ---------------------------------------------------------- 23 EEGLAB
        self.new(tr("In MATLAB", "In MATLAB"), tr("A minimal EEGLAB pipeline", "Una pipeline EEGLAB minima"))
        code = ["EEG = pop_loadset('sub-01_task-oddball_eeg.set');",
                "EEG = pop_eegfiltnew(EEG, 'locutoff', 0.1, 'hicutoff', 40);   % zero-phase FIR",
                "orig = EEG.chanlocs;",
                "EEG = pop_clean_rawdata(EEG, 'FlatlineCriterion', 5, 'ChannelCriterion', 0.8, ...",
                "        'LineNoiseCriterion', 4, 'BurstCriterion', 'off', 'WindowCriterion', 'off');",
                "EEG = pop_interp(EEG, orig, 'spherical');                      % bad channels",
                "EEG = pop_reref(EEG, []);                                      % average reference",
                "tmp = pop_eegfiltnew(EEG, 'locutoff', 1);                      % 1-Hz copy for ICA",
                "tmp = pop_runica(tmp, 'icatype', 'runica', 'extended', 1, 'pca', rank(double(tmp.data')));",
                "EEG.icaweights = tmp.icaweights; EEG.icasphere = tmp.icasphere;",
                "EEG.icachansind = tmp.icachansind; EEG.icawinv = []; EEG = eeg_checkset(EEG);",
                "EEG = pop_iclabel(EEG, 'default');",
                "EEG = pop_icflag(EEG, [NaN NaN; 0.9 1; 0.9 1; NaN NaN; NaN NaN; NaN NaN; NaN NaN]);",
                "EEG = pop_subcomp(EEG, find(EEG.reject.gcompreject), 0);       % back-projection",
                "EEG = pop_epoch(EEG, {'S1'}, [-0.2 0.8]);",
                "EEG = pop_rmbase(EEG, [-200 0]);"]
        cl = code_lines(code, 15)
        if cl.width > 12.6: cl.scale_to_fit_width(12.6)
        cc_ = card(cl, CARD, pad=0.25).move_to(np.array([0, -0.45, 0]))
        self.play(FadeIn(cc_[0]))
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.1) for x in cl], lag_ratio=0.12), run_time=3.0)

        # ---------------------------------------------------------- 24 pipeline automatiche
        self.new(tr("Pipelines", "Pipeline"), tr("Automated pipelines and reporting", "Pipeline automatiche e documentazione"))
        pp = [("PREP", tr("robust referencing, bad channels (Bigdely-Shamlo et al., 2015)", "riferimento robusto, canali cattivi (Bigdely-Shamlo et al., 2015)")),
              ("HAPPE", tr("infants, short noisy recordings (Gabard-Durnam et al., 2018)", "neonati, registrazioni brevi e rumorose (Gabard-Durnam et al., 2018)")),
              ("Automagic", tr("large datasets, quality ratings (Pedroni et al., 2019)", "grandi dataset, valutazioni di qualità (Pedroni et al., 2019)")),
              ("MNE / FieldTrip", tr("Python / MATLAB: same steps, different defaults", "Python / MATLAB: stessi passi, default diversi"))]
        cs_ = VGroup()
        for k, (h_, d_) in enumerate(pp):
            box = RoundedRectangle(corner_radius=0.14, width=3.0, height=1.9, fill_color=CARD if k % 2 == 0 else CARD2, fill_opacity=1, stroke_width=0)
            tx = VGroup(TX(h_, font=BODY, font_size=20, color=TEAL, weight=BOLD), T(d_, 15, n=30)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            tx.move_to(box).align_to(box, UP).shift(DOWN * 0.22)
            cs_.add(VGroup(box, tx))
        cs_.arrange(RIGHT, buff=0.2).move_to(np.array([0, 1.2, 0]))
        for c_ in cs_: self.play(FadeIn(c_, shift=UP * 0.15), run_time=0.4)
        bl = bullets([tr("Automatic ≠ unsupervised: check ++quality metrics++ and plots for every subject.", "Automatico ≠ non supervisionato: controllare ++metriche di qualità++ e grafici per ogni soggetto."),
                      tr("Choices create a ++\"garden of forking paths\"++: fix the pipeline ++before++ looking at effects (pre-registration).", "Le scelte creano un ++\"giardino dei sentieri che si biforcano\"++: fissare la pipeline ++prima++ di guardare gli effetti (pre-registrazione)."),
                      tr("Report following ++COBIDAS-MEEG++ (Pernet et al., 2020); share code and BIDS data.", "Documentare secondo ++COBIDAS-MEEG++ (Pernet et al., 2020); condividere codice e dati BIDS.")], 18, n=90, gap=0.25).move_to(np.array([0, -1.6, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.45)

        # ---------------------------------------------------------- 25 domande
        self.new(tr("Check your understanding", "Verifica"), tr("Three questions", "Tre domande"))
        g = rows_mob([tr("Why must bad channels be removed ++before++ computing the average reference?", "Perché i canali cattivi vanno tolti ++prima++ di calcolare il riferimento medio?"),
                      tr("64 channels, average reference, 2 interpolated channels: how many ICs should you estimate?", "64 canali, riferimento medio, 2 canali interpolati: quante IC dovresti stimare?"),
                      tr("An ERP difference starts 20 ms ++before++ the stimulus. What could explain it?", "Una differenza ERP inizia 20 ms ++prima++ dello stimolo. Che cosa potrebbe spiegarla?")], 21, n=84, h=1.05, gap=0.35, col=ACC).shift(DOWN * 0.3)
        for r_ in g: self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.7)

        # ---------------------------------------------------------- 26 messaggi chiave
        self.new(tr("Take-home messages", "Messaggi chiave"), tr("Take-home messages", "Messaggi chiave"))
        g = rows_mob([tr("A pipeline is a sequence of ++choices++: justify, report, share.", "Una pipeline è una sequenza di ++scelte++: motivarle, riportarle, condividerle."),
                      tr("Filter the ++continuous++ data; know the ++delay/acausality++ of your filters.", "Filtrare i dati ++continui++; conoscere ++ritardo/acausalità++ dei filtri."),
                      tr("Bad channels out ++before++ average reference; interpolation ++reduces rank++.", "Canali cattivi fuori ++prima++ del riferimento medio; l'interpolazione ++riduce il rango++."),
                      tr("ICA = ++linear unmixing++ of independent, non-Gaussian sources.", "ICA = ++separazione lineare++ di sorgenti indipendenti e non gaussiane."),
                      tr("Remove only ++clear++ artifact ICs; ICLabel helps, your eyes decide.", "Rimuovere solo IC artefattuali ++chiare++; ICLabel aiuta, i tuoi occhi decidono.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 27 letture
        self.new(tr("Suggested reading", "Letture consigliate"), tr("Suggested reading", "Letture consigliate"))
        refs_slide(self, ["Widmann, Schröger & Maess (2015) *J Neurosci Methods* 250:34–46.", "Bigdely-Shamlo et al. (2015) *Front Neuroinform* 9:16.",
                          "Perrin et al. (1989) *Electroencephalogr Clin Neurophysiol* 72:184–187.", "Bell & Sejnowski (1995) *Neural Comput* 7:1129–1159.",
                          "Jung et al. (2000) *Psychophysiology* 37:163–178.", "Hyvärinen & Oja (2000) *Neural Netw* 13:411–430.",
                          "Delorme et al. (2012) *PLoS One* 7:e30135.", "Chaumon, Bishop & Busch (2015) *J Neurosci Methods* 250:47–63.",
                          "Pion-Tonachini et al. (2019) *NeuroImage* 198:181–197.", "Mullen et al. (2015) *IEEE Trans Biomed Eng* 62:2553–2567.",
                          "Delorme (2023) *Sci Rep* 13:2372.", "Pernet et al. (2020) *Nat Neurosci* 23:1473–1483."], 17)
        self.end()
