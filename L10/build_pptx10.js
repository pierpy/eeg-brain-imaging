// EEG – Lecture 10: decoding and applications (bilingue: node build_pptx10.js en|it)
const __R = (function () { const p = require("path"), fs = require("fs"); let d = process.env.COURSE_ROOT || __dirname;
  while (!fs.existsSync(p.join(d, ".course_root")) && p.dirname(d) !== d) d = p.dirname(d); return d; })();
const LANGARG = process.argv[2] || "en";
global.CFG = { lang: LANGARG, fig: __R + "/L10/figpng_" + LANGARG, common: __R + "/common",
  footer: LANGARG === "it" ? "Brain Imaging · EEG · Lezione 10 · Decoding e applicazioni" : "Brain Imaging · EEG · Lecture 10 · Decoding and applications",
  lezione: LANGARG === "it" ? "Lezione 10" : "Lecture 10",
  titolo: LANGARG === "it" ? "Leggere la mente?\nDecoding e applicazioni" : "Reading the mind?\nDecoding and applications", titoloSize: 42 };
const L = require(__R + "/common/pptlib_eeg.js");
const { tr: t, pres, fig, content, text, formula, card, badge, copertina, save } = L;
const { INK, ACC, TEAL, TXT, MUTED, TINT, WHITE, SERIF, SANS, W, H, MX, X0, Y0, CW } = L.C;
const OUT = process.argv[3] || `${__R}/L10/out/EEG_L10_${LANGARG}.pptx`;
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
  const s = content(t("Lecture 10", "Lezione 10"), t("Today: from brain signals to predictions", "Oggi: dai segnali cerebrali alle predizioni"),
    { notes: t("Main references: Grootswagers, Wardle & Carlson (2017) J Cogn Neurosci 29:677 (decoding dynamic brain patterns from EEG/MEG); King & Dehaene (2014) Trends Cogn Sci 18:203; Haufe et al. (2014) NeuroImage 87:96; Wolpaw & Wolpaw (2012) Brain–Computer Interfaces.", "Riferimenti principali: Grootswagers, Wardle & Carlson (2017) J Cogn Neurosci 29:677 (decoding di pattern dinamici da EEG/MEG); King & Dehaene (2014) Trends Cogn Sci 18:203; Haufe et al. (2014) NeuroImage 87:96; Wolpaw & Wolpaw (2012) Brain–Computer Interfaces.") });
  rows(s, [t("*Encoding vs decoding*: two directions of inference.", "*Encoding vs decoding*: due direzioni di inferenza."),
    t("*MVPA*: linear classifiers, cross-validation, overfitting, metrics.", "*MVPA*: classificatori lineari, cross-validation, overfitting, metriche."),
    t("Interpreting classifiers: ++weights vs patterns++ (Haufe et al., 2014).", "Interpretare i classificatori: ++pesi vs pattern++ (Haufe et al., 2014)."),
    t("*Time-resolved decoding* and ++temporal generalisation++.", "*Decoding risolto nel tempo* e ++generalizzazione temporale++."),
    t("*Applications*: BCI, clinical EEG, EEG–fMRI; course wrap-up.", "*Applicazioni*: BCI, EEG clinico, EEG–fMRI; sintesi del corso.")], X0, Y0, CW, 0.85, 0.15, 18);
}

// 3 encoding decoding
{
  const s = content(t("Two directions", "Due direzioni"), t("Encoding and decoding", "Encoding e decoding"),
    { notes: t("Naselaris et al. (2011) NeuroImage 56:400 (encoding and decoding in fMRI); Haynes & Rees (2006) Nat Rev Neurosci 7:523. ERPs/GLMs are encoding models: they predict the signal from conditions. MVPA decodes conditions from multichannel patterns: more sensitive to distributed effects, no need to choose channels a priori.", "Naselaris et al. (2011) NeuroImage 56:400 (encoding e decoding in fMRI); Haynes & Rees (2006) Nat Rev Neurosci 7:523. ERP/GLM sono modelli di encoding: predicono il segnale dalle condizioni. L'MVPA decodifica le condizioni dai pattern multicanale: più sensibile a effetti distribuiti, senza scegliere i canali a priori.") });
  fig(s, "f03_encdec", X0 + 0.3, Y0, CW - 0.6, 2.3, "c", "Encoding decoding");
  rows(s, [t("*Univariate* (ERP): one channel at a time → multiple comparisons, choice of electrodes.", "*Univariata* (ERP): un canale alla volta → confronti multipli, scelta degli elettrodi."),
    t("*Multivariate* (MVPA): uses the ++whole pattern++; detects distributed, weak, individual-specific effects.", "*Multivariata* (MVPA): usa l'++intero pattern++; rileva effetti distribuiti, deboli, specifici dell'individuo."),
    t("Question changes: from \"where/when is the effect?\" to \"++is information present++?\"", "Cambia la domanda: da \"dove/quando è l'effetto?\" a \"++l'informazione è presente++?\"")], X0, 4.1, CW, 0.6, 0.08, 16);
  meta(s, t("a ++sommelier++ does not measure one molecule: the pattern of many tells the wine.", "un ++sommelier++ non misura una molecola: il pattern di molte rivela il vino."), X0, 6.3, CW, 0.5, 14);
}

