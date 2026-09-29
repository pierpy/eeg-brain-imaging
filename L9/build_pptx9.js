// EEG – Lecture 9: source imaging and connectivity (bilingue: node build_pptx9.js en|it)
const __R = (function () { const p = require("path"), fs = require("fs"); let d = process.env.COURSE_ROOT || __dirname;
  while (!fs.existsSync(p.join(d, ".course_root")) && p.dirname(d) !== d) d = p.dirname(d); return d; })();
const LANGARG = process.argv[2] || "en";
global.CFG = { lang: LANGARG, fig: __R + "/L9/figpng_" + LANGARG, common: __R + "/common",
  footer: LANGARG === "it" ? "Brain Imaging · EEG · Lezione 9 · Sorgenti e connettività" : "Brain Imaging · EEG · Lecture 9 · Source imaging and connectivity",
  lezione: LANGARG === "it" ? "Lezione 9" : "Lecture 9",
  titolo: LANGARG === "it" ? "Dallo scalpo al cervello:\nsorgenti e connettività" : "From scalp to brain:\nsources and connectivity", titoloSize: 40 };
const L = require(__R + "/common/pptlib_eeg.js");
const { tr: t, pres, fig, content, text, formula, card, badge, copertina, save } = L;
const { INK, ACC, TEAL, TXT, MUTED, TINT, WHITE, SERIF, SANS, W, H, MX, X0, Y0, CW } = L.C;
const OUT = process.argv[3] || `${__R}/L9/out/EEG_L9_${LANGARG}.pptx`;
const PEACH = "FDF0E9";
function note(s, str, x, y, w, h, sz = 17, fill = TINT) { card(s, x, y, w, h, fill); text(s, [str], x + 0.25, y + 0.05, w - 0.5, h - 0.1, { sz, valign: "middle", align: "center" }); }
function meta(s, str, x, y, w, h, sz = 17) { card(s, x, y, w, h, PEACH); text(s, [{ t: "~" + t("Metaphor", "Metafora") + "~  " + str }], x + 0.25, y + 0.05, w - 0.5, h - 0.1, { sz, valign: "middle" }); }
function section(n, en, it) { return L.sezione(n, t(en, it)); }
function rows(s, items, x, y, w, h, gap, sz = 18, colBadge = TEAL) {
  items.forEach((it, i) => { const yy = y + i * (h + gap); card(s, x, yy, w, h, i % 2 ? PEACH : TINT); badge(s, i + 1, x + 0.18, yy + h / 2 - 0.23, colBadge); text(s, [it], x + 0.85, yy, w - 1.05, h, { sz, valign: "middle" }); });
}
function cards(s, items, y, h, sz = 15) {
  const n = items.length, w = (CW - 0.2 * (n - 1)) / n;
  items.forEach(([hd, d], i) => { const x = X0 + i * (w + 0.2); card(s, x, y, w, h, i % 2 ? PEACH : TINT); text(s, [{ t: "~" + hd + "~" }, { t: d }], x + 0.2, y + 0.1, w - 0.4, h - 0.2, { sz, after: 6 }); });
}
const B = (en, it) => ({ t: t(en, it), b: true });

copertina();

// 2 obiettivi
{
  const s = content(t("Lecture 9", "Lezione 9"), t("Today: where and how brain regions talk", "Oggi: dove e come dialogano le regioni cerebrali"),
    { notes: t("Main references: Michel et al. (2004) Clin Neurophysiol 115:2195; Michel & Brunet (2019) Front Neurol 10:325 (EEG source imaging: a practical review); Bastos & Schoffelen (2016) Front Syst Neurosci 9:175 (connectivity tutorial).", "Riferimenti principali: Michel et al. (2004) Clin Neurophysiol 115:2195; Michel & Brunet (2019) Front Neurol 10:325 (EEG source imaging: review pratica); Bastos & Schoffelen (2016) Front Syst Neurosci 9:175 (tutorial sulla connettività).") });
  rows(s, [t("*Forward problem*: head models and the ++lead field++.", "*Problema diretto*: modelli di testa e ++lead field++."),
    t("*Inverse problem*: why it is ++ill-posed++ and how priors solve it.", "*Problema inverso*: perché è ++mal posto++ e come lo risolvono le ipotesi a priori."),
    t("Dipole fitting, MNE, sLORETA/eLORETA, ++beamformers++.", "Fit di dipoli, MNE, sLORETA/eLORETA, ++beamformer++."),
    t("*Connectivity*: coherence, PLV, wPLI, Granger — and the ++volume-conduction++ trap.", "*Connettività*: coerenza, PLV, wPLI, Granger — e la trappola della ++conduzione di volume++."),
    t("*Graph theory*: the brain as a network.", "*Teoria dei grafi*: il cervello come rete.")], X0, Y0, CW, 0.85, 0.15, 18);
}

