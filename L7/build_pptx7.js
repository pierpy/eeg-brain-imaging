// EEG – Lecture 7: event-related potentials (bilingue: node build_pptx7.js en|it)
const __R = (function () { const p = require("path"), fs = require("fs"); let d = process.env.COURSE_ROOT || __dirname;
  while (!fs.existsSync(p.join(d, ".course_root")) && p.dirname(d) !== d) d = p.dirname(d); return d; })();
const LANGARG = process.argv[2] || "en";
global.CFG = { lang: LANGARG, fig: __R + "/L7/figpng_" + LANGARG, common: __R + "/common",
  footer: LANGARG === "it" ? "Brain Imaging · EEG · Lezione 7 · Potenziali evento-correlati" : "Brain Imaging · EEG · Lecture 7 · Event-related potentials",
  lezione: LANGARG === "it" ? "Lezione 7" : "Lecture 7",
  titolo: LANGARG === "it" ? "Potenziali evento-correlati:\ndalla media alle componenti" : "Event-related potentials:\nfrom averages to components", titoloSize: 40 };
const L = require(__R + "/common/pptlib_eeg.js");
const { tr: t, pres, fig, content, text, formula, card, badge, copertina, save } = L;
const { INK, ACC, TEAL, TXT, MUTED, TINT, WHITE, SERIF, SANS, W, H, MX, X0, Y0, CW } = L.C;
const OUT = process.argv[3] || `${__R}/L7/out/EEG_L7_${LANGARG}.pptx`;
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
  const s = content(t("Lecture 7", "Lezione 7"), t("Today: the brain's response to an event", "Oggi: la risposta del cervello a un evento"),
    { notes: t("Main references: Luck (2014) An Introduction to the Event-Related Potential Technique; Kappenman & Luck (2012) Oxford Handbook of ERP Components.", "Riferimenti principali: Luck (2014) An Introduction to the Event-Related Potential Technique; Kappenman & Luck (2012) Oxford Handbook of ERP Components.") });
  rows(s, [t("*Averaging*: why it works, what it assumes, how many trials.", "*Media*: perché funziona, cosa assume, quanti trial."),
    t("++Peaks are not components++: the superposition problem.", "++I picchi non sono componenti++: il problema della sovrapposizione."),
    t("The ERP *component zoo*: P1/N1, N170, MMN, P3, N400, ERN, N2pc.", "Lo *zoo delle componenti*: P1/N1, N170, MMN, P3, N400, ERN, N2pc."),
    t("*Measuring* amplitudes and latencies without fooling ourselves.", "*Misurare* ampiezze e latenze senza ingannarsi."),
    t("*Statistics*: mass-univariate, cluster permutation, single-trial models.", "*Statistica*: mass-univariata, permutazioni a cluster, modelli a singolo trial.")], X0, Y0, CW, 0.85, 0.15, 18);
}

// 3 media
{
  const s = content(t("What is an ERP?", "Che cos'è un ERP?"), t("Averaging lifts a small response out of the EEG", "La media fa emergere una piccola risposta dall'EEG"),
    { notes: t("Dawson (1954) first averaged evoked responses; the ERP is typically 1–10 µV, the ongoing EEG 20–50 µV. Averaging N time-locked trials reduces uncorrelated noise by √N.", "Dawson (1954) fu il primo a mediare le risposte evocate; l'ERP è tipicamente 1–10 µV, l'EEG di fondo 20–50 µV. Mediare N trial agganciati nel tempo riduce il rumore non correlato di √N.") });
  fig(s, "f03_averaging", X0, Y0, CW, 3.2, "c", "Averaging");
  text(s, [B("The ERP (≈ 1–10 µV) is buried in the ongoing EEG (≈ 20–50 µV).", "L'ERP (≈ 1–10 µV) è sepolto nell'EEG di fondo (≈ 20–50 µV)."),
    B("Average many trials ++time-locked++ to the event: what is locked stays, the rest cancels.", "Mediare molti trial ++agganciati nel tempo++ all'evento: ciò che è agganciato resta, il resto si annulla."),
    B("ERPs have ++ms resolution++: they tell ++when++ processing differs between conditions.", "Gli ERP hanno ++risoluzione al ms++: dicono ++quando++ l'elaborazione differisce tra condizioni.")], X0, 4.8, CW, 1.5, { sz: 16, after: 8 });
  meta(s, t("a ++long exposure++ at night: moving cars vanish, the street lamp that is always there appears.", "una ++lunga esposizione++ di notte: le auto in movimento spariscono, il lampione sempre presente appare."), X0, 6.25, CW, 0.5, 14);
}

