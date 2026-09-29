// EEG – Lecture 3: from neurons to scalp (bilingue: node build_pptx3.js en|it)
const __R = (function () { const p = require("path"), fs = require("fs"); let d = process.env.COURSE_ROOT || __dirname;
  while (!fs.existsSync(p.join(d, ".course_root")) && p.dirname(d) !== d) d = p.dirname(d); return d; })();
const LANGARG = process.argv[2] || "en";
global.CFG = { lang: LANGARG, fig: __R + "/L3/figpng_" + LANGARG, common: __R + "/common",
  footer: LANGARG === "it" ? "Brain Imaging · EEG · Lezione 3 · Dai neuroni allo scalpo" : "Brain Imaging · EEG · Lecture 3 · From neurons to scalp",
  lezione: LANGARG === "it" ? "Lezione 3" : "Lecture 3",
  titolo: LANGARG === "it" ? "Dai neuroni allo scalpo:\ndipoli, conduzione, ritmi" : "From neurons to scalp:\ndipoles, conduction, rhythms", titoloSize: 40 };
const L = require(__R + "/common/pptlib_eeg.js");
const { tr: t, pres, fig, content, text, formula, card, badge, copertina, save } = L;
const { INK, ACC, TEAL, TXT, MUTED, TINT, WHITE, SERIF, SANS, W, H, MX, X0, Y0, CW } = L.C;
const OUT = process.argv[3] || `${__R}/L3/out/EEG_L3_${LANGARG}.pptx`;
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
  const s = content(t("Lecture 3", "Lezione 3"), t("Today: from cells to the scalp signal", "Oggi: dalle cellule al segnale di scalpo"),
    { notes: t("Link: Lecture 2 explained single-cell currents; now we scale up to populations, the head as a conductor, and rhythms.", "Collegamento: la Lezione 2 ha spiegato le correnti della singola cellula; ora passiamo alle popolazioni, alla testa come conduttore e ai ritmi.") });
  rows(s, [t("The ++scales++ of brain electrical activity: spikes, LFP, EEG.", "Le ++scale++ dell'attività elettrica cerebrale: spike, LFP, EEG."),
    t("The *current dipole* as the building block of scalp maps.", "Il *dipolo di corrente* come mattone delle mappe di scalpo."),
    t("*Volume conduction*: head tissues, conductivities, lead field.", "*Conduzione di volume*: tessuti della testa, conducibilità, lead field."),
    t("How ++montages++ and ++references++ change what we see.", "Come ++montaggi++ e ++riferimenti++ cambiano ciò che vediamo."),
    t("The *EEG rhythms*: spectrum, bands, topography, vigilance and sleep.", "I *ritmi EEG*: spettro, bande, topografia, vigilanza e sonno.")], X0, Y0, CW, 0.85, 0.15, 18);
}

section(1, "Scales of brain electrical activity", "Le scale dell'attività elettrica cerebrale");

// 4 scale
{
  const s = content(t("Scales (1)", "Scale (1)"), t("Micro, meso, macro: three windows on the same activity", "Micro, meso, macro: tre finestre sulla stessa attività"),
    { notes: t("Adapted from Varela et al. (2001) Nat Rev Neurosci 2:229 and Le Van Quyen (2011) New Ideas Psychol 29:57.", "Adattato da Varela et al. (2001) Nat Rev Neurosci 2:229 e Le Van Quyen (2011) New Ideas Psychol 29:57.") });
  fig(s, "f04_scales", X0, Y0, CW, 2.6, "c", "Scales");
  text(s, [B("*Spikes* (single/multi-unit): output of individual neurons, µm–100 µm, ~1 ms.", "*Spike* (singola/multi-unità): output di singoli neuroni, µm–100 µm, ~1 ms."),
    B("*Local field potential (LFP)*: summed synaptic input of a local network (≈0.1–1 mm).", "*Potenziale di campo locale (LFP)*: input sinaptico sommato di una rete locale (≈0.1–1 mm)."),
    B("*EEG*: the LFPs of ++centimetres++ of cortex, filtered by the head. Each level loses detail but gains overview.", "*EEG*: gli LFP di ++centimetri++ di corteccia, filtrati dalla testa. Ogni livello perde dettaglio ma guadagna visione d'insieme.")], X0, 4.5, CW, 2.2, { sz: 17, after: 10 });
}