// 3 forward/inverse
{
  const s = content(t("Two problems", "Due problemi"), t("Forward and inverse problems", "Problema diretto e problema inverso"),
    { notes: t("Forward: given sources and a head model, compute scalp potentials — unique solution (Helmholtz, 1853, showed the inverse is not). Inverse: given scalp data, estimate sources — infinitely many solutions without constraints.", "Diretto: date sorgenti e modello di testa, calcolare i potenziali di scalpo — soluzione unica (Helmholtz, 1853, mostrò che l'inverso non lo è). Inverso: dati i potenziali, stimare le sorgenti — infinite soluzioni senza vincoli.") });
  fig(s, "f03_forward", X0, Y0, 7.4, 3.6, "l", "Forward and inverse");
  formula(s, "y(t) = L · j(t) + n(t)", 8.2, Y0, 4.5, 0.8, { sz: 24, fill: PEACH });
  text(s, [B("*Forward*: sources + head model → scalp map. ++Unique++, pure physics.", "*Diretto*: sorgenti + modello di testa → mappa di scalpo. ++Unico++, pura fisica."),
    B("*Inverse*: scalp map → sources. ++Not unique++ (Helmholtz, 1853): infinitely many source configurations give the same map.", "*Inverso*: mappa di scalpo → sorgenti. ++Non unico++ (Helmholtz, 1853): infinite configurazioni danno la stessa mappa."),
    B("Solutions need ++priors++: few dipoles, minimum energy, smoothness, sparsity…", "Le soluzioni richiedono ++ipotesi a priori++: pochi dipoli, minima energia, regolarità, sparsità…")], 8.2, 2.5, 4.5, 3.9, { sz: 15, after: 12 });
  meta(s, t("hearing a ++chord++ and guessing which fingers pressed which keys: many answers are possible.", "sentire un ++accordo++ e indovinare quali dita hanno premuto quali tasti: molte risposte sono possibili."), X0, 5.9, 7.4, 0.8, 15);
}

section(1, "The forward problem", "Il problema diretto");

// 5 modelli di testa
{
  const s = content(t("Forward (1)", "Diretto (1)"), t("Head models", "Modelli di testa"),
    { notes: t("Spherical models: Berg & Scherg (1994). BEM: Fuchs et al. (2002), OpenMEEG (Gramfort et al., 2010). FEM: Vorwerk et al. (2014) NeuroImage 100:590 — including CSF and grey/white distinction matters; skull conductivity is the main uncertainty. Template head (MNI) if no individual MRI; digitised electrode positions improve accuracy.", "Modelli sferici: Berg & Scherg (1994). BEM: Fuchs et al. (2002), OpenMEEG (Gramfort et al., 2010). FEM: Vorwerk et al. (2014) NeuroImage 100:590 — includere liquor e distinzione grigia/bianca conta; la conducibilità del cranio è la principale incertezza. Testa template (MNI) se manca la RM individuale; le posizioni digitalizzate degli elettrodi migliorano l'accuratezza.") });
  fig(s, "f05_headmodels", X0, Y0, CW, 2.9, "c", "Head models");
  rows(s, [t("Tissues differ in conductivity: the ++skull++ (≈ 0.01 S/m) is ≈ 30–50× less conductive than scalp and brain (Lecture 3).", "I tessuti hanno conducibilità diverse: il ++cranio++ (≈ 0,01 S/m) conduce ≈ 30–50× meno di scalpo e cervello (Lezione 3)."),
    t("Individual ++MRI++ or a ++template++ (MNI) head; ++digitised++ electrode positions.", "++RM++ individuale o testa ++template++ (MNI); posizioni degli elettrodi ++digitalizzate++."),
    t("Main uncertainty: ++skull conductivity++ and holes; FEM can include CSF and anisotropy (Vorwerk et al., 2014).", "Incertezza principale: ++conducibilità del cranio++ e fori; il FEM include liquor e anisotropia (Vorwerk et al., 2014).")], X0, 4.45, CW, 0.66, 0.12, 15);
}

// 6 lead field
{
  const s = content(t("Forward (2)", "Diretto (2)"), t("The lead field matrix", "La matrice lead field"),
    { notes: t("Source space: a few thousand dipoles on the cortical surface (orientation fixed normal to cortex) or on a volumetric grid (3 orientations each). L has size N_electrodes × N_sources; each column is the scalp topography produced by a unit dipole. Computed once per subject/head model.", "Spazio delle sorgenti: qualche migliaio di dipoli sulla superficie corticale (orientazione fissa normale alla corteccia) o su una griglia volumetrica (3 orientazioni ciascuno). L ha dimensione N_elettrodi × N_sorgenti; ogni colonna è la topografia prodotta da un dipolo unitario. Si calcola una volta per soggetto/modello di testa.") });
  fig(s, "f06_leadfield", X0, Y0, 8.0, 3.2, "l", "Lead field");
  text(s, [B("*Source space*: thousands of dipoles on the ++cortical surface++ (orientation normal to it) or on a 3D grid.", "*Spazio delle sorgenti*: migliaia di dipoli sulla ++superficie corticale++ (orientati normalmente) o su una griglia 3D."),
    B("*L* (electrodes × sources): column k = ++scalp map of a unit dipole++ at k.", "*L* (elettrodi × sorgenti): colonna k = ++mappa di scalpo di un dipolo unitario++ in k."),
    B("Superficial sources have ++large++ columns, deep ones ++small++: a built-in depth bias.", "Le sorgenti superficiali hanno colonne ++grandi++, quelle profonde ++piccole++: un bias di profondità intrinseco.")], 8.6, Y0, 4.1, 4.8, { sz: 15, after: 12 });
  formula(s, "N_{el} ≈ 64–256   ≪   N_{src} ≈ 5 000–15 000", X0, 4.9, 8.0, 0.75, { sz: 20, fill: PEACH });
}

