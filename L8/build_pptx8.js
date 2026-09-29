// EEG – Lecture 8: spatial analysis and microstates (bilingue: node build_pptx8.js en|it)
const __R = (function () { const p = require("path"), fs = require("fs"); let d = process.env.COURSE_ROOT || __dirname;
  while (!fs.existsSync(p.join(d, ".course_root")) && p.dirname(d) !== d) d = p.dirname(d); return d; })();
const LANGARG = process.argv[2] || "en";
global.CFG = { lang: LANGARG, fig: __R + "/L8/figpng_" + LANGARG, common: __R + "/common",
  footer: LANGARG === "it" ? "Brain Imaging · EEG · Lezione 8 · Analisi spaziale e microstati" : "Brain Imaging · EEG · Lecture 8 · Spatial analysis and microstates",
  lezione: LANGARG === "it" ? "Lezione 8" : "Lecture 8",
  titolo: LANGARG === "it" ? "Analisi spaziale\ne microstati EEG" : "Spatial analysis\nand EEG microstates", titoloSize: 42 };
const L = require(__R + "/common/pptlib_eeg.js");
const { tr: t, pres, fig, content, text, formula, card, badge, copertina, save } = L;
const { INK, ACC, TEAL, TXT, MUTED, TINT, WHITE, SERIF, SANS, W, H, MX, X0, Y0, CW } = L.C;
const OUT = process.argv[3] || `${__R}/L8/out/EEG_L8_${LANGARG}.pptx`;
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
  const s = content(t("Lecture 8", "Lezione 8"), t("Today: looking at the whole map, not single electrodes", "Oggi: guardare la mappa intera, non i singoli elettrodi"),
    { notes: t("Main reference: Michel & Koenig (2018) NeuroImage 180:577 — review on EEG microstates; Murray, Brunet & Michel (2008) Brain Topogr 20:249 — topographic ERP analyses.", "Riferimento principale: Michel & Koenig (2018) NeuroImage 180:577 — review sui microstati EEG; Murray, Brunet & Michel (2008) Brain Topogr 20:249 — analisi topografiche degli ERP.") });
  rows(s, [t("Limits of ++single-channel++ analysis; reference-free descriptors.", "Limiti dell'analisi ++a canale singolo++; descrittori indipendenti dal riferimento."),
    t("*Global Field Power* and *Global Map Dissimilarity*.", "*Global Field Power* e *Global Map Dissimilarity*."),
    t("*Microstates*: clustering (k-means, modified k-means, TAAHC), choosing k, back-fitting.", "*Microstati*: clustering (k-means, k-means modificato, TAAHC), scelta di k, back-fitting."),
    t("Microstate ++metrics++ and their neural meaning (fMRI networks, sources).", "++Metriche++ dei microstati e significato neurale (reti fMRI, sorgenti)."),
    t("*Applications*: cognition, sleep, anaesthesia, psychiatry, brain stimulation.", "*Applicazioni*: cognizione, sonno, anestesia, psichiatria, stimolazione cerebrale.")], X0, Y0, CW, 0.85, 0.15, 18);
}

// 3 perché spaziale
{
  const s = content(t("Why spatial analysis?", "Perché l'analisi spaziale?"), t("From many waveforms to one map per instant", "Da molte forme d'onda a una mappa per istante"),
    { notes: t("Traditional spontaneous-EEG analyses (spectral, envelope, time-frequency, connectivity) are channel-wise and reference-dependent. A topographic approach treats each instant as a map: a change of map shape implies a change of the active generators (Lehmann, 1987; Michel et al., 2009 'Electrical Neuroimaging').", "Le analisi tradizionali dell'EEG spontaneo (spettrale, inviluppo, tempo-frequenza, connettività) sono canale per canale e dipendono dal riferimento. Un approccio topografico tratta ogni istante come una mappa: un cambiamento di forma della mappa implica un cambiamento dei generatori attivi (Lehmann, 1987; Michel et al., 2009 'Electrical Neuroimaging').") });
  cards(s, [[t("Channel-wise analysis", "Analisi per canale"), t("spectra, envelopes, TF, connectivity on selected electrodes: ++depends on the reference++ and on the choice of channels.", "spettri, inviluppi, TF, connettività su elettrodi scelti: ++dipende dal riferimento++ e dalla scelta dei canali.")],
    [t("Map-wise analysis", "Analisi per mappa"), t("each instant = one ++scalp map++; the map ++shape++ does not change with the reference.", "ogni istante = una ++mappa di scalpo++; la ++forma++ della mappa non cambia con il riferimento.")],
    [t("Physical logic", "Logica fisica"), t("different map shape ⇒ ++different active generators++; same shape, different strength ⇒ same generators, more/less active.", "forma diversa ⇒ ++generatori attivi diversi++; stessa forma, intensità diversa ⇒ stessi generatori, più/meno attivi.")]], Y0, 3.0, 15);
  meta(s, t("a ++weather map++: meteorologists do not compare single stations, they look at the whole pressure pattern.", "una ++mappa meteo++: i meteorologi non confrontano singole stazioni, guardano l'intero campo di pressione."), X0, 4.9, CW, 0.7, 16);
}

section(1, "The scalp field as a map", "Il campo di scalpo come mappa");

