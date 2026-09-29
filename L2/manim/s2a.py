from base import *
import figs2 as F2
import neuro as N

ION = {"Na": ACC, "K": TEAL, "Cl": GRN, "Ca": AMB}


class A2_Membrana(Base):
    start_num = 1

    def construct(self):
        # ---------------------------------------------------------- 1 copertina: uno spike che corre lungo l'assone
        self.new(first=True); self.num = 1
        f = F2.f05_neuron(); fit(f, 0.55, np.array([3.6, -1.9, 0]))
        keep = [k for k in f if not k.startswith("l_")]

        def vis():
            self.play(LaggedStart(*[FadeIn(f[k]) for k in keep], lag_ratio=0.1), run_time=1.5)
        copertina(self, tr("Lecture 2", "Lezione 2"), tr("The cellular bases\nof the EEG", "Le basi cellulari\ndell'EEG"), vis)
        soma = f["soma"].get_center(); a0 = f["axon"].get_start(); a1 = f["axon"].get_end()
        path = polyline(soma + np.array([-0.9, 0.5, 0]), soma, a0, a1)
        loop_packets(self, [(path, 2, lambda u: AMB if u < 0.35 else ACC, 0.07)], T=2.4)

        # ---------------------------------------------------------- 2 percorso
        self.new(tr("Lecture 2", "Lezione 2"), tr("From ions to scalp potentials", "Dagli ioni ai potenziali di scalpo"))
        g = rows_mob([tr("The *neuron* and its ++membrane++: why a cell has a voltage.", "Il *neurone* e la sua ++membrana++: perché una cellula ha una tensione."),
                      tr("*Resting potential*: ++Nernst++ and ++Goldman++.", "*Potenziale di riposo*: ++Nernst++ e ++Goldman++."),
                      tr("*Action potential*: channels, threshold, propagation.", "*Potenziale d'azione*: canali, soglia, propagazione."),
                      tr("*Synapses*: EPSP/IPSP and ++summation++.", "*Sinapsi*: EPSP/IPSP e ++sommazione++."),
                      tr("To the EEG: ++sinks/sources++, pyramids, ++thalamocortical loops++.", "Verso l'EEG: ++pozzi/sorgenti++, piramidali, ++anelli talamo-corticali++.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 3 la domanda
        self.new(tr("The question", "La domanda"), tr("What happens in a neuron when the EEG goes down?", "Che cosa succede in un neurone quando l'EEG scende?"))
        f = F2.f03_question(); fit(f, 0.85, np.array([-3.0, -0.6, 0]))
        self.play(Create(f["scalp"]), FadeIn(f["sl"]), FadeIn(f["el"]))
        self.play(Create(f["cell"]), run_time=1.5)
        self.play(FadeIn(f["base"]), Create(f["tr"]), FadeIn(f["neg"]))
        self.play(FadeIn(f["q"], scale=1.5))
        bl = bullets([tr("A ++negative++ wave of tens of ms at the scalp.", "Un'onda ++negativa++ di decine di ms sullo scalpo."),
                      tr("Which ++cellular events++? Where do currents flow?", "Quali ++eventi cellulari++? Dove scorrono le correnti?"),
                      tr("Ingredients: ~membrane~, ~ions~, ~channels~, ~synapses~.", "Ingredienti: ~membrana~, ~ioni~, ~canali~, ~sinapsi~."),
                      tr("⚠ Clinical EEG often plots ++negative up++.", "⚠ L'EEG clinico spesso disegna il ++negativo in alto++.")], 21, n=34, gap=0.35).move_to(np.array([3.6, -0.3, 0]))
        for b_ in bl: self.play(FadeIn(b_))

        # ---------------------------------------------------------- 4 sezione
        self.new(); section_title(self, 1, tr("The neuron and its membrane", "Il neurone e la sua membrana"))

        # ---------------------------------------------------------- 5 anatomia + flusso del segnale
        self.new(tr("The neuron", "Il neurone"), tr("Receive, integrate, transmit", "Ricevere, integrare, trasmettere"))
        f = F2.f05_neuron(); fit(f, 0.95, np.array([0.3, 0.2, 0]))
        self.play(Create(f["dend"]), FadeIn(f["l_d"]), run_time=1.4)
        self.play(FadeIn(f["soma"]), FadeIn(f["l_s"]))
        self.play(FadeIn(f["hill"]), FadeIn(f["l_h"]))
        self.play(Create(f["axon"]), LaggedStart(*[FadeIn(m) for m in f["myelin"]], lag_ratio=0.1), FadeIn(f["l_m"]), run_time=1.4)
        self.play(FadeIn(f["term"]), FadeIn(f["l_t"]))
        mt = metaphor(tr("a ++tree that listens++ (dendrites) and a ++cable that talks++ (axon); the hillock decides when to speak.",
                         "un ++albero che ascolta++ (dendriti) e un ++cavo che parla++ (assone); il monticolo decide quando parlare."), 19, 100).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(mt))
        soma = f["soma"].get_center(); ends = [m.get_end() for m in f["dend"] if isinstance(m, Line)][::3]
        streams = [(polyline(e, soma, f["axon"].get_start(), f["axon"].get_end()), 1, lambda u: AMB if u < 0.35 else ACC, 0.07) for e in ends[:4]]
        loop_packets(self, streams, T=3.0)

        # ---------------------------------------------------------- 6 membrana: canali che lasciano passare ioni
        self.new(tr("The membrane", "La membrana"), tr("A thin insulator with gates", "Un sottile isolante con cancelli"))
        f = F2.f06_membrane(); fit(f, 0.9, np.array([-2.2, 0.5, 0]))
        self.play(LaggedStart(*[FadeIn(m) for m in f["heads"]], lag_ratio=0.01), FadeIn(f["tails"]), run_time=1.5)
        self.play(FadeIn(f["ch0"]), FadeIn(f["ch1"]), FadeIn(f["cl0"]), FadeIn(f["cl1"]), FadeIn(f["out"]), FadeIn(f["in"]))
        self.play(FadeIn(f["th"]))
        bl = bullets([tr("++Bilayer++ ≈5 nm: separates charges → ++capacitor++.", "++Doppio strato++ ≈5 nm: separa le cariche → ++condensatore++."),
                      tr("*Channels*: selective pores gated by ++voltage++ or ++ligands++.", "*Canali*: pori selettivi comandati da ++tensione++ o ++ligandi++."),
                      tr("*Pumps* (Na⁺/K⁺-ATPase) keep the gradients.", "Le *pompe* (Na⁺/K⁺-ATPasi) mantengono i gradienti.")], 19, n=30, gap=0.35).move_to(np.array([4.6, 0.4, 0]))
        for b_ in bl: self.play(FadeIn(b_))
        mt = metaphor(tr("a ++dam++: pumps fill the reservoir, channels are the ++sluice gates++.", "una ++diga++: le pompe riempiono il bacino, i canali sono le ++paratoie++."), 18, 100).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(mt))
        ck = f["ch0"].get_center(); cn = f["ch1"].get_center(); hgt = f["ch0"].height
        pk = polyline(ck + UP * 0.0 + DOWN * hgt * 0.9, ck + UP * hgt * 0.9)   # K+ esce (dal basso = dentro verso l'alto = fuori)
        pn = polyline(cn + UP * hgt * 0.9, cn + DOWN * hgt * 0.9)              # Na+ entra
        loop_packets(self, [(pk, 3, TEAL, 0.09), (pn, 2, ACC, 0.09)], T=2.0)

        # ---------------------------------------------------------- 7 concentrazioni
        self.new(tr("Ions", "Ioni"), tr("Unequal concentrations inside and outside", "Concentrazioni diverse dentro e fuori"))
        f = F2.f07_ions(); fit(f, 0.95, np.array([-2.4, -0.4, 0]))
        self.play(FadeIn(f["ax"]), *[FadeIn(f[k]) for k in f if k.startswith("t")], FadeIn(f["leg"]))
        for k in range(4):
            bi, bo = f[f"bi{k}"], f[f"bo{k}"]
            self.play(GrowFromEdge(bi, DOWN), GrowFromEdge(bo, DOWN), FadeIn(f[f"n{k}"]), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(f[f"e{k}"]) for k in range(4)], lag_ratio=0.2))
        bl = bullets([tr("~K⁺~ inside, ~Na⁺ Cl⁻ Ca²⁺~ outside.", "~K⁺~ dentro, ~Na⁺ Cl⁻ Ca²⁺~ fuori."),
                      tr("Ca²⁺ inside is ++10 000× lower++.", "Il Ca²⁺ interno è ++10 000 volte più basso++."),
                      tr("Each gradient = a ++charged battery++.", "Ogni gradiente = una ++batteria carica++.")], 20, n=30, gap=0.35).move_to(np.array([4.4, 0.0, 0]))
        for b_ in bl: self.play(FadeIn(b_))

        # ---------------------------------------------------------- 8 due forze: si raggiunge l'equilibrio di Nernst
        self.new(tr("Resting potential (1)", "Potenziale di riposo (1)"), tr("Diffusion vs electric force", "Diffusione contro forza elettrica"))
        cm = np.array([-3.2, -0.8, 0])
        mem = Line(cm + UP * 1.7, cm + DOWN * 1.7, color=AMB, stroke_width=8)
        lin = T(tr("inside", "dentro"), 18).move_to(cm + np.array([-1.6, 1.95, 0])); lout = T(tr("outside", "fuori"), 18).move_to(cm + np.array([1.6, 1.95, 0]))
        rng = np.random.default_rng(5)
        n_ = 24
        side0 = np.array([-1] * 20 + [1] * 4)
        pos0 = np.c_[rng.uniform(0.3, 2.6, n_), rng.uniform(-1.4, 1.4, n_)]
        prog = ValueTracker(0.0)            # 0 -> 1: 6 ioni passano fuori
        movers = [0, 3, 6, 9, 12, 15]

        def ions():
            g = VGroup()
            p = prog.get_value()
            for k in range(n_):
                s = side0[k]; x = pos0[k, 0] * s
                if k in movers:
                    j = movers.index(k); u = np.clip(p * 6 - j, 0, 1)
                    x = -pos0[k, 0] * (1 - u) + (0.6 + 0.3 * j) * u
                g.add(Dot(cm + np.array([x, pos0[k, 1], 0]), radius=0.09, color=TEAL))
            return g

        def meter():
            p = prog.get_value(); V = N.nernst(5, 140) * min(1.0, p * 1.05)
            base = np.array([0.4, -2.2, 0])
            ld = 1.6 - 0.8 * p; le = 0.2 + 0.6 * p
            return VGroup(Arrow(cm + np.array([-0.8, 2.4, 0]), cm + np.array([-0.8 + ld, 2.4, 0]), buff=0, color=TEAL, stroke_width=5, tip_length=0.18),
                          Arrow(cm + np.array([0.8, -2.15, 0]), cm + np.array([0.8 - le, -2.15, 0]), buff=0, color=ACC, stroke_width=5, tip_length=0.18),
                          M(rf"V_m = {V:.0f}\ \mathrm{{mV}}", AMB, 0.8).move_to(np.array([0.9, 1.3, 0])))
        iz = always_redraw(ions); mz = always_redraw(meter)
        self.play(Create(mem), FadeIn(lin), FadeIn(lout), FadeIn(iz))
        la = VGroup(T(tr("diffusion", "diffusione"), 16, TEAL).move_to(cm + np.array([-2.0, 2.4, 0])), T(tr("electric force", "forza elettrica"), 16, ACC).move_to(cm + np.array([2.2, -2.15, 0])))
        self.play(FadeIn(mz), FadeIn(la))
        self.play(prog.animate.set_value(1.0), run_time=4.0, rate_func=linear)
        iz.clear_updaters(); mz.clear_updaters()
        eq = fcard(r"E_{ion} = \frac{RT}{zF}\ln\frac{[\mathrm{ion}]_{out}}{[\mathrm{ion}]_{in}}", CARD2, 0.85).move_to(np.array([3.9, 0.0, 0]))
        tx = T(tr("Equilibrium: E_K ≈ −89 mV, E_{Na} ≈ +67 mV (37 °C)", "Equilibrio: E_K ≈ −89 mV, E_{Na} ≈ +67 mV (37 °C)"), 18, MUT, n=60).next_to(eq, DOWN, buff=0.35)
        self.play(FadeIn(eq[0]), Write(eq[1])); self.play(FadeIn(tx))
        # loop: equilibrio dinamico — ioni che attraversano avanti e indietro in egual numero
        loop_start(self)
        ph = ValueTracker(0.0)
        self.remove(iz)

        def eq_ions():
            g = VGroup(); x_ = ph.get_value()
            for k in range(n_):
                s = side0[k]; x = pos0[k, 0] * s
                if k in movers:
                    j = movers.index(k); x = (0.6 + 0.3 * j)
                if k in (1, 4):          # due ioni che fanno la spola attraverso la membrana
                    u = 0.5 - 0.5 * np.cos(2 * np.pi * (x_ + 0.5 * (k == 4)))
                    x = -0.8 + 1.6 * u
                g.add(Dot(cm + np.array([x, pos0[k, 1], 0]), radius=0.09, color=TEAL))
            return g
        ez = always_redraw(eq_ions); self.add(ez)
        loop_play(self, ph, 3.0); ez.clear_updaters()

        # ---------------------------------------------------------- 9 GHK: il voto pesato
        self.new(tr("Resting potential (2)", "Potenziale di riposo (2)"), tr("A weighted vote of the ions (GHK)", "Un voto pesato degli ioni (GHK)"))
        f = F2.f10_scale(4.6); fit(f, 1.0, np.array([-3.7, -0.5, 0]))
        self.play(FadeIn(f["ax"]), *[FadeIn(f[k]) for k in f if k.startswith("t")], FadeIn(f["u"]))
        self.play(LaggedStart(*[FadeIn(f[f"m{k}"]) for k in range(5)], lag_ratio=0.2))
        v0, v1, H_ = -100, 140, 4.6
        yv = lambda v: f["ax"].get_bottom()[1] + (v - v0) / (v1 - v0) * H_
        xa = f["ax"].get_center()[0]
        pna = ValueTracker(0.05)
        mk = always_redraw(lambda: VGroup(Triangle(fill_opacity=1, color=AMB).scale(0.14).rotate(-PI / 2).move_to(np.array([xa - 0.35, yv(N.ghk(1, pna.get_value(), 0.45)), 0])),
                                          M(rf"V = {N.ghk(1, pna.get_value(), 0.45):.0f}\,\mathrm{{mV}}", AMB, 0.6).move_to(np.array([xa - 1.5, yv(N.ghk(1, pna.get_value(), 0.45)), 0]))))
        self.play(FadeIn(mk))
        eq = fcard(r"V = \frac{RT}{F}\ln\frac{p_K[K]_o + p_{Na}[Na]_o + p_{Cl}[Cl]_i}{p_K[K]_i + p_{Na}[Na]_i + p_{Cl}[Cl]_o}", CARD2, 0.7).move_to(np.array([3.0, 1.3, 0]))
        self.play(FadeIn(eq[0]), Write(eq[1]))
        bl = bullets([tr("Each ion pulls V toward its E, ++weighted by permeability++.", "Ogni ione tira V verso il suo E, ++pesato per la permeabilità++."),
                      tr("Rest: p_K : p_{Na} : p_{Cl} ≈ 1 : 0.05 : 0.45 → ≈ −65 mV.", "Riposo: p_K : p_{Na} : p_{Cl} ≈ 1 : 0,05 : 0,45 → ≈ −65 mV."),
                      tr("Open Na⁺ channels (p_{Na} ×400) → V jumps toward E_{Na}: ++a spike++.", "Aprire i canali Na⁺ (p_{Na} ×400) → V salta verso E_{Na}: ++uno spike++.")], 18, n=46, gap=0.3).next_to(eq, DOWN, buff=0.45).align_to(eq, LEFT)
        for b_ in bl[:2]: self.play(FadeIn(b_))
        self.play(FadeIn(bl[2]), pna.animate.set_value(20.0), run_time=1.5)
        self.play(pna.animate.set_value(0.05), run_time=1.0)
        mk.clear_updaters()
        loop_start(self)
        ph = ValueTracker(0.0)
        self.remove(mk)
        pfun = lambda u: 0.05 * (400.0 ** (np.exp(-0.5 * ((u - 0.35) / 0.06) ** 2)))
        mk2 = always_redraw(lambda: VGroup(Triangle(fill_opacity=1, color=AMB).scale(0.14).rotate(-PI / 2).move_to(np.array([xa - 0.35, yv(N.ghk(1, pfun(ph.get_value()), 0.45)), 0])),
                                           M(rf"V = {N.ghk(1, pfun(ph.get_value()), 0.45):.0f}\,\mathrm{{mV}}", AMB, 0.6).move_to(np.array([xa - 1.5, yv(N.ghk(1, pfun(ph.get_value()), 0.45)), 0]))))
        self.add(mk2); loop_play(self, ph, 2.5); mk2.clear_updaters()

        # ---------------------------------------------------------- 10 sezione
        self.new(); section_title(self, 2, tr("The action potential", "Il potenziale d'azione"))

        # ---------------------------------------------------------- 11 HH
        self.new(tr("Action potential (1)", "Potenziale d'azione (1)"), tr("Anatomy of a spike (Hodgkin–Huxley)", "Anatomia di uno spike (Hodgkin–Huxley)"))
        f = F2.f13_ap(6.4, 3.4); fit(f, 1.0, np.array([-2.8, -0.5, 0]))
        self.play(FadeIn(f["ax"]), FadeIn(f["thr"]), FadeIn(f["thl"]), FadeIn(f["l0"]))
        self.play(Create(f["V"]), run_time=3, rate_func=linear)
        self.play(Create(f["gNa"]), FadeIn(f["lNa"]), Create(f["gK"]), FadeIn(f["lK"]), run_time=2)
        ph_ = [tr("stimulus depolarises", "lo stimolo depolarizza"), tr("threshold: Na⁺ channels open", "soglia: si aprono i Na⁺"), tr("Na⁺ rushes in → +40 mV", "entra Na⁺ → +40 mV"),
               tr("Na⁺ inactivate, K⁺ open", "Na⁺ inattivati, K⁺ aperti"), tr("repolarisation, undershoot", "ripolarizzazione, iperpolarizzazione"), tr("refractory, back to rest", "refrattarietà, ritorno al riposo")]
        lst = VGroup(*[VGroup(VGroup(Circle(0.17, color=AMB, fill_opacity=1, stroke_width=0), TX(str(i + 1), font=BODY, font_size=15, color=BG if False else "#16213A", weight=BOLD)), T(p, 18, n=34)).arrange(RIGHT, buff=0.2) for i, p in enumerate(ph_)]).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(np.array([4.2, -0.4, 0]))
        for i in range(6):
            self.play(FadeIn(f[f"p{i}"], scale=1.5), FadeIn(lst[i], shift=LEFT * 0.2), run_time=0.6)
        # loop: cursore che ripercorre lo spike
        V_ = f["V"]
        loop_start(self)
        ph = ValueTracker(0.0)
        cur = always_redraw(lambda: Dot(V_.point_from_proportion(ph.get_value()), radius=0.09, color=AMB))
        self.add(cur); loop_play(self, ph, 3.0); cur.clear_updaters()

        # ---------------------------------------------------------- 12 tutto o nulla
        self.new(tr("Action potential (2)", "Potenziale d'azione (2)"), tr("All-or-none: the rate carries the information", "Tutto o nulla: conta la frequenza"))
        f = F2.f14_fI(6.0); fit(f, 0.85, np.array([-1.2, -0.15, 0]))
        for k in range(3):
            self.play(Create(f[f"v{k}"]), FadeIn(f[f"l{k}"]), run_time=1.3, rate_func=linear)
        self.play(FadeIn(f["note"]))
        mt = metaphor(tr("a ++toilet flush++: press gently and nothing happens; past the point, the flush is always the same.", "lo ++sciacquone++: premi piano e non succede nulla; oltre il punto, lo scarico è sempre uguale."), 18, 100).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(mt))

        # ---------------------------------------------------------- 13 propagazione continua vs saltatoria
        self.new(tr("Action potential (3)", "Potenziale d'azione (3)"), tr("Continuous and saltatory conduction", "Conduzione continua e saltatoria"))
        f = F2.f15_conduction(10.0); fit(f, 1.0, np.array([0, 0.6, 0]))
        self.play(Create(f["ax0"]), FadeIn(f["l0"]))
        self.play(Create(f["ax1"]), LaggedStart(*[FadeIn(f[f"my{j}"]) for j in range(6)], lag_ratio=0.1), FadeIn(f["l1"]))
        cap = T(tr("~For EEG~: spikes are brief (≈1 ms) and move away → they ++contribute little++ to the scalp signal.", "~Per l'EEG~: gli spike sono brevi (≈1 ms) e si allontanano → ++contribuiscono poco++ al segnale di scalpo."), 20, n=100).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(cap))
        x0 = f["ax0"].get_start()[0]; x1 = f["ax0"].get_end()[0]; y0 = f["ax0"].get_center()[1]; y1 = f["ax1"].get_center()[1]
        nodes = [f["my0"].get_left()[0] - 0.12] + [f[f"my{j}"].get_right()[0] + 0.12 for j in range(6)]
        loop_start(self)
        ph = ValueTracker(0.0)

        def waves():
            u = ph.get_value()
            xs_ = np.linspace(x0, x1, 200)
            c0 = x0 + (x1 - x0) * u                                   # lenta: 1 passaggio per periodo
            g = VGroup(VMobject(color=TEAL, stroke_width=4).set_points_as_corners([np.array([x, y0 + 0.45 * np.exp(-0.5 * ((x - c0) / 0.25) ** 2), 0]) for x in xs_]))
            j = int((u * 4 * len(nodes)) % len(nodes))                # veloce: 4 passaggi, a salti di nodo
            g.add(Dot(np.array([nodes[j], y1, 0]), radius=0.16, color=ACC), Dot(np.array([nodes[j], y1, 0]), radius=0.3, color=ACC, fill_opacity=0.25))
            return g
        wz = always_redraw(waves); self.add(wz); loop_play(self, ph, 4.0); wz.clear_updaters()
        self.end()