section(2, "The inverse problem", "Il problema inverso");

// 8 mal posto
{
  const s = content(t("Inverse (1)", "Inverso (1)"), t("An ill-posed problem", "Un problema mal posto"),
    { notes: t("Underdetermined linear system: any vector in the null space of L can be added to a solution without changing the data. Plus: noise, head model errors. Constraints (priors) select one solution; different priors → different answers.", "Sistema lineare sottodeterminato: qualunque vettore nello spazio nullo di L può essere aggiunto a una soluzione senza cambiare i dati. In più: rumore, errori del modello di testa. I vincoli (ipotesi) selezionano una soluzione; ipotesi diverse → risposte diverse.") });
  fig(s, "f07_illposed", X0, Y0, 7.2, 3.9, "l", "Ill-posed");
  text(s, [B("Far fewer ++equations++ (electrodes) than ++unknowns++ (sources).", "Molte meno ++equazioni++ (elettrodi) che ++incognite++ (sorgenti)."),
    B("\"Silent\" source patterns (++null space++ of L) can be added without changing the data.", "Configurazioni \"silenti\" (++spazio nullo++ di L) si possono aggiungere senza cambiare i dati."),
    B("Every method = a ++prior++ about what solutions are plausible.", "Ogni metodo = un'++ipotesi a priori++ su quali soluzioni sono plausibili."),
    B("⚠ Results are ++estimates++ with limited spatial resolution (≈ cm).", "⚠ I risultati sono ++stime++ con risoluzione spaziale limitata (≈ cm).")], 7.9, Y0, 4.8, 4.8, { sz: 15, after: 12 });
}

// 9 dipoli
{
  const s = content(t("Inverse (2)", "Inverso (2)"), t("Equivalent current dipoles", "Dipoli di corrente equivalenti"),
    { notes: t("Scherg & Von Cramon (1985); Mosher, Lewis & Leahy (1992) IEEE TBME 39:541. Non-linear search of position (and linear estimate of moment) minimising residual variance. Works well for focal activity (early ERP components, interictal spikes). Requires the number of dipoles a priori; local minima.", "Scherg & Von Cramon (1985); Mosher, Lewis & Leahy (1992) IEEE TBME 39:541. Ricerca non lineare della posizione (e stima lineare del momento) che minimizza la varianza residua. Funziona bene per attività focale (componenti ERP precoci, spike intercritici). Richiede il numero di dipoli a priori; minimi locali.") });
  formula(s, "min_{pos}  ‖ y − L(pos) · q ‖²      →  residual variance, GOF", X0 + 1.5, Y0, CW - 3.0, 0.8, { sz: 20, fill: PEACH });
  cards(s, [[t("Idea", "Idea"), t("assume ++one or few++ dipoles; search position and orientation that best explain the map.", "assumere ++uno o pochi++ dipoli; cercare posizione e orientazione che spiegano meglio la mappa.")],
    [t("When it works", "Quando funziona"), t("++focal++ activity: early evoked components, ++interictal spikes++ in epilepsy.", "attività ++focale++: componenti evocate precoci, ++spike intercritici++ nell'epilessia.")],
    [t("Limits", "Limiti"), t("number of dipoles must be ++chosen a priori++; local minima; fails for ++extended++ sources.", "il numero di dipoli va ++scelto a priori++; minimi locali; fallisce per sorgenti ++estese++.")]], 2.5, 2.6, 15);
  note(s, t("Goodness of fit (GOF) > 90 % is necessary but ++not sufficient++: a wrong model can fit well.", "Una bontà di adattamento (GOF) > 90 % è necessaria ma ++non sufficiente++: un modello sbagliato può adattarsi bene."), X0, 5.4, CW, 0.8, 16);
}