// 5 GFP
{
  const s = content(t("Spatial descriptors (1)", "Descrittori spaziali (1)"), t("Global Field Power: the strength of the map", "Global Field Power: l'intensità della mappa"),
    { notes: t("Lehmann & Skrandies (1980) Electroencephalogr Clin Neurophysiol 48:609. GFP is the spatial standard deviation of the average-referenced map; it is reference-free. GFP peaks are moments of high signal-to-noise and maximal topographic stability.", "Lehmann & Skrandies (1980) Electroencephalogr Clin Neurophysiol 48:609. La GFP è la deviazione standard spaziale della mappa a riferimento medio; è indipendente dal riferimento. I picchi di GFP sono momenti di alto rapporto segnale/rumore e massima stabilità topografica.") });
  formula(s, "GFP(t) = √[ (1/N) Σ_{i} (V_{i}(t) − V̄(t))² ]", X0 + 2.5, Y0, CW - 5.0, 0.8, { sz: 22, fill: PEACH });
  fig(s, "f05_gfp", X0, 2.5, 7.4, 2.8, "l", "GFP");
  text(s, [B("GFP = ++spatial standard deviation++ across electrodes (Lehmann & Skrandies, 1980).", "GFP = ++deviazione standard spaziale++ tra gli elettrodi (Lehmann & Skrandies, 1980)."),
    B("++Reference-free++: one number per instant, the \"hilliness\" of the map.", "++Indipendente dal riferimento++: un numero per istante, quanto è \"montuosa\" la mappa."),
    B("GFP ++peaks++: highest SNR, most stable topographies → used for clustering.", "++Picchi++ di GFP: SNR massimo, topografie più stabili → usati per il clustering.")], 8.1, 2.5, 4.6, 3.8, { sz: 15, after: 12 });
}

// 6 GMD
{
  const s = content(t("Spatial descriptors (2)", "Descrittori spaziali (2)"), t("Global Map Dissimilarity: the shape of the map", "Global Map Dissimilarity: la forma della mappa"),
    { notes: t("Lehmann & Skrandies (1980); GMD = √(2(1−r)) with r the spatial correlation of GFP-normalised maps (range 0–2). TANOVA tests GMD between conditions by permutation (Murray et al., 2008; Koenig et al., 2011 RAGU, Comput Intell Neurosci).", "Lehmann & Skrandies (1980); GMD = √(2(1−r)) con r la correlazione spaziale delle mappe normalizzate per la GFP (intervallo 0–2). La TANOVA testa la GMD tra condizioni per permutazione (Murray et al., 2008; Koenig et al., 2011 RAGU, Comput Intell Neurosci).") });
  fig(s, "f06_gmd", X0, Y0, 7.6, 3.4, "l", "GMD");
  formula(s, "GMD = √[ 2 (1 − r_{uv}) ]", 8.3, Y0, 4.4, 0.8, { sz: 22, fill: PEACH });
  text(s, [B("Compare maps ++after normalising by GFP++: strength is removed, only ++shape++ remains.", "Confrontare le mappe ++dopo averle normalizzate per la GFP++: si toglie l'intensità, resta la ++forma++."),
    B("0 = identical shape; 2 = inverted polarity.", "0 = forma identica; 2 = polarità invertita."),
    B("*TANOVA*: permutation test of GMD between conditions (Murray et al., 2008).", "*TANOVA*: test di permutazione della GMD tra condizioni (Murray et al., 2008).")], 8.3, 2.6, 4.4, 3.4, { sz: 15, after: 12 });
  note(s, t("Two orthogonal questions: ++how strong++ (GFP) and ++which generators++ (GMD).", "Due domande ortogonali: ++quanto è forte++ (GFP) e ++quali generatori++ (GMD)."), X0, 5.4, 7.6, 0.8, 16);
}

// 7 quasi-stabilità
{
  const s = content(t("Microstates (1)", "Microstati (1)"), t("The EEG as a sequence of quasi-stable maps", "L'EEG come sequenza di mappe quasi stabili"),
    { notes: t("Lehmann et al. (1987) Electroencephalogr Clin Neurophysiol 67:271 — 'atoms of thought'. The map topography stays stable for ~60–120 ms, while its polarity may reverse with the oscillation, and then changes abruptly.", "Lehmann et al. (1987) Electroencephalogr Clin Neurophysiol 67:271 — 'atomi del pensiero'. La topografia resta stabile per ~60–120 ms, mentre la polarità può invertirsi con l'oscillazione, poi cambia bruscamente.") });
  fig(s, "f07_sequence", X0, Y0, CW, 2.7, "c", "Microstate sequence");
  text(s, [B("The map shape stays ++stable for ≈ 60–120 ms++ and then ++switches abruptly++ (Lehmann et al., 1987).", "La forma della mappa resta ++stabile per ≈ 60–120 ms++ e poi ++cambia bruscamente++ (Lehmann et al., 1987)."),
    B("Polarity may reverse with the oscillation: ++only the shape counts++.", "La polarità può invertirsi con l'oscillazione: ++conta solo la forma++."),
    B("These periods are *microstates*: \"atoms of thought\", building blocks of spontaneous mentation.", "Questi periodi sono i *microstati*: \"atomi del pensiero\", mattoni dell'attività mentale spontanea.")], X0, 4.65, CW, 1.5, { sz: 15, after: 6 });
  meta(s, t("a ++slide show++: each slide stays on screen for a moment, then the projector jumps to the next.", "una ++proiezione di diapositive++: ogni diapositiva resta per un attimo, poi il proiettore salta alla successiva."), X0, 6.2, CW, 0.55, 15);
}