section(1, "Multivariate pattern analysis", "Analisi multivariata dei pattern");

// 5 LDA
{
  const s = content(t("MVPA (1)", "MVPA (1)"), t("A linear classifier", "Un classificatore lineare"),
    { notes: t("LDA with shrinkage (Ledoit–Wolf) is a strong default for EEG (Blankertz et al., 2011 NeuroImage 56:814; Grootswagers et al., 2017). SVM and logistic regression give similar results. Features: amplitudes of all channels at a time point (or a short window).", "L'LDA con shrinkage (Ledoit–Wolf) è un ottimo default per l'EEG (Blankertz et al., 2011 NeuroImage 56:814; Grootswagers et al., 2017). SVM e regressione logistica danno risultati simili. Feature: ampiezze di tutti i canali in un istante (o in una breve finestra).") });
  fig(s, "f05_lda", X0, Y0, 7.6, 3.6, "l", "LDA");
  formula(s, "w = Σ^{−1} (μ_{1} − μ_{0})      ŷ = sign(wᵀx + b)", X0, 5.2, 7.6, 0.75, { sz: 19, fill: PEACH });
  text(s, [B("Each trial = a ++point in channel space++ (x = amplitudes at time t).", "Ogni trial = un ++punto nello spazio dei canali++ (x = ampiezze all'istante t)."),
    B("A linear classifier finds a ++hyperplane++ separating the classes.", "Un classificatore lineare trova un ++iperpiano++ che separa le classi."),
    B("*LDA with shrinkage* (regularised covariance) is a robust default for EEG (Blankertz et al., 2011).", "*LDA con shrinkage* (covarianza regolarizzata) è un default robusto per l'EEG (Blankertz et al., 2011)."),
    B("Also: SVM, logistic regression — similar performance.", "Anche: SVM, regressione logistica — prestazioni simili.")], 8.3, Y0, 4.4, 4.8, { sz: 15, after: 12 });
}

// 6 CV
{
  const s = content(t("MVPA (2)", "MVPA (2)"), t("Training, testing, cross-validation", "Addestramento, test, cross-validation"),
    { notes: t("Never test on training data. k-fold CV (k = 5–10), stratified; preprocessing steps fitted on the data (e.g., PCA, scaling, ICA selection based on labels) must be done inside the folds to avoid leakage (Varoquaux et al., 2017 NeuroImage 145:166 — cross-validation failure: small sample sizes lead to large error bars).", "Mai testare sui dati di addestramento. CV k-fold (k = 5–10), stratificata; i passi di pre-elaborazione stimati sui dati (es. PCA, normalizzazione, selezione basata sulle etichette) vanno fatti dentro i fold per evitare leakage (Varoquaux et al., 2017 NeuroImage 145:166 — con campioni piccoli le barre d'errore sono grandi).") });
  fig(s, "f06_cv", X0 + 0.5, Y0, CW - 1.0, 2.6, "c", "Cross-validation");
  rows(s, [t("Test data must be ++never seen++ during training.", "I dati di test non devono ++mai essere visti++ durante l'addestramento."),
    t("*k-fold*: split into k parts, train on k−1, test on the left-out, rotate, average.", "*k-fold*: dividere in k parti, addestrare su k−1, testare sulla esclusa, ruotare, mediare."),
    t("⚠ *Leakage*: any step using labels or all data (feature selection, normalisation) ++inside the folds++.", "⚠ *Leakage*: ogni passo che usa etichette o tutti i dati (selezione di feature, normalizzazione) ++dentro i fold++."),
    t("Small samples → ++large error bars++ (Varoquaux et al., 2017).", "Campioni piccoli → ++barre d'errore ampie++ (Varoquaux et al., 2017).")], X0, 4.1, CW, 0.62, 0.1, 15, ACC);
}

