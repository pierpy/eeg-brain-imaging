// EEG – Lecture 5: preprocessing and ICA (bilingue: node build_pptx5.js en|it)
const __R = (function () { const p = require("path"), fs = require("fs"); let d = process.env.COURSE_ROOT || __dirname;
  while (!fs.existsSync(p.join(d, ".course_root")) && p.dirname(d) !== d) d = p.dirname(d); return d; })();
const LANGARG = process.argv[2] || "en";
global.CFG = { lang: LANGARG, fig: __R + "/L5/figpng_" + LANGARG, common: __R + "/common",
  footer: LANGARG === "it" ? "Brain Imaging · EEG · Lezione 5 · Pre-elaborazione e ICA" : "Brain Imaging · EEG · Lecture 5 · Preprocessing and ICA",
  lezione: LANGARG === "it" ? "Lezione 5" : "Lecture 5",
  titolo: LANGARG === "it" ? "Pre-elaborazione e ICA:\ndal segnale grezzo ai dati puliti" : "Preprocessing and ICA:\nfrom raw signal to clean data", titoloSize: 40 };
const L = require(__R + "/common/pptlib_eeg.js");
const { tr: t, pres, fig, content, text, formula, card, badge, copertina, save } = L;
const { INK, ACC, TEAL, TXT, MUTED, TINT, WHITE, SERIF, SANS, W, H, MX, X0, Y0, CW } = L.C;
const OUT = process.argv[3] || `${__R}/L5/out/EEG_L5_${LANGARG}.pptx`;
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
  const s = content(t("Lecture 5", "Lezione 5"), t("Today: turning raw EEG into analysable data", "Oggi: trasformare l'EEG grezzo in dati analizzabili"),
    { notes: t("Preprocessing choices change results: document every step (Keil et al., 2014; Pernet et al., 2020 COBIDAS-MEEG).", "Le scelte di pre-elaborazione cambiano i risultati: documentare ogni passo (Keil et al., 2014; Pernet et al., 2020 COBIDAS-MEEG).") });
  rows(s, [t("A ++standard pipeline++ and why the order matters.", "Una ++pipeline standard++ e perché l'ordine conta."),
    t("*Filtering* and resampling without distorting the signal.", "*Filtraggio* e ricampionamento senza distorcere il segnale."),
    t("*Bad channels*, interpolation and ++re-referencing++.", "*Canali cattivi*, interpolazione e ++ri-referenziazione++."),
    t("*Epoching*, baseline correction and ++artifact rejection++.", "*Epoche*, correzione della baseline e ++rigetto degli artefatti++."),
    t("*Independent Component Analysis*: theory, practice, ICLabel.", "*Analisi delle componenti indipendenti*: teoria, pratica, ICLabel.")], X0, Y0, CW, 0.85, 0.15, 18);
}

// 3 pipeline
{
  const s = content(t("The pipeline", "La pipeline"), t("Seven steps from raw file to clean epochs", "Sette passi dal file grezzo alle epoche pulite"),
    { notes: t("There is no single correct pipeline; what matters is that it is justified, reproducible and reported. Robbins et al. (2020) and Delorme (2023) show that simple pipelines are often as good as complex ones.", "Non esiste un'unica pipeline corretta: conta che sia motivata, riproducibile e documentata. Robbins et al. (2020) e Delorme (2023) mostrano che pipeline semplici spesso valgono quanto quelle complesse.") });
  fig(s, "f03_pipeline", X0, Y0 + 0.2, CW, 1.6, "c", "Preprocessing pipeline");
  text(s, [B("Order matters: ++filter before epoching++ (edge effects), ++remove bad channels before average reference++, ++ICA before baseline++.", "L'ordine conta: ++filtrare prima di epocare++ (effetti di bordo), ++togliere i canali cattivi prima del riferimento medio++, ++ICA prima della baseline++."),
    B("Every step is a ++choice++ with consequences: report parameters and software versions.", "Ogni passo è una ++scelta++ con conseguenze: riportare parametri e versioni del software."),
    B("Look at the data ~before, during and after~ each step (plots, spectra, topographies).", "Guardare i dati ~prima, durante e dopo~ ogni passo (tracciati, spettri, topografie)."),
    B("\"EEG is better left alone\": minimal pipelines are often enough (Delorme, 2023).", "\"L'EEG è meglio lasciarlo in pace\": pipeline minime spesso bastano (Delorme, 2023).")], X0, 3.6, CW, 2.5, { sz: 17, after: 10 });
  meta(s, t("cooking: ++wash and cut++ the vegetables before cooking — but peel too much and nothing is left.", "la cucina: ++lavare e tagliare++ le verdure prima di cuocerle — ma sbucciando troppo non resta nulla."), X0, 6.2, CW, 0.55, 15);
}

section(1, "Filtering and resampling", "Filtraggio e ricampionamento");

