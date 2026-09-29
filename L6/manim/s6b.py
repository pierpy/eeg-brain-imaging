from base import *
import figs6 as F6
from scipy.signal import spectrogram
from scipy.ndimage import gaussian_filter


def dec(v, n=2):
    s = f"{v:.{n}f}"
    return s if LANG == "en" else s.replace(".", ",")


def curve(pts, col, sw=3, smooth=False):
    m = VMobject(color=col, stroke_width=sw)
    return m.set_points_smoothly(pts) if smooth else m.set_points_as_corners(pts)


def img(Z, W, H, c, cmap="seq", vmin=None, vmax=None):
    return F6.mat_img(Z, W, H, c, cmap, vmin, vmax)


def analytic_band(x, fs, lo, hi):
    """segnale analitico in banda per un segnale periodico (filtro ideale in frequenza, circolare)."""
    X = np.fft.fft(x); f = np.fft.fftfreq(len(x), 1 / fs)
    H = ((f >= lo) & (f <= hi)) * 2.0
    return np.fft.ifft(X * H)


class B6_TF(Base):
    start_num = 13

    def construct(self):
        # ---------------------------------------------------------- 13 sezione
        self.new(first=True); section_title(self, 3, tr("Time-frequency analysis", "Analisi tempo-frequenza"))

        # ---------------------------------------------------------- 14 STFT: la finestra scorre e disegna gli spettrogrammi
        self.new(tr("Time-frequency (1)", "Tempo-frequenza (1)"), tr("STFT and the time–frequency trade-off", "STFT e il compromesso tempo–frequenza"))
        t, x = F6.test_signal()
        Ws = 12.4; Os = np.array([-6.2, 1.55, 0])
        sig = E.trace(t, x, Os, Ws, 0.28, FG, 1.3)
        Wm = 5.6; Hm = 2.5
        maps = []; frames = []
        for k, win in enumerate((0.125, 1.0)):
            fr, tt, S = F6.stft_map(win)
            c = np.array([-3.2 + 6.4 * k, -0.85, 0])
            maps.append(img(S, Wm, Hm, c, vmin=0, vmax=0.8))
            O_ = c - np.array([Wm / 2, Hm / 2, 0])
            frames.append(VGroup(F6.frame_axes(O_, Wm, Hm, [(0, "0"), (0.5, "2"), (1, "4 s")], [(0, "0"), (0.5, "20"), (1, "40 Hz")]),
                                 T(tr(f"window {int(win * 1000)} ms: " + ("sharp in time" if k == 0 else "sharp in frequency"), f"finestra {int(win * 1000)} ms: " + ("nitida nel tempo" if k == 0 else "nitida in frequenza")), 17, ACC if k == 0 else TEAL).move_to(c + np.array([0, Hm / 2 + 0.3, 0]))))
        uT = ValueTracker(1.0)
        BG = config.background_color

        def covers():
            u = uT.get_value(); g = VGroup()
            for k, win in enumerate((0.125, 1.0)):
                c = np.array([-3.2 + 6.4 * k, -0.85, 0])
                w = max((1 - u) * Wm, 0.001)
                g.add(Rectangle(width=w, height=Hm + 0.02, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(c + np.array([Wm / 2 - w / 2, 0, 0])))
            wx = Os + np.array([u * Ws, 0, 0])
            for k, win in enumerate((0.125, 1.0)):
                ww = win / 4.0 * Ws
                g.add(Rectangle(width=ww, height=0.8, stroke_width=2, stroke_color=ACC if k == 0 else TEAL, fill_opacity=0.08, fill_color=ACC if k == 0 else TEAL).move_to(wx))
            return g
        self.play(Create(sig), run_time=1.0)
        self.play(*[FadeIn(m) for m in maps], *[FadeIn(fr_) for fr_ in frames])
        fm = fcard(r"\Delta t\cdot\Delta f \geq 1/4\pi", CARD2, 0.65).move_to(np.array([0, -3.05, 0]))
        self.play(FadeIn(fm))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: uT.set_value(ph.get_value()))
        cz = always_redraw(covers)
        self.add(drv, cz); self.bring_to_front(*frames, fm); loop_play(self, ph, 8.0); drv.clear_updaters(); cz.clear_updaters()

        # ---------------------------------------------------------- 15 Morlet: la wavelet scorre e produce la potenza
        self.new(tr("Time-frequency (2)", "Tempo-frequenza (2)"), tr("Morlet wavelets: windows that scale with f", "Wavelet di Morlet: finestre che scalano con f"))
        fs = 250; D = 4.0; t = np.arange(0, D, 1 / fs)
        x = E.periodic_eeg(D, fs, seed=21, peaks=((10, 1.5, 0.2),), uv=6)[1] + 12 * np.exp(-0.5 * ((t - 2.0) / 0.45) ** 2) * np.sin(2 * np.pi * 10 * t)
        wt = np.arange(-0.5, 0.5, 1 / fs)
        w, s_ = F6.morlet(10, 6, wt)
        conv = np.convolve(np.concatenate([x, x, x]), w, "same")[len(x):2 * len(x)] / fs
        pw = np.abs(conv) ** 2; pw /= pw.max()
        Wx = 12.0; Ox = np.array([-6.0, 1.0, 0]); hx = 0.04
        X = lambda tt, y, O_=Ox, h=hx: O_ + np.array([tt / D * Wx, h * y, 0])
        sig = E.trace(t, x, Ox, Wx, hx, FG, 1.5)
        Op = np.array([-6.0, -2.3, 0])
        cT = ValueTracker(0.5)

        def slide():
            c = cT.get_value()
            g = VGroup()
            g.add(curve([X(c + a, 14 * b.real) for a, b in zip(wt, w)], ACC, 3))
            g.add(curve([X(c + a, 14 * abs(b)) for a, b in zip(wt, w)], AMB, 1.5))
            m = t <= c
            if m.sum() > 2:
                g.add(curve([Op + np.array([a / D * Wx, 1.35 * b, 0]) for a, b in zip(t[m], pw[m])], TEAL, 3.5))
            g.add(Dot(Op + np.array([c / D * Wx, 1.35 * np.interp(c, t, pw), 0]), radius=0.07, color=TEAL))
            return g
        axp = VGroup(Line(Op, Op + np.array([Wx, 0, 0]), color=MUT, stroke_width=1.5), T(tr("10-Hz power |z(t)|²", "potenza a 10 Hz |z(t)|²"), 17, TEAL).move_to(Op + np.array([Wx - 1.5, 0.45, 0])))
        sz = always_redraw(slide)
        self.play(Create(sig), Create(axp), FadeIn(sz), run_time=1.2)
        fm = fcard(r"w(t)=e^{i2\pi f t}\,e^{-t^2/2\sigma^2},\quad \sigma_t=\frac{n}{2\pi f}", CARD2, 0.7).move_to(np.array([2.5, -0.05, 0]))
        cap = T(tr("sine × Gaussian, ++n cycles++ at every f", "sinusoide × gaussiana, ++n cicli++ a ogni f"), 17).move_to(np.array([-3.4, -0.05, 0]))
        self.play(FadeIn(fm), FadeIn(cap))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: cT.set_value(0.5 + 3.0 * ph.get_value()))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); sz.clear_updaters()

        # ---------------------------------------------------------- 16 quanti cicli: tempo vs frequenza
        self.new(tr("Time-frequency (3)", "Tempo-frequenza (3)"), tr("How many cycles?", "Quanti cicli?"))
        nT = ValueTracker(3.0)
        wt = np.linspace(-0.6, 0.6, 900)
        Ow = np.array([-3.4, 0.6, 0]); Ww = 5.6
        Of = np.array([1.2, -0.6, 0]); Wf = 5.2; Hf = 2.3
        ff = np.linspace(0, 20, 300)

        def cyc():
            n = nT.get_value(); w, s = F6.morlet(10, n, wt)
            sf = 1 / (2 * np.pi * s)
            g = VGroup(curve([Ow + np.array([a / 1.2 * Ww, 1.1 * b.real, 0]) for a, b in zip(wt, w)], TEAL, 2.5),
                       curve([Ow + np.array([a / 1.2 * Ww, 1.1 * abs(b), 0]) for a, b in zip(wt, w)], ACC, 2))
            g.add(curve([Of + np.array([f / 20 * Wf, Hf * np.exp(-0.5 * ((f - 10) / sf) ** 2), 0]) for f in ff], ACC, 3.5))
            g.add(T(tr(f"n = **{dec(n, 1)}** cycles at 10 Hz", f"n = **{dec(n, 1)}** cicli a 10 Hz"), 22, AMB).move_to(np.array([0, 2.05, 0])))
            g.add(T(f"σ_t = **{dec(s * 1000, 0)} ms**", 19, TEAL).move_to(Ow + np.array([0, -1.45, 0])))
            g.add(T(f"σ_f = **{dec(sf, 2)} Hz**", 19, ACC).move_to(Of + np.array([Wf / 2, -0.6, 0])))
            return g
        axc = VGroup(Line(Of, Of + np.array([Wf + 0.2, 0, 0]), color=MUT, stroke_width=1.5), *[T(str(v), 13, MUT).move_to(Of + np.array([v / 20 * Wf, -0.25, 0])) for v in (0, 10, 20)],
                     T(tr("time domain", "dominio del tempo"), 15, MUT).move_to(Ow + np.array([0, 1.3, 0])), T(tr("frequency domain", "dominio delle frequenze"), 15, MUT).move_to(Of + np.array([Wf / 2, Hf + 0.3, 0])))
        cz = always_redraw(cyc)
        self.play(FadeIn(axc), FadeIn(cz))
        g = rows_mob([tr("Few cycles: sharp in ++time++; many cycles: sharp in ++frequency++.", "Pochi cicli: nitido nel ++tempo++; molti cicli: nitido in ++frequenza++."),
                      tr("Common: log-spaced frequencies, cycles ++3 → 10++; report the ++FWHM++ (Cohen, 2019).", "Comune: frequenze logaritmiche, cicli ++3 → 10++; riportare la ++FWHM++ (Cohen, 2019)."),
                      tr("*Edge effects*: pad epochs by ≈ 1.5 wavelet lengths.", "*Effetti di bordo*: estendere le epoche di ≈ 1,5 lunghezze di wavelet.")], 17, n=100, h=0.55, gap=0.1, col=ACC).move_to(np.array([0, -2.55, 0]))
        self.play(LaggedStart(*[FadeIn(r_) for r_ in g], lag_ratio=0.2), run_time=1.2)
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: nT.set_value(3.0 * (12 / 3.0) ** (0.5 - 0.5 * np.cos(2 * np.pi * ph.get_value()))))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); cz.clear_updaters()

        # ---------------------------------------------------------- 17 mappa TF: potenza grezza -> dB rispetto alla baseline
        self.new(tr("Time-frequency (4)", "Tempo-frequenza (4)"), tr("TF maps and baseline normalisation", "Mappe TF e normalizzazione alla baseline"))
        Z = F6.tf_model()
        Fg = F6.TF_F[:, None]
        raw = np.log10((1 / Fg ** 1.6) * 10 ** (Z / 10))
        Wm = 6.6; Hm = 3.4; cm = np.array([-2.6, -0.3, 0]); Om = cm - np.array([Wm / 2, Hm / 2, 0])
        fy = lambda v: E.logpos(v, 2, 40, 1.0)
        ax = F6.frame_axes(Om, Wm, Hm, [((v + 0.5) / 2.0, s) for v, s in ((-0.5, "−0.5"), (0, "0"), (0.5, "0.5"), (1.0, "1"), (1.5, "1.5 s"))], [(fy(v), str(v)) for v in (2, 4, 10, 20, 40)], "", "Hz", col=FG)
        m_raw = img(raw, Wm, Hm, cm)
        m_db = img(Z, Wm, Hm, cm, cmap="div", vmax=3.0)
        l_raw = T(tr("raw power: dominated by 1/f", "potenza grezza: dominata da 1/f"), 19, AMB).move_to(cm + np.array([0, Hm / 2 + 0.3, 0]))
        l_db = T(tr("dB vs baseline (−400…−100 ms): ERD/ERS appear", "dB rispetto alla baseline (−400…−100 ms): compaiono ERD/ERS"), 19, AMB).move_to(l_raw)
        bl = Rectangle(width=0.3 / 2.0 * Wm, height=Hm, stroke_width=2, stroke_color=AMB, fill_opacity=0).move_to(Om + np.array([(0.25 / 2.0) * Wm, Hm / 2, 0]))
        z0 = DashedLine(Om + np.array([0.25 * Wm, 0, 0]), Om + np.array([0.25 * Wm, Hm, 0]), color=FG, stroke_width=2)
        self.play(FadeIn(m_raw), Create(ax), FadeIn(l_raw), Create(z0), run_time=1.2)
        self.play(Create(bl))
        fm = fcard(r"\mathrm{dB}(t,f)=10\log_{10}\frac{P(t,f)}{P_{base}(f)}", CARD2, 0.7).move_to(np.array([4.2, 1.5, 0]))
        self.play(FadeIn(fm))
        self.next_slide()
        self.play(FadeIn(m_db), FadeOut(m_raw), FadeOut(l_raw), FadeIn(l_db), run_time=1.5)
        self.bring_to_front(z0, bl)
        labs = VGroup(*[T(s, 15, "#1A2340").move_to(Om + np.array([(tt + 0.5) / 2 * Wm, fy(fq) * Hm + 0.3, 0])) for tt, fq, s in ((0.25, 5, "theta ERS"), (0.75, 10.5, "alpha ERD"), (1.25, 20, tr("beta rebound", "rebound beta")))])
        bl2 = bullets([tr("*ERD* = decrease (blue), *ERS* = increase (red) (Pfurtscheller & Lopes da Silva, 1999).", "*ERD* = diminuzione (blu), *ERS* = aumento (rosso) (Pfurtscheller & Lopes da Silva, 1999)."),
                       tr("dB, % change or z-score: choose one, ++report it++.", "dB, variazione % o z-score: sceglierne uno e ++riportarlo++.")], 16, n=34, gap=0.25).move_to(np.array([4.3, -0.8, 0]))
        self.play(FadeIn(labs), FadeIn(bl2))

        # ---------------------------------------------------------- 18 evocato vs indotto: i trial si accumulano
        self.new(tr("Time-frequency (5)", "Tempo-frequenza (5)"), tr("Evoked versus induced activity", "Attività evocata e indotta"))
        te, XE = F6.trials_ev_ind(60, jitter=False)
        _, XI = F6.trials_ev_ind(60, jitter=True)
        from scipy.signal import hilbert
        PE = np.abs(hilbert(XE, axis=1)) ** 2; PI_ = np.abs(hilbert(XI, axis=1)) ** 2
        Wt = 4.8; xs = [-6.1, 1.4]
        nT = ValueTracker(1)

        def evi():
            n = max(int(nT.get_value()), 1)
            g = VGroup()
            for k, (Xk, Pk, col) in enumerate(((XE, PE, ACC), (XI, PI_, TEAL))):
                x0 = xs[k]
                g.add(E.trace(te, Xk[n - 1], np.array([x0, 1.2, 0]), Wt, 0.35, MUT, 1.3))
                g.add(E.trace(te, Xk[:n].mean(0), np.array([x0, -0.55, 0]), Wt, 0.5, col, 3))
                pm = Pk[:n].mean(0)
                g.add(E.trace(te, pm / 1.0, np.array([x0, -2.6, 0]), Wt, 0.9, AMB, 3))
            g.add(T(tr(f"trials: **{n}**", f"trial: **{n}**"), 20, AMB).move_to(np.array([0, 2.1, 0])))
            return g
        heads = VGroup(T(tr("~evoked~ (phase-locked)", "~evocata~ (agganciata in fase)"), 18).move_to(np.array([xs[0] + Wt / 2, 1.85, 0])),
                       T(tr("~induced~ (phase-jittered)", "~indotta~ (fase variabile)"), 18).move_to(np.array([xs[1] + Wt / 2, 1.85, 0])))
        rl = VGroup(*[T(s, 15, MUT).move_to(np.array([0.15, y, 0])) for s, y in ((tr("single trial", "singolo trial"), 1.2), (tr("average\n(ERP)", "media\n(ERP)"), -0.55), (tr("average\nof power", "media della\npotenza"), -2.2))])
        ez = always_redraw(evi)
        self.play(FadeIn(heads), FadeIn(rl), FadeIn(ez))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: nT.set_value(1 + 59 * ph.get_value()))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); ez.clear_updaters()

        # ---------------------------------------------------------- 19 sezione
        self.new(); section_title(self, 4, tr("Phase and coupling", "Fase e accoppiamento"))

        # ---------------------------------------------------------- 20 Hilbert: il fasore analitico
        self.new(tr("Phase (1)", "Fase (1)"), tr("Band-pass + Hilbert: amplitude and phase", "Passa-banda + Hilbert: ampiezza e fase"))
        fs = 250; D = 4.0; t, x = E.periodic_eeg(D, fs, seed=12, peaks=((10, 0.8, 2.0),), uv=20)
        z = analytic_band(x, fs, 8, 12)
        amp = np.abs(z); phs = np.angle(z)
        win = 1.0; Wtr = 7.4; x0 = -6.2
        Ob = np.array([x0, 0.9, 0]); Oe = Ob; Op_ = np.array([x0, -1.7, 0])
        cc = np.array([4.6, 0.2, 0]); Rr = 1.6
        sc = Rr / amp.max()
        vT = ValueTracker(0.0)

        def hil():
            s0 = vT.get_value() * D
            g = VGroup(E.window_trace(t, x, s0, win, np.array([x0, 2.0, 0]), Wtr, 0.012, MUT, 1.2),
                       E.window_trace(t, z.real, s0, win, Ob, Wtr, 0.025, TEAL, 2.5),
                       E.window_trace(t, amp, s0, win, Oe, Wtr, 0.025, ACC, 3),
                       E.window_trace(t, phs, s0, win, Op_, Wtr, 0.22, AMB, 2))
            k = int(round((s0 + win) * fs)) % len(t)
            zz = z[k]
            tip = cc + sc * np.array([zz.real, zz.imag, 0])
            g.add(Arrow(cc, tip, buff=0, color=ACC, stroke_width=5, tip_length=0.18, max_tip_length_to_length_ratio=0.3))
            g.add(DashedLine(tip, np.array([x0 + Wtr, Ob[1] + 0.025 * zz.real, 0]), color=MUT, stroke_width=1, stroke_opacity=0.5))
            return g
        axh = VGroup(Circle(radius=Rr, color=MUT, stroke_width=1.2).move_to(cc), Line(cc + np.array([-Rr - 0.2, 0, 0]), cc + np.array([Rr + 0.2, 0, 0]), color=MUT, stroke_width=1),
                     Line(cc + np.array([0, -Rr - 0.2, 0]), cc + np.array([0, Rr + 0.2, 0]), color=MUT, stroke_width=1),
                     T("Re", 14, MUT).move_to(cc + np.array([Rr + 0.45, 0, 0])), T("Im", 14, MUT).move_to(cc + np.array([0, Rr + 0.35, 0])),
                     T(tr("raw", "grezzo"), 14, MUT).move_to(np.array([x0 - 0.5, 2.0, 0])), T("8–12 Hz", 14, TEAL).move_to(np.array([x0 - 0.55, 0.9, 0])),
                     T(tr("phase", "fase"), 14, AMB).move_to(np.array([x0 - 0.5, -1.7, 0])), T(tr("amplitude = arrow length", "ampiezza = lunghezza della freccia"), 15, ACC).move_to(cc + np.array([0, -Rr - 0.45, 0])))
        hz = always_redraw(hil)
        self.play(FadeIn(axh), FadeIn(hz), run_time=1.2)
        fm = fcard(r"z(t)=x(t)+i\,\mathcal{H}[x](t)=A(t)\,e^{i\varphi(t)}", CARD2, 0.7).move_to(np.array([-2.5, -3.0, 0]))
        self.play(FadeIn(fm))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: vT.set_value(ph.get_value()))
        self.add(drv); loop_play(self, ph, 16.0); drv.clear_updaters(); hz.clear_updaters()

        # ---------------------------------------------------------- 21 ITPC: vettori di fase che ruotano insieme
        self.new(tr("Phase (2)", "Fase (2)"), tr("Inter-trial phase coherence", "Coerenza di fase tra trial"))
        rng = np.random.default_rng(4)
        N = 30; base_ph = rng.uniform(-np.pi, np.pi, N); lock_ph = rng.normal(0, 0.45, N)
        cc = np.array([-3.4, -0.3, 0]); Rr = 2.1
        kT = ValueTracker(1.0); rotT = ValueTracker(0.0)

        def itpc():
            k = kT.get_value(); r = rotT.get_value()
            ph_ = (1 - k) * base_ph + k * lock_ph + r
            g = VGroup(*[Line(cc, cc + Rr * np.array([np.cos(a), np.sin(a), 0]), color=TEAL, stroke_width=2, stroke_opacity=0.7) for a in ph_])
            mz = np.mean(np.exp(1j * ph_))
            g.add(Arrow(cc, cc + Rr * np.array([mz.real, mz.imag, 0]), buff=0, color=ACC, stroke_width=7, tip_length=0.22, max_tip_length_to_length_ratio=0.4))
            g.add(T(f"ITPC = **{dec(abs(mz))}**", 24, ACC).move_to(cc + np.array([0, -Rr - 0.45, 0])))
            return g
        circ = Circle(radius=Rr, color=MUT, stroke_width=1.5).move_to(cc)
        iz = always_redraw(itpc)
        self.play(Create(circ), FadeIn(iz))
        fm = fcard(r"\mathrm{ITPC}(t,f)=\Big|\frac{1}{N}\sum_k e^{i\varphi_k(t,f)}\Big|", CARD2, 0.7).move_to(np.array([3.3, 1.5, 0]))
        bl = bullets([tr("Each trial = a ++unit vector++; average: 0 random, 1 aligned.", "Ogni trial = un ++vettore unitario++; media: 0 casuale, 1 allineato."),
                      tr("Independent of power: ++phase locking/resetting++.", "Indipendente dalla potenza: ++aggancio/reset di fase++."),
                      tr("⚠ Null ≈ 1/√N: ++equalise trial counts++.", "⚠ Nullo ≈ 1/√N: ++pareggiare i trial++.")], 16, n=36, gap=0.24).move_to(np.array([3.4, -0.6, 0]))
        mt = metaphor(tr("a ++rowing crew++: the boat moves only if strokes are in phase.", "un ++equipaggio di canottaggio++: la barca va solo se le remate sono in fase."), 15, n=60).move_to(np.array([3.4, -2.6, 0]))
        self.play(FadeIn(fm)); self.play(FadeIn(bl)); self.play(FadeIn(mt))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: (kT.set_value(0.5 + 0.5 * np.cos(2 * np.pi * ph.get_value())), rotT.set_value(2 * np.pi * 4 * ph.get_value())))
        self.add(drv); loop_play(self, ph, 12.0); drv.clear_updaters(); iz.clear_updaters()

        # ---------------------------------------------------------- 22 PAC
        self.new(tr("Phase (3)", "Fase (3)"), tr("Cross-frequency coupling: phase–amplitude", "Accoppiamento tra frequenze: fase–ampiezza"))
        t, th, gam, x = F6.pac_signal(2.0, 500)
        Wp = 7.4; x0 = -6.0
        Os_ = [np.array([x0, 1.4, 0]), np.array([x0, 0.0, 0]), np.array([x0, -1.3, 0])]
        sigs = [(t, x), (t, th), (t, gam)]; cols = [FG, TEAL, ACC]; hs = [0.55, 0.45, 1.1]
        lab = VGroup(T(tr("signal", "segnale"), 15, MUT).move_to(Os_[0] + np.array([-0.0, 0.85, 0]), aligned_edge=LEFT), T(tr("theta (6 Hz)", "theta (6 Hz)"), 15, TEAL).move_to(Os_[1] + np.array([0, 0.65, 0]), aligned_edge=LEFT),
                     T(tr("gamma (60 Hz) amplitude", "ampiezza gamma (60 Hz)"), 15, ACC).move_to(Os_[2] + np.array([0, 0.65, 0]), aligned_edge=LEFT))
        tr0 = VGroup(*[E.window_trace(tt, xx, 0.0, 1.0, O_, Wp, h, c, 1.6) for (tt, xx), O_, c, h in zip(sigs, Os_, cols, hs)])
        f = F6.f22_pac(6.0)
        hist = VGroup(f["hb"], f["hax"], f["hl"], f["ht"])
        hist.scale(1.0).move_to(np.array([4.6, 0.2, 0]))
        self.play(FadeIn(lab), Create(tr0), run_time=1.2)
        self.play(FadeIn(hist))
        bl = bullets([tr("*PAC*: gamma ++amplitude++ follows theta ++phase++ (Canolty et al., 2006).", "*PAC*: l'++ampiezza++ gamma segue la ++fase++ theta (Canolty et al., 2006)."),
                      tr("*Modulation index*: distance of the histogram from flat (Tort et al., 2010).", "*Indice di modulazione*: distanza dell'istogramma dal piatto (Tort et al., 2010)."),
                      tr("⚠ Sharp, non-sinusoidal waves → ++spurious PAC++ (Cole & Voytek, 2017).", "⚠ Onde ripide non sinusoidali → ++PAC spurio++ (Cole & Voytek, 2017).")], 16, n=100, gap=0.16).move_to(np.array([0, -2.75, 0]))
        self.play(FadeIn(bl))
        loop_start(self)
        ph = ValueTracker(0.0)
        live = always_redraw(lambda: VGroup(*[E.window_trace(tt, xx, ph.get_value() * 2.0, 1.0, O_, Wp, h, c, 1.6) for (tt, xx), O_, c, h in zip(sigs, Os_, cols, hs)]))
        self.remove(tr0); self.add(live); loop_play(self, ph, 6.0); live.clear_updaters()

        # ---------------------------------------------------------- 23 MATLAB
        self.new(tr("In MATLAB", "In MATLAB"), tr("Welch spectrum and Morlet wavelet convolution", "Welch e convoluzione con wavelet di Morlet"))
        code = ["fs = EEG.srate;  x = squeeze(EEG.data(chan,:,:));            % time x trials",
                "[pxx, f] = pwelch(x(:), hann(2*fs), fs, [], fs);             % Welch: 2-s Hann, 50% overlap",
                "frex = logspace(log10(2), log10(40), 30);                    % 2-40 Hz, log-spaced",
                "ncyc = logspace(log10(3), log10(10), 30);                    % 3 -> 10 cycles",
                "wt = -2:1/fs:2;  half = floor(numel(wt)/2);",
                "nConv = numel(x) + numel(wt) - 1;  X = fft(x(:).', nConv);",
                "tf = zeros(numel(frex), size(x,1));  itpc = tf;",
                "for fi = 1:numel(frex)",
                "    s  = ncyc(fi) / (2*pi*frex(fi));",
                "    W  = fft(exp(2i*pi*frex(fi)*wt) .* exp(-wt.^2/(2*s^2)), nConv);",
                "    as = ifft(X .* W ./ max(W));  as = reshape(as(half+1:end-half), size(x));",
                "    tf(fi,:)   = mean(abs(as).^2, 2);                         % total power",
                "    itpc(fi,:) = abs(mean(exp(1i*angle(as)), 2));            % phase coherence",
                "end",
                "bl = EEG.times >= -400 & EEG.times <= -100;",
                "tfdB = 10*log10(tf ./ mean(tf(:,bl), 2));                    % baseline in dB"]
        cl = code_lines(code, 15)
        if cl.width > 12.6: cl.scale_to_fit_width(12.6)
        cc_ = card(cl, CARD, pad=0.25).move_to(np.array([0, -0.45, 0]))
        self.play(FadeIn(cc_[0]))
        self.play(LaggedStart(*[FadeIn(x_, shift=RIGHT * 0.1) for x_ in cl], lag_ratio=0.12), run_time=3.0)

        # ---------------------------------------------------------- 24 trappole
        self.new(tr("Pitfalls", "Trappole"), tr("Six ways to fool yourself with frequencies", "Sei modi di ingannarsi con le frequenze"))
        g = rows_mob([tr("A \"band power\" change that is really a ++1/f slope++ change.", "Un cambiamento di \"potenza di banda\" che è in realtà di ++pendenza 1/f++."),
                      tr("\"Gamma\" that is ++muscle++ or ++microsaccades++.", "\"Gamma\" che è ++muscolo++ o ++microsaccadi++."),
                      tr("Oscillations created by ++filters++, ++edges++ or sharp ERPs.", "Oscillazioni create da ++filtri++, ++bordi++ o ERP ripidi."),
                      tr("An oscillation where there is only a ++transient++ burst.", "Un'oscillazione dove c'è solo un ++burst transitorio++."),
                      tr("Time × frequency × channel tests: ++cluster-based permutation++ (Maris & Oostenveld, 2007).", "Test tempo × frequenza × canale: ++permutazioni a cluster++ (Maris & Oostenveld, 2007)."),
                      tr("ITPC and coherence ++biased++ by unequal trial numbers.", "ITPC e coerenza ++distorte++ da numeri di trial diversi.")], 19, n=90, h=0.66, gap=0.12, col=ACC).shift(DOWN * 0.4)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.2), run_time=2.5)

        # ---------------------------------------------------------- 25 domande
        self.new(tr("Check your understanding", "Verifica"), tr("Three questions", "Tre domande"))
        g = rows_mob([tr("With 500-ms windows, can you separate alpha peaks at 10 and 11 Hz? Why?", "Con finestre di 500 ms puoi separare picchi alfa a 10 e 11 Hz? Perché?"),
                      tr("4-Hz power with 7-cycle wavelets in −200…800 ms epochs: what is the problem?", "Potenza a 4 Hz con wavelet a 7 cicli in epoche −200…800 ms: qual è il problema?"),
                      tr("A gamma burst appears in single-trial power but not in the TF map of the ERP. Why?", "Un burst gamma compare nella potenza dei singoli trial ma non nella mappa TF dell'ERP. Perché?")], 21, n=84, h=1.05, gap=0.35, col=ACC).shift(DOWN * 0.3)
        for r_ in g: self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.7)

        # ---------------------------------------------------------- 26 messaggi chiave
        self.new(tr("Take-home messages", "Messaggi chiave"), tr("Take-home messages", "Messaggi chiave"))
        g = rows_mob([tr("Δf = 1/T: ++resolution needs time++; taper to avoid leakage.", "Δf = 1/T: ++la risoluzione richiede tempo++; finestrare contro il leakage."),
                      tr("Average (Welch, multitaper) for ++stable spectra++; log axes.", "Mediare (Welch, multitaper) per spettri ++stabili++; assi log."),
                      tr("Separate ++peaks++ from the ++1/f++ background.", "Separare i ++picchi++ dal fondo ++1/f++."),
                      tr("Wavelets: ++cycles set the time–frequency trade-off++; normalise to baseline.", "Wavelet: ++i cicli regolano il compromesso tempo–frequenza++; normalizzare alla baseline."),
                      tr("Evoked ≠ induced; ITPC = ++phase locking++; PAC needs care.", "Evocata ≠ indotta; ITPC = ++aggancio di fase++; il PAC richiede cautela.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 27 letture
        self.new(tr("Suggested reading", "Letture consigliate"), tr("Suggested reading", "Letture consigliate"))
        refs_slide(self, ["Cohen (2014) *Analyzing Neural Time Series Data*, MIT Press.", "Cohen (2019) *NeuroImage* 199:81–86.",
                          "Welch (1967) *IEEE Trans Audio Electroacoust* 15:70–73.", "Thomson (1982) *Proc IEEE* 70:1055–1096.",
                          "Donoghue et al. (2020) *Nat Neurosci* 23:1655–1665.", "Klimesch (1999) *Brain Res Rev* 29:169–195.",
                          "Pfurtscheller & Lopes da Silva (1999) *Clin Neurophysiol* 110:1842–1857.", "Tallon-Baudry & Bertrand (1999) *Trends Cogn Sci* 3:151–162.",
                          "Canolty et al. (2006) *Science* 313:1626–1628.", "Tort et al. (2010) *J Neurophysiol* 104:1195–1210.",
                          "Cole & Voytek (2017) *Trends Cogn Sci* 21:137–149.", "Maris & Oostenveld (2007) *J Neurosci Methods* 164:177–190."], 17)
        self.end()