// 5 sincronia
{
  const s = content(t("Scales (2)", "Scale (2)"), t("Neural synchronisation makes the EEG visible", "La sincronizzazione neurale rende visibile l'EEG"),
    { notes: t("8 simulated oscillators at 8 Hz: random phases vs identical phases.", "8 oscillatori simulati a 8 Hz: fasi casuali vs fasi identiche.") });
  fig(s, "f05_sync", X0, Y0, 8.0, 4.7, "l", "Synchronisation");
  text(s, [B("Same neurons, same activity, same energy: only the ++timing++ differs.", "Stessi neuroni, stessa attività, stessa energia: cambia solo la ++tempistica++."),
    B("Random phases → contributions ++cancel++; aligned phases → they ++add up++.", "Fasi casuali → i contributi si ++annullano++; fasi allineate → si ++sommano++."),
    B("~EEG amplitude reflects synchrony~, not the amount of firing.", "~L'ampiezza EEG riflette la sincronia~, non la quantità di scarica.")], 8.7, Y0 + 0.3, 4.0, 4.4, { sz: 17, after: 14 });
  meta(s, t("a ++choir++: 50 voices singing different songs = noise; the same song = music.", "un ++coro++: 50 voci che cantano canzoni diverse = rumore; la stessa canzone = musica."), X0, 6.05, CW, 0.65, 16);
}

// 6 strati
{
  const s = content(t("Scales (3)", "Scale (3)"), t("Where the synapse is decides the surface polarity", "La posizione della sinapsi decide la polarità in superficie"),
    { notes: t("Classic laminar scheme (e.g. Olejniczak 2006 J Clin Neurophysiol 23:186). Thalamic input to layer IV vs cortico-cortical input to layer I.", "Schema laminare classico (es. Olejniczak 2006 J Clin Neurophysiol 23:186). Input talamico allo strato IV vs input cortico-corticale allo strato I.") });
  fig(s, "f06_layers", X0, Y0, 7.6, 4.9, "l", "Layer IV vs layer I input");
  text(s, [B("*Thalamic* input to ++layer IV++ (basal dendrites): sink deep, source superficial → surface ~positive~.", "Input *talamico* allo ++strato IV++ (dendriti basali): pozzo profondo, sorgente superficiale → superficie ~positiva~."),
    B("*Cortico-cortical* input to ++layer I++ (apical tufts): sink superficial → surface ~negative~.", "Input *cortico-corticale* allo ++strato I++ (ciuffi apicali): pozzo superficiale → superficie ~negativa~."),
    B("Same kind of synapse (EPSP), ++opposite scalp sign++: polarity tells *where*, not *what*.", "Stesso tipo di sinapsi (EPSP), ++segno opposto++ sullo scalpo: la polarità dice *dove*, non *che cosa*.")], 8.3, Y0 + 0.2, 4.4, 4.8, { sz: 16, after: 12 });
}

section(2, "The current dipole", "Il dipolo di corrente");