// 5 filtri
{
  const s = content(t("Filtering (1)", "Filtraggio (1)"), t("Causal or zero-phase? FIR or IIR?", "Causale o a fase zero? FIR o IIR?"),
    { notes: t("Widmann, Schröger & Maess (2015) J Neurosci Methods 250:34. A one-pass causal filter delays the signal; a two-pass (forward-backward) filter has zero phase but is acausal: effects can leak before stimulus onset. For ERP latency studies prefer zero-phase or linear-phase FIR with delay correction; for onset latencies consider causal filters (VanRullen, 2011; Rousselet, 2012).", "Widmann, Schröger & Maess (2015) J Neurosci Methods 250:34. Un filtro causale a un passaggio ritarda il segnale; uno a due passaggi (avanti-indietro) ha fase zero ma è acausale: gli effetti possono «anticipare» l'onset. Per le latenze ERP preferire fase zero o FIR a fase lineare con correzione del ritardo; per le latenze d'onset considerare filtri causali (VanRullen, 2011; Rousselet, 2012).") });
  fig(s, "f05_causal", X0, Y0, 6.4, 3.2, "l", "Causal vs zero-phase");
  text(s, [B("*Causal* (one pass): output depends only on the past → ++delays++ peaks.", "*Causale* (un passaggio): l'uscita dipende solo dal passato → ++ritarda++ i picchi."),
    B("*Zero-phase* (forward + backward, filtfilt): no delay, but ++acausal++: small effects can appear ++before++ onset.", "*Fase zero* (avanti + indietro, filtfilt): nessun ritardo, ma ++acausale++: piccoli effetti possono apparire ++prima++ dell'onset."),
    B("*FIR*: always stable, linear phase; *IIR*: steep with low order, but nonlinear phase.", "*FIR*: sempre stabili, fase lineare; *IIR*: ripidi con ordine basso, ma fase non lineare."),
    B("Typical: HP ++0.1 Hz++ for ERPs (≤ 0.1 Hz for slow components), ++1 Hz++ for ICA, LP 30–40 Hz.", "Tipico: HP ++0,1 Hz++ per ERP (≤ 0,1 Hz per componenti lente), ++1 Hz++ per ICA, LP 30–40 Hz.")], 7.2, Y0, 5.5, 4.6, { sz: 15, after: 10 });
  note(s, t("Filter the ++continuous++ data, not the epochs: edges produce artifacts. ~Report type, order, cut-off, transition band.~", "Filtrare i dati ++continui++, non le epoche: i bordi creano artefatti. ~Riportare tipo, ordine, taglio, banda di transizione.~"), X0, 4.8, 6.4, 1.3, 15);
  meta(s, t("a zero-phase filter is like ++editing a film afterwards++: nothing is late, but you can \"see the future\".", "un filtro a fase zero è come ++montare un film a posteriori++: niente è in ritardo, ma si può \"vedere il futuro\"."), X0, 6.25, CW, 0.5, 14);
}

// 6 ricampionamento e rete
{
  const s = content(t("Filtering (2)", "Filtraggio (2)"), t("Resampling and line-noise removal", "Ricampionamento e rimozione della rete"),
    { notes: t("Downsampling functions (MATLAB resample, EEGLAB pop_resample) apply an anti-aliasing low-pass automatically. Zapline: de Cheveigné (2020) NeuroImage 207:116356; Zapline-plus: Klug & Kloosterman (2022) Hum Brain Mapp.", "Le funzioni di sottocampionamento (resample di MATLAB, pop_resample di EEGLAB) applicano automaticamente un passa-basso anti-aliasing. Zapline: de Cheveigné (2020) NeuroImage 207:116356; Zapline-plus: Klug & Kloosterman (2022) Hum Brain Mapp.") });
  cards(s, [[t("Downsampling", "Sottocampionamento"), t("1000 → 250 Hz saves memory and time. Always ++low-pass first++ (resample does it); never just take every 4th sample.", "1000 → 250 Hz fa risparmiare memoria e tempo. Sempre ++passa-basso prima++ (resample lo fa); mai prendere semplicemente un campione ogni 4.")],
    [t("Notch filter", "Filtro notch"), t("Simple but ++rings++ in time and removes brain activity at 50 Hz: avoid if you study gamma.", "Semplice ma ++oscilla++ nel tempo e toglie attività cerebrale a 50 Hz: evitarlo se si studia la gamma.")],
    [t("Spatial methods", "Metodi spaziali"), t("++CleanLine++ (regression of sinusoids), ++Zapline(-plus)++ (spatial filter): remove the line with minimal distortion.", "++CleanLine++ (regressione di sinusoidi), ++Zapline(-plus)++ (filtro spaziale): tolgono la rete con distorsione minima.")]], Y0, 3.0, 16);
  text(s, [B("Resample ++after++ high-pass filtering at the high rate? Order is flexible, but keep f_{s} > 2.5 × LP cut-off.", "Ricampionare ++dopo++ il passa-alto all'alta frequenza? L'ordine è flessibile, ma mantenere f_{s} > 2,5 × taglio del passa-basso."),
    B("Check the ++spectrum++ before and after: a good step removes the peak, not the neighbours.", "Controllare lo ++spettro++ prima e dopo: un buon passo toglie il picco, non i vicini.")], X0, 4.8, CW, 1.5, { sz: 17, after: 10 });
}

section(2, "Bad channels and re-referencing", "Canali cattivi e ri-referenziazione");

// 8 canali cattivi
{
  const s = content(t("Bad channels (1)", "Canali cattivi (1)"), t("Finding bad channels", "Trovare i canali cattivi"),
    { notes: t("PREP pipeline: Bigdely-Shamlo et al. (2015) Front Neuroinform 9:16 (deviation, correlation, predictability via RANSAC, high-frequency noise). EEGLAB clean_rawdata: flat-line, channel correlation (default 0.8), line-noise criteria.", "Pipeline PREP: Bigdely-Shamlo et al. (2015) Front Neuroinform 9:16 (deviazione, correlazione, predicibilità via RANSAC, rumore ad alta frequenza). clean_rawdata di EEGLAB: linea piatta, correlazione tra canali (default 0,8), criterio del rumore di rete.") });
  fig(s, "f08_badch", X0, Y0, 6.8, 4.4, "l", "Bad channels");
  text(s, [B("*Flat*: disconnected electrode (variance ≈ 0).", "*Piatto*: elettrodo scollegato (varianza ≈ 0)."),
    B("*Noisy*: high-frequency noise, extreme variance (robust z > 3–5).", "*Rumoroso*: rumore ad alta frequenza, varianza estrema (z robusto > 3–5)."),
    B("*Drifting / uncorrelated*: poor contact; low correlation with neighbours (r < 0.8) or poorly predicted by them (++RANSAC++).", "*In deriva / scorrelato*: cattivo contatto; bassa correlazione con i vicini (r < 0,8) o mal predetto da essi (++RANSAC++)."),
    B("Automatic detection (PREP, clean\\_rawdata) + ~visual inspection~.", "Rilevamento automatico (PREP, clean\\_rawdata) + ~ispezione visiva~."),
    B("Rule of thumb: > 10–15 % bad channels → question the recording.", "Regola pratica: > 10–15 % di canali cattivi → mettere in dubbio la registrazione.")], 7.6, Y0, 5.1, 4.8, { sz: 15, after: 10 });
  meta(s, t("an ++orchestra++: one detuned violin is easier to mute than to ignore.", "un'++orchestra++: un violino stonato è più facile da zittire che da ignorare."), X0, 6.2, CW, 0.55, 15);
}