section(2, "Microstate analysis", "Analisi dei microstati");

// 9 pipeline
{
  const s = content(t("Microstates (2)", "Microstati (2)"), t("The analysis pipeline", "La pipeline di analisi"),
    { notes: t("Standard pipeline (Michel & Koenig, 2018): band-pass 1–40 Hz, average reference, GFP peaks, clustering per subject, then group-level clustering of individual templates, back-fitting to all samples, computation of temporal parameters and statistics.", "Pipeline standard (Michel & Koenig, 2018): passa-banda 1–40 Hz, riferimento medio, picchi di GFP, clustering per soggetto, poi clustering di gruppo dei template individuali, back-fitting su tutti i campioni, calcolo dei parametri temporali e statistica.") });
  fig(s, "f09_pipeline", X0, Y0 + 0.2, CW, 1.6, "c", "Microstate pipeline");
  rows(s, [t("Preprocess: band-pass ++1–40 Hz++, artifact removal, ++average reference++.", "Pre-elaborare: passa-banda ++1–40 Hz++, rimozione artefatti, ++riferimento medio++."),
    t("Take maps at ++GFP peaks++ (highest SNR).", "Prendere le mappe ai ++picchi di GFP++ (SNR massimo)."),
    t("Cluster ++per subject++, then cluster the individual templates at ++group level++.", "Clustering ++per soggetto++, poi clustering dei template individuali a ++livello di gruppo++."),
    t("++Back-fit++ group templates to every sample; compute ++metrics++ and statistics.", "++Back-fitting++ dei template di gruppo su ogni campione; calcolare ++metriche++ e statistica.")], X0, 3.6, CW, 0.66, 0.12, 16, ACC);
}

// 10 k-means
{
  const s = content(t("Clustering (1)", "Clustering (1)"), t("k-means and modified k-means", "k-means e k-means modificato"),
    { notes: t("Pascual-Marqui, Michel & Lehmann (1995) IEEE Trans Biomed Eng 42:658 — modified k-means for EEG: maps are assigned by absolute spatial correlation (polarity ignored), cluster centres are the first principal component of the assigned maps. Several random initialisations; keep the solution with the highest GEV.", "Pascual-Marqui, Michel & Lehmann (1995) IEEE Trans Biomed Eng 42:658 — k-means modificato per l'EEG: le mappe si assegnano per correlazione spaziale assoluta (polarità ignorata), i centri sono la prima componente principale delle mappe assegnate. Più inizializzazioni casuali; si tiene la soluzione con la GEV più alta.") });
  fig(s, "f10_kmeans", X0, Y0, 7.4, 3.6, "l", "k-means");
  text(s, [B("Each map is a ++point in N-dimensional space++ (N = channels).", "Ogni mappa è un ++punto in uno spazio a N dimensioni++ (N = canali)."),
    B("*k-means*: assign each map to the nearest centre, update centres, repeat.", "*k-means*: assegnare ogni mappa al centro più vicino, aggiornare i centri, ripetere."),
    B("*Modified k-means* (Pascual-Marqui et al., 1995): similarity = |spatial correlation| → ++opposite polarities = same state++.", "*K-means modificato* (Pascual-Marqui et al., 1995): somiglianza = |correlazione spaziale| → ++polarità opposte = stesso stato++."),
    B("Random starts: repeat 50–100 times, keep the best GEV.", "Partenze casuali: ripetere 50–100 volte, tenere la GEV migliore.")], 8.1, Y0, 4.6, 4.6, { sz: 15, after: 10 });
}

// 11 TAAHC
{
  const s = content(t("Clustering (2)", "Clustering (2)"), t("Hierarchical alternatives: AAHC and TAAHC", "Alternative gerarchiche: AAHC e TAAHC"),
    { notes: t("AAHC: Murray et al. (2008) Brain Topogr 20:249; TAAHC: Khanna et al. (2014) Brain Topogr 27:540 (Microstates in resting-state EEG: current status and future directions, Khanna et al. 2015 Neurosci Biobehav Rev 49:105). Deterministic: no random initialisation.", "AAHC: Murray et al. (2008) Brain Topogr 20:249; TAAHC: Khanna et al. (2014) Brain Topogr 27:540 (e review Khanna et al. 2015 Neurosci Biobehav Rev 49:105). Deterministico: nessuna inizializzazione casuale.") });
  cards(s, [["AAHC", t("*Atomize and Agglomerate Hierarchical Clustering*: start with every map as a cluster; repeatedly ++dissolve the worst cluster++ and redistribute its maps (Murray et al., 2008).", "*Atomize and Agglomerate Hierarchical Clustering*: si parte con ogni mappa come cluster; si ++scioglie il cluster peggiore++ e se ne ridistribuiscono le mappe (Murray et al., 2008).")],
    ["TAAHC", t("*Topographic* AAHC: the worst cluster is the one with the ++lowest summed correlation++ with its members (Khanna et al., 2014).", "AAHC *topografico*: il cluster peggiore è quello con la ++minore correlazione sommata++ con i suoi membri (Khanna et al., 2014).")],
    [t("Pros & cons", "Pro e contro"), t("++Deterministic++ and gives all k at once; slower on large datasets. k-means is fast but depends on initialisation.", "++Deterministico++ e fornisce tutti i k in una volta; più lento su grandi dataset. Il k-means è veloce ma dipende dall'inizializzazione.")]], Y0, 3.3, 15);
  note(s, t("In practice both methods give very ++similar templates++: what matters more is data quality and the choice of k.", "In pratica i due metodi danno ++template molto simili++: contano di più la qualità dei dati e la scelta di k."), X0, 5.0, CW, 0.8, 16);
}

