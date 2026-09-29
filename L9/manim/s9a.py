from base import *
import figs9 as F9

NS, NE = F9.NS, F9.NE
LF = F9.leadfield()


def dec(v, n=2):
    s = f"{v:.{n}f}"
    return s if LANG == "en" else s.replace(".", ",")


def gsrc(pos, w=3.0, amp=1.0):
    return amp * np.exp(-0.5 * ((np.arange(NS) - pos) / w) ** 2)


def kernel(method="sloreta", lam=0.05):
    W = np.eye(NS) if method != "wmne" else np.diag(1 / np.linalg.norm(LF, axis=0) ** 2)
    GW = LF @ W @ LF.T
    K = W @ LF.T @ np.linalg.inv(GW + lam * np.trace(GW) / NE * np.eye(NE))
    if method == "sloreta":
        K = K / np.sqrt(np.clip(np.diag(K @ LF), 1e-12, None))[:, None]
    return K


def scene_head(c, R, j=None, y=None, sw=6):
    return VGroup(F9.headc(c, R), F9.cortex_mob(c, R, j, sw=sw), F9.sensors_mob(c, R, y, r=0.065))


class A9_Sorgenti(Base):
    start_num = 1

    def construct(self):
        # ---------------------------------------------------------- 1 copertina: sorgente che si sposta, sensori che rispondono
        self.new(first=True); self.num = 1
        c = np.array([5.3, -2.9, 0]); R = 1.35
        uT = ValueTracker(0.0)

        def cov():
            pos = 60 + 45 * np.sin(2 * np.pi * uT.get_value())
            j = gsrc(pos, 2.5)
            return scene_head(c, R, j, LF @ j, sw=5)

        def vis():
            self.play(FadeIn(cov()))
        copertina(self, tr("Lecture 9", "Lezione 9"), tr("From scalp to brain:\nsources and connectivity", "Dallo scalpo al cervello:\nsorgenti e connettività"), vis)
        self.remove(*[m for m in self.mobjects if isinstance(m, VGroup) and len(m) == 3])
        loop_start(self)
        ph = ValueTracker(0.0)
        cz = always_redraw(lambda: (uT.set_value(ph.get_value()), cov())[1])
        self.add(cz); loop_play(self, ph, 8.0); cz.clear_updaters()

        # ---------------------------------------------------------- 2 obiettivi
        self.new(tr("Lecture 9", "Lezione 9"), tr("Today: where and how brain regions talk", "Oggi: dove e come dialogano le regioni cerebrali"))
        g = rows_mob([tr("*Forward problem*: head models and the ++lead field++.", "*Problema diretto*: modelli di testa e ++lead field++."),
                      tr("*Inverse problem*: why it is ++ill-posed++ and how priors solve it.", "*Problema inverso*: perché è ++mal posto++ e come lo risolvono le ipotesi."),
                      tr("Dipole fitting, MNE, sLORETA/eLORETA, ++beamformers++.", "Fit di dipoli, MNE, sLORETA/eLORETA, ++beamformer++."),
                      tr("*Connectivity*: coherence, PLV, wPLI, Granger — and ++volume conduction++.", "*Connettività*: coerenza, PLV, wPLI, Granger — e ++conduzione di volume++."),
                      tr("*Graph theory*: the brain as a network.", "*Teoria dei grafi*: il cervello come rete.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 3 diretto / inverso dal vivo
        self.new(tr("Two problems", "Due problemi"), tr("Forward and inverse problems", "Problema diretto e problema inverso"))
        R = 2.0; c1 = np.array([-4.2, -0.6, 0]); c2 = np.array([0.4, -0.6, 0])
        K = kernel("sloreta")
        pT = ValueTracker(40.0)

        def fi():
            j = gsrc(pT.get_value(), 2.5); y = LF @ j; jh = K @ y
            return VGroup(scene_head(c1, R, j, None), scene_head(c2, R, jh, y))
        fz = always_redraw(fi)
        labs = VGroup(T(tr("true sources j", "sorgenti vere j"), 17).move_to(c1 + np.array([0, -0.55, 0])), T(tr("data y → estimate ĵ (sLORETA)", "dati y → stima ĵ (sLORETA)"), 17).move_to(c2 + np.array([0, -0.55, 0])),
                      Arrow(np.array([-2.0, 1.7, 0]), np.array([-1.3, 1.7, 0]), buff=0, color=TEAL, stroke_width=4, tip_length=0.18))
        self.play(FadeIn(fz), FadeIn(labs))
        fm = fcard(r"\mathbf{y}(t)=\mathbf{L}\,\mathbf{j}(t)+\mathbf{n}(t)", CARD2, 0.8).move_to(np.array([4.6, 1.6, 0]))
        bl = bullets([tr("*Forward*: unique, pure physics.", "*Diretto*: unico, pura fisica."),
                      tr("*Inverse*: ++not unique++ (Helmholtz, 1853).", "*Inverso*: ++non unico++ (Helmholtz, 1853)."),
                      tr("Solutions need ++priors++.", "Le soluzioni richiedono ++ipotesi a priori++.")], 17, n=26, gap=0.28).move_to(np.array([4.6, -0.2, 0]))
        mt = metaphor(tr("hearing a ++chord++ and guessing which fingers pressed which keys.", "sentire un ++accordo++ e indovinare quali dita hanno premuto quali tasti."), 16).move_to(np.array([0, -3.0, 0]))
        self.play(FadeIn(fm), FadeIn(bl), FadeIn(mt))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: pT.set_value(60 + 45 * np.sin(2 * np.pi * ph.get_value())))
        self.add(drv); loop_play(self, ph, 10.0); drv.clear_updaters(); fz.clear_updaters()

        # ---------------------------------------------------------- 4 sezione
        self.new(); section_title(self, 1, tr("The forward problem", "Il problema diretto"))

        # ---------------------------------------------------------- 5 modelli di testa
        self.new(tr("Forward (1)", "Diretto (1)"), tr("Head models", "Modelli di testa"))
        f = F9.f05_headmodels(1.3); fit(f, 1.0, np.array([0, 0.7, 0]))
        for k in range(3):
            parts = [f[key] for key in f if key.startswith(f"s{k}") or key == f"mesh{k}" or key == f"l{k}" or key == f"d{k}"]
            self.play(LaggedStart(*[FadeIn(p_) for p_ in parts], lag_ratio=0.15), run_time=0.9)
        g = rows_mob([tr("Skull (≈ 0.01 S/m) is ≈ 30–50× less conductive than scalp and brain.", "Il cranio (≈ 0,01 S/m) conduce ≈ 30–50× meno di scalpo e cervello."),
                      tr("Individual ++MRI++ or ++template++ head; ++digitised++ electrode positions.", "++RM++ individuale o testa ++template++; posizioni ++digitalizzate++."),
                      tr("Main uncertainty: ++skull conductivity++ (Vorwerk et al., 2014).", "Incertezza principale: ++conducibilità del cranio++ (Vorwerk et al., 2014).")], 18, n=100, h=0.6, gap=0.12).move_to(np.array([0, -2.3, 0]))
        self.play(LaggedStart(*[FadeIn(r_) for r_ in g], lag_ratio=0.2), run_time=1.2)

        # ---------------------------------------------------------- 6 lead field: la colonna scorre
        self.new(tr("Forward (2)", "Diretto (2)"), tr("The lead field matrix", "La matrice lead field"))
        vm = np.abs(LF).max() * 0.6
        img = (np.dstack([E.cmap_rdbu(LF / vm), np.ones(LF.shape)]) * 255).astype(np.uint8)
        Wm, Hm = 5.0, 2.8; cm = np.array([-3.6, 0.3, 0])
        mimg = ImageMobject(img); mimg.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        mimg.stretch_to_fit_width(Wm); mimg.stretch_to_fit_height(Hm); mimg.move_to(cm)
        frm = VGroup(Rectangle(width=Wm, height=Hm, color=FG, stroke_width=1.5).move_to(cm), T(tr(f"{NS} sources", f"{NS} sorgenti"), 15, MUT).move_to(cm + np.array([0, -Hm / 2 - 0.3, 0])),
                     T(tr(f"{NE} electrodes", f"{NE} elettrodi"), 15, MUT).rotate(PI / 2).move_to(cm + np.array([-Wm / 2 - 0.3, 0, 0])))
        self.play(FadeIn(mimg), FadeIn(frm))
        cT = ValueTracker(20.0)
        ch = np.array([2.8, -0.9, 0]); Rh = 2.1

        def col():
            k = int(round(cT.get_value()))
            j = np.zeros(NS); j[max(k - 1, 0):k + 2] = 1
            return VGroup(Rectangle(width=Wm / NS * 3, height=Hm, color=ACC, stroke_width=3).move_to(cm + np.array([-Wm / 2 + Wm * (k + 0.5) / NS, 0, 0])),
                          scene_head(ch, Rh, j, LF[:, k]),
                          T(tr(f"column **{k}**: norm = **{dec(np.linalg.norm(LF[:, k]), 1)}**", f"colonna **{k}**: norma = **{dec(np.linalg.norm(LF[:, k]), 1)}**"), 18, AMB).move_to(ch + np.array([0, 2.75, 0])))
        cz = always_redraw(col)
        self.play(FadeIn(cz))
        bl = bullets([tr("Column k = ++scalp map of a unit dipole++ at k.", "Colonna k = ++mappa di un dipolo unitario++ in k."),
                      tr("Deep/tangential sources → ++small++ columns: depth bias.", "Sorgenti profonde/tangenziali → colonne ++piccole++: bias di profondità."),
                      tr("N_{el} ≈ 64–256 ≪ N_{src} ≈ 5 000–15 000.", "N_{el} ≈ 64–256 ≪ N_{src} ≈ 5 000–15 000.")], 16, n=48, gap=0.2).move_to(np.array([-3.4, -2.4, 0]))
        self.play(FadeIn(bl))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: cT.set_value(60 - 55 * np.cos(2 * np.pi * ph.get_value())))
        self.add(drv); loop_play(self, ph, 10.0); drv.clear_updaters(); cz.clear_updaters()

        # ---------------------------------------------------------- 7 sezione
        self.new(); section_title(self, 2, tr("The inverse problem", "Il problema inverso"))

        # ---------------------------------------------------------- 8 mal posto: si aggiunge lo spazio nullo, i dati non cambiano
        self.new(tr("Inverse (1)", "Inverso (1)"), tr("An ill-posed problem", "Un problema mal posto"))
        j1 = gsrc(60, 4)
        Lp = np.linalg.pinv(LF); Nsp = np.eye(NS) - Lp @ LF
        rng = np.random.default_rng(2)
        z1 = Nsp @ rng.normal(size=NS); z2 = Nsp @ rng.normal(size=NS)
        z1 *= 2.5 / np.abs(z1).max(); z2 *= 2.5 / np.abs(z2).max()
        aT = ValueTracker(0.0)
        c = np.array([-3.0, -0.8, 0]); R = 2.3

        def ill():
            a = aT.get_value()
            j = j1 + np.sin(2 * np.pi * a) * z1 + np.sin(4 * np.pi * a) * z2 * 0.7
            y = LF @ j
            res = np.linalg.norm(y - LF @ j1) / np.linalg.norm(LF @ j1)
            return VGroup(scene_head(c, R, j, y), T(tr(f"change in scalp data: **{dec(100 * res, 3)} %**", f"variazione dei dati di scalpo: **{dec(100 * res, 3)} %**"), 19, AMB).move_to(c + np.array([0, -0.6, 0])))
        iz = always_redraw(ill)
        self.play(FadeIn(iz))
        bl = bullets([tr(f"{NE} equations, {NS} unknowns.", f"{NE} equazioni, {NS} incognite."),
                      tr("\"Silent\" patterns (++null space++ of L) change the sources but ++not the data++.", "Configurazioni \"silenti\" (++spazio nullo++ di L) cambiano le sorgenti ma ++non i dati++."),
                      tr("Every method = a ++prior++ on plausible solutions.", "Ogni metodo = un'++ipotesi a priori++ sulle soluzioni plausibili."),
                      tr("⚠ Spatial resolution ≈ ++cm++.", "⚠ Risoluzione spaziale ≈ ++cm++.")], 17, n=34, gap=0.3).move_to(np.array([3.6, -0.3, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.4)
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: aT.set_value(ph.get_value()))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); iz.clear_updaters()

        # ---------------------------------------------------------- 9 fit di dipolo: scansione della varianza residua
        self.new(tr("Inverse (2)", "Inverso (2)"), tr("Equivalent current dipoles", "Dipoli di corrente equivalenti"))
        rng = np.random.default_rng(1)
        ytrue = LF[:, 35] + rng.normal(size=NE) * np.abs(LF[:, 35]).max() * 0.1
        rv = np.array([1 - (LF[:, k] @ ytrue) ** 2 / ((LF[:, k] @ LF[:, k]) * (ytrue @ ytrue)) for k in range(NS)])
        c = np.array([-3.4, -0.9, 0]); R = 2.2
        Or = np.array([1.2, -1.8, 0]); Wr = 5.2; Hr = 2.4
        kT = ValueTracker(10.0)

        def dip():
            k = int(round(kT.get_value()))
            q = (LF[:, k] @ ytrue) / (LF[:, k] @ LF[:, k])
            j = np.zeros(NS); j[max(k - 1, 0):k + 2] = 1
            g = VGroup(scene_head(c, R, j, ytrue))
            g.add(VMobject(color=TEAL, stroke_width=3).set_points_as_corners([Or + np.array([i / NS * Wr, (1 - v) * Hr, 0]) for i, v in enumerate(rv[:k + 1])]))
            g.add(Dot(Or + np.array([k / NS * Wr, (1 - rv[k]) * Hr, 0]), radius=0.08, color=AMB))
            g.add(T(tr(f"GOF = **{dec(100 * (1 - rv[k]), 0)} %**", f"GOF = **{dec(100 * (1 - rv[k]), 0)} %**"), 20, AMB).move_to(Or + np.array([Wr / 2, Hr + 0.4, 0])))
            return g
        axr = VGroup(Line(Or, Or + np.array([Wr, 0, 0]), color=MUT, stroke_width=1.5), Line(Or, Or + np.array([0, Hr, 0]), color=MUT, stroke_width=1.5),
                     T(tr("dipole position along the cortex", "posizione del dipolo lungo la corteccia"), 14, MUT).move_to(Or + np.array([Wr / 2, -0.3, 0])),
                     T(tr("data: measured map", "dati: mappa misurata"), 15, MUT).move_to(c + np.array([0, -0.55, 0])))
        dz = always_redraw(dip)
        self.play(FadeIn(axr), FadeIn(dz))
        fm = fcard(r"\min_{\mathrm{pos}}\;\lVert \mathbf{y}-\mathbf{L}(\mathrm{pos})\,\mathbf{q}\rVert^2", CARD2, 0.7).move_to(np.array([3.8, 1.75, 0]))
        cap = T(tr("Works for ++focal++ activity (early ERPs, interictal spikes); number of dipoles chosen ++a priori++; GOF high ≠ correct model.", "Funziona per attività ++focale++ (ERP precoci, spike intercritici); numero di dipoli scelto ++a priori++; GOF alta ≠ modello corretto."), 16, n=120).move_to(np.array([0, -3.05, 0]))
        self.play(FadeIn(fm), FadeIn(cap))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: kT.set_value(min(ph.get_value() * 1.25, 1.0) * (NS - 1)))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); dz.clear_updaters()

        # ---------------------------------------------------------- 10 metodi distribuiti dal vivo
        self.new(tr("Inverse (3)", "Inverso (3)"), tr("Distributed solutions: MNE, sLORETA, beamformers", "Soluzioni distribuite: MNE, sLORETA, beamformer"))
        Ks = [kernel("mne"), kernel("wmne"), kernel("sloreta")]
        rng = np.random.default_rng(5)
        tt = np.arange(300) / 250; s = np.sin(2 * np.pi * 10 * tt)
        noise = rng.normal(size=(NE, 300))
        pT = ValueTracker(40.0)
        names = [tr("true", "vera"), "MNE", tr("weighted MNE", "MNE pesato"), "sLORETA", "LCMV"]
        cs = [np.array([-5.2 + 2.6 * k, 0.9, 0]) for k in range(5)]
        R = 1.15

        def meth():
            p = pT.get_value(); k0 = int(round(p))
            Y = np.outer(LF[:, k0], s) + noise * np.abs(LF[:, k0]).max() * 0.08
            C = Y @ Y.T / Y.shape[1]
            y = LF[:, k0]
            ests = [gsrc(p, 2.5)] + [K_ @ y for K_ in Ks] + [F9.inverse(LF, None, "lcmv", C=C)]
            return VGroup(*[VGroup(F9.headc(c_, R, sw=2.5), F9.cortex_mob(c_, R, e, sw=5)) for c_, e in zip(cs, ests)])
        mz = always_redraw(meth)
        labs = VGroup(*[T(n_, 15).move_to(c_ + np.array([0, -0.35, 0])) for n_, c_ in zip(names, cs)])
        self.play(FadeIn(mz), FadeIn(labs))
        fm = fcard(r"\hat{\mathbf{j}}=\mathbf{W}\mathbf{L}^{\!\top}(\mathbf{L}\mathbf{W}\mathbf{L}^{\!\top}+\lambda\mathbf{I})^{-1}\mathbf{y}", CARD2, 0.65).move_to(np.array([0, -0.9, 0]))
        g = rows_mob([tr("*MNE*: minimum energy, ++surface bias++ → depth weighting. *sLORETA/eLORETA*: standardised, ++zero localisation error++ for single sources (in theory).", "*MNE*: minima energia, ++bias superficiale++ → pesi di profondità. *sLORETA/eLORETA*: standardizzato, ++errore nullo++ per sorgente singola (in teoria)."),
                      tr("*Beamformer (LCMV/DICS)*: spatial filter from the ++data covariance++; focal, but fails with ++correlated sources++ (Van Veen et al., 1997).", "*Beamformer (LCMV/DICS)*: filtro spaziale dalla ++covarianza dei dati++; focale, ma fallisce con ++sorgenti correlate++ (Van Veen et al., 1997).")], 15, n=120, h=0.72, gap=0.1).move_to(np.array([0, -2.45, 0]))
        self.play(FadeIn(fm), FadeIn(g))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: pT.set_value(60 + 40 * np.sin(2 * np.pi * ph.get_value())))
        self.add(drv); loop_play(self, ph, 10.0); drv.clear_updaters(); mz.clear_updaters()

        # ---------------------------------------------------------- 11 regolarizzazione dal vivo
        self.new(tr("Inverse (4)", "Inverso (4)"), tr("Regularisation and what limits accuracy", "Regolarizzazione e limiti di accuratezza"))
        rng = np.random.default_rng(3)
        y = LF[:, 55] + rng.normal(size=NE) * np.abs(LF[:, 55]).max() * 0.15
        lams = np.logspace(-4, 0.5, 60)
        EST = [kernel("sloreta", l_) @ y for l_ in lams]
        lT = ValueTracker(0.0)
        c = np.array([-3.2, -0.9, 0]); R = 2.4

        def reg():
            k = int(np.clip(round(lT.get_value() * 59), 0, 59))
            lam = lams[k]
            lab = tr("fits noise", "segue il rumore") if lam < 3e-3 else (tr("over-smooth", "troppo liscio") if lam > 0.5 else tr("adequate", "adeguato"))
            col = ACC if (lam < 3e-3 or lam > 0.5) else TEAL
            return VGroup(F9.headc(c, R), F9.cortex_mob(c, R, EST[k]), F9.cortex_mob(c, R * 0.0 + R, None, col=None, sw=0) if False else VGroup(),
                          T(f"λ = **{lam:.0e}** · {lab}".replace("e-0", "e-").replace("e+0", "e+"), 20, col).move_to(c + np.array([0, -0.6, 0])))
        rz = always_redraw(reg)
        mark = Dot(np.array([*(F9.src_pos()[55] * R + c[:2]), 0]), radius=0.1, color=AMB)
        self.play(FadeIn(rz), FadeIn(mark), FadeIn(T(tr("● true source", "● sorgente vera"), 15, AMB).move_to(c + np.array([0, 2.75, 0]))))
        bl = bullets([tr("λ trades ++fit++ vs ++smoothness/energy++.", "λ bilancia ++adattamento++ e ++regolarità/energia++."),
                      tr("Set from ++SNR++, L-curve or cross-validation.", "Fissarlo da ++SNR++, curva L o cross-validation."),
                      tr("Accuracy: ++≥ 64 electrodes++, full coverage, good head model (Michel & Brunet, 2019).", "Accuratezza: ++≥ 64 elettrodi++, copertura completa, buon modello di testa (Michel & Brunet, 2019)."),
                      tr("Validate with ++simulations++ / intracranial data.", "Validare con ++simulazioni++ / dati intracranici.")], 16, n=34, gap=0.28).move_to(np.array([3.8, -0.4, 0]))
        for b_ in bl: self.play(FadeIn(b_), run_time=0.35)
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: lT.set_value(0.5 - 0.5 * np.cos(2 * np.pi * ph.get_value())))
        self.add(drv); loop_play(self, ph, 10.0); drv.clear_updaters(); rz.clear_updaters()
        self.end()