// 9 interpolazione
{
  const s = content(t("Bad channels (2)", "Canali cattivi (2)"), t("Interpolation with spherical splines", "Interpolazione con spline sferiche"),
    { notes: t("Perrin et al. (1989) Electroencephalogr Clin Neurophysiol 72:184. Interpolated channels add no information: they reduce the data rank by one each. Interpolate before average reference so that every region contributes.", "Perrin et al. (1989) Electroencephalogr Clin Neurophysiol 72:184. I canali interpolati non aggiungono informazione: riducono il rango dei dati di uno ciascuno. Interpolare prima del riferimento medio perché ogni regione contribuisca.") });
  fig(s, "f09_interp", X0 + 0.5, Y0, 6.0, 3.3, "c", "Interpolation");
  text(s, [B("The missing channel is estimated from its neighbours using the ++smooth field++ on the scalp (Perrin et al., 1989).", "Il canale mancante si stima dai vicini sfruttando il ++campo liscio++ sullo scalpo (Perrin et al., 1989)."),
    B("Works if bad channels are ++few and scattered++; clusters of bad channels cannot be recovered.", "Funziona se i canali cattivi sono ++pochi e sparsi++; gruppi di canali cattivi non si recuperano."),
    B("⚠ Interpolation adds ++no new information++: the data ++rank++ decreases.", "⚠ L'interpolazione ++non aggiunge informazione++: il ++rango++ dei dati diminuisce.")], 7.2, Y0, 5.5, 4.2, { sz: 16, after: 12 });
  formula(s, "V_{C4} ≈ Σ_{j} w_{j} · V_{j}     (w from spherical splines)", X0, 5.3, 6.6, 0.75, { sz: 18, fill: PEACH });
}

// 10 riferimento medio e rango
{
  const s = content(t("Re-referencing", "Ri-referenziazione"), t("Average reference and the rank of the data", "Riferimento medio e rango dei dati"),
    { notes: t("Average reference: V_avg(ch) = V(ch) − mean over channels. After it, the channels sum to zero → rank N−1. ICA must then use N−1 components (EEGLAB pop_runica 'pca' option or automatic rank detection) — otherwise ghost components appear (Kim et al., 2023).", "Riferimento medio: V_avg(ch) = V(ch) − media sui canali. Dopo, i canali sommano a zero → rango N−1. L'ICA deve allora usare N−1 componenti (opzione 'pca' di pop_runica o stima automatica del rango) — altrimenti compaiono componenti fantasma (Kim et al., 2023).") });
  formula(s, "V_{avg}(ch) = V(ch) − (1/N) Σ_{k} V(k)", X0 + 2.5, Y0, CW - 5.0, 0.8, { sz: 24, fill: PEACH });
  text(s, [B("Remove/interpolate bad channels ++first++: one bad channel contaminates ++all++ channels through the mean.", "Togliere/interpolare i canali cattivi ++prima++: un canale cattivo contamina ++tutti++ i canali attraverso la media."),
    B("With ≥ 64 well-spread electrodes the average reference approximates a ++zero-potential++ reference (Dien, 1998).", "Con ≥ 64 elettrodi ben distribuiti il riferimento medio approssima un riferimento a ++potenziale zero++ (Dien, 1998)."),
    B("After average reference the channels sum to zero → ++rank = N − 1++ (minus 1 for each interpolated channel).", "Dopo il riferimento medio i canali sommano a zero → ++rango = N − 1++ (meno 1 per ogni canale interpolato)."),
    B("~Tell ICA the true rank~, or it will return spurious \"ghost\" components.", "~Comunicare all'ICA il rango vero~, altrimenti restituisce componenti \"fantasma\" spurie.")], X0, 2.6, CW, 3.4, { sz: 18, after: 12 });
}

section(3, "Epochs, baseline and rejection", "Epoche, baseline e rigetto");

// 12 epoche
{
  const s = content(t("Epochs (1)", "Epoche (1)"), t("Cutting the continuous signal around events", "Tagliare il segnale continuo attorno agli eventi"),
    { notes: t("Triggers must be verified (photodiode). Epoch windows should include a pre-stimulus baseline and extra margins if time-frequency analyses follow (edge effects of wavelets).", "I trigger vanno verificati (fotodiodo). Le finestre devono includere una baseline pre-stimolo e margini extra se seguono analisi tempo-frequenza (effetti di bordo delle wavelet).") });
  fig(s, "f12_epochs", X0, Y0, CW, 3.3, "c", "Epoching");
  text(s, [B("*Epoch* = a time window locked to an event (stimulus or response), e.g. −200 … +800 ms.", "*Epoca* = una finestra temporale agganciata a un evento (stimolo o risposta), es. −200 … +800 ms."),
    B("*Baseline correction*: subtract the mean of the pre-stimulus interval from each channel and epoch.", "*Correzione della baseline*: sottrarre la media dell'intervallo pre-stimolo a ogni canale ed epoca."),
    B("Longer epochs for ++time-frequency++ analysis (wavelet edge effects) and for slow components.", "Epoche più lunghe per l'analisi ++tempo-frequenza++ (effetti di bordo delle wavelet) e per componenti lente.")], X0, 5.05, CW, 1.7, { sz: 15, after: 6 });
}