// 10 metodi distribuiti
{
  const s = content(t("Inverse (3)", "Inverso (3)"), t("Distributed solutions: MNE, sLORETA, beamformers", "Soluzioni distribuite: MNE, sLORETA, beamformer"),
    { notes: t("MNE: Hämäläinen & Ilmoniemi (1994) Med Biol Eng Comput 32:35; LORETA: Pascual-Marqui et al. (1994) Int J Psychophysiol 18:49; sLORETA: Pascual-Marqui (2002) Methods Find Exp Clin Pharmacol 24D:5; eLORETA: Pascual-Marqui (2007) arXiv; LCMV beamformer: Van Veen et al. (1997) IEEE TBME 44:867. Simulated 2D model: one source at 10 Hz plus noise.", "MNE: Hämäläinen & Ilmoniemi (1994) Med Biol Eng Comput 32:35; LORETA: Pascual-Marqui et al. (1994) Int J Psychophysiol 18:49; sLORETA: Pascual-Marqui (2002) Methods Find Exp Clin Pharmacol 24D:5; eLORETA: Pascual-Marqui (2007) arXiv; beamformer LCMV: Van Veen et al. (1997) IEEE TBME 44:867. Modello 2D simulato: una sorgente a 10 Hz più rumore.") });
  fig(s, "f10_methods", X0, Y0, CW, 1.9, "c", "Inverse methods");
  formula(s, "ĵ = W Lᵀ (L W Lᵀ + λ I)^{−1} y", X0 + 3.3, 3.5, CW - 6.6, 0.7, { sz: 20, fill: PEACH });
  cards(s, [["MNE", t("smallest-energy solution; ++biased to the surface++; use depth weighting (W).", "soluzione a minima energia; ++sbilanciata verso la superficie++; usare pesi di profondità (W).")],
    ["sLORETA / eLORETA", t("standardised MNE; ++zero localisation error++ for single sources (in theory); blurred.", "MNE standardizzato; ++errore di localizzazione nullo++ per sorgente singola (in teoria); sfocato.")],
    [t("LCMV / DICS beamformer", "Beamformer LCMV / DICS"), t("spatial filter per location using the ++data covariance++; focal, but fails with ++correlated sources++.", "filtro spaziale per ogni posizione usando la ++covarianza dei dati++; focale, ma fallisce con ++sorgenti correlate++.")],
    [t("Sparse / Bayesian", "Sparsi / bayesiani"), t("MxNE, MSP, Champagne: favour ++few active sources++.", "MxNE, MSP, Champagne: privilegiano ++poche sorgenti attive++.")]], 4.4, 2.2, 13);
}

// 11 regolarizzazione e accuratezza
{
  const s = content(t("Inverse (4)", "Inverso (4)"), t("Regularisation and what limits accuracy", "Regolarizzazione e limiti di accuratezza"),
    { notes: t("λ is often set from the SNR (MNE-Python default λ² = 1/SNR² with SNR = 3). Accuracy: number and positions of electrodes (≥ 64, full coverage incl. inferior: Michel & Brunet, 2019; Song et al., 2015 NeuroImage), head model, noise covariance. Validation with intracranial recordings or simulations.", "λ spesso si fissa dall'SNR (default MNE-Python λ² = 1/SNR² con SNR = 3). Accuratezza: numero e posizioni degli elettrodi (≥ 64, copertura completa anche inferiore: Michel & Brunet, 2019; Song et al., 2015 NeuroImage), modello di testa, covarianza del rumore. Validazione con registrazioni intracraniche o simulazioni.") });
  fig(s, "f11_lambda", X0 + 1.0, Y0, CW - 2.0, 2.3, "c", "Regularisation");
  rows(s, [t("λ trades ++fit to the data++ against ++smoothness/energy++: too small fits noise, too large blurs.", "λ bilancia l'++adattamento ai dati++ e la ++regolarità/energia++: troppo piccolo segue il rumore, troppo grande sfoca."),
    t("Accuracy needs ++≥ 64 electrodes++ with ++full head coverage++ (inferior temporal and occipital too) (Michel & Brunet, 2019).", "L'accuratezza richiede ++≥ 64 elettrodi++ con ++copertura completa++ (anche temporale inferiore e occipitale) (Michel & Brunet, 2019)."),
    t("Plus: good ++head model++, digitised positions, noise covariance from baseline.", "Inoltre: buon ++modello di testa++, posizioni digitalizzate, covarianza del rumore dalla baseline."),
    t("Validate with ++simulations++ and, when possible, ++intracranial++ data.", "Validare con ++simulazioni++ e, quando possibile, dati ++intracranici++.")], X0, 4.0, CW, 0.6, 0.1, 15, ACC);
}

section(3, "Functional connectivity", "Connettività funzionale");