// 8 dipolo
{
  const s = content(t("Dipole (1)", "Dipolo (1)"), t("The current dipole: the atom of the EEG", "Il dipolo di corrente: l'atomo dell'EEG"),
    { notes: t("Infinite homogeneous medium formula; in a real head the lead field replaces 1/(4πσ). Typical cortical dipole moment density ~0.1–1 nA·m/mm².", "Formula per mezzo omogeneo infinito; nella testa reale il lead field sostituisce 1/(4πσ). Densità tipica di momento corticale ~0,1–1 nA·m/mm².") });
  fig(s, "f07_dipole", X0, Y0, 6.6, 4.5, "l", "Dipole potential");
  text(s, [B("A sink and a source separated by distance d, with current I: a *current dipole* p = I·d (A·m).", "Un pozzo e una sorgente a distanza d, con corrente I: un *dipolo di corrente* p = I·d (A·m)."),
    B("Its potential at distance r and angle θ:", "Il suo potenziale a distanza r e angolo θ:")], 7.3, Y0 + 0.1, 5.4, 1.9, { sz: 17, after: 10 });
  formula(s, "$V$ = $p$ cos θ / ( 4π σ $r$^2 )", 7.5, 3.75, 5.0, 0.8, { sz: 24, fill: PEACH });
  text(s, [B("Positive in front, negative behind, zero on the \"equator\".", "Positivo davanti, negativo dietro, zero sull'\"equatore\"."),
    B("Falls as ++1/r²++: deep sources are weak and blurred.", "Decade come ++1/r²++: sorgenti profonde deboli e sfocate.")], 7.3, 4.75, 5.4, 1.7, { sz: 17, after: 8 });
}

// 9 mappe
{
  const s = content(t("Dipole (2)", "Dipolo (2)"), t("One dipole, three different scalp maps", "Un dipolo, tre mappe di scalpo diverse"),
    { notes: t("Simulated: single dipole in a sphere (homogeneous approximation + Gaussian blur for the skull). Radial → monopolar; tangential → bipolar; deep → wide and weak.", "Simulato: un dipolo in una sfera (approssimazione omogenea + sfocatura gaussiana per il cranio). Radiale → monopolare; tangenziale → bipolare; profondo → largo e debole.") });
  fig(s, "f08_maps", X0 + 0.5, Y0, CW - 1.0, 3.0, "c", "Dipole maps");
  text(s, [B("*Radial* dipole (gyral crown): a ++single extremum++ above the source.", "Dipolo *radiale* (cresta del giro): un ++solo estremo++ sopra la sorgente."),
    B("*Tangential* dipole (sulcal wall): a ++positive/negative pair++; the source lies ++between++ the two poles, not under the maximum!", "Dipolo *tangenziale* (parete del solco): una ++coppia positivo/negativo++; la sorgente sta ++tra++ i due poli, non sotto il massimo!"),
    B("*Deep* dipole: wider and weaker map.", "Dipolo *profondo*: mappa più larga e più debole.")], X0, 4.95, CW, 1.8, { sz: 17, after: 8 });
}

section(3, "Volume conduction and head models", "Conduzione di volume e modelli di testa");

// 11 strati testa
{
  const s = content(t("Volume conduction (1)", "Conduzione di volume (1)"), t("The head is a layered conductor", "La testa è un conduttore a strati"),
    { notes: t("Conductivities from Vorwerk et al. (2014) NeuroImage 100:590; skull/brain ratio historically 1:80 (Rush & Driscoll 1968), measured ~1:15–1:50 (Oostendorp et al. 2000).", "Conducibilità da Vorwerk et al. (2014) NeuroImage 100:590; rapporto cranio/cervello storicamente 1:80 (Rush & Driscoll 1968), misurato ~1:15–1:50 (Oostendorp et al. 2000).") });
  fig(s, "f10_head", X0, Y0, 6.6, 4.4, "l", "Head layers");
  text(s, [B("Currents spread through every tissue (*volume conduction*): the EEG sees them ++instantaneously++ (quasi-static regime).", "Le correnti si propagano in ogni tessuto (*conduzione di volume*): l'EEG le vede ++istantaneamente++ (regime quasi-statico)."),
    B("The ++skull++ is ≈30–50× less conductive than the brain: it ++smears++ the potential laterally over several cm.", "Il ++cranio++ è ≈30–50 volte meno conduttivo del cervello: ++spalma++ il potenziale lateralmente su diversi cm."),
    B("CSF is highly conductive and shunts currents.", "Il liquor è molto conduttivo e devia le correnti."),
    B("MEG is almost insensitive to the skull → sharper maps (but blind to radial dipoles).", "La MEG è quasi insensibile al cranio → mappe più nitide (ma cieca ai dipoli radiali).")], 7.3, Y0 + 0.1, 5.4, 5.0, { sz: 16, after: 11 });
  meta(s, t("the skull is a ++frosted glass++: you still see the light, but not its exact shape.", "il cranio è un ++vetro smerigliato++: vedi ancora la luce, ma non la sua forma esatta."), X0, 5.95, 6.6, 0.75, 16);
}

