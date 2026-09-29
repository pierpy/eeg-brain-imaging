from base import *
import figs8 as F8
from s8a import MSC, TM, MASK, tmap, morph, dec


def cards_row(items, w, h, y, size=16, n=30, head=20):
    cs = VGroup()
    for k, (h_, d_) in enumerate(items):
        box = RoundedRectangle(corner_radius=0.14, width=w, height=h, fill_color=CARD if k % 2 == 0 else CARD2, fill_opacity=1, stroke_width=0)
        tx = VGroup(TX(h_, font=BODY, font_size=head, color=TEAL, weight=BOLD), T(d_, size, n=n)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        tx.move_to(box).align_to(box, UP).shift(DOWN * 0.25)
        cs.add(VGroup(box, tx))
    return cs.arrange(RIGHT, buff=0.2).move_to(np.array([0, y, 0]))


class B8_Microstati(Base):
    start_num = 8

    def construct(self):
        fs = F8.FS8
        # ---------------------------------------------------------- 8 sezione
        self.new(first=True); section_title(self, 2, tr("Microstate analysis", "Analisi dei microstati"))

        # ---------------------------------------------------------- 9 pipeline
        self.new(tr("Microstates (2)", "Microstati (2)"), tr("The analysis pipeline", "La pipeline di analisi"))
        f = F8.f09_pipeline(13.0)
        for m in f.values(): m.shift(UP * 1.3)
        for k in range(6):
            an = [FadeIn(f[f"b{k}"], shift=UP * 0.1)]
            if k < 5: an.append(GrowArrow(f[f"a{k}"]))
            self.play(*an, run_time=0.35)
        g = rows_mob([tr("Band-pass ++1–40 Hz++, artifact removal, ++average reference++.", "Passa-banda ++1–40 Hz++, rimozione artefatti, ++riferimento medio++."),
                      tr("Maps at ++GFP peaks++ (highest SNR).", "Mappe ai ++picchi di GFP++ (SNR massimo)."),
                      tr("Cluster ++per subject++, then the individual templates at ++group level++.", "Clustering ++per soggetto++, poi dei template individuali a ++livello di gruppo++."),
                      tr("++Back-fit++ group templates to every sample; compute ++metrics++.", "++Back-fitting++ dei template di gruppo su ogni campione; calcolare le ++metriche++.")], 18, n=90, h=0.62, gap=0.12, col=ACC).move_to(np.array([0, -1.35, 0]))
        self.play(LaggedStart(*[FadeIn(r_) for r_ in g], lag_ratio=0.2), run_time=1.5)
        boxes = [f[f"b{k}"][0] for k in range(6)]
        loop_start(self)
        ph = ValueTracker(0.0)
        hl = always_redraw(lambda: SurroundingRectangle(boxes[min(int(ph.get_value() * 6), 5)], color=AMB, stroke_width=6, buff=0.08, corner_radius=0.18))
        self.add(hl); loop_play(self, ph, 6.0); hl.clear_updaters()

        # ---------------------------------------------------------- 10 k-means modificato: iterazioni sui dati 2D
        self.new(tr("Clustering (1)", "Clustering (1)"), tr("k-means and modified k-means", "k-means e k-means modificato"))
        rng = np.random.default_rng(4)
        dirs = [np.array([np.cos(a), np.sin(a)]) for a in (0.5, 2.2)]
        P_ = np.array([s * d * rng.uniform(0.4, 1.0) + rng.normal(0, 0.08, 2) for d in dirs for s in (1, -1) for _ in range(40)])
        Pn = P_ / np.linalg.norm(P_, axis=1, keepdims=True)
        c0 = np.array([-3.3, -0.3, 0]); R = 2.1
        # iterazioni del k-means modificato
        T_ = np.array([[np.cos(1.3), np.sin(1.3)], [np.cos(1.5), np.sin(1.5)]]); hist = [T_.copy()]
        for it in range(8):
            lab = np.abs(Pn @ T_.T).argmax(1)
            for k in range(2):
                M = P_[lab == k]
                w, v = np.linalg.eigh(M.T @ M); T_[k] = v[:, -1]
            hist.append(T_.copy())
        itT = ValueTracker(0)

        def km():
            i = int(itT.get_value()); Tk = hist[i]
            lab = np.abs(Pn @ Tk.T).argmax(1)
            g = VGroup(*[Dot(c0 + np.array([p[0] * R, p[1] * R, 0]), radius=0.045, color=MSC[l]) for p, l in zip(P_, lab)])
            for k in range(2):
                g.add(DashedLine(c0 - np.array([*Tk[k], 0]) * R * 1.1, c0 + np.array([*Tk[k], 0]) * R * 1.1, color=MSC[k], stroke_width=3))
            gev = np.mean(np.max(np.abs(Pn @ Tk.T), 1) ** 2)
            g.add(T(tr(f"iteration **{i}** · mean corr² = **{dec(gev, 2)}**", f"iterazione **{i}** · corr² media = **{dec(gev, 2)}**"), 18, AMB).move_to(c0 + np.array([0, R + 0.35, 0])))
            return g
        ax = VGroup(Line(c0 + np.array([-R, 0, 0]), c0 + np.array([R, 0, 0]), color=MUT, stroke_width=1.2), Line(c0 + np.array([0, -R, 0]), c0 + np.array([0, R, 0]), color=MUT, stroke_width=1.2),
                    T("ch1", 14, MUT).move_to(c0 + np.array([R + 0.3, 0, 0])), T("ch2", 14, MUT).move_to(c0 + np.array([0.35, -R, 0])))
        kz = always_redraw(km)
        self.play(FadeIn(ax), FadeIn(kz))
        bl = bullets([tr("Each map = a ++point in N-dim space++.", "Ogni mappa = un ++punto nello spazio a N dimensioni++."),
                      tr("Assign maps by ++|spatial correlation|++: opposite polarities = same state.", "Assegnare le mappe per ++|correlazione spaziale|++: polarità opposte = stesso stato."),
                      tr("Update each template = ++1st principal component++ of its maps (Pascual-Marqui et al., 1995).", "Aggiornare ogni template = ++1ª componente principale++ delle sue mappe (Pascual-Marqui et al., 1995)."),
                      tr("Repeat from many random starts; keep the best ++GEV++.", "Ripetere da molte partenze casuali; tenere la ++GEV++ migliore.")], 16, n=36, gap=0.26).move_to(np.array([3.8, -0.3, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.35)
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: itT.set_value(min(int(ph.get_value() * 10), 8)))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); kz.clear_updaters()

        # ---------------------------------------------------------- 11 AAHC / TAAHC
        self.new(tr("Clustering (2)", "Clustering (2)"), tr("Hierarchical alternatives: AAHC and TAAHC", "Alternative gerarchiche: AAHC e TAAHC"))
        cs = cards_row([("AAHC", tr("start with every map as a cluster; repeatedly ++dissolve the worst++ and redistribute its maps (Murray et al., 2008).", "si parte con ogni mappa come cluster; si ++scioglie il peggiore++ e se ne ridistribuiscono le mappe (Murray et al., 2008).")),
                        ("TAAHC", tr("*topographic* AAHC: worst = ++lowest summed correlation++ with its members (Khanna et al., 2014).", "AAHC *topografico*: peggiore = ++minore correlazione sommata++ con i membri (Khanna et al., 2014).")),
                        (tr("Pros & cons", "Pro e contro"), tr("++deterministic++, all k at once; slower. k-means: fast, depends on initialisation.", "++deterministico++, tutti i k insieme; più lento. k-means: veloce, dipende dall'inizializzazione."))], 4.0, 2.4, 1.2, 16, 34)
        for c_ in cs: self.play(FadeIn(c_, shift=UP * 0.15), run_time=0.4)
        # dendrogramma animato: 8 cluster che si fondono
        base = np.array([-3.5, -2.6, 0]); dx = 1.0
        xs = [base[0] + dx * i for i in range(8)]
        cols = [MSC[i % 4] for i in range(8)]
        nT = ValueTracker(8)
        merges = [(0, 4), (1, 5), (2, 6), (3, 7)]

        def dend():
            nk = int(round(nT.get_value()))
            g = VGroup()
            for i in range(8):
                g.add(Dot(np.array([xs[i], base[1], 0]), radius=0.12, color=cols[i]))
            done = 8 - nk
            for j, (a, b) in enumerate(merges[:done]):
                y = base[1] + 0.4 + 0.15 * j
                g.add(VMobject(color=MSC[a], stroke_width=3).set_points_as_corners([np.array([xs[a], base[1] + 0.12, 0]), np.array([xs[a], y, 0]), np.array([xs[b], y, 0]), np.array([xs[b], base[1] + 0.12, 0])]))
            g.add(T(f"k = **{nk}**", 20, AMB).move_to(np.array([4.9, base[1] + 0.3, 0])))
            return g
        dz = always_redraw(dend)
        self.play(FadeIn(dz))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: nT.set_value(8 - min(int(ph.get_value() * 5), 4)))
        self.add(drv); loop_play(self, ph, 6.0); drv.clear_updaters(); dz.clear_updaters()

        # ---------------------------------------------------------- 12 scelta di k: cursore sui criteri
        self.new(tr("Clustering (3)", "Clustering (3)"), tr("How many microstates? Criteria of fit", "Quanti microstati? Criteri di adattamento"))
        f = F8.f12_criteria(3.4, 2.1); fit(f, 1.0, np.array([0, 0.5, 0]))
        self.play(*[FadeIn(m) for m in f.values()], run_time=1.2)
        kT = ValueTracker(2.0)
        ax0 = [f[f"ax{j}"][0] for j in range(3)]

        def cur():
            k = kT.get_value(); g = VGroup()
            for a in ax0:
                x = a.get_start()[0] + (k - 2) / 8 * 3.4
                g.add(Line(np.array([x, a.get_start()[1], 0]), np.array([x, a.get_start()[1] + 2.2, 0]), color=AMB, stroke_width=2.5))
            g.add(T(f"k = **{int(round(k))}**", 22, AMB).move_to(np.array([0, -1.55, 0])))
            return g
        cz = always_redraw(cur)
        self.add(cz)
        bl = bullets([tr("*GEV* always grows: look for the ++elbow++; *CV* ++minimum++; *KL* ++maximum++.", "La *GEV* cresce sempre: cercare il ++gomito++; *CV* ++minimo++; *KL* ++massimo++."),
                      tr("Resting EEG: ++4 maps ≈ 70–80 %++ of variance; high density may support ++5–7++ (Custo et al., 2017).", "EEG a riposo: ++4 mappe ≈ 70–80 %++ della varianza; l'alta densità ne può supportare ++5–7++ (Custo et al., 2017).")], 17, n=100, gap=0.22).move_to(np.array([0, -2.5, 0]))
        self.play(FadeIn(bl))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: kT.set_value(6 - 4 * np.cos(2 * np.pi * ph.get_value())))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); cz.clear_updaters()

        # ---------------------------------------------------------- 13 template
        self.new(tr("Templates", "Template"), tr("The four canonical microstate classes", "Le quattro classi canoniche di microstati"))
        maps = Group()
        desc = [tr("left-right", "sinistra-destra"), tr("right-left", "destra-sinistra"), tr("anterior-posterior", "antero-posteriore"), tr("fronto-central", "fronto-centrale")]
        for k in range(4):
            c = np.array([-4.5 + 3.0 * k, 0.6, 0])
            maps.add(Group(tmap(TM[k], c, 1.1), Text("ABCD"[k], font=BODY, font_size=30, color=MSC[k], weight=BOLD).move_to(c + np.array([0, 1.5, 0])), T(desc[k], 15, MUT).move_to(c + np.array([0, -1.4, 0]))))
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in maps], lag_ratio=0.25), run_time=2.0)
        bl = bullets([tr("Classes *A–D* are ++highly reproducible++ across labs, montages and ages (Koenig et al., 2002).", "Le classi *A–D* sono ++molto riproducibili++ tra laboratori, montaggi ed età (Koenig et al., 2002)."),
                      tr("Our data: 62 ch → GEV ≈ 78 % (Zappasodi et al., 2019); 128 ch → GEV ≈ 83 %.", "Nostri dati: 62 canali → GEV ≈ 78 % (Zappasodi et al., 2019); 128 canali → GEV ≈ 83 %.")], 17, n=100, gap=0.22).move_to(np.array([0, -2.45, 0]))
        self.play(FadeIn(bl))

        # ---------------------------------------------------------- 14 back-fitting: correlazioni istante per istante
        self.new(tr("Back-fitting", "Back-fitting"), tr("Labelling every time point", "Etichettare ogni istante"))
        t, X, lab0 = F8.simulate(4.0, seed=33, snr=15)
        Tv = F8.template_vec()
        lab, _ = F8.backfit(X, Tv)
        Xn = X / (np.linalg.norm(X, axis=0) + 1e-12); C = np.abs(Tv @ Xn)
        g_ = F8.gfp(X); n = len(t)
        Wb = 12.0; Og = np.array([-6.0, -1.9, 0]); win = 1.0
        cm = np.array([-3.5, 1.1, 0]); Rm = 1.0
        pT = ValueTracker(0.0)

        def bf():
            s0 = pT.get_value() * 4.0
            k0 = int(round(s0 * fs)); nw = int(win * fs); idx = (k0 + np.arange(nw)) % n
            gr = VGroup(); i = 0
            while i < nw:
                j = i
                while j < nw and lab[idx[j]] == lab[idx[i]]: j += 1
                xa = Og[0] + i / nw * Wb; xb = Og[0] + j / nw * Wb
                gr.add(Rectangle(width=max(xb - xa, 0.01), height=1.0, stroke_width=0, fill_color=MSC[lab[idx[i]]], fill_opacity=0.5).move_to(np.array([(xa + xb) / 2, Og[1] + 0.5, 0])))
                i = j
            gr.add(E.window_trace(t, g_, s0, win, Og, Wb, 0.04, FG, 2.5))
            xm = Og[0] + Wb / 2
            gr.add(Line(np.array([xm, Og[1] - 0.1, 0]), np.array([xm, Og[1] + 1.1, 0]), color=AMB, stroke_width=3))
            kc = idx[nw // 2]
            for q in range(4):
                h = C[q, kc] * 1.8
                gr.add(Rectangle(width=0.5, height=max(h, 0.01), stroke_width=0, fill_color=MSC[q], fill_opacity=1.0 if q == lab[kc] else 0.35).move_to(np.array([1.0 + 0.8 * q, -0.2, 0]), aligned_edge=DOWN))
                gr.add(Text("ABCD"[q], font=BODY, font_size=18, color=MSC[q], weight=BOLD).move_to(np.array([1.0 + 0.8 * q, -0.45, 0])))
            gr.add(T(tr("|corr| with templates", "|corr| con i template"), 16, MUT).move_to(np.array([2.2, 1.95, 0])))
            return gr

        def mnow():
            k = (int(round(pT.get_value() * 4.0 * fs)) + int(win * fs / 2)) % n
            V, m = E.interp_map(X[:, k], n=81, p=2.5)
            return Group(*E.topomap(V, m, cm, Rm, vmax=np.abs(V[m]).max() * 1.05 + 1e-9))
        tm = Group(*[tmap(TM[q], np.array([4.9 + 0.0, 1.35 - 0.0, 0]) + np.array([(q % 2) * 1.0 - 0.5, -(q // 2) * 1.0, 0]), 0.42) for q in range(4)])
        bz = always_redraw(bf); mz = mnow()
        self.play(FadeIn(bz), FadeIn(mz), FadeIn(tm))
        cap = T(tr("Winner-takes-all: each sample gets the template with the ++highest |correlation|++; short segments (< 20–30 ms) are smoothed.", "Winner-takes-all: ogni campione prende il template con la ++massima |correlazione|++; i segmenti brevi (< 20–30 ms) vengono livellati."), 16, n=120).move_to(np.array([0, -3.05, 0]))
        self.play(FadeIn(cap))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: pT.set_value(ph.get_value()))
        self.remove(mz); mz = redraw(mnow)
        self.add(drv, mz); loop_play(self, ph, 24.0); drv.clear_updaters(); bz.clear_updaters(); mz.clear_updaters()

        # ---------------------------------------------------------- 15 metriche
        self.new(tr("Metrics", "Metriche"), tr("Temporal parameters of microstates", "Parametri temporali dei microstati"))
        f = F8.f16_metrics(2.2, 1.8); fit(f, 1.0, np.array([0, 0.4, 0]))
        bars = [f[k] for k in f if k.startswith("b")]
        self.play(*[FadeIn(f[k]) for k in f if not k.startswith("b") and not k.startswith("q") and not k.startswith("n")], run_time=0.8)
        self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.05), run_time=1.5)
        self.play(*[FadeIn(f[k]) for k in f if k.startswith("q") or k.startswith("n")], run_time=1.0)
        g = rows_mob([tr("*Duration* ≈ 60–120 ms · *occurrence* ≈ 3–5 /s · *coverage* % time · *GEV* per class.", "*Durata* ≈ 60–120 ms · *occorrenza* ≈ 3–5 /s · *copertura* % del tempo · *GEV* per classe."),
                      tr("*Transitions*: the ++syntax++ of the sequence — compare with chance (illustrative simulated values).", "*Transizioni*: la ++sintassi++ della sequenza — confrontare con il caso (valori simulati illustrativi).")], 17, n=110, h=0.6, gap=0.12).move_to(np.array([0, -2.6, 0]))
        self.play(FadeIn(g))

        # ---------------------------------------------------------- 16 sezione
        self.new(); section_title(self, 3, tr("What are microstates?", "Che cosa sono i microstati?"))

        # ---------------------------------------------------------- 17 fMRI: convoluzione con la HRF
        self.new(tr("Meaning (1)", "Significato (1)"), tr("Microstates and fMRI resting-state networks", "Microstati e reti fMRI a riposo"))
        rng = np.random.default_rng(5)
        D = 60.0; dt = 0.05; tt = np.arange(0, D, dt)
        occ = (rng.uniform(size=len(tt)) < (0.25 + 0.2 * np.sin(2 * np.pi * tt / 20.0))).astype(float)
        th = np.arange(0, 30, dt)
        hrf = th ** 5 * np.exp(-th) / 120 - th ** 15 * np.exp(-th) / (6 * 1.3e12)
        hrf = th ** 5 * np.exp(-th) / 120 - 0.1 * th ** 15 * np.exp(-th) / 1.3e12
        reg = np.convolve(np.tile(occ, 2), hrf)[len(tt):2 * len(tt)]; reg = (reg - reg.mean()) / reg.std()
        Wr = 7.2; x0 = -6.2; winr = 20.0
        pT = ValueTracker(0.0)

        def fm():
            s0 = pT.get_value() * D
            return VGroup(E.window_trace(tt, occ, s0, winr, np.array([x0, 0.9, 0]), Wr, 0.6, MSC[2], 1.2),
                          E.window_trace(tt, reg, s0, winr, np.array([x0, -1.2, 0]), Wr, 0.35, ACC, 3.5))
        labs = VGroup(T(tr("microstate C present (1/0), 50-ms bins", "microstato C presente (1/0), bin da 50 ms"), 15, MSC[2]).move_to(np.array([x0 + Wr / 2, 1.85, 0])),
                      T(tr("⊗ HRF → slow BOLD regressor", "⊗ HRF → regressore BOLD lento"), 15, ACC).move_to(np.array([x0 + Wr / 2, -0.15, 0])))
        fz = always_redraw(fm)
        self.play(FadeIn(labs), FadeIn(fz))
        nets = [tr("A ↔ auditory", "A ↔ uditiva"), tr("B ↔ visual", "B ↔ visiva"), tr("C ↔ salience", "C ↔ salienza"), tr("D ↔ attention", "D ↔ attenzione")]
        nl = VGroup(*[T(s_, 18, MSC[k]) for k, s_ in enumerate(nets)]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(np.array([3.4, 1.0, 0]))
        bl = bullets([tr("GLM with HRF-convolved microstate time courses (Britz et al., 2010; Musso et al., 2010).", "GLM con andamenti dei microstati convoluti con la HRF (Britz et al., 2010; Musso et al., 2010)."),
                      tr("++Scale-free++ dynamics link 100-ms states to slow networks (Van De Ville et al., 2010).", "Dinamica ++scale-free++ che collega stati da 100 ms a reti lente (Van De Ville et al., 2010)."),
                      tr("⚠ Mapping ++debated++.", "⚠ Corrispondenza ++dibattuta++.")], 15, n=40, gap=0.22).move_to(np.array([3.9, -1.6, 0]))
        self.play(FadeIn(nl)); self.play(FadeIn(bl))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: pT.set_value(ph.get_value()))
        self.add(drv); loop_play(self, ph, 20.0); drv.clear_updaters(); fz.clear_updaters()

        # ---------------------------------------------------------- 18 sorgenti
        self.new(tr("Meaning (2)", "Significato (2)"), tr("Where do microstates come from?", "Da dove vengono i microstati?"))
        g = rows_mob([tr("Each map = ++synchronous activity of a distributed network++, not one dipole.", "Ogni mappa = ++attività sincrona di una rete distribuita++, non un dipolo."),
                      tr("Sources in ++insula, cingulate, occipital, parietal, prefrontal++ cortex (Custo et al., 2017).", "Sorgenti in ++insula, cingolo, corteccia occipitale, parietale, prefrontale++ (Custo et al., 2017)."),
                      tr("With ++256 channels++: 7 classes (A–G).", "Con ++256 canali++: 7 classi (A–G)."),
                      tr("⚠ Same map ≠ same sources: the ++inverse problem++ (next lecture).", "⚠ Stessa mappa ≠ stesse sorgenti: il ++problema inverso++ (prossima lezione).")], 20).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.0)

        # ---------------------------------------------------------- 19 sezione
        self.new(); section_title(self, 4, tr("Applications", "Applicazioni"))

        # ---------------------------------------------------------- 20 condizioni: durata che cambia
        self.new(tr("Applications (1)", "Applicazioni (1)"), tr("States of mind and brain", "Stati della mente e del cervello"))
        cs = cards_row([(tr("Cognition", "Cognizione"), tr("task vs rest changes C, D (Seitzman et al., 2017); ++fluid reasoning++ components (Zappasodi et al., 2019).", "compito vs riposo cambia C, D (Seitzman et al., 2017); componenti del ++ragionamento fluido++ (Zappasodi et al., 2019).")),
                        (tr("Sleep", "Sonno"), tr("durations ++increase++ in deep sleep (Brodbeck et al., 2012).", "durate ++più lunghe++ nel sonno profondo (Brodbeck et al., 2012).")),
                        (tr("Anaesthesia", "Anestesia"), tr("propofol: ++shorter, less variable++ microstates (Li et al., 2021).", "propofol: microstati ++più brevi e meno variabili++ (Li et al., 2021).")),
                        (tr("Age", "Età"), tr("parameters change ++lawfully with age++ (Koenig et al., 2002).", "i parametri cambiano ++regolarmente con l'età++ (Koenig et al., 2002)."))], 3.0, 2.6, 1.0, 15, 28)
        for c_ in cs: self.play(FadeIn(c_, shift=UP * 0.15), run_time=0.4)
        dT = ValueTracker(0.0)
        rng = np.random.default_rng(1)
        seqL = rng.integers(0, 4, 400); durs = rng.uniform(0.6, 1.4, 400)

        def strip(u):
            sc = 1.0 + 0.8 * np.sin(2 * np.pi * u)      # durata media che respira
            g = VGroup(); x = -6.2; i = 0; base_ms = 0.18
            while x < 6.2 and i < 400:
                w = base_ms * durs[i] * sc
                g.add(Rectangle(width=min(w, 6.2 - x), height=0.45, stroke_width=0, fill_color=MSC[seqL[i]], fill_opacity=0.85).move_to(np.array([x + min(w, 6.2 - x) / 2, -1.9, 0])))
                x += w; i += 1
            g.add(T(tr(f"mean duration ≈ **{int(90 * sc)} ms**", f"durata media ≈ **{int(90 * sc)} ms**"), 18, AMB).move_to(np.array([0, -2.55, 0])))
            return g
        sz = always_redraw(lambda: strip(dT.get_value()))
        self.play(FadeIn(sz))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: dT.set_value(ph.get_value()))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); sz.clear_updaters()

        # ---------------------------------------------------------- 21 clinica
        self.new(tr("Applications (2)", "Applicazioni (2)"), tr("Psychiatry and brain stimulation", "Psichiatria e stimolazione cerebrale"))
        g = rows_mob([tr("*Schizophrenia*: shorter D, more C; a candidate ++endophenotype++ (da Cruz et al., 2020).", "*Schizofrenia*: D più breve, C più frequente; possibile ++endofenotipo++ (da Cruz et al., 2020)."),
                      tr("*Bipolar disorder*: altered dynamics linked to clinical state (Vellante et al., 2020).", "*Disturbo bipolare*: dinamica alterata legata allo stato clinico (Vellante et al., 2020)."),
                      tr("*Brain stimulation*: parietal rTMS ++selectively++ changes specific microstates (Croce et al., 2018).", "*Stimolazione*: la rTMS parietale modifica ++selettivamente++ microstati specifici (Croce et al., 2018)."),
                      tr("Also: dementia, epilepsy, neonatal EEG, disorders of consciousness.", "Inoltre: demenza, epilessia, EEG neonatale, disturbi di coscienza.")], 20).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.0)

        # ---------------------------------------------------------- 22 MATLAB
        self.new(tr("In MATLAB", "In MATLAB"), tr("Microstates with a few lines of code", "Microstati in poche righe di codice"))
        code = ["X   = EEG.data - mean(EEG.data, 1);                % average reference (ch x time)",
                "gfp = std(X, 1, 1);                                % Global Field Power",
                "[~, pk] = findpeaks(gfp);  M = X(:, pk);           % maps at GFP peaks",
                "M = M ./ vecnorm(M);  K = 4;  best = -Inf;",
                "for rep = 1:50                                     % random restarts",
                "    T = M(:, randperm(size(M,2), K));",
                "    for it = 1:100",
                "        [~, lab] = max(abs(T' * M));                % polarity-invariant assignment",
                "        for k = 1:K",
                "            [v,~] = eigs(M(:,lab==k) * M(:,lab==k)', 1);  T(:,k) = v;   % 1st PC",
                "        end",
                "    end",
                "    c = max(abs(T' * M));  gev = sum((gfp(pk).*c).^2) / sum(gfp(pk).^2);",
                "    if gev > best, best = gev; Tbest = T; end",
                "end",
                "Xn = X ./ vecnorm(X);  [~, seq] = max(abs(Tbest' * Xn));   % back-fitting"]
        cl = code_lines(code, 15)
        if cl.width > 12.6: cl.scale_to_fit_width(12.6)
        cc_ = card(cl, CARD, pad=0.25).move_to(np.array([0, -0.45, 0]))
        self.play(FadeIn(cc_[0]))
        self.play(LaggedStart(*[FadeIn(x_, shift=RIGHT * 0.1) for x_ in cl], lag_ratio=0.12), run_time=3.0)

        # ---------------------------------------------------------- 23 trappole
        self.new(tr("Pitfalls", "Trappole"), tr("Pitfalls and open questions", "Trappole e questioni aperte"))
        g = rows_mob([tr("Results depend on ++filter band++, channels and clustering choices: report them.", "I risultati dipendono da ++banda del filtro++, canali e clustering: riportarli."),
                      tr("k is a ++modelling choice++ (4 vs 5–7).", "k è una ++scelta di modello++ (4 vs 5–7)."),
                      tr("Use ++group or normative templates++; beware circularity.", "Usare template ++di gruppo o normativi++; attenzione alla circolarità."),
                      tr("Labels across studies matched ++by eye or correlation++: check.", "Etichette tra studi abbinate ++a occhio o per correlazione++: verificare."),
                      tr("Functional meaning of each class still ++debated++.", "Significato funzionale di ogni classe ancora ++dibattuto++.")], 20, col=ACC).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.2), run_time=2.0)

        # ---------------------------------------------------------- 24 domande
        self.new(tr("Check your understanding", "Verifica"), tr("Three questions", "Tre domande"))
        g = rows_mob([tr("GMD = 0 but different GFP between conditions: what about the generators?", "GMD = 0 ma GFP diversa tra condizioni: che dire dei generatori?"),
                      tr("Why does modified k-means ignore map polarity?", "Perché il k-means modificato ignora la polarità?"),
                      tr("GEV 75 % with k = 4, 82 % with k = 8: why is 8 not automatically better?", "GEV 75 % con k = 4, 82 % con k = 8: perché 8 non è automaticamente meglio?")], 21, n=84, h=1.05, gap=0.35, col=ACC).shift(DOWN * 0.3)
        for r_ in g: self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.7)

        # ---------------------------------------------------------- 25 messaggi chiave
        self.new(tr("Take-home messages", "Messaggi chiave"), tr("Take-home messages", "Messaggi chiave"))
        g = rows_mob([tr("Maps are ++reference-free++: GFP = strength, GMD = shape.", "Mappe ++indipendenti dal riferimento++: GFP = intensità, GMD = forma."),
                      tr("Spontaneous EEG = sequence of ++quasi-stable maps++ (≈ 100 ms).", "EEG spontaneo = sequenza di ++mappe quasi stabili++ (≈ 100 ms)."),
                      tr("GFP peaks → ++modified k-means / TAAHC++ → templates → back-fitting.", "Picchi di GFP → ++k-means modificato / TAAHC++ → template → back-fitting."),
                      tr("A–D explain ≈ 70–80 % of variance; linked to ++large-scale networks++.", "A–D spiegano ≈ 70–80 % della varianza; legati a ++reti su larga scala++."),
                      tr("Sensitive to ++cognition, sleep, drugs, disease, stimulation++.", "Sensibili a ++cognizione, sonno, farmaci, malattia, stimolazione++.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 26 letture
        self.new(tr("Suggested reading", "Letture consigliate"), tr("Suggested reading", "Letture consigliate"))
        refs_slide(self, ["Michel & Koenig (2018) *NeuroImage* 180:577–593.", "Lehmann & Skrandies (1980) *Electroencephalogr Clin Neurophysiol* 48:609–621.",
                          "Lehmann, Ozaki & Pal (1987) *Electroencephalogr Clin Neurophysiol* 67:271–288.", "Pascual-Marqui, Michel & Lehmann (1995) *IEEE Trans Biomed Eng* 42:658–665.",
                          "Murray, Brunet & Michel (2008) *Brain Topogr* 20:249–264.", "Koenig et al. (2002) *NeuroImage* 16:41–48.",
                          "Britz, Van De Ville & Michel (2010) *NeuroImage* 52:1162–1170.", "Van De Ville, Britz & Michel (2010) *PNAS* 107:18179–18184.",
                          "Custo et al. (2017) *Brain Connect* 7:671–682.", "Zappasodi et al. (2019) *NeuroImage* 189:560–573.",
                          "Croce, Zappasodi & Capotosto (2018) *Sci Rep* 8:1287.", "da Cruz et al. (2020) *Nat Commun* 11:3089."], 17)
        self.end()