section(1, "From trials to ERPs", "Dai trial agli ERP");

// 5 ipotesi e jitter
{
  const s = content(t("Averaging (1)", "Media (1)"), t("What averaging assumes — and latency jitter", "Che cosa assume la media — e il jitter di latenza"),
    { notes: t("The signal-plus-noise model: x_k(t) = s(t) + n_k(t). If latency varies across trials, the average is the signal convolved with the latency distribution: smaller and broader (Luck, 2014, ch. 8). Remedies: response-locking, Woody filter, single-trial latency estimation (e.g. RIDE: Ouyang et al., 2015).", "Il modello segnale più rumore: x_k(t) = s(t) + n_k(t). Se la latenza varia tra i trial, la media è il segnale convoluto con la distribuzione delle latenze: più piccolo e più largo (Luck, 2014, cap. 8). Rimedi: agganciare alla risposta, filtro di Woody, stima della latenza a singolo trial (es. RIDE: Ouyang et al., 2015).") });
  formula(s, "x_{k}(t) = s(t) + n_{k}(t)", X0, Y0, 5.0, 0.75, { sz: 22, fill: PEACH });
  text(s, [B("Same signal s(t) in every trial.", "Stesso segnale s(t) in ogni trial."),
    B("Noise with ++zero mean++, independent of the event.", "Rumore a ++media nulla++, indipendente dall'evento."),
    B("If latency ++jitters++, the average is ++smaller and wider++ (not the typical single trial).", "Se la latenza ++varia++, la media è ++più piccola e più larga++ (non il trial tipico)."),
    B("Remedies: response-locked averages, Woody filter, single-trial methods.", "Rimedi: medie agganciate alla risposta, filtro di Woody, metodi a singolo trial.")], X0, 2.5, 5.0, 3.9, { sz: 16, after: 12 });
  fig(s, "f05_jitter", 5.9, Y0, 6.8, 4.6, "c", "Latency jitter");
}

// 6 SNR
{
  const s = content(t("Averaging (2)", "Media (2)"), t("How many trials? Noise falls with √N", "Quanti trial? Il rumore cala con √N"),
    { notes: t("Boudewyn et al. (2018) Psychophysiology 55:e13049 — trials needed depend on component and effect size. Luck et al. (2021) Psychophysiology 58:e13793 — standardized measurement error (SME) as a data-quality metric.", "Boudewyn et al. (2018) Psychophysiology 55:e13049 — i trial necessari dipendono da componente ed effetto. Luck et al. (2021) Psychophysiology 58:e13793 — errore di misura standardizzato (SME) come metrica di qualità dei dati.") });
  fig(s, "f06_snr", X0, Y0, 6.4, 4.4, "l", "SNR");
  text(s, [B("Residual noise ∝ 1/√N: to ++halve++ the noise you need ++4×++ the trials.", "Rumore residuo ∝ 1/√N: per ++dimezzare++ il rumore servono ++4×++ i trial."),
    B("Rules of thumb: large components (P3) ≈ 30–40 trials; small ones (N2pc, MMN, ERN) often ++100+++.", "Regole pratiche: componenti grandi (P3) ≈ 30–40 trial; piccole (N2pc, MMN, ERN) spesso ++100+++."),
    B("More participants and more trials trade off (Boudewyn et al., 2018).", "Più partecipanti e più trial si compensano (Boudewyn et al., 2018)."),
    B("Report data quality: the *SME* (standardized measurement error, Luck et al., 2021).", "Riportare la qualità dei dati: lo *SME* (errore di misura standardizzato, Luck et al., 2021).")], 7.3, Y0, 5.4, 4.8, { sz: 16, after: 12 });
}

// 7 componenti
{
  const s = content(t("Averaging (3)", "Media (3)"), t("Peaks are not components", "I picchi non sono componenti"),
    { notes: t("Luck (2005/2014) 'Ten simple rules' — rule 1: peaks and components are not the same thing. The observed waveform is the sum of overlapping latent components with different scalp distributions; a change in one component can move peaks of the sum.", "Luck (2005/2014) 'Ten simple rules' — regola 1: picchi e componenti non sono la stessa cosa. La forma d'onda osservata è la somma di componenti latenti sovrapposte con distribuzioni di scalpo diverse; il cambiamento di una componente può spostare i picchi della somma.") });
  fig(s, "f07_components", X0, Y0, CW, 3.7, "c", "Components");
  text(s, [B("The ERP is a ++sum of latent components++ that overlap in time and space.", "L'ERP è una ++somma di componenti latenti++ sovrapposte nel tempo e nello spazio."),
    B("Only C2 changed — yet the ++peak latency moved++. A latency change of a peak ≠ a slower process.", "È cambiata solo C2 — eppure la ++latenza del picco si è spostata++. Un picco che si sposta ≠ un processo più lento."),
    B("Use ++difference waves++, topographies and converging manipulations to isolate components.", "Usare ++onde differenza++, topografie e manipolazioni convergenti per isolare le componenti.")], X0, 5.35, CW, 1.4, { sz: 15, after: 6 });
}