// 12 scelta di k
{
  const s = content(t("Clustering (3)", "Clustering (3)"), t("How many microstates? Criteria of fit", "Quanti microstati? Criteri di adattamento"),
    { notes: t("GEV: sum over time of GFP²·corr² divided by sum of GFP². Cross-validation criterion (Pascual-Marqui et al., 1995), Krzanowski–Lai criterion (Krzanowski & Lai, 1988 Biometrics 44:23). Meta-criterion combining several indices: Bréchet et al. (2019) NeuroImage; Custo et al. (2017) found 7 maps with high-density EEG.", "GEV: somma nel tempo di GFP²·corr² divisa per la somma di GFP². Criterio di cross-validation (Pascual-Marqui et al., 1995), criterio di Krzanowski–Lai (Krzanowski & Lai, 1988 Biometrics 44:23). Meta-criterio che combina più indici: Bréchet et al. (2019) NeuroImage; Custo et al. (2017) hanno trovato 7 mappe con EEG ad alta densità.") });
  fig(s, "f12_criteria", X0, Y0, CW, 2.6, "c", "Criteria");
  formula(s, "GEV = Σ_{t} [GFP(t) · corr(V_{t}, M_{k(t)})]² / Σ_{t} GFP(t)²", X0 + 1.8, 4.2, CW - 3.6, 0.7, { sz: 19, fill: PEACH });
  text(s, [B("*GEV* always grows with k: look for the ++elbow++. *CV* has a ++minimum++, *KL* a ++maximum++ at the optimal k.", "La *GEV* cresce sempre con k: cercare il ++gomito++. La *CV* ha un ++minimo++, *KL* un ++massimo++ al k ottimale."),
    B("Resting EEG: ++4 maps explain ≈ 70–80 %++ of the variance; high-density data may support ++5–7++ maps (Custo et al., 2017).", "EEG a riposo: ++4 mappe spiegano ≈ 70–80 %++ della varianza; dati ad alta densità possono supportarne ++5–7++ (Custo et al., 2017).")], X0, 5.05, CW, 1.6, { sz: 16, after: 8 });
}

// 13 template
{
  const s = content(t("Templates", "Template"), t("The four canonical microstate classes", "Le quattro classi canoniche di microstati"),
    { notes: t("Koenig et al. (2002) NeuroImage 16:41 (normative data across age, 6–80 years); Michel & Koenig (2018). Classes A–D are highly replicated across labs; in the user's own datasets: Zappasodi et al. 2019 (62 ch, 20 subj, 1–40 Hz, GEV ≈ 78 %) and Croce et al. 2020 (128 ch, 30 subj, 1–40 Hz, GEV ≈ 83 %).", "Koenig et al. (2002) NeuroImage 16:41 (dati normativi per età, 6–80 anni); Michel & Koenig (2018). Le classi A–D sono molto replicate tra laboratori; nei nostri dati: Zappasodi et al. 2019 (62 canali, 20 soggetti, 1–40 Hz, GEV ≈ 78 %) e Croce et al. 2020 (128 canali, 30 soggetti, 1–40 Hz, GEV ≈ 83 %).") });
  fig(s, "f13_templates", X0 + 0.5, Y0, CW - 1.0, 2.9, "c", "Templates A–D");
  text(s, [B("Classes *A–D* are ++remarkably reproducible++ across labs, montages and ages (Koenig et al., 2002).", "Le classi *A–D* sono ++molto riproducibili++ tra laboratori, montaggi ed età (Koenig et al., 2002)."),
    B("Example from our data: 62 ch → GEV ≈ 78 % (Zappasodi et al., 2019); 128 ch → GEV ≈ 83 %.", "Esempio dai nostri dati: 62 canali → GEV ≈ 78 % (Zappasodi et al., 2019); 128 canali → GEV ≈ 83 %."),
    B("Labels follow ++map shape++ (by convention), not function.", "Le etichette seguono la ++forma della mappa++ (per convenzione), non la funzione.")], X0, 4.8, CW, 1.8, { sz: 16, after: 10 });
}