// 12 lead field
{
  const s = content(t("Volume conduction (2)", "Conduzione di volume (2)"), t("Head models and the lead field: V = L · j", "Modelli di testa e lead field: V = L · j"),
    { notes: t("Forward models: spherical (analytic), BEM (boundary element), FEM (finite element) from individual MRI. Linear superposition holds because Maxwell's equations are linear in the quasi-static regime.", "Modelli diretti: sferici (analitici), BEM, FEM da RM individuale. La sovrapposizione lineare vale perché le equazioni di Maxwell sono lineari nel regime quasi-statico.") });
  fig(s, "f11_leadfield", X0, Y0, 6.2, 3.8, "l", "Lead field");
  text(s, [B("Each electrode sees a ++weighted sum++ of all sources: the weights form the *lead field* L.", "Ogni elettrodo vede una ++somma pesata++ di tutte le sorgenti: i pesi formano il *lead field* L."),
    B("L depends only on ++geometry and conductivities++ (head model), not on the data.", "L dipende solo da ++geometria e conducibilità++ (modello di testa), non dai dati."),
    B("Models: *spheres* (fast, approximate) → *BEM* → *FEM* (individual MRI, most accurate).", "Modelli: *sfere* (veloci, approssimate) → *BEM* → *FEM* (RM individuale, più accurati)."),
    B("Forward: j → V (easy). Inverse: V → j (ill-posed, Lecture 9).", "Diretto: j → V (facile). Inverso: V → j (mal posto, Lezione 9).")], 7.0, Y0 + 0.1, 5.7, 4.8, { sz: 16, after: 11 });
  note(s, t("Consequence: neighbouring electrodes are ++correlated++ even without any brain interaction → beware of spurious connectivity (Lecture 9).", "Conseguenza: elettrodi vicini sono ++correlati++ anche senza alcuna interazione cerebrale → attenzione alla connettività spuria (Lezione 9)."), X0, 5.4, 6.2, 1.2, 15);
}

// 13 montaggi
{
  const s = content(t("Recording geometry", "Geometria di registrazione"), t("Referential vs bipolar montages", "Montaggi referenziali e bipolari"),
    { notes: t("Simulated: C3 source with a common slow component in all channels. Bipolar derivations cancel common activity and show local gradients.", "Simulato: sorgente in C3 con una componente lenta comune a tutti i canali. Le derivazioni bipolari cancellano l'attività comune e mostrano i gradienti locali.") });
  fig(s, "f13_montage", X0, Y0, 8.2, 3.6, "l", "Montages");
  text(s, [B("*Referential*: each electrode vs a common reference (e.g. ear, mastoid, Cz, average).", "*Referenziale*: ogni elettrodo contro un riferimento comune (es. orecchio, mastoide, Cz, media)."),
    B("*Bipolar*: difference between ++neighbouring++ electrodes → common activity cancels, local gradients remain.", "*Bipolare*: differenza tra elettrodi ++vicini++ → l'attività comune si annulla, restano i gradienti locali."),
    B("*Average reference* and *surface Laplacian (CSD)* are ++re-referencing++ computed offline (Lecture 4).", "*Riferimento medio* e *Laplaciano di superficie (CSD)* sono ++ri-referenziazioni++ calcolate offline (Lezione 4).")], 8.8, Y0 + 0.1, 3.9, 5.0, { sz: 15, after: 10 });
  note(s, t("No montage is \"true\": each is a different ++view++ of the same fields.", "Nessun montaggio è \"vero\": ognuno è una diversa ++vista++ degli stessi campi."), X0, 5.6, 8.2, 0.8, 16);
}