// 7 overfitting
{
  const s = content(t("MVPA (3)", "MVPA (3)"), t("Overfitting and the curse of dimensionality", "Overfitting e maledizione della dimensionalità"),
    { notes: t("With 64 channels × 100 time points = 6400 features and 100 trials, any classifier can fit noise perfectly. Remedies: regularisation (shrinkage, L2), fewer features (time-resolved decoding, averaging windows, PCA), more trials, pseudo-trials (averaging small groups of trials; Grootswagers et al., 2017).", "Con 64 canali × 100 campioni = 6400 feature e 100 trial, qualunque classificatore può adattarsi perfettamente al rumore. Rimedi: regolarizzazione (shrinkage, L2), meno feature (decoding nel tempo, finestre mediate, PCA), più trial, pseudo-trial (media di piccoli gruppi di trial; Grootswagers et al., 2017).") });
  fig(s, "f07_overfit", X0, Y0, 6.2, 4.4, "l", "Overfitting");
  text(s, [B("Many features, few trials → the model ++memorises noise++: training accuracy ≈ 100 %, test ≈ chance.", "Molte feature, pochi trial → il modello ++memorizza il rumore++: accuratezza di addestramento ≈ 100 %, test ≈ caso."),
    B("Remedies: ++regularisation++, fewer features (per time point), ++more trials++, ++pseudo-trials++.", "Rimedi: ++regolarizzazione++, meno feature (per istante), ++più trial++, ++pseudo-trial++."),
    B("Only ++cross-validated++ accuracy counts.", "Conta solo l'accuratezza ++in cross-validation++.")], 7.0, Y0, 5.7, 4.6, { sz: 16, after: 12 });
  meta(s, t("a student who ++memorises the answers++ of last year's exam fails a new one.", "uno studente che ++memorizza le risposte++ dell'esame dell'anno scorso fallisce quello nuovo."), X0, 6.2, CW, 0.55, 15);
}

section(2, "Evaluating and interpreting", "Valutare e interpretare");

// 9 metriche
{
  const s = content(t("Evaluation (1)", "Valutazione (1)"), t("Performance metrics and chance level", "Metriche di prestazione e livello del caso"),
    { notes: t("Balanced accuracy for unbalanced classes; d' = z(hit) − z(FA); AUC is threshold-free. Chance is not exactly 50 % with few trials: test significance by label permutation (Combrisson & Jerbi, 2015 J Neurosci Methods 250:126) and at group level by t-tests against chance or prevalence inference (Allefeld et al., 2016).", "Accuratezza bilanciata per classi sbilanciate; d' = z(hit) − z(FA); l'AUC non dipende dalla soglia. Il caso non è esattamente 50 % con pochi trial: testare la significatività con permutazione delle etichette (Combrisson & Jerbi, 2015 J Neurosci Methods 250:126) e a livello di gruppo con t-test contro il caso o inferenza di prevalenza (Allefeld et al., 2016).") });
  fig(s, "f09_metrics", X0, Y0, 8.0, 3.8, "l", "Metrics");
  text(s, [B("*Confusion matrix* → accuracy; ++balanced accuracy++ if classes are unbalanced.", "*Matrice di confusione* → accuratezza; ++accuratezza bilanciata++ se le classi sono sbilanciate."),
    B("*d′* and *AUC*: threshold-free sensitivity (signal detection theory).", "*d′* e *AUC*: sensibilità indipendente dalla soglia (teoria della detezione del segnale)."),
    B("⚠ Chance ≠ 50 % with few trials: use ++label permutation++ (Combrisson & Jerbi, 2015).", "⚠ Il caso ≠ 50 % con pochi trial: usare la ++permutazione delle etichette++ (Combrisson & Jerbi, 2015).")], 8.6, Y0, 4.1, 4.8, { sz: 15, after: 12 });
}

// 10 Haufe
{
  const s = content(t("Evaluation (2)", "Valutazione (2)"), t("Weights are not patterns", "I pesi non sono pattern"),
    { notes: t("Haufe et al. (2014) NeuroImage 87:96. A backward model's weights W combine signal and noise suppression: a channel with large weight may carry no signal (it cancels noise). The forward-model activation pattern A = Σ_x W Σ_ŝ⁻¹ is interpretable as the spatial pattern of the signal of interest.", "Haufe et al. (2014) NeuroImage 87:96. I pesi W di un modello all'indietro combinano segnale e soppressione del rumore: un canale con peso grande può non contenere segnale (cancella il rumore). Il pattern di attivazione A = Σ_x W Σ_ŝ⁻¹ del modello diretto è interpretabile come distribuzione spaziale del segnale d'interesse.") });
  fig(s, "f10_haufe", X0, Y0, CW, 2.8, "c", "Haufe");
  formula(s, "A = Σ_{x} · W · Σ_{ŝ}^{−1}", X0 + 4.0, 4.6, CW - 8.0, 0.7, { sz: 22, fill: PEACH });
  text(s, [B("Weights (*backward model*) also ++cancel noise++: a large weight can sit on a channel ++without signal++.", "I pesi (*modello all'indietro*) ++cancellano anche il rumore++: un peso grande può stare su un canale ++senza segnale++."),
    B("Transform them into *activation patterns* (forward model) before interpreting topographies (Haufe et al., 2014).", "Trasformarli in *pattern di attivazione* (modello diretto) prima di interpretare le topografie (Haufe et al., 2014).")], X0, 5.35, CW, 1.3, { sz: 16, after: 6 });
}