section(2, "The ERP component zoo", "Lo zoo delle componenti ERP");

// 9 zoo
{
  const s = content(t("Components (1)", "Componenti (1)"), t("A timeline of classic ERP components", "Una linea del tempo delle componenti classiche"),
    { notes: t("Naming: polarity (P/N) + order or latency (P1, N170, P300). Components are defined by polarity, latency, scalp distribution and sensitivity to experimental manipulations (Donchin et al., 1978; Kappenman & Luck, 2012).", "Nomenclatura: polarità (P/N) + ordine o latenza (P1, N170, P300). Le componenti sono definite da polarità, latenza, distribuzione sullo scalpo e sensibilità alle manipolazioni sperimentali (Donchin et al., 1978; Kappenman & Luck, 2012).") });
  fig(s, "f09_zoo", X0, Y0, CW, 3.9, "c", "Component zoo");
  note(s, t("Name = ++polarity++ (P/N) + ++order or latency++. Defined by latency, polarity, ++topography++ and ++what modulates it++.", "Nome = ++polarità++ (P/N) + ++ordine o latenza++. Definita da latenza, polarità, ++topografia++ e ++da cosa è modulata++."), X0, 5.6, CW, 0.9, 16);
}

// 10 componenti sensoriali e percettive
{
  const s = content(t("Components (2)", "Componenti (2)"), t("Early components: sensation, attention, prediction", "Componenti precoci: sensazione, attenzione, predizione"),
    { notes: t("Hillyard et al. (1973) Science 182:177 (N1 and auditory attention); Mangun & Hillyard (1991) (P1/N1 visual spatial attention); Bentin et al. (1996) J Cogn Neurosci 8:551 (N170); Näätänen et al. (1978, 2007) Clin Neurophysiol 118:2544 (MMN).", "Hillyard et al. (1973) Science 182:177 (N1 e attenzione uditiva); Mangun & Hillyard (1991) (P1/N1 e attenzione spaziale visiva); Bentin et al. (1996) J Cogn Neurosci 8:551 (N170); Näätänen et al. (1978, 2007) Clin Neurophysiol 118:2544 (MMN).") });
  cards(s, [["P1 / N1 (80–200 ms)", t("visual/auditory sensory responses; ++larger for attended++ locations (Hillyard et al., 1973; Mangun & Hillyard, 1991).", "risposte sensoriali visive/uditive; ++più grandi per le posizioni attese++ (Hillyard et al., 1973; Mangun & Hillyard, 1991).")],
    ["N170 (≈ 170 ms)", t("occipito-temporal, ++larger for faces++ than objects (Bentin et al., 1996).", "occipito-temporale, ++più grande per i volti++ che per gli oggetti (Bentin et al., 1996).")],
    ["MMN (150–250 ms)", t("fronto-central negativity to a ++deviant++ sound in a regular sequence, even without attention (Näätänen et al., 2007).", "negatività fronto-centrale a un suono ++deviante++ in una sequenza regolare, anche senza attenzione (Näätänen et al., 2007).")]], Y0, 3.0, 15);
  text(s, [B("Early components index ++sensory processing++ and how attention and predictions ++gate++ it.", "Le componenti precoci indicizzano l'++elaborazione sensoriale++ e come attenzione e predizioni la ++regolano++."),
    B("Clinical use: MMN in schizophrenia and disorders of consciousness; auditory brainstem responses in newborn screening.", "Uso clinico: MMN nella schizofrenia e nei disturbi di coscienza; potenziali uditivi del tronco nello screening neonatale.")], X0, 4.8, CW, 1.6, { sz: 16, after: 10 });
}

