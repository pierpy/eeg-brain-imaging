from base import *
import figs3 as F3


def scroll_group(self, sigs, Os, W, h, win, cols, T_, sw=2.0, old=None):
    """più tracce periodiche che scorrono insieme (loop senza scatti)."""
    D = sigs[0][0][-1] + (sigs[0][0][1] - sigs[0][0][0])
    loop_start(self)
    ph = ValueTracker(0.0)
    live = always_redraw(lambda: VGroup(*[E.window_trace(t, x, ph.get_value() * D, win, O, W, h, c, sw) for (t, x), O, c in zip(sigs, Os, cols)]))
    if old is not None:
        for m in old:
            self.remove(m)
        self.remove(old)
    self.add(live)
    loop_play(self, ph, T_)
    live.clear_updaters()


class A3_Dipoli(Base):
    start_num = 1

    def construct(self):
        # ---------------------------------------------------------- 1 copertina: dipolo che ruota con la sua mappa
        self.new(first=True); self.num = 1
        c = np.array([5.5, -2.35, 0]); Rr = 1.05
        th = ValueTracker(0.0)

        def mp():
            a = th.get_value()
            V, m = E.dipole_map([0.25 * np.sin(a), 0.1, 0.65], [np.sin(a), np.cos(a), 0.6], n=101, blur=0.2)
            img, out = E.topomap(V, m, c, Rr)
            return Group(img, out)

        def vis():
            self.play(FadeIn(mp()))
        copertina(self, tr("Lecture 3", "Lezione 3"), tr("From neurons to scalp:\ndipoles, conduction, rhythms", "Dai neuroni allo scalpo:\ndipoli, conduzione, ritmi"), vis)
        self.remove(*[m for m in self.mobjects if isinstance(m, Group) and len(m) == 2 and isinstance(m[0], ImageMobject)])
        loop_start(self)
        ph = ValueTracker(0.0)
        mz = redraw(lambda: (th.set_value(2 * PI * ph.get_value()), mp())[1])
        self.add(mz); loop_play(self, ph, 6.0); mz.clear_updaters()

        # ---------------------------------------------------------- 2 obiettivi
        self.new(tr("Lecture 3", "Lezione 3"), tr("Today: from cells to the scalp signal", "Oggi: dalle cellule al segnale di scalpo"))
        g = rows_mob([tr("The ++scales++ of brain activity: spikes, LFP, EEG.", "Le ++scale++ dell'attività cerebrale: spike, LFP, EEG."),
                      tr("The *current dipole*: building block of scalp maps.", "Il *dipolo di corrente*: mattone delle mappe di scalpo."),
                      tr("*Volume conduction*: tissues, conductivities, lead field.", "*Conduzione di volume*: tessuti, conducibilità, lead field."),
                      tr("++Montages++ and ++references++.", "++Montaggi++ e ++riferimenti++."),
                      tr("*Rhythms*: spectrum, bands, vigilance, sleep.", "*Ritmi*: spettro, bande, vigilanza, sonno.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 3 sezione
        self.new(); section_title(self, 1, tr("Scales of brain electrical activity", "Le scale dell'attività elettrica"))

        # ---------------------------------------------------------- 4 scale (tracce che scorrono)
        self.new(tr("Scales (1)", "Scale (1)"), tr("Micro, meso, macro", "Micro, meso, macro"))
        f = F3.f04_scales(3.4); fit(f, 1.0, np.array([0, 0.9, 0]))
        for k in range(3):
            self.play(Create(f[f"b{k}"]), FadeIn(f[f"t{k}"]), Create(f[f"x{k}"]), FadeIn(f[f"d{k}"]), *([GrowArrow(f[f"a{k}"])] if k < 2 else []), run_time=1.0)
        bl = bullets([tr("*Spikes*: output of single neurons (µm, ~1 ms).", "*Spike*: output di singoli neuroni (µm, ~1 ms)."),
                      tr("*LFP*: summed synaptic input of local networks (mm).", "*LFP*: input sinaptico sommato di reti locali (mm)."),
                      tr("*EEG*: LFPs of cm of cortex, filtered by the head.", "*EEG*: LFP di cm di corteccia, filtrati dalla testa.")], 20, n=90, gap=0.25).to_edge(DOWN, buff=0.75).to_edge(LEFT, buff=0.9)
        for b_ in bl: self.play(FadeIn(b_))
        # segnali periodici per il loop
        fs = 500; D = 2.0; tt = np.arange(0, D, 1 / fs)
        rng = np.random.default_rng(2)
        sp = 0.08 * E.periodic_eeg(D, fs, seed=1, uv=2.5)[1]
        for cc in rng.uniform(0, D, 16):
            sp += np.where(np.abs(tt - cc) < 0.004, -np.sin(np.pi * (tt - cc + 0.004) / 0.004) * 1.2, 0)
        lfp = E.periodic_eeg(D, fs, seed=3, peaks=((7, 1, 2), (23, 3, 0.5)), slope=0.5, uv=2.5)[1] / 2.0
        ee = E.periodic_eeg(D, fs, seed=4, uv=2.5)[1] / 2.5
        Os = [f[f"x{k}"].get_start() for k in range(3)]
        Os = [np.array([o[0], f[f"b{k}"].get_center()[1] - 0.2, 0]) for k, o in enumerate(Os)]
        Wd = f["x0"].get_width()
        scroll_group(self, [(tt, sp), (tt, lfp), (tt, ee)], Os, Wd, 0.55, 1.0, [AMB, TEAL, ACC], 4.0, old=VGroup(f["x0"], f["x1"], f["x2"]))

        # ---------------------------------------------------------- 5 sincronia (oscillatori dal vivo)
        self.new(tr("Scales (2)", "Scale (2)"), tr("Synchronisation makes the EEG visible", "La sincronizzazione rende visibile l'EEG"))
        N_ = 8; rng = np.random.default_rng(1); ph0 = rng.uniform(0, 2 * np.pi, N_)
        sy = ValueTracker(0.0); tt_ = ValueTracker(0.0)
        x0 = -6.2; Wd = 6.4

        def oscs():
            g = VGroup(); phs = (1 - sy.get_value()) * ph0; us = np.linspace(0, 1, 80)
            for k in range(N_):
                y0 = 2.0 - 0.3 * k
                g.add(VMobject(color=MUT, stroke_width=1.5).set_points_smoothly([np.array([x0 + Wd * u, y0 + 0.1 * np.sin(2 * np.pi * (4 * u + tt_.get_value()) + phs[k]), 0]) for u in us]))
            s = [np.sum(np.sin(2 * np.pi * (4 * u + tt_.get_value()) + phs)) for u in us]
            g.add(VMobject(color=ACC if sy.get_value() > 0.5 else TEAL, stroke_width=4).set_points_smoothly([np.array([x0 + Wd * u, -1.6 + 0.12 * v, 0]) for u, v in zip(us, s)]))
            return g
        oz = always_redraw(oscs)
        lab = VGroup(T(tr("8 neurons", "8 neuroni"), 16, MUT).move_to(np.array([x0 - 0.6, 1.0, 0])).rotate(PI / 2), T("Σ", 26, ACC).move_to(np.array([x0 - 0.5, -1.6, 0])))
        self.play(FadeIn(oz), FadeIn(lab))
        self.play(tt_.animate.set_value(1.5), run_time=1.5, rate_func=linear)
        self.play(sy.animate.set_value(1.0), tt_.animate.set_value(3.5), run_time=2.5, rate_func=linear)
        oz.clear_updaters()
        bl = bullets([tr("Same activity, same energy: only ++timing++ differs.", "Stessa attività, stessa energia: cambia solo la ++tempistica++."),
                      tr("Random phases → ++cancel++; aligned → ++add up++.", "Fasi casuali → si ++annullano++; allineate → si ++sommano++."),
                      tr("~EEG amplitude = synchrony~", "~Ampiezza EEG = sincronia~")], 20, n=26, gap=0.35).move_to(np.array([3.9, 0.4, 0]))
        for b_ in bl: self.play(FadeIn(b_))
        mt = metaphor(tr("a ++choir++: different songs = noise; the same song = music.", "un ++coro++: canzoni diverse = rumore; la stessa canzone = musica."), 18, 100).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(mt))
        loop_start(self)
        ph = ValueTracker(0.0)
        self.remove(oz)
        oz2 = always_redraw(lambda: (sy.set_value(0.5 - 0.5 * np.cos(2 * np.pi * ph.get_value())), tt_.set_value(8 * ph.get_value()), oscs())[2])
        self.add(oz2); loop_play(self, ph, 8.0); oz2.clear_updaters()

        # ---------------------------------------------------------- 6 strati: input IV vs I
        self.new(tr("Scales (3)", "Scale (3)"), tr("Where the synapse is decides the surface sign", "La posizione della sinapsi decide il segno"))
        f = F3.f06_layers(); fit(f, 0.85, np.array([-2.3, -0.5, 0]))
        for c_ in range(2):
            self.play(Create(f[f"surf{c_}"]), *[Create(f[f"p{c_}{k}"]) for k in range(3)], FadeIn(f[f"lab{c_}"]), run_time=1.0)
            self.play(GrowArrow(f[f"inp{c_}"]))
            self.play(FadeIn(f[f"sink{c_}"], scale=1.5), FadeIn(f[f"src{c_}"], scale=1.5), FadeIn(f[f"el{c_}"]))
        bl = bullets([tr("*Thalamic* input, ++layer IV++ → surface ~positive~.", "Input *talamico*, ++strato IV++ → superficie ~positiva~."),
                      tr("*Cortico-cortical*, ++layer I++ → surface ~negative~.", "*Cortico-corticale*, ++strato I++ → superficie ~negativa~."),
                      tr("Polarity tells ++where++, not ++what++.", "La polarità dice ++dove++, non ++che cosa++.")], 19, n=30, gap=0.35).move_to(np.array([4.7, 0.0, 0]))
        for b_ in bl: self.play(FadeIn(b_))
        # loop: corrente extracellulare dalla sorgente al pozzo, in entrambe le colonne
        streams = []
        for c_ in range(2):
            a = f[f"src{c_}"].get_center(); b = f[f"sink{c_}"].get_center()
            for off in (0.25, 0.55):
                streams.append((polyline(a, a + RIGHT * off, b + RIGHT * off, b), 2, AMB, 0.05))
        loop_packets(self, streams, T=2.0)

        # ---------------------------------------------------------- 7 sezione
        self.new(); section_title(self, 2, tr("The current dipole", "Il dipolo di corrente"))

        # ---------------------------------------------------------- 8 dipolo: campo che ruota
        self.new(tr("Dipole (1)", "Dipolo (1)"), tr("The current dipole: the atom of the EEG", "Il dipolo di corrente: l'atomo dell'EEG"))
        Wp, Hp = 6.0, 4.2; cen = np.array([-3.2, -0.5, 0])
        ang = ValueTracker(0.0)

        def plane():
            a = ang.get_value(); n = 180
            xs = np.linspace(-Wp / 2, Wp / 2, n); ys = np.linspace(-Hp / 2, Hp / 2, int(n * Hp / Wp))
            X, Y = np.meshgrid(xs, ys[::-1])
            u = np.array([np.sin(a), np.cos(a)]); d = 0.25
            r1 = np.hypot(X - d * u[0], Y - d * u[1]) + 0.08; r2 = np.hypot(X + d * u[0], Y + d * u[1]) + 0.08
            V = 1 / r1 - 1 / r2
            rgb = E.cmap_rdbu(np.tanh(V / (0.2 * np.abs(V).max())))
            img = ImageMobject((np.dstack([rgb, np.ones_like(V)]) * 255).astype(np.uint8)); img.height = Hp; img.move_to(cen)
            arr = Arrow(cen - 0.5 * np.array([u[0], u[1], 0]), cen + 0.5 * np.array([u[0], u[1], 0]), buff=0, color="#16213A", stroke_width=7, tip_length=0.2)
            return Group(img, arr, Rectangle(width=Wp, height=Hp, color=MUT, stroke_width=2).move_to(cen))
        pz = redraw(plane)
        self.play(FadeIn(pz))
        bl = bullets([tr("Sink + source at distance d, current I: *dipole* p = I·d.", "Pozzo + sorgente a distanza d, corrente I: *dipolo* p = I·d."),
                      tr("~Red~ in front, ~blue~ behind, zero on the \"equator\".", "~Rosso~ davanti, ~blu~ dietro, zero sull'\"equatore\"."),
                      tr("Amplitude falls as ++1/r²++.", "L'ampiezza decade come ++1/r²++.")], 19, n=32, gap=0.3).move_to(np.array([3.6, 1.1, 0]))
        eq = fcard(r"V(r,\theta) = \frac{p\cos\theta}{4\pi\sigma r^2}", CARD2, 0.9).move_to(np.array([3.6, -1.6, 0]))
        for b_ in bl: self.play(FadeIn(b_))
        self.play(FadeIn(eq[0]), Write(eq[1]))
        pz.clear_updaters()
        loop_start(self)
        ph = ValueTracker(0.0)
        self.remove(pz)
        pz2 = redraw(lambda: (ang.set_value(2 * PI * ph.get_value()), plane())[1])
        self.add(pz2); loop_play(self, ph, 6.0); pz2.clear_updaters()

        # ---------------------------------------------------------- 9 mappe: il dipolo viaggia radiale -> tangenziale -> profondo
        self.new(tr("Dipole (2)", "Dipolo (2)"), tr("One dipole, different scalp maps", "Un dipolo, mappe di scalpo diverse"))
        f = F3.f08_maps(1.05); fit(f, 1.0, np.array([0, 0.9, 0]))
        for k in range(3):
            self.play(FadeIn(f[f"m{k}"]), FadeIn(f[f"o{k}"]), FadeIn(f[f"l{k}"]), run_time=0.8)
        bl = bullets([tr("*Radial*: one extremum above the source.", "*Radiale*: un estremo sopra la sorgente."),
                      tr("*Tangential*: a +/− pair; the source is ++between++ the poles!", "*Tangenziale*: una coppia +/−; la sorgente è ++tra++ i poli!"),
                      tr("*Deep*: wider and weaker.", "*Profondo*: più larga e più debole.")], 20, n=70, gap=0.25).to_edge(DOWN, buff=0.7).to_edge(LEFT, buff=1.0)
        for b_ in bl: self.play(FadeIn(b_))

        # ---------------------------------------------------------- 10 sezione
        self.new(); section_title(self, 3, tr("Volume conduction and head models", "Conduzione di volume e modelli di testa"))

        # ---------------------------------------------------------- 11 strati della testa + effetto del cranio
        self.new(tr("Volume conduction (1)", "Conduzione di volume (1)"), tr("The head is a layered conductor", "La testa è un conduttore a strati"))
        f = F3.f10_head(1.6); fit(f, 0.9, np.array([-2.6, 0.3, 0]))
        for k in range(4):
            self.play(GrowFromCenter(f[f"c{k}"]), FadeIn(f[f"t{k}"]), run_time=0.6)
        cm = np.array([4.9, 0.6, 0]); Rm = 1.2
        bl_ = ValueTracker(0.0)
        mz = redraw(lambda: Group(*E.topomap(*E.dipole_map([0.0, 0.1, 0.8], [0.2, 0, 1], n=101, blur=bl_.get_value()), cm, Rm)))
        lab = always_redraw(lambda: T(tr("skull blur", "sfocatura del cranio") + f": {bl_.get_value():.2f}", 16, MUT).next_to(cm + DOWN * Rm, DOWN, buff=0.2))
        self.play(FadeIn(mz), FadeIn(lab))
        self.play(bl_.animate.set_value(0.35), run_time=2.5)
        mz.clear_updaters(); lab.clear_updaters()
        mt = metaphor(tr("the skull is ++frosted glass++: the light passes, its shape is lost.", "il cranio è un ++vetro smerigliato++: la luce passa, la forma si perde."), 18, 100).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(mt))
        loop_start(self)
        ph = ValueTracker(0.0)
        self.remove(mz, lab)
        mz2 = redraw(lambda: (bl_.set_value(0.175 + 0.175 * np.cos(2 * np.pi * ph.get_value())), Group(*E.topomap(*E.dipole_map([0.0, 0.1, 0.8], [0.2, 0, 1], n=101, blur=bl_.get_value()), cm, Rm)))[1])
        lab2 = always_redraw(lambda: T(tr("skull blur", "sfocatura del cranio") + f": {bl_.get_value():.2f}", 16, MUT).next_to(cm + DOWN * Rm, DOWN, buff=0.2))
        self.add(mz2, lab2); loop_play(self, ph, 5.0); mz2.clear_updaters(); lab2.clear_updaters()

        # ---------------------------------------------------------- 12 lead field: V = L j dal vivo
        self.new(tr("Volume conduction (2)", "Conduzione di volume (2)"), tr("The lead field: V = L · j", "Il lead field: V = L · j"))
        f = F3.f11_leadfield(); fit(f, 1.15, np.array([-2.6, 0.2, 0]))
        self.play(FadeIn(f["L"], lag_ratio=0.01), FadeIn(f["lL"]), run_time=1.5)
        self.play(FadeIn(f["j"]), FadeIn(f["lj"]), FadeIn(f["dot"]))
        self.play(FadeIn(f["V"]), FadeIn(f["lV"]), FadeIn(f["eq"]))
        bl = bullets([tr("Each electrode = ++weighted sum++ of all sources.", "Ogni elettrodo = ++somma pesata++ di tutte le sorgenti."),
                      tr("L depends only on ++geometry and conductivities++.", "L dipende solo da ++geometria e conducibilità++."),
                      tr("Spheres → BEM → FEM (individual MRI).", "Sfere → BEM → FEM (RM individuale)."),
                      tr("Nearby channels are ++correlated++ anyway.", "Canali vicini sono comunque ++correlati++.")], 19, n=30, gap=0.3).move_to(np.array([4.6, 0.1, 0]))
        for b_ in bl: self.play(FadeIn(b_))
        rng = np.random.default_rng(3)
        Lnum = np.tanh(rng.normal(size=(8, 14)))
        jcells = list(f["j"]); vcells = list(f["V"])
        loop_start(self)
        ph = ValueTracker(0.0)

        def live():
            u = ph.get_value(); g = VGroup()
            pos = 13 * (0.5 - 0.5 * np.cos(2 * np.pi * u))
            j = np.exp(-0.5 * ((np.arange(14) - pos) / 1.2) ** 2)
            v = Lnum @ j; v = v / 3.0
            for k, c in enumerate(jcells):
                g.add(c.copy().set_fill(ACC, opacity=0.1 + 0.85 * j[k]))
            for k, c in enumerate(vcells):
                g.add(c.copy().set_fill(F3.rgb_to_hex_(E.cmap_rdbu(np.array(np.tanh(v[k])))), opacity=1))
            return g
        self.remove(f["j"], f["V"])
        lz = always_redraw(live); self.add(lz); loop_play(self, ph, 6.0); lz.clear_updaters()

        # ---------------------------------------------------------- 13 montaggi (tracce che scorrono)
        self.new(tr("Recording geometry", "Geometria di registrazione"), tr("Referential vs bipolar montages", "Montaggi referenziali e bipolari"))
        f = F3.f13_montage(4.4); fit(f, 1.05, np.array([-1.8, 0.1, 0]))
        self.play(FadeIn(f["head"]), FadeIn(f["img"]), FadeIn(f["o"]), *[FadeIn(f[f"e{k}"]) for k in range(3)])
        self.play(FadeIn(f["tu"]), *[FadeIn(f[f"u{k}"]) for k in range(3)])
        self.play(FadeIn(f["tb"]), *[FadeIn(f[f"b{k}"]) for k in range(2)])
        bl = bullets([tr("*Referential*: vs a common reference.", "*Referenziale*: contro un riferimento comune."),
                      tr("*Bipolar*: neighbour differences → common activity cancels.", "*Bipolare*: differenze tra vicini → l'attività comune si annulla."),
                      tr("No montage is \"true\": different ++views++.", "Nessun montaggio è \"vero\": ++viste++ diverse.")], 18, n=26, gap=0.3).move_to(np.array([5.0, 0.0, 0]))
        for b_ in bl: self.play(FadeIn(b_))
        t, x = E.periodic_eeg(2.0, seed=5, peaks=((10, 1, 1.5),), uv=30)
        common = 0.5 * E.periodic_eeg(2.0, seed=9, peaks=((1.5, 0.5, 2),), uv=30)[1]
        amps = {"F3": 0.6, "C3": 1.0, "P3": 0.8}
        sig = {n: amps[n] * x + common for n in amps}
        tr_u = [f[f"u{k}"][1] for k in range(3)]; tr_b = [f[f"b{k}"][1] for k in range(2)]
        Os = [m.get_left() for m in tr_u + tr_b]
        Wd = tr_u[0].get_width(); hh = 0.006 * 1.05
        sigs = [(t, sig["F3"]), (t, sig["C3"]), (t, sig["P3"]), (t, sig["F3"] - sig["C3"]), (t, sig["C3"] - sig["P3"])]
        Os = [np.array([o[0], m.get_center()[1], 0]) for o, m in zip(Os, tr_u + tr_b)]
        scroll_group(self, sigs, Os, Wd, hh, 2.0, [TEAL] * 3 + [ACC] * 2, 4.0, sw=1.8, old=VGroup(*tr_u, *tr_b))
        self.end()