// 13 tipi di connettività
{
  const s = content(t("Connectivity (1)", "Connettività (1)"), t("Structural, functional, effective", "Strutturale, funzionale, effettiva"),
    { notes: t("Friston (2011) Brain Connect 1:13 — functional (statistical dependence) vs effective (causal influence) connectivity. Bastos & Schoffelen (2016). Metrics families: amplitude-based (envelope correlation), phase-based (coherence, PLV, PLI/wPLI), directed (Granger, PDC, DTF), model-based (DCM).", "Friston (2011) Brain Connect 1:13 — connettività funzionale (dipendenza statistica) vs effettiva (influenza causale). Bastos & Schoffelen (2016). Famiglie di metriche: basate sull'ampiezza (correlazione degli inviluppi), sulla fase (coerenza, PLV, PLI/wPLI), dirette (Granger, PDC, DTF), basate su modelli (DCM).") });
  cards(s, [[t("Structural", "Strutturale"), t("anatomical links (white-matter tracts, DTI).", "connessioni anatomiche (fasci di sostanza bianca, DTI).")],
    [t("Functional", "Funzionale"), t("++statistical dependence++ between signals: correlation, coherence, phase locking. No direction.", "++dipendenza statistica++ tra segnali: correlazione, coerenza, aggancio di fase. Senza direzione.")],
    [t("Effective", "Effettiva"), t("++directed++ influence: Granger causality, PDC/DTF, dynamic causal modelling (Friston, 2011).", "influenza ++diretta++: causalità di Granger, PDC/DTF, dynamic causal modelling (Friston, 2011).")]], Y0, 2.3, 15);
  rows(s, [t("*Amplitude*-based: correlation of band-limited envelopes (orthogonalised; Hipp et al., 2012).", "Basate sull'*ampiezza*: correlazione degli inviluppi in banda (ortogonalizzati; Hipp et al., 2012)."),
    t("*Phase*-based: coherence, PLV, imaginary coherence, PLI/wPLI.", "Basate sulla *fase*: coerenza, PLV, coerenza immaginaria, PLI/wPLI."),
    t("*Directed*: Granger, PDC, DTF (multivariate autoregressive models).", "*Dirette*: Granger, PDC, DTF (modelli autoregressivi multivariati).")], X0, 3.9, CW, 0.66, 0.12, 15, ACC);
}

// 14 conduzione di volume
{
  const s = content(t("Connectivity (2)", "Connettività (2)"), t("The volume-conduction trap", "La trappola della conduzione di volume"),
    { notes: t("Nolte et al. (2004) Clin Neurophysiol 115:2292; Schoffelen & Gross (2009) Hum Brain Mapp 30:1857; Palva et al. (2018) NeuroImage 173:632 (ghost interactions). Volume conduction is instantaneous at EEG frequencies (quasi-static approximation), so it produces zero-lag correlations. Source-level analysis reduces but does not remove leakage.", "Nolte et al. (2004) Clin Neurophysiol 115:2292; Schoffelen & Gross (2009) Hum Brain Mapp 30:1857; Palva et al. (2018) NeuroImage 173:632 (interazioni fantasma). La conduzione di volume è istantanea alle frequenze EEG (approssimazione quasi-statica), quindi produce correlazioni a ritardo zero. L'analisi alle sorgenti riduce ma non elimina il leakage.") });
  fig(s, "f14_vc", X0, Y0, CW, 3.0, "c", "Volume conduction");
  rows(s, [t("One source is seen by ++many electrodes++ at the ++same instant++ → spurious ++zero-lag++ coupling.", "Una sorgente è vista da ++molti elettrodi++ nello ++stesso istante++ → accoppiamento spurio a ++ritardo zero++."),
    t("The ++reference++ adds its own common signal to all channels.", "Il ++riferimento++ aggiunge il proprio segnale comune a tutti i canali."),
    t("Remedies: ++source-level++ analysis + ++lag-based++ metrics (imaginary coherence, wPLI) or ++orthogonalisation++.", "Rimedi: analisi ++alle sorgenti++ + metriche ++basate sul ritardo++ (coerenza immaginaria, wPLI) o ++ortogonalizzazione++.")], X0, 4.75, CW, 0.62, 0.1, 15, ACC);
}

