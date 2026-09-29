// EEG – Lecture 4: recording (bilingue: node build_pptx4.js en|it)
const __R = (function () { const p = require("path"), fs = require("fs"); let d = process.env.COURSE_ROOT || __dirname;
  while (!fs.existsSync(p.join(d, ".course_root")) && p.dirname(d) !== d) d = p.dirname(d); return d; })();
const LANGARG = process.argv[2] || "en";
global.CFG = { lang: LANGARG, fig: __R + "/L4/figpng_" + LANGARG, common: __R + "/common",
  footer: LANGARG === "it" ? "Brain Imaging · EEG · Lezione 4 · Registrazione dell'EEG" : "Brain Imaging · EEG · Lecture 4 · Recording the EEG",
  lezione: LANGARG === "it" ? "Lezione 4" : "Lecture 4",
  titolo: LANGARG === "it" ? "Registrare l'EEG:\nelettrodi, segnali, artefatti" : "Recording the EEG:\nelectrodes, signals, artifacts", titoloSize: 42 };
const L = require(__R + "/common/pptlib_eeg.js");
const { tr: t, pres, fig, content, text, formula, card, badge, copertina, save } = L;
const { INK, ACC, TEAL, TXT, MUTED, TINT, WHITE, SERIF, SANS, W, H, MX, X0, Y0, CW } = L.C;
const OUT = process.argv[3] || `${__R}/L4/out/EEG_L4_${LANGARG}.pptx`;
const PEACH = "FDF0E9";
function note(s, str, x, y, w, h, sz = 17, fill = TINT) { card(s, x, y, w, h, fill); text(s, [str], x + 0.25, y + 0.05, w - 0.5, h - 0.1, { sz, valign: "middle", align: "center" }); }
function meta(s, str, x, y, w, h, sz = 17) { card(s, x, y, w, h, PEACH); text(s, [{ t: "~" + t("Metaphor", "Metafora") + "~  " + str }], x + 0.25, y + 0.05, w - 0.5, h - 0.1, { sz, valign: "middle" }); }
function section(n, en, it) { return L.sezione(n, t(en, it)); }
function rows(s, items, x, y, w, h, gap, sz = 18, colBadge = TEAL) {
  items.forEach((it, i) => { const yy = y + i * (h + gap); card(s, x, yy, w, h, i % 2 ? PEACH : TINT); badge(s, i + 1, x + 0.18, yy + h / 2 - 0.23, colBadge); text(s, [it], x + 0.85, yy, w - 1.05, h, { sz, valign: "middle" }); });
}
const B = (en, it) => ({ t: t(en, it), b: true });

copertina();

// 2 obiettivi
{
  const s = content(t("Lecture 4", "Lezione 4"), t("Today: from the scalp to a clean data file", "Oggi: dallo scalpo a un file di dati pulito"),
    { notes: t("This is the most practical lecture: many analysis problems are born at recording time and cannot be fixed afterwards.", "È la lezione più pratica: molti problemi di analisi nascono in registrazione e non si possono correggere dopo.") });
  rows(s, [t("The ++recording chain++: electrodes, amplifier, filters, ADC.", "La ++catena di registrazione++: elettrodi, amplificatore, filtri, ADC."),
    t("*Electrodes*, impedance and the ++10-20 system++.", "*Elettrodi*, impedenza e ++sistema 10-20++."),
    t("*Differential amplification*, CMRR and the ++reference++ problem.", "*Amplificazione differenziale*, CMRR e il problema del ++riferimento++."),
    t("*Digitisation*: sampling, Nyquist, aliasing, resolution, filters.", "*Digitalizzazione*: campionamento, Nyquist, aliasing, risoluzione, filtri."),
    t("*Artifacts* and a ++good-practice++ checklist.", "*Artefatti* e una checklist di ++buona pratica++.")], X0, Y0, CW, 0.85, 0.15, 18);
}

// 3 catena
{
  const s = content(t("The recording chain", "La catena di registrazione"), t("Five stages between the brain and your hard disk", "Cinque stadi tra il cervello e il disco"),
    { notes: t("Each stage can add noise or distortion; the EEG is only as good as its weakest link.", "Ogni stadio può aggiungere rumore o distorsione; l'EEG vale quanto il suo anello più debole.") });
  fig(s, "f03_chain", X0, Y0 + 0.2, CW, 1.9, "c", "Recording chain");
  text(s, [B("Signal of ++10–100 µV++ must be amplified ≈10⁴–10⁵ times without adding noise.", "Un segnale di ++10–100 µV++ va amplificato ≈10⁴–10⁵ volte senza aggiungere rumore."),
    B("Analog filters limit the band ++before++ sampling (anti-aliasing).", "I filtri analogici limitano la banda ++prima++ del campionamento (anti-aliasing)."),
    B("The ADC turns voltage into numbers: ++sampling rate++ and ++bit depth++.", "L'ADC trasforma la tensione in numeri: ++frequenza di campionamento++ e ++risoluzione in bit++."),
    B("Triggers from the stimulation PC mark events in the data (essential for ERPs).", "I trigger dal PC di stimolazione marcano gli eventi nei dati (essenziali per gli ERP).")], X0, 3.9, CW, 2.4, { sz: 17, after: 10 });
  meta(s, t("a ++hi-fi system++: a great speaker cannot fix a scratched record.", "un ++impianto hi-fi++: un ottimo altoparlante non ripara un disco graffiato."), X0, 6.2, CW, 0.55, 15);
}