// 13 rigetto
{
  const s = content(t("Epochs (2)", "Epoche (2)"), t("Rejecting bad epochs", "Rigettare le epoche cattive"),
    { notes: t("Luck (2014) ch. 6. Artifact Subspace Reconstruction: Mullen et al. (2015) IEEE TBME 62:2553; Chang et al. (2020) IEEE TBME 67:1114. Balance data quality against the number of trials; report how many trials were rejected per condition.", "Luck (2014) cap. 6. Artifact Subspace Reconstruction: Mullen et al. (2015) IEEE TBME 62:2553; Chang et al. (2020) IEEE TBME 67:1114. Bilanciare la qualità dei dati e il numero di trial; riportare quanti trial sono stati rigettati per condizione.") });
  fig(s, "f14_reject", X0, Y0, 4.8, 4.6, "l", "Epoch rejection");
  text(s, [B("*Thresholds*: absolute (±100 µV) or peak-to-peak in a moving window.", "*Soglie*: assolute (±100 µV) o picco-picco in finestra mobile."),
    B("*Statistics*: improbable data, kurtosis, joint probability across channels.", "*Statistiche*: dati improbabili, curtosi, probabilità congiunta tra canali."),
    B("*ASR* (Artifact Subspace Reconstruction): repairs short high-variance bursts on the continuous data (Mullen et al., 2015).", "*ASR* (Artifact Subspace Reconstruction): ripara brevi burst ad alta varianza sui dati continui (Mullen et al., 2015)."),
    B("Keep ++enough trials++ and ++similar numbers++ across conditions; report rejection rates.", "Mantenere ++abbastanza trial++ e ++numeri simili++ tra condizioni; riportare le percentuali di rigetto."),
    B("~Correct~ what you can (ICA), ~reject~ what you must.", "~Correggere~ ciò che si può (ICA), ~rigettare~ ciò che si deve.")], 5.8, Y0, 6.9, 4.8, { sz: 16, after: 12 });
}

section(4, "Independent Component Analysis", "Analisi delle componenti indipendenti");

// 15 cocktail party
{
  const s = content(t("ICA (1)", "ICA (1)"), t("The cocktail-party problem", "Il problema del cocktail party"),
    { notes: t("Bell & Sejnowski (1995) Neural Comput 7:1129; Makeig et al. (1996) NIPS 8; Jung et al. (2000) Psychophysiology 37:163. Each electrode records a weighted sum of all sources; ICA estimates an unmixing matrix W so that the outputs are maximally independent.", "Bell & Sejnowski (1995) Neural Comput 7:1129; Makeig et al. (1996) NIPS 8; Jung et al. (2000) Psychophysiology 37:163. Ogni elettrodo registra una somma pesata di tutte le sorgenti; l'ICA stima una matrice di separazione W tale che le uscite siano massimamente indipendenti.") });
  fig(s, "f16_cocktail", X0, Y0, CW, 2.9, "c", "Cocktail party");
  text(s, [B("Several people talk at once; each microphone records a ++different mixture++. Can we recover each voice without knowing the room?", "Più persone parlano insieme; ogni microfono registra una ++miscela diversa++. Possiamo recuperare ogni voce senza conoscere la stanza?"),
    B("EEG: electrodes = microphones; brain, eyes, muscles, heart = speakers. Volume conduction = ++instantaneous linear mixing++.", "EEG: elettrodi = microfoni; cervello, occhi, muscoli, cuore = oratori. Conduzione di volume = ++miscelazione lineare istantanea++."),
    B("ICA is ++blind++: it uses only the statistics of the data.", "L'ICA è ++cieca++: usa solo la statistica dei dati.")], X0, 4.5, CW, 2.2, { sz: 17, after: 10 });
}

// 16 modello
{
  const s = content(t("ICA (2)", "ICA (2)"), t("The model and its assumptions", "Il modello e le sue ipotesi"),
    { notes: t("x(t) = A s(t); W ≈ A⁻¹; s(t) = W x(t). Columns of A = scalp maps of the components; rows of W = spatial filters. Ambiguities: order, sign and scale of the components are arbitrary. Hyvärinen & Oja (2000) Neural Netw 13:411.", "x(t) = A s(t); W ≈ A⁻¹; s(t) = W x(t). Colonne di A = mappe di scalpo delle componenti; righe di W = filtri spaziali. Ambiguità: ordine, segno e scala delle componenti sono arbitrari. Hyvärinen & Oja (2000) Neural Netw 13:411.") });
  formula(s, "x(t) = A · s(t)          ŝ(t) = W · x(t),   W ≈ A^{−1}", X0 + 0.5, Y0, 6.2, 0.8, { sz: 21, fill: PEACH });
  fig(s, "f17_scatter", X0 + 0.3, 2.5, 6.4, 3.4, "c", "ICA scatter");
  text(s, [B("*Columns of A*: scalp maps (topographies) of the components.", "*Colonne di A*: mappe di scalpo (topografie) delle componenti."),
    B("*Rows of W*: spatial filters that extract each component.", "*Righe di W*: filtri spaziali che estraggono ogni componente."),
    { t: "~" + t("Assumptions", "Ipotesi") + "~" },
    B("Sources ++statistically independent++ and ++non-Gaussian++.", "Sorgenti ++statisticamente indipendenti++ e ++non gaussiane++."),
    B("Mixing ++linear, instantaneous, stationary++ (fixed sources).", "Miscelazione ++lineare, istantanea, stazionaria++ (sorgenti fisse)."),
    B("Number of sources ≤ number of channels (rank).", "Numero di sorgenti ≤ numero di canali (rango)."),
    B("Order, sign and scale of components are ++arbitrary++.", "Ordine, segno e scala delle componenti sono ++arbitrari++.")], 7.3, Y0, 5.4, 5.0, { sz: 16, after: 8 });
}