// 15 coerenza e fase
{
  const s = content(t("Connectivity (3)", "Connettività (3)"), t("Coherence, PLV and lag-based measures", "Coerenza, PLV e misure basate sul ritardo"),
    { notes: t("Coherence: |S_xy|²/(S_xx S_yy). PLV: Lachaux et al. (1999) Hum Brain Mapp 8:194. Imaginary coherence: Nolte et al. (2004). PLI: Stam et al. (2007) Hum Brain Mapp 28:1178. wPLI: Vinck et al. (2011) NeuroImage 55:1548 (debiased version recommended). All are biased by the number of trials.", "Coerenza: |S_xy|²/(S_xx S_yy). PLV: Lachaux et al. (1999) Hum Brain Mapp 8:194. Coerenza immaginaria: Nolte et al. (2004). PLI: Stam et al. (2007) Hum Brain Mapp 28:1178. wPLI: Vinck et al. (2011) NeuroImage 55:1548 (consigliata la versione debiased). Tutte sono distorte dal numero di trial.") });
  fig(s, "f16_phase", X0, Y0, CW, 2.8, "c", "Phase measures");
  formula(s, "PLV = | ⟨ e^{iΔφ} ⟩ |          wPLI = | ⟨ Im S_{xy} ⟩ | / ⟨ | Im S_{xy} | ⟩", X0 + 1.2, 4.3, CW - 2.4, 0.7, { sz: 19, fill: PEACH });
  text(s, [B("*Coherence* / *PLV*: consistency of the phase difference — ++high also at zero lag++ (volume conduction!).", "*Coerenza* / *PLV*: costanza della differenza di fase — ++alta anche a ritardo zero++ (conduzione di volume!)."),
    B("*Imaginary coherence*, *PLI*, *wPLI*: use only the ++non-zero-lag++ part → insensitive to instantaneous mixing (but also to true zero-lag coupling).", "*Coerenza immaginaria*, *PLI*, *wPLI*: usano solo la parte a ++ritardo non nullo++ → insensibili alla miscelazione istantanea (ma anche all'accoppiamento vero a ritardo zero).")], X0, 5.15, CW, 1.5, { sz: 15, after: 6 });
}

// 16 Granger
{
  const s = content(t("Connectivity (4)", "Connettività (4)"), t("Directed connectivity: Granger causality", "Connettività diretta: causalità di Granger"),
    { notes: t("Granger (1969) Econometrica 37:424; Seth, Barrett & Barnett (2015) J Neurosci 35:3293 (Granger causality analysis in neuroscience); DTF: Kamiński & Blinowska (1991) Biol Cybern 65:203; PDC: Baccalá & Sameshima (2001) Biol Cybern 84:463. Caveats: stationarity, model order, common inputs, volume conduction and filtering can create spurious causality.", "Granger (1969) Econometrica 37:424; Seth, Barrett & Barnett (2015) J Neurosci 35:3293 (analisi di Granger in neuroscienze); DTF: Kamiński & Blinowska (1991) Biol Cybern 65:203; PDC: Baccalá & Sameshima (2001) Biol Cybern 84:463. Cautele: stazionarietà, ordine del modello, ingressi comuni, conduzione di volume e filtraggio possono creare causalità spuria.") });
  fig(s, "f18_granger", X0, Y0, CW, 2.8, "c", "Granger");
  text(s, [B("X \"Granger-causes\" Y if the ++past of X++ improves the prediction of Y beyond Y's own past (Granger, 1969).", "X \"Granger-causa\" Y se il ++passato di X++ migliora la predizione di Y oltre il passato di Y stesso (Granger, 1969)."),
    B("Estimated with ++autoregressive models++; spectral versions: ++PDC, DTF++, spectral Granger.", "Stimata con ++modelli autoregressivi++; versioni spettrali: ++PDC, DTF++, Granger spettrale."),
    B("⚠ Prediction ≠ causation: common inputs, filtering and volume conduction can create ++spurious directions++ (Seth et al., 2015).", "⚠ Predizione ≠ causa: ingressi comuni, filtraggio e conduzione di volume possono creare ++direzioni spurie++ (Seth et al., 2015).")], X0, 4.75, CW, 1.9, { sz: 15, after: 8 });
}

// 17 grafi
{
  const s = content(t("Networks", "Reti"), t("The brain as a graph", "Il cervello come grafo"),
    { notes: t("Bullmore & Sporns (2009) Nat Rev Neurosci 10:186; Rubinov & Sporns (2010) NeuroImage 52:1059 (Brain Connectivity Toolbox, MATLAB). Watts & Strogatz (1998) Nature 393:440 (small world). Graph metrics depend on thresholding, density, number of nodes: compare networks with matched density and null models.", "Bullmore & Sporns (2009) Nat Rev Neurosci 10:186; Rubinov & Sporns (2010) NeuroImage 52:1059 (Brain Connectivity Toolbox, MATLAB). Watts & Strogatz (1998) Nature 393:440 (small world). Le metriche di grafo dipendono da soglia, densità, numero di nodi: confrontare reti con densità uguale e modelli nulli.") });
  fig(s, "f19_graph", X0, Y0, 8.0, 3.7, "l", "Graph");
  text(s, [B("Nodes = electrodes or ++regions++; edges = connectivity values (thresholded or weighted).", "Nodi = elettrodi o ++regioni++; archi = valori di connettività (con soglia o pesati)."),
    B("Brain networks are ++small-world++ and ++modular++ with ++hubs++ (Bullmore & Sporns, 2009).", "Le reti cerebrali sono ++small-world++ e ++modulari++ con ++hub++ (Bullmore & Sporns, 2009)."),
    B("⚠ Metrics depend on ++density++ and thresholds: compare with ++null models++.", "⚠ Le metriche dipendono da ++densità++ e soglie: confrontare con ++modelli nulli++."),
    B("MATLAB: Brain Connectivity Toolbox (Rubinov & Sporns, 2010).", "MATLAB: Brain Connectivity Toolbox (Rubinov & Sporns, 2010).")], 8.6, Y0, 4.1, 4.8, { sz: 14, after: 12 });
}