// 11 P300
{
  const s = content(t("Components (3)", "Componenti (3)"), t("The P3 and the oddball paradigm", "La P3 e il paradigma oddball"),
    { notes: t("Sutton et al. (1965) Science 150:1187; Polich (2007) Clin Neurophysiol 118:2128. P3a (fronto-central, novelty) vs P3b (parietal, task-relevant targets). Amplitude ∝ improbability and relevance; latency ∝ stimulus evaluation time. Basis of the P300 speller BCI (Farwell & Donchin, 1988).", "Sutton et al. (1965) Science 150:1187; Polich (2007) Clin Neurophysiol 118:2128. P3a (fronto-centrale, novità) vs P3b (parietale, target rilevanti). Ampiezza ∝ improbabilità e rilevanza; latenza ∝ tempo di valutazione dello stimolo. Base del P300 speller BCI (Farwell & Donchin, 1988).") });
  fig(s, "f11_oddball", X0, Y0, 7.0, 4.4, "l", "Oddball P3");
  text(s, [B("*Oddball*: rare targets among frequent standards → large ++parietal positivity++ at 300–600 ms.", "*Oddball*: target rari tra standard frequenti → grande ++positività parietale++ a 300–600 ms."),
    B("Amplitude grows with ++improbability++ and ++task relevance++; latency tracks ++evaluation time++.", "L'ampiezza cresce con ++improbabilità++ e ++rilevanza++; la latenza segue il ++tempo di valutazione++."),
    B("*P3a* (novelty, fronto-central) vs *P3b* (targets, parietal) (Polich, 2007).", "*P3a* (novità, fronto-centrale) vs *P3b* (target, parietale) (Polich, 2007)."),
    B("Workhorse of the ++P300 speller++ BCI (Farwell & Donchin, 1988).", "Cavallo di battaglia del ++P300 speller++ (Farwell & Donchin, 1988).")], 7.8, Y0, 4.9, 4.8, { sz: 15, after: 12 });
}

// 12 N400
{
  const s = content(t("Components (4)", "Componenti (4)"), t("Language: N400 and P600", "Linguaggio: N400 e P600"),
    { notes: t("Kutas & Hillyard (1980) Science 207:203; Kutas & Federmeier (2011) Annu Rev Psychol 62:621 (thirty years of N400). P600: Osterhout & Holcomb (1992) — syntactic anomalies and reanalysis.", "Kutas & Hillyard (1980) Science 207:203; Kutas & Federmeier (2011) Annu Rev Psychol 62:621 (trent'anni di N400). P600: Osterhout & Holcomb (1992) — anomalie sintattiche e rianalisi.") });
  fig(s, "f12_n400", X0, Y0, 5.8, 4.8, "l", "N400");
  text(s, [B("*N400*: centro-parietal negativity ≈ 250–500 ms, ++larger for unexpected words++ (Kutas & Hillyard, 1980).", "*N400*: negatività centro-parietale ≈ 250–500 ms, ++più grande per parole inattese++ (Kutas & Hillyard, 1980)."),
    B("Graded by ++cloze probability++: it indexes access to meaning and prediction, not just \"errors\".", "Graduata dalla ++probabilità cloze++: indica accesso al significato e predizione, non solo \"errori\"."),
    B("*P600*: late positivity to ++syntactic++ violations and reanalysis (Osterhout & Holcomb, 1992).", "*P600*: positività tardiva a violazioni ++sintattiche++ e rianalisi (Osterhout & Holcomb, 1992)."),
    B("Not only language: pictures, gestures, arithmetic facts.", "Non solo linguaggio: immagini, gesti, fatti aritmetici.")], 6.7, Y0, 6.0, 4.8, { sz: 16, after: 12 });
}

// 13 motorie ed errore
{
  const s = content(t("Components (5)", "Componenti (5)"), t("Preparing and monitoring actions", "Preparare e monitorare le azioni"),
    { notes: t("Walter et al. (1964) Nature 203:380 (CNV); Kornhuber & Deecke (1965) (Bereitschaftspotential); Coles (1989) (LRP); Falkenstein et al. (1991), Gehring et al. (1993) Psychol Sci 4:385 (ERN/Ne); Pe: Overbeek et al. (2005).", "Walter et al. (1964) Nature 203:380 (CNV); Kornhuber & Deecke (1965) (Bereitschaftspotential); Coles (1989) (LRP); Falkenstein et al. (1991), Gehring et al. (1993) Psychol Sci 4:385 (ERN/Ne); Pe: Overbeek et al. (2005).") });
  cards(s, [["CNV", t("slow negativity between a warning and an imperative stimulus: ++anticipation++ (Walter et al., 1964).", "negatività lenta tra un segnale di avviso e lo stimolo imperativo: ++anticipazione++ (Walter et al., 1964).")],
    [t("Readiness potential / LRP", "Potenziale di prontezza / LRP"), t("builds up before voluntary movements; the ++lateralized++ part (C3/C4) shows ++which hand++ is prepared.", "cresce prima dei movimenti volontari; la parte ++lateralizzata++ (C3/C4) mostra ++quale mano++ si prepara.")],
    ["ERN / Pe", t("fronto-central negativity ≈ 50–100 ms ++after an error++, then a positivity (Pe) linked to error awareness (Gehring et al., 1993).", "negatività fronto-centrale ≈ 50–100 ms ++dopo un errore++, poi una positività (Pe) legata alla consapevolezza dell'errore (Gehring et al., 1993).")]], Y0, 3.2, 15);
  note(s, t("Response-locked averages: time zero = ++button press++, not stimulus onset.", "Medie agganciate alla risposta: tempo zero = ++pressione del tasto++, non l'onset dello stimolo."), X0, 5.0, CW, 0.8, 16);
}