// 11 decoding nel tempo
{
  const s = content(t("Time-resolved decoding (1)", "Decoding nel tempo (1)"), t("When does the brain know?", "Quando il cervello \"sa\"?"),
    { notes: t("Train and test a classifier independently at each time point (Grootswagers et al., 2017). Above-chance clusters are tested with cluster-based permutation across subjects. The onset of decodability indicates when information becomes available — but beware filter-induced smearing (Van Driel et al., 2021 J Neurosci Methods).", "Addestrare e testare un classificatore separatamente a ogni istante (Grootswagers et al., 2017). I cluster sopra il caso si testano con permutazioni a cluster tra soggetti. L'onset della decodificabilità indica quando l'informazione diventa disponibile — attenzione allo spostamento indotto dai filtri (Van Driel et al., 2021 J Neurosci Methods).") });
  fig(s, "f11_timedec", X0, Y0, 6.8, 4.2, "l", "Time-resolved decoding");
  text(s, [B("Repeat the classification ++at every time point++ (features = channels).", "Ripetere la classificazione ++a ogni istante++ (feature = canali)."),
    B("The accuracy curve shows ++when++ information is present, with ms resolution.", "La curva di accuratezza mostra ++quando++ l'informazione è presente, con risoluzione al ms."),
    B("Group statistics: accuracy vs chance with ++cluster-based permutation++.", "Statistica di gruppo: accuratezza vs caso con ++permutazioni a cluster++."),
    B("⚠ High-pass filters can ++shift++ the apparent onset (Van Driel et al., 2021).", "⚠ I filtri passa-alto possono ++spostare++ l'onset apparente (Van Driel et al., 2021).")], 7.6, Y0, 5.1, 4.8, { sz: 15, after: 12 });
}

// 12 generalizzazione temporale
{
  const s = content(t("Time-resolved decoding (2)", "Decoding nel tempo (2)"), t("Temporal generalisation", "Generalizzazione temporale"),
    { notes: t("King & Dehaene (2014) Trends Cogn Sci 18:203 — train at t, test at t'. A diagonal pattern indicates a chain of transient codes; a square indicates a sustained code; off-diagonal below-chance indicates reversal. Example with N2pc/visual search: Fahrenfort et al. (2017) J Cogn Neurosci.", "King & Dehaene (2014) Trends Cogn Sci 18:203 — addestrare a t, testare a t'. Una diagonale indica una catena di codici transitori; un quadrato un codice sostenuto; valori sotto il caso fuori diagonale indicano inversione. Esempio con N2pc/ricerca visiva: Fahrenfort et al. (2017) J Cogn Neurosci.") });
  fig(s, "f12_tgm", X0, Y0, 8.2, 3.8, "l", "Temporal generalisation");
  text(s, [B("Train at time t, ++test at every t′++ → a time × time matrix (King & Dehaene, 2014).", "Addestrare all'istante t, ++testare a ogni t′++ → una matrice tempo × tempo (King & Dehaene, 2014)."),
    B("++Diagonal++ = a chain of transient codes; ++square++ = a sustained code.", "++Diagonale++ = catena di codici transitori; ++quadrato++ = codice sostenuto."),
    B("Our simulation: an early transient (~200 ms) and a sustained late code (350–600 ms).", "Nella simulazione: un codice precoce transitorio (~200 ms) e uno tardivo sostenuto (350–600 ms).")], 8.8, Y0, 3.9, 4.8, { sz: 14, after: 12 });
}

section(3, "Applications", "Applicazioni");