// 17 non gaussianità
{
  const s = content(t("ICA (3)", "ICA (3)"), t("Why non-Gaussianity reveals the sources", "Perché la non gaussianità rivela le sorgenti"),
    { notes: t("Central limit theorem: sums of independent variables tend to a Gaussian. So ICA looks for projections that are as non-Gaussian as possible (kurtosis, negentropy) — or, equivalently, maximises the information transmitted (Infomax). Blinks are super-Gaussian (sparse), line noise is sub-Gaussian.", "Teorema del limite centrale: le somme di variabili indipendenti tendono a una gaussiana. Quindi l'ICA cerca proiezioni il più possibile non gaussiane (curtosi, negentropia) — o, equivalentemente, massimizza l'informazione trasmessa (Infomax). Gli ammiccamenti sono super-gaussiani (sparsi), la rete è sub-gaussiana.") });
  fig(s, "f18_clt", X0 + 0.5, Y0, CW - 1.0, 2.8, "c", "Central limit theorem");
  text(s, [B("A mixture of independent sources is ++more Gaussian++ than each source (central limit theorem).", "Una miscela di sorgenti indipendenti è ++più gaussiana++ di ogni sorgente (teorema del limite centrale)."),
    B("So: rotate the data until the outputs are ++as non-Gaussian as possible++ (kurtosis, negentropy) → you have found the sources.", "Quindi: ruotare i dati finché le uscite sono ++il più possibile non gaussiane++ (curtosi, negentropia) → si sono trovate le sorgenti."),
    B("Blinks and ECG are *super-Gaussian* (sparse, heavy tails); line noise is *sub-Gaussian*: extended Infomax handles both.", "Ammiccamenti ed ECG sono *super-gaussiani* (sparsi, code pesanti); la rete è *sub-gaussiana*: l'Infomax esteso li gestisce entrambi.")], X0, 4.55, CW, 1.75, { sz: 16, after: 8 });
  meta(s, t("a ++smoothie++ tastes \"average\": to recognise the fruits, look for the most distinctive flavours.", "un ++frullato++ ha un sapore \"medio\": per riconoscere i frutti, cerca i sapori più distintivi."), X0, 6.3, CW, 0.5, 14);
}

// 18 algoritmi e pratica
{
  const s = content(t("ICA (4)", "ICA (4)"), t("Algorithms and practical recipes", "Algoritmi e ricette pratiche"),
    { notes: t("Infomax: Bell & Sejnowski (1995); extended Infomax: Lee, Girolami & Sejnowski (1999) Neural Comput 11:417; FastICA: Hyvärinen (1999) IEEE TNN 10:626; AMICA: Palmer et al. (2011); comparison: Delorme et al. (2012) PLoS One 7:e30135. 1-Hz high-pass for ICA: Winkler et al. (2015) EMBC; Klug & Gramann (2021) Eur J Neurosci. Data amount: Onton & Makeig (2006) suggest k·N² samples with k ≳ 20–30.", "Infomax: Bell & Sejnowski (1995); Infomax esteso: Lee, Girolami & Sejnowski (1999) Neural Comput 11:417; FastICA: Hyvärinen (1999) IEEE TNN 10:626; AMICA: Palmer et al. (2011); confronto: Delorme et al. (2012) PLoS One 7:e30135. Passa-alto a 1 Hz per l'ICA: Winkler et al. (2015) EMBC; Klug & Gramann (2021) Eur J Neurosci. Quantità di dati: Onton & Makeig (2006) suggeriscono k·N² campioni con k ≳ 20–30.") });
  cards(s, [["Infomax / ext. Infomax", t("maximises information flow; EEGLAB runica default (Bell & Sejnowski, 1995; Lee et al., 1999)", "massimizza il flusso d'informazione; default di runica in EEGLAB (Bell & Sejnowski, 1995; Lee et al., 1999)")],
    ["FastICA", t("fixed-point, maximises negentropy; fast but less stable across runs (Hyvärinen, 1999)", "punto fisso, massimizza la negentropia; veloce ma meno stabile tra esecuzioni (Hyvärinen, 1999)")],
    ["AMICA", t("adaptive mixture model; best separation in comparisons, slower (Delorme et al., 2012)", "modello a miscela adattivo; migliore separazione nei confronti, più lento (Delorme et al., 2012)")],
    ["SOBI", t("uses temporal correlations (second-order); good for rhythmic sources (Belouchrani et al., 1997)", "usa le correlazioni temporali (secondo ordine); buono per sorgenti ritmiche (Belouchrani et al., 1997)")]], Y0, 2.0, 14);
  rows(s, [t("Train ICA on a ++1-Hz high-passed copy++, then apply the weights to the 0.1-Hz data (Winkler et al., 2015).", "Addestrare l'ICA su una ++copia filtrata a 1 Hz++, poi applicare i pesi ai dati a 0,1 Hz (Winkler et al., 2015)."),
    t("Enough data: ++≈ 20–30 × N²++ samples (N = channels); remove gross, non-stereotyped artifacts first.", "Dati sufficienti: ++≈ 20–30 × N²++ campioni (N = canali); togliere prima gli artefatti grossolani non stereotipati."),
    t("Set the number of components to the ++data rank++ (after reference and interpolation).", "Impostare il numero di componenti al ++rango dei dati++ (dopo riferimento e interpolazione).")], X0, 3.8, CW, 0.8, 0.15, 16, ACC);
}

