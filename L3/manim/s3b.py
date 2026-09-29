from base import *
import figs3 as F3
from s3a import scroll_group


class B3_Ritmi(Base):
    start_num = 14

    def construct(self):
        # ---------------------------------------------------------- 14 sezione
        self.new(first=True); section_title(self, 4, tr("The EEG rhythms", "I ritmi EEG"))

        # ---------------------------------------------------------- 15 spettro: 1/f + picchi che crescono
        self.new(tr("Rhythms (1)", "Ritmi (1)"), tr("The spectrum: 1/f background with peaks", "Lo spettro: fondo 1/f con picchi"))
        Wp, Hp = 6.0, 3.8; O = np.array([-6.0, -2.4, 0])
        fr = np.logspace(0, np.log10(45), 200)
        lx = lambda v: E.logpos(v, 1, 45, Wp)
        ap = lambda v, chi=1.6: -chi * np.log10(v)
        pk = lambda v, a_al, a_be: a_al * np.exp(-0.5 * ((v - 10) / 1.2) ** 2) + a_be * np.exp(-0.5 * ((v - 20) / 2.5) ** 2)
        yy = lambda L: (L + 2.8) / 3.6 * Hp
        ax = E.axes(O, Wp + 0.2, Hp + 0.2, tr("frequency (Hz, log)", "frequenza (Hz, log)"), tr("power (log)", "potenza (log)"))
        ticks = VGroup(*[VGroup(Line(O + np.array([lx(v), -0.06, 0]), O + np.array([lx(v), 0.06, 0]), color=FG, stroke_width=2), T(str(v), 14, MUT).move_to(O + np.array([lx(v), -0.3, 0]))) for v in (1, 4, 8, 13, 30)])
        a_al = ValueTracker(0.0); a_be = ValueTracker(0.0); chi = ValueTracker(1.6)

        def spec():
            L = ap(fr, chi.get_value()) + pk(fr, a_al.get_value(), a_be.get_value())
            g = VGroup(VMobject(color=TEAL, stroke_width=4).set_points_smoothly([O + np.array([lx(v), yy(l), 0]) for v, l in zip(fr, L)]))
            g.add(DashedLine(O + np.array([lx(1), yy(ap(1, chi.get_value())), 0]), O + np.array([lx(45), yy(ap(45, chi.get_value())), 0]), color=MUT, stroke_width=2))
            return g
        sz = always_redraw(spec)
        self.play(Create(ax), FadeIn(ticks), FadeIn(sz))
        la = T(tr("aperiodic 1/f", "aperiodica 1/f"), 16, MUT).move_to(O + np.array([lx(3), yy(ap(3)) - 0.45, 0]))
        self.play(FadeIn(la))
        self.play(a_al.animate.set_value(1.2), run_time=1.5)
        lp = T(tr("alpha peak", "picco alfa"), 16, ACC).move_to(O + np.array([lx(10), yy(ap(10) + 1.2) + 0.3, 0]))
        self.play(FadeIn(lp), a_be.animate.set_value(0.35), run_time=1.2)
        bl = bullets([tr("Power ∝ ++1/f^{χ}++: *aperiodic* background.", "Potenza ∝ ++1/f^{χ}++: fondo *aperiodico*."),
                      tr("*Periodic* peaks = true oscillations.", "Picchi *periodici* = vere oscillazioni."),
                      tr("~Band power ≠ oscillation~: a steeper slope changes \"theta power\" without theta!", "~Potenza di banda ≠ oscillazione~: una pendenza diversa cambia la \"potenza theta\" senza theta!"),
                      tr("χ may track the ++E/I balance++ (Gao et al., 2017).", "χ potrebbe riflettere il ++bilancio E/I++ (Gao et al., 2017).")], 18, n=36, gap=0.3).move_to(np.array([4.0, 0.0, 0]))
        for b_ in bl: self.play(FadeIn(b_))
        sz.clear_updaters()
        # loop: occhi aperti/chiusi (alfa su e giù) e pendenza che respira
        loop_start(self)
        ph = ValueTracker(0.0)
        self.remove(sz)
        sz2 = always_redraw(lambda: (a_al.set_value(0.7 + 0.5 * np.cos(2 * np.pi * ph.get_value())), chi.set_value(1.6 + 0.25 * np.sin(2 * np.pi * ph.get_value())), spec())[2])
        self.add(sz2); loop_play(self, ph, 6.0); sz2.clear_updaters()

        # ---------------------------------------------------------- 16 bande (onde che scorrono)
        self.new(tr("Rhythms (2)", "Ritmi (2)"), tr("The classical frequency bands", "Le bande di frequenza classiche"))
        bands = [("δ delta", "0.5–4 Hz", 2.0, 1.0, PURP, tr("deep sleep, infants; focal = lesion", "sonno profondo, neonati; focale = lesione")),
                 ("θ theta", "4–8 Hz", 6.0, 0.8, TEAL, tr("drowsiness; frontal-midline theta (control)", "sonnolenza; theta frontale mediano (controllo)")),
                 ("α alpha", "8–13 Hz", 10.0, 0.7, ACC, tr("posterior, eyes closed; IAF ≈10 Hz", "posteriore, occhi chiusi; IAF ≈10 Hz")),
                 ("μ mu", "8–13 Hz", 10.0, 0.55, "#E0603A", tr("sensorimotor; blocked by movement", "sensomotorio; bloccato dal movimento")),
                 ("β beta", "13–30 Hz", 20.0, 0.35, AMB, tr("sensorimotor, post-movement rebound", "sensomotorio, rebound post-movimento")),
                 ("γ gamma", "30–80 Hz", 40.0, 0.2, GRN, tr("local; ⚠ muscle, microsaccades", "locale; ⚠ muscoli, microsaccadi"))]
        Ow = -3.6; Ww = 4.2
        rows = VGroup()
        for k, (n_, r_, fq, a_, col, d_) in enumerate(bands):
            y = 1.9 - 0.8 * k
            rows.add(VGroup(TX(n_, font=SERIF_F, font_size=24, color=col, weight=BOLD).move_to(np.array([-5.8, y + 0.12, 0])), T(r_, 14, MUT).move_to(np.array([-5.8, y - 0.2, 0])),
                            T(d_, 17, n=46).move_to(np.array([0, y, 0])).align_to(np.array([1.0, 0, 0]), LEFT)))

        def waves(u):
            g = VGroup(); us = np.linspace(0, 1, 300)
            for k, (n_, r_, fq, a_, col, d_) in enumerate(bands):
                y = 1.9 - 0.8 * k
                g.add(VMobject(color=col, stroke_width=2.5).set_points_as_corners([np.array([Ow + Ww * s, y + 0.32 * a_ * np.sin(2 * np.pi * fq * (s * 0.5 - u)), 0]) for s in us]))
            return g
        w0 = waves(0.0)
        for k in range(6):
            self.play(FadeIn(rows[k]), Create(w0[k]), run_time=0.6)
        loop_start(self)
        ph = ValueTracker(0.0)
        self.remove(w0)
        wz = always_redraw(lambda: waves(ph.get_value())); self.add(wz); loop_play(self, ph, 2.0); wz.clear_updaters()

        # ---------------------------------------------------------- 17 alfa e mu: ERD
        self.new(tr("Rhythms (3)", "Ritmi (3)"), tr("Alpha and mu: same frequency, different roles", "Alfa e mu: stessa frequenza, ruoli diversi"))
        occ = [[-0.35, -0.85, 0.35], [0.35, -0.85, 0.35]]; cenm = [[-0.8, 0.0, 0.6], [0.8, 0.0, 0.6]]
        Va, ma = F3.smooth_map(occ, 0.45, 101); Vm, mm = F3.smooth_map(cenm, 0.45, 101)
        ca = np.array([-4.6, 0.5, 0]); cmu = np.array([-1.6, 0.5, 0]); Rr = 1.2
        fa = ValueTracker(1.0); fm = ValueTracker(1.0)
        mz = redraw(lambda: Group(*E.topomap(Va * fa.get_value(), ma, ca, Rr, vmax=1.0), *E.topomap(Vm * fm.get_value(), mm, cmu, Rr, vmax=1.0)))
        la = T(tr("alpha", "alfa"), 20, ACC).next_to(ca + DOWN * Rr, DOWN, buff=0.2); lm = T("mu", 20, ACC).next_to(cmu + DOWN * Rr, DOWN, buff=0.2)
        self.play(FadeIn(mz), FadeIn(la), FadeIn(lm))
        ev = always_redraw(lambda: T(tr("eyes open", "occhi aperti") if fa.get_value() < 0.5 else tr("eyes closed", "occhi chiusi"), 18, TEAL).move_to(ca + UP * (Rr + 0.45)))
        mv = always_redraw(lambda: T(tr("movement", "movimento") if fm.get_value() < 0.5 else tr("rest", "riposo"), 18, TEAL).move_to(cmu + UP * (Rr + 0.45)))
        self.add(ev, mv)
        self.play(fa.animate.set_value(0.15), run_time=1.2); self.play(fa.animate.set_value(1.0), run_time=1.0)
        self.play(fm.animate.set_value(0.15), run_time=1.2); self.play(fm.animate.set_value(1.0), run_time=1.0)
        for m in (mz, ev, mv): m.clear_updaters()
        bl = bullets([tr("*Alpha*: occipito-parietal, blocked by ++visual input++.", "*Alfa*: occipito-parietale, bloccato dall'++input visivo++."),
                      tr("*Mu*: C3/C4, blocked by ++movement++, ++motor imagery++, action observation.", "*Mu*: C3/C4, bloccato da ++movimento++, ++immaginazione motoria++, osservazione."),
                      tr("Power decrease = *ERD*; increase = *ERS* → motor-imagery BCIs.", "Calo di potenza = *ERD*; aumento = *ERS* → BCI a immaginazione motoria.")], 18, n=38, gap=0.3).move_to(np.array([3.9, 0.6, 0]))
        for b_ in bl: self.play(FadeIn(b_))
        mt = metaphor(tr("idle rhythms are an engine ++idling++: give the region work and the hum disappears.", "i ritmi di riposo sono un motore ++al minimo++: dai lavoro alla regione e il ronzio sparisce."), 18, 100).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(mt))
        loop_start(self)
        ph = ValueTracker(0.0)
        self.remove(mz, ev, mv)
        sq = lambda u: 0.15 + 0.85 * (0.5 + 0.5 * np.cos(2 * np.pi * u))
        mz2 = redraw(lambda: (fa.set_value(sq(ph.get_value())), fm.set_value(sq(ph.get_value() + 0.5)), Group(*E.topomap(Va * fa.get_value(), ma, ca, Rr, vmax=1.0), *E.topomap(Vm * fm.get_value(), mm, cmu, Rr, vmax=1.0)))[2])
        ev2 = always_redraw(lambda: T(tr("eyes open", "occhi aperti") if sq(ph.get_value()) < 0.5 else tr("eyes closed", "occhi chiusi"), 18, TEAL).move_to(ca + UP * (Rr + 0.45)))
        mv2 = always_redraw(lambda: T(tr("movement", "movimento") if sq(ph.get_value() + 0.5) < 0.5 else tr("rest", "riposo"), 18, TEAL).move_to(cmu + UP * (Rr + 0.45)))
        self.add(mz2, ev2, mv2); loop_play(self, ph, 6.0)
        for m in (mz2, ev2, mv2): m.clear_updaters()

        # ---------------------------------------------------------- 18 ampiezza vs frequenza
        self.new(tr("Rhythms (4)", "Ritmi (4)"), tr("Slower rhythms are larger", "I ritmi lenti sono più ampi"))
        f = F3.f21_ampfreq(5.5, 3.4); fit(f, 1.0, np.array([-3.0, -0.3, 0]))
        self.play(FadeIn(f["ax"]), Create(f["c"]))
        self.play(LaggedStart(*[AnimationGroup(FadeIn(f[f"d{k}"], scale=2), FadeIn(f[f"l{k}"])) for k in range(5)], lag_ratio=0.2), FadeIn(f["n"]))
        bl = bullets([tr("Oscillations need ++round trips++; conduction delays limit the speed of large loops.", "Le oscillazioni richiedono ++andata e ritorno++; i ritardi limitano la velocità dei grandi anelli."),
                      tr("~Slow~ = ++large++ networks → large EEG; ~fast~ = ++local++.", "~Lenti~ = reti ++ampie++ → EEG ampio; ~veloci~ = ++locali++."),
                      tr("Rhythms form a ++hierarchy++ (Buzsáki & Draguhn, 2004).", "I ritmi formano una ++gerarchia++ (Buzsáki & Draguhn, 2004).")], 18, n=36, gap=0.35).move_to(np.array([3.8, 0.0, 0]))
        for b_ in bl: self.play(FadeIn(b_))

        # ---------------------------------------------------------- 19 sezione
        self.new(); section_title(self, 5, tr("Resting-state EEG, vigilance and sleep", "EEG a riposo, vigilanza e sonno"))

        # ---------------------------------------------------------- 20 vigilanza (tracce che scorrono)
        self.new(tr("Resting state (1)", "Stato di riposo (1)"), tr("Resting EEG probes arousal and vigilance", "L'EEG a riposo sonda arousal e vigilanza"))
        f = F3.f22_vigilance(7.0); fit(f, 0.85, np.array([0.3, 0.0, 0]))
        for k in range(5):
            self.play(Create(f[f"x{k}"]), FadeIn(f[f"l{k}"]), run_time=0.8)
        self.play(FadeIn(f["sb"]))
        cap = T(tr("In a few minutes of \"rest\" people drift along the ++vigilance continuum++: ~control it~ when comparing groups.", "In pochi minuti di \"riposo\" si scivola lungo il ++continuum di vigilanza++: ~controllarla~ quando si confrontano gruppi."), 19, n=100).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(cap))
        t, S = F3.stage_signals()
        Os = [np.array([f[f"x{k}"].get_left()[0], f[f"x{k}"].get_center()[1], 0]) for k in range(5)]
        Os = [np.array([f[f"x{k}"].points[0][0], f[f"x{k}"].points[0][1] - S[k][0] * 0.006 * 0.85, 0]) for k in range(5)]
        cols = [AMB, ACC, TEAL, PURP, "#9FB0E0"]
        scroll_group(self, [(t, s) for s in S], Os, f["x0"].get_width(), 0.006 * 0.85, 4.0, cols, 8.0, sw=1.8, old=VGroup(*[f[f"x{k}"] for k in range(5)]))

        # ---------------------------------------------------------- 21 sonno: cursore sull'ipnogramma
        self.new(tr("Resting state (2)", "Stato di riposo (2)"), tr("Sleep: the EEG defines the stages", "Sonno: l'EEG definisce gli stadi"))
        f = F3.f23_hypnogram(7.6, 2.6); fit(f, 1.0, np.array([-2.2, 0.3, 0]))
        self.play(*[FadeIn(f[k]) for k in f if k != "h"])
        self.play(Create(f["h"]), run_time=3, rate_func=linear)
        bl = bullets([tr("*N1*: alpha disappears, theta.", "*N1*: l'alfa scompare, theta."), tr("*N2*: ++spindles++, ++K-complexes++.", "*N2*: ++fusi++, ++complessi K++."),
                      tr("*N3*: ++slow waves++ (<2 Hz).", "*N3*: ++onde lente++ (<2 Hz)."), tr("*REM*: wake-like EEG, atonia.", "*REM*: EEG simile alla veglia, atonia.")], 18, n=26, gap=0.3).move_to(np.array([4.9, 0.6, 0]))
        for b_ in bl: self.play(FadeIn(b_))
        nb = card(T(tr("Spindles and delta come from ++thalamocortical burst mode++ (Lecture 2).", "Fusi e delta nascono dal ++modo burst talamo-corticale++ (Lezione 2)."), 18, n=90), CARD2).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(nb))
        hyp = f["h"]
        loop_start(self)
        ph = ValueTracker(0.0)
        cur = always_redraw(lambda: Dot(hyp.point_from_proportion(ph.get_value() * 0.999), radius=0.1, color=AMB))
        self.add(cur); loop_play(self, ph, 8.0); cur.clear_updaters()

        # ---------------------------------------------------------- 22 domande
        self.new(tr("Check your understanding", "Verifica"), tr("Three questions", "Tre domande"))
        g = rows_mob([tr("Positive maximum at C3, negative at P3: where is the source?", "Massimo positivo in C3, negativo in P3: dov'è la sorgente?"),
                      tr("Fz and FCz are highly correlated: do they communicate?", "Fz e FCz sono molto correlati: comunicano?"),
                      tr("More \"theta power\" in patients: two alternative explanations?", "Più \"potenza theta\" nei pazienti: due spiegazioni alternative?")], 22, n=80, h=1.05, gap=0.35, col=ACC).shift(DOWN * 0.3)
        for r_ in g: self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.7)

        # ---------------------------------------------------------- 23 messaggi chiave
        self.new(tr("Take-home messages", "Messaggi chiave"), tr("Take-home messages", "Messaggi chiave"))
        g = rows_mob([tr("EEG = ++macroscopic++ view of synchronised LFPs.", "EEG = visione ++macroscopica++ di LFP sincronizzati."),
                      tr("++Dipoles++: radial → one extremum, tangential → a pair; ∝ 1/r².", "++Dipoli++: radiale → un estremo, tangenziale → una coppia; ∝ 1/r²."),
                      tr("Skull ++blurs++; V = L·j is ++linear++; channels are correlated.", "Il cranio ++sfoca++; V = L·j è ++lineare++; i canali sono correlati."),
                      tr("Spectrum = ++1/f++ + ++peaks++; bands have topographies.", "Spettro = ++1/f++ + ++picchi++; le bande hanno topografie."),
                      tr("Resting EEG reflects ++vigilance++; sleep stages are EEG-defined.", "L'EEG a riposo riflette la ++vigilanza++; il sonno è definito dall'EEG.")], 21).shift(DOWN * 0.35)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.25), run_time=2.5)

        # ---------------------------------------------------------- 24 letture
        self.new(tr("Suggested reading", "Letture consigliate"), tr("Suggested reading", "Letture consigliate"))
        refs_slide(self, ["Nunez & Srinivasan (2006) *Electric Fields of the Brain*, 2nd ed., OUP.", "Buzsáki (2006) *Rhythms of the Brain*, OUP.",
                          "Buzsáki & Draguhn (2004) *Science* 304:1926–1929.", "Varela et al. (2001) *Nat Rev Neurosci* 2:229–239.",
                          "Olejniczak (2006) *J Clin Neurophysiol* 23:186–189.", "Vorwerk et al. (2014) *NeuroImage* 100:590–607.",
                          "Donoghue et al. (2020) *Nat Neurosci* 23:1655–1665.", "Pfurtscheller & Lopes da Silva (1999) *Clin Neurophysiol* 110:1842–1857.",
                          "Babiloni et al. (2020) *Clin Neurophysiol* 131:285–307."])
        self.end()