// 14 BCI
{
  const s = content(t("Applications (1)", "Applicazioni (1)"), t("Brain–computer interfaces", "Interfacce cervello–computer"),
    { notes: t("Wolpaw et al. (2002) Clin Neurophysiol 113:767; Lotte et al. (2018) J Neural Eng 15:031005 (review of classification algorithms). Paradigms: P300 speller (Farwell & Donchin, 1988), SSVEP, motor imagery (mu/beta ERD; Pfurtscheller & Neuper, 2001). Applications: communication in ALS/locked-in, neurorehabilitation after stroke (Ang et al., 2015), neurofeedback.", "Wolpaw et al. (2002) Clin Neurophysiol 113:767; Lotte et al. (2018) J Neural Eng 15:031005 (review sugli algoritmi di classificazione). Paradigmi: P300 speller (Farwell & Donchin, 1988), SSVEP, immaginazione motoria (ERD mu/beta; Pfurtscheller & Neuper, 2001). Applicazioni: comunicazione nella SLA/locked-in, neuroriabilitazione dopo ictus (Ang et al., 2015), neurofeedback.") });
  fig(s, "f15_bci", X0, Y0, CW, 2.1, "c", "BCI loop");
  cards(s, [["P300 speller", t("rare flashes of the attended row/column evoke a ++P3++ (Farwell & Donchin, 1988).", "i lampi rari della riga/colonna attesa evocano una ++P3++ (Farwell & Donchin, 1988).")],
    ["SSVEP", t("targets flicker at ++different frequencies++; the attended one dominates the spectrum.", "i target lampeggiano a ++frequenze diverse++; quello atteso domina lo spettro.")],
    [t("Motor imagery", "Immaginazione motoria"), t("imagining a hand movement → contralateral ++mu/beta ERD++ (Pfurtscheller & Neuper, 2001).", "immaginare un movimento della mano → ++ERD mu/beta++ controlaterale (Pfurtscheller & Neuper, 2001).")],
    [t("Uses", "Usi"), t("communication in ++ALS/locked-in++, stroke ++rehabilitation++, neurofeedback.", "comunicazione in ++SLA/locked-in++, ++riabilitazione++ dopo ictus, neurofeedback.")]], 4.0, 2.4, 13);
}

// 15 paradigmi
{
  const s = content(t("Applications (2)", "Applicazioni (2)"), t("P300 speller and SSVEP", "P300 speller e SSVEP"),
    { notes: t("Information transfer rate (bits/min) combines accuracy, number of classes and speed (Wolpaw et al., 2002). SSVEP detection with canonical correlation analysis (Lin et al., 2006 IEEE TBME). Dry-electrode and wearable systems enable out-of-lab use but with lower SNR.", "Il tasso di trasferimento d'informazione (bit/min) combina accuratezza, numero di classi e velocità (Wolpaw et al., 2002). Rilevamento SSVEP con analisi delle correlazioni canoniche (Lin et al., 2006 IEEE TBME). Sistemi a secco e indossabili permettono l'uso fuori dal laboratorio ma con SNR minore.") });
  fig(s, "f16_paradigms", X0, Y0, CW, 3.0, "c", "BCI paradigms");
  rows(s, [t("*P300*: classify target vs non-target ERPs (LDA); average several repetitions for reliability.", "*P300*: classificare ERP target vs non target (LDA); mediare più ripetizioni per affidabilità."),
    t("*SSVEP*: detect the flicker frequency and its ++harmonics++ (e.g. CCA); fast, little training.", "*SSVEP*: rilevare la frequenza di lampeggio e le ++armoniche++ (es. CCA); veloce, poco addestramento."),
    t("Performance: ++information transfer rate++ (bits/min) = accuracy × classes × speed.", "Prestazioni: ++tasso di trasferimento d'informazione++ (bit/min) = accuratezza × classi × velocità.")], X0, 4.85, CW, 0.6, 0.1, 15, ACC);
}

// 16 clinica
{
  const s = content(t("Applications (3)", "Applicazioni (3)"), t("Clinical EEG", "EEG clinico"),
    { notes: t("Epilepsy: interictal epileptiform discharges, seizure detection, presurgical ESI (Mégevand & Seeck, 2018; Brodbeck et al., 2011 Brain 134:2887). Sleep: AASM scoring. Disorders of consciousness: EEG markers and covert command following (Claassen et al., 2019 NEJM 380:2497). Anaesthesia depth monitoring. Dementia: slowing of rhythms. Brain death: electrocerebral silence.", "Epilessia: scariche epilettiformi intercritiche, rilevamento delle crisi, ESI prechirurgico (Mégevand & Seeck, 2018; Brodbeck et al., 2011 Brain 134:2887). Sonno: stadiazione AASM. Disturbi di coscienza: marcatori EEG e risposta nascosta ai comandi (Claassen et al., 2019 NEJM 380:2497). Monitoraggio della profondità dell'anestesia. Demenza: rallentamento dei ritmi. Morte cerebrale: silenzio elettrocerebrale.") });
  cards(s, [[t("Epilepsy", "Epilessia"), t("spikes, seizures, ++presurgical source imaging++ (Brodbeck et al., 2011).", "spike, crisi, ++source imaging prechirurgico++ (Brodbeck et al., 2011).")],
    [t("Sleep", "Sonno"), t("stages, apnoea, ++automatic scoring++ with machine learning.", "stadi, apnee, ++stadiazione automatica++ con machine learning.")],
    [t("Consciousness", "Coscienza"), t("coma and disorders of consciousness: ++covert command following++ detected by decoding (Claassen et al., 2019).", "coma e disturbi di coscienza: ++risposta nascosta ai comandi++ rilevata con il decoding (Claassen et al., 2019).")],
    [t("Anaesthesia & dementia", "Anestesia e demenza"), t("depth-of-anaesthesia monitors; ++slowing++ of rhythms in dementia.", "monitor della profondità dell'anestesia; ++rallentamento++ dei ritmi nella demenza.")]], Y0, 3.2, 14);
  note(s, t("EEG is ++cheap, portable, bedside++ and millisecond-precise: ideal for monitoring and screening.", "L'EEG è ++economico, portatile, al letto del paziente++ e preciso al ms: ideale per monitoraggio e screening."), X0, 5.0, CW, 0.8, 16);
}