section(1, "Electrodes and montage", "Elettrodi e montaggio");

// 5 tipi elettrodi
{
  const s = content(t("Electrodes (1)", "Elettrodi (1)"), t("Types of electrodes", "Tipi di elettrodi"),
    { notes: t("Ag/AgCl is non-polarisable: stable half-cell potential, good for low frequencies. Dry electrodes: higher impedance, more motion artifacts.", "Ag/AgCl è non polarizzabile: potenziale di semicella stabile, buono per le basse frequenze. Elettrodi a secco: impedenza più alta, più artefatti da movimento.") });
  const e = [[t("Wet (gel) Ag/AgCl", "Umidi (gel) Ag/AgCl"), t("gold standard; stable, non-polarisable; low impedance; slow set-up", "gold standard; stabili, non polarizzabili; bassa impedenza; montaggio lento")],
    [t("Saline / sponge", "Salini / spugna"), t("fast set-up (HydroCel); dry out in ≈1 h", "montaggio rapido (HydroCel); si asciugano in ≈1 h")],
    [t("Dry", "A secco"), t("no gel, wearable/BCI; higher impedance, motion-sensitive", "senza gel, indossabili/BCI; impedenza più alta, sensibili al movimento")],
    [t("Active", "Attivi"), t("pre-amplifier at the electrode: less cable noise, tolerate higher impedance", "pre-amplificatore sull'elettrodo: meno rumore dai cavi, tollerano impedenze più alte")]];
  e.forEach(([h, d], i) => {
    const x = X0 + (i % 2) * (CW / 2 + 0.15), y = Y0 + Math.floor(i / 2) * 1.75, w = CW / 2 - 0.15;
    card(s, x, y, w, 1.55, i % 3 ? PEACH : TINT);
    text(s, [{ t: "~" + h + "~" }, { t: d }], x + 0.25, y + 0.1, w - 0.5, 1.35, { sz: 17, after: 6 });
  });
  note(s, t("The electrode–gel–skin interface is an ++electrochemical junction++: it generates a DC potential that drifts with sweat and movement.", "L'interfaccia elettrodo–gel–pelle è una ++giunzione elettrochimica++: genera un potenziale continuo che deriva con sudore e movimento."), X0, 5.4, CW, 0.9, 16);
}

// 6 impedenza
{
  const s = content(t("Electrodes (2)", "Elettrodi (2)"), t("Impedance: keep it low and balanced", "Impedenza: bassa e bilanciata"),
    { notes: t("Kappenman & Luck (2010) Psychophysiology 47:888: high impedance increases low-frequency noise, especially in warm/humid conditions; effects on statistical power.", "Kappenman & Luck (2010) Psychophysiology 47:888: l'alta impedenza aumenta il rumore a bassa frequenza, soprattutto in condizioni calde/umide; effetti sulla potenza statistica.") });
  text(s, [B("*Impedance* (Ω) = opposition of the electrode–skin junction to alternating current.", "*Impedenza* (Ω) = opposizione della giunzione elettrodo–pelle alla corrente alternata."),
    B("Typical targets: ++< 5–10 kΩ++ for passive electrodes; active systems tolerate ++< 25–50 kΩ++.", "Obiettivi tipici: ++< 5–10 kΩ++ per elettrodi passivi; i sistemi attivi tollerano ++< 25–50 kΩ++."),
    B("High impedance → more ++skin potentials++, ++line noise++ and ++low-frequency drifts++ → lower statistical power (Kappenman & Luck, 2010).", "Alta impedenza → più ++potenziali cutanei++, ++rumore di rete++ e ++derive lente++ → minore potenza statistica (Kappenman & Luck, 2010)."),
    B("~Balanced~ impedances between active and reference improve common-mode rejection.", "Impedenze ~bilanciate~ tra attivo e riferimento migliorano la reiezione di modo comune."),
    B("Skin preparation: gentle abrasion, alcohol, enough gel — but no bridges between electrodes!", "Preparazione della pelle: leggera abrasione, alcol, gel sufficiente — ma nessun ponte tra elettrodi!")], X0, Y0, CW, 4.2, { sz: 18, after: 12 });
  meta(s, t("the gel is a ++bridge++ between skin and metal: too little and the road is bumpy, too much and it floods into the neighbour's road (salt bridge).", "il gel è un ++ponte++ tra pelle e metallo: troppo poco e la strada è dissestata, troppo e allaga la strada del vicino (ponte salino)."), X0, 5.6, CW, 0.9, 16);
}