// 14 backfitting
{
  const s = content(t("Back-fitting", "Back-fitting"), t("Labelling every time point", "Etichettare ogni istante"),
    { notes: t("Winner-takes-all: each sample (or each GFP peak with interpolation between peaks) is labelled with the template of maximal absolute spatial correlation. Temporal smoothing (e.g. minimum segment duration, Pascual-Marqui 1995 smoothing) avoids spurious short segments. Low-GFP samples are unreliable.", "Winner-takes-all: ogni campione (o ogni picco di GFP con interpolazione tra i picchi) riceve l'etichetta del template con massima correlazione spaziale assoluta. Uno smoothing temporale (es. durata minima dei segmenti, smoothing di Pascual-Marqui 1995) evita segmenti brevi spuri. I campioni a bassa GFP sono inaffidabili.") });
  fig(s, "f15_backfit", X0, Y0, CW, 2.4, "c", "Back-fitting");
  text(s, [B("Each sample gets the label of the template with the ++highest |spatial correlation|++ (*winner-takes-all*).", "Ogni campione riceve l'etichetta del template con la ++massima |correlazione spaziale|++ (*winner-takes-all*)."),
    B("++Temporal smoothing++: reject segments shorter than ≈ 20–30 ms; low-GFP samples take the neighbour's label.", "++Smoothing temporale++: scartare segmenti più brevi di ≈ 20–30 ms; i campioni a bassa GFP prendono l'etichetta del vicino."),
    B("Result: the EEG becomes a ++symbolic sequence++ … B C A D A B D C …", "Risultato: l'EEG diventa una ++sequenza simbolica++ … B C A D A B D C …")], X0, 4.0, CW, 2.3, { sz: 16, after: 10 });
}

// 15 metriche
{
  const s = content(t("Metrics", "Metriche"), t("Temporal parameters of microstates", "Parametri temporali dei microstati"),
    { notes: t("Standard metrics: mean duration (ms), occurrence (per second), coverage (% of time), GEV per class, transition probabilities (compare with those expected from occurrence). Typical resting values: duration 60–120 ms, occurrence 3–5/s (Michel & Koenig, 2018).", "Metriche standard: durata media (ms), occorrenza (al secondo), copertura (% del tempo), GEV per classe, probabilità di transizione (confrontarle con quelle attese dall'occorrenza). Valori tipici a riposo: durata 60–120 ms, occorrenza 3–5/s (Michel & Koenig, 2018).") });
  fig(s, "f16_metrics", X0, Y0, CW, 2.9, "c", "Metrics");
  cards(s, [[t("Duration", "Durata"), t("mean time a state lasts (≈ 60–120 ms)", "tempo medio di permanenza (≈ 60–120 ms)")], [t("Occurrence", "Occorrenza"), t("how often it appears per second (≈ 3–5 /s)", "quante volte compare al secondo (≈ 3–5 /s)")],
    [t("Coverage", "Copertura"), t("fraction of time it dominates", "frazione di tempo in cui domina")], [t("GEV / transitions", "GEV / transizioni"), t("variance explained; syntax of the sequence", "varianza spiegata; sintassi della sequenza")]], 4.4, 1.5, 14);
  note(s, t("Illustrative values from simulated data.", "Valori illustrativi da dati simulati."), X0, 6.05, CW, 0.5, 13);
}

section(3, "What are microstates?", "Che cosa sono i microstati?");

// 17 fMRI
{
  const s = content(t("Meaning (1)", "Significato (1)"), t("Microstates and fMRI resting-state networks", "Microstati e reti fMRI a riposo"),
    { notes: t("Britz, Van De Ville & Michel (2010) NeuroImage 52:1162; Musso et al. (2010) NeuroImage 52:1149; Yuan et al. (2012) NeuroImage 60:2062. Microstate time courses convolved with the HRF and used as GLM regressors correlate with BOLD resting-state networks. The mapping (A auditory, B visual, C salience, D attention) is debated and not one-to-one.", "Britz, Van De Ville & Michel (2010) NeuroImage 52:1162; Musso et al. (2010) NeuroImage 52:1149; Yuan et al. (2012) NeuroImage 60:2062. Gli andamenti dei microstati convoluti con la HRF e usati come regressori nel GLM correlano con reti BOLD a riposo. La corrispondenza (A uditiva, B visiva, C salienza, D attenzione) è dibattuta e non biunivoca.") });
  fig(s, "f13_templates", X0 + 1.0, Y0, CW - 2.0, 2.2, "c", "Templates");
  const nets = [t("auditory / phonological", "uditiva / fonologica"), t("visual", "visiva"), t("salience / cognitive control", "salienza / controllo cognitivo"), t("dorsal attention / fronto-parietal", "attenzione dorsale / fronto-parietale")];
  nets.forEach((n, i) => { const x = X0 + 1.0 + i * (CW - 2.0) / 4, w = (CW - 2.0) / 4 - 0.15; card(s, x, 3.95, w, 0.75, i % 2 ? PEACH : TINT); text(s, [{ t: n, align: "center" }], x + 0.1, 3.95, w - 0.2, 0.75, { sz: 13, valign: "middle" }); });
  text(s, [B("Microstate time courses, convolved with the ++HRF++, predict BOLD in ++resting-state networks++ (Britz et al., 2010; Musso et al., 2010).", "Gli andamenti dei microstati, convoluti con la ++HRF++, predicono il BOLD in ++reti a riposo++ (Britz et al., 2010; Musso et al., 2010)."),
    B("Microstates are ++fast++ (≈ 100 ms), networks ++slow++ (seconds): the sequence shows ++scale-free++ dynamics bridging the two (Van De Ville et al., 2010).", "I microstati sono ++veloci++ (≈ 100 ms), le reti ++lente++ (secondi): la sequenza ha dinamica ++scale-free++ che collega le due scale (Van De Ville et al., 2010)."),
    B("⚠ The one-to-one mapping is ++debated++.", "⚠ La corrispondenza uno-a-uno è ++dibattuta++.")], X0, 4.9, CW, 1.8, { sz: 15, after: 6 });
}