// 19 galleria componenti
{
  const s = content(t("ICA (5)", "ICA (5)"), t("Reading components: map, time course, spectrum", "Leggere le componenti: mappa, andamento, spettro"),
    { notes: t("Chaumon, Bishop & Busch (2015) J Neurosci Methods 250:47 — a practical guide to IC classification. Eye: frontal map, blinks/saccades in time, low-frequency spectrum. Muscle: focal temporal/edge map, broadband >20 Hz. Heart: broad gradient, regular QRS. Channel noise: single-electrode map. Brain: dipolar map, 1/f spectrum with alpha peak.", "Chaumon, Bishop & Busch (2015) J Neurosci Methods 250:47 — guida pratica alla classificazione delle IC. Occhio: mappa frontale, ammiccamenti/saccadi, spettro a bassa frequenza. Muscolo: mappa focale temporale/di bordo, banda larga >20 Hz. Cuore: gradiente ampio, QRS regolari. Rumore di canale: mappa su un solo elettrodo. Cervello: mappa dipolare, spettro 1/f con picco alfa.") });
  fig(s, "f20_ics", X0, Y0, CW, 2.8, "c", "Component gallery");
  text(s, [B("*Brain* ICs: smooth ++dipolar++ maps, 1/f spectrum with peaks (alpha, mu, beta).", "IC *cerebrali*: mappe ++dipolari++ lisce, spettro 1/f con picchi (alfa, mu, beta)."),
    B("*Eye*: strong frontal map; blinks/saccades; power at low frequencies.", "*Occhio*: forte mappa frontale; ammiccamenti/saccadi; potenza alle basse frequenze."),
    B("*Muscle*: focal at the edge (temporal), ++broadband > 20 Hz++. *Heart*: broad gradient, regular beats ≈ 1 Hz.", "*Muscolo*: focale al bordo (temporale), ++banda larga > 20 Hz++. *Cuore*: gradiente ampio, battiti regolari ≈ 1 Hz."),
    B("*Channel / line*: one electrode or 50 Hz only.", "*Canale / rete*: un solo elettrodo o solo 50 Hz.")], X0, 4.7, CW, 2.0, { sz: 15, after: 6 });
}

// 20 ICLabel
{
  const s = content(t("ICA (6)", "ICA (6)"), t("ICLabel: automatic component classification", "ICLabel: classificazione automatica delle componenti"),
    { notes: t("Pion-Tonachini, Kreutz-Delgado & Makeig (2019) NeuroImage 198:181. Trained on >6000 datasets labelled by crowd-sourcing. Outputs 7 class probabilities. Common rule: remove eye and muscle ICs with p > 0.8–0.9; always check a few components by eye.", "Pion-Tonachini, Kreutz-Delgado & Makeig (2019) NeuroImage 198:181. Addestrato su >6000 dataset etichettati in crowd-sourcing. Restituisce 7 probabilità di classe. Regola comune: rimuovere IC oculari e muscolari con p > 0,8–0,9; verificare sempre alcune componenti a occhio.") });
  const cls = [["Brain", "0.02"], ["Muscle", "0.01"], ["Eye", "0.95"], ["Heart", "0.00"], ["Line Noise", "0.00"], ["Channel Noise", "0.01"], ["Other", "0.01"]];
  card(s, X0, Y0, 5.2, 4.5, TINT);
  s.addText(t("Example: IC 1 (blink)", "Esempio: IC 1 (ammiccamento)"), { x: X0 + 0.25, y: Y0 + 0.1, w: 4.7, h: 0.45, fontFace: SANS, fontSize: 16, bold: true, color: TEAL, margin: 0, isTextBox: true });
  cls.forEach(([c, p], i) => {
    const y = Y0 + 0.7 + i * 0.52, v = parseFloat(p);
    s.addText(c, { x: X0 + 0.25, y, w: 1.9, h: 0.4, fontFace: SANS, fontSize: 14, color: TXT, valign: "middle", margin: 0, isTextBox: true });
    s.addShape(pres.shapes.RECTANGLE, { x: X0 + 2.2, y: y + 0.08, w: Math.max(0.03, 2.3 * v), h: 0.24, fill: { color: v > 0.5 ? ACC : TEAL }, line: { color: v > 0.5 ? ACC : TEAL } });
    s.addText(LANGARG === "it" ? p.replace(".", ",") : p, { x: X0 + 4.55, y, w: 0.6, h: 0.4, fontFace: SANS, fontSize: 13, color: MUTED, valign: "middle", margin: 0, isTextBox: true });
  });
  text(s, [B("A neural network trained on thousands of expert-labelled components returns ++7 class probabilities++ (Pion-Tonachini et al., 2019).", "Una rete neurale addestrata su migliaia di componenti etichettate da esperti restituisce ++7 probabilità di classe++ (Pion-Tonachini et al., 2019)."),
    B("Typical rule: flag *Eye* and *Muscle* ICs with p > 0.8–0.9.", "Regola tipica: marcare le IC *Oculari* e *Muscolari* con p > 0,8–0,9."),
    B("It is a ++help, not an oracle++: check maps, spectra and time courses.", "È un ++aiuto, non un oracolo++: controllare mappe, spettri e andamenti."),
    B("Report: algorithm, rank, how many ICs removed and by which criterion.", "Riportare: algoritmo, rango, quante IC rimosse e con quale criterio.")], 6.3, Y0, 6.4, 4.6, { sz: 16, after: 12 });
}