// 7 10-20
{
  const s = content(t("Electrodes (3)", "Elettrodi (3)"), t("The international 10-20 system", "Il sistema internazionale 10-20"),
    { notes: t("Jasper (1958) Electroenceph Clin Neurophysiol 10:371. Distances are 10% and 20% of nasion–inion and preauricular distances → comparable positions across head sizes.", "Jasper (1958) Electroenceph Clin Neurophysiol 10:371. Distanze del 10% e 20% di nasion–inion e distanze preauricolari → posizioni confrontabili tra teste diverse.") });
  fig(s, "f06_1020", X0, Y0, 8.0, 4.8, "l", "10-20 system");
  text(s, [B("Positions at ++10 % and 20 %++ of the nasion–inion and ear-to-ear distances: ~relative~, so they adapt to every head.", "Posizioni al ++10 % e 20 %++ delle distanze nasion–inion e tra le orecchie: ~relative~, quindi si adattano a ogni testa."),
    B("Letters = region: *Fp* frontopolar, *F* frontal, *C* central, *T* temporal, *P* parietal, *O* occipital.", "Lettere = regione: *Fp* frontopolare, *F* frontale, *C* centrale, *T* temporale, *P* parietale, *O* occipitale."),
    B("Numbers: odd = left, even = right, *z* = midline.", "Numeri: dispari = sinistra, pari = destra, *z* = linea mediana.")], 8.6, Y0 + 0.1, 4.1, 4.8, { sz: 16, after: 12 });
}

// 8 alta densità
{
  const s = content(t("Electrodes (4)", "Elettrodi (4)"), t("How many electrodes? 10-10, 10-5 and high density", "Quanti elettrodi? 10-10, 10-5 e alta densità"),
    { notes: t("Oostenveld & Praamstra (2001) Clin Neurophysiol 112:713 (10-5 system). Srinivasan et al. (1998): ~2–3 cm spacing needed to sample scalp potentials without spatial aliasing.", "Oostenveld & Praamstra (2001) Clin Neurophysiol 112:713 (sistema 10-5). Srinivasan et al. (1998): serve una spaziatura di ~2–3 cm per non avere aliasing spaziale.") });
  const c = [["19–21", t("clinical 10-20: epilepsy, sleep", "10-20 clinico: epilessia, sonno")], ["32–64", t("10-10: most cognitive studies, ERPs", "10-10: la maggior parte degli studi cognitivi, ERP")],
    ["128–256", t("high density (10-5, geodesic): source imaging, microstates", "alta densità (10-5, geodetico): source imaging, microstati")], ["1–8", t("wearable, BCI, sleep headbands", "indossabili, BCI, fasce per il sonno")]];
  c.forEach(([n, d], i) => {
    const x = X0 + i * (CW / 4 + 0.03), w = CW / 4 - 0.2;
    card(s, x, Y0, w, 2.3, i % 2 ? PEACH : TINT);
    s.addText(n, { x, y: Y0 + 0.15, w, h: 0.8, fontFace: SERIF, fontSize: 30, bold: true, color: i % 2 ? ACC : TEAL, align: "center", margin: 0, isTextBox: true });
    text(s, [{ t: d, align: "center" }], x + 0.15, Y0 + 1.0, w - 0.3, 1.2, { sz: 15 });
  });
  text(s, [B("More electrodes = better ++spatial sampling++: scalp potentials vary over ≈2–3 cm, so ≥ 64–128 channels are needed for good topographies and source imaging.", "Più elettrodi = migliore ++campionamento spaziale++: i potenziali di scalpo variano su ≈2–3 cm, quindi servono ≥ 64–128 canali per buone topografie e source imaging."),
    B("But: longer set-up, more bad channels, more gel bridges. ~Choose the montage from the question.~", "Ma: montaggio più lungo, più canali cattivi, più ponti di gel. ~Scegliere il montaggio in base alla domanda.~")], X0, 4.35, CW, 2.2, { sz: 17, after: 10 });
}

section(2, "Amplification and reference", "Amplificazione e riferimento");

