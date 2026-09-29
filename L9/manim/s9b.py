from base import *
import figs9 as F9
from s9a import LF, NS, NE, dec, gsrc, scene_head


def cards_row(items, w, h, y, size=16, n=30, head=20):
    cs = VGroup()
    for k, (h_, d_) in enumerate(items):
        box = RoundedRectangle(corner_radius=0.14, width=w, height=h, fill_color=CARD if k % 2 == 0 else CARD2, fill_opacity=1, stroke_width=0)
        tx = VGroup(TX(h_, font=BODY, font_size=head, color=TEAL, weight=BOLD), T(d_, size, n=n)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        tx.move_to(box).align_to(box, UP).shift(DOWN * 0.25)
        cs.add(VGroup(box, tx))
    return cs.arrange(RIGHT, buff=0.2).move_to(np.array([0, y, 0]))


class B9_Connettivita(Base):
    start_num = 12

    def construct(self):
        # ---------------------------------------------------------- 12 sezione
        self.new(first=True); section_title(self, 3, tr("Functional connectivity", "Connettività funzionale"))

        # ---------------------------------------------------------- 13 tipi
        self.new(tr("Connectivity (1)", "Connettività (1)"), tr("Structural, functional, effective", "Strutturale, funzionale, effettiva"))
        cs = cards_row([(tr("Structural", "Strutturale"), tr("anatomical links (white-matter tracts, DTI).", "connessioni anatomiche (fasci di sostanza bianca, DTI).")),
                        (tr("Functional", "Funzionale"), tr("++statistical dependence++: correlation, coherence, phase locking; no direction.", "++dipendenza statistica++: correlazione, coerenza, aggancio di fase; senza direzione.")),
                        (tr("Effective", "Effettiva"), tr("++directed++ influence: Granger, PDC/DTF, DCM (Friston, 2011).", "influenza ++diretta++: Granger, PDC/DTF, DCM (Friston, 2011)."))], 4.0, 2.3, 1.1, 16, 34)
        for c_ in cs: self.play(FadeIn(c_, shift=UP * 0.15), run_time=0.4)
        g = rows_mob([tr("*Amplitude*: envelope correlation (orthogonalised; Hipp et al., 2012).", "*Ampiezza*: correlazione degli inviluppi (ortogonalizzati; Hipp et al., 2012)."),
                      tr("*Phase*: coherence, PLV, imaginary coherence, PLI/wPLI.", "*Fase*: coerenza, PLV, coerenza immaginaria, PLI/wPLI."),
                      tr("*Directed*: Granger, PDC, DTF (autoregressive models).", "*Dirette*: Granger, PDC, DTF (modelli autoregressivi).")], 18, n=100, h=0.62, gap=0.12, col=ACC).move_to(np.array([0, -1.75, 0]))
        self.play(LaggedStart(*[FadeIn(r_) for r_ in g], lag_ratio=0.2), run_time=1.2)

        # ---------------------------------------------------------- 14 conduzione di volume
        self.new(tr("Connectivity (2)", "Connettività (2)"), tr("The volume-conduction trap", "La trappola della conduzione di volume"))
        c = np.array([-3.9, -0.5, 0]); R = 2.3
        D = 2.0; fs = 250; t = np.arange(0, D, 1 / fs)
        s = E.periodic_eeg(D, fs, seed=5, peaks=((6, 0.8, 2.0),), uv=20)[1]; s = s / np.abs(s).max()
        e1, e2 = 12, 19
        Ep = F9.el_pos() * R + c[:2]
        pT = ValueTracker(0.0)

        def vc():
            k = int(round(pT.get_value() * D * fs)) % len(t)
            amp = s[k]
            j = gsrc(60, 2.5, amp)
            g = VGroup(scene_head(c, R, j * 0 + gsrc(60, 2.5), LF @ j if abs(amp) > 1e-3 else LF @ gsrc(60, 2.5) * 1e-3))
            for e_, col in ((e1, TEAL), (e2, AMB)):
                g.add(Circle(radius=0.17, color=col, stroke_width=4).move_to(np.array([*Ep[e_], 0])))
            x1 = s * LF[e1, 60]; x2 = s * LF[e2, 60]; m = np.abs(LF[:, 60]).max()
            g.add(E.window_trace(t, x1 / m, pT.get_value() * D, 1.0, np.array([0.3, 1.2, 0]), 5.6, 0.9, TEAL, 2.5))
            g.add(E.window_trace(t, x2 / m, pT.get_value() * D, 1.0, np.array([0.3, -0.3, 0]), 5.6, 0.9, AMB, 2.5))
            return g
        vz = always_redraw(vc)
        self.play(FadeIn(vz))
        cap = T(tr("One source → many electrodes at the ++same instant++: spurious ++zero-lag++ coupling (also from the ++reference++).", "Una sorgente → molti elettrodi nello ++stesso istante++: accoppiamento spurio a ++ritardo zero++ (anche dal ++riferimento++)."), 17, n=110).move_to(np.array([0.5, -2.15, 0]))
        cap2 = T(tr("Remedies: ++source level++ + ++lag-based++ metrics or orthogonalisation (Nolte et al., 2004; Palva et al., 2018).", "Rimedi: livello delle ++sorgenti++ + metriche ++basate sul ritardo++ o ortogonalizzazione (Nolte et al., 2004; Palva et al., 2018)."), 16, n=120, col=TEAL).move_to(np.array([0.3, -2.95, 0]))
        self.play(FadeIn(cap), FadeIn(cap2))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: pT.set_value(ph.get_value()))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); vz.clear_updaters()

        # ---------------------------------------------------------- 15 fase: il ritardo cambia, PLV vs wPLI
        self.new(tr("Connectivity (3)", "Connettività (3)"), tr("Coherence, PLV and lag-based measures", "Coerenza, PLV e misure basate sul ritardo"))
        rng = np.random.default_rng(7)
        base = rng.normal(0, 0.35, 400)
        lagT = ValueTracker(0.0); rotT = ValueTracker(0.0)
        cc = np.array([-3.4, -0.2, 0]); R = 2.1
        Ob = np.array([1.3, -1.6, 0])

        def ph_():
            lag = lagT.get_value(); rot = rotT.get_value()
            d = base + lag
            g = VGroup(Circle(radius=R, color=MUT, stroke_width=1.5).move_to(cc), Line(cc + np.array([-R, 0, 0]), cc + np.array([R, 0, 0]), color=MUT, stroke_width=1),
                       Line(cc + np.array([0, -R, 0]), cc + np.array([0, R, 0]), color=MUT, stroke_width=1))
            g.add(*[Line(cc, cc + R * np.array([np.cos(a), np.sin(a), 0]), color=TEAL, stroke_width=1.3, stroke_opacity=0.55) for a in d[:70]])
            z = np.exp(1j * d); plv = abs(z.mean()); wpli = abs(np.mean(np.sin(d))) / np.mean(np.abs(np.sin(d)))
            g.add(Arrow(cc, cc + R * np.array([z.mean().real, z.mean().imag, 0]), buff=0, color=ACC, stroke_width=6, tip_length=0.2, max_tip_length_to_length_ratio=0.3))
            for i, (nm, v, col) in enumerate((("PLV", plv, ACC), ("wPLI", wpli, TEAL))):
                g.add(Rectangle(width=0.9, height=max(v * 2.4, 0.01), stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(Ob + np.array([0.8 + 1.6 * i, 0, 0]), aligned_edge=DOWN))
                g.add(T(f"{nm} = **{dec(v)}**", 17, col).move_to(Ob + np.array([0.8 + 1.6 * i, -0.3, 0])))
            g.add(T(tr(f"mean phase lag = **{int(np.degrees(lag))}°**", f"ritardo di fase medio = **{int(np.degrees(lag))}°**"), 20, AMB).move_to(cc + np.array([0, R + 0.35, 0])))
            return g
        pz = always_redraw(ph_)
        axb = Line(Ob, Ob + np.array([3.3, 0, 0]), color=FG, stroke_width=1.5)
        self.play(FadeIn(pz), FadeIn(axb))
        fm = fcard(r"\mathrm{wPLI}=\frac{|\langle \mathrm{Im}\,S_{xy}\rangle|}{\langle|\mathrm{Im}\,S_{xy}|\rangle}", CARD2, 0.65).move_to(np.array([5.0, 1.4, 0]))
        cap = VGroup(T(tr("*PLV/coherence*: high ++also at zero lag++.", "*PLV/coerenza*: alti ++anche a ritardo zero++."), 16, n=34),
                     T(tr("*Imag. coherence, PLI, wPLI*: only ++non-zero lag++ (Nolte 2004; Vinck 2011).", "*Coer. immaginaria, PLI, wPLI*: solo ritardo ++non nullo++ (Nolte 2004; Vinck 2011)."), 16, n=34)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(np.array([4.6, -0.3, 0]))
        self.play(FadeIn(fm), FadeIn(cap))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: lagT.set_value(PI / 2 * (0.5 - 0.5 * np.cos(2 * np.pi * ph.get_value()))))
        self.add(drv); loop_play(self, ph, 10.0); drv.clear_updaters(); pz.clear_updaters()

        # ---------------------------------------------------------- 16 Granger: tracce che scorrono
        self.new(tr("Connectivity (4)", "Connettività (4)"), tr("Directed connectivity: Granger causality", "Connettività diretta: causalità di Granger"))
        x, y = F9.granger_sim(2000)
        n0 = 1000; xs = x[n0:n0 + 400]; ys = y[n0:n0 + 400]
        tg = np.arange(400) / 100.0
        f = F9.f18_granger(6.0)
        bars = VGroup(f["b1"], f["b2"], f["ax"], f["t1"], f["t2"], f["v1"], f["v2"], f["tt"]).shift(RIGHT * 0.6 + UP * 0.2)
        Ox = np.array([-6.0, 1.3, 0]); Oy = np.array([-6.0, -0.4, 0]); W_ = 6.4
        tr0 = VGroup(E.window_trace(tg, xs, 0, 1.2, Ox, W_, 0.2, TEAL, 2), E.window_trace(tg, ys, 0, 1.2, Oy, W_, 0.2, ACC, 2))
        lab = VGroup(T("X", 20, TEAL).move_to(Ox + np.array([-0.35, 0, 0])), T("Y", 20, ACC).move_to(Oy + np.array([-0.35, 0, 0])),
                     CurvedArrow(Ox + np.array([W_ + 0.3, -0.2, 0]), Oy + np.array([W_ + 0.3, 0.2, 0]), color=ACC, angle=-PI / 3, stroke_width=4))
        self.play(FadeIn(lab), Create(tr0), FadeIn(bars))
        bl = bullets([tr("X \"Granger-causes\" Y if the ++past of X++ improves the prediction of Y (Granger, 1969).", "X \"Granger-causa\" Y se il ++passato di X++ migliora la predizione di Y (Granger, 1969)."),
                      tr("Autoregressive models; spectral versions ++PDC, DTF++.", "Modelli autoregressivi; versioni spettrali ++PDC, DTF++."),
                      tr("⚠ Prediction ≠ causation: common inputs, filtering, volume conduction (Seth et al., 2015).", "⚠ Predizione ≠ causa: ingressi comuni, filtraggio, conduzione di volume (Seth et al., 2015).")], 16, n=100, gap=0.18).move_to(np.array([0, -2.4, 0]))
        self.play(FadeIn(bl))
        loop_start(self)
        ph = ValueTracker(0.0)
        live = always_redraw(lambda: VGroup(E.window_trace(tg, xs, ph.get_value() * 4.0, 1.2, Ox, W_, 0.2, TEAL, 2), E.window_trace(tg, ys, ph.get_value() * 4.0, 1.2, Oy, W_, 0.2, ACC, 2)))
        self.remove(tr0); self.add(live); loop_play(self, ph, 10.0); live.clear_updaters()

        # ---------------------------------------------------------- 17 grafo: la soglia cambia la densità
        self.new(tr("Networks", "Reti"), tr("The brain as a graph", "Il cervello come grafo"))
        hc = np.array([-3.4, -0.5, 0]); Rh = 2.3
        names = E.NAMES; pos = [hc + E.el2d(n_, Rh) for n_ in names]
        rng = np.random.default_rng(3)
        Nn = len(names)
        Wt = np.zeros((Nn, Nn))
        for i in range(Nn):
            for j in range(i + 1, Nn):
                d = np.linalg.norm(pos[i] - pos[j])
                Wt[i, j] = Wt[j, i] = np.clip(np.exp(-d / 1.4) + rng.normal(0, 0.12), 0, 1)
        vals = np.sort(Wt[np.triu_indices(Nn, 1)])[::-1]
        thT = ValueTracker(0.2)

        def graph():
            dens = thT.get_value()
            k = max(int(dens * len(vals)), 1); th = vals[k - 1]
            A = (Wt >= th).astype(float); np.fill_diagonal(A, 0)
            deg = A.sum(0)
            g = VGroup(E.head(hc, Rh))
            for i in range(Nn):
                for j in range(i + 1, Nn):
                    if A[i, j]: g.add(Line(pos[i], pos[j], color=TEAL, stroke_width=1.5 + 2 * Wt[i, j], stroke_opacity=0.7))
            g.add(*[Dot(pos[i], radius=0.07 + 0.02 * deg[i], color=ACC) for i in range(Nn)])
            # clustering medio
            C = []
            for i in range(Nn):
                nb = np.where(A[i])[0]
                if len(nb) > 1:
                    sub = A[np.ix_(nb, nb)]; C.append(sub.sum() / (len(nb) * (len(nb) - 1)))
            g.add(T(tr(f"density **{int(100 * dens)} %** · mean clustering **{dec(np.mean(C) if C else 0)}**", f"densità **{int(100 * dens)} %** · clustering medio **{dec(np.mean(C) if C else 0)}**"), 18, AMB).move_to(hc + np.array([0, Rh + 0.45, 0])))
            return g
        gz = always_redraw(graph)
        self.play(FadeIn(gz))
        items = [(tr("degree", "grado"), tr("links per node (hubs)", "connessioni per nodo (hub)")), (tr("clustering", "clustering"), tr("neighbours linked to each other", "vicini collegati tra loro")),
                 (tr("path length", "lunghezza dei cammini"), tr("steps between nodes", "passi tra i nodi")), ("small-world", tr("high clustering + short paths", "alto clustering + cammini brevi"))]
        il = VGroup(*[VGroup(T(f"~{a}~", 18), T(b, 15, MUT)).arrange(DOWN, aligned_edge=LEFT, buff=0.08) for a, b in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(np.array([3.6, 0.3, 0]))
        cap = T(tr("⚠ Metrics depend on ++density/threshold++: compare with ++null models++ (Bullmore & Sporns, 2009; Rubinov & Sporns, 2010).", "⚠ Le metriche dipendono da ++densità/soglia++: confrontare con ++modelli nulli++ (Bullmore & Sporns, 2009; Rubinov & Sporns, 2010)."), 15, n=60).move_to(np.array([3.6, -2.4, 0]))
        self.play(FadeIn(il), FadeIn(cap))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: thT.set_value(0.25 - 0.17 * np.cos(2 * np.pi * ph.get_value())))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); gz.clear_updaters()

        # ---------------------------------------------------------- 18 sezione
        self.new(); section_title(self, 4, tr("In practice", "In pratica"))

        # ---------------------------------------------------------- 19 MATLAB
        self.new(tr("In MATLAB", "In MATLAB"), tr("Source imaging and wPLI with FieldTrip", "Sorgenti e wPLI con FieldTrip"))
        code = ["load standard_bem;  elec = ft_read_sens('standard_1020.elc');           % template head",
                "cfg = []; cfg.headmodel = vol; cfg.elec = elec;",
                "cfg.sourcemodel = ft_read_headshape('cortex_5124.surf.gii');",
                "lf = ft_prepare_leadfield(cfg, data);                                    % forward",
                "cfg = []; cfg.covariance = 'yes'; cfg.keeptrials = 'yes';",
                "tl  = ft_timelockanalysis(cfg, data);",
                "cfg = []; cfg.method = 'eloreta'; cfg.sourcemodel = lf; cfg.headmodel = vol;",
                "cfg.eloreta.keepfilter = 'yes'; cfg.eloreta.lambda = 0.05;",
                "src = ft_sourceanalysis(cfg, tl);                                        % inverse",
                "cfg = []; cfg.method = 'mtmfft'; cfg.taper = 'dpss'; cfg.tapsmofrq = 2;",
                "cfg.foi = 8:1:13; cfg.output = 'fourier'; cfg.keeptrials = 'yes';",
                "freq = ft_freqanalysis(cfg, data);",
                "cfg = []; cfg.method = 'wpli_debiased';",
                "conn = ft_connectivityanalysis(cfg, freq);                               % lag-based",
                "W = squeeze(mean(conn.wpli_debiasedspctrm, 3));",
                "C = clustering_coef_wu(abs(W));                                          % BCT"]
        cl = code_lines(code, 15)
        if cl.width > 12.6: cl.scale_to_fit_width(12.6)
        cc_ = card(cl, CARD, pad=0.25).move_to(np.array([0, -0.45, 0]))
        self.play(FadeIn(cc_[0]))
        self.play(LaggedStart(*[FadeIn(x_, shift=RIGHT * 0.1) for x_ in cl], lag_ratio=0.12), run_time=3.0)

        # ---------------------------------------------------------- 20 checklist
        self.new(tr("Good practice", "Buona pratica"), tr("A checklist for sources and connectivity", "Una checklist per sorgenti e connettività"))
        g = rows_mob([tr("≥ 64 channels, ++full coverage++, digitised positions, good head model.", "≥ 64 canali, ++copertura completa++, posizioni digitalizzate, buon modello di testa."),
                      tr("Report inverse method, ++regularisation++, source space, noise covariance.", "Riportare metodo inverso, ++regolarizzazione++, spazio sorgenti, covarianza del rumore."),
                      tr("Connectivity at ++source level++ with ++lag-based++ or orthogonalised metrics.", "Connettività alle ++sorgenti++ con metriche ++basate sul ritardo++ o ortogonalizzate."),
                      tr("Equalise ++trials++ and ++SNR++ between conditions.", "Pareggiare ++trial++ e ++SNR++ tra condizioni."),
                      tr("Test against ++surrogates/permutations++; \"where\" at ++cm++ scale.", "Testare contro ++surrogati/permutazioni++; il \"dove\" alla scala dei ++cm++.")], 20).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.2), run_time=2.0)

        # ---------------------------------------------------------- 21 domande
        self.new(tr("Check your understanding", "Verifica"), tr("Three questions", "Tre domande"))
        g = rows_mob([tr("Why can two very different source configurations produce the same scalp map?", "Perché due configurazioni di sorgenti molto diverse possono dare la stessa mappa?"),
                      tr("Fz–FCz alpha coherence = 0.9: evidence of communication? What would you compute?", "Coerenza alfa Fz–FCz = 0,9: prova di comunicazione? Che cosa calcoleresti?"),
                      tr("Two synchronous bilateral auditory sources: why might a beamformer miss them?", "Due sorgenti uditive bilaterali sincrone: perché un beamformer potrebbe non vederle?")], 21, n=84, h=1.05, gap=0.35, col=ACC).shift(DOWN * 0.3)
        for r_ in g: self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.7)

        # ---------------------------------------------------------- 22 messaggi chiave
        self.new(tr("Take-home messages", "Messaggi chiave"), tr("Take-home messages", "Messaggi chiave"))
        g = rows_mob([tr("Forward ++unique++ (y = L·j); inverse ++ill-posed++, needs priors.", "Diretto ++unico++ (y = L·j); inverso ++mal posto++, servono ipotesi."),
                      tr("Dipoles for ++focal++ sources; MNE/sLORETA for distributed; beamformers for ++uncorrelated++ ones.", "Dipoli per sorgenti ++focali++; MNE/sLORETA per distribuite; beamformer per sorgenti ++non correlate++."),
                      tr("Accuracy needs ++electrodes, coverage, head model++.", "L'accuratezza richiede ++elettrodi, copertura, modello di testa++."),
                      tr("Sensor coherence is ++contaminated by volume conduction++: lag-based, source level.", "La coerenza ai sensori è ++contaminata dalla conduzione di volume++: metriche col ritardo, alle sorgenti."),
                      tr("Granger = ++prediction++; graphs summarise ++network organisation++.", "Granger = ++predizione++; i grafi riassumono l'++organizzazione di rete++.")], 20).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 23 letture
        self.new(tr("Suggested reading", "Letture consigliate"), tr("Suggested reading", "Letture consigliate"))
        refs_slide(self, ["Michel et al. (2004) *Clin Neurophysiol* 115:2195–2222.", "Michel & Brunet (2019) *Front Neurol* 10:325.",
                          "Hämäläinen & Ilmoniemi (1994) *Med Biol Eng Comput* 32:35–42.", "Pascual-Marqui (2002) *Methods Find Exp Clin Pharmacol* 24D:5–12.",
                          "Van Veen et al. (1997) *IEEE Trans Biomed Eng* 44:867–880.", "Vorwerk et al. (2014) *NeuroImage* 100:590–607.",
                          "Nolte et al. (2004) *Clin Neurophysiol* 115:2292–2307.", "Vinck et al. (2011) *NeuroImage* 55:1548–1565.",
                          "Bastos & Schoffelen (2016) *Front Syst Neurosci* 9:175.", "Seth, Barrett & Barnett (2015) *J Neurosci* 35:3293–3297.",
                          "Bullmore & Sporns (2009) *Nat Rev Neurosci* 10:186–198.", "Oostenveld et al. (2011) *Comput Intell Neurosci* 2011:156869."], 17)
        self.end()
