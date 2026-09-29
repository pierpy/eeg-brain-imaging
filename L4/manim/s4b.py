from base import *
import figs4 as F4
from s4a import scroll_group
from scipy.signal import butter, sosfiltfilt, welch


BG_ = P.bg


def hx(rgb):
    r, g, b = (np.clip(np.asarray(rgb, float), 0, 1) * 255).astype(int)
    return "#%02x%02x%02x" % (r, g, b)


def smooth_step(x, a, w=0.025):
    return 0.5 * (1 + np.tanh((x - a) / w))


class B4_Digitale(Base):
    start_num = 12

    def construct(self):
        # ---------------------------------------------------------- 12 sezione
        self.new(first=True); section_title(self, 3, tr("Digitisation and filtering", "Digitalizzazione e filtraggio"))

        # ---------------------------------------------------------- 13 aliasing + ruota di carro (dal vivo)
        self.new(tr("Digitisation (1)", "Digitalizzazione (1)"), tr("Sampling, Nyquist and aliasing", "Campionamento, Nyquist e aliasing"))
        fs = 50.0; Tw = 0.3; W = 8.0; Hh = 0.8; O = np.array([-6.4, 0.65, 0])
        fT = ValueTracker(45.0)
        fa_ = lambda f: f - fs * np.round(f / fs)
        X = lambda tt, y: O + np.array([tt / Tw * W, Hh * y, 0])
        tt = np.linspace(0, Tw, 700); ts = np.arange(0, Tw + 1e-9, 1 / fs)

        def wave():
            f = fT.get_value(); fa = fa_(f)
            g = VGroup(VMobject(color=TEAL, stroke_width=2.2).set_points_as_corners([X(a, np.sin(2 * np.pi * f * a)) for a in tt]))
            g.add(VMobject(color=ACC, stroke_width=3.5).set_points_smoothly([X(a, np.sin(2 * np.pi * fa * a)) for a in tt[::4]]))
            g.add(VGroup(*[Dot(X(a, np.sin(2 * np.pi * f * a)), radius=0.07, color=ACC) for a in ts]))
            return g
        base = Line(O, O + np.array([W, 0, 0]), color=MUT, stroke_width=1.2)
        lt = T(tr("~true signal~ (continuous)", "~segnale vero~ (continuo)"), 17).move_to(O + np.array([1.8, 1.2, 0]))
        ls = T(tr("*samples* at f_{s} = 50 Hz", "*campioni* a f_{s} = 50 Hz"), 17).move_to(O + np.array([W - 1.8, 1.2, 0]))
        wv = always_redraw(wave)
        self.play(Create(base), FadeIn(lt), FadeIn(ls), FadeIn(wv), run_time=1.2)

        def readout():
            f = fT.get_value(); fa = abs(fa_(f))
            col = TEAL if f <= 25 else ACC
            return T(tr(f"true: **{f:.0f} Hz**   →   seen: **{fa:.0f} Hz**", f"vero: **{f:.0f} Hz**   →   visto: **{fa:.0f} Hz**"), 22, col=col).move_to(np.array([-2.4, -0.5, 0]))
        ro = always_redraw(readout); self.add(ro)
        # ruota "stroboscopica": gira alla frequenza apparente
        wc = np.array([4.7, 0.6, 0]); wr = 1.15
        Tl = 12.0; slow = 0.04
        phs = np.linspace(0, 1, 4001)
        fav = fa_(25 + 20 * np.cos(2 * np.pi * phs))
        ang = np.concatenate([[0], np.cumsum((fav[1:] + fav[:-1]) / 2 * np.diff(phs))]) * Tl * slow * 2 * np.pi
        ang = ang - ang[-1] * phs  # chiude il loop esattamente
        aT = ValueTracker(0.0)

        def wheel():
            a = aT.get_value()
            g = VGroup(Circle(radius=wr, color=FG, stroke_width=4).move_to(wc), Dot(wc, radius=0.08, color=FG))
            for k in range(4):
                th = a + k * PI / 2
                g.add(Line(wc, wc + wr * np.array([np.cos(th), np.sin(th), 0]), color=AMB if k == 0 else FG, stroke_width=4 if k == 0 else 2.5))
            return g
        wh = always_redraw(wheel)
        wl = T(tr("what the camera (ADC) sees", "ciò che vede la cinepresa (ADC)"), 16, MUT).move_to(wc + np.array([0, -1.5, 0]))
        self.play(FadeIn(wh), FadeIn(wl))
        fm = fcard(r"f_s > 2\,f_{max} \qquad f_{Nyquist} = f_s/2", CARD2, 0.8).move_to(np.array([-3.4, -1.45, 0]))
        bl = bullets([tr("Above f_{s}/2 frequencies ++fold back++ as fake slow ones (*aliasing*): the anti-alias low-pass must act ++before++ the ADC.", "Sopra f_{s}/2 le frequenze si ++ripiegano++ come false lente (*aliasing*): il passa-basso anti-alias deve agire ++prima++ dell'ADC."),
                      tr("Typical EEG: f_{s} = 250–1000 Hz.", "EEG tipico: f_{s} = 250–1000 Hz.")], 16, n=52, gap=0.15).move_to(np.array([2.9, -1.55, 0]))
        mt = metaphor(tr("the ++wagon-wheel effect++ in films: a fast wheel seems to turn slowly backwards.", "l'++effetto ruota di carro++ nei film: una ruota veloce sembra girare lenta all'indietro."), 16).move_to(np.array([0, -3.0, 0]))
        self.play(FadeIn(fm), FadeIn(bl), FadeIn(mt))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject()
        drv.add_updater(lambda m: (fT.set_value(25 + 20 * np.cos(2 * np.pi * ph.get_value())), aT.set_value(float(np.interp(ph.get_value(), phs, ang)))))
        self.add(drv); loop_play(self, ph, Tl); drv.clear_updaters(); wv.clear_updaters(); ro.clear_updaters(); wh.clear_updaters()

        # ---------------------------------------------------------- 14 quantizzazione (bit che cambiano)
        self.new(tr("Digitisation (2)", "Digitalizzazione (2)"), tr("Amplitude resolution and dynamic range", "Risoluzione in ampiezza e dinamica"))
        Wq = 6.6; Hq = 1.5; Oq = np.array([-6.3, 0.35, 0])
        tq = np.linspace(0, 1, 900)
        xq = 0.75 * np.sin(2 * np.pi * 1.3 * tq) + 0.22 * np.sin(2 * np.pi * 4.1 * tq + 1)
        bT = ValueTracker(3)
        Pq = lambda a, y: Oq + np.array([a * Wq, Hq * y, 0])

        def quant():
            b = int(round(bT.get_value())); n = 2 ** b
            q = np.round((xq + 1) / 2 * (n - 1)) / (n - 1) * 2 - 1
            g = VGroup()
            if b <= 4:
                for k in range(n):
                    y = k / (n - 1) * 2 - 1
                    g.add(Line(Pq(0, y), Pq(1, y), color=MUT, stroke_width=0.8, stroke_opacity=0.5))
            g.add(VMobject(color=TEAL, stroke_width=2.5).set_points_as_corners([Pq(a, y) for a, y in zip(tq, xq)]))
            g.add(VMobject(color=ACC, stroke_width=3).set_points_as_corners([Pq(a, y) for a, y in zip(tq, q)]))
            g.add(T(tr(f"**{b} bit** → {n} levels", f"**{b} bit** → {n} livelli"), 24, col=ACC).move_to(np.array([3.4, 0.6, 0])))
            return g
        qz = always_redraw(quant)
        rg = VGroup(DoubleArrow(Pq(-0.04, -1), Pq(-0.04, 1), buff=0, color=MUT, stroke_width=2, tip_length=0.14), T("range", 15, MUT).move_to(Pq(-0.04, 1.2)))
        self.play(FadeIn(rg), FadeIn(qz), run_time=1.0)
        fm = fcard(r"\mathrm{LSB} = \mathrm{range}/2^{\,bits}", CARD2, 0.9).move_to(np.array([3.4, 1.75, 0]))
        cmp_ = VGroup(T(tr("16 bit: ±3 mV → ≈0.1 µV", "16 bit: ±3 mV → ≈0,1 µV"), 18), T(tr("24 bit: ±400 mV → ≈0.05 µV", "24 bit: ±400 mV → ≈0,05 µV"), 18)).arrange(DOWN, buff=0.15).move_to(np.array([3.4, -0.45, 0]))
        self.play(FadeIn(fm), FadeIn(cmp_))
        bl = bullets([tr("The range must contain large ++DC offsets++ and artifacts without *clipping*.", "Il range deve contenere grandi ++offset DC++ e artefatti senza *clipping*."),
                      tr("24-bit amplifiers record ++DC-coupled++: drifts are removed offline.", "Gli amplificatori a 24 bit registrano in ++DC++: le derive si tolgono offline."),
                      tr("Resolution ≪ noise floor (≈0.5–1 µV): bits are rarely the bottleneck.", "Risoluzione ≪ rumore di fondo (≈0,5–1 µV): i bit raramente sono il collo di bottiglia.")], 17, n=90, gap=0.16).move_to(np.array([0, -2.45, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.4)
        loop_start(self)
        ph = ValueTracker(0.0)
        seq = [3, 4, 5, 6, 5, 4, 3, 2]
        drv = Mobject(); drv.add_updater(lambda m: bT.set_value(seq[min(int(ph.get_value() * 8), 7)]))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); qz.clear_updaters()

        # ---------------------------------------------------------- 15 filtri: il passa-alto che deforma un'onda lenta
        self.new(tr("Digitisation (3)", "Digitalizzazione (3)"), tr("Filters: useful but dangerous", "Filtri: utili ma pericolosi"))
        Wf = 5.8; Hf = 1.7; Of = np.array([-6.3, 0.0, 0])
        fr = np.logspace(-2, np.log10(250), 300)
        lxf = lambda v: E.logpos(v, 0.01, 250, Wf)
        fcT = ValueTracker(0.01)
        axf = E.axes(Of, Wf + 0.2, Hf + 0.3, "", tr("gain", "guadagno"))
        tks = VGroup(*[VGroup(Line(Of + np.array([lxf(v), -0.05, 0]), Of + np.array([lxf(v), 0.05, 0]), color=FG, stroke_width=2), T(s_, 13, MUT).move_to(Of + np.array([lxf(v), -0.25, 0])))
                       for v, s_ in ((0.01, "0.01"), (0.1, "0.1"), (1, "1"), (10, "10"), (100, "100 Hz"))])

        def resp():
            fc = fcT.get_value()
            g = (1 / (1 + (fc / fr) ** 4)) * (1 / (1 + (fr / 40) ** 8))
            return VGroup(VMobject(color=TEAL, stroke_width=3.5).set_points_smoothly([Of + np.array([lxf(v), Hf * a, 0]) for v, a in zip(fr, g)]),
                          DashedLine(Of + np.array([lxf(fc), 0, 0]), Of + np.array([lxf(fc), Hf + 0.1, 0]), color=ACC, stroke_width=2))
        # onda lenta tipo P300/LPP e sua versione filtrata
        fsx = 100.0
        tx = np.arange(-10, 12, 1 / fsx)
        erp = 8 * np.exp(-0.5 * ((tx - 0.55) / 0.22) ** 2)
        fcs = np.logspace(-2, np.log10(2.0), 121)
        filt = np.array([sosfiltfilt(butter(2, fc, "highpass", fs=fsx, output="sos"), erp) for fc in fcs])
        m = (tx >= -0.2) & (tx <= 1.6)
        Ot = np.array([-6.3, -2.5, 0]); Wt_ = 5.8; ht = 0.14
        Pt = lambda a, y: Ot + np.array([(a + 0.2) / 1.8 * Wt_, ht * y, 0])
        zero = Line(Pt(-0.2, 0), Pt(1.6, 0), color=MUT, stroke_width=1.2)
        orig = DashedVMobject(VMobject(color=FG, stroke_width=2).set_points_as_corners([Pt(a, y) for a, y in zip(tx[m], erp[m])]), num_dashes=40)

        def filtered():
            k = int(np.argmin(np.abs(np.log10(fcs) - np.log10(fcT.get_value()))))
            g = VGroup(VMobject(color=ACC, stroke_width=3.5).set_points_as_corners([Pt(a, y) for a, y in zip(tx[m], filt[k][m])]))
            g.add(T(tr(f"high-pass f_{{c}} = **{fcs[k]:.2f} Hz**", f"passa-alto f_{{c}} = **{fcs[k]:.2f} Hz**").replace(".", "." if LANG == "en" else ","), 19, col=ACC).move_to(np.array([-3.4, -0.85, 0])))
            return g
        rs = always_redraw(resp); fl = always_redraw(filtered)
        lbl = VGroup(T(tr("frequency response", "risposta in frequenza"), 15, MUT).move_to(Of + np.array([Wf / 2 + 0.6, Hf + 0.35, 0])),
                     T(tr("a slow ERP (dashed) after filtering", "un ERP lento (tratteggio) dopo il filtro"), 15, MUT).move_to(Ot + np.array([Wt_ / 2, -0.55, 0])))
        self.play(Create(axf), FadeIn(tks), FadeIn(rs), FadeIn(lbl[0]), run_time=1.0)
        self.play(Create(zero), Create(orig), FadeIn(fl), FadeIn(lbl[1]), run_time=1.0)
        bl = bullets([tr("*High-pass*: removes drifts; > 0.1–0.3 Hz ++distorts slow ERPs++ and creates artificial peaks (Acunzo et al., 2012; Tanner et al., 2015).", "*Passa-alto*: rimuove le derive; > 0,1–0,3 Hz ++distorce gli ERP lenti++ e crea picchi artificiali (Acunzo et al., 2012; Tanner et al., 2015)."),
                      tr("*Low-pass*: removes EMG; one is always before the ADC.", "*Passa-basso*: rimuove l'EMG; uno è sempre prima dell'ADC."),
                      tr("*Notch*: removes 50/60 Hz but ++rings++ in time.", "*Notch*: toglie 50/60 Hz ma ++oscilla++ nel tempo."),
                      tr("~Record wide-band, filter offline, report type, order and cut-off~ (Widmann et al., 2015).", "~Registrare a banda larga, filtrare offline, riportare tipo, ordine e taglio~ (Widmann et al., 2015).")], 16, n=42, gap=0.2).move_to(np.array([3.7, 0.0, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.4)
        mt = metaphor(tr("a filter is a ++sieve++: it keeps the flour, not the stones — but it also changes the texture.", "un filtro è un ++setaccio++: tiene la farina, non i sassi — ma cambia anche la consistenza."), 15, n=56).move_to(np.array([3.7, -2.75, 0]))
        self.play(FadeIn(mt))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: fcT.set_value(10 ** (-2 + np.log10(200) * (0.5 - 0.5 * np.cos(2 * np.pi * ph.get_value())))))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); rs.clear_updaters(); fl.clear_updaters()

        # ---------------------------------------------------------- 16 sezione
        self.new(); section_title(self, 4, tr("Artifacts", "Artefatti"))

        # ---------------------------------------------------------- 17 galleria di artefatti (tracce che scorrono)
        self.new(tr("Artifacts (1)", "Artefatti (1)"), tr("A gallery of artifacts", "Una galleria di artefatti"))
        t, chans = F4.artifact_signals()
        Wa = 8.0; xa = -5.5; hs = 0.0042
        Os = [np.array([xa, 1.75 - 0.82 * k, 0]) for k in range(6)]
        names = VGroup(*[T(n_, 16, MUT).move_to(O_ + np.array([-0.45, 0, 0])) for (n_, _), O_ in zip(chans, Os)])
        tr0 = VGroup(*[E.window_trace(t, x, 0.0, 3.0, O_, Wa, hs, TEAL, 1.6) for (_, x), O_ in zip(chans, Os)])
        self.play(FadeIn(names), LaggedStart(*[Create(x) for x in tr0], lag_ratio=0.15), run_time=1.8)
        leg = [(tr("Blinks", "Ammiccamenti"), tr("frontal, 100–200 µV", "frontali, 100–200 µV")), (tr("Saccades", "Saccadi"), tr("box-shaped, F7/F8", "a gradino, F7/F8")),
               ("EMG", tr("temporal, > 20 Hz", "temporale, > 20 Hz")), ("ECG", tr("regular peaks ≈1 Hz", "picchi regolari ≈1 Hz")),
               (tr("Line noise", "Rete"), "50/60 Hz"), (tr("Electrode pop", "Pop dell'elettrodo"), tr("sudden step", "gradino improvviso"))]
        lg = VGroup(*[T(f"~{a_}~: {b_}", 16, n=30) for a_, b_ in leg]).arrange(DOWN, aligned_edge=LEFT, buff=0.33).move_to(np.array([4.9, -0.3, 0]))
        self.play(LaggedStart(*[FadeIn(x) for x in lg], lag_ratio=0.15), run_time=1.5)
        scroll_group(self, [(t, x) for _, x in chans], Os, Wa, hs, 3.0, [TEAL] * 6, 6.0, 1.6, old=tr0)

        # ---------------------------------------------------------- 18 occhi: il dipolo corneo-retinico (dal vivo)
        self.new(tr("Artifacts (2)", "Artefatti (2)"), tr("Eyes and muscles: the biggest offenders", "Occhi e muscoli: i principali colpevoli"))
        hc = np.array([-3.6, -0.55, 0]); Rh = 2.1
        eyes = [hc + np.array([s * 0.36 * Rh, 1.0 * Rh, 0]) for s in (-1, 1)]
        eln = ["Fp1", "Fp2", "F7", "F8", "F3", "F4", "Fz"]
        epos = {n_: hc + E.el2d(n_, Rh) for n_ in eln}
        Tl = 8.0
        phs = np.linspace(0, 1, 801)
        thv = np.radians(28) * (smooth_step(phs, 0.08) - smooth_step(phs, 0.3) - smooth_step(phs, 0.45) + smooth_step(phs, 0.67))
        blv = np.exp(-0.5 * ((phs - 0.85) / 0.025) ** 2)

        def pots(th, bl_):
            out = {}
            for n_ in eln:
                v = 0.0
                for e in eyes:
                    d = epos[n_] - e; r = np.linalg.norm(d)
                    p = np.array([np.sin(th), np.cos(th), 0]); p0 = np.array([0, 1, 0])
                    v += np.dot(p - p0, d) / r ** 3
                    v += 4.0 * bl_ * np.exp(-r / 1.2)
                out[n_] = v
            return out
        allv = [pots(a, b) for a, b in zip(thv, blv)]
        vmax = max(abs(v) for d in allv for v in d.values())
        heog = np.array([d["F8"] - d["F7"] for d in allv]); heog = heog / np.abs(heog).max()
        veog = np.array([(d["Fp1"] + d["Fp2"]) / 2 for d in allv]); veog = veog / np.abs(veog).max()
        phT = ValueTracker(0.0)

        def head_live():
            u = phT.get_value(); th = float(np.interp(u, phs, thv)); b = float(np.interp(u, phs, blv))
            v = pots(th, b)
            g = VGroup(E.head(hc, Rh))
            for e in eyes:
                d = np.array([np.sin(th), np.cos(th), 0])
                g.add(Circle(radius=0.3, color=FG, stroke_width=2.5, fill_color=BG_, fill_opacity=1).move_to(e))
                g.add(Dot(e + 0.24 * d, radius=0.09, color=ACC), T("+", 14, ACC).move_to(e + 0.47 * d), T("−", 14, TEAL).move_to(e - 0.47 * d))
                g.add(Line(e + 0.3 * np.array([-1, 0.1, 0]), e + 0.3 * np.array([1, 0.1, 0]), color=AMB, stroke_width=5).set_opacity(min(1, 3 * b)))
            for n_ in eln:
                col = hx(E.cmap_rdbu(np.array(v[n_] / vmax * 1.3)))
                g.add(Circle(radius=0.26, color=FG, stroke_width=1.5, fill_color=col, fill_opacity=1).move_to(epos[n_]))
                g.add(T(n_, 13, "#1A2340").move_to(epos[n_]))
            return g
        Ow = 0.8; Ww = 5.6
        Pw = lambda u, y, y0: np.array([Ow + u * Ww, y0 + 0.75 * y, 0])
        cH = VMobject(color=ACC, stroke_width=3).set_points_as_corners([Pw(u, y, 1.2) for u, y in zip(phs, heog)])
        cV = VMobject(color=TEAL, stroke_width=3).set_points_as_corners([Pw(u, y, -0.55) for u, y in zip(phs, veog)])
        lH = T(tr("HEOG = F8 − F7 (saccades)", "HEOG = F8 − F7 (saccadi)"), 16, ACC).move_to(np.array([Ow + Ww / 2, 2.2, 0]))
        lV = T(tr("frontal (Fp1+Fp2)/2 (blink)", "frontale (Fp1+Fp2)/2 (ammiccamento)"), 16, TEAL).move_to(np.array([Ow + Ww / 2, 0.35, 0]))
        hl = always_redraw(head_live)
        self.play(FadeIn(hl), run_time=1.0)
        self.play(Create(cH), Create(cV), FadeIn(lH), FadeIn(lV), run_time=1.2)
        bl = bullets([tr("The eye is a ++dipole++ (cornea +, retina −): saccades → opposite steps at F7/F8; blinks → frontal positivity.", "L'occhio è un ++dipolo++ (cornea +, retina −): saccadi → gradini opposti in F7/F8; ammiccamenti → positività frontale."),
                      tr("*Muscles*: broadband > 20 Hz, temporal; microsaccades mimic ++induced gamma++ (Yuval-Greenberg et al., 2008).", "*Muscoli*: banda larga > 20 Hz, temporali; le microsaccadi imitano la ++gamma indotta++ (Yuval-Greenberg et al., 2008).")], 15, n=62, gap=0.16).move_to(np.array([3.6, -2.35, 0]))
        self.play(FadeIn(bl))
        cur = always_redraw(lambda: Line(Pw(phT.get_value(), -1.25, -0.55), Pw(phT.get_value(), 1.25, 1.2) + np.array([0, 0.1, 0]), color=AMB, stroke_width=2))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: phT.set_value(ph.get_value()))
        self.add(drv, cur); loop_play(self, ph, Tl); drv.clear_updaters(); hl.clear_updaters(); cur.clear_updaters()

        # ---------------------------------------------------------- 19 rumore di rete: il picco cresce con l'impedenza
        self.new(tr("Artifacts (3)", "Artefatti (3)"), tr("Line noise and its harmonics", "Rumore di rete e armoniche"))
        tl_, xl_ = E.periodic_eeg(20.0, seed=3, peaks=((10, 1, 1.2),), slope=2.2)
        frq, pw = welch(xl_, 250, nperseg=1000)
        mm = (frq >= 1) & (frq <= 120); frq, pw = frq[mm], pw[mm]
        Wl = 5.8; Hl = 3.4; Ol = np.array([-6.3, -2.3, 0])
        lo_, hi_ = np.log10(pw.min()), np.log10(pw.max() * 30)
        zT = ValueTracker(5.0)

        def spec():
            z = zT.get_value(); a = (z / 50) ** 2 * pw.max() * 25
            p = pw + a * np.exp(-0.5 * ((frq - 50) / 0.5) ** 2) + 0.2 * a * np.exp(-0.5 * ((frq - 100) / 0.5) ** 2)
            y = (np.log10(p) - lo_) / (hi_ - lo_) * Hl
            g = VGroup(VMobject(color=TEAL, stroke_width=3).set_points_as_corners([Ol + np.array([f_ / 120 * Wl, b_, 0]) for f_, b_ in zip(frq, y)]))
            g.add(T(f"Z = **{z:.0f} kΩ**", 22, col=ACC if z > 20 else TEAL).move_to(Ol + np.array([Wl * 0.55, Hl + 0.25, 0])))
            return g
        axl = E.axes(Ol, Wl + 0.2, Hl + 0.4, tr("frequency (Hz)", "frequenza (Hz)"), tr("power (log)", "potenza (log)"))
        tkl = VGroup(*[T(str(v), 13, MUT).move_to(Ol + np.array([v / 120 * Wl, -0.25, 0])) for v in (0, 25, 50, 75, 100)])
        sp = always_redraw(spec)
        self.play(Create(axl), FadeIn(tkl), FadeIn(sp), run_time=1.0)
        bl = bullets([tr("Mains (50 Hz in Europe) couples into cables and body: worse with ++high or unbalanced impedance++.", "La rete (50 Hz in Europa) si accoppia a cavi e corpo: peggiora con impedenze ++alte o sbilanciate++."),
                      tr("Sources: lamps, monitors, power supplies; keep cables short.", "Sorgenti: lampade, monitor, alimentatori; cavi corti."),
                      tr("Removal: notch, spectrum interpolation, CleanLine, ++Zapline++ (de Cheveigné, 2020).", "Rimozione: notch, interpolazione spettrale, CleanLine, ++Zapline++ (de Cheveigné, 2020)."),
                      tr("A 50 Hz peak ≫ neighbours = ~check that electrode!~", "Un picco a 50 Hz ≫ vicini = ~controllare quell'elettrodo!~")], 17, n=44, gap=0.24).move_to(np.array([3.6, -0.3, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.4)
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: zT.set_value(27.5 - 22.5 * np.cos(2 * np.pi * ph.get_value())))
        self.add(drv); loop_play(self, ph, 6.0); drv.clear_updaters(); sp.clear_updaters()

        # ---------------------------------------------------------- 20 sezione
        self.new(); section_title(self, 5, tr("Good recording practice", "Buona pratica di registrazione"))

        # ---------------------------------------------------------- 21 checklist
        self.new(tr("Good practice (1)", "Buona pratica (1)"), tr("A recording checklist", "Una checklist di registrazione"))
        g = rows_mob([tr("Quiet, dimly lit, electrically clean room; participant comfortable and informed.", "Stanza silenziosa, poco illuminata, elettricamente pulita; partecipante comodo e informato."),
                      tr("Measure head size, centre the cap (Cz at the vertex), log impedances.", "Misurare la testa, centrare la cuffia (Cz al vertice), annotare le impedenze."),
                      tr("Check raw data: blinks, jaw clench, eyes closed → alpha (a quick \"sanity test\").", "Controllare i dati grezzi: ammiccamenti, mandibola, occhi chiusi → alfa (\"test di sanità\")."),
                      tr("Resting blocks (eyes open/closed) before tasks; breaks against drowsiness.", "Blocchi di riposo (occhi aperti/chiusi) prima dei compiti; pause contro la sonnolenza."),
                      tr("Test triggers with a ++photodiode++: measure the real stimulus–trigger delay.", "Testare i trigger con un ++fotodiodo++: misurare il ritardo reale stimolo–trigger."),
                      tr("Lab notebook: bad channels, events, anything unusual.", "Diario di laboratorio: canali cattivi, eventi, tutto ciò che è insolito.")], 19, n=90, h=0.66, gap=0.13, col=ACC).shift(DOWN * 0.4)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.2), run_time=2.5)

        # ---------------------------------------------------------- 22 BIDS
        self.new(tr("Good practice (2)", "Buona pratica (2)"), tr("Data formats and sharing: EEG-BIDS", "Formati e condivisione: EEG-BIDS"))
        bl = bullets([tr("Vendor formats vary (BrainVision, BDF, EDF, EGI, CNT…): always keep the ++raw++ files.", "I formati variano (BrainVision, BDF, EDF, EGI, CNT…): conservare sempre i file ++grezzi++."),
                      tr("*EEG-BIDS* (Pernet et al., 2019): standard folders for subject/session/task, electrodes, channels, events, sidecar JSON.", "*EEG-BIDS* (Pernet et al., 2019): cartelle standard per soggetto/sessione/compito, elettrodi, canali, eventi, JSON."),
                      tr("Benefits: ++reproducibility++, automatic pipelines, sharing on OpenNeuro.", "Vantaggi: ++riproducibilità++, pipeline automatiche, condivisione su OpenNeuro."),
                      tr("Tools: MNE-BIDS (Python), bids-matlab-tools / EEGLAB plug-in.", "Strumenti: MNE-BIDS (Python), bids-matlab-tools / plug-in EEGLAB.")], 18, n=44, gap=0.26).move_to(np.array([-3.0, -0.4, 0]))
        tree = ["sub-01/", "  eeg/", "    sub-01_task-oddball_eeg.vhdr", "    sub-01_task-oddball_eeg.json", "    sub-01_task-oddball_channels.tsv",
                "    sub-01_task-oddball_events.tsv", "    sub-01_electrodes.tsv", "dataset_description.json", "participants.tsv"]
        tl = VGroup(*[Text(s_, font="DejaVu Sans Mono", font_size=18, color=TEAL if not s_.startswith(" ") else FG) for s_ in tree]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        tc = card(tl).move_to(np.array([3.6, -0.4, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.4)
        self.play(FadeIn(tc[0]), LaggedStart(*[FadeIn(x, shift=RIGHT * 0.1) for x in tl], lag_ratio=0.12), run_time=1.6)

        # ---------------------------------------------------------- 23 domande
        self.new(tr("Check your understanding", "Verifica"), tr("Three questions", "Tre domande"))
        g = rows_mob([tr("You sample at 100 Hz without anti-aliasing and there is 60 Hz noise. What appears in your data?", "Campioni a 100 Hz senza anti-aliasing e c'è rumore a 60 Hz. Che cosa compare nei dati?"),
                      tr("Why does 50 Hz noise increase when one electrode has much higher impedance?", "Perché il rumore a 50 Hz aumenta se un elettrodo ha impedenza molto più alta?"),
                      tr("Gamma increases at T7/T8 in a difficult task: two non-neural explanations?", "Aumento di gamma in T7/T8 in un compito difficile: due spiegazioni non neurali?")], 21, n=84, h=1.05, gap=0.35, col=ACC).shift(DOWN * 0.3)
        for r_ in g: self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.7)

        # ---------------------------------------------------------- 24 messaggi chiave
        self.new(tr("Take-home messages", "Messaggi chiave"), tr("Take-home messages", "Messaggi chiave"))
        g = rows_mob([tr("Good data are made at ++recording time++: impedance, montage, environment.", "I buoni dati si fanno ++in registrazione++: impedenza, montaggio, ambiente."),
                      tr("10-20 (and 10-10/10-5) give ++standard, relative++ positions.", "Il 10-20 (e 10-10/10-5) fornisce posizioni ++standard e relative++."),
                      tr("Differential amplifiers reject ++common-mode++ noise; there is ++no neutral reference++.", "Gli amplificatori differenziali respingono il ++modo comune++; ++non esiste un riferimento neutro++."),
                      tr("f_{s} > 2 f_{max} (++Nyquist++); filters help but ++distort++: report them.", "f_{s} > 2 f_{max} (++Nyquist++); i filtri aiutano ma ++distorcono++: riportarli."),
                      tr("Know your ++artifacts++ (eyes, muscles, heart, mains); store data in ++BIDS++.", "Conoscere gli ++artefatti++ (occhi, muscoli, cuore, rete); salvare in ++BIDS++.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 25 letture
        self.new(tr("Suggested reading", "Letture consigliate"), tr("Suggested reading", "Letture consigliate"))
        refs_slide(self, ["Luck (2014) *An Introduction to the Event-Related Potential Technique*, 2nd ed., MIT Press (ch. 5, 7).",
                          "Jasper (1958) *Electroencephalogr Clin Neurophysiol* 10:371–375.", "Oostenveld & Praamstra (2001) *Clin Neurophysiol* 112:713–719.",
                          "Kappenman & Luck (2010) *Psychophysiology* 47:888–904.", "Yao (2001) *Physiol Meas* 22:693–711.",
                          "Widmann, Schröger & Maess (2015) *J Neurosci Methods* 250:34–46.", "Tanner, Morgan-Short & Luck (2015) *Psychophysiology* 52:997–1009.",
                          "Yuval-Greenberg et al. (2008) *Neuron* 58:429–441.", "de Cheveigné (2020) *NeuroImage* 207:116356.",
                          "Keil et al. (2014) *Psychophysiology* 51:1–21.", "Pernet et al. (2019) *Sci Data* 6:103."], 17)
        self.end()