// 10 amplificatore differenziale
{
  const s = content(t("Amplifier (1)", "Amplificatore (1)"), t("Differential amplification and common-mode rejection", "Amplificazione differenziale e reiezione di modo comune"),
    { notes: t("Mains interference couples capacitively to the body and appears almost identically on all electrodes (common mode). A driven-right-leg / ground electrode helps.", "Il disturbo di rete si accoppia capacitivamente al corpo e compare quasi identico su tutti gli elettrodi (modo comune). L'elettrodo di terra / driven-right-leg aiuta.") });
  fig(s, "f08_diffamp", X0, Y0, CW, 2.9, "c", "Differential amplifier");
  text(s, [B("The amplifier outputs ++active − reference++: what is ++common++ to both inputs (mains, body potential) cancels.", "L'amplificatore restituisce ++attivo − riferimento++: ciò che è ++comune++ ai due ingressi (rete, potenziale del corpo) si annulla."),
    B("*CMRR*: how well common signals are rejected (≥ 100 dB = 100 000×). Unbalanced impedances degrade it.", "*CMRR*: quanto bene si respingono i segnali comuni (≥ 100 dB = 100 000×). Impedenze sbilanciate lo peggiorano."),
    B("A separate *ground* electrode (or driven right leg) sets the amplifier's operating point.", "Un elettrodo di *terra* separato (o driven right leg) fissa il punto di lavoro dell'amplificatore.")], X0, 4.75, CW, 1.4, { sz: 15, after: 6 });
  meta(s, t("++noise-cancelling headphones++: they record the ambient noise and subtract it.", "le ++cuffie a cancellazione di rumore++: registrano il rumore ambientale e lo sottraggono."), X0, 6.2, CW, 0.55, 15);
}

// 11 riferimento
{
  const s = content(t("Reference (1)", "Riferimento (1)"), t("There is no neutral reference", "Non esiste un riferimento neutro"),
    { notes: t("Yao (2001) Physiol Meas 22:693 (REST); Dien (1998) Behav Res Methods (average reference); Nunez & Srinivasan (2006).", "Yao (2001) Physiol Meas 22:693 (REST); Dien (1998) Behav Res Methods (riferimento medio); Nunez & Srinivasan (2006).") });
  const r = [[t("Vertex (Cz)", "Vertice (Cz)"), t("common in recording; kills activity at Cz", "comune in registrazione; azzera l'attività in Cz")],
    [t("Linked mastoids / ears", "Mastoidi / orecchie collegate"), t("classic for ERPs; mastoids are not silent (temporal activity)", "classico per gli ERP; le mastoidi non sono silenziose (attività temporale)")],
    [t("Nose / chin", "Naso / mento"), t("far from cortex but prone to muscle and eye artifacts", "lontano dalla corteccia ma soggetto ad artefatti muscolari e oculari")],
    [t("Average reference", "Riferimento medio"), t("mean of all channels: good with ≥ 64 evenly spread electrodes", "media di tutti i canali: buono con ≥ 64 elettrodi ben distribuiti")],
    [t("REST (infinity reference)", "REST (riferimento all'infinito)"), t("model-based estimate of a reference at infinity (Yao, 2001)", "stima basata su modello di un riferimento all'infinito (Yao, 2001)")]];
  r.forEach(([h, d], i) => {
    const y = Y0 + i * 0.86;
    card(s, X0, y, CW, 0.74, i % 2 ? PEACH : TINT);
    s.addText(h, { x: X0 + 0.2, y, w: 3.6, h: 0.74, fontFace: SANS, fontSize: 17, bold: true, color: TEAL, valign: "middle", margin: 0, isTextBox: true });
    text(s, [d], X0 + 3.9, y, CW - 4.1, 0.74, { sz: 16, valign: "middle" });
  });
  note(s, t("Re-referencing is ++linear++ and can be done offline: V_{new}(ch) = V(ch) − V_{new ref}. ~Always report the reference.~", "La ri-referenziazione è ++lineare++ e si fa offline: V_{nuovo}(ch) = V(ch) − V_{nuovo rif}. ~Riportare sempre il riferimento.~"), X0, 6.15, CW, 0.65, 16);
}

section(3, "Digitisation and filtering", "Digitalizzazione e filtraggio");

// 13 campionamento / aliasing
{
  const s = content(t("Digitisation (1)", "Digitalizzazione (1)"), t("Sampling, Nyquist and aliasing", "Campionamento, Nyquist e aliasing"),
    { notes: t("Nyquist–Shannon: a signal can be reconstructed if sampled at more than twice its highest frequency. Anti-aliasing low-pass must act BEFORE the ADC.", "Nyquist–Shannon: un segnale si ricostruisce se campionato a più del doppio della sua frequenza massima. Il passa-basso anti-aliasing deve agire PRIMA dell'ADC.") });
  fig(s, "f11_alias", X0, Y0, CW, 2.7, "c", "Aliasing");
  formula(s, "$f$_s > 2 · $f$_{max}      ( $f$_{Nyquist} = $f$_s / 2 )", X0 + 3.0, 4.55, CW - 6.0, 0.7, { sz: 22, fill: PEACH });
  text(s, [B("Frequencies above f_{s}/2 do not disappear: they ++fold back++ as fake low frequencies (*aliasing*).", "Le frequenze sopra f_{s}/2 non spariscono: si ++ripiegano++ come false basse frequenze (*aliasing*)."),
    B("Typical EEG: f_{s} = 250–1000 Hz (higher for high-gamma or brainstem responses).", "EEG tipico: f_{s} = 250–1000 Hz (di più per high-gamma o risposte del tronco).")], X0, 5.3, CW, 0.9, { sz: 15, after: 4 });
  meta(s, t("the ++wagon-wheel effect++ in films: a fast wheel seems to turn slowly backwards.", "l'++effetto ruota di carro++ nei film: una ruota veloce sembra girare lenta all'indietro."), X0, 6.25, CW, 0.5, 14);
}