// 17 EEG-fMRI
{
  const s = content(t("Applications (4)", "Applicazioni (4)"), t("Multimodal imaging: EEG–fMRI", "Imaging multimodale: EEG–fMRI"),
    { notes: t("Goldman et al. (2002) NeuroReport 13:2487 and Laufs et al. (2003) PNAS 100:11053: alpha power anticorrelated with occipital/parietal BOLD. Artifacts in the scanner: gradient (template subtraction, Allen et al., 2000) and ballistocardiogram (Allen et al., 1998). Integration approaches: EEG-informed fMRI, fMRI-informed source imaging, symmetric fusion (Huster et al., 2012 J Neurosci 32:6053). Microstate–BOLD: Lecture 8.", "Goldman et al. (2002) NeuroReport 13:2487 e Laufs et al. (2003) PNAS 100:11053: potenza alfa anticorrelata con il BOLD occipitale/parietale. Artefatti nello scanner: gradiente (sottrazione del template, Allen et al., 2000) e balistocardiogramma (Allen et al., 1998). Approcci di integrazione: fMRI informata dall'EEG, source imaging informato dall'fMRI, fusione simmetrica (Huster et al., 2012 J Neurosci 32:6053). Microstati–BOLD: Lezione 8.") });
  fig(s, "f18_eegfmri", X0, Y0, 7.6, 3.2, "l", "EEG-fMRI");
  text(s, [B("EEG = ++when++ (ms); fMRI = ++where++ (mm): complementary.", "EEG = ++quando++ (ms); fMRI = ++dove++ (mm): complementari."),
    B("*EEG-informed fMRI*: EEG features ⊗ HRF as GLM regressors (e.g. alpha ↔ ++negative++ occipital BOLD; Goldman et al., 2002; Laufs et al., 2003).", "*fMRI informata dall'EEG*: feature EEG ⊗ HRF come regressori GLM (es. alfa ↔ BOLD occipitale ++negativo++; Goldman et al., 2002; Laufs et al., 2003)."),
    B("Challenges: ++gradient++ and ++ballistocardiogram++ artifacts (Allen et al., 1998, 2000).", "Sfide: artefatti di ++gradiente++ e ++balistocardiogramma++ (Allen et al., 1998, 2000).")], 8.2, Y0, 4.5, 4.8, { sz: 14, after: 12 });
  note(s, t("Also: EEG + TMS (causal probing), EEG + eye tracking, EEG + fNIRS.", "Inoltre: EEG + TMS (sondaggio causale), EEG + eye tracking, EEG + fNIRS."), X0, 4.95, 7.6, 0.7, 15);
}

section(4, "In practice and wrap-up", "In pratica e sintesi");

// 19 MATLAB
{
  const s = content(t("In MATLAB", "In MATLAB"), t("Time-resolved decoding with cross-validation", "Decoding nel tempo con cross-validation"),
    { notes: t("Plain MATLAB (Statistics and Machine Learning Toolbox: fitcdiscr, cvpartition). Alternatives: MVPA-Light (Treder, 2020 Front Neurosci 14:289), CoSMoMVPA (Oosterhof et al., 2016), ADAM toolbox (Fahrenfort et al., 2018). Remember: equal trial numbers per class, shrinkage, permutation test for chance.", "MATLAB di base (Statistics and Machine Learning Toolbox: fitcdiscr, cvpartition). Alternative: MVPA-Light (Treder, 2020 Front Neurosci 14:289), CoSMoMVPA (Oosterhof et al., 2016), ADAM toolbox (Fahrenfort et al., 2018). Ricordare: stesso numero di trial per classe, shrinkage, test di permutazione per il caso.") });
  card(s, X0, Y0, CW, 5.1, TINT);
  const code = [
    "X = cat(3, A.data, B.data);  X = permute(X, [3 1 2]);        % trials x channels x time",
    "y = [zeros(size(A.data,3),1); ones(size(B.data,3),1)];",
    "cv = cvpartition(y, 'KFold', 5);  nT = size(X,3);  acc = zeros(1,nT);",
    "for t = 1:nT",
    "    Xt = X(:,:,t);  c = 0;",
    "    for k = 1:cv.NumTestSets",
    "        tr = training(cv,k);  te = test(cv,k);",
    "        mdl = fitcdiscr(Xt(tr,:), y(tr), 'DiscrimType','linear', 'Gamma',0.2);  % shrinkage LDA",
    "        c = c + sum(predict(mdl, Xt(te,:)) == y(te));",
    "    end",
    "    acc(t) = c / numel(y);",
    "end",
    "w = mdl.Coeffs(1,2).Linear;                                   % weights (last time point)",
    "Apat = cov(Xt) * w;                                           % activation pattern (Haufe 2014)",
    "plot(A.times, acc); yline(0.5, '--'); xlabel('time (ms)'); ylabel('accuracy');",
    "% chance: repeat with y(randperm(numel(y))) 1000 times -> null distribution"];
  text(s, code.map(c => ({ t: c })), X0 + 0.25, Y0 + 0.15, CW - 0.5, 4.8, { raw: true, sz: 12, face: "Consolas", after: 3 });
}