// 18 sorgenti
{
  const s = content(t("Meaning (2)", "Significato (2)"), t("Where do microstates come from?", "Da dove vengono i microstati?"),
    { notes: t("Custo et al. (2017) Brain Connect 7:671 — 7 microstate classes from 256-channel EEG, sources estimated by spatiotemporal regression (Custo et al., 2014 NeuroImage). Each microstate = distributed network, not a single source; the same map can arise from different source configurations (inverse problem, Lecture 9).", "Custo et al. (2017) Brain Connect 7:671 — 7 classi di microstati da EEG a 256 canali, sorgenti stimate con regressione spazio-temporale (Custo et al., 2014 NeuroImage). Ogni microstato = rete distribuita, non una sorgente singola; la stessa mappa può nascere da configurazioni di sorgenti diverse (problema inverso, Lezione 9).") });
  rows(s, [t("Each map reflects the ++synchronous activity of a distributed network++, not a single dipole.", "Ogni mappa riflette l'++attività sincrona di una rete distribuita++, non un singolo dipolo."),
    t("Source imaging (spatiotemporal regression) localises generators in ++insula, cingulate, occipital, parietal, prefrontal++ cortex (Custo et al., 2017).", "Il source imaging (regressione spazio-temporale) localizza i generatori in ++insula, cingolo, corteccia occipitale, parietale, prefrontale++ (Custo et al., 2017)."),
    t("With ++256 channels++, 7 classes are identified (A–G).", "Con ++256 canali++ si identificano 7 classi (A–G)."),
    t("⚠ Same map ≠ same sources: inverse problem (next lecture).", "⚠ Stessa mappa ≠ stesse sorgenti: problema inverso (prossima lezione).")], X0, Y0, CW, 0.9, 0.15, 17);
}

section(4, "Applications", "Applicazioni");

// 20 condizioni
{
  const s = content(t("Applications (1)", "Applicazioni (1)"), t("States of mind and brain", "Stati della mente e del cervello"),
    { notes: t("Seitzman et al. (2017) NeuroImage 146:533 (task vs rest, eyes open/closed); Zappasodi et al. (2019) NeuroImage 189:560 (fluid reasoning); Brodbeck et al. (2012) NeuroImage 62:2129 (sleep); Bréchet et al. (2020) Sci Rep; Li et al. (2021) IEEE J Biomed Health Inform (propofol: microstates become shorter and less variable with sedation). Koenig et al. (2002) (age).", "Seitzman et al. (2017) NeuroImage 146:533 (compito vs riposo, occhi aperti/chiusi); Zappasodi et al. (2019) NeuroImage 189:560 (ragionamento fluido); Brodbeck et al. (2012) NeuroImage 62:2129 (sonno); Bréchet et al. (2020) Sci Rep; Li et al. (2021) IEEE J Biomed Health Inform (propofol: microstati più brevi e meno variabili con la sedazione). Koenig et al. (2002) (età).") });
  cards(s, [[t("Cognition", "Cognizione"), t("serial subtraction vs rest changes C and D (Seitzman et al., 2017); microstates ++distinguish components of fluid reasoning++ (Zappasodi et al., 2019).", "sottrazione seriale vs riposo cambia C e D (Seitzman et al., 2017); i microstati ++distinguono componenti del ragionamento fluido++ (Zappasodi et al., 2019).")],
    [t("Sleep", "Sonno"), t("microstate durations ++increase++ in deep sleep (Brodbeck et al., 2012).", "le durate dei microstati ++aumentano++ nel sonno profondo (Brodbeck et al., 2012).")],
    [t("Anaesthesia", "Anestesia"), t("with propofol, microstates become ++shorter and less variable++ as sedation deepens (Li et al., 2021).", "con il propofol i microstati diventano ++più brevi e meno variabili++ al crescere della sedazione (Li et al., 2021).")],
    [t("Age", "Età"), t("parameters change ++lawfully across the lifespan++ (Koenig et al., 2002).", "i parametri cambiano ++regolarmente nell'arco della vita++ (Koenig et al., 2002).")]], Y0, 3.4, 14);
  note(s, t("Microstates are a ++sensitive, low-cost++ index of global brain state.", "I microstati sono un indice ++sensibile ed economico++ dello stato cerebrale globale."), X0, 5.1, CW, 0.8, 16);
}