// 14 risoluzione ADC
{
  const s = content(t("Digitisation (2)", "Digitalizzazione (2)"), t("Amplitude resolution and dynamic range", "Risoluzione in ampiezza e dinamica"),
    { notes: t("24-bit DC-coupled amplifiers (e.g. ±400 mV range) have LSB ≈ 0.05 µV; 16-bit older systems needed high-pass filtering in hardware.", "Gli amplificatori DC a 24 bit (es. range ±400 mV) hanno LSB ≈ 0,05 µV; i vecchi sistemi a 16 bit richiedevano un passa-alto hardware.") });
  formula(s, "LSB = range / 2^{bits}", X0 + 3.8, Y0, CW - 7.6, 0.75, { sz: 26, fill: PEACH });
  const c = [["16 bit", "65 536", t("±3 mV → ≈0.1 µV", "±3 mV → ≈0,1 µV")], ["24 bit", "16 777 216", t("±400 mV → ≈0.05 µV", "±400 mV → ≈0,05 µV")]];
  c.forEach(([b, n, d], i) => {
    const x = X0 + 1.5 + i * 5.3;
    card(s, x, 2.75, 4.5, 1.6, i ? PEACH : TINT);
    text(s, [{ t: "**" + b + "**  · " + n + t(" levels", " livelli"), align: "center" }, { t: d, align: "center", c: TEAL }], x, 2.9, 4.5, 1.4, { sz: 18, after: 6 });
  });
  text(s, [B("The range must contain large ++DC offsets++ and artifacts without *clipping* (saturation).", "Il range deve contenere grandi ++offset DC++ e artefatti senza *clipping* (saturazione)."),
    B("Modern 24-bit amplifiers record ++DC-coupled++: slow potentials are preserved, drifts are removed offline.", "I moderni amplificatori a 24 bit registrano in ++DC++: i potenziali lenti si conservano, le derive si tolgono offline."),
    B("Resolution ≪ noise floor (≈0.5–1 µV): bits are rarely the bottleneck today.", "Risoluzione ≪ rumore di fondo (≈0,5–1 µV): oggi i bit raramente sono il collo di bottiglia.")], X0, 4.65, CW, 2.0, { sz: 17, after: 10 });
}

// 15 filtri
{
  const s = content(t("Digitisation (3)", "Digitalizzazione (3)"), t("Filters: useful but dangerous", "Filtri: utili ma pericolosi"),
    { notes: t("Widmann, Schröger & Maess (2015) J Neurosci Methods 250:34; Acunzo et al. (2012) J Neurosci Methods 209:212; Tanner et al. (2015) Psychophysiology 52:997 (high-pass > 0.1 Hz distorts ERPs).", "Widmann, Schröger & Maess (2015) J Neurosci Methods 250:34; Acunzo et al. (2012) J Neurosci Methods 209:212; Tanner et al. (2015) Psychophysiology 52:997 (passa-alto > 0,1 Hz distorce gli ERP).") });
  fig(s, "f13_filters", X0, Y0, 6.4, 4.1, "l", "Filter responses");
  text(s, [B("*High-pass* (0.01–1 Hz): removes drifts. Too high (> 0.1–0.3 Hz) ++distorts slow ERPs++ and creates artificial peaks.", "*Passa-alto* (0,01–1 Hz): rimuove le derive. Troppo alto (> 0,1–0,3 Hz) ++distorce gli ERP lenti++ e crea picchi artificiali."),
    B("*Low-pass* (30–100 Hz): removes muscle noise; always one before the ADC (anti-alias).", "*Passa-basso* (30–100 Hz): rimuove il rumore muscolare; sempre uno prima dell'ADC (anti-alias)."),
    B("*Notch* (50 Hz in Europe, 60 Hz in the Americas): removes line noise, but ++rings++ in time.", "*Notch* (50 Hz in Europa, 60 Hz nelle Americhe): rimuove la rete, ma ++oscilla++ nel tempo."),
    B("~Rule~: record wide-band, filter offline, report filter type, order and cut-off.", "~Regola~: registrare a banda larga, filtrare offline, riportare tipo, ordine e frequenza di taglio.")], 7.2, Y0 + 0.1, 5.5, 5.0, { sz: 15, after: 10 });
  meta(s, t("a filter is a ++sieve++: choose holes that keep the flour, not the stones — and be aware it also changes the texture.", "un filtro è un ++setaccio++: scegli i fori che tengono la farina, non i sassi — sapendo che cambia anche la consistenza."), X0, 5.8, 6.4, 0.85, 15);
}

section(4, "Artifacts", "Artefatti");