section(4, "In practice", "In pratica");

// 19 MATLAB
{
  const s = content(t("In MATLAB", "In MATLAB"), t("Source imaging and wPLI with FieldTrip", "Sorgenti e wPLI con FieldTrip"),
    { notes: t("FieldTrip (Oostenveld et al., 2011 Comput Intell Neurosci). Template files ship with FieldTrip (standard_bem.mat, standard_1020.elc, cortex_5124.surf.gii). For resting data use a frequency-domain beamformer (DICS) or eLORETA; for connectivity at source level, project single trials with the common filter.", "FieldTrip (Oostenveld et al., 2011 Comput Intell Neurosci). I file template sono inclusi in FieldTrip (standard_bem.mat, standard_1020.elc, cortex_5124.surf.gii). Per dati a riposo usare un beamformer nel dominio delle frequenze (DICS) o eLORETA; per la connettività alle sorgenti proiettare i singoli trial con il filtro comune.") });
  card(s, X0, Y0, CW, 5.1, TINT);
  const code = [
    "load standard_bem;  elec = ft_read_sens('standard_1020.elc');           % template head",
    "cfg = []; cfg.headmodel = vol; cfg.elec = elec;",
    "cfg.sourcemodel = ft_read_headshape('cortex_5124.surf.gii');",
    "lf = ft_prepare_leadfield(cfg, data);                                    % forward",
    "cfg = []; cfg.covariance = 'yes'; cfg.keeptrials = 'yes';",
    "tl  = ft_timelockanalysis(cfg, data);",
    "cfg = []; cfg.method = 'eloreta'; cfg.sourcemodel = lf; cfg.headmodel = vol;",
    "cfg.eloreta.keepfilter = 'yes'; cfg.eloreta.lambda = 0.05;",
    "src = ft_sourceanalysis(cfg, tl);                                        % inverse",
    "cfg = []; cfg.method = 'mtmfft'; cfg.taper = 'dpss'; cfg.tapsmofrq = 2;",
    "cfg.foi = 8:1:13; cfg.output = 'fourier'; cfg.keeptrials = 'yes';",
    "freq = ft_freqanalysis(cfg, data);                                       % sensor or virtual channels",
    "cfg = []; cfg.method = 'wpli_debiased';",
    "conn = ft_connectivityanalysis(cfg, freq);                               % lag-based connectivity",
    "W = squeeze(mean(conn.wpli_debiasedspctrm, 3));                          % channel x channel",
    "C = clustering_coef_wu(abs(W));  % Brain Connectivity Toolbox"];
  text(s, code.map(c => ({ t: c })), X0 + 0.25, Y0 + 0.15, CW - 0.5, 4.8, { raw: true, sz: 12, face: "Consolas", after: 3 });
}

// 20 buone pratiche
{
  const s = content(t("Good practice", "Buona pratica"), t("A checklist for sources and connectivity", "Una checklist per sorgenti e connettività"),
    { notes: t("Michel & Brunet (2019); Bastos & Schoffelen (2016); Pernet et al. (2020) COBIDAS MEEG; Colclough et al. (2016) NeuroImage 138:284 (reliability of connectivity measures); Miljevic et al. (2022) (resting EEG connectivity reproducibility).", "Michel & Brunet (2019); Bastos & Schoffelen (2016); Pernet et al. (2020) COBIDAS MEEG; Colclough et al. (2016) NeuroImage 138:284 (affidabilità delle misure di connettività); Miljevic et al. (2022) (riproducibilità della connettività EEG a riposo).") });
  rows(s, [t("≥ 64 channels, ++full coverage++, digitised positions, good head model.", "≥ 64 canali, ++copertura completa++, posizioni digitalizzate, buon modello di testa."),
    t("Report inverse method, ++regularisation++, source space, noise covariance.", "Riportare metodo inverso, ++regolarizzazione++, spazio delle sorgenti, covarianza del rumore."),
    t("Connectivity: prefer ++source level++ + ++lag-based++ or orthogonalised metrics.", "Connettività: preferire il ++livello delle sorgenti++ + metriche ++basate sul ritardo++ o ortogonalizzate."),
    t("Equalise ++trial numbers++ and ++SNR++ between conditions (bias!).", "Pareggiare ++numero di trial++ e ++SNR++ tra condizioni (bias!)."),
    t("Test against ++surrogates/permutations++; interpret \"where\" at the ++cm++ scale.", "Testare contro ++surrogati/permutazioni++; interpretare il \"dove\" alla scala dei ++cm++.")], X0, Y0, CW, 0.82, 0.14, 16);
}

