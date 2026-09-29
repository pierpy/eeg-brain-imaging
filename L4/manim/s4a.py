from base import *
import figs4 as F4


def scroll_group(self, sigs, Os, W, h, win, cols, T_, sw=2.0, old=None, extra=()):
    """più tracce periodiche che scorrono insieme (loop senza scatti)."""
    D = sigs[0][0][-1] + (sigs[0][0][1] - sigs[0][0][0])
    loop_start(self)
    ph = ValueTracker(0.0)
    live = always_redraw(lambda: VGroup(*[E.window_trace(t, x, ph.get_value() * D, win, O, W, h, c, sw) for (t, x), O, c in zip(sigs, Os, cols)]))
    if old is not None:
        self.remove(old)
    self.add(live)
    loop_play(self, ph, T_, *extra)
    live.clear_updaters()
    return live


def sunflower(n, R):
    k = np.arange(n) + 0.5
    r = R * np.sqrt(k / n); a = k * np.pi * (3 - np.sqrt(5))
    return [np.array([r_ * np.sin(a_), r_ * np.cos(a_), 0]) for r_, a_ in zip(r, a)]


class A4_Catena(Base):
    start_num = 1

    def construct(self):
        # ---------------------------------------------------------- 1 copertina: tracce che scorrono da una testa
        self.new(first=True); self.num = 1
        hc = np.array([5.7, -2.35, 0]); Rh = 0.95
        sigs = [E.periodic_eeg(4.0, seed=s, peaks=((10.0, 1.0, 1.0 - 0.2 * k), (20.0, 2.0, 0.3)), uv=20) for k, s in enumerate((11, 12, 13))]
        Os = [np.array([2.0, -1.75 - 0.6 * k, 0]) for k in range(3)]
        cols = [TEAL, ACC, AMB]

        def vis():
            hd = VGroup(E.head(hc, Rh), E.electrodes(hc, Rh, r=0.04))
            tr0 = VGroup(*[E.window_trace(t, x, 0.0, 1.5, O, 2.6, 0.012, c, 1.8) for (t, x), O, c in zip(sigs, Os, cols)])
            self.play(FadeIn(hd), Create(tr0), run_time=1.2)
            self.tr0 = tr0
        copertina(self, tr("Lecture 4", "Lezione 4"), tr("Recording the EEG:\nelectrodes, signals, artifacts", "Registrare l'EEG:\nelettrodi, segnali, artefatti"), vis)
        scroll_group(self, sigs, Os, 2.6, 0.012, 1.5, cols, 4.0, 1.8, old=self.tr0)

        # ---------------------------------------------------------- 2 obiettivi
        self.new(tr("Lecture 4", "Lezione 4"), tr("Today: from the scalp to a clean data file", "Oggi: dallo scalpo a un file di dati pulito"))
        g = rows_mob([tr("The ++recording chain++: electrodes, amplifier, filters, ADC.", "La ++catena di registrazione++: elettrodi, amplificatore, filtri, ADC."),
                      tr("*Electrodes*, impedance and the ++10-20 system++.", "*Elettrodi*, impedenza e il ++sistema 10-20++."),
                      tr("*Differential amplification*, CMRR and the ++reference++ problem.", "*Amplificazione differenziale*, CMRR e il problema del ++riferimento++."),
                      tr("*Digitisation*: sampling, Nyquist, aliasing, resolution, filters.", "*Digitalizzazione*: campionamento, Nyquist, aliasing, risoluzione, filtri."),
                      tr("*Artifacts* and a ++good-practice++ checklist.", "*Artefatti* e una checklist di ++buona pratica++.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 3 catena: un "pacchetto" di segnale attraversa gli stadi
        self.new(tr("The recording chain", "La catena di registrazione"), tr("Five stages between the brain and your hard disk", "Cinque stadi tra il cervello e il disco"))
        f = F4.f03_chain(12.4)
        for m in f.values():
            m.shift(UP * 0.85)
        for k in range(5):
            anims = [FadeIn(f[f"b{k}"], shift=UP * 0.1), FadeIn(f[f"s{k}"])]
            if k < 4: anims.append(GrowArrow(f[f"a{k}"]))
            self.play(*anims, run_time=0.45)
        bl = bullets([tr("Signal of ++10–100 µV++: amplified ≈10⁴–10⁵ times without adding noise.", "Segnale di ++10–100 µV++: amplificato ≈10⁴–10⁵ volte senza aggiungere rumore."),
                      tr("Analog filters limit the band ++before++ sampling (anti-aliasing).", "I filtri analogici limitano la banda ++prima++ del campionamento (anti-aliasing)."),
                      tr("The ADC turns voltage into numbers: ++sampling rate++ and ++bit depth++.", "L'ADC trasforma la tensione in numeri: ++campionamento++ e ++bit++."),
                      tr("Triggers from the stimulus PC mark events (essential for ERPs).", "I trigger dal PC di stimolazione marcano gli eventi (essenziali per gli ERP).")], 18, n=80, gap=0.2).move_to(np.array([0, -1.35, 0]))
        mt = metaphor(tr("a ++hi-fi system++: a great speaker cannot fix a scratched record.", "un ++impianto hi-fi++: un ottimo altoparlante non ripara un disco graffiato."), 17).move_to(np.array([0, -3.05, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.5)
        self.play(FadeIn(mt))
        xs = [f[f"b{k}"].get_center()[0] for k in range(5)]
        yp = f["b0"].get_top()[1] + 0.35

        def packet(u):
            x0 = -6.4 + 12.8 * u
            amp = 0.07 if x0 < xs[1] else 0.28
            noisy = x0 < xs[2]
            ss = np.linspace(-0.45, 0.45, 90)
            rng = np.random.default_rng(3)
            nz = rng.normal(size=len(ss)) * (0.35 if noisy else 0.0)
            y = amp * (np.sin(2 * np.pi * 2.2 * ss / 0.9) + nz) * np.exp(-(ss / 0.35) ** 2)
            if x0 < xs[3]:
                return VMobject(color=AMB, stroke_width=3).set_points_as_corners([np.array([x0 + a, yp + b, 0]) for a, b in zip(ss, y)])
            idx = np.arange(0, len(ss), 6)
            return VGroup(*[Dot(np.array([x0 + ss[i], yp + y[i], 0]), radius=0.045, color=AMB) for i in idx])
        loop_start(self)
        ph = ValueTracker(0.0)
        pk = always_redraw(lambda: packet(ph.get_value()))
        self.add(pk); loop_play(self, ph, 5.0); pk.clear_updaters()

        # ---------------------------------------------------------- 4 sezione
        self.new(); section_title(self, 1, tr("Electrodes and montage", "Elettrodi e montaggio"))

        # ---------------------------------------------------------- 5 tipi di elettrodi
        self.new(tr("Electrodes (1)", "Elettrodi (1)"), tr("Types of electrodes", "Tipi di elettrodi"))
        kinds = [(tr("Wet (gel) Ag/AgCl", "Umidi (gel) Ag/AgCl"), tr("gold standard; stable, non-polarisable; low impedance; slow set-up", "gold standard; stabili, non polarizzabili; bassa impedenza; montaggio lento")),
                 (tr("Saline / sponge", "Salini / spugna"), tr("fast set-up (HydroCel); dry out in ≈1 h", "montaggio rapido (HydroCel); si asciugano in ≈1 h")),
                 (tr("Dry", "Secchi"), tr("no gel, wearable/BCI; higher impedance, motion-sensitive", "senza gel, indossabili/BCI; impedenza alta, sensibili al movimento")),
                 (tr("Active", "Attivi"), tr("pre-amplifier at the electrode: less cable noise, tolerate higher impedance", "pre-amplificatore sull'elettrodo: meno rumore dai cavi, tollerano impedenze più alte"))]
        cards = VGroup()
        for k, (h_, d_) in enumerate(kinds):
            box = RoundedRectangle(corner_radius=0.14, width=6.1, height=1.55, fill_color=CARD if k in (0, 3) else CARD2, fill_opacity=1, stroke_width=0)
            tx = VGroup(TX(h_, font=BODY, font_size=22, color=TEAL, weight=BOLD), T(d_, 18, n=58)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            tx.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.3)
            cards.add(VGroup(box, tx))
        cards.arrange_in_grid(2, 2, buff=(0.3, 0.3)).move_to(np.array([0, 0.45, 0]))
        for c_ in cards: self.play(FadeIn(c_, shift=UP * 0.15), run_time=0.5)
        nt = card(T(tr("The electrode–gel–skin interface is an ++electrochemical junction++: it generates a DC potential that drifts with sweat and movement.", "L'interfaccia elettrodo–gel–pelle è una ++giunzione elettrochimica++: genera un potenziale DC che deriva con sudore e movimento."), 18, n=100))
        nt.move_to(np.array([0, -2.35, 0]))
        self.play(FadeIn(nt))

        # ---------------------------------------------------------- 6 impedenza: bassa vs alta (tracce che scorrono)
        self.new(tr("Electrodes (2)", "Elettrodi (2)"), tr("Impedance: keep it low and balanced", "Impedenza: bassa e bilanciata"))
        bl = bullets([tr("*Impedance* (Ω): opposition of the electrode–skin junction to AC current.", "*Impedenza* (Ω): opposizione della giunzione elettrodo–pelle alla corrente alternata."),
                      tr("Targets: ++< 5–10 kΩ++ (passive); ++< 25–50 kΩ++ (active).", "Obiettivi: ++< 5–10 kΩ++ (passivi); ++< 25–50 kΩ++ (attivi)."),
                      tr("High Z → ++skin potentials++, ++line noise++, ++drifts++ → less power (Kappenman & Luck, 2010).", "Z alta → ++potenziali cutanei++, ++rete++, ++derive++ → meno potenza (Kappenman & Luck, 2010)."),
                      tr("~Balanced~ impedances improve common-mode rejection.", "Impedenze ~bilanciate~ migliorano la reiezione di modo comune."),
                      tr("Abrasion, alcohol, enough gel — ++no bridges++!", "Abrasione, alcol, gel sufficiente — ++niente ponti++!")], 18, n=42, gap=0.24).to_edge(LEFT, buff=0.6).shift(DOWN * 0.35)
        for b_ in bl: self.play(FadeIn(b_), run_time=0.45)
        D = 4.0; fs = 500
        t, clean = E.periodic_eeg(D, fs=fs, seed=21, peaks=((10.0, 1.0, 1.0),), uv=20)
        noisy = clean + 14 * np.sin(2 * np.pi * 50 * t) + 30 * np.sin(2 * np.pi * t / D) + 12 * np.sin(2 * np.pi * 3 * t / D + 1)
        Wt = 5.2; x0 = 1.2
        Os = [np.array([x0, 1.0, 0]), np.array([x0, -1.6, 0])]
        lab = VGroup(T(tr("~5 kΩ~: clean", "~5 kΩ~: pulito"), 18).move_to(np.array([x0 + Wt / 2, 1.95, 0])),
                     T(tr("*50 kΩ*: drifts + 50 Hz", "*50 kΩ*: derive + 50 Hz"), 18).move_to(np.array([x0 + Wt / 2, -0.55, 0])))
        tr0 = VGroup(E.window_trace(t, clean, 0.0, 1.0, Os[0], Wt, 0.012, TEAL, 1.8), E.window_trace(t, noisy, 0.0, 1.0, Os[1], Wt, 0.012, ACC, 1.8))
        self.play(FadeIn(lab), Create(tr0), run_time=1.0)
        mt = metaphor(tr("the gel is a ++bridge++: too little and the road is bumpy; too much and it floods the neighbour's road.", "il gel è un ++ponte++: troppo poco e la strada è dissestata; troppo e allaga la strada del vicino."), 16, n=110).move_to(np.array([0, -3.05, 0]))
        self.play(FadeIn(mt))
        scroll_group(self, [(t, clean), (t, noisy)], Os, Wt, 0.012, 1.0, [TEAL, ACC], 4.0, 1.8, old=tr0)

        # ---------------------------------------------------------- 7 sistema 10-20
        self.new(tr("Electrodes (3)", "Elettrodi (3)"), tr("The international 10-20 system", "Il sistema internazionale 10-20"))
        f = F4.f06_1020(1.9); fit(f, 0.82, np.array([-2.6, -0.45, 0]))
        self.play(Create(f["head"]), *[Create(f[k]) for k in ("r0", "r1", "ml", "cl")], run_time=1.0)
        self.play(LaggedStart(*[FadeIn(f["e" + n], scale=0.6) for n in E.NAMES], lag_ratio=0.08), run_time=2.0)
        self.play(Create(f["side"]), FadeIn(f["nas"]), FadeIn(f["ini"]), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(f[f"s{k}"]) for k in range(5)], *[FadeIn(f[f"p{k}"]) for k in range(6)], lag_ratio=0.1), FadeIn(f["lg"]), run_time=1.5)
        bl = bullets([tr("Positions at ++10 %++ and ++20 %++ of nasion–inion and ear-to-ear distances: ~relative~.", "Posizioni al ++10 %++ e ++20 %++ delle distanze nasion–inion e tra le orecchie: ~relative~."),
                      tr("Letters = region: *Fp*, *F*, *C*, *T*, *P*, *O*.", "Lettere = regione: *Fp*, *F*, *C*, *T*, *P*, *O*."),
                      tr("Odd = left, even = right, *z* = midline.", "Dispari = sinistra, pari = destra, *z* = linea mediana."),
                      tr("Jasper (1958); 10-10: Chatrian et al. (1985); 10-5: Oostenveld & Praamstra (2001).", "Jasper (1958); 10-10: Chatrian et al. (1985); 10-5: Oostenveld & Praamstra (2001).")], 17, n=30, gap=0.26).move_to(np.array([4.6, -0.4, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.45)

        # ---------------------------------------------------------- 8 quanti elettrodi: 19 → 64 → 128 → 256
        self.new(tr("Electrodes (4)", "Elettrodi (4)"), tr("How many electrodes? 10-10, 10-5 and high density", "Quanti elettrodi? 10-10, 10-5 e alta densità"))
        hc = np.array([-3.6, -0.55, 0]); Rh = 2.3
        hd = E.head(hc, Rh)
        self.play(Create(hd))
        pts19 = [hc + E.el2d(n, Rh) for n in E.NAMES]
        dots = VGroup(*[Dot(p, radius=0.09, color=AMB) for p in pts19])
        cnt = TX("19", font=SERIF_F, font_size=60, color=AMB, weight=BOLD).move_to(np.array([1.2, 1.4, 0]))
        use = T(tr("clinical 10-20: epilepsy, sleep", "10-20 clinico: epilessia, sonno"), 20).next_to(cnt, DOWN, buff=0.2)
        self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.04), FadeIn(cnt), FadeIn(use), run_time=1.2)
        steps = [(64, "64", tr("10-10: most cognitive studies, ERPs", "10-10: la maggior parte degli studi cognitivi, ERP"), ACC, 0.07),
                 (128, "128", tr("high density: source imaging, microstates", "alta densità: sorgenti, microstati"), TEAL, 0.055),
                 (256, "256", tr("10-5 / geodesic nets", "10-5 / reti geodetiche"), PURP, 0.04)]
        for n_, s_, u_, col, r_ in steps:
            self.next_slide()
            nd = VGroup(*[Dot(hc + p, radius=r_, color=col) for p in sunflower(n_, Rh * 0.93)])
            c2 = TX(s_, font=SERIF_F, font_size=60, color=col, weight=BOLD).move_to(cnt)
            u2 = T(u_, 20).next_to(c2, DOWN, buff=0.2)
            self.play(FadeOut(dots), FadeIn(nd, lag_ratio=0.01), Transform(cnt, c2), Transform(use, u2), run_time=1.2)
            dots = nd
        bl = bullets([tr("Scalp potentials vary over ≈2–3 cm: ++≥ 64–128 channels++ for good topographies and sources.", "I potenziali di scalpo variano su ≈2–3 cm: ++≥ 64–128 canali++ per buone topografie e sorgenti."),
                      tr("But: longer set-up, more bad channels, more gel bridges.", "Ma: montaggio più lungo, più canali cattivi, più ponti di gel."),
                      tr("~Choose the montage from the question.~", "~Scegliere il montaggio in base alla domanda.~")], 18, n=46, gap=0.25).move_to(np.array([3.4, -1.3, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.45)

        # ---------------------------------------------------------- 9 sezione
        self.new(); section_title(self, 2, tr("Amplification and reference", "Amplificazione e riferimento"))

        # ---------------------------------------------------------- 10 amplificatore differenziale: il rumore comune si cancella (dal vivo)
        self.new(tr("Amplifier (1)", "Amplificatore (1)"), tr("Differential amplification and CMRR", "Amplificazione differenziale e CMRR"))
        f = F4.f08_diffamp(3.2); fit(f, 0.85, np.array([0.0, 0.7, 0]))
        self.play(FadeIn(f["la"]), Create(f["a"]), FadeIn(f["lb"]), Create(f["b"]), run_time=1.2)
        self.play(Create(f["wa"]), Create(f["wb"]), Create(f["amp"]), FadeIn(f["pl"]), FadeIn(f["mi"]), run_time=1.0)
        self.play(Create(f["out"]), FadeIn(f["lo"]), run_time=1.0)
        self.play(Write(f["cm"]))
        bl = bullets([tr("Output = ++active − reference++: what is ++common++ to both inputs (mains, body potential) cancels.", "Uscita = ++attivo − riferimento++: ciò che è ++comune++ ai due ingressi (rete, potenziale del corpo) si annulla."),
                      tr("*CMRR* ≥ 100 dB = 100 000×; unbalanced impedances degrade it. A *ground* (or DRL) sets the operating point.", "*CMRR* ≥ 100 dB = 100 000×; impedenze sbilanciate lo peggiorano. La *terra* (o DRL) fissa il punto di lavoro.")], 17, n=96, gap=0.16).move_to(np.array([0, -1.95, 0]))
        mt = metaphor(tr("++noise-cancelling headphones++: they record the ambient noise and subtract it.", "le ++cuffie a cancellazione di rumore++: registrano il rumore ambientale e lo sottraggono."), 16).move_to(np.array([0, -3.0, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.5)
        self.play(FadeIn(mt))
        # loop: rete che "respira" in ampiezza, EEG che scorre; l'uscita resta pulita
        k_ = 0.85; Wd = 3.2 * k_
        Oa, Ob, Oo = f["a"].points[0].copy(), f["b"].points[0].copy(), f["out"].points[0].copy()
        Dd = 2.0; fsd = 1000
        tt, br = E.periodic_eeg(Dd, fs=fsd, seed=31, peaks=((10.0, 1.0, 1.5),), uv=1.0)
        br = br / np.std(br) * 0.3
        mains = np.sin(2 * np.pi * 50 * tt)
        loop_start(self)
        ph = ValueTracker(0.0)

        def live():
            u = ph.get_value(); a = 1.2 * (1 + 0.45 * np.sin(2 * np.pi * u))
            st = u * Dd
            return VGroup(E.window_trace(tt, br + a * mains, st, 0.4, Oa, Wd, 0.35 * k_, TEAL, 2),
                          E.window_trace(tt, a * mains, st, 0.4, Ob, Wd, 0.35 * k_, TEAL, 2),
                          E.window_trace(tt, br, st, 0.4, Oo, Wd, 0.6 * k_, ACC, 3))
        self.remove(f["a"], f["b"], f["out"])
        lv = always_redraw(live); self.add(lv); loop_play(self, ph, 8.0); lv.clear_updaters()

        # ---------------------------------------------------------- 11 riferimento
        self.new(tr("Reference (1)", "Riferimento (1)"), tr("There is no neutral reference", "Non esiste un riferimento neutro"))
        refs = [(tr("Vertex (Cz)", "Vertice (Cz)"), tr("common in recording; kills activity at Cz", "comune in registrazione; azzera l'attività in Cz")),
                (tr("Linked mastoids / ears", "Mastoidi / orecchie collegate"), tr("classic for ERPs; mastoids are not silent", "classico per gli ERP; le mastoidi non sono silenziose")),
                (tr("Nose / chin", "Naso / mento"), tr("far from cortex, but muscle and eye artifacts", "lontano dalla corteccia, ma artefatti muscolari e oculari")),
                (tr("Average reference", "Riferimento medio"), tr("mean of all channels: good with ≥ 64 evenly spread electrodes", "media di tutti i canali: buono con ≥ 64 elettrodi ben distribuiti")),
                (tr("REST", "REST"), tr("model-based reference at infinity (Yao, 2001)", "riferimento all'infinito basato su modello (Yao, 2001)"))]
        rows = VGroup()
        for k, (a_, b_) in enumerate(refs):
            box = RoundedRectangle(corner_radius=0.12, width=12.4, height=0.68, fill_color=CARD if k % 2 == 0 else CARD2, fill_opacity=1, stroke_width=0)
            la = TX(a_, font=BODY, font_size=20, color=TEAL, weight=BOLD).move_to(box).align_to(box, LEFT).shift(RIGHT * 0.3)
            lb = T(b_, 19, n=70).move_to(box).align_to(box, LEFT).shift(RIGHT * 4.3)
            rows.add(VGroup(box, la, lb))
        rows.arrange(DOWN, buff=0.14).move_to(np.array([0, 0.35, 0]))
        for r_ in rows: self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.45)
        fm = fcard(r"V_{new}(ch) = V(ch) - V_{newref}", CARD, 0.85).move_to(np.array([-2.2, -2.75, 0]))
        rn = T(tr("Re-referencing is ++linear++ and offline. ~Always report the reference.~", "La ri-referenziazione è ++lineare++ e offline. ~Riportare sempre il riferimento.~"), 18, n=40).next_to(fm, RIGHT, buff=0.5)
        self.play(FadeIn(fm), FadeIn(rn))
        self.end()