section(4, "The EEG rhythms", "I ritmi EEG");

// 15 spettro
{
  const s = content(t("Rhythms (1)", "Ritmi (1)"), t("The power spectrum: a 1/f background with peaks", "Lo spettro di potenza: un fondo 1/f con picchi"),
    { notes: t("Simulated spectrum (Welch). Separate periodic and aperiodic components: Donoghue et al. (2020) Nat Neurosci 23:1655 (FOOOF / specparam).", "Spettro simulato (Welch). Separare componenti periodiche e aperiodiche: Donoghue et al. (2020) Nat Neurosci 23:1655 (FOOOF / specparam).") });
  fig(s, "f15_spectrum", X0, Y0, 6.2, 5.0, "l", "Power spectrum");
  text(s, [B("Power decreases roughly as ++1/f^{χ}++: the *aperiodic* component (scale-free background).", "La potenza decresce circa come ++1/f^{χ}++: la componente *aperiodica* (fondo senza scala)."),
    B("On top: *periodic* peaks = true oscillations (alpha ≈10 Hz, beta ≈20 Hz).", "Sopra: picchi *periodici* = vere oscillazioni (alfa ≈10 Hz, beta ≈20 Hz)."),
    B("~Band power ≠ oscillation~: a change in the 1/f slope changes \"theta power\" even without theta!", "~Potenza di banda ≠ oscillazione~: una variazione della pendenza 1/f cambia la \"potenza theta\" anche senza theta!"),
    B("The aperiodic exponent may track the cortical ++excitation/inhibition balance++ (Gao et al., 2017).", "L'esponente aperiodico potrebbe riflettere il bilancio ++eccitazione/inibizione++ corticale (Gao et al., 2017).")], 7.0, Y0 + 0.1, 5.7, 5.0, { sz: 16, after: 12 });
}

// 16 bande
{
  const s = content(t("Rhythms (2)", "Ritmi (2)"), t("The classical frequency bands", "Le bande di frequenza classiche"),
    { notes: t("Band limits follow the IFCN glossary (Kane et al. 2017, Clin Neurophysiol Pract 2:170); exact limits vary across studies.", "I limiti seguono il glossario IFCN (Kane et al. 2017, Clin Neurophysiol Pract 2:170); variano tra studi.") });
  const b = [["δ delta", "0.5–4 Hz", t("deep sleep (N3), infants; focal delta in awake adults = lesion sign", "sonno profondo (N3), neonati; delta focale nell'adulto sveglio = segno di lesione"), "8E7CC3"],
    ["θ theta", "4–8 Hz", t("drowsiness; frontal-midline theta in working memory and cognitive control", "sonnolenza; theta frontale mediano in memoria di lavoro e controllo cognitivo"), TEAL],
    ["α alpha", "8–13 Hz", t("posterior, eyes closed; blocks with eyes opening; IAF ≈10 Hz in adults", "posteriore, occhi chiusi; si blocca aprendo gli occhi; IAF ≈10 Hz negli adulti"), ACC],
    ["μ mu", "8–13 Hz", t("sensorimotor, arch-shaped; desynchronises with movement or motor imagery", "sensomotorio, ad arco; si desincronizza con movimento o immaginazione motoria"), "C2410C"],
    ["β beta", "13–30 Hz", t("sensorimotor, post-movement rebound; increased by benzodiazepines", "sensomotorio, rebound post-movimento; aumentato dalle benzodiazepine"), "B7791F"],
    ["γ gamma", "30–80+ Hz", t("local processing; ⚠ contaminated by muscle and microsaccades", "elaborazione locale; ⚠ contaminata da muscoli e microsaccadi"), "2E8B57"]];
  b.forEach(([n, r, d, c], i) => {
    const y = Y0 + i * 0.83;
    card(s, X0, y, CW, 0.72, i % 2 ? PEACH : TINT);
    s.addText(n, { x: X0 + 0.15, y, w: 1.6, h: 0.72, fontFace: SERIF, fontSize: 19, bold: true, color: c, valign: "middle", margin: 0, isTextBox: true });
    s.addText(r, { x: X0 + 1.75, y, w: 1.5, h: 0.72, fontFace: SANS, fontSize: 15, color: MUTED, valign: "middle", margin: 0, isTextBox: true });
    text(s, [d], X0 + 3.3, y, CW - 3.5, 0.72, { sz: 15, valign: "middle" });
  });
}