// 14 N2pc
{
  const s = content(t("Components (6)", "Componenti (6)"), t("N2pc: tracking spatial attention with a subtraction", "N2pc: seguire l'attenzione spaziale con una sottrazione"),
    { notes: t("Luck & Hillyard (1994) Psychophysiology 31:291; Eimer (1996) Electroencephalogr Clin Neurophysiol 99:225. Contralateral minus ipsilateral at posterior sites (PO7/PO8) cancels everything that is not lateralised with respect to the attended item.", "Luck & Hillyard (1994) Psychophysiology 31:291; Eimer (1996) Electroencephalogr Clin Neurophysiol 99:225. Controlaterale meno ipsilaterale ai siti posteriori (PO7/PO8) cancella tutto ciò che non è lateralizzato rispetto all'oggetto atteso.") });
  fig(s, "f14_n2pc", X0, Y0, 7.8, 4.4, "l", "N2pc");
  text(s, [B("Target on the left: posterior electrodes on the ++right++ (contralateral) become more negative at ≈ 200–300 ms.", "Target a sinistra: gli elettrodi posteriori a ++destra++ (controlaterali) diventano più negativi a ≈ 200–300 ms."),
    B("*Contra − ipsi* removes everything non-lateralised: a clean marker of ++attentional selection++.", "*Contro − ipsi* rimuove tutto ciò che non è lateralizzato: un marcatore pulito della ++selezione attentiva++."),
    B("Same logic: LRP (hands), CDA (visual working memory).", "Stessa logica: LRP (mani), CDA (memoria di lavoro visiva).")], 8.5, Y0, 4.2, 4.8, { sz: 15, after: 12 });
}

section(3, "Measuring ERPs", "Misurare gli ERP");

// 16 misure
{
  const s = content(t("Measurement (1)", "Misura (1)"), t("Amplitude and latency measures", "Misure di ampiezza e latenza"),
    { notes: t("Luck (2014) ch. 9; Clayson, Baldwin & Larson (2013) Psychophysiology 50:174 (peak vs mean amplitude); Kiesel et al. (2008) Psychophysiology 45:250 (latency measures, jackknifing).", "Luck (2014) cap. 9; Clayson, Baldwin & Larson (2013) Psychophysiology 50:174 (picco vs ampiezza media); Kiesel et al. (2008) Psychophysiology 45:250 (misure di latenza, jackknife).") });
  fig(s, "f16_measures", X0, Y0, 6.8, 4.5, "l", "Measures");
  text(s, [B("*Mean amplitude* in a window: robust to noise, ++not biased++ by the number of trials — preferred.", "*Ampiezza media* in una finestra: robusta al rumore, ++non distorta++ dal numero di trial — preferita."),
    B("*Peak amplitude*: sensitive to noise; ++biased++ upward with fewer trials.", "*Ampiezza di picco*: sensibile al rumore; ++distorta++ verso l'alto con meno trial."),
    B("*Latency*: fractional-area (50 %) or fractional-peak latency, with ++jackknifing++ for group comparisons (Kiesel et al., 2008).", "*Latenza*: latenza a frazione d'area (50 %) o di picco, con ++jackknife++ per i confronti di gruppo (Kiesel et al., 2008).")], 7.6, Y0, 5.1, 4.8, { sz: 15, after: 12 });
}