// 17 panoramica artefatti
{
  const s = content(t("Artifacts (1)", "Artefatti (1)"), t("A gallery of artifacts", "Una galleria di artefatti"),
    { notes: t("Simulated examples. Physiological: ocular, muscular, cardiac, sweat, movement. Non-physiological: line noise, electrode pop, cable movement.", "Esempi simulati. Fisiologici: oculari, muscolari, cardiaci, sudore, movimento. Non fisiologici: rete, pop dell'elettrodo, movimento dei cavi.") });
  fig(s, "f15_artifacts", X0, Y0, 7.3, 5.0, "l", "Artifacts");
  const a = [[t("Eye blinks", "Ammiccamenti"), t("frontal, 100–200 µV, 200–400 ms", "frontali, 100–200 µV, 200–400 ms")], [t("Saccades", "Saccadi"), t("box-shaped, opposite polarity at F7/F8", "a gradino, polarità opposta in F7/F8")],
    [t("Muscle (EMG)", "Muscolo (EMG)"), t("temporal/frontal, broadband > 20 Hz", "temporali/frontali, banda larga > 20 Hz")], ["ECG", t("regular sharp peaks ≈1 Hz", "picchi regolari ≈1 Hz")],
    [t("Line noise", "Rete elettrica"), t("50/60 Hz sinusoid + harmonics", "sinusoide 50/60 Hz + armoniche")], [t("Electrode pop", "Pop dell'elettrodo"), t("sudden step on one channel", "gradino improvviso su un canale")]];
  a.forEach(([h, d], i) => {
    const y = Y0 + i * 0.84;
    card(s, 8.1, y, 4.6, 0.74, i % 2 ? PEACH : TINT);
    text(s, [{ t: "~" + h + "~: " + d }], 8.3, y, 4.3, 0.74, { sz: 14, valign: "middle" });
  });
}

// 18 occhi e muscoli
{
  const s = content(t("Artifacts (2)", "Artefatti (2)"), t("Eyes and muscles: the biggest offenders", "Occhi e muscoli: i principali colpevoli"),
    { notes: t("The eye is a dipole (cornea +, retina −): Berg & Scherg (1991). Microsaccade spike potentials mimic induced gamma: Yuval-Greenberg et al. (2008) Neuron 58:429.", "L'occhio è un dipolo (cornea +, retina −): Berg & Scherg (1991). I potenziali di spike delle microsaccadi imitano la gamma indotta: Yuval-Greenberg et al. (2008) Neuron 58:429.") });
  const cw = (CW - 0.4) / 2;
  card(s, X0, Y0, cw, 4.2, TINT);
  text(s, [{ t: "~" + t("Ocular", "Oculari") + "~", align: "center" },
    B("The eye is a ++dipole++ (cornea +, retina −): rotations and eyelid movements change the scalp field.", "L'occhio è un ++dipolo++ (cornea +, retina −): rotazioni e movimenti palpebrali cambiano il campo sullo scalpo."),
    B("Blinks: large frontal positivity. Horizontal saccades: opposite steps at F7/F8.", "Ammiccamenti: grande positività frontale. Saccadi orizzontali: gradini opposti in F7/F8."),
    B("Record ++EOG++ (above/below and beside the eyes) to identify them.", "Registrare l'++EOG++ (sopra/sotto e ai lati degli occhi) per identificarli.")], X0 + 0.25, Y0 + 0.1, cw - 0.5, 4.0, { sz: 15, after: 10 });
  card(s, X0 + cw + 0.4, Y0, cw, 4.2, PEACH);
  text(s, [{ t: "~" + t("Muscular", "Muscolari") + "~", align: "center" },
    B("Jaw, forehead, neck muscles: broadband, maximal at ++temporal++ sites and > 20 Hz.", "Mandibola, fronte, collo: banda larga, massimo nelle sedi ++temporali++ e > 20 Hz."),
    B("It overlaps with ++beta and gamma++: \"gamma\" effects may be muscle.", "Si sovrappone a ++beta e gamma++: effetti \"gamma\" possono essere muscolari."),
    B("⚠ Microsaccades produce a spike potential that mimics ++induced gamma++ (Yuval-Greenberg et al., 2008).", "⚠ Le microsaccadi producono uno spike potential che imita la ++gamma indotta++ (Yuval-Greenberg et al., 2008).")], X0 + cw + 0.65, Y0 + 0.1, cw - 0.5, 4.0, { sz: 15, after: 10 });
  note(s, t("Prevention beats correction: fixation cross, relaxed posture, breaks, instructions (\"blink between trials\").", "Prevenire è meglio che correggere: croce di fissazione, postura rilassata, pause, istruzioni (\"ammicca tra un trial e l'altro\")."), X0, 6.0, CW, 0.7, 16);
}