// 17 alfa e mu
{
  const s = content(t("Rhythms (3)", "Ritmi (3)"), t("Alpha and mu: same frequency, different places and roles", "Alfa e mu: stessa frequenza, luoghi e ruoli diversi"),
    { notes: t("Pfurtscheller & Lopes da Silva (1999) Clin Neurophysiol 110:1842 (ERD/ERS). Klimesch (1999) Brain Res Rev 29:169 (IAF and cognition).", "Pfurtscheller & Lopes da Silva (1999) Clin Neurophysiol 110:1842 (ERD/ERS). Klimesch (1999) Brain Res Rev 29:169 (IAF e cognizione).") });
  fig(s, "f18_alpha_mu", X0, Y0, 6.6, 3.6, "l", "Alpha and mu topographies");
  text(s, [B("*Alpha*: occipito-parietal, maximal with eyes closed, reduced by visual input and attention.", "*Alfa*: occipito-parietale, massimo a occhi chiusi, ridotto da input visivo e attenzione."),
    B("*Mu*: over sensorimotor cortex (C3/C4), reduced by ++movement++, ++motor imagery++ and action observation.", "*Mu*: sulla corteccia sensomotoria (C3/C4), ridotto da ++movimento++, ++immaginazione motoria++ e osservazione di azioni."),
    B("A power decrease = *event-related desynchronisation (ERD)*; increase = *ERS*. Basis of motor-imagery BCIs (Lecture 10).", "Diminuzione di potenza = *desincronizzazione evento-correlata (ERD)*; aumento = *ERS*. Base delle BCI a immaginazione motoria (Lezione 10).")], 7.3, Y0 + 0.1, 5.4, 5.0, { sz: 16, after: 12 });
  meta(s, t("idle rhythms are an engine ++idling++: when the region gets work to do, the idle hum disappears.", "i ritmi di riposo sono un motore ++al minimo++: quando la regione deve lavorare, il ronzio del minimo scompare."), X0, 5.4, 6.6, 1.1, 16);
}

// 18 ampiezza/frequenza
{
  const s = content(t("Rhythms (4)", "Ritmi (4)"), t("Slower rhythms are larger: size of the network", "I ritmi lenti sono più ampi: la dimensione della rete"),
    { notes: t("Buzsáki & Draguhn (2004) Science 304:1926: slow oscillations recruit larger networks because of axonal conduction delays.", "Buzsáki & Draguhn (2004) Science 304:1926: le oscillazioni lente reclutano reti più ampie per via dei ritardi di conduzione assonale.") });
  fig(s, "f21_ampfreq", X0, Y0, 6.0, 4.8, "l", "Amplitude vs frequency");
  text(s, [B("Oscillations need ++round trips++ of activity; conduction delays limit how fast distant regions can stay in phase.", "Le oscillazioni richiedono ++andata e ritorno++ dell'attività; i ritardi di conduzione limitano la velocità con cui regioni lontane restano in fase."),
    B("~Slow~ rhythms engage ++large++ networks (more neurons → larger EEG); ~fast~ rhythms are ++local++.", "I ritmi ~lenti~ coinvolgono reti ++ampie++ (più neuroni → EEG più ampio); i ritmi ~veloci~ sono ++locali++."),
    B("Brain rhythms form a ++hierarchy++ with roughly constant ratios between bands (Buzsáki & Draguhn, 2004).", "I ritmi cerebrali formano una ++gerarchia++ con rapporti circa costanti tra bande (Buzsáki & Draguhn, 2004).")], 6.9, Y0 + 0.1, 5.8, 4.8, { sz: 16, after: 12 });
}