// 21 clinica
{
  const s = content(t("Applications (2)", "Applicazioni (2)"), t("Psychiatry and brain stimulation", "Psichiatria e stimolazione cerebrale"),
    { notes: t("Schizophrenia: shorter D, more C — meta-analysis Rieger et al. (2016) Front Psychiatry; da Cruz et al. (2020) Nat Commun 11:3089 (candidate endophenotype). Bipolar disorder: Vellante et al. (2020) J Affect Disord. TMS: Croce, Zappasodi & Capotosto (2018) Sci Rep — offline stimulation of parietal cortex selectively affects microstates.", "Schizofrenia: D più breve, C più frequente — meta-analisi Rieger et al. (2016) Front Psychiatry; da Cruz et al. (2020) Nat Commun 11:3089 (candidato endofenotipo). Disturbo bipolare: Vellante et al. (2020) J Affect Disord. TMS: Croce, Zappasodi & Capotosto (2018) Sci Rep — la stimolazione offline della corteccia parietale modifica selettivamente i microstati.") });
  rows(s, [t("*Schizophrenia*: shorter class D, more frequent class C; a candidate ++endophenotype++ (da Cruz et al., 2020).", "*Schizofrenia*: classe D più breve, classe C più frequente; un possibile ++endofenotipo++ (da Cruz et al., 2020)."),
    t("*Bipolar disorder*: altered microstate dynamics related to clinical state (Vellante et al., 2020).", "*Disturbo bipolare*: dinamica dei microstati alterata e legata allo stato clinico (Vellante et al., 2020)."),
    t("*Brain stimulation*: rTMS over parietal cortex ++selectively++ changes specific microstates (Croce et al., 2018).", "*Stimolazione cerebrale*: la rTMS sulla corteccia parietale modifica ++selettivamente++ microstati specifici (Croce et al., 2018)."),
    t("Also: dementia, epilepsy, neonatal EEG, disorders of consciousness.", "Inoltre: demenza, epilessia, EEG neonatale, disturbi di coscienza.")], X0, Y0, CW, 0.9, 0.15, 16);
}

// 22 MATLAB
{
  const s = content(t("In MATLAB", "In MATLAB"), t("Microstates with a few lines of code", "Microstati in poche righe di codice"),
    { notes: t("Didactic implementation of modified k-means (Pascual-Marqui et al., 1995). For real analyses use the Microstate EEGLAB toolbox (Poulsen et al., 2018) or Koenig's MICROSTATELAB plug-in, which include smoothing, group clustering and statistics.", "Implementazione didattica del k-means modificato (Pascual-Marqui et al., 1995). Per analisi reali usare il Microstate EEGLAB toolbox (Poulsen et al., 2018) o il plug-in MICROSTATELAB di Koenig, che includono smoothing, clustering di gruppo e statistica.") });
  card(s, X0, Y0, CW, 5.1, TINT);
  const code = [
    "X   = EEG.data - mean(EEG.data, 1);                % average reference (ch x time)",
    "gfp = std(X, 1, 1);                                % Global Field Power",
    "[~, pk] = findpeaks(gfp);  M = X(:, pk);           % maps at GFP peaks",
    "M = M ./ vecnorm(M);  K = 4;  best = -Inf;",
    "for rep = 1:50                                     % random restarts",
    "    T = M(:, randperm(size(M,2), K));",
    "    for it = 1:100",
    "        [~, lab] = max(abs(T' * M));                % polarity-invariant assignment",
    "        for k = 1:K",
    "            [v,~] = eigs(M(:,lab==k) * M(:,lab==k)', 1);  T(:,k) = v;   % 1st PC",
    "        end",
    "    end",
    "    c = max(abs(T' * M));  gev = sum((gfp(pk).*c).^2) / sum(gfp(pk).^2);",
    "    if gev > best, best = gev; Tbest = T; end",
    "end",
    "Xn = X ./ vecnorm(X);  [~, seq] = max(abs(Tbest' * Xn));   % back-fitting"];
  text(s, code.map(c => ({ t: c })), X0 + 0.25, Y0 + 0.15, CW - 0.5, 4.8, { raw: true, sz: 12, face: "Consolas", after: 3 });
}

// 23 trappole
{
  const s = content(t("Pitfalls", "Trappole"), t("Pitfalls and open questions", "Trappole e questioni aperte"),
    { notes: t("von Wegner et al. (2018) NeuroImage (information-theoretic analysis of microstate sequences, non-Markovian dynamics); Koenig et al. (2024) review on standards (MICROSTATELAB); sensitivity to filter band and number of channels; circularity of templates computed on the same data used for statistics.", "von Wegner et al. (2018) NeuroImage (analisi di teoria dell'informazione delle sequenze di microstati, dinamica non markoviana); Koenig et al. (2024) review sugli standard (MICROSTATELAB); sensibilità alla banda del filtro e al numero di canali; circolarità dei template calcolati sugli stessi dati usati per la statistica.") });
  rows(s, [t("Results depend on ++filter band++, number of channels and clustering choices: report them.", "I risultati dipendono da ++banda del filtro++, numero di canali e scelte di clustering: riportarli."),
    t("k is a ++modelling choice++, not a law of nature (4 vs 5–7).", "k è una ++scelta di modello++, non una legge di natura (4 vs 5–7)."),
    t("Use ++group or normative templates++ to compare groups; beware circularity.", "Usare template ++di gruppo o normativi++ per confrontare i gruppi; attenzione alla circolarità."),
    t("Class labels (A–D) across studies are matched ++by eye or correlation++: check.", "Le etichette (A–D) tra studi si abbinano ++a occhio o per correlazione++: verificare."),
    t("Functional interpretation of each class is still ++debated++.", "L'interpretazione funzionale di ogni classe è ancora ++dibattuta++.")], X0, Y0, CW, 0.8, 0.14, 16, ACC);
}

