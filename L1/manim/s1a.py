from base import *
import figs1 as F1

PURP = "#8E7CC3"; GRN = "#6FCF97"


def rows_mob(items, size=21, n=70, w=12.2, h=0.78, gap=0.16, col=TEAL):
    g = VGroup()
    for i, s in enumerate(items):
        box = RoundedRectangle(corner_radius=0.12, width=w, height=h, fill_color=CARD if i % 2 == 0 else CARD2, fill_opacity=1, stroke_width=0)
        b = VGroup(Circle(0.21, color=col, fill_opacity=1, stroke_width=0), TX(str(i + 1), font=BODY, font_size=17, color=WHITE, weight=BOLD))
        r = VGroup(b, T(s, size, n=n)).arrange(RIGHT, buff=0.3).move_to(box).align_to(box, LEFT).shift(RIGHT * 0.2)
        g.add(VGroup(box, r))
    g.arrange(DOWN, buff=gap)
    return g


def metaphor(s, size=19, n=100):
    return card(T("~" + tr("Metaphor", "Metafora") + "~  " + s, size, n=n), CARD2)


def scroll_loop(self, sig, O, w, h, win, col=TEAL, sw=2.5, T_=None, old=None, extra=None):
    """EEG che scorre in modo periodico (loop senza scatti)."""
    t, x = sig
    D = t[-1] + (t[1] - t[0])
    loop_start(self)
    ph = ValueTracker(0.0)
    live = always_redraw(lambda: E.window_trace(t, x, ph.get_value() * D, win, O, w, h, col, sw))
    if old is not None: self.remove(old)
    self.add(live)
    loop_play(self, ph, T_ or D)
    live.clear_updaters()
    return live