section(5, "Resting-state EEG, vigilance and sleep", "EEG a riposo, vigilanza e sonno");

// 20 vigilanza
{
  const s = content(t("Resting state (1)", "Stato di riposo (1)"), t("The resting-state EEG probes arousal and vigilance", "L'EEG a riposo sonda arousal e vigilanza"),
    { notes: t("Babiloni et al. (2020) Clin Neurophysiol 131:285 (IFCN rsEEG guidelines); Hegerl & Hensch (2014) VIGALL. Traces are simulated.", "Babiloni et al. (2020) Clin Neurophysiol 131:285 (linee guida IFCN rsEEG); Hegerl & Hensch (2014) VIGALL. Tracciati simulati.") });
  fig(s, "f22_vigilance", X0, Y0, CW, 3.9, "c", "Vigilance continuum");
  text(s, [B("Within a few minutes of \"rest\", subjects drift along the ++vigilance continuum++: alert → relaxed → drowsy → sleep.", "In pochi minuti di \"riposo\", i soggetti scivolano lungo il ++continuum di vigilanza++: vigile → rilassato → sonnolento → sonno."),
    B("~Practical rule~: always control vigilance (instructions, eyes-open/closed blocks, short recordings) when comparing groups.", "~Regola pratica~: controllare sempre la vigilanza (istruzioni, blocchi a occhi aperti/chiusi, registrazioni brevi) quando si confrontano gruppi.")], X0, 5.75, CW, 1.1, { sz: 15, after: 6 });
}

// 21 sonno
{
  const s = content(t("Resting state (2)", "Stato di riposo (2)"), t("Sleep: the EEG defines the stages", "Sonno: l'EEG definisce gli stadi"),
    { notes: t("AASM scoring manual (Berry et al.). Spindles 11–16 Hz; slow waves ≥75 µV, 0.5–2 Hz; REM: low-voltage mixed EEG, rapid eye movements, muscle atonia.", "Manuale AASM (Berry et al.). Fusi 11–16 Hz; onde lente ≥75 µV, 0,5–2 Hz; REM: EEG misto a basso voltaggio, movimenti oculari rapidi, atonia.") });
  fig(s, "f23_hypnogram", X0, Y0, 7.4, 3.6, "l", "Hypnogram");
  text(s, [B("*N1*: alpha disappears, theta, vertex waves.", "*N1*: l'alfa scompare, theta, onde al vertice."),
    B("*N2*: ++sleep spindles++ (11–16 Hz, thalamocortical) and ++K-complexes++.", "*N2*: ++fusi del sonno++ (11–16 Hz, talamo-corticali) e ++complessi K++."),
    B("*N3*: ++slow waves++ (<2 Hz, high amplitude): cortical up/down states.", "*N3*: ++onde lente++ (<2 Hz, alta ampiezza): stati up/down corticali."),
    B("*REM*: EEG similar to wake, rapid eye movements, muscle atonia, dreams.", "*REM*: EEG simile alla veglia, movimenti oculari rapidi, atonia muscolare, sogni.")], 8.0, Y0 + 0.1, 4.7, 5.0, { sz: 15, after: 10 });
  note(s, t("Link to Lecture 2: spindles and delta arise from ++thalamocortical burst mode++.", "Collegamento con la Lezione 2: fusi e delta nascono dal ++modo burst talamo-corticale++."), X0, 5.6, 7.4, 0.8, 16);
}