// 24 domande
{
  const s = content(t("Check your understanding", "Verifica"), t("Three questions", "Tre domande"),
    { notes: t("(1) Same shape, different strength: GFP differs, GMD = 0 → same generators, different activation. (2) EEG oscillates: polarity reverses every half-cycle while the generator configuration is unchanged. (3) GEV always increases with k; use CV/KL or meta-criteria.", "(1) Stessa forma, intensità diversa: GFP diversa, GMD = 0 → stessi generatori, attivazione diversa. (2) L'EEG oscilla: la polarità si inverte ogni mezzo ciclo mentre la configurazione dei generatori non cambia. (3) La GEV cresce sempre con k; usare CV/KL o meta-criteri.") });
  rows(s, [t("Two conditions have maps with GMD = 0 but different GFP. What can you conclude about the generators?", "Due condizioni hanno mappe con GMD = 0 ma GFP diversa. Che cosa puoi concludere sui generatori?"),
    t("Why does modified k-means ignore map polarity?", "Perché il k-means modificato ignora la polarità delle mappe?"),
    t("GEV is 75 % with k = 4 and 82 % with k = 8. Why is k = 8 not automatically better?", "La GEV è 75 % con k = 4 e 82 % con k = 8. Perché k = 8 non è automaticamente migliore?")], X0, Y0 + 0.2, CW, 1.2, 0.35, 18, ACC);
}

// 25 take home
{
  const s = content(t("Take-home messages", "Messaggi chiave"), t("Take-home messages", "Messaggi chiave"));
  rows(s, [t("Maps are ++reference-free++: GFP = strength, GMD = shape.", "Le mappe sono ++indipendenti dal riferimento++: GFP = intensità, GMD = forma."),
    t("Spontaneous EEG = sequence of ++quasi-stable maps++ (microstates, ≈ 100 ms).", "EEG spontaneo = sequenza di ++mappe quasi stabili++ (microstati, ≈ 100 ms)."),
    t("GFP peaks → ++modified k-means / TAAHC++ → templates → back-fitting → metrics.", "Picchi di GFP → ++k-means modificato / TAAHC++ → template → back-fitting → metriche."),
    t("Four classes (A–D) explain ≈ 70–80 % of variance; they relate to ++large-scale networks++.", "Quattro classi (A–D) spiegano ≈ 70–80 % della varianza; sono legate a ++reti su larga scala++."),
    t("Sensitive to ++cognition, sleep, drugs, disease, stimulation++.", "Sensibili a ++cognizione, sonno, farmaci, malattia, stimolazione++.")], X0, Y0, CW, 0.85, 0.15, 17);
}

// 26 letture
{
  const s = content(t("Suggested reading", "Letture consigliate"), t("Suggested reading", "Letture consigliate"));
  text(s, [
    { t: "Michel C.M., Koenig T. (2018) EEG microstates as a tool for studying the temporal dynamics of whole-brain neuronal networks: a review. *NeuroImage* 180:577–593.", b: true },
    { t: "Lehmann D., Skrandies W. (1980) Reference-free identification of components of checkerboard-evoked multichannel potential fields. *Electroencephalogr Clin Neurophysiol* 48:609–621.", b: true },
    { t: "Lehmann D., Ozaki H., Pal I. (1987) EEG alpha map series: brain micro-states by space-oriented adaptive segmentation. *Electroencephalogr Clin Neurophysiol* 67:271–288.", b: true },
    { t: "Pascual-Marqui R.D., Michel C.M., Lehmann D. (1995) Segmentation of brain electrical activity into microstates. *IEEE Trans Biomed Eng* 42:658–665.", b: true },
    { t: "Murray M.M., Brunet D., Michel C.M. (2008) Topographic ERP analyses: a step-by-step tutorial review. *Brain Topogr* 20:249–264.", b: true },
    { t: "Koenig T. et al. (2002) Millisecond by millisecond, year by year: normative EEG microstates and developmental stages. *NeuroImage* 16:41–48.", b: true },
    { t: "Britz J., Van De Ville D., Michel C.M. (2010) BOLD correlates of EEG topography reveal rapid resting-state network dynamics. *NeuroImage* 52:1162–1170.", b: true },
    { t: "Van De Ville D., Britz J., Michel C.M. (2010) EEG microstate sequences in healthy humans at rest reveal scale-free dynamics. *PNAS* 107:18179–18184.", b: true },
    { t: "Custo A. et al. (2017) Electroencephalographic resting-state networks: source localization of microstates. *Brain Connect* 7:671–682.", b: true },
    { t: "Zappasodi F. et al. (2019) EEG microstates distinguish between cognitive components of fluid reasoning. *NeuroImage* 189:560–573.", b: true },
    { t: "Croce P., Zappasodi F., Capotosto P. (2018) Offline stimulation of human parietal cortex differently affects resting EEG microstates. *Sci Rep* 8:1287.", b: true },
    { t: "da Cruz J.R. et al. (2020) EEG microstates are a candidate endophenotype for schizophrenia. *Nat Commun* 11:3089.", b: true }], X0, Y0, CW, 5.2, { sz: 11, after: 4 });
}

save(OUT);
