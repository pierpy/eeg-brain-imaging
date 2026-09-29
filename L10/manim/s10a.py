from base import *
import figs10 as F10
from scipy.ndimage import gaussian_filter1d

TD = F10.TD


def dec(v, n=2):
    s = f"{v:.{n}f}"
    return s if LANG == "en" else s.replace(".", ",")


def cards_row(items, w, h, y, size=16, n=30, head=20):
    cs = VGroup()
    for k, (h_, d_) in enumerate(items):
        box = RoundedRectangle(corner_radius=0.14, width=w, height=h, fill_color=CARD if k % 2 == 0 else CARD2, fill_opacity=1, stroke_width=0)
        tx = VGroup(TX(h_, font=BODY, font_size=head, color=TEAL, weight=BOLD), T(d_, size, n=n)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        tx.move_to(box).align_to(box, UP).shift(DOWN * 0.25)
        cs.add(VGroup(box, tx))
    return cs.arrange(RIGHT, buff=0.2).move_to(np.array([0, y, 0]))


class A10_MVPA(Base):
    start_num = 1

    def construct(self):
        # ---------------------------------------------------------- 1 copertina: nuvole di punti con iperpiano che ruota
        self.new(first=True); self.num = 1
        rng = np.random.default_rng(3)
        A = rng.multivariate_normal([-0.4, 0.4], [[0.2, 0.15], [0.15, 0.2]], 50); B = rng.multivariate_normal([0.4, -0.4], [[0.2, 0.15], [0.15, 0.2]], 50)
        c = np.array([5.2, -2.3, 0]); sc = 0.9
        dots = VGroup(*[Dot(c + np.array([*(a * sc), 0]), radius=0.04, color=TEAL) for a in A], *[Dot(c + np.array([*(b * sc), 0]), radius=0.04, color=ACC) for b in B])

        def vis():
            self.play(FadeIn(dots))
        copertina(self, tr("Lecture 10", "Lezione 10"), tr("Reading the mind?\nDecoding and applications", "Leggere la mente?\nDecoding e applicazioni"), vis)
        loop_start(self)
        ph = ValueTracker(0.0)
        hz = always_redraw(lambda: DashedLine(c + 1.4 * np.array([np.cos(PI / 4 + 0.3 * np.sin(2 * PI * ph.get_value())), np.sin(PI / 4 + 0.3 * np.sin(2 * PI * ph.get_value())), 0]),
                                              c - 1.4 * np.array([np.cos(PI / 4 + 0.3 * np.sin(2 * PI * ph.get_value())), np.sin(PI / 4 + 0.3 * np.sin(2 * PI * ph.get_value())), 0]), color=FG, stroke_width=3))
        self.add(hz); loop_play(self, ph, 6.0); hz.clear_updaters()

        # ---------------------------------------------------------- 2 obiettivi
        self.new(tr("Lecture 10", "Lezione 10"), tr("Today: from brain signals to predictions", "Oggi: dai segnali cerebrali alle predizioni"))
        g = rows_mob([tr("*Encoding vs decoding*: two directions of inference.", "*Encoding vs decoding*: due direzioni di inferenza."),
                      tr("*MVPA*: linear classifiers, cross-validation, overfitting, metrics.", "*MVPA*: classificatori lineari, cross-validation, overfitting, metriche."),
                      tr("Interpreting classifiers: ++weights vs patterns++.", "Interpretare i classificatori: ++pesi vs pattern++."),
                      tr("*Time-resolved decoding* and ++temporal generalisation++.", "*Decoding nel tempo* e ++generalizzazione temporale++."),
                      tr("*Applications*: BCI, clinical EEG, EEG–fMRI; course wrap-up.", "*Applicazioni*: BCI, EEG clinico, EEG–fMRI; sintesi del corso.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 3 encoding / decoding: frecce animate
        self.new(tr("Two directions", "Due direzioni"), tr("Encoding and decoding", "Encoding e decoding"))
        f = F10.f03_encdec(12.0); fit(f, 1.0, np.array([0, 0.8, 0]))
        self.play(FadeIn(f["s"]), FadeIn(f["b"]), FadeIn(f["e"]), GrowArrow(f["a1"]), GrowArrow(f["a2"]), run_time=1.0)
        self.play(FadeIn(f["enc"]), run_time=0.8); self.play(FadeIn(f["dec"]), run_time=0.8)
        g = rows_mob([tr("*Univariate* (ERP): one channel at a time → multiple comparisons.", "*Univariata* (ERP): un canale alla volta → confronti multipli."),
                      tr("*Multivariate* (MVPA): the ++whole pattern++; distributed, weak, individual effects.", "*Multivariata* (MVPA): l'++intero pattern++; effetti distribuiti, deboli, individuali."),
                      tr("New question: \"++is the information present, and when?++\"", "Nuova domanda: \"++l'informazione è presente, e quando?++\"")], 17, n=100, h=0.58, gap=0.1).move_to(np.array([0, -1.75, 0]))
        mt = metaphor(tr("a ++sommelier++: the pattern of many molecules tells the wine.", "un ++sommelier++: il pattern di molte molecole rivela il vino."), 16).move_to(np.array([0, -3.1, 0]))
        self.play(FadeIn(g), FadeIn(mt))
        loop_start(self)
        ph = ValueTracker(0.0)
        pulse = always_redraw(lambda: VGroup(Dot(f["enc"][0].point_from_proportion(ph.get_value()), radius=0.11, color=TEAL), Dot(f["dec"][0].point_from_proportion(ph.get_value()), radius=0.11, color=ACC)))
        self.add(pulse); loop_play(self, ph, 4.0); pulse.clear_updaters()

        # ---------------------------------------------------------- 4 sezione
        self.new(); section_title(self, 1, tr("Multivariate pattern analysis", "Analisi multivariata dei pattern"))

        # ---------------------------------------------------------- 5 LDA: l'iperpiano converge
        self.new(tr("MVPA (1)", "MVPA (1)"), tr("A linear classifier", "Un classificatore lineare"))
        rng = np.random.default_rng(3)
        C = np.array([[1.0, 0.8], [0.8, 1.0]]) * 0.25
        A = rng.multivariate_normal([-0.35, 0.35], C, 60); B = rng.multivariate_normal([0.35, -0.35], C, 60)
        X = np.vstack([A, B]); y = np.r_[np.zeros(60), np.ones(60)].astype(int)
        w_opt, b_opt = F10.lda_fit(X, y, 0.05)
        c0 = np.array([-3.4, -0.4, 0]); sc = 1.45
        ax = VGroup(Line(c0 + np.array([-2.3, -2.3, 0]), c0 + np.array([2.3, -2.3, 0]), color=MUT, stroke_width=1.5), Line(c0 + np.array([-2.3, -2.3, 0]), c0 + np.array([-2.3, 2.3, 0]), color=MUT, stroke_width=1.5),
                    T(tr("channel 1", "canale 1"), 14, MUT).move_to(c0 + np.array([0, -2.6, 0])), T(tr("channel 2", "canale 2"), 14, MUT).rotate(PI / 2).move_to(c0 + np.array([-2.6, 0, 0])))
        pts = VGroup(*[Dot(c0 + np.array([*(a * sc), 0]), radius=0.05, color=TEAL) for a in A], *[Dot(c0 + np.array([*(b * sc), 0]), radius=0.05, color=ACC) for b in B])
        self.play(FadeIn(ax), FadeIn(pts, lag_ratio=0.01))
        thT = ValueTracker(0.0)
        th_opt = np.arctan2(w_opt[1], w_opt[0])

        def hyp():
            th = th_opt + 1.2 * np.cos(np.pi * thT.get_value()) * (1 - thT.get_value())
            wv = np.array([np.cos(th), np.sin(th)])
            proj = X @ wv; thr = (proj[y == 0].mean() + proj[y == 1].mean()) / 2
            acc = np.mean((proj > thr) == (y == 1)) if np.mean((proj > thr) == (y == 1)) >= 0.5 else np.mean((proj <= thr) == (y == 1))
            p0 = thr * wv; d = np.array([-wv[1], wv[0]])
            g = VGroup(DashedLine(c0 + np.array([*((p0 - 1.5 * d) * sc), 0]), c0 + np.array([*((p0 + 1.5 * d) * sc), 0]), color=FG, stroke_width=3),
                       Arrow(c0 + np.array([*(p0 * sc), 0]), c0 + np.array([*((p0 + 0.7 * wv) * sc), 0]), buff=0, color=AMB, stroke_width=5, tip_length=0.18))
            g.add(T(tr(f"accuracy = **{int(100 * acc)} %**", f"accuratezza = **{int(100 * acc)} %**"), 20, AMB).move_to(c0 + np.array([0, 2.55, 0])))
            return g
        hz = always_redraw(hyp)
        self.play(FadeIn(hz))
        fm = fcard(r"\mathbf{w}=\boldsymbol{\Sigma}^{-1}(\boldsymbol{\mu}_1-\boldsymbol{\mu}_0),\quad \hat y=\mathrm{sign}(\mathbf{w}^{\top}\mathbf{x}+b)", CARD2, 0.6).move_to(np.array([3.3, 1.7, 0]))
        bl = bullets([tr("Trial = ++point in channel space++.", "Trial = ++punto nello spazio dei canali++."),
                      tr("Find the ++hyperplane++ that best separates the classes.", "Trovare l'++iperpiano++ che separa meglio le classi."),
                      tr("*Shrinkage LDA*: robust default for EEG (Blankertz et al., 2011).", "*LDA con shrinkage*: default robusto per l'EEG (Blankertz et al., 2011)."),
                      tr("SVM, logistic regression: similar.", "SVM, regressione logistica: simili.")], 16, n=36, gap=0.28).move_to(np.array([3.4, -0.7, 0]))
        self.play(FadeIn(fm), FadeIn(bl))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: thT.set_value(0.5 - 0.5 * np.cos(2 * np.pi * ph.get_value())))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); hz.clear_updaters()

        # ---------------------------------------------------------- 6 cross-validation: il fold di test ruota
        self.new(tr("MVPA (2)", "MVPA (2)"), tr("Training, testing, cross-validation", "Addestramento, test, cross-validation"))
        k = 5; Wc = 10.0
        fT = ValueTracker(0.0)
        accs = [0.71, 0.68, 0.74, 0.66, 0.72]

        def cv():
            r = min(int(fT.get_value() * k), k - 1)
            g = VGroup()
            for cc in range(k):
                test = cc == r
                g.add(Rectangle(width=Wc / k - 0.1, height=0.9, stroke_width=0, fill_color=ACC if test else TEAL, fill_opacity=0.85 if test else 0.35).move_to(np.array([-Wc / 2 + Wc / k * (cc + 0.5), 1.2, 0])))
                g.add(T(tr("test", "test") if test else tr("train", "train"), 16, FG).move_to(np.array([-Wc / 2 + Wc / k * (cc + 0.5), 1.2, 0])))
            g.add(T(tr(f"fold **{r + 1}** · accuracy **{int(100 * accs[r])} %** · mean so far **{int(100 * np.mean(accs[:r + 1]))} %**", f"fold **{r + 1}** · accuratezza **{int(100 * accs[r])} %** · media finora **{int(100 * np.mean(accs[:r + 1]))} %**"), 20, AMB).move_to(np.array([0, 2.1, 0])))
            return g
        cz = always_redraw(cv)
        self.play(FadeIn(cz))
        g = rows_mob([tr("Test data ++never seen++ during training.", "Dati di test ++mai visti++ durante l'addestramento."),
                      tr("*k-fold*: train on k−1, test on the left-out, rotate, average.", "*k-fold*: addestrare su k−1, testare sulla esclusa, ruotare, mediare."),
                      tr("⚠ *Leakage*: selection/normalisation ++inside the folds++.", "⚠ *Leakage*: selezione/normalizzazione ++dentro i fold++."),
                      tr("Small samples → ++large error bars++ (Varoquaux et al., 2017).", "Campioni piccoli → ++barre d'errore ampie++ (Varoquaux et al., 2017).")], 18, n=100, h=0.6, gap=0.1, col=ACC).move_to(np.array([0, -1.5, 0]))
        self.play(FadeIn(g))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: fT.set_value(ph.get_value() * 0.9999))
        self.add(drv); loop_play(self, ph, 7.5); drv.clear_updaters(); cz.clear_updaters()

        # ---------------------------------------------------------- 7 overfitting: complessità che cresce
        self.new(tr("MVPA (3)", "MVPA (3)"), tr("Overfitting and the curse of dimensionality", "Overfitting e maledizione della dimensionalità"))
        Wo = 6.0; Ho = 3.0; Oo = np.array([-6.2, -1.9, 0])
        xx = np.linspace(0, 1, 100)
        trc = 0.66 + 0.33 * (1 - np.exp(-4 * xx)); tec = 0.56 + 0.3 * np.exp(-((xx - 0.35) / 0.3) ** 2) + 0.04 * (1 - xx)
        Yo = lambda v: (v - 0.45) / 0.6 * Ho
        axo = VGroup(E.axes(Oo, Wo + 0.2, Ho + 0.2, tr("features / complexity", "feature / complessità"), tr("accuracy", "accuratezza")),
                     DashedLine(Oo + np.array([0, Yo(0.5), 0]), Oo + np.array([Wo, Yo(0.5), 0]), color=MUT, stroke_width=1.5))
        self.play(FadeIn(axo))
        uT = ValueTracker(0.02)

        def ov():
            u = uT.get_value(); m = xx <= u
            g = VGroup(VMobject(color=TEAL, stroke_width=3.5).set_points_as_corners([Oo + np.array([a * Wo, Yo(b), 0]) for a, b in zip(xx[m], trc[m])]),
                       VMobject(color=ACC, stroke_width=3.5).set_points_as_corners([Oo + np.array([a * Wo, Yo(b), 0]) for a, b in zip(xx[m], tec[m])]))
            i = m.sum() - 1
            g.add(T(tr(f"train **{int(100 * trc[i])} %** · test **{int(100 * tec[i])} %**", f"train **{int(100 * trc[i])} %** · test **{int(100 * tec[i])} %**"), 20, AMB).move_to(Oo + np.array([Wo / 2, Ho + 0.55, 0])))
            return g
        oz = always_redraw(ov)
        self.play(FadeIn(oz))
        self.play(uT.animate.set_value(1.0), run_time=2.5)
        bl = bullets([tr("Many features, few trials → model ++memorises noise++.", "Molte feature, pochi trial → il modello ++memorizza il rumore++."),
                      tr("Remedies: ++regularisation++, fewer features, ++more trials++, ++pseudo-trials++.", "Rimedi: ++regolarizzazione++, meno feature, ++più trial++, ++pseudo-trial++."),
                      tr("Only ++cross-validated++ accuracy counts.", "Conta solo l'accuratezza ++in cross-validation++.")], 17, n=36, gap=0.3).move_to(np.array([3.7, 0.2, 0]))
        mt = metaphor(tr("a student who ++memorises last year's answers++ fails the new exam.", "uno studente che ++memorizza le risposte dell'anno scorso++ fallisce il nuovo esame."), 15, n=60).move_to(np.array([3.7, -2.4, 0]))
        self.play(FadeIn(bl), FadeIn(mt))
        loop_start(self)
        ph = ValueTracker(0.0)
        drv = Mobject(); drv.add_updater(lambda m_: uT.set_value(0.02 + 0.98 * (0.5 + 0.5 * np.cos(2 * np.pi * ph.get_value()))))
        self.add(drv); loop_play(self, ph, 8.0); drv.clear_updaters(); oz.clear_updaters()
        self.end()