// 17 onde differenza
{
  const s = content(t("Measurement (2)", "Misura (2)"), t("Difference waves, topographies — and circularity", "Onde differenza, topografie — e circolarità"),
    { notes: t("Luck & Gaspelin (2017) Psychophysiology 54:146 'How to get statistically significant effects in any ERP experiment (and why you shouldn't)'. Kriegeskorte et al. (2009) Nat Neurosci 12:535 on double dipping. Use a priori windows, collapsed localisers or mass-univariate tests.", "Luck & Gaspelin (2017) Psychophysiology 54:146 'How to get statistically significant effects in any ERP experiment (and why you shouldn't)'. Kriegeskorte et al. (2009) Nat Neurosci 12:535 sul double dipping. Usare finestre a priori, localizzatori collassati o test mass-univariati.") });
  fig(s, "f17_diffwave", X0, Y0, CW, 3.3, "c", "Difference waves");
  rows(s, [t("*Difference wave* (B − A) isolates what the manipulation changes; its ++topography++ helps identify the component.", "L'*onda differenza* (B − A) isola ciò che la manipolazione cambia; la sua ++topografia++ aiuta a identificare la componente."),
    t("⚠ Choosing the window/electrodes ++after looking at the effect++ inflates false positives (double dipping).", "⚠ Scegliere finestra/elettrodi ++dopo aver visto l'effetto++ gonfia i falsi positivi (double dipping)."),
    t("Use ++a priori++ windows, a ++collapsed localiser++ (average of conditions), or mass-univariate tests (Luck & Gaspelin, 2017).", "Usare finestre ++a priori++, un ++localizzatore collassato++ (media delle condizioni) o test mass-univariati (Luck & Gaspelin, 2017).")], X0, 4.75, CW, 0.62, 0.1, 14, ACC);
}

section(4, "Statistics for ERPs", "Statistica per gli ERP");

// 19 cluster
{
  const s = content(t("Statistics (1)", "Statistica (1)"), t("Mass-univariate tests and cluster-based permutation", "Test mass-univariati e permutazioni a cluster"),
    { notes: t("Maris & Oostenveld (2007) J Neurosci Methods 164:177; Groppe, Urbach & Kutas (2011) Psychophysiology 48:1711 (tutorial). The cluster test controls the family-wise error at the level of the whole data space but does not localise effects precisely in time or space (Sassenhagen & Draschkow, 2019 Psychophysiology 56:e13335).", "Maris & Oostenveld (2007) J Neurosci Methods 164:177; Groppe, Urbach & Kutas (2011) Psychophysiology 48:1711 (tutorial). Il test a cluster controlla l'errore familywise sull'intero spazio dei dati ma non localizza con precisione gli effetti nel tempo o nello spazio (Sassenhagen & Draschkow, 2019 Psychophysiology 56:e13335).") });
  fig(s, "f20_cluster", X0, Y0, CW, 2.75, "c", "Cluster permutation");
  rows(s, [t("Test ++every++ time point × channel → thousands of tests → multiple-comparison problem.", "Testare ++ogni++ punto tempo × canale → migliaia di test → problema dei confronti multipli."),
    t("*Cluster permutation*: group adjacent supra-threshold points, sum their t (cluster mass), compare with the ++max-cluster++ distribution from shuffled labels.", "*Permutazioni a cluster*: raggruppare punti adiacenti sopra soglia, sommarne i t (massa), confrontare con la distribuzione del ++cluster massimo++ ottenuta mescolando le etichette."),
    t("⚠ It says ++there is an effect++, not exactly ++where/when++ it starts (Sassenhagen & Draschkow, 2019).", "⚠ Dice che ++c'è un effetto++, non esattamente ++dove/quando++ inizia (Sassenhagen & Draschkow, 2019).")], X0, 4.6, CW, 0.64, 0.1, 14, ACC);
}

// 20 modelli
{
  const s = content(t("Statistics (2)", "Statistica (2)"), t("Beyond averages: single-trial and regression models", "Oltre le medie: modelli a singolo trial e di regressione"),
    { notes: t("LIMO EEG: Pernet et al. (2011) Comput Intell Neurosci; linear mixed models: Frömer, Maier & Abdel Rahman (2018) Front Neurosci 12:48; regression ERPs: Smith & Kutas (2015) Psychophysiology 52:157; deconvolution of overlapping responses: Ehinger & Dimigen (2019) PeerJ 7:e7838 (Unfold toolbox).", "LIMO EEG: Pernet et al. (2011) Comput Intell Neurosci; modelli lineari misti: Frömer, Maier & Abdel Rahman (2018) Front Neurosci 12:48; ERP di regressione: Smith & Kutas (2015) Psychophysiology 52:157; deconvoluzione delle risposte sovrapposte: Ehinger & Dimigen (2019) PeerJ 7:e7838 (toolbox Unfold).") });
  cards(s, [[t("Hierarchical GLM (LIMO)", "GLM gerarchico (LIMO)"), t("fit single trials per subject, then test betas across subjects (Pernet et al., 2011).", "modellare i singoli trial per soggetto, poi testare i beta tra soggetti (Pernet et al., 2011).")],
    [t("Mixed models", "Modelli misti"), t("subjects and items as ++random effects++; continuous predictors (Frömer et al., 2018).", "soggetti e item come ++effetti casuali++; predittori continui (Frömer et al., 2018).")],
    [t("Regression ERPs (rERP)", "ERP di regressione (rERP)"), t("the ERP as a ++regression coefficient++ over time (Smith & Kutas, 2015).", "l'ERP come ++coefficiente di regressione++ nel tempo (Smith & Kutas, 2015).")],
    [t("Deconvolution", "Deconvoluzione"), t("separate ++overlapping++ responses (stimulus, saccade, button) with fast event rates (Unfold: Ehinger & Dimigen, 2019).", "separare risposte ++sovrapposte++ (stimolo, saccade, tasto) con eventi rapidi (Unfold: Ehinger & Dimigen, 2019).")]], Y0, 2.9, 14);
  note(s, t("Averages hide ++trial-by-trial variability++: models use it — and use all the data.", "Le medie nascondono la ++variabilità trial per trial++: i modelli la sfruttano — e usano tutti i dati."), X0, 4.8, CW, 0.8, 16);
}