// 21 back-projection
{
  const s = content(t("ICA (7)", "ICA (7)"), t("Removing artifacts: back-projection", "Rimuovere gli artefatti: retro-proiezione"),
    { notes: t("x_clean = A_{:,k∉art} s_{k∉art}. The artifact is subtracted from all channels at once, without losing trials. If a component mixes brain and artifact (poor separation), removing it also removes brain signal — hence the importance of good ICA training data.", "x_pulito = A_{:,k∉art} s_{k∉art}. L'artefatto viene sottratto da tutti i canali insieme, senza perdere trial. Se una componente mescola cervello e artefatto (separazione scarsa), rimuoverla toglie anche segnale cerebrale — da qui l'importanza di buoni dati di addestramento.") });
  fig(s, "f22_backproj", X0, Y0, CW, 2.9, "c", "Back-projection");
  formula(s, "x_{clean}(t) = Σ_{k ∉ artifacts} a_{k} · s_{k}(t)", X0 + 3.0, 4.85, CW - 6.0, 0.75, { sz: 20, fill: PEACH });
  text(s, [B("Set artifact components to zero and ++re-mix++ the rest: all trials are kept.", "Azzerare le componenti artefattuali e ++ri-miscelare++ il resto: si conservano tutti i trial."),
    B("⚠ Poorly separated ICs contain brain signal too: remove ++only clear artifacts++.", "⚠ IC mal separate contengono anche segnale cerebrale: rimuovere ++solo artefatti chiari++.")], X0, 5.75, CW, 1.0, { sz: 16, after: 6 });
}

section(5, "Pipelines in practice", "Pipeline in pratica");

// 23 EEGLAB
{
  const s = content(t("In MATLAB", "In MATLAB"), t("A minimal EEGLAB pipeline", "Una pipeline EEGLAB minima"),
    { notes: t("Functions from EEGLAB (Delorme & Makeig, 2004) and its plug-ins clean_rawdata and ICLabel. ICLabel class order: Brain, Muscle, Eye, Heart, Line Noise, Channel Noise, Other. Adapt thresholds to your data and always inspect the result.", "Funzioni di EEGLAB (Delorme & Makeig, 2004) e dei plug-in clean_rawdata e ICLabel. Ordine delle classi di ICLabel: Brain, Muscle, Eye, Heart, Line Noise, Channel Noise, Other. Adattare le soglie ai propri dati e ispezionare sempre il risultato.") });
  card(s, X0, Y0, CW, 5.1, TINT);
  const code = [
    "EEG = pop_loadset('sub-01_task-oddball_eeg.set');",
    "EEG = pop_eegfiltnew(EEG, 'locutoff', 0.1, 'hicutoff', 40);        % zero-phase FIR",
    "orig = EEG.chanlocs;",
    "EEG = pop_clean_rawdata(EEG, 'FlatlineCriterion', 5, 'ChannelCriterion', 0.8, ...",
    "        'LineNoiseCriterion', 4, 'BurstCriterion', 'off', 'WindowCriterion', 'off');",
    "EEG = pop_interp(EEG, orig, 'spherical');                           % bad channels",
    "EEG = pop_reref(EEG, []);                                           % average reference",
    "tmp = pop_eegfiltnew(EEG, 'locutoff', 1);                           % 1-Hz copy for ICA",
    "tmp = pop_runica(tmp, 'icatype', 'runica', 'extended', 1, 'pca', rank(double(tmp.data')));",
    "EEG.icaweights = tmp.icaweights; EEG.icasphere = tmp.icasphere;",
    "EEG.icachansind = tmp.icachansind; EEG.icawinv = []; EEG = eeg_checkset(EEG);",
    "EEG = pop_iclabel(EEG, 'default');",
    "EEG = pop_icflag(EEG, [NaN NaN; 0.9 1; 0.9 1; NaN NaN; NaN NaN; NaN NaN; NaN NaN]);",
    "EEG = pop_subcomp(EEG, find(EEG.reject.gcompreject), 0);            % back-projection",
    "EEG = pop_epoch(EEG, {'S1'}, [-0.2 0.8]);",
    "EEG = pop_rmbase(EEG, [-200 0]);"];
  text(s, code.map(c => ({ t: c, c: c.includes("%") ? TXT : TXT })), X0 + 0.25, Y0 + 0.15, CW - 0.5, 4.8, { raw: true, sz: 12, face: "Consolas", after: 3 });
}

// 24 pipeline automatiche
{
  const s = content(t("Pipelines", "Pipeline"), t("Automated pipelines and reporting", "Pipeline automatiche e documentazione"),
    { notes: t("PREP: Bigdely-Shamlo et al. (2015); HAPPE: Gabard-Durnam et al. (2018) Front Neurosci 12:97; APP: da Cruz et al. (2018); Automagic: Pedroni et al. (2019) NeuroImage 200:460; Delorme (2023) Sci Rep 13:2372 'EEG is better left alone'. Reporting: Keil et al. (2014); Pernet et al. (2020) Nat Neurosci 23:1473 (COBIDAS MEEG).", "PREP: Bigdely-Shamlo et al. (2015); HAPPE: Gabard-Durnam et al. (2018) Front Neurosci 12:97; APP: da Cruz et al. (2018); Automagic: Pedroni et al. (2019) NeuroImage 200:460; Delorme (2023) Sci Rep 13:2372 'EEG is better left alone'. Documentazione: Keil et al. (2014); Pernet et al. (2020) Nat Neurosci 23:1473 (COBIDAS MEEG).") });
  cards(s, [["PREP", t("robust referencing, bad-channel detection (Bigdely-Shamlo et al., 2015)", "riferimento robusto, rilevamento dei canali cattivi (Bigdely-Shamlo et al., 2015)")],
    ["HAPPE", t("for infants and short, noisy recordings (Gabard-Durnam et al., 2018)", "per neonati e registrazioni brevi e rumorose (Gabard-Durnam et al., 2018)")],
    ["Automagic", t("large datasets, quality ratings per file (Pedroni et al., 2019)", "grandi dataset, valutazioni di qualità per file (Pedroni et al., 2019)")],
    ["MNE / FieldTrip", t("Python / MATLAB alternatives; same steps, different defaults", "alternative in Python / MATLAB; stessi passi, default diversi")]], Y0, 1.9, 14);
  text(s, [B("Automatic ≠ unsupervised: check ++quality metrics++ and plots for every subject.", "Automatico ≠ non supervisionato: controllare ++metriche di qualità++ e grafici per ogni soggetto."),
    B("Preprocessing choices create a ++\"garden of forking paths\"++: decide the pipeline ++before++ looking at the effects (pre-registration).", "Le scelte di pre-elaborazione creano un ++\"giardino dei sentieri che si biforcano\"++: decidere la pipeline ++prima++ di guardare gli effetti (pre-registrazione)."),
    B("Report following ++COBIDAS-MEEG++ (Pernet et al., 2020) and share code + BIDS data.", "Documentare secondo ++COBIDAS-MEEG++ (Pernet et al., 2020) e condividere codice + dati BIDS.")], X0, 3.7, CW, 2.8, { sz: 17, after: 12 });
}

