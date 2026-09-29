from base import *
import figs1 as F1
from s1a import rows_mob, metaphor, PURP, GRN


class B1_Natura(Base):
    start_num = 12

    def section(self, n, title):
        num = TX(f"{n:02d}", font=SERIF_F, font_size=110, color=ACC, weight=BOLD).to_edge(LEFT, buff=1.0).shift(UP * 0.6)
        ti = TX(title, font=SERIF_F, font_size=52, color=FG, weight=BOLD).next_to(num, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(FadeIn(num, shift=RIGHT * 0.3), Write(ti), run_time=1.2)

    def construct(self):
        # ---------------------------------------------------------- 12 sezione
        self.new(first=True)
        self.section(2, tr("So what is EEG, really?", "Ma che cos'è davvero l'EEG?"))

        # ---------------------------------------------------------- 13 definizione e ordini di grandezza
        self.new(tr("Definition", "Definizione"), tr("EEG: a tiny voltage recorded on the scalp", "EEG: una tensione minuscola sullo scalpo"))
        d = card(T(tr("The *EEG* is the time course of the ++potential difference++ between scalp electrodes, generated mainly by the summed ++postsynaptic currents++ of millions of synchronous cortical ++pyramidal neurons++.",
                      "L'*EEG* è l'andamento nel tempo della ++differenza di potenziale++ tra elettrodi di scalpo, generata soprattutto dalle ++correnti postsinaptiche++ sommate di milioni di ++neuroni piramidali++ corticali sincroni."), 21, n=96), CARD2).to_edge(UP, buff=1.75)
        self.play(FadeIn(d))
        f = F1.f15_magnitudes(7.0); fit(f, 0.85, np.array([-2.0, -1.4, 0]))
        self.play(*[FadeIn(f[k]) for k in f if k.startswith(("n", "ax", "t", "note"))])
        for k in range(5):
            b = f[f"b{k}"]; tgt = b.copy(); b.stretch_to_fit_width(0.01).align_to(tgt, LEFT)
            self.play(Transform(b, tgt), FadeIn(f[f"v{k}"]), run_time=0.6)
        bl = bullets([tr("10–100 µV: ~1000× smaller~ than the ECG.", "10–100 µV: ~1000× più piccolo~ dell'ECG."), tr("Frequencies ≈0.5–100 Hz.", "Frequenze ≈0.5–100 Hz."),
                      tr("⇒ high-gain amplifiers, low impedance, artifact control.", "⇒ amplificatori ad alto guadagno, bassa impedenza, controllo artefatti.")], 19, n=30, gap=0.3).move_to(np.array([4.6, -1.3, 0]))
        for b_ in bl: self.play(FadeIn(b_))

        # ---------------------------------------------------------- 14 analogia idraulica
        self.new(tr("Basic concepts", "Concetti di base"), tr("Voltage, current, resistance: a hydraulic analogy", "Tensione, corrente, resistenza: analogia idraulica"))
        f = F1.f16_water(); fit(f, 0.95, np.array([0.3, 0.3, 0]))
        self.play(FadeIn(VGroup(f["t1"], f["w1"], f["t2"], f["w2"], f["p1"], f["p2"])))
        self.play(GrowArrow(f["dv"]), FadeIn(f["V"]))
        path = polyline(f["t1"].get_corner(DR) + np.array([0.1, 0.62, 0]), f["t2"].get_corner(DL) + np.array([-0.1, 0.62, 0]))
        cap = VGroup(T(tr("~Voltage~ = pressure difference · ~current~ = flow · ~resistance~ = narrowing", "~Tensione~ = differenza di pressione · ~corrente~ = portata · ~resistenza~ = strozzatura"), 20, n=100)).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(f["I"]), FadeIn(f["R"]), Write(f["ohm"]), FadeIn(cap))
        # loop: la corrente scorre (più veloce nella strozzatura)
        a0 = f["p1"].get_start(); a1 = f["p1"].get_end(); yc = (f["p1"].get_start()[1] + f["p2"].get_start()[1]) / 2
        xa, xb = f["p1"].points[0][0], f["p1"].points[-1][0]
        loop_start(self)
        ph = ValueTracker(0.0)
        n = 14
        xs0 = np.linspace(0, 1, n, endpoint=False)

        def xpos(u):
            # velocità ∝ 1/sezione: nel tratto centrale (strozzatura) scorre ~2 volte più veloce (mappa u -> x)
            g = lambda s_: s_ - 0.08 * np.sin(2 * np.pi * s_)
            return xa + (xb - xa) * g(u)

        def drops():
            return VGroup(*[Dot(np.array([xpos((s_ + ph.get_value()) % 1.0), yc, 0]), radius=0.06, color=TEAL) for s_ in xs0])
        dd = always_redraw(drops); self.add(dd)
        loop_play(self, ph, 3.0); dd.clear_updaters()

        # ---------------------------------------------------------- 15 differenza di potenziale
        self.new(tr("What EEG measures (1)", "Che cosa misura l'EEG (1)"), tr("Every channel is a potential difference", "Ogni canale è una differenza di potenziale"))
        f = F1.f17_diff(); fit(f, 0.8, np.array([-3.2, 0.5, 0]))
        self.play(FadeIn(f["head"]), FadeIn(f["ea"]), FadeIn(f["er"]), FadeIn(f["la"]), FadeIn(f["lr"]))
        self.play(Create(f["wa"]), Create(f["wr"]), FadeIn(f["amp"]), FadeIn(f["pl"]), FadeIn(f["mi"]), GrowArrow(f["out"]))
        # tracce: attivo, riferimento, differenza
        tp, xa_ = E.periodic_eeg(4.0, seed=11, uv=20)
        _, xr = E.periodic_eeg(4.0, seed=12, peaks=((1.0, 0.5, 0.0),), uv=8)
        xa_ = xa_ + xr
        O = [np.array([1.6, 1.3, 0]), np.array([1.6, 0.1, 0]), np.array([1.6, -1.1, 0])]
        labs = [tr("φ active", "φ attivo"), tr("φ reference", "φ riferimento"), "V = φa − φr"]
        cols = [ACC, MUT, TEAL]; sigs = [xa_, xr, xa_ - xr]
        trs = VGroup(*[E.window_trace(tp, sigs[k], 0, 2.0, O[k], 5.0, 0.02, cols[k], 2.2) for k in range(3)])
        lb = VGroup(*[T(labs[k], 18, cols[k]).next_to(O[k], LEFT, buff=0.2).shift(UP * 0.05) for k in range(3)])
        lb = VGroup(*[T(labs[k], 18, cols[k]).move_to(O[k] + np.array([0.9, 0.5, 0])) for k in range(3)])
        for k in range(3): self.play(Create(trs[k]), FadeIn(lb[k]), run_time=1.0)
        mt = metaphor(tr("altitude: a mountain is \"3000 m\" only ++with respect to sea level++.", "l'altitudine: una montagna è \"3000 m\" solo ++rispetto al livello del mare++."), 19, 100).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(mt))
        loop_start(self)
        ph = ValueTracker(0.0)
        live = always_redraw(lambda: VGroup(*[E.window_trace(tp, sigs[k], ph.get_value() * 4.0, 2.0, O[k], 5.0, 0.02, cols[k], 2.2) for k in range(3)]))
        self.remove(trs); self.add(live); loop_play(self, ph, 4.0); live.clear_updaters()

        # ---------------------------------------------------------- 16 spike vs PSP
        self.new(tr("What EEG measures (2)", "Che cosa misura l'EEG (2)"), tr("Spikes or synaptic potentials?", "Spike o potenziali sinaptici?"))
        f = F1.f18_summation(5.6); fit(f, 1.0, np.array([0, 0.2, 0]))
        self.play(FadeIn(f["ts"]), FadeIn(f["tp"]))
        self.play(LaggedStart(*[Create(f[f"s{k}"]) for k in range(5)], lag_ratio=0.15), LaggedStart(*[Create(f[f"p{k}"]) for k in range(5)], lag_ratio=0.15), run_time=2)
        self.play(FadeIn(f["sig"]), FadeIn(f["sig2"]), TransformFromCopy(VGroup(*[f[f"s{k}"] for k in range(5)]), f["ss"]), TransformFromCopy(VGroup(*[f[f"p{k}"] for k in range(5)]), f["ps"]), run_time=1.8)
        cap = T(tr("Brief spikes rarely overlap and cancel; slow PSPs ++overlap and add up++ → they dominate the EEG.", "Gli spike brevi si sovrappongono raramente e si annullano; i PSP lenti ++si sovrappongono e si sommano++ → dominano l'EEG."), 21, n=100).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(cap))

        # ---------------------------------------------------------- 17 sincronia
        self.new(tr("What EEG measures (3)", "Che cosa misura l'EEG (3)"), tr("Synchrony: why a few neurons dominate", "Sincronia: perché pochi neuroni dominano"))
        N = 40
        rng = np.random.default_rng(8); ph0 = rng.uniform(0, 2 * np.pi, N)
        sy = ValueTracker(0.0); tt = ValueTracker(0.0)
        Ob = np.array([-6.2, -0.2, 0])

        def oscs():
            g = VGroup()
            phs = (1 - sy.get_value()) * ph0
            ts = np.linspace(0, 1, 60)
            for k in range(8):
                y0 = 1.6 - 0.32 * k
                pts = [np.array([-6.2 + 4.0 * u, y0 + 0.1 * np.sin(2 * np.pi * (2 * u + tt.get_value()) + phs[k]), 0]) for u in ts]
                g.add(VMobject(color=TEAL, stroke_width=1.8).set_points_smoothly(pts))
            s_ = np.array([np.sum(np.sin(2 * np.pi * (2 * u + tt.get_value()) + phs)) / N for u in ts])
            g.add(VMobject(color=ACC, stroke_width=4).set_points_smoothly([np.array([-6.2 + 4.0 * u, -1.6 + 1.0 * v, 0]) for u, v in zip(ts, s_)]))
            return g
        oz = always_redraw(oscs)
        lab = VGroup(T(tr("8 of N = 40 neurons", "8 di N = 40 neuroni"), 16, MUT).move_to(np.array([-4.2, 2.1, 0])), T("Σ / N", 20, ACC).move_to(np.array([-6.6, -1.6, 0])))
        self.play(FadeIn(oz), FadeIn(lab))
        self.play(tt.animate.set_value(1.5), run_time=1.5, rate_func=linear)
        self.play(sy.animate.set_value(1.0), tt.animate.set_value(3.5), run_time=2.5, rate_func=linear)
        oz.clear_updaters()
        f = F1.f19_sync(5.0); fit(f, 0.85, np.array([1.3, -0.1, 0]))
        self.play(FadeIn(f["ax"]), *[FadeIn(f[k]) for k in f if k.startswith("t")])
        self.play(Create(f["asy"]), FadeIn(f["la"])); self.play(Create(f["sync"]), FadeIn(f["ls"]))
        txtb = bullets([tr("random phases: sum ∝ *√N*", "fasi casuali: somma ∝ *√N*"), tr("in phase: sum ∝ *N*", "in fase: somma ∝ *N*"),
                        tr("N = 10⁶ → ×1000", "N = 10⁶ → ×1000"), tr("~EEG measures synchrony~", "~L'EEG misura la sincronia~")], 18, n=22, gap=0.3).move_to(np.array([5.3, 0.3, 0]))
        for b_ in txtb: self.play(FadeIn(b_), run_time=0.5)
        loop_start(self)
        tt.set_value(0.0)
        self.remove(oz); oz = always_redraw(oscs); self.add(oz)
        loop_play(self, tt, 2.0); oz.clear_updaters()

        # ---------------------------------------------------------- 18 campi aperti / chiusi
        self.new(tr("What EEG measures (4)", "Che cosa misura l'EEG (4)"), tr("Geometry matters: open and closed fields", "Conta la geometria: campi aperti e chiusi"))
        f = F1.f20_fields(); fit(f, 1.0, np.array([0, 0.2, 0]))
        self.play(LaggedStart(*[Create(f[f"p{k}"]) for k in range(5)], lag_ratio=0.15), Create(f["st"]), run_time=2)
        self.play(*[GrowArrow(a) for a in f["ar"]], FadeIn(f["lo"]), FadeIn(f["lc"]))
        cap = T(tr("Pyramidal cells (layers III and V) are ++aligned++ perpendicular to the surface: their dipoles add up.", "Le piramidali (strati III e V) sono ++allineate++ perpendicolarmente alla superficie: i loro dipoli si sommano."), 20, n=100).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(cap))
        # loop: dipoli che pulsano (aperto) e dipoli radiali della stellata che si annullano
        loop_start(self)
        ph = ValueTracker(0.0)
        bases = [a.get_start() for a in f["ar"]]
        cst = f["st"][0].get_center()

        def pulse():
            a_ = np.sin(2 * np.pi * ph.get_value())
            g = VGroup(*[Arrow(b, b + UP * (0.9 * a_ if abs(a_) > 0.05 else 0.05), buff=0, color=ACC, stroke_width=4, tip_length=0.15) for b in bases])
            for k in range(6):
                ang = 2 * np.pi * k / 6
                u = np.array([np.cos(ang), np.sin(ang), 0])
                g.add(Arrow(cst, cst + u * (0.5 * a_ if abs(a_) > 0.05 else 0.05), buff=0, color=TEAL, stroke_width=3, tip_length=0.12))
            return g
        self.remove(f["ar"]); pz = always_redraw(pulse); self.add(pz)
        loop_play(self, ph, 2.0); pz.clear_updaters()

        # ---------------------------------------------------------- 19 tre requisiti
        self.new(tr("What EEG measures (5)", "Che cosa misura l'EEG (5)"), tr("Three requirements for a scalp-visible signal", "Tre requisiti per un segnale visibile"))
        g = rows_mob([tr("*Synchrony*: events ++at the same time++.", "*Sincronia*: eventi ++nello stesso momento++."),
                      tr("*Alignment*: ++same orientation++ (pyramidal).", "*Allineamento*: ++stessa orientazione++ (piramidali)."),
                      tr("*Extent*: ≥ 6–10 cm², ++radial++ is best.", "*Estensione*: ≥ 6–10 cm², meglio se ++radiale++.")], 19, n=40, w=5.8, h=0.95, gap=0.25).to_edge(LEFT, buff=0.7).shift(UP * 0.4)
        for r_ in g: self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.6)
        f = F1.f21_gyrus(6.2); fit(f, 0.85, np.array([3.5, 0.1, 0]))
        self.play(FadeIn(f["skull"]), FadeIn(f["sk"]), Create(f["cx"]))
        ds = [f[k] for k in f if k.startswith("d")]
        self.play(LaggedStart(*[GrowArrow(a) for a in ds], lag_ratio=0.08), run_time=1.5)
        self.play(FadeIn(f["lr"]), FadeIn(f["lt"]))
        nb = card(T(tr("Absence of EEG change ≠ absence of neural activity.", "Assenza di variazioni EEG ≠ assenza di attività neurale."), 19, n=90), CARD2).to_edge(DOWN, buff=0.65)
        self.play(FadeIn(nb))

        # ---------------------------------------------------------- 20 conduzione di volume: dipolo che ruota
        self.new(tr("What EEG measures (6)", "Che cosa misura l'EEG (6)"), tr("Volume conduction and the inverse problem", "Conduzione di volume e problema inverso"))
        cL = np.array([-4.3, 0.3, 0]); cR = np.array([-0.6, 0.3, 0]); R = 1.45
        hd = VGroup(Circle(radius=R, color=FG, stroke_width=3).move_to(cL), Circle(radius=R * 0.88, color=MUT, stroke_width=2).move_to(cL), T(tr("side view · nose →", "vista laterale · naso →"), 15, MUT).move_to(cL + np.array([0, R + 0.3, 0])))
        th = ValueTracker(0.0)
        pos = np.array([0.0, 0.15, 0.55])

        def dip():
            a_ = th.get_value()
            c = cL + np.array([pos[1], pos[2] - 0.3, 0]) * R      # vista laterale: x = avanti, y = alto
            u = np.array([np.sin(a_), np.cos(a_), 0])
            return Arrow(c - 0.45 * u, c + 0.45 * u, buff=0, color=ACC, stroke_width=6, tip_length=0.2)

        def mp():
            a_ = th.get_value()
            V, m = E.dipole_map(pos, [0.0, np.sin(a_), np.cos(a_)], n=101, blur=0.22)
            img, out = E.topomap(V, m, cR, R)
            return Group(img, out)
        self.play(FadeIn(hd), FadeIn(T(tr("side view: dipole in the cortex", "vista laterale: dipolo nella corteccia"), 16, MUT).next_to(hd, DOWN, buff=0.2)))
        dz = always_redraw(dip); mz = redraw(mp)
        self.play(FadeIn(dz), FadeIn(mz), FadeIn(T(tr("scalp map", "mappa di scalpo"), 16, MUT).next_to(cR + DOWN * R, DOWN, buff=0.2)))
        self.play(th.animate.set_value(PI / 2), run_time=2.5)
        self.play(th.animate.set_value(0.0), run_time=1.5)
        dz.clear_updaters(); mz.clear_updaters()
        bl = bullets([tr("Currents spread through brain, CSF, ++skull++, scalp: each electrode sees a ++blurred mix++.", "Le correnti attraversano cervello, liquor, ++cranio++, scalpo: ogni elettrodo vede una ++miscela sfocata++."),
                      tr("*Forward*: sources → map (unique).", "*Diretto*: sorgenti → mappa (unico)."),
                      tr("*Inverse*: map → sources, ++ill-posed++ (Helmholtz 1853) → constraints (L9).", "*Inverso*: mappa → sorgenti, ++mal posto++ (Helmholtz 1853) → vincoli (L9).")], 18, n=30, gap=0.35).move_to(np.array([4.4, 0.2, 0]))
        for b_ in bl: self.play(FadeIn(b_))
        loop_start(self)
        th.set_value(0.0)
        self.remove(dz, mz); dz = always_redraw(dip)
        ph = ValueTracker(0.0)
        mz = redraw(lambda: (th.set_value(2 * PI * ph.get_value()), mp())[1])
        dz = always_redraw(lambda: (th.set_value(2 * PI * ph.get_value()), dip())[1])
        self.add(dz, mz)
        loop_play(self, ph, 6.0); dz.clear_updaters(); mz.clear_updaters()

        # ---------------------------------------------------------- 21 canali -> mappe
        self.new(tr("What EEG measures (7)", "Che cosa misura l'EEG (7)"), tr("From channels to topographic maps", "Dai canali alle mappe topografiche"))
        # EEG periodico a 19 canali: sorgente alfa occipitale + sorgente lenta frontale
        tp, s1 = E.periodic_eeg(4.0, seed=21, peaks=((10, 0.6, 2.0),), slope=0.5, uv=30)
        _, s2 = E.periodic_eeg(4.0, seed=22, peaks=((3, 0.6, 2.0),), slope=1.5, uv=30)
        X = []
        for k, nm in enumerate(E.NAMES):
            e = E.el3d(nm)
            X.append(1.3 * max(0, -e[1]) ** 1.5 * s1 + 1.1 * max(0, e[1]) ** 1.5 * s2 + 0.15 * E.periodic_eeg(4.0, seed=40 + k, uv=30)[1])
        X = np.array(X)
        show = ["Fp1", "Fz", "C3", "Cz", "P3", "Pz", "O1", "O2"]
        Ox = -6.0; Wt = 6.0; win = 2.0
        yy = lambda k: 1.9 - 0.55 * k
        lbl = VGroup(*[T(nm, 15, MUT).move_to(np.array([Ox - 0.4, yy(k), 0])) for k, nm in enumerate(show)])
        cR = np.array([3.7, 0.0, 0]); Rr = 1.7

        def traces(off):
            return VGroup(*[E.window_trace(tp, X[E.NAMES.index(nm)], off, win, np.array([Ox, yy(k), 0]), Wt, 0.006, TEAL, 1.8) for k, nm in enumerate(show)])

        def cursor(off):
            return DashedLine(np.array([Ox + Wt * 0.5, 2.3, 0]), np.array([Ox + Wt * 0.5, -2.2, 0]), color=ACC, stroke_width=2.5)

        def tmap(off):
            i0 = int(round(((off + win * 0.5) % 4.0) * 250)) % X.shape[1]
            V, m = E.interp_map(X[:, i0], n=101)
            img, out = E.topomap(V, m, cR, Rr, elec=True)
            return Group(img, out)
        tz = traces(0.0)
        self.play(FadeIn(lbl), LaggedStart(*[Create(x_) for x_ in tz], lag_ratio=0.1), run_time=2)
        self.play(Create(cursor(0)))
        m0 = tmap(0.0)
        self.play(FadeIn(m0))
        cap = T(tr("One value per electrode at each instant → an interpolated ++scalp map++. EEG = a ++movie of maps++.", "Un valore per elettrodo in ogni istante → una ++mappa di scalpo++ interpolata. EEG = un ++film di mappe++."), 20, n=100).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(cap))
        loop_start(self)
        ph = ValueTracker(0.0)
        self.remove(tz, m0)
        lz = always_redraw(lambda: traces(ph.get_value() * 4.0))
        mz = redraw(lambda: tmap(ph.get_value() * 4.0))
        self.add(lz, mz)
        loop_play(self, ph, 8.0); lz.clear_updaters(); mz.clear_updaters()

        # ---------------------------------------------------------- 22 ritmi
        self.new(tr("Preview", "Anteprima"), tr("The EEG rhythms", "I ritmi EEG"))
        f = F1.f26_rhythms(6.0); fit(f, 0.9, np.array([-0.3, -0.35, 0]))
        for k in range(5):
            self.play(FadeIn(f[f"n{k}"]), FadeIn(f[f"r{k}"]), Create(f[f"x{k}"]), FadeIn(f[f"s{k}"]), run_time=0.8)
        self.play(FadeIn(f["sb"]))
        # loop: le onde scorrono (1 s di segnale = numero intero di cicli per ogni banda)
        freqs = [2.0, 6.0, 10.0, 20.0, 40.0]; amps = [1.0, 0.8, 0.7, 0.35, 0.2]
        cols = ["#8E7CC3", TEAL, ACC, AMB, GRN]
        O0 = [f[f"x{k}"].points[0] for k in range(5)]
        Wd = f[f"x{k}"].get_width()
        hs = 0.38 * 0.9
        loop_start(self)
        ph = ValueTracker(0.0)

        def waves():
            g = VGroup()
            tt_ = np.linspace(0, 1, 400)
            for k in range(5):
                y0 = O0[k][1] - amps[k] * hs * np.sin(0)
                base = np.array([O0[k][0], f[f"n{k}"].get_center()[1] - 0.12 * 0.9, 0])
                pts = [base + np.array([u * Wd, amps[k] * hs * np.sin(2 * np.pi * freqs[k] * (u - ph.get_value() / 2)), 0]) for u in tt_]
                g.add(VMobject(color=cols[k], stroke_width=2.5).set_points_as_corners(pts))
            return g
        self.remove(*[f[f"x{k}"] for k in range(5)])
        wz = always_redraw(waves); self.add(wz)
        loop_play(self, ph, 2.0); wz.clear_updaters()

        # ---------------------------------------------------------- 23 punti di forza e limiti
        self.new(tr("Strengths and limits", "Punti di forza e limiti"), tr("EEG: what it is good at, what it is not", "EEG: in cosa è bravo, in cosa no"))
        L_ = card(VGroup(T("~" + tr("Strengths", "Punti di forza") + "~", 24),
                         bullets([tr("++ms++ temporal resolution", "risoluzione temporale al ++ms++"), tr("++direct++ neural measure", "misura neurale ++diretta++"),
                                  tr("non-invasive, cheap, portable", "non invasivo, economico, portatile"), tr("combinable: fMRI, TMS, BCI", "combinabile: fMRI, TMS, BCI"),
                                  tr("clinical gold standard: epilepsy, sleep", "gold standard clinico: epilessia, sonno")], 19, n=34, gap=0.25)).arrange(DOWN, aligned_edge=LEFT, buff=0.3), CARD)
        R_ = card(VGroup(T("~" + tr("Limitations", "Limiti") + "~", 24),
                         bullets([tr("poor ++spatial++ resolution (cm)", "scarsa risoluzione ++spaziale++ (cm)"), tr("mostly cortical, radial, synchronous", "soprattutto corticale, radiale, sincrono"),
                                  tr("deep structures hardly visible", "strutture profonde poco visibili"), tr("reference-dependent, artifacts", "dipende dal riferimento, artefatti"),
                                  tr("polarity ≠ excitation/inhibition", "polarità ≠ eccitazione/inibizione")], 19, n=34, gap=0.25)).arrange(DOWN, aligned_edge=LEFT, buff=0.3), CARD2)
        VGroup(L_, R_).arrange(RIGHT, buff=0.5, aligned_edge=UP).shift(DOWN * 0.3)
        self.play(FadeIn(L_, shift=RIGHT * 0.2)); self.play(FadeIn(R_, shift=LEFT * 0.2))

        # ---------------------------------------------------------- 24 famiglie di analisi
        self.new(tr("Analysis", "Analisi"), tr("What will we do with the EEG?", "Che cosa faremo con l'EEG?"))
        fam = [(tr("Preprocessing & ICA", "Preprocessing e ICA"), 5), (tr("Spectra & time-frequency", "Spettri e tempo-frequenza"), 6), (tr("Event-related potentials", "Potenziali evento-correlati"), 7),
               (tr("Topographies & microstates", "Topografie e microstati"), 8), (tr("Sources & connectivity", "Sorgenti e connettività"), 9), (tr("Decoding (MVPA)", "Decoding (MVPA)"), 10)]
        cs = VGroup()
        for i, (n_, l_) in enumerate(fam):
            box = RoundedRectangle(corner_radius=0.14, width=3.8, height=1.3, fill_color=CARD if i % 2 == 0 else CARD2, fill_opacity=1, stroke_width=0)
            cs.add(VGroup(box, VGroup(T("**" + n_ + "**", 20, n=30), T("~" + tr("Lecture", "Lezione") + f" {l_}~", 18)).arrange(DOWN, buff=0.12).move_to(box)))
        cs.arrange_in_grid(2, 3, buff=(0.35, 0.35)).shift(UP * 0.4)
        self.play(LaggedStart(*[FadeIn(c_, scale=0.9) for c_ in cs], lag_ratio=0.15), run_time=2)
        sw = T(tr("*Software*: EEGLAB, FieldTrip, Brainstorm (MATLAB) · MNE-Python. Analyses ++combine++.", "*Software*: EEGLAB, FieldTrip, Brainstorm (MATLAB) · MNE-Python. Le analisi ++si combinano++."), 20, n=100).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(sw))

        # ---------------------------------------------------------- 25 domande
        self.new(tr("Check your understanding", "Verifica"), tr("Three questions", "Tre domande"))
        g = rows_mob([tr("Why do ≈1 % of synchronous pyramidal neurons outweigh the other 99 %?", "Perché ≈l'1 % di piramidali sincroni pesa più del restante 99 %?"),
                      tr("\"At Cz the brain potential is +12 µV\": what is missing?", "\"In Cz il potenziale cerebrale è +12 µV\": che cosa manca?"),
                      tr("150 ms or 250 ms after a stimulus? EEG or fMRI, and why?", "150 ms o 250 ms dopo uno stimolo? EEG o fMRI, e perché?")], 22, n=80, h=1.05, gap=0.35, col=ACC).shift(DOWN * 0.3)
        for r_ in g: self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.7)

        # ---------------------------------------------------------- 26 messaggi chiave
        self.new(tr("Take-home messages", "Messaggi chiave"), tr("Take-home messages", "Messaggi chiave"))
        g = rows_mob([tr("EEG = ++potential differences++, ++µV++, ++ms++.", "EEG = ++differenze di potenziale++, ++µV++, ++ms++."),
                      tr("Source: ++synchronous postsynaptic currents++ of aligned ++pyramidal++ cells.", "Sorgente: ++correnti postsinaptiche sincrone++ di cellule ++piramidali++ allineate."),
                      tr("~Synchrony, alignment, extent~: much activity is invisible.", "~Sincronia, allineamento, estensione~: molta attività è invisibile."),
                      tr("Volume conduction blurs; the ++inverse problem++ is ill-posed.", "La conduzione di volume sfoca; il ++problema inverso++ è mal posto."),
                      tr("From Galvani and Berger to ++computational++ neuroscience.", "Da Galvani e Berger alle neuroscienze ++computazionali++.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 27 letture
        self.new(tr("Suggested reading", "Letture consigliate"), tr("Suggested reading", "Letture consigliate"))
        refs = ["Nunez & Srinivasan (2006) *Electric Fields of the Brain*, 2nd ed., OUP.",
                "Buzsáki, Anastassiou & Koch (2012) *Nat Rev Neurosci* 13:407–420.",
                "Cohen (2014) *Analyzing Neural Time Series Data*, MIT Press.",
                "Luck (2014) *An Introduction to the ERP Technique*, 2nd ed., MIT Press.",
                "Berger (1929) *Arch Psychiatr Nervenkr* 87:527–570.",
                "Caton (1875) *Br Med J* 2:278.",
                "Sejnowski, Churchland & Movshon (2014) *Nat Neurosci* 17:1440–1441.",
                "Tao et al. (2005) *Epilepsia* 46:669–676."]
        rb = bullets(refs, 19, n=100, gap=0.22).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(r_) for r_ in rb], lag_ratio=0.1), run_time=2)
        self.end()