section(5, "ERPs in practice", "ERP in pratica");

// 22 MATLAB
{
  const s = content(t("In MATLAB", "In MATLAB"), t("ERPs, difference waves and a permutation test", "ERP, onde differenza e un test di permutazione"),
    { notes: t("Plain MATLAB on EEGLAB epoched datasets (one per condition). For group-level cluster tests use FieldTrip ft_timelockstatistics (cfg.method = 'montecarlo', cfg.correctm = 'cluster') or ERPLAB/LIMO.", "MATLAB di base su dataset EEGLAB a epoche (uno per condizione). Per i test a cluster di gruppo usare ft_timelockstatistics di FieldTrip (cfg.method = 'montecarlo', cfg.correctm = 'cluster') o ERPLAB/LIMO.") });
  card(s, X0, Y0, CW, 5.1, TINT);
  const code = [
    "A = pop_loadset('sub-01_std.set');  B = pop_loadset('sub-01_dev.set');",
    "ch = find(strcmpi({A.chanlocs.labels}, 'Pz'));  t = A.times;          % ms",
    "erpA = mean(A.data(ch,:,:), 3);  erpB = mean(B.data(ch,:,:), 3);    % averages",
    "dw   = erpB - erpA;                                                  % difference wave",
    "win  = t >= 300 & t <= 500;                                          % a priori window",
    "mA = squeeze(mean(A.data(ch,win,:), 2));  mB = squeeze(mean(B.data(ch,win,:), 2));",
    "obs = mean(mB) - mean(mA);                                           % mean-amplitude effect",
    "all = [mA; mB];  nA = numel(mA);  nPerm = 5000;  null = zeros(nPerm,1);",
    "for p = 1:nPerm",
    "    idx = randperm(numel(all));",
    "    null(p) = mean(all(idx(nA+1:end))) - mean(all(idx(1:nA)));",
    "end",
    "pval = (sum(abs(null) >= abs(obs)) + 1) / (nPerm + 1);",
    "plot(t, erpA, t, erpB, t, dw, 'k', 'LineWidth', 2); set(gca,'YDir','normal');",
    "xlabel('time (ms)'); ylabel('\\muV'); legend('standard','deviant','difference');"];
  text(s, code.map(c => ({ t: c })), X0 + 0.25, Y0 + 0.15, CW - 0.5, 4.8, { raw: true, sz: 12, face: "Consolas", after: 3 });
}

// 23 buone pratiche
{
  const s = content(t("Good practice", "Buona pratica"), t("Reporting ERP studies", "Documentare uno studio ERP"),
    { notes: t("Keil et al. (2014) Psychophysiology 51:1–21; Keil et al. (2022) update; Luck (2014) ch. 13; Pernet et al. (2020) COBIDAS MEEG.", "Keil et al. (2014) Psychophysiology 51:1–21; aggiornamento Keil et al. (2022); Luck (2014) cap. 13; Pernet et al. (2020) COBIDAS MEEG.") });
  rows(s, [t("Trials per condition ++after rejection++; data quality (SME).", "Trial per condizione ++dopo il rigetto++; qualità dei dati (SME)."),
    t("Reference, filters (type, cut-off, order), baseline window.", "Riferimento, filtri (tipo, taglio, ordine), finestra di baseline."),
    t("Measurement windows and electrodes ++justified a priori++.", "Finestre di misura ed elettrodi ++motivati a priori++."),
    t("Show ++waveforms and topographies++, not only bar plots.", "Mostrare ++forme d'onda e topografie++, non solo istogrammi."),
    t("Share data (BIDS) and code; pre-register when possible.", "Condividere dati (BIDS) e codice; pre-registrare quando possibile.")], X0, Y0, CW, 0.82, 0.14, 17);
}