// 25 domande
{
  const s = content(t("Check your understanding", "Verifica"), t("Three questions", "Tre domande"),
    { notes: t("(1) The average includes the bad channel → noise spread everywhere. (2) Rank deficiency: 64 channels, average reference, 2 interpolated → rank 61. (3) Zero-phase filters are acausal: the effect may be a filter artifact; check with a causal filter.", "(1) La media include il canale cattivo → rumore diffuso ovunque. (2) Rango: 64 canali, riferimento medio, 2 interpolati → rango 61. (3) I filtri a fase zero sono acausali: l'effetto potrebbe essere un artefatto del filtro; verificare con un filtro causale.") });
  rows(s, [t("Why must bad channels be removed ++before++ computing the average reference?", "Perché i canali cattivi vanno tolti ++prima++ di calcolare il riferimento medio?"),
    t("64 channels, average reference, 2 interpolated channels: how many ICs should you estimate?", "64 canali, riferimento medio, 2 canali interpolati: quante IC dovresti stimare?"),
    t("An ERP difference starts 20 ms ++before++ the stimulus. What could explain it?", "Una differenza ERP inizia 20 ms ++prima++ dello stimolo. Che cosa potrebbe spiegarla?")], X0, Y0 + 0.2, CW, 1.2, 0.35, 18, ACC);
}

// 26 take home
{
  const s = content(t("Take-home messages", "Messaggi chiave"), t("Take-home messages", "Messaggi chiave"));
  rows(s, [t("A pipeline is a sequence of ++choices++: justify, report, share.", "Una pipeline è una sequenza di ++scelte++: motivarle, riportarle, condividerle."),
    t("Filter the ++continuous++ data; know the ++delay/acausality++ of your filters.", "Filtrare i dati ++continui++; conoscere ++ritardo/acausalità++ dei propri filtri."),
    t("Bad channels out ++before++ average reference; interpolation ++reduces rank++.", "Canali cattivi fuori ++prima++ del riferimento medio; l'interpolazione ++riduce il rango++."),
    t("ICA = ++linear unmixing++ of independent, non-Gaussian sources.", "ICA = ++separazione lineare++ di sorgenti indipendenti e non gaussiane."),
    t("Remove only ++clear++ artifact ICs; ICLabel helps, your eyes decide.", "Rimuovere solo IC artefattuali ++chiare++; ICLabel aiuta, i tuoi occhi decidono.")], X0, Y0, CW, 0.85, 0.15, 17);
}

// 27 letture
{
  const s = content(t("Suggested reading", "Letture consigliate"), t("Suggested reading", "Letture consigliate"));
  text(s, [
    { t: "Widmann A., Schröger E., Maess B. (2015) Digital filter design for electrophysiological data – a practical approach. *J Neurosci Methods* 250:34–46.", b: true },
    { t: "Bigdely-Shamlo N. et al. (2015) The PREP pipeline: standardized preprocessing for large-scale EEG analysis. *Front Neuroinform* 9:16.", b: true },
    { t: "Perrin F. et al. (1989) Spherical splines for scalp potential and current density mapping. *Electroencephalogr Clin Neurophysiol* 72:184–187.", b: true },
    { t: "Bell A.J., Sejnowski T.J. (1995) An information-maximization approach to blind separation and blind deconvolution. *Neural Comput* 7:1129–1159.", b: true },
    { t: "Jung T.-P. et al. (2000) Removing electroencephalographic artifacts by blind source separation. *Psychophysiology* 37:163–178.", b: true },
    { t: "Hyvärinen A., Oja E. (2000) Independent component analysis: algorithms and applications. *Neural Netw* 13:411–430.", b: true },
    { t: "Delorme A. et al. (2012) Independent EEG sources are dipolar. *PLoS One* 7:e30135.", b: true },
    { t: "Chaumon M., Bishop D.V.M., Busch N.A. (2015) A practical guide to the selection of independent components of the EEG. *J Neurosci Methods* 250:47–63.", b: true },
    { t: "Pion-Tonachini L., Kreutz-Delgado K., Makeig S. (2019) ICLabel: an automated EEG independent component classifier. *NeuroImage* 198:181–197.", b: true },
    { t: "Mullen T.R. et al. (2015) Real-time neuroimaging and cognitive monitoring using wearable dry EEG. *IEEE Trans Biomed Eng* 62:2553–2567.", b: true },
    { t: "Delorme A. (2023) EEG is better left alone. *Sci Rep* 13:2372.", b: true },
    { t: "Pernet C. et al. (2020) Issues and recommendations from the OHBM COBIDAS MEEG committee. *Nat Neurosci* 23:1473–1483.", b: true }], X0, Y0, CW, 5.2, { sz: 12, after: 5 });
}

save(OUT);