// 20 etica
{
  const s = content(t("Ethics", "Etica"), t("Neural data are personal data", "I dati neurali sono dati personali"),
    { notes: t("Ienca & Andorno (2017) Life Sci Soc Policy 13:5 (towards new human rights: cognitive liberty, mental privacy); Yuste et al. (2017) Nature 551:159 (four ethical priorities for neurotechnologies and AI); GDPR: EEG is health/biometric data. Consumer EEG devices and data sharing.", "Ienca & Andorno (2017) Life Sci Soc Policy 13:5 (nuovi diritti umani: libertà cognitiva, privacy mentale); Yuste et al. (2017) Nature 551:159 (quattro priorità etiche per neurotecnologie e IA); GDPR: l'EEG è un dato sanitario/biometrico. Dispositivi EEG consumer e condivisione dei dati.") });
  rows(s, [t("Decoding reads ++information++, not \"thoughts\": accuracy is limited and task-specific.", "Il decoding legge ++informazione++, non \"pensieri\": l'accuratezza è limitata e specifica del compito."),
    t("EEG is ++health/biometric data++ (GDPR): consent, anonymisation, secure sharing.", "L'EEG è un ++dato sanitario/biometrico++ (GDPR): consenso, anonimizzazione, condivisione sicura."),
    t("Consumer neurotech raises questions of ++mental privacy++ and ++cognitive liberty++ (Ienca & Andorno, 2017; Yuste et al., 2017).", "La neurotecnologia consumer pone questioni di ++privacy mentale++ e ++libertà cognitiva++ (Ienca & Andorno, 2017; Yuste et al., 2017)."),
    t("Report limits honestly: avoid ++hype++ in communication.", "Riportare onestamente i limiti: evitare l'++hype++ nella comunicazione.")], X0, Y0, CW, 0.9, 0.15, 16);
}

// 21 sintesi del corso
{
  const s = content(t("Course wrap-up", "Sintesi del corso"), t("Ten lectures in one slide", "Dieci lezioni in una slide"),
    { notes: t("A map of the course to review for the exam.", "Una mappa del corso da ripassare per l'esame.") });
  const L_ = [[t("1 · History & what EEG measures", "1 · Storia e cosa misura l'EEG"), t("6 · Spectra & time-frequency", "6 · Spettri e tempo-frequenza")],
    [t("2 · Cellular bases", "2 · Basi cellulari"), t("7 · ERPs", "7 · ERP")],
    [t("3 · From neurons to scalp", "3 · Dai neuroni allo scalpo"), t("8 · Spatial analysis & microstates", "8 · Analisi spaziale e microstati")],
    [t("4 · Recording", "4 · Registrazione"), t("9 · Sources & connectivity", "9 · Sorgenti e connettività")],
    [t("5 · Preprocessing & ICA", "5 · Pre-elaborazione e ICA"), t("10 · Decoding & applications", "10 · Decoding e applicazioni")]];
  L_.forEach(([a, b], i) => {
    const y = Y0 + i * 0.78;
    card(s, X0, y, CW / 2 - 0.1, 0.7, TINT); text(s, [{ t: "~" + a + "~" }], X0 + 0.2, y, CW / 2 - 0.4, 0.7, { sz: 16, valign: "middle" });
    card(s, X0 + CW / 2 + 0.1, y, CW / 2 - 0.1, 0.7, PEACH); text(s, [{ t: "*" + b + "*" }], X0 + CW / 2 + 0.3, y, CW / 2 - 0.4, 0.7, { sz: 16, valign: "middle" });
  });
  note(s, t("~Physics~ → ~recording~ → ~cleaning~ → ~time, frequency, space~ → ~sources and networks~ → ~prediction~.", "~Fisica~ → ~registrazione~ → ~pulizia~ → ~tempo, frequenza, spazio~ → ~sorgenti e reti~ → ~predizione~."), X0, 5.75, CW, 0.65, 16);
}