// 19 rete elettrica
{
  const s = content(t("Artifacts (3)", "Artefatti (3)"), t("Line noise and its harmonics", "Rumore di rete e armoniche"),
    { notes: t("Simulated spectrum with 50 Hz and 100 Hz components. Alternatives to notch: CleanLine / Zapline (de Cheveigné 2020 NeuroImage 207:116356).", "Spettro simulato con componenti a 50 e 100 Hz. Alternative al notch: CleanLine / Zapline (de Cheveigné 2020 NeuroImage 207:116356).") });
  fig(s, "f18_linenoise", X0, Y0, 6.0, 4.8, "l", "Line noise spectrum");
  text(s, [B("Mains (50 Hz in Europe) couples into cables and the body; it is worse with ++high or unbalanced impedance++.", "La rete (50 Hz in Europa) si accoppia a cavi e corpo; peggiora con impedenze ++alte o sbilanciate++."),
    B("Sources: lamps, monitors, power supplies, other devices; keep cables short and away from power lines.", "Sorgenti: lampade, monitor, alimentatori, altri dispositivi; cavi corti e lontani dalla rete."),
    B("Removal: notch filter, ++spectrum interpolation++, CleanLine, ++Zapline++ (less distortion).", "Rimozione: filtro notch, ++interpolazione spettrale++, CleanLine, ++Zapline++ (meno distorsione)."),
    B("A 50 Hz peak ≫ neighbours = check that channel's electrode!", "Un picco a 50 Hz ≫ vicini = controllare l'elettrodo di quel canale!")], 6.9, Y0 + 0.1, 5.8, 5.0, { sz: 16, after: 12 });
}

section(5, "Good recording practice", "Buona pratica di registrazione");

// 21 checklist
{
  const s = content(t("Good practice (1)", "Buona pratica (1)"), t("A recording checklist", "Una checklist di registrazione"),
    { notes: t("Keil et al. (2014) Psychophysiology 51:1: committee report on publication guidelines for EEG/MEG studies.", "Keil et al. (2014) Psychophysiology 51:1: rapporto sulle linee guida di pubblicazione per studi EEG/MEG.") });
  const items = [t("Quiet, dimly lit, electrically clean room; participant comfortable and informed.", "Stanza silenziosa, poco illuminata, elettricamente pulita; partecipante comodo e informato."),
    t("Measure head size, cap well centred (Cz at the vertex), impedances logged.", "Misurare la testa, cuffia ben centrata (Cz al vertice), impedenze annotate."),
    t("Check raw data on screen: blinks, jaw clench, eyes closed → alpha (a quick ++\"sanity test\"++).", "Controllare i dati grezzi a schermo: ammiccamenti, serrare la mandibola, occhi chiusi → alfa (un rapido ++\"test di sanità\"++)."),
    t("Resting blocks (eyes open/closed) before tasks; breaks to reduce fatigue and drowsiness.", "Blocchi di riposo (occhi aperti/chiusi) prima dei compiti; pause per ridurre fatica e sonnolenza."),
    t("Triggers tested with a ++photodiode++: measure the real stimulus–trigger delay.", "Trigger testati con un ++fotodiodo++: misurare il ritardo reale stimolo–trigger."),
    t("Lab notebook: bad channels, events, anything unusual (sneezes, talking, movement).", "Diario di laboratorio: canali cattivi, eventi, tutto ciò che è insolito (starnuti, parlato, movimenti).")];
  rows(s, items, X0, Y0, CW, 0.72, 0.12, 16, ACC);
}

// 22 dati e BIDS
{
  const s = content(t("Good practice (2)", "Buona pratica (2)"), t("Data formats and sharing: EEG-BIDS", "Formati e condivisione: EEG-BIDS"),
    { notes: t("Pernet et al. (2019) Sci Data 6:103. Formats accepted: EDF, BDF, BrainVision, EEGLAB .set.", "Pernet et al. (2019) Sci Data 6:103. Formati accettati: EDF, BDF, BrainVision, EEGLAB .set.") });
  text(s, [B("Vendor formats vary (BrainVision, BDF, EDF, EGI, CNT…): always keep the ++raw++ files.", "I formati dei produttori variano (BrainVision, BDF, EDF, EGI, CNT…): conservare sempre i file ++grezzi++."),
    B("*EEG-BIDS* (Pernet et al., 2019) organises data and metadata in a standard folder structure: subject/session/task, electrodes, channels, events, sidecar JSON.", "*EEG-BIDS* (Pernet et al., 2019) organizza dati e metadati in una struttura standard: soggetto/sessione/compito, elettrodi, canali, eventi, JSON di accompagnamento."),
    B("Benefits: ++reproducibility++, automatic pipelines, sharing on OpenNeuro.", "Vantaggi: ++riproducibilità++, pipeline automatiche, condivisione su OpenNeuro."),
    B("Tools: MNE-BIDS (Python), bids-matlab-tools / EEGLAB plug-in.", "Strumenti: MNE-BIDS (Python), bids-matlab-tools / plug-in EEGLAB.")], X0, Y0, 7.0, 4.8, { sz: 17, after: 12 });
  card(s, 8.0, Y0, 4.7, 4.6, TINT);
  text(s, [{ t: "sub-01/", c: TEAL }, { t: "  eeg/" }, { t: "    sub-01_task-oddball_eeg.vhdr" }, { t: "    sub-01_task-oddball_eeg.json" }, { t: "    sub-01_task-oddball_channels.tsv" },
    { t: "    sub-01_task-oddball_events.tsv" }, { t: "    sub-01_electrodes.tsv" }, { t: "dataset_description.json", c: TEAL }, { t: "participants.tsv", c: TEAL }], 8.2, Y0 + 0.2, 4.4, 4.3, { raw: true, sz: 13, face: "Consolas", after: 2 });
}