// 24 domande
{
  const s = content(t("Check your understanding", "Verifica"), t("Three questions", "Tre domande"),
    { notes: t("(1) 4× trials (√4 = 2). (2) Latency jitter reduces and smears the average; use response-locked or single-trial methods. (3) Circular analysis: windows chosen on the effect inflate false positives.", "(1) 4× i trial (√4 = 2). (2) Il jitter di latenza riduce e allarga la media; usare medie agganciate alla risposta o metodi a singolo trial. (3) Analisi circolare: finestre scelte sull'effetto gonfiano i falsi positivi.") });
  rows(s, [t("With 40 trials the residual noise is 2 µV. How many trials to reach 1 µV?", "Con 40 trial il rumore residuo è 2 µV. Quanti trial servono per 1 µV?"),
    t("Patients show a smaller, wider P3 than controls. Give an explanation that is not \"less P3\".", "I pazienti mostrano una P3 più piccola e larga dei controlli. Dai una spiegazione diversa da \"meno P3\"."),
    t("You pick the 50-ms window where conditions differ most, then test it. What is wrong?", "Scegli la finestra di 50 ms dove le condizioni differiscono di più, poi la testi. Che cosa non va?")], X0, Y0 + 0.2, CW, 1.2, 0.35, 18, ACC);
}

// 25 messaggi chiave
{
  const s = content(t("Take-home messages", "Messaggi chiave"), t("Take-home messages", "Messaggi chiave"));
  rows(s, [t("Averaging: noise ∝ ++1/√N++; assumes a constant, time-locked signal.", "Media: rumore ∝ ++1/√N++; presuppone un segnale costante e agganciato nel tempo."),
    t("++Peaks ≠ components++: use difference waves and topographies.", "++Picchi ≠ componenti++: usare onde differenza e topografie."),
    t("Components (P1/N1, N170, MMN, P3, N400, ERN, N2pc) index ++specific processes++.", "Le componenti (P1/N1, N170, MMN, P3, N400, ERN, N2pc) indicano ++processi specifici++."),
    t("Prefer ++mean amplitude++ and fractional-area latency; windows ++a priori++.", "Preferire l'++ampiezza media++ e la latenza a frazione d'area; finestre ++a priori++."),
    t("Correct for multiple comparisons (++cluster permutation++) or model single trials.", "Correggere i confronti multipli (++permutazioni a cluster++) o modellare i singoli trial.")], X0, Y0, CW, 0.85, 0.15, 17);
}

// 26 letture
{
  const s = content(t("Suggested reading", "Letture consigliate"), t("Suggested reading", "Letture consigliate"));
  text(s, [
    { t: "Luck S.J. (2014) *An Introduction to the Event-Related Potential Technique*, 2nd ed. MIT Press.", b: true },
    { t: "Kappenman E.S., Luck S.J. (eds) (2012) *The Oxford Handbook of Event-Related Potential Components*. OUP.", b: true },
    { t: "Sutton S. et al. (1965) Evoked-potential correlates of stimulus uncertainty. *Science* 150:1187–1188.", b: true },
    { t: "Polich J. (2007) Updating P300: an integrative theory of P3a and P3b. *Clin Neurophysiol* 118:2128–2148.", b: true },
    { t: "Kutas M., Federmeier K.D. (2011) Thirty years and counting: finding meaning in the N400. *Annu Rev Psychol* 62:621–647.", b: true },
    { t: "Näätänen R. et al. (2007) The mismatch negativity (MMN) in basic research of central auditory processing. *Clin Neurophysiol* 118:2544–2590.", b: true },
    { t: "Luck S.J., Hillyard S.A. (1994) Electrophysiological correlates of feature analysis during visual search. *Psychophysiology* 31:291–308.", b: true },
    { t: "Gehring W.J. et al. (1993) A neural system for error detection and compensation. *Psychol Sci* 4:385–390.", b: true },
    { t: "Luck S.J., Gaspelin N. (2017) How to get statistically significant effects in any ERP experiment (and why you shouldn't). *Psychophysiology* 54:146–157.", b: true },
    { t: "Groppe D.M., Urbach T.P., Kutas M. (2011) Mass univariate analysis of event-related brain potentials/fields I. *Psychophysiology* 48:1711–1725.", b: true },
    { t: "Maris E., Oostenveld R. (2007) Nonparametric statistical testing of EEG- and MEG-data. *J Neurosci Methods* 164:177–190.", b: true },
    { t: "Luck S.J. et al. (2021) Standardized measurement error: a universal metric of data quality for averaged ERPs. *Psychophysiology* 58:e13793.", b: true }], X0, Y0, CW, 5.2, { sz: 12, after: 5 });
}

save(OUT);