// 21 domande
{
  const s = content(t("Check your understanding", "Verifica"), t("Three questions", "Tre domande"),
    { notes: t("(1) Null space: infinitely many solutions; priors. (2) Volume conduction/common reference create zero-lag coherence; use imaginary coherence/wPLI at source level. (3) Beamformers suppress correlated sources (they cancel each other).", "(1) Spazio nullo: infinite soluzioni; ipotesi a priori. (2) Conduzione di volume/riferimento comune creano coerenza a ritardo zero; usare coerenza immaginaria/wPLI alle sorgenti. (3) I beamformer sopprimono sorgenti correlate (si cancellano a vicenda).") });
  rows(s, [t("Why can two very different source configurations produce exactly the same scalp map?", "Perché due configurazioni di sorgenti molto diverse possono produrre la stessa identica mappa di scalpo?"),
    t("Fz and FCz show coherence 0.9 in alpha. Is this evidence of communication? What would you compute instead?", "Fz e FCz mostrano coerenza 0,9 in alfa. È prova di comunicazione? Che cosa calcoleresti invece?"),
    t("Two bilateral auditory sources are perfectly synchronous. Why might a beamformer miss them?", "Due sorgenti uditive bilaterali sono perfettamente sincrone. Perché un beamformer potrebbe non vederle?")], X0, Y0 + 0.2, CW, 1.2, 0.35, 17, ACC);
}

// 22 take home
{
  const s = content(t("Take-home messages", "Messaggi chiave"), t("Take-home messages", "Messaggi chiave"));
  rows(s, [t("Forward is ++unique++ (y = L·j); inverse is ++ill-posed++ and needs priors.", "Il diretto è ++unico++ (y = L·j); l'inverso è ++mal posto++ e richiede ipotesi a priori."),
    t("Dipoles for ++focal++ sources; MNE/sLORETA/eLORETA for distributed; beamformers for ++uncorrelated++ sources.", "Dipoli per sorgenti ++focali++; MNE/sLORETA/eLORETA per distribuite; beamformer per sorgenti ++non correlate++."),
    t("Accuracy needs ++electrodes, coverage and head models++.", "L'accuratezza richiede ++elettrodi, copertura e modelli di testa++."),
    t("Sensor-level coherence is ++contaminated by volume conduction++: use lag-based metrics at source level.", "La coerenza ai sensori è ++contaminata dalla conduzione di volume++: usare metriche basate sul ritardo alle sorgenti."),
    t("Granger = ++prediction++, not causation; graphs summarise ++network organisation++.", "Granger = ++predizione++, non causa; i grafi riassumono l'++organizzazione della rete++.")], X0, Y0, CW, 0.85, 0.15, 16);
}

// 23 letture
{
  const s = content(t("Suggested reading", "Letture consigliate"), t("Suggested reading", "Letture consigliate"));
  text(s, [
    { t: "Michel C.M. et al. (2004) EEG source imaging. *Clin Neurophysiol* 115:2195–2222.", b: true },
    { t: "Michel C.M., Brunet D. (2019) EEG source imaging: a practical review of the analysis steps. *Front Neurol* 10:325.", b: true },
    { t: "Hämäläinen M.S., Ilmoniemi R.J. (1994) Interpreting magnetic fields of the brain: minimum norm estimates. *Med Biol Eng Comput* 32:35–42.", b: true },
    { t: "Pascual-Marqui R.D. (2002) Standardized low-resolution brain electromagnetic tomography (sLORETA). *Methods Find Exp Clin Pharmacol* 24D:5–12.", b: true },
    { t: "Van Veen B.D. et al. (1997) Localization of brain electrical activity via linearly constrained minimum variance spatial filtering. *IEEE Trans Biomed Eng* 44:867–880.", b: true },
    { t: "Vorwerk J. et al. (2014) A guideline for head volume conductor modeling in EEG and MEG. *NeuroImage* 100:590–607.", b: true },
    { t: "Nolte G. et al. (2004) Identifying true brain interaction from EEG data using the imaginary part of coherency. *Clin Neurophysiol* 115:2292–2307.", b: true },
    { t: "Vinck M. et al. (2011) An improved index of phase-synchronization for electrophysiological data. *NeuroImage* 55:1548–1565.", b: true },
    { t: "Bastos A.M., Schoffelen J.-M. (2016) A tutorial review of functional connectivity analysis methods. *Front Syst Neurosci* 9:175.", b: true },
    { t: "Seth A.K., Barrett A.B., Barnett L. (2015) Granger causality analysis in neuroscience and neuroimaging. *J Neurosci* 35:3293–3297.", b: true },
    { t: "Bullmore E., Sporns O. (2009) Complex brain networks: graph theoretical analysis. *Nat Rev Neurosci* 10:186–198.", b: true },
    { t: "Oostenveld R. et al. (2011) FieldTrip: open source software for advanced analysis of MEG, EEG and invasive electrophysiological data. *Comput Intell Neurosci* 2011:156869.", b: true }], X0, Y0, CW, 5.2, { sz: 11, after: 4 });
}

save(OUT);