// 22 domande
{
  const s = content(t("Check your understanding", "Verifica"), t("Three questions", "Tre domande"),
    { notes: t("(1) Overfitting/leakage: features selected on all data; accuracy must be cross-validated with selection inside folds. (2) Weights ≠ patterns: compute A = Σ_x w. (3) Diagonal → transient chain; square → sustained representation.", "(1) Overfitting/leakage: feature selezionate su tutti i dati; l'accuratezza va stimata in CV con la selezione dentro i fold. (2) Pesi ≠ pattern: calcolare A = Σ_x w. (3) Diagonale → catena transitoria; quadrato → rappresentazione sostenuta.") });
  rows(s, [t("You select the 10 most discriminative channels on all data, then cross-validate: 95 %. What went wrong?", "Selezioni i 10 canali più discriminanti su tutti i dati, poi fai la cross-validation: 95 %. Che cosa non va?"),
    t("Your classifier has a large weight at Fp1. Does Fp1 carry the effect?", "Il tuo classificatore ha un peso grande in Fp1. Fp1 contiene l'effetto?"),
    t("The temporal generalisation matrix is a thin diagonal. What does it mean?", "La matrice di generalizzazione temporale è una sottile diagonale. Che cosa significa?")], X0, Y0 + 0.2, CW, 1.2, 0.35, 17, ACC);
}

// 23 messaggi chiave
{
  const s = content(t("Take-home messages", "Messaggi chiave"), t("Take-home messages", "Messaggi chiave"));
  rows(s, [t("Decoding asks \"++is the information there, and when?++\" using whole patterns.", "Il decoding chiede \"++l'informazione c'è, e quando?++\" usando pattern interi."),
    t("++Cross-validate++, regularise, avoid ++leakage++; test chance by permutation.", "++Cross-validation++, regolarizzazione, niente ++leakage++; testare il caso con permutazioni."),
    t("Interpret ++patterns++, not weights (Haufe et al., 2014).", "Interpretare i ++pattern++, non i pesi (Haufe et al., 2014)."),
    t("Temporal generalisation reveals the ++dynamics of codes++.", "La generalizzazione temporale rivela la ++dinamica dei codici++."),
    t("EEG powers ++BCIs, clinical monitoring, multimodal imaging++ — with ethical care.", "L'EEG alimenta ++BCI, monitoraggio clinico, imaging multimodale++ — con attenzione etica.")], X0, Y0, CW, 0.85, 0.15, 17);
}

// 24 letture
{
  const s = content(t("Suggested reading", "Letture consigliate"), t("Suggested reading", "Letture consigliate"));
  text(s, [
    { t: "Grootswagers T., Wardle S.G., Carlson T.A. (2017) Decoding dynamic brain patterns from evoked responses: a tutorial on MVPA applied to time series neuroimaging data. *J Cogn Neurosci* 29:677–697.", b: true },
    { t: "King J.-R., Dehaene S. (2014) Characterizing the dynamics of mental representations: the temporal generalization method. *Trends Cogn Sci* 18:203–210.", b: true },
    { t: "Haufe S. et al. (2014) On the interpretation of weight vectors of linear models in multivariate neuroimaging. *NeuroImage* 87:96–110.", b: true },
    { t: "Blankertz B. et al. (2011) Single-trial analysis and classification of ERP components — a tutorial. *NeuroImage* 56:814–825.", b: true },
    { t: "Varoquaux G. et al. (2017) Assessing and tuning brain decoders: cross-validation, caveats, and guidelines. *NeuroImage* 145:166–179.", b: true },
    { t: "Combrisson E., Jerbi K. (2015) Exceeding chance level by chance. *J Neurosci Methods* 250:126–136.", b: true },
    { t: "Wolpaw J.R. et al. (2002) Brain–computer interfaces for communication and control. *Clin Neurophysiol* 113:767–791.", b: true },
    { t: "Lotte F. et al. (2018) A review of classification algorithms for EEG-based brain–computer interfaces: a 10 year update. *J Neural Eng* 15:031005.", b: true },
    { t: "Laufs H. et al. (2003) EEG-correlated fMRI of human alpha activity. *NeuroImage* 19:1463–1476.", b: true },
    { t: "Claassen J. et al. (2019) Detection of brain activation in unresponsive patients with acute brain injury. *N Engl J Med* 380:2497–2505.", b: true },
    { t: "Treder M.S. (2020) MVPA-Light: a classification and regression toolbox for multi-dimensional data. *Front Neurosci* 14:289.", b: true },
    { t: "Yuste R. et al. (2017) Four ethical priorities for neurotechnologies and AI. *Nature* 551:159–163.", b: true }], X0, Y0, CW, 5.2, { sz: 11, after: 4 });
}

save(OUT);