// 23 domande
{
  const s = content(t("Check your understanding", "Verifica"), t("Three questions", "Tre domande"),
    { notes: t("(1) Aliasing: 60 Hz sampled at 100 Hz → 40 Hz; must low-pass before ADC. (2) Common-mode: 50 Hz on both inputs cancels only if impedances are balanced. (3) Muscle or microsaccades.", "(1) Aliasing: 60 Hz campionati a 100 Hz → 40 Hz; serve il passa-basso prima dell'ADC. (2) Modo comune: il 50 Hz si annulla solo con impedenze bilanciate. (3) Muscolo o microsaccadi.") });
  rows(s, [t("You sample at 100 Hz without anti-aliasing and there is 60 Hz noise. What appears in your data?", "Campioni a 100 Hz senza anti-aliasing e c'è rumore a 60 Hz. Che cosa compare nei dati?"),
    t("Why does 50 Hz noise increase when one electrode has much higher impedance than the others?", "Perché il rumore a 50 Hz aumenta quando un elettrodo ha un'impedenza molto più alta degli altri?"),
    t("You find a gamma increase at T7/T8 during a difficult task. Name two non-neural explanations.", "Trovi un aumento di gamma in T7/T8 durante un compito difficile. Indica due spiegazioni non neurali.")], X0, Y0 + 0.2, CW, 1.2, 0.35, 18, ACC);
}

// 24 take home
{
  const s = content(t("Take-home messages", "Messaggi chiave"), t("Take-home messages", "Messaggi chiave"));
  rows(s, [t("Good data are made at ++recording time++: impedance, montage, environment.", "I buoni dati si fanno ++in registrazione++: impedenza, montaggio, ambiente."),
    t("10-20 (and 10-10/10-5) give ++standard, relative++ positions.", "Il 10-20 (e 10-10/10-5) fornisce posizioni ++standard e relative++."),
    t("Differential amplifiers reject ++common-mode++ noise; there is ++no neutral reference++.", "Gli amplificatori differenziali respingono il rumore di ++modo comune++; ++non esiste un riferimento neutro++."),
    t("f_{s} > 2 f_{max} (++Nyquist++); filters help but ++distort++: report them.", "f_{s} > 2 f_{max} (++Nyquist++); i filtri aiutano ma ++distorcono++: riportarli."),
    t("Know your ++artifacts++ (eyes, muscles, heart, mains) and store data in ++BIDS++.", "Conoscere gli ++artefatti++ (occhi, muscoli, cuore, rete) e salvare i dati in ++BIDS++.")], X0, Y0, CW, 0.85, 0.15, 17);
}

// 25 letture
{
  const s = content(t("Suggested reading", "Letture consigliate"), t("Suggested reading", "Letture consigliate"));
  text(s, [
    { t: "Luck S.J. (2014) *An Introduction to the Event-Related Potential Technique*, 2nd ed. MIT Press — ch. 5 (recording) and 7 (filtering).", b: true },
    { t: "Jasper H.H. (1958) The ten-twenty electrode system of the International Federation. *Electroencephalogr Clin Neurophysiol* 10:371–375.", b: true },
    { t: "Oostenveld R., Praamstra P. (2001) The five percent electrode system for high-resolution EEG and ERP measurements. *Clin Neurophysiol* 112:713–719.", b: true },
    { t: "Kappenman E.S., Luck S.J. (2010) The effects of electrode impedance on data quality and statistical significance in ERP recordings. *Psychophysiology* 47:888–904.", b: true },
    { t: "Yao D. (2001) A method to standardize a reference of scalp EEG recordings to a point at infinity. *Physiol Meas* 22:693–711.", b: true },
    { t: "Widmann A., Schröger E., Maess B. (2015) Digital filter design for electrophysiological data – a practical approach. *J Neurosci Methods* 250:34–46.", b: true },
    { t: "Yuval-Greenberg S. et al. (2008) Transient induced gamma-band response in EEG as a manifestation of miniature saccades. *Neuron* 58:429–441.", b: true },
    { t: "Keil A. et al. (2014) Committee report: publication guidelines and recommendations for studies using EEG and MEG. *Psychophysiology* 51:1–21.", b: true },
    { t: "Pernet C.R. et al. (2019) EEG-BIDS, an extension to the brain imaging data structure for electroencephalography. *Sci Data* 6:103.", b: true }], X0, Y0, CW, 5.1, { sz: 13, after: 6 });
}

save(OUT);
