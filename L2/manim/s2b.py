from base import *
import figs2 as F2
import neuro as N


class B2_Sinapsi(Base):
    start_num = 14

    def construct(self):
        # ---------------------------------------------------------- 14 sezione
        self.new(first=True); section_title(self, 3, tr("Synapses: where the EEG is born", "Sinapsi: dove nasce l'EEG"))

        # ---------------------------------------------------------- 15 trasmissione sinaptica animata
        self.new(tr("Synapses (1)", "Sinapsi (1)"), tr("Chemical transmission, step by step", "Trasmissione chimica, passo per passo"))
        f = F2.f17_synapse(); fit(f, 0.9, np.array([-3.6, -0.5, 0]))
        self.play(Create(f["pre"]), Create(f["post"]), FadeIn(f["lpre"]), FadeIn(f["lpost"]))
        self.play(*[FadeIn(f[k]) for k in f if k.startswith(("v", "r", "ca", "l"))])
        g = rows_mob([tr("Spike reaches the terminal", "Lo spike arriva al terminale"), tr("++Ca²⁺ channels++ open, Ca²⁺ enters", "Si aprono i ++canali Ca²⁺++, entra Ca²⁺"),
                      tr("++Vesicles++ release transmitter", "Le ++vescicole++ liberano il trasmettitore"), tr("Transmitter binds ++receptors++", "Il trasmettitore lega i ++recettori++"),
                      tr("Ions flow → ++PSP++ (10–100 ms)", "Scorrono ioni → ++PSP++ (10–100 ms)")], 19, n=40, w=6.2, h=0.72, gap=0.14, col=ACC).move_to(np.array([3.4, -0.4, 0]))
        for r_ in g: self.play(FadeIn(r_, shift=LEFT * 0.2), run_time=0.5)
        # loop: ciclo di rilascio (Ca entra, vescicola si fonde, trasmettitore diffonde, recettori si illuminano)
        cas = [f["ca0"].get_center(), f["ca1"].get_center()]
        vpos = f["v2"].get_center(); cleft_y = (f["r0"].get_center()[1] + f["ca0"].get_center()[1]) / 2
        recs = [f[f"r{k}"] for k in range(4)]
        loop_start(self)
        ph = ValueTracker(0.0)
        rng = np.random.default_rng(3); jit = rng.uniform(-1.0, 1.0, 10)

        def cycle():
            u = ph.get_value(); gg = VGroup()
            for c in cas:                                         # Ca2+ entra (0-0.25)
                a = np.clip(u / 0.25, 0, 1)
                if 0 < u < 0.3:
                    gg.add(Dot(c + UP * (-0.35 + 0.7 * a), radius=0.06, color=AMB))
            b = np.clip((u - 0.2) / 0.2, 0, 1)                    # vescicola scende e si fonde (0.2-0.4)
            vp = vpos + (np.array([0, cleft_y + 0.25, 0]) - vpos) * np.array([0, 1, 0]) * b
            if u < 0.45:
                gg.add(Circle(radius=0.15, color=AMB, fill_color=AMB, fill_opacity=0.5).move_to(vp))
            c_ = np.clip((u - 0.4) / 0.3, 0, 1)                    # trasmettitore diffonde (0.4-0.7)
            if 0.4 < u < 0.85:
                for j in range(10):
                    gg.add(Dot(np.array([vpos[0] + jit[j] * 0.9 * c_, cleft_y + 0.2 - 0.25 * c_, 0]), radius=0.04, color=AMB, fill_opacity=1 - np.clip((u - 0.7) / 0.15, 0, 1)))
            glow = np.exp(-0.5 * ((u - 0.72) / 0.08) ** 2)
            for r in recs:
                gg.add(r.copy().set_fill(interpolate_color(ManimColor(ACC), ManimColor(WHITE), glow), opacity=0.9))
            return gg
        cz = always_redraw(cycle); self.add(cz); loop_play(self, ph, 3.0); cz.clear_updaters()

        # ---------------------------------------------------------- 16 EPSP / IPSP
        self.new(tr("Synapses (2)", "Sinapsi (2)"), tr("Excitatory and inhibitory synapses", "Sinapsi eccitatorie e inibitorie"))
        f = F2.f18_epsp_ipsp(6.0); fit(f, 0.95, np.array([-2.6, -0.3, 0]))
        for k in range(2):
            self.play(FadeIn(f[f"b{k}"]), FadeIn(f[f"l{k}"]), Create(f[f"v{k}"]), FadeIn(f[f"e{k}"]), run_time=1.3)
        self.play(FadeIn(f["sc"]))
        bl = bullets([tr("*Glutamate* → Na⁺ in → ++EPSP++ (toward threshold)", "*Glutammato* → entra Na⁺ → ++EPSP++ (verso la soglia)"),
                      tr("*GABA* → Cl⁻ in / K⁺ out → ++IPSP++", "*GABA* → entra Cl⁻ / esce K⁺ → ++IPSP++"),
                      tr("PSPs are ++graded++ and ++slow++", "I PSP sono ++graduati++ e ++lenti++")], 19, n=30, gap=0.35).move_to(np.array([4.5, 0.1, 0]))
        for b_ in bl: self.play(FadeIn(b_))

        # ---------------------------------------------------------- 17 sommazione (animata dal vivo)
        self.new(tr("Synapses (3)", "Sinapsi (3)"), tr("Temporal and spatial summation", "Sommazione temporale e spaziale"))
        O = np.array([-6.0, -0.4, 0]); Wd = 7.0; yv = lambda v: (v + 72) / 22 * 2.2
        rate = ValueTracker(25.0)
        axl = Line(O + UP * yv(-72), O + UP * yv(-72) + RIGHT * Wd, color=MUT, stroke_width=2)
        thr = DashedLine(O + UP * yv(-55), O + UP * yv(-55) + RIGHT * Wd, color=MUT, stroke_width=2)
        thl = T(tr("threshold", "soglia"), 16, MUT).next_to(thr, RIGHT, buff=0.1)

        def trace():
            t, V, sp = F2.summation(rate.get_value(), T=200.0)
            g = VGroup(VMobject(color=ACC if sp else TEAL, stroke_width=3).set_points_as_corners([O + np.array([a / 200 * Wd, yv(v), 0]) for a, v in zip(t[::4], V[::4])]))
            for i in sp:
                x = t[i] / 200 * Wd
                g.add(Line(O + np.array([x, yv(-55), 0]), O + np.array([x, yv(-55) + 1.0, 0]), color=ACC, stroke_width=3))
            g.add(M(rf"\text{{input}} = {rate.get_value():.0f}\ \mathrm{{Hz}}", AMB, 0.65).move_to(O + np.array([1.4, -0.55, 0])))
            return g
        tz = always_redraw(trace)
        self.play(Create(axl), Create(thr), FadeIn(thl), FadeIn(tz))
        self.play(rate.animate.set_value(90.0), run_time=3.5, rate_func=linear)
        tz.clear_updaters()
        f = F2.f20_spatial(); fit(f, 0.85, np.array([4.4, 0.2, 0]))
        self.play(Create(f["cell"]), FadeIn(f["hill"]), FadeIn(f["hl"]))
        self.play(LaggedStart(*[FadeIn(f[f"s{k}"], scale=1.5) for k in range(3)], lag_ratio=0.3))
        mt = metaphor(tr("a ++committee vote++: yes (EPSP) and no (IPSP), counted by the chair (hillock).", "una ++votazione++: sì (EPSP) e no (IPSP), contati dal presidente (monticolo)."), 18, 100).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(mt))
        # loop: frequenza che oscilla 25 <-> 90 Hz, segnali che viaggiano dalle sinapsi al monticolo
        loop_start(self)
        ph = ValueTracker(0.0)
        self.remove(tz)
        tz2 = always_redraw(lambda: (rate.set_value(57.5 - 32.5 * np.cos(2 * np.pi * ph.get_value())), trace())[1])
        hc = f["hill"].get_center()
        pk = lambda k: polyline(f[f"s{k}"].get_center(), hc)
        pz = always_redraw(lambda: VGroup(*[Dot(pk(k).point_from_proportion((ph.get_value() * 3 + k * 0.33) % 1.0), radius=0.07, color=[ACC, ACC, TEAL][k]) for k in range(3)]))
        self.add(tz2, pz); loop_play(self, ph, 6.0); tz2.clear_updaters(); pz.clear_updaters()

        # ---------------------------------------------------------- 18 sezione
        self.new(); section_title(self, 4, tr("From synapses to the scalp EEG", "Dalle sinapsi all'EEG di scalpo"))

        # ---------------------------------------------------------- 19 PSP vs spike
        self.new(tr("Synapses → EEG (1)", "Sinapsi → EEG (1)"), tr("Why PSPs, not spikes, make the EEG", "Perché PSP e non spike fanno l'EEG"))
        f = F2.f22_decay(5.0); fit(f, 0.9, np.array([-3.6, -0.4, 0]))
        self.play(FadeIn(f["ax"]))
        self.play(Create(f["d"]), FadeIn(f["ld"])); self.play(Create(f["q"]), FadeIn(f["lq"]))
        L_ = card(VGroup(T("~" + tr("Postsynaptic potential", "Potenziale postsinaptico") + "~", 20),
                         bullets([tr("10–100 ms", "10–100 ms"), tr("dipole ∝ 1/r²", "dipolo ∝ 1/r²"), tr("++sums well++", "++si somma bene++")], 18, n=26, gap=0.2)).arrange(DOWN, aligned_edge=LEFT, buff=0.2), CARD2)
        R_ = card(VGroup(T("~" + tr("Action potential", "Potenziale d'azione") + "~", 20),
                         bullets([tr("≈1 ms", "≈1 ms"), tr("quadrupole ∝ 1/r³", "quadrupolo ∝ 1/r³"), tr("++sums poorly++", "++si somma male++")], 18, n=26, gap=0.2)).arrange(DOWN, aligned_edge=LEFT, buff=0.2), CARD)
        VGroup(L_, R_).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(np.array([3.5, 0.3, 0]))
        self.play(FadeIn(L_)); self.play(FadeIn(R_))
        nb = T(tr("Scalp EEG ≈ summed ++postsynaptic++ currents of many synchronous neurons.", "EEG di scalpo ≈ somma delle correnti ++postsinaptiche++ di molti neuroni sincroni."), 20, n=100).to_edge(DOWN, buff=0.75)
        self.play(FadeIn(nb))

        # ---------------------------------------------------------- 20 pozzi e sorgenti (animazione delle correnti)
        self.new(tr("Synapses → EEG (2)", "Sinapsi → EEG (2)"), tr("Sinks, sources and the origin of polarity", "Pozzi, sorgenti e origine della polarità"))
        f = F2.f23_sinksource(); fit(f, 0.95, np.array([-4.2, -0.5, 0]))
        self.play(Create(f["cell"]), FadeIn(f["surf"]), FadeIn(f["sl"]))
        self.play(FadeIn(f["sink"], scale=1.5), FadeIn(f["src"], scale=1.5))
        arcs = [f[k] for k in f if k.startswith("c") and k != "cell"]
        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.1))
        # potenziale di superficie
        el = Circle(radius=0.12, color=FG, fill_color=BG if False else "#16213A", fill_opacity=1).move_to(f["surf"].get_center() + UP * 0.25)
        tp = np.linspace(0, 1, 100); wv = -np.exp(-0.5 * ((tp - 0.4) / 0.1) ** 2)
        eegw = VMobject(color=TEAL, stroke_width=3).set_points_smoothly([np.array([-2.0 + 1.6 * u, 2.3 + 0.5 * v, 0]) for u, v in zip(tp, wv)])
        self.play(FadeIn(el), Create(eegw))
        bl = bullets([tr("EPSP on the ++apical dendrite++: positive ions enter → *sink* (−) near the surface.", "EPSP sul ++dendrite apicale++: entrano ioni positivi → *pozzo* (−) vicino alla superficie."),
                      tr("Current exits near the soma → *source* (+) in depth.", "La corrente esce vicino al soma → *sorgente* (+) in profondità."),
                      tr("Sink above + source below = ++current dipole++ → surface ~negative~.", "Pozzo sopra + sorgente sotto = ++dipolo di corrente++ → superficie ~negativa~.")], 19, n=48, gap=0.3).move_to(np.array([2.8, 0.7, 0]))
        for b_ in bl: self.play(FadeIn(b_))
        warn = card(T(tr("⚠ An ++IPSP near the soma++ gives the same scalp sign: ++polarity alone cannot distinguish excitation from inhibition++.",
                         "⚠ Un ++IPSP vicino al soma++ dà lo stesso segno sullo scalpo: ++la sola polarità non distingue eccitazione e inibizione++."), 18, n=60), CARD2).move_to(np.array([2.8, -2.2, 0]))
        self.play(FadeIn(warn))
        # loop: cariche che scorrono lungo le linee di corrente extracellulari (sorgente -> pozzo)
        streams = [(a, 2, AMB, 0.05) for a in arcs]
        # le linee sono disegnate da sorgente a pozzo: il flusso extracellulare va dalla sorgente (+) al pozzo (−)
        loop_packets(self, streams, T=2.5)

        # ---------------------------------------------------------- 21 piramidali
        self.new(tr("Synapses → EEG (3)", "Sinapsi → EEG (3)"), tr("Pyramidal neurons: the main generators", "Neuroni piramidali: i principali generatori"))
        pyr = VGroup(*[E.pyramidal(np.array([-5.2 + 0.55 * k, -1.2, 0]), 0.6) for k in range(6)])
        st = VGroup(*[E.stellate(np.array([2.2 + 1.2 * (k % 3), -0.6 - 1.0 * (k // 3), 0]), 0.45, n=8, seed=k) for k in range(6)])
        self.play(LaggedStart(*[Create(p) for p in pyr], lag_ratio=0.1), LaggedStart(*[Create(s_) for s_ in st], lag_ratio=0.1), run_time=2)
        lp = T(tr("~Pyramidal~ (≈70–80 %): aligned → ++open field++", "~Piramidali~ (≈70–80 %): allineate → ++campo aperto++"), 19, n=40).move_to(np.array([-3.9, 1.3, 0]))
        ls = T(tr("~Stellate/interneurons~ (≈20–30 %): radial → ++closed field++, EEG \"ghosts\"", "~Stellate/interneuroni~ (≈20–30 %): radiali → ++campo chiuso++, \"fantasmi\" per l'EEG"), 19, n=40).move_to(np.array([3.4, 1.3, 0]))
        self.play(FadeIn(lp), FadeIn(ls))
        nb = T(tr("Different methods see different cells: EEG ≠ fMRI is ++physiology++, not error.", "Metodi diversi vedono cellule diverse: EEG ≠ fMRI è ++fisiologia++, non errore."), 20, n=100).to_edge(DOWN, buff=0.75)
        self.play(FadeIn(nb))
        # loop: dipoli piramidali che pulsano in fase (somma) vs stellate (annullamento)
        loop_start(self)
        ph = ValueTracker(0.0)
        bases = [np.array([-5.2 + 0.55 * k, -0.4, 0]) for k in range(6)]
        cst = [s_[0].get_center() for s_ in st]

        def puls():
            a_ = np.sin(2 * np.pi * ph.get_value()); g = VGroup()
            for b in bases:
                g.add(Arrow(b, b + UP * (0.9 * a_ if abs(a_) > 0.05 else 0.05), buff=0, color=ACC, stroke_width=4, tip_length=0.14))
            tot = 6 * a_
            g.add(Arrow(np.array([-3.8, -2.6, 0]), np.array([-3.8, -2.6 + 0.12 * tot + 0.001, 0]), buff=0, color=ACC, stroke_width=8, tip_length=0.2), M(r"\Sigma", ACC, 0.7).move_to(np.array([-4.3, -2.6, 0])))
            for c in cst:
                for k in range(4):
                    u = np.array([np.cos(k * PI / 2), np.sin(k * PI / 2), 0])
                    g.add(Arrow(c, c + u * (0.35 * a_ if abs(a_) > 0.05 else 0.02), buff=0, color=TEAL, stroke_width=2.5, tip_length=0.08))
            g.add(M(r"\Sigma \approx 0", TEAL, 0.7).move_to(np.array([3.4, -2.6, 0])))
            return g
        pzz = always_redraw(puls); self.add(pzz); loop_play(self, ph, 2.0); pzz.clear_updaters()

        # ---------------------------------------------------------- 22 sezione
        self.new(); section_title(self, 5, tr("Thalamocortical loops and rhythms", "Anelli talamo-corticali e ritmi"))

        # ---------------------------------------------------------- 23 anello talamo-corticale
        self.new(tr("Rhythms (1)", "Ritmi (1)"), tr("The thalamocortical loop: a rhythm generator", "L'anello talamo-corticale: un generatore di ritmi"))
        f = F2.f25_loop(); fit(f, 1.0, np.array([-3.4, -0.5, 0]))
        self.play(FadeIn(f["ctx"]), FadeIn(f["ctxl"]), FadeIn(f["tc"]), FadeIn(f["trn"]))
        for a, l in (("sens", "sl"), ("a1", None), ("a2", None), ("a4", "l4"), ("a3", "l3")):
            self.play(Create(f[a]), *([FadeIn(f[l])] if l else []), run_time=0.7)
        bl = bullets([tr("*TC* neurons relay input to cortex (glutamate).", "I neuroni *TC* inviano l'input alla corteccia (glutammato)."),
                      tr("*TRN* ++inhibits++ TC cells (GABA).", "Il *TRN* ++inibisce++ le cellule TC (GABA)."),
                      tr("Excitation → inhibition → rebound: the loop ++oscillates++.", "Eccitazione → inibizione → rimbalzo: l'anello ++oscilla++."),
                      tr("The EEG sees the ++cortical PSPs++ it paces.", "L'EEG vede i ++PSP corticali++ che esso scandisce.")], 19, n=34, gap=0.35).move_to(np.array([3.6, -0.2, 0]))
        for b_ in bl: self.play(FadeIn(b_))
        # loop: attività che gira nell'anello; la corteccia "pulsa"
        p1 = f["a1"]; p2_ = f["a2"]; p3 = f["a3"]; p4 = f["a4"]
        cyc = [p4, p3]      # TC -> TRN -> TC (anello di ritmo), con uscita verso la corteccia
        loop_start(self)
        ph = ValueTracker(0.0)
        ctx0 = f["ctx"]

        def act():
            u = ph.get_value(); g = VGroup()
            for k in range(2):
                v = (2 * u) % 1.0
                seg = p4 if v < 0.5 else p3; w = (v % 0.5) * 2
                g.add(Dot(seg.point_from_proportion(min(w, 0.999)), radius=0.08, color=TEAL if v < 0.5 else PURP))
            g.add(Dot(p1.point_from_proportion((2 * u) % 1.0 * 0.999), radius=0.08, color=TEAL))
            glow = 0.5 + 0.5 * np.cos(2 * np.pi * 2 * u - 1.0)
            g.add(ctx0.copy().set_fill(ACC, opacity=0.15 + 0.45 * glow))
            return g
        az = always_redraw(act); self.add(az); loop_play(self, ph, 2.0); az.clear_updaters()

        # ---------------------------------------------------------- 24 modi tonico / burst
        self.new(tr("Rhythms (2)", "Ritmi (2)"), tr("Tonic vs burst firing: wake and sleep", "Scarica tonica e a burst: veglia e sonno"))
        f = F2.f25_modes(6.0); fit(f, 0.95, np.array([-2.9, -0.3, 0]))
        self.play(Create(f["v0"]), FadeIn(f["l0"]), run_time=2, rate_func=linear)
        self.play(Create(f["v1"]), FadeIn(f["l1"]), run_time=2, rate_func=linear)
        self.play(FadeIn(f["sc"]))
        bl = bullets([tr("~Depolarised~ (wake): tonic, faithful relay.", "~Depolarizzato~ (veglia): tonico, trasmissione fedele."),
                      tr("~Hyperpolarised~ (sleep): T-type Ca²⁺ → LTS + ++burst++.", "~Iperpolarizzato~ (sonno): Ca²⁺ tipo T → LTS + ++burst++."),
                      tr("Rhythmic bursts → ++spindles++ (11–16 Hz), ++delta++.", "Burst ritmici → ++fusi++ (11–16 Hz), ++delta++.")], 19, n=30, gap=0.35).move_to(np.array([4.6, 0.0, 0]))
        for b_ in bl: self.play(FadeIn(b_))
        loop_start(self)
        ph = ValueTracker(0.0)
        tr0, tr1 = f["v0"], f["v1"]
        cur = always_redraw(lambda: VGroup(Dot(tr0.point_from_proportion(ph.get_value() * 0.999), radius=0.08, color=AMB), Dot(tr1.point_from_proportion(ph.get_value() * 0.999), radius=0.08, color=AMB)))
        self.add(cur); loop_play(self, ph, 4.0); cur.clear_updaters()

        # ---------------------------------------------------------- 25 alfa e inibizione: il semaforo
        self.new(tr("Rhythms (3)", "Ritmi (3)"), tr("Alpha: a signature of active inhibition", "Alfa: una firma di inibizione attiva"))
        bl = bullets([tr("High-threshold TC neurons (gap junctions) burst at ++alpha/theta++ (Hughes et al., 2004).", "Neuroni TC ad alta soglia (gap junction) scaricano a burst in ++alfa/theta++ (Hughes et al., 2004)."),
                      tr("They drive interneurons that ++rhythmically inhibit++ relay cells → information passes in ++windows++.", "Pilotano interneuroni che ++inibiscono ritmicamente++ le cellule relay → l'informazione passa a ++finestre++."),
                      tr("*Gating by inhibition*: alpha rises where input should be ++ignored++.", "*Gating per inibizione*: l'alfa cresce dove l'input va ++ignorato++.")], 19, n=52, gap=0.35).to_edge(LEFT, buff=0.7).to_edge(UP, buff=1.9)
        for b_ in bl: self.play(FadeIn(b_))
        # alfa + finestre di trasmissione
        O = np.array([-6.0, -1.9, 0]); Wd = 7.4
        tt = np.linspace(0, 1, 400)
        alpha = VMobject(color=ACC, stroke_width=3).set_points_smoothly([O + np.array([u * Wd, 0.5 * np.sin(2 * np.pi * 5 * u), 0]) for u in tt])
        la = T(tr("alpha (10 Hz)", "alfa (10 Hz)"), 16, ACC).next_to(alpha, UP, buff=0.1).align_to(alpha, LEFT)
        wins = VGroup(*[Rectangle(width=Wd / 5 * 0.35, height=1.4, stroke_width=0, fill_color=TEAL, fill_opacity=0.18).move_to(O + np.array([(k + 0.75) * Wd / 5, 0, 0])) for k in range(5)])
        lw = T(tr("windows of excitability", "finestre di eccitabilità"), 16, TEAL).next_to(wins, DOWN, buff=0.1)
        self.play(Create(alpha), FadeIn(la)); self.play(FadeIn(wins), FadeIn(lw))
        # semaforo
        tl = VGroup(RoundedRectangle(corner_radius=0.2, width=1.0, height=2.4, fill_color="#0E1628", fill_opacity=1, stroke_color=MUT))
        tl.move_to(np.array([4.6, -1.4, 0]))
        mt = metaphor(tr("alpha is a ++traffic light++ that blinks: the sensory road is open only in short windows.", "l'alfa è un ++semaforo++ che lampeggia: la strada sensoriale è aperta solo per brevi finestre."), 17, 40).move_to(np.array([4.3, 1.0, 0]))
        self.play(FadeIn(tl), FadeIn(mt))
        loop_start(self)
        ph = ValueTracker(0.0)
        cen = tl.get_center()

        def light():
            u = ph.get_value(); ph10 = (5 * u) % 1.0
            green = 0.6 < ph10 < 0.9
            g = VGroup(Circle(radius=0.33, color=ACC if not green else MUT, fill_color=ACC if not green else "#3A2A2E", fill_opacity=1).move_to(cen + UP * 0.55),
                       Circle(radius=0.33, color=TEAL if green else MUT, fill_color=TEAL if green else "#223057", fill_opacity=1).move_to(cen + DOWN * 0.55))
            g.add(Dot(O + np.array([u * Wd, 0.5 * np.sin(2 * np.pi * 5 * u), 0]), radius=0.08, color=AMB))
            return g
        lz = always_redraw(light); self.add(lz); loop_play(self, ph, 2.5); lz.clear_updaters()

        # ---------------------------------------------------------- 26 domande
        self.new(tr("Check your understanding", "Verifica"), tr("Three questions", "Tre domande"))
        g = rows_mob([tr("Extracellular K⁺ doubles (5 → 10 mM): what happens to E_K and V_{rest}?", "Il K⁺ esterno raddoppia (5 → 10 mM): che succede a E_K e V_{riposo}?"),
                      tr("Two physical reasons why PSPs, not spikes, dominate the EEG.", "Due ragioni fisiche per cui i PSP, e non gli spike, dominano l'EEG."),
                      tr("A negative wave at Fz: is the frontal cortex excited?", "Un'onda negativa in Fz: la corteccia frontale è eccitata?")], 22, n=80, h=1.05, gap=0.35, col=ACC).shift(DOWN * 0.3)
        for r_ in g: self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.7)

        # ---------------------------------------------------------- 27 messaggi chiave
        self.new(tr("Take-home messages", "Messaggi chiave"), tr("Take-home messages", "Messaggi chiave"))
        g = rows_mob([tr("Gradients + permeability = ++membrane potential++ (≈ −65 mV).", "Gradienti + permeabilità = ++potenziale di membrana++ (≈ −65 mV)."),
                      tr("Spikes: ++all-or-none++, ≈1 ms.", "Spike: ++tutto-o-nulla++, ≈1 ms."),
                      tr("PSPs: ++graded++, ++slow++, they sum.", "PSP: ++graduati++, ++lenti++, si sommano."),
                      tr("Synchronous PSPs in ++pyramidal++ cells → dipoles → EEG. Polarity is ambiguous.", "PSP sincroni nelle ++piramidali++ → dipoli → EEG. La polarità è ambigua."),
                      tr("++Thalamocortical loops++ pace rhythms: spindles, delta, alpha.", "Gli ++anelli talamo-corticali++ scandiscono i ritmi: fusi, delta, alfa.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 28 letture
        self.new(tr("Suggested reading", "Letture consigliate"), tr("Suggested reading", "Letture consigliate"))
        refs_slide(self, ["Kandel et al. (2021) *Principles of Neural Science*, 6th ed.", "Hille (2001) *Ion Channels of Excitable Membranes*, 3rd ed.",
                          "Hodgkin & Huxley (1952) *J Physiol* 117:500–544.", "Buzsáki, Anastassiou & Koch (2012) *Nat Rev Neurosci* 13:407–420.",
                          "Steriade, McCormick & Sejnowski (1993) *Science* 262:679–685.", "Llinás & Jahnsen (1982) *Nature* 297:406–408.",
                          "Hughes et al. (2004) *Neuron* 42:253–268.", "Klimesch (2012) *Trends Cogn Sci* 16:606–617.",
                          "Womelsdorf et al. (2014) *Nat Neurosci* 17:1031–1039."])
        self.end()
