from base import *
import figs8 as F8

MSC = F8.MS_COL


def dec(v, n=2):
    s = f"{v:.{n}f}"
    return s if LANG == "en" else s.replace(".", ",")


TM = [V / np.abs(V[m]).max() for V, m in F8.template_maps(81)]
MASK = F8.template_maps(81)[0][1]


def tmap(V, c, R, vmax=1.0, elec=False):
    img, out = E.topomap(V, MASK, c, R, vmax=vmax, elec=elec)
    return Group(img, out)


def morph(u):
    """u in [0,4): mappa che passa con continuità A→B→C→D→A."""
    k = int(np.floor(u)) % 4; f = u - np.floor(u)
    s = 0.5 - 0.5 * np.cos(np.pi * np.clip((f - 0.5) / 0.5, 0, 1))
    return TM[k] * (1 - s) + TM[(k + 1) % 4] * s, k if s < 0.5 else (k + 1) % 4


class A8_Mappe(Base):
    start_num = 1

    def construct(self):
        # ---------------------------------------------------------- 1 copertina: mappa che scorre tra A-D
        self.new(first=True); self.num = 1
        c = np.array([5.3, -2.3, 0]); Rr = 1.05
        uT = ValueTracker(0.0)

        def mp():
            V, k = morph(uT.get_value())
            return Group(tmap(V, c, Rr), Text("ABCD"[k], font=BODY, font_size=30, color=MSC[k], weight=BOLD).move_to(c + np.array([-1.5, 0.8, 0])))

        def vis():
            self.play(FadeIn(mp()))
        copertina(self, tr("Lecture 8", "Lezione 8"), tr("Spatial analysis\nand EEG microstates", "Analisi spaziale\ne microstati EEG"), vis)
        self.remove(*[m for m in self.mobjects if isinstance(m, Group)])
        loop_start(self)
        ph = ValueTracker(0.0)
        mz = redraw(lambda: (uT.set_value(4 * ph.get_value()), mp())[1])
        self.add(mz); loop_play(self, ph, 8.0); mz.clear_updaters()

        # ---------------------------------------------------------- 2 obiettivi
        self.new(tr("Lecture 8", "Lezione 8"), tr("Today: the whole map, not single electrodes", "Oggi: la mappa intera, non i singoli elettrodi"))
        g = rows_mob([tr("Limits of ++single-channel++ analysis; reference-free descriptors.", "Limiti dell'analisi ++a canale singolo++; descrittori indipendenti dal riferimento."),
                      tr("*Global Field Power* and *Global Map Dissimilarity*.", "*Global Field Power* e *Global Map Dissimilarity*."),
                      tr("*Microstates*: clustering, choosing k, back-fitting.", "*Microstati*: clustering, scelta di k, back-fitting."),
                      tr("Microstate ++metrics++ and their neural meaning.", "++Metriche++ dei microstati e significato neurale."),
                      tr("*Applications*: cognition, sleep, anaesthesia, psychiatry, stimulation.", "*Applicazioni*: cognizione, sonno, anestesia, psichiatria, stimolazione.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 3 da forme d'onda a mappe: EEG che scorre + mappa istantanea
        self.new(tr("Why spatial analysis?", "Perché l'analisi spaziale?"), tr("From many waveforms to one map per instant", "Da molte forme d'onda a una mappa per istante"))
        t, X, lab = F8.simulate(4.0, seed=12)
        chs = [0, 4, 9, 14, 18]
        Wt = 6.4; x0 = -6.3; win = 0.8; fs = F8.FS8
        Os = [np.array([x0, 1.5 - 0.75 * i, 0]) for i in range(len(chs))]
        nm = VGroup(*[T(E.NAMES[ch], 14, MUT).move_to(O + np.array([-0.4, 0, 0])) for ch, O in zip(chs, Os)])
        cm = np.array([3.6, 0.0, 0]); Rm = 1.9
        pT = ValueTracker(0.0)

        def live():
            s0 = pT.get_value() * 4.0
            g = VGroup(*[E.window_trace(t, X[ch], s0, win, O, Wt, 0.015, TEAL, 1.6) for ch, O in zip(chs, Os)])
            g.add(Line(np.array([x0 + Wt, 1.9, 0]), np.array([x0 + Wt, -1.9, 0]), color=AMB, stroke_width=2.5))
            return g

        def mapnow():
            k = int(round((pT.get_value() * 4.0 + win) * fs)) % X.shape[1]
            V, m = E.interp_map(X[:, k], n=81, p=2.5)
            return Group(*E.topomap(V, m, cm, Rm, vmax=np.abs(V[m]).max() * 1.05 + 1e-9, elec=True))
        lz = always_redraw(live); m0 = mapnow()
        self.play(FadeIn(nm), FadeIn(lz), FadeIn(m0))
        cap = T(tr("Channel-wise measures ++depend on the reference++; the ++shape++ of the map does not. Different shape ⇒ ++different generators++.", "Le misure per canale ++dipendono dal riferimento++; la ++forma++ della mappa no. Forma diversa ⇒ ++generatori diversi++."), 17, n=110).move_to(np.array([0, -2.45, 0]))
        mt = metaphor(tr("a ++weather map++: look at the whole pressure pattern, not single stations.", "una ++mappa meteo++: guardare l'intero campo di pressione, non le singole stazioni."), 16).move_to(np.array([0, -3.15, 0]))
        self.play(FadeIn(cap), FadeIn(mt))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: pT.set_value(ph.get_value()))
        self.remove(m0); mz = redraw(mapnow)
        self.add(drv, mz); loop_play(self, ph, 16.0); drv.clear_updaters(); lz.clear_updaters(); mz.clear_updaters()

        # ---------------------------------------------------------- 4 sezione
        self.new(); section_title(self, 1, tr("The scalp field as a map", "Il campo di scalpo come mappa"))

        # ---------------------------------------------------------- 5 GFP: butterfly che scorre
        self.new(tr("Spatial descriptors (1)", "Descrittori spaziali (1)"), tr("Global Field Power: the strength of the map", "Global Field Power: l'intensità della mappa"))
        g_ = F8.gfp(X)
        Wb = 7.4; Ob = np.array([-6.3, 0.9, 0]); Og = np.array([-6.3, -1.6, 0])
        pT = ValueTracker(0.0)
        cm = np.array([4.4, -0.55, 0]); Rm = 1.3

        def butter():
            s0 = pT.get_value() * 4.0
            gr = VGroup(*[E.window_trace(t, x, s0, win, Ob, Wb, 0.02, MUT, 1) for x in X])
            gr.add(E.window_trace(t, g_, s0, win, Og, Wb, 0.08, ACC, 3))
            gr.add(Line(np.array([-6.3 + Wb, 1.9, 0]), np.array([-6.3 + Wb, -1.8, 0]), color=AMB, stroke_width=2.5))
            k = int(round((s0 + win) * fs)) % X.shape[1]
            gr.add(T(f"GFP = **{dec(g_[k], 1)} µV**", 20, ACC).move_to(cm + np.array([0, -Rm - 0.45, 0])))
            return gr

        def mapnow2():
            k = int(round((pT.get_value() * 4.0 + win) * fs)) % X.shape[1]
            V, m = E.interp_map(X[:, k], n=81, p=2.5)
            return Group(*E.topomap(V, m, cm, Rm, vmax=np.abs(X).max() * 0.35))
        bz = always_redraw(butter); mz = mapnow2()
        lab_ = VGroup(T(tr("butterfly (all channels)", "butterfly (tutti i canali)"), 15, MUT).move_to(Ob + np.array([1.5, 1.0, 0])), T("GFP", 17, ACC).move_to(Og + np.array([-0.45, 0.3, 0])))
        fm = fcard(r"\mathrm{GFP}(t)=\sqrt{\tfrac{1}{N}\sum_i \big(V_i(t)-\bar V(t)\big)^2}", CARD2, 0.6).move_to(np.array([3.8, 1.75, 0]))
        self.play(FadeIn(lab_), FadeIn(bz), FadeIn(mz), FadeIn(fm))
        cap = T(tr("GFP = spatial standard deviation: ++reference-free++; its ++peaks++ have the highest SNR (Lehmann & Skrandies, 1980).", "GFP = deviazione standard spaziale: ++indipendente dal riferimento++; i suoi ++picchi++ hanno l'SNR massimo (Lehmann & Skrandies, 1980)."), 16, n=120).move_to(np.array([0, -2.95, 0]))
        self.play(FadeIn(cap))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: pT.set_value(ph.get_value()))
        self.remove(mz); mz = redraw(mapnow2)
        self.add(drv, mz); loop_play(self, ph, 16.0); drv.clear_updaters(); bz.clear_updaters(); mz.clear_updaters()

        # ---------------------------------------------------------- 6 GMD: forma vs intensità
        self.new(tr("Spatial descriptors (2)", "Descrittori spaziali (2)"), tr("Global Map Dissimilarity: the shape of the map", "Global Map Dissimilarity: la forma della mappa"))
        c1 = np.array([-4.6, 0.3, 0]); c2 = np.array([-0.9, 0.3, 0]); Rm = 1.4
        aT = ValueTracker(0.0)
        u = TM[2]

        def gmd():
            a = aT.get_value()
            sc = 1.0 + 0.8 * np.sin(2 * np.pi * a)
            w = np.clip(0.5 - 0.5 * np.cos(2 * np.pi * a), 0, 1)
            v = sc * ((1 - w) * TM[2] + w * TM[0])
            un = (u - u[MASK].mean()) / u[MASK].std(); vn = (v - v[MASK].mean()) / v[MASK].std()
            r = np.mean(un[MASK] * vn[MASK])
            gm = np.sqrt(max(2 * (1 - r), 0))
            return Group(tmap(u, c1, Rm, 1.8), tmap(v, c2, Rm, 1.8),
                         Text(f"GFP ratio = {dec(sc, 2)}", font=BODY, font_size=22, color=TEAL).move_to(np.array([-2.75, -1.75, 0])),
                         Text(f"GMD = {dec(gm, 2)}", font=BODY, font_size=26, color=ACC, weight=BOLD).move_to(np.array([-2.75, -2.25, 0])))
        gz = gmd()
        labs = VGroup(T(tr("map u", "mappa u"), 17).move_to(c1 + np.array([0, Rm + 0.35, 0])), T(tr("map v", "mappa v"), 17).move_to(c2 + np.array([0, Rm + 0.35, 0])))
        self.play(FadeIn(gz), FadeIn(labs))
        fm = fcard(r"\mathrm{GMD}=\sqrt{2\,(1-r_{uv})}", CARD2, 0.8).move_to(np.array([4.0, 1.6, 0]))
        bl = bullets([tr("Normalise by GFP → only ++shape++ remains.", "Normalizzare per la GFP → resta solo la ++forma++."),
                      tr("0 = same shape, 2 = inverted.", "0 = stessa forma, 2 = invertita."),
                      tr("Two questions: ++how strong++ (GFP) and ++which generators++ (GMD).", "Due domande: ++quanto forte++ (GFP) e ++quali generatori++ (GMD)."),
                      tr("*TANOVA*: permutation test on GMD (Murray et al., 2008).", "*TANOVA*: test di permutazione sulla GMD (Murray et al., 2008).")], 16, n=34, gap=0.26).move_to(np.array([4.0, -0.9, 0]))
        self.play(FadeIn(fm), FadeIn(bl))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: aT.set_value(ph.get_value()))
        self.remove(gz); gz = redraw(gmd)
        self.add(drv, gz); loop_play(self, ph, 8.0); drv.clear_updaters(); gz.clear_updaters()

        # ---------------------------------------------------------- 7 microstati: mappa istantanea + barra di stati
        self.new(tr("Microstates (1)", "Microstati (1)"), tr("The EEG as a sequence of quasi-stable maps", "L'EEG come sequenza di mappe quasi stabili"))
        t, X, lab = F8.simulate(4.0, seed=21, snr=40)
        g_ = F8.gfp(X)
        Wb = 12.0; Og = np.array([-6.0, -1.3, 0]); win = 1.0
        cm = np.array([0, 1.15, 0]); Rm = 1.0
        pT = ValueTracker(0.0)
        n = len(t)

        def seq():
            s0 = pT.get_value() * 4.0
            k0 = int(round(s0 * fs)); nw = int(win * fs)
            idx = (k0 + np.arange(nw)) % n
            gr = VGroup()
            i = 0
            while i < nw:
                j = i
                while j < nw and lab[idx[j]] == lab[idx[i]]: j += 1
                xa = Og[0] + i / nw * Wb; xb = Og[0] + j / nw * Wb
                gr.add(Rectangle(width=max(xb - xa, 0.01), height=1.2, stroke_width=0, fill_color=MSC[lab[idx[i]]], fill_opacity=0.45).move_to(np.array([(xa + xb) / 2, Og[1] + 0.6, 0])))
                if j - i > 8: gr.add(Text("ABCD"[lab[idx[i]]], font=BODY, font_size=16, color=MSC[lab[idx[i]]], weight=BOLD).move_to(np.array([(xa + xb) / 2, Og[1] - 0.3, 0])))
                i = j
            gr.add(E.window_trace(t, g_, s0, win, Og, Wb, 0.05, FG, 2.5))
            gr.add(Line(np.array([Og[0] + Wb / 2, Og[1] - 0.1, 0]), np.array([Og[0] + Wb / 2, Og[1] + 1.35, 0]), color=AMB, stroke_width=3))
            return gr

        def mnow():
            k = (int(round(pT.get_value() * 4.0 * fs)) + int(win * fs / 2)) % n
            V, m = E.interp_map(X[:, k], n=81, p=2.5)
            return Group(*E.topomap(V, m, cm, Rm, vmax=np.abs(V[m]).max() * 1.05 + 1e-9))
        sz = always_redraw(seq); mz = mnow()
        self.play(FadeIn(sz), FadeIn(mz))
        cap = T(tr("The map ++shape++ stays stable ≈ 60–120 ms, polarity flips with the oscillation, then it ++switches abruptly++ (Lehmann et al., 1987).", "La ++forma++ resta stabile ≈ 60–120 ms, la polarità si inverte con l'oscillazione, poi ++cambia bruscamente++ (Lehmann et al., 1987)."), 16, n=120).move_to(np.array([0, -2.45, 0]))
        mt = metaphor(tr("a ++slide show++: each slide stays for a moment, then the projector jumps.", "una ++proiezione di diapositive++: ogni diapositiva resta un attimo, poi il proiettore salta."), 16).move_to(np.array([0, -3.1, 0]))
        self.play(FadeIn(cap), FadeIn(mt))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: pT.set_value(ph.get_value()))
        self.remove(mz); mz = redraw(mnow)
        self.add(drv, mz); loop_play(self, ph, 24.0); drv.clear_updaters(); sz.clear_updaters(); mz.clear_updaters()
        self.end()