// 22 domande
{
  const s = content(t("Check your understanding", "Verifica"), t("Three questions", "Tre domande"),
    { notes: t("(1) Tangential dipole: source between the two extrema. (2) Correlation through volume conduction. (3) Check the aperiodic component and vigilance.", "(1) Dipolo tangenziale: la sorgente è tra i due estremi. (2) Correlazione per conduzione di volume. (3) Controllare la componente aperiodica e la vigilanza.") });
  rows(s, [t("A map shows a positive maximum at C3 and a negative one at P3. Where is the source likely to be?", "Una mappa mostra un massimo positivo in C3 e uno negativo in P3. Dove si trova probabilmente la sorgente?"),
    t("Fz and FCz are highly correlated. Does this prove the two regions communicate?", "Fz e FCz sono molto correlati. Questo prova che le due regioni comunicano?"),
    t("Patients show more \"theta power\" than controls. List two explanations other than more theta oscillations.", "I pazienti mostrano più \"potenza theta\" dei controlli. Elenca due spiegazioni diverse da più oscillazioni theta.")], X0, Y0 + 0.2, CW, 1.2, 0.35, 18, ACC);
}

// 23 take home
{
  const s = content(t("Take-home messages", "Messaggi chiave"), t("Take-home messages", "Messaggi chiave"));
  rows(s, [t("EEG = ++macroscopic++ view of synchronised LFPs over cm of cortex.", "EEG = visione ++macroscopica++ di LFP sincronizzati su cm di corteccia."),
    t("Current ++dipoles++: radial → one extremum, tangential → a pair; amplitude ∝ 1/r².", "++Dipoli++ di corrente: radiale → un estremo, tangenziale → una coppia; ampiezza ∝ 1/r²."),
    t("The skull ++blurs++; the lead field is ++linear++ (V = L·j); nearby channels are correlated.", "Il cranio ++sfoca++; il lead field è ++lineare++ (V = L·j); canali vicini sono correlati."),
    t("Spectrum = ++1/f++ background + oscillatory ++peaks++; bands have typical topographies.", "Spettro = fondo ++1/f++ + ++picchi++ oscillatori; le bande hanno topografie tipiche."),
    t("Resting EEG reflects ++vigilance++; sleep stages are defined by the EEG.", "L'EEG a riposo riflette la ++vigilanza++; gli stadi del sonno sono definiti dall'EEG.")], X0, Y0, CW, 0.85, 0.15, 17);
}

// 24 letture
{
  const s = content(t("Suggested reading", "Letture consigliate"), t("Suggested reading", "Letture consigliate"));
  text(s, [
    { t: "Nunez P.L., Srinivasan R. (2006) *Electric Fields of the Brain*, 2nd ed. OUP — chapters on dipoles and head models.", b: true },
    { t: "Buzsáki G. (2006) *Rhythms of the Brain*. OUP.", b: true },
    { t: "Buzsáki G., Draguhn A. (2004) Neuronal oscillations in cortical networks. *Science* 304:1926–1929.", b: true },
    { t: "Varela F. et al. (2001) The brainweb: phase synchronization and large-scale integration. *Nat Rev Neurosci* 2:229–239.", b: true },
    { t: "Olejniczak P. (2006) Neurophysiologic basis of EEG. *J Clin Neurophysiol* 23:186–189.", b: true },
    { t: "Vorwerk J. et al. (2014) A guideline for head volume conductor modeling in EEG and MEG. *NeuroImage* 100:590–607.", b: true },
    { t: "Donoghue T. et al. (2020) Parameterizing neural power spectra into periodic and aperiodic components. *Nat Neurosci* 23:1655–1665.", b: true },
    { t: "Pfurtscheller G., Lopes da Silva F.H. (1999) Event-related EEG/MEG synchronization and desynchronization. *Clin Neurophysiol* 110:1842–1857.", b: true },
    { t: "Babiloni C. et al. (2020) International Federation of Clinical Neurophysiology (IFCN) – EEG research workgroup: recommendations on frequency and topographic analysis of resting state EEG rhythms. *Clin Neurophysiol* 131:285–307.", b: true }], X0, Y0, CW, 5.1, { sz: 13, after: 6 });
}

save(OUT);
