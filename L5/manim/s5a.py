from base import *
import figs5 as F5
from scipy.signal import butter, sosfilt, sosfiltfilt


class A5_Pipeline(Base):
    start_num = 1

    def construct(self):
        # ---------------------------------------------------------- 1 copertina: tracciato grezzo e pulito che scorrono
        self.new(first=True); self.num = 1
        hc = np.array([5.7, -2.35, 0]); Rh = 0.95
        t, names, brain, raw = F5.blink_mix(4.0)
        sigs = [(t, raw[0]), (t, brain[0])]
        Os = [np.array([2.0, -1.85, 0]), np.array([2.0, -2.75, 0])]
        cols = [ACC, TEAL]

        def vis():
            hd = VGroup(E.head(hc, Rh), E.electrodes(hc, Rh, r=0.04))
            tr0 = VGroup(*[E.window_trace(tt, x, 0.0, 2.0, O, 2.6, 0.0035, c, 1.8) for (tt, x), O, c in zip(sigs, Os, cols)])
            self.play(FadeIn(hd), Create(tr0), run_time=1.2)
            self.tr0 = tr0
        copertina(self, tr("Lecture 5", "Lezione 5"), tr("Preprocessing and ICA:\nfrom raw signal to clean data", "Pre-elaborazione e ICA:\ndal segnale grezzo ai dati puliti"), vis)
        scroll_many(self, sigs, Os, 2.6, 0.0035, 2.0, cols, 4.0, 1.8, old=self.tr0)

        # ---------------------------------------------------------- 2 obiettivi
        self.new(tr("Lecture 5", "Lezione 5"), tr("Today: turning raw EEG into analysable data", "Oggi: trasformare l'EEG grezzo in dati analizzabili"))
        g = rows_mob([tr("A ++standard pipeline++ and why the order matters.", "Una ++pipeline standard++ e perché l'ordine conta."),
                      tr("*Filtering* and resampling without distorting the signal.", "*Filtraggio* e ricampionamento senza distorcere il segnale."),
                      tr("*Bad channels*, interpolation and ++re-referencing++.", "*Canali cattivi*, interpolazione e ++ri-referenziazione++."),
                      tr("*Epoching*, baseline correction and ++artifact rejection++.", "*Epoche*, correzione della baseline e ++rigetto degli artefatti++."),
                      tr("*Independent Component Analysis*: theory, practice, ICLabel.", "*Analisi delle componenti indipendenti*: teoria, pratica, ICLabel.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 3 pipeline: un evidenziatore percorre i passi
        self.new(tr("The pipeline", "La pipeline"), tr("Seven steps from raw file to clean epochs", "Sette passi dal file grezzo alle epoche pulite"))
        f = F5.f03_pipeline(13.0)
        for m in f.values():
            m.shift(UP * 1.2)
        for k in range(7):
            anims = [FadeIn(f[f"b{k}"], shift=UP * 0.1)]
            if k < 6: anims.append(GrowArrow(f[f"a{k}"]))
            self.play(*anims, run_time=0.35)
        bl = bullets([tr("Order matters: ++filter before epoching++, ++bad channels out before average reference++, ++ICA before baseline++.", "L'ordine conta: ++filtrare prima di epocare++, ++canali cattivi fuori prima del riferimento medio++, ++ICA prima della baseline++."),
                      tr("Every step is a ++choice++: report parameters and software versions.", "Ogni passo è una ++scelta++: riportare parametri e versioni del software."),
                      tr("Look at the data ~before, during and after~ each step.", "Guardare i dati ~prima, durante e dopo~ ogni passo."),
                      tr("\"EEG is better left alone\": minimal pipelines are often enough (Delorme, 2023).", "\"L'EEG è meglio lasciarlo in pace\": pipeline minime spesso bastano (Delorme, 2023).")], 18, n=84, gap=0.2).move_to(np.array([0, -0.9, 0]))
        mt = metaphor(tr("cooking: ++wash and cut++ the vegetables first — but peel too much and nothing is left.", "la cucina: ++lavare e tagliare++ le verdure prima — ma sbucciando troppo non resta nulla."), 17).move_to(np.array([0, -3.0, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.45)
        self.play(FadeIn(mt))
        boxes = [f[f"b{k}"][0] for k in range(7)]
        loop_start(self)
        ph = ValueTracker(0.0)
        hl = always_redraw(lambda: SurroundingRectangle(boxes[min(int(ph.get_value() * 7), 6)], color=AMB, stroke_width=6, buff=0.08, corner_radius=0.18))
        self.add(hl); loop_play(self, ph, 7.0); hl.clear_updaters()

        # ---------------------------------------------------------- 4 sezione
        self.new(); section_title(self, 1, tr("Filtering and resampling", "Filtraggio e ricampionamento"))

        # ---------------------------------------------------------- 5 causale vs fase zero (taglio che cambia dal vivo)
        self.new(tr("Filtering (1)", "Filtraggio (1)"), tr("Causal or zero-phase? FIR or IIR?", "Causale o a fase zero? FIR o IIR?"))
        tt = np.arange(-1.0, 2.0, 1 / 250)
        x = F5.erp_wave(tt)
        fcs = np.logspace(np.log10(4.0), np.log10(40.0), 81)
        CAUS = np.array([sosfilt(butter(4, fc, "lowpass", fs=250, output="sos"), x) for fc in fcs])
        ZERO = np.array([sosfiltfilt(butter(4, fc, "lowpass", fs=250, output="sos"), x) for fc in fcs])
        m = (tt >= -0.1) & (tt <= 0.7)
        Wp = 6.4; Hs = 0.15; Op = np.array([-6.4, -0.9, 0])
        X = lambda a, b: Op + np.array([(a + 0.1) / 0.8 * Wp, Hs * b, 0])
        fcT = ValueTracker(fcs[-1])
        kk = lambda: int(np.argmin(np.abs(np.log10(fcs) - np.log10(fcT.get_value()))))
        base_ = VGroup(Line(X(-0.1, 0), X(0.7, 0), color=MUT, stroke_width=1.2), DashedLine(X(0, -8), X(0, 11), color=MUT, stroke_width=1.5),
                       T("0 ms", 14, MUT).move_to(X(0, -8.8)), T("600 ms", 14, MUT).move_to(X(0.6, -1.2)))
        orig = VMobject(color=FG, stroke_width=2.5).set_points_as_corners([X(a, b) for a, b in zip(tt[m], x[m])])

        def live():
            k = kk()
            g = VGroup(VMobject(color=ACC, stroke_width=3.5).set_points_as_corners([X(a, b) for a, b in zip(tt[m], CAUS[k][m])]),
                       VMobject(color=TEAL, stroke_width=3.5).set_points_as_corners([X(a, b) for a, b in zip(tt[m], ZERO[k][m])]))
            mm = (tt > 0.25) & (tt < 0.6)
            d = (tt[mm][np.argmax(CAUS[k][mm])] - tt[mm][np.argmax(ZERO[k][mm])]) * 1000
            s_ = tr(f"low-pass f_{{c}} = **{fcs[k]:.0f} Hz** → causal delay ≈ **{d:.0f} ms**", f"passa-basso f_{{c}} = **{fcs[k]:.0f} Hz** → ritardo causale ≈ **{d:.0f} ms**")
            g.add(T(s_, 19, AMB).move_to(np.array([-3.2, 2.0, 0])))
            return g
        lg = VGroup(T(tr("original", "originale"), 16, FG), T(tr("causal (one pass)", "causale (un passaggio)"), 16, ACC), T(tr("zero-phase (filtfilt)", "fase zero (filtfilt)"), 16, TEAL)).arrange(RIGHT, buff=0.5).move_to(np.array([-3.2, -2.55, 0]))
        lv = always_redraw(live)
        self.play(FadeIn(base_), Create(orig), FadeIn(lg), run_time=1.0)
        self.play(FadeIn(lv))
        bl = bullets([tr("*Causal*: depends only on the past → ++delays++ peaks.", "*Causale*: dipende solo dal passato → ++ritarda++ i picchi."),
                      tr("*Zero-phase*: no delay but ++acausal++: effects can leak ++before++ onset.", "*Fase zero*: nessun ritardo ma ++acausale++: effetti possono comparire ++prima++ dell'onset."),
                      tr("*FIR*: stable, linear phase; *IIR*: steep, nonlinear phase.", "*FIR*: stabili, fase lineare; *IIR*: ripidi, fase non lineare."),
                      tr("HP ++0.1 Hz++ for ERPs, ++1 Hz++ for ICA; LP 30–40 Hz (Widmann et al., 2015).", "HP ++0,1 Hz++ per ERP, ++1 Hz++ per ICA; LP 30–40 Hz (Widmann et al., 2015).")], 16, n=38, gap=0.22).move_to(np.array([3.9, 0.1, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.4)
        mt = metaphor(tr("zero-phase = ++editing a film afterwards++: nothing is late, but you can \"see the future\".", "fase zero = ++montare un film a posteriori++: niente è in ritardo, ma si può \"vedere il futuro\"."), 16).move_to(np.array([0, -3.2, 0]))
        self.play(FadeIn(mt))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: fcT.set_value(10 ** (np.log10(40) - np.log10(10) * (0.5 - 0.5 * np.cos(2 * np.pi * ph.get_value())))))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); lv.clear_updaters()

        # ---------------------------------------------------------- 6 ricampionamento e rete
        self.new(tr("Filtering (2)", "Filtraggio (2)"), tr("Resampling and line-noise removal", "Ricampionamento e rimozione della rete"))
        kinds = [(tr("Downsampling", "Sottocampionamento"), tr("1000 → 250 Hz saves memory. Always ++low-pass first++ (resample does it); never just keep every 4th sample.", "1000 → 250 Hz fa risparmiare memoria. Sempre ++passa-basso prima++ (resample lo fa); mai tenere un campione ogni 4.")),
                 (tr("Notch filter", "Filtro notch"), tr("Simple but ++rings++ in time and removes brain activity at 50 Hz: avoid it for gamma.", "Semplice ma ++oscilla++ nel tempo e toglie attività cerebrale a 50 Hz: evitarlo per la gamma.")),
                 (tr("Spatial methods", "Metodi spaziali"), tr("++CleanLine++ (sinusoid regression), ++Zapline(-plus)++ (spatial filter): minimal distortion (de Cheveigné, 2020).", "++CleanLine++ (regressione di sinusoidi), ++Zapline(-plus)++ (filtro spaziale): distorsione minima (de Cheveigné, 2020)."))]
        cs = VGroup()
        for k, (h_, d_) in enumerate(kinds):
            box = RoundedRectangle(corner_radius=0.14, width=4.0, height=3.0, fill_color=CARD if k % 2 == 0 else CARD2, fill_opacity=1, stroke_width=0)
            tx = VGroup(TX(h_, font=BODY, font_size=22, color=TEAL, weight=BOLD), T(d_, 18, n=34)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            tx.move_to(box).align_to(box, UP).shift(DOWN * 0.3)
            cs.add(VGroup(box, tx))
        cs.arrange(RIGHT, buff=0.25).move_to(np.array([0, 0.4, 0]))
        for c_ in cs: self.play(FadeIn(c_, shift=UP * 0.15), run_time=0.5)
        bl = bullets([tr("Keep f_{s} > 2.5 × low-pass cut-off after resampling.", "Mantenere f_{s} > 2,5 × taglio del passa-basso dopo il ricampionamento."),
                      tr("Check the ++spectrum++ before/after: remove the peak, not the neighbours.", "Controllare lo ++spettro++ prima/dopo: togliere il picco, non i vicini.")], 18, n=90, gap=0.2).move_to(np.array([0, -2.35, 0]))
        self.play(FadeIn(bl))

        # ---------------------------------------------------------- 7 sezione
        self.new(); section_title(self, 2, tr("Bad channels and re-referencing", "Canali cattivi e ri-referenziazione"))

        # ---------------------------------------------------------- 8 canali cattivi (tracce che scorrono)
        self.new(tr("Bad channels (1)", "Canali cattivi (1)"), tr("Finding bad channels", "Trovare i canali cattivi"))
        t, chans = F5.bad_signals(4.0)
        labs = {"C3": tr("flat", "piatto"), "C4": tr("noisy", "rumoroso"), "CP2": tr("drifting", "in deriva")}
        Wb = 7.2; xb = -5.6
        Os = [np.array([xb, 2.0 - 0.6 * k, 0]) for k in range(8)]
        cols = [ACC if n in labs else TEAL for n, _ in chans]
        nm = VGroup(*[T(n, 15, ACC if n in labs else MUT).move_to(O + np.array([-0.45, 0, 0])) for (n, _), O in zip(chans, Os)])
        tg = VGroup(*[T(f"~{labs[n]}~" if False else labs[n], 15, ACC).move_to(O + np.array([Wb + 0.55, 0, 0])) for (n, _), O in zip(chans, Os) if n in labs])
        tr0 = VGroup(*[E.window_trace(t, x, 0.0, 2.0, O, Wb, 0.006, c, 1.4) for (_, x), O, c in zip(chans, Os, cols)])
        self.play(FadeIn(nm), LaggedStart(*[Create(x) for x in tr0], lag_ratio=0.1), run_time=1.5)
        self.play(FadeIn(tg))
        bl = bullets([tr("*Flat*: variance ≈ 0.", "*Piatto*: varianza ≈ 0."),
                      tr("*Noisy*: robust z > 3–5.", "*Rumoroso*: z robusto > 3–5."),
                      tr("*Drifting*: low correlation with neighbours (r < 0.8), ++RANSAC++ (PREP).", "*In deriva*: bassa correlazione con i vicini (r < 0,8), ++RANSAC++ (PREP)."),
                      tr("Automatic + ~visual check~; > 10–15 % bad → question the recording.", "Automatico + ~controllo visivo~; > 10–15 % cattivi → dubitare della registrazione.")], 15, n=26, gap=0.22).move_to(np.array([4.9, -0.2, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.4)
        scroll_many(self, [(t, x) for _, x in chans], Os, Wb, 0.006, 2.0, cols, 4.0, 1.4, old=tr0)

        # ---------------------------------------------------------- 9 interpolazione (la mappa si ripara)
        self.new(tr("Bad channels (2)", "Canali cattivi (2)"), tr("Interpolation with spherical splines", "Interpolazione con spline sferiche"))
        bad, good = F5.bad_topos()
        cm = np.array([-3.2, -0.45, 0]); Rm = 2.2

        def mp(v):
            V, mk = E.interp_map(v, n=121, p=2.5)
            img, out = E.topomap(V, mk, cm, Rm, vmax=1.0, elec=True)
            return Group(img, out)
        m_bad, m_good = mp(bad), mp(good)
        ring = Circle(radius=0.22, color=AMB, stroke_width=5).move_to(cm + E.el2d("C4", Rm))
        l_bad = T(tr("C4 broken", "C4 guasto"), 22, ACC).move_to(cm + np.array([0, -Rm - 0.45, 0]))
        l_good = T(tr("C4 interpolated", "C4 interpolato"), 22, TEAL).move_to(l_bad)
        self.play(FadeIn(m_bad), Create(ring), FadeIn(l_bad), run_time=1.2)
        bl = bullets([tr("Estimate the missing channel from its neighbours with the ++smooth scalp field++ (Perrin et al., 1989).", "Stimare il canale mancante dai vicini con il ++campo liscio++ sullo scalpo (Perrin et al., 1989)."),
                      tr("Only for ++few, scattered++ bad channels.", "Solo per canali cattivi ++pochi e sparsi++."),
                      tr("⚠ ++No new information++: the data ++rank++ decreases by one per channel.", "⚠ ++Nessuna informazione nuova++: il ++rango++ scende di uno per canale.")], 18, n=38, gap=0.3).move_to(np.array([3.5, 0.2, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.45)
        self.next_slide()
        self.play(FadeIn(m_good), FadeOut(m_bad), FadeOut(l_bad), FadeIn(l_good), run_time=2.0)
        self.remove(ring); self.play(Create(ring), run_time=0.4)

        # ---------------------------------------------------------- 10 riferimento medio: un canale cattivo contamina tutti
        self.new(tr("Re-referencing", "Ri-referenziazione"), tr("Average reference and the rank of the data", "Riferimento medio e rango dei dati"))
        fm = fcard(r"V_{avg}(ch) = V(ch) - \frac{1}{N}\sum_k V(k)", CARD2, 0.8).move_to(np.array([-3.2, 1.8, 0]))
        self.play(FadeIn(fm))
        vals = np.array([3.0, -2.0, 4.0, 1.0, -1.0, 2.0, -3.0, 0.5])
        chn = ["Fz", "C3", "Cz", "C4", "P3", "Pz", "P4", "Oz"]
        badA = ValueTracker(0.0); refT = ValueTracker(0.0)
        y0 = -0.8; sc = 0.05; xs0 = -6.0; dx = 0.72

        def bars():
            v = vals.copy(); v[5] += badA.get_value()
            mu = v.mean()
            v2 = v - refT.get_value() * mu
            g = VGroup(Line(np.array([xs0 - 0.3, y0, 0]), np.array([xs0 + dx * 8, y0, 0]), color=MUT, stroke_width=1.5))
            for k, a in enumerate(v2):
                x_ = xs0 + dx * (k + 0.5)
                col = ACC if k == 5 and badA.get_value() > 1 else TEAL
                h = max(abs(a) * sc, 0.01)
                g.add(Rectangle(width=0.45, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(np.array([x_, y0 + np.sign(a) * h / 2, 0])))
                g.add(T(chn[k], 13, MUT).move_to(np.array([x_, -2.9, 0])))
            ym = y0 + (1 - refT.get_value()) * mu * sc
            g.add(DashedLine(np.array([xs0 - 0.3, ym, 0]), np.array([xs0 + dx * 8, ym, 0]), color=AMB, stroke_width=2.5))
            g.add(T(tr("mean", "media"), 14, AMB).move_to(np.array([xs0 + dx * 8 + 0.45, ym, 0])))
            return g
        bz = always_redraw(bars)
        self.play(FadeIn(bz))
        self.next_slide()
        self.play(refT.animate.set_value(1.0), run_time=1.2)
        self.next_slide()
        self.play(refT.animate.set_value(0.0), run_time=0.6)
        self.play(badA.animate.set_value(40.0), run_time=1.0)
        self.play(refT.animate.set_value(1.0), run_time=1.2)
        bl = bullets([tr("Remove/interpolate bad channels ++first++: one bad channel contaminates ++all++ through the mean.", "Togliere/interpolare i canali cattivi ++prima++: un canale cattivo contamina ++tutti++ attraverso la media."),
                      tr("≥ 64 well-spread electrodes → approximates a ++zero-potential++ reference (Dien, 1998).", "≥ 64 elettrodi ben distribuiti → approssima un riferimento a ++potenziale zero++ (Dien, 1998)."),
                      tr("Channels now sum to zero → ++rank = N − 1++ (−1 per interpolated channel). ~Tell ICA the true rank.~", "I canali ora sommano a zero → ++rango = N − 1++ (−1 per canale interpolato). ~Comunicare all'ICA il rango vero.~")], 17, n=40, gap=0.28).move_to(np.array([3.7, -0.3, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.45)
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: badA.set_value(40.0 * (0.5 + 0.5 * np.cos(2 * np.pi * ph.get_value()))))
        self.add(drv); loop_play(self, ph, 5.0); drv.clear_updaters(); bz.clear_updaters()

        # ---------------------------------------------------------- 11 sezione
        self.new(); section_title(self, 3, tr("Epochs, baseline and rejection", "Epoche, baseline e rigetto"))

        # ---------------------------------------------------------- 12 epoche e media che si accumula
        self.new(tr("Epochs (1)", "Epoche (1)"), tr("Cutting the continuous signal around events", "Tagliare il segnale continuo attorno agli eventi"))
        t, x = F5.cont_signal()
        Wc = 12.6; Oc = np.array([-6.3, 1.15, 0]); hc_ = 0.028
        Xc = lambda tt_: Oc + np.array([tt_ / 6.5 * Wc, 0, 0])
        cont = E.trace(t, x, Oc, Wc, hc_, TEAL, 1.6)
        evs = VGroup(*[VGroup(Line(Xc(e) + np.array([0, -0.7, 0]), Xc(e) + np.array([0, 0.8, 0]), color=ACC, stroke_width=2.5), T(f"S{k + 1}", 14, ACC).move_to(Xc(e) + np.array([0, 1.0, 0]))) for k, e in enumerate(F5.EVENTS)])
        wins = VGroup(*[Rectangle(width=Wc / 6.5, height=1.3, stroke_width=0, fill_color=AMB, fill_opacity=0.18).move_to(Xc(e + 0.3)) for e in F5.EVENTS])
        self.play(Create(cont), run_time=1.5)
        self.play(FadeIn(evs), FadeIn(wins))
        # epoche che scendono e si impilano
        We = 4.2; xe = -6.3
        segs = VGroup(); targets = VGroup()
        for k, e in enumerate(F5.EVENTS):
            mm = (t >= e - 0.2) & (t < e + 0.8)
            segs.add(E.trace(t[mm], x[mm], Xc(e - 0.2), Wc / 6.5, hc_, TEAL, 1.6, e - 0.2, e + 0.8))
            targets.add(E.trace(t[mm] - e, x[mm], np.array([xe, -0.35 - 0.55 * k, 0]), We, 0.014, TEAL, 1.5, -0.2, 0.8))
        self.play(*[Transform(s_, t_) for s_, t_ in zip(segs, targets)], run_time=1.5)
        blr = Rectangle(width=We * 0.2, height=2.3, stroke_width=0, fill_color=MUT, fill_opacity=0.25).move_to(np.array([xe + We * 0.1, -1.18, 0]))
        blt = T("baseline", 14, MUT).move_to(np.array([xe + We * 0.1, -2.55, 0]))
        self.play(FadeIn(blr), FadeIn(blt))
        # media che si pulisce aumentando le epoche
        te = np.arange(-0.2, 0.8, 1 / 250)
        EP = np.array([F5.erp_wave(te) + E.periodic_eeg(1.0, 250, seed=100 + i, peaks=((10, 1, 0.8),), uv=12)[1] for i in range(64)])
        Oa = np.array([0.4, -1.55, 0]); Wa = 5.8; ha = 0.06
        Xa = lambda a, b: Oa + np.array([(a + 0.2) * Wa, ha * b, 0])
        nT = ValueTracker(1)

        def avg():
            n = int(round(nT.get_value()))
            y = EP[:n].mean(0)
            return VGroup(VMobject(color=ACC, stroke_width=3).set_points_as_corners([Xa(a, b) for a, b in zip(te, y)]),
                          T(tr(f"average of **{n}** epochs", f"media di **{n}** epoche"), 18, ACC).move_to(Oa + np.array([Wa / 2, 1.45, 0])))
        axa = VGroup(Line(Xa(-0.2, 0), Xa(0.8, 0), color=MUT, stroke_width=1.2), DashedLine(Xa(0, -10), Xa(0, 14), color=MUT, stroke_width=1.2),
                     T(tr("noise ∝ 1/√n", "rumore ∝ 1/√n"), 16, MUT).move_to(Oa + np.array([Wa / 2, -1.45, 0])))
        az = always_redraw(avg)
        self.play(FadeIn(axa), FadeIn(az))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: nT.set_value(1 + 63 * ph.get_value() ** 2))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); az.clear_updaters()

        # ---------------------------------------------------------- 13 rigetto delle epoche
        self.new(tr("Epochs (2)", "Epoche (2)"), tr("Rejecting bad epochs", "Rigettare le epoche cattive"))
        f = F5.f14_reject(5.0); fit(f, 0.95, np.array([-3.4, -0.45, 0]))
        parts = [f[f"x{k}"] for k in range(5)]
        self.play(*[Create(f[f"u{k}"]) for k in range(5)], *[Create(f[f"d{k}"]) for k in range(5)], FadeIn(f["th"]), run_time=0.8)
        self.play(LaggedStart(*[Create(p_) for p_ in parts], lag_ratio=0.15), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(f[f"k{k}"], scale=1.5) for k in range(5)], lag_ratio=0.15), run_time=1.0)
        self.play(f["x2"].animate.set_stroke(opacity=0.25), run_time=0.6)
        bl = bullets([tr("*Thresholds*: absolute (±100 µV) or peak-to-peak.", "*Soglie*: assolute (±100 µV) o picco-picco."),
                      tr("*Statistics*: improbability, kurtosis, joint probability.", "*Statistiche*: improbabilità, curtosi, probabilità congiunta."),
                      tr("*ASR*: repairs short high-variance bursts (Mullen et al., 2015).", "*ASR*: ripara brevi burst ad alta varianza (Mullen et al., 2015)."),
                      tr("Keep ++enough++ and ++balanced++ trials; report rejection rates.", "Mantenere trial ++sufficienti++ e ++bilanciati++; riportare i tassi di rigetto."),
                      tr("~Correct~ what you can (ICA), ~reject~ what you must.", "~Correggere~ ciò che si può (ICA), ~rigettare~ ciò che si deve.")], 17, n=38, gap=0.26).move_to(np.array([3.6, -0.3, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.4)
        self.end()