class A1_Storia(Base):
    start_num = 1

    def construct(self):
        # ---------------------------------------------------------- 1 copertina
        self.new(first=True); self.num = 1
        sigs = [E.periodic_eeg(4.0, seed=30 + k, peaks=((10, 1.2, 1.2 if k > 2 else 0.4),)) for k in range(6)]
        cols = [TEAL, ACC, TEAL, AMB, TEAL, ACC]
        Os = [np.array([2.6, -0.75 - 0.42 * k, 0]) for k in range(6)]

        def vis():
            tr0 = VGroup(*[E.window_trace(*sigs[k], 0.0, 2.0, Os[k], 3.9, 0.005, cols[k], 2) for k in range(6)])
            self.play(LaggedStart(*[Create(m) for m in tr0], lag_ratio=0.15), run_time=2)
            self.tr0 = tr0
        copertina(self, tr("Lecture 1", "Lezione 1"), tr("What is EEG?\nHistory and physical basis", "Che cos'è l'EEG?\nStoria e basi fisiche"), vis)
        loop_start(self)
        ph = ValueTracker(0.0)
        live = always_redraw(lambda: VGroup(*[E.window_trace(*sigs[k], ph.get_value() * 4.0, 2.0, Os[k], 3.9, 0.005, cols[k], 2) for k in range(6)]))
        self.remove(self.tr0); self.add(live)
        loop_play(self, ph, 4.0); live.clear_updaters()

        # ---------------------------------------------------------- 2 mappa del corso
        self.new(tr("Course map", "Mappa del corso"), tr("Brain Imaging – EEG: 10 lectures, 20 hours", "Brain Imaging – EEG: 10 lezioni, 20 ore"))
        v = [tr("What is EEG? History and physical basis", "Che cos'è l'EEG? Storia e basi fisiche"), tr("Cellular bases of EEG", "Basi cellulari dell'EEG"),
             tr("From neurons to scalp: dipoles, rhythms", "Dai neuroni allo scalpo: dipoli, ritmi"), tr("Recording: 10-20, montages, artifacts", "Registrazione: 10-20, montaggi, artefatti"),
             tr("Preprocessing and ICA", "Preprocessing e ICA"), tr("Spectral and time-frequency analysis", "Analisi spettrale e tempo-frequenza"),
             tr("Event-related potentials (ERPs)", "Potenziali evento-correlati (ERP)"), tr("Spatial analysis and microstates", "Analisi spaziale e microstati"),
             tr("Source imaging and connectivity", "Source imaging e connettività"), tr("Decoding (MVPA) and applications", "Decoding (MVPA) e applicazioni")]
        cards = VGroup()
        for i, s in enumerate(v):
            col = TEAL if i < 3 else (PURP if i < 5 else ACC)
            box = RoundedRectangle(corner_radius=0.12, width=6.0, height=0.82, fill_color=CARD2 if i == 0 else CARD, fill_opacity=1, stroke_width=0)
            b = VGroup(Circle(0.22, color=col, fill_opacity=1, stroke_width=0), TX(str(i + 1), font=BODY, font_size=17, color=WHITE, weight=BOLD))
            r = VGroup(b, T(("**" + s + "**") if i == 0 else s, 19, n=44)).arrange(RIGHT, buff=0.28).move_to(box).align_to(box, LEFT).shift(RIGHT * 0.18)
            cards.add(VGroup(box, r).move_to(np.array([-3.2 + 6.4 * (i // 5), 1.75 - 0.98 * (i % 5), 0])))
        self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.15) for c_ in cards], lag_ratio=0.1), run_time=2.5)
        leg = T(tr("~physiology~ (1–3) → ~measurement~ (4–5) → ~analysis~ (6–10)", "~fisiologia~ (1–3) → ~misura~ (4–5) → ~analisi~ (6–10)"), 20, n=90).to_edge(DOWN, buff=0.75)
        self.play(FadeIn(leg))
        self.play(Indicate(cards[0], scale_factor=1.04))

        # ---------------------------------------------------------- 3 obiettivi
        self.new(tr("Today", "Oggi"), tr("Learning objectives", "Obiettivi di apprendimento"))
        g = rows_mob([tr("Place EEG in the landscape of ++brain imaging methods++.", "Collocare l'EEG tra i ++metodi di brain imaging++."),
                      tr("Know the ++key historical steps++, from Galvani to decoding.", "Conoscere le ++tappe storiche++, da Galvani al decoding."),
                      tr("Explain *what* EEG measures: ++synchronous postsynaptic currents++.", "Spiegare *che cosa* misura l'EEG: ++correnti postsinaptiche sincrone++."),
                      tr("Understand the ++three requirements++ and ++volume conduction++.", "Capire i ++tre requisiti++ e la ++conduzione di volume++."),
                      tr("Preview the ++analysis families++ of the course.", "Anteprima delle ++famiglie di analisi++ del corso.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 4 motivazione + metafora dello stadio
        self.new(tr("Motivation", "Motivazione"), tr("Why listen to the brain's electricity?", "Perché ascoltare l'elettricità del cervello?"))
        nums = [("86 × 10⁹", tr("neurons", "neuroni")), ("≈10¹⁴", tr("synapses", "sinapsi")), ("≈20 %", tr("of resting energy", "dell'energia a riposo")), ("1 ms", tr("neural time scale", "scala temporale neurale"))]
        nc = VGroup()
        for i, (a, b) in enumerate(nums):
            box = RoundedRectangle(corner_radius=0.14, width=2.8, height=1.5, fill_color=CARD if i % 2 == 0 else CARD2, fill_opacity=1, stroke_width=0)
            nc.add(VGroup(box, VGroup(TX(a, font=SERIF_F, font_size=40, color=TEAL if i % 2 == 0 else ACC, weight=BOLD), T(b, 18, MUT, n=26)).arrange(DOWN, buff=0.1).move_to(box)))
        nc.arrange(RIGHT, buff=0.3).shift(UP * 1.3)
        self.play(LaggedStart(*[FadeIn(c_, scale=0.9) for c_ in nc], lag_ratio=0.2), run_time=1.8)
        mt = metaphor(tr("the EEG is a set of microphones ++outside a stadium++: single conversations are lost, but ++a chant sung together++ is heard far away.",
                         "l'EEG è un insieme di microfoni ++fuori da uno stadio++: le singole conversazioni si perdono, ma ++un coro cantato insieme++ si sente da lontano."), 19, 100).to_edge(DOWN, buff=0.7)
        # stadio: 12x6 "tifosi" con fase casuale -> sincronizzazione
        rng = np.random.default_rng(4)
        ph0 = rng.uniform(0, 2 * np.pi, 72)
        sync = ValueTracker(0.0); tt = ValueTracker(0.0)
        cen = np.array([-2.6, -1.05, 0])

        def fans():
            s_ = sync.get_value(); g_ = VGroup()
            phs = (1 - s_) * ph0
            for k in range(72):
                v_ = 0.5 + 0.5 * np.sin(2 * np.pi * 1.0 * tt.get_value() + phs[k])
                g_.add(Dot(cen + np.array([(k % 12) * 0.32 - 1.8, (k // 12) * 0.22 - 0.55, 0]), radius=0.07, color=interpolate_color(ManimColor(CARD2), ManimColor(AMB), v_)))
            return g_

        def meter():
            s_ = sync.get_value(); phs = (1 - s_) * ph0
            amp = abs(np.sum(np.exp(1j * (2 * np.pi * tt.get_value() + phs)))) / 72
            base = np.array([2.2, -1.65, 0])
            return VGroup(Rectangle(width=0.5, height=1.4, color=MUT, stroke_width=2).move_to(base + UP * 0.7),
                          bar(1.4 * amp, ACC, base, w=0.5, op=0.9),
                          T(tr("microphone", "microfono"), 16, MUT).next_to(base, DOWN, buff=0.12))
        fz = always_redraw(fans); mz = always_redraw(meter)
        self.play(FadeIn(fz), FadeIn(mz), FadeIn(mt))
        self.play(tt.animate.set_value(2.0), run_time=2.0, rate_func=linear)
        lab = T(tr("in phase", "in fase"), 20, ACC).move_to(np.array([2.2, 0.15, 0]))
        self.play(sync.animate.set_value(1.0), tt.animate.set_value(4.0), FadeIn(lab), run_time=2.0, rate_func=linear)
        fz.clear_updaters(); mz.clear_updaters()
        loop_start(self)
        tt.set_value(0.0)
        self.remove(fz, mz); fz = always_redraw(fans); mz = always_redraw(meter); self.add(fz, mz)
        loop_play(self, tt, 2.0)
        fz.clear_updaters(); mz.clear_updaters()

        # ---------------------------------------------------------- 5 paesaggio del brain imaging
        self.new(tr("Brain imaging landscape", "Il paesaggio del brain imaging"), tr("Where does EEG sit? Space vs time", "Dove si colloca l'EEG? Spazio e tempo"))
        f = F1.f05_resolution(); fit(f, 0.95, np.array([-2.6, -0.55, 0]))
        keys = [k for k in f.keys() if not k.startswith(("EEG", "fNIRS", "fMRI", "PET", "ECoG", "LFP", "Single"))]
        self.play(*[FadeIn(f[k]) for k in keys])
        order = ["Single unit", "LFP", "ECoG", "fMRI", "PET", "fNIRS", "EEG / MEG"]
        for n_ in order:
            self.play(GrowFromCenter(f[n_]), FadeIn(f[n_ + "l"]), run_time=0.6)
        bl = bullets([tr("*EEG/MEG*: ++milliseconds++, but cm blur.", "*EEG/MEG*: ++millisecondi++, ma sfocatura di cm."),
                      tr("*fMRI*: mm, but ++seconds++.", "*fMRI*: mm, ma ++secondi++."),
                      tr("*Invasive*: sharp and fast, but surgery.", "*Invasivi*: precisi e veloci, ma chirurgia."),
                      tr("~No single method sees everything~ → multimodal imaging.", "~Nessun metodo vede tutto~ → imaging multimodale.")], 20, n=30, gap=0.35).move_to(np.array([4.4, -0.3, 0]))
        self.play(Indicate(f["EEG / MEG"], scale_factor=1.05), FadeIn(bl[0]))
        for b_ in bl[1:]: self.play(FadeIn(b_))

        # ---------------------------------------------------------- 6 diretto vs indiretto
        self.new(tr("Brain imaging landscape (2)", "Il paesaggio del brain imaging (2)"), tr("Direct (electrical) vs indirect (hemodynamic)", "Diretto (elettrico) vs indiretto (emodinamico)"))
        f = F1.f06_eeg_vs_bold(7.2); fit(f, 0.88, np.array([-2.4, -0.2, 0]))
        self.play(FadeIn(VGroup(*[f[k] for k in f if k.startswith(("b", "t", "l0"))])), Create(f["s0"]))
        self.play(FadeIn(f["l1"]), Create(f["s1"]), run_time=1.0)
        self.play(FadeIn(f["l2"]), Create(f["s2"]), run_time=2.5)
        bl = bullets([tr("EEG: ++electric field++ of neuronal currents, no delay.", "EEG: ++campo elettrico++ delle correnti neuronali, nessun ritardo."),
                      tr("BOLD/fNIRS: ++blood oxygenation++ via *neurovascular coupling*, peak ≈5 s later.", "BOLD/fNIRS: ++ossigenazione++ via *accoppiamento neurovascolare*, picco ≈5 s dopo."),
                      tr("Two events 200 ms apart: ~distinct~ in EEG, ~merged~ in BOLD.", "Due eventi a 200 ms: ~distinti~ nell'EEG, ~fusi~ nel BOLD.")], 19, n=30, gap=0.35).move_to(np.array([4.6, 0.2, 0]))
        for b_ in bl: self.play(FadeIn(b_))
        mt = metaphor(tr("EEG hears the ++thunder++ as it happens; fMRI sees the ++puddles++ afterwards.", "L'EEG sente il ++tuono++ mentre avviene; la fMRI vede le ++pozzanghere++ dopo."), 18, 100).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(mt))
        # loop: cursore temporale che scorre sui tre segnali
        x0 = f["b0"].get_start()[0]; x1 = f["b0"].get_end()[0]; ytop = f["l0"].get_top()[1]; ybot = f["b2"].get_start()[1] - 0.1
        loop_start(self)
        ph = ValueTracker(0.0)
        cur = always_redraw(lambda: DashedLine(np.array([x0 + (x1 - x0) * ph.get_value(), ytop, 0]), np.array([x0 + (x1 - x0) * ph.get_value(), ybot, 0]), color=AMB, stroke_width=2))
        self.add(cur); loop_play(self, ph, 5.0); cur.clear_updaters()

        # ---------------------------------------------------------- 7 sezione storia
        self.new()
        self.section(1, tr("A short history of EEG", "Breve storia dell'EEG"))

        # ---------------------------------------------------------- 8 Galvani
        self.new(tr("History (1)", "Storia (1)"), tr("Galvani and \"animal electricity\" (1791)", "Galvani e l'«elettricità animale» (1791)"))
        bl = bullets([tr("Bologna, 1780s: an arc of ++two different metals++ touching nerve and muscle makes a frog leg ~twitch~.", "Bologna, anni '80 del '700: un arco di ++due metalli diversi++ che tocca nervo e muscolo fa ~contrarre~ la zampa di rana."),
                      tr("Galvani: tissues produce their own *animal electricity*.", "Galvani: i tessuti producono una propria *elettricità animale*."),
                      tr("Volta: the current comes from the metals → the ++battery++ (1800).", "Volta: la corrente viene dai metalli → la ++pila++ (1800)."),
                      tr("~Both partly right~: birth of ++electrophysiology++.", "~Entrambi in parte nel giusto~: nasce l'++elettrofisiologia++.")], 20, n=40, gap=0.35).to_edge(LEFT, buff=0.8).to_edge(UP, buff=1.9)
        f = F1.f08_galvani(); fit(f, 0.85, np.array([4.0, -0.3, 0]))
        self.play(FadeIn(bl[0]), FadeIn(VGroup(f["mus"], f["tend"], f["nerve"], f["ln"], f["lm"])))
        arc = f["arc"]
        self.play(Create(arc), FadeIn(f["cu"]), FadeIn(f["zn"]))

        def twitch():
            self.play(f["mus"].animate.stretch(0.8, 0).stretch(1.3, 1), Flash(arc.get_start(), color=AMB, line_length=0.2), run_time=0.35)
            self.play(f["mus"].animate.stretch(1 / 0.8, 0).stretch(1 / 1.3, 1), run_time=0.45)
        twitch()
        for b_ in bl[1:]: self.play(FadeIn(b_))
        loop_start(self)
        ph = ValueTracker(0.0)
        m0 = f["mus"].copy(); self.remove(f["mus"])
        sq = lambda u: max(0.0, np.sin(2 * np.pi * u)) ** 2
        mm = always_redraw(lambda: m0.copy().stretch(1 - 0.2 * sq(ph.get_value()), 0).stretch(1 + 0.3 * sq(ph.get_value()), 1))
        spark = always_redraw(lambda: Dot(arc.get_start(), radius=0.12 * sq(ph.get_value() + 0.05) + 0.001, color=AMB))
        self.add(mm, spark); loop_play(self, ph, 1.6); mm.clear_updaters(); spark.clear_updaters()

        # ---------------------------------------------------------- 9 dal nervo al cervello
        self.new(tr("History (2)", "Storia (2)"), tr("From nerves to the brain (1840–1913)", "Dal nervo al cervello (1840–1913)"))
        ev = [("1840s", tr("du Bois-Reymond: the nerve impulse is an electrical \"action current\"", "du Bois-Reymond: l'impulso nervoso è una \"corrente d'azione\"")),
              ("1850", tr("Helmholtz: conduction velocity ≈25–40 m/s in the frog", "Helmholtz: velocità di conduzione ≈25–40 m/s nella rana")),
              ("1870", tr("Fritsch & Hitzig: the cortex is electrically excitable", "Fritsch & Hitzig: la corteccia è eccitabile elettricamente")),
              ("1875", tr("Caton: spontaneous currents from exposed animal cortex", "Caton: correnti spontanee dalla corteccia esposta di animali")),
              ("1890", tr("Beck: sensory stimuli suppress brain oscillations", "Beck: gli stimoli sensoriali sopprimono le oscillazioni")),
              ("1913", tr("Pravdich-Neminsky: first \"electrocerebrogram\" (dog)", "Pravdich-Neminsky: primo \"elettrocerebrogramma\" (cane)"))]
        axl = Arrow(np.array([-6.2, 2.0, 0]), np.array([-6.2, -3.0, 0]), buff=0, color=MUT, stroke_width=3, tip_length=0.15)
        self.play(GrowArrow(axl))
        for i, (y_, d_) in enumerate(ev):
            yy = 1.75 - 0.82 * i
            g = VGroup(Dot(np.array([-6.2, yy, 0]), radius=0.08, color=ACC), TX(y_, font=SERIF_F, font_size=26, color=ACC, weight=BOLD).move_to(np.array([-5.2, yy, 0])),
                       T(d_, 21, n=80).move_to(np.array([0, yy, 0])).align_to(np.array([-4.3, 0, 0]), LEFT))
            self.play(FadeIn(g, shift=RIGHT * 0.2), run_time=0.7)

        # ---------------------------------------------------------- 10 Berger
        self.new(tr("History (3)", "Storia (3)"), tr("Hans Berger: the first human EEG (1924)", "Hans Berger: il primo EEG umano (1924)"))
        bl = bullets([tr("Jena, *6 July 1924*: first human EEG; published only in ++1929++.", "Jena, *6 luglio 1924*: primo EEG umano; pubblicato solo nel ++1929++."),
                      tr("~Alpha~ rhythm (≈10 Hz, eyes closed) and ~beta~ rhythm.", "Ritmo ~alfa~ (≈10 Hz, occhi chiusi) e ritmo ~beta~."),
                      tr("*Alpha blocking* when the eyes open: the \"Berger effect\".", "*Blocco dell'alfa* all'apertura degli occhi: l'«effetto Berger».")], 21, n=80, gap=0.3).to_edge(LEFT, buff=0.8).to_edge(UP, buff=1.9)
        self.play(FadeIn(bl[0])); self.play(FadeIn(bl[1]))
        # EEG in modalità "sweep": alfa a occhi chiusi, poi occhi aperti
        t = np.arange(0, 6, 1 / 250)
        xa = 0.5 * E.pink(len(t), 5) + 2.2 * np.sin(2 * np.pi * 10.2 * t) * (1 + 0.25 * np.sin(2 * np.pi * 0.5 * t))
        eo = 0.5 * E.pink(len(t), 6) + 0.35 * np.sin(2 * np.pi * 10.2 * t) + 0.5 * np.sin(2 * np.pi * 21 * t)
        O = np.array([-5.8, -1.5, 0]); Wd = 9.0
        eye = lambda open_: VGroup(Ellipse(width=0.9, height=0.45 if open_ else 0.06, color=FG, stroke_width=3),
                                   *([Dot(radius=0.12, color=TEAL)] if open_ else [])).move_to(np.array([5.2, -1.5, 0]))
        e0 = eye(False); lab = T(tr("eyes closed", "occhi chiusi"), 18, MUT).next_to(e0, DOWN, buff=0.25)
        tr1 = E.trace(t, xa, O, Wd, 0.22, TEAL, 2.2)
        self.play(FadeIn(e0), FadeIn(lab), Create(tr1), run_time=3, rate_func=linear)
        self.play(FadeIn(bl[2]))
        e1 = eye(True); lab1 = T(tr("eyes open", "occhi aperti"), 18, ACC).next_to(e1, DOWN, buff=0.25)
        tr2 = E.trace(t, eo, O + DOWN * 0.0, Wd, 0.22, ACC, 2.2)
        self.play(ReplacementTransform(e0, e1), ReplacementTransform(lab, lab1), FadeOut(tr1), Create(tr2), run_time=3, rate_func=linear)
        # loop: occhi che si chiudono e si aprono, tracciato che scorre (alfa quando chiusi)
        tp, xp = E.periodic_eeg(8.0, seed=7, peaks=((10.2, 0.5, 0.0),), uv=12)
        alpha_env = lambda s: 0.5 - 0.5 * np.cos(2 * np.pi * s / 8.0)       # 0 aperti -> 1 chiusi -> 0
        xloop = xp + 30 * alpha_env(tp) * np.sin(2 * np.pi * 10.0 * tp)
        loop_start(self)
        ph = ValueTracker(0.0)
        live = always_redraw(lambda: E.window_trace(tp, xloop, ph.get_value() * 8.0, 3.0, O, Wd, 0.014, interpolate_color(ManimColor(ACC), ManimColor(TEAL), alpha_env((ph.get_value() * 8.0 + 3.0) % 8.0)), 2.2))
        eyel = always_redraw(lambda: VGroup(Ellipse(width=0.9, height=0.06 + 0.39 * (1 - alpha_env((ph.get_value() * 8.0 + 3.0) % 8.0)), color=FG, stroke_width=3)).move_to(np.array([5.2, -1.5, 0])))
        self.remove(tr2, e1, lab1); self.add(live, eyel)
        loop_play(self, ph, 8.0); live.clear_updaters(); eyel.clear_updaters()

        # ---------------------------------------------------------- 11 clinica e calcolo
        self.new(tr("History (4)", "Storia (4)"), tr("From curiosity to clinic to computation", "Dalla curiosità alla clinica al calcolo"))
        ev = [(1934, tr("Adrian & Matthews confirm the Berger rhythm", "Adrian & Matthews confermano il ritmo di Berger")), (1935, tr("3 Hz spike-and-wave in absence epilepsy", "punta-onda 3 Hz nell'epilessia di assenza")),
              (1937, tr("EEG stages of sleep", "stadi EEG del sonno")), (1954, tr("averaging → evoked potentials", "media → potenziali evocati")),
              (1958, tr("10-20 electrode system", "sistema 10-20")), (1965, tr("P300; FFT algorithm", "P300; algoritmo FFT")),
              (1987, tr("EEG microstates", "microstati EEG")), (1996, tr("ICA for EEG", "ICA per l'EEG")),
              (2002, tr("brain-computer interfaces", "interfacce cervello-computer")), (2015, tr("machine learning, decoding", "machine learning, decoding"))]
        axl = Arrow(np.array([-6.3, -0.2, 0]), np.array([6.4, -0.2, 0]), buff=0, color=MUT, stroke_width=3, tip_length=0.18)
        self.play(GrowArrow(axl))
        for i, (y_, d_) in enumerate(ev):
            up = 1 if i % 2 == 0 else -1
            p = np.array([-5.6 + 1.25 * i, -0.2, 0])
            col = [TEAL, ACC, AMB][i // 4] if i < 8 else PURP
            g = VGroup(Dot(p, radius=0.08, color=col), Line(p, p + UP * 0.55 * up, color=col, stroke_width=2),
                       TX(str(y_), font=SERIF_F, font_size=22, color=col, weight=BOLD).move_to(p + UP * 0.8 * up),
                       T(d_, 15, FG, n=18).move_to(p + UP * (1.45 if up > 0 else -1.5)))
            self.play(FadeIn(g, shift=UP * 0.1 * up), run_time=0.5)
        self.end()

    def section(self, n, title):
        num = TX(f"{n:02d}", font=SERIF_F, font_size=110, color=ACC, weight=BOLD).to_edge(LEFT, buff=1.0).shift(UP * 0.6)
        ti = TX(title, font=SERIF_F, font_size=52, color=FG, weight=BOLD).next_to(num, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(FadeIn(num, shift=RIGHT * 0.3), Write(ti), run_time=1.2)
