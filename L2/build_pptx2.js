// EEG – Lecture 2: cellular bases of EEG (bilingue: node build_pptx2.js en|it)
const __R = (function () { const p = require("path"), fs = require("fs"); let d = process.env.COURSE_ROOT || __dirname;
  while (!fs.existsSync(p.join(d, ".course_root")) && p.dirname(d) !== d) d = p.dirname(d); return d; })();
const LANGARG = process.argv[2] || "en";
global.CFG = { lang: LANGARG, fig: __R + "/L2/figpng_" + LANGARG, common: __R + "/common",
  footer: LANGARG === "it" ? "Brain Imaging · EEG · Lezione 2 · Basi cellulari dell'EEG" : "Brain Imaging · EEG · Lecture 2 · Cellular bases of EEG",
  lezione: LANGARG === "it" ? "Lezione 2" : "Lecture 2",
  titolo: LANGARG === "it" ? "Le basi cellulari\ndell'EEG" : "The cellular bases\nof the EEG", titoloSize: 46 };
const L = require(__R + "/common/pptlib_eeg.js");
const { tr: t, pres, fig, content, text, formula, card, badge, copertina, save } = L;
const { INK, ACC, TEAL, TXT, MUTED, TINT, WHITE, SERIF, SANS, W, H, MX, X0, Y0, CW } = L.C;
const OUT = process.argv[3] || `${__R}/L2/out/EEG_L2_${LANGARG}.pptx`;
const PEACH = "FDF0E9";
function note(s, str, x, y, w, h, sz = 17, fill = TINT) {
  card(s, x, y, w, h, fill);
  text(s, [str], x + 0.25, y + 0.05, w - 0.5, h - 0.1, { sz, valign: "middle", align: "center" });
}
function meta(s, str, x, y, w, h, sz = 17) {
  card(s, x, y, w, h, PEACH);
  text(s, [{ t: "~" + t("Metaphor", "Metafora") + "~  " + str }], x + 0.25, y + 0.05, w - 0.5, h - 0.1, { sz, valign: "middle" });
}
function section(n, en, it) { return L.sezione(n, t(en, it)); }
function rows(s, items, x, y, w, h, gap, sz = 18, colBadge = TEAL) {
  items.forEach((it, i) => {
    const yy = y + i * (h + gap);
    card(s, x, yy, w, h, i % 2 ? PEACH : TINT);
    badge(s, i + 1, x + 0.18, yy + h / 2 - 0.23, colBadge);
    text(s, [it], x + 0.85, yy, w - 1.05, h, { sz, valign: "middle" });
  });
}
const B = (en, it) => ({ t: t(en, it), b: true });

// 1 ------------------------------------------------------------ copertina
copertina();

// 2 ------------------------------------------------------------ obiettivi
{
  const s = content(t("Lecture 2", "Lezione 2"), t("From ions to scalp potentials: today's path", "Dagli ioni ai potenziali di scalpo: il percorso di oggi"),
    { notes: t("Link to Lecture 1: we said EEG = synchronous postsynaptic currents. Today we open the black box of the single neuron.", "Collegamento con la Lezione 1: EEG = correnti postsinaptiche sincrone. Oggi apriamo la scatola nera del singolo neurone.") });
  rows(s, [t("The *neuron* and its ++membrane++: why a cell has a voltage.", "Il *neurone* e la sua ++membrana++: perché una cellula ha una tensione."),
    t("*Resting potential*: diffusion vs electric force, ++Nernst++ and ++Goldman++ equations.", "*Potenziale di riposo*: diffusione contro forza elettrica, equazioni di ++Nernst++ e ++Goldman++."),
    t("*Action potential*: voltage-gated channels, threshold, propagation (Hodgkin–Huxley).", "*Potenziale d'azione*: canali voltaggio-dipendenti, soglia, propagazione (Hodgkin–Huxley)."),
    t("*Synapses*: EPSP/IPSP, temporal and spatial ++summation++.", "*Sinapsi*: EPSP/IPSP, ++sommazione++ temporale e spaziale."),
    t("From synapses to EEG: ++sinks and sources++, pyramidal cells, ++thalamocortical loops++ and rhythms.", "Dalle sinapsi all'EEG: ++pozzi e sorgenti++, cellule piramidali, ++anelli talamo-corticali++ e ritmi.")], X0, Y0, CW, 0.85, 0.15, 18);
}

// 3 ------------------------------------------------------------ la domanda
{
  const s = content(t("The question", "La domanda"), t("What happens in a neuron when the EEG goes down?", "Che cosa succede in un neurone quando l'EEG scende?"),
    { notes: t("By EEG convention negative is often plotted up (clinical) or down (research): always check the axis!", "Per convenzione il negativo è spesso disegnato in alto (clinica) o in basso (ricerca): controllare sempre l'asse!") });
  fig(s, "f03_question", X0, Y0, 5.8, 4.9, "c", "Pyramidal cell under the scalp");
  text(s, [B("A scalp electrode records a ++negative deflection++ lasting tens of milliseconds.", "Un elettrodo di scalpo registra una ++deflessione negativa++ di qualche decina di millisecondi."),
    B("Which ++cellular events++ produce it? Where do the currents flow? Why tens of ms and not 1 ms?", "Quali ++eventi cellulari++ la producono? Dove scorrono le correnti? Perché decine di ms e non 1 ms?"),
    B("To answer we need four ingredients: ~membrane~, ~ions~, ~channels~, ~synapses~.", "Per rispondere servono quattro ingredienti: ~membrana~, ~ioni~, ~canali~, ~sinapsi~."),
    { t: t("⚠ Polarity conventions differ: clinical EEG often plots ++negative up++. Always check the axis.", "⚠ Le convenzioni di polarità variano: l'EEG clinico spesso disegna il ++negativo in alto++. Controllare sempre l'asse."), b: true, c: MUTED }], 6.8, Y0 + 0.2, 5.9, 4.6, { sz: 18, after: 14 });
}

// 4 ------------------------------------------------------------ sezione neurone
section(1, "The neuron and its membrane", "Il neurone e la sua membrana");

// 5 ------------------------------------------------------------ anatomia
{
  const s = content(t("The neuron", "Il neurone"), t("A cell specialised to receive, integrate and transmit", "Una cellula specializzata per ricevere, integrare e trasmettere"),
    { notes: t("Numbers: a cortical pyramidal cell receives ~10^4 synapses; dendrites ~90% of the membrane surface.", "Numeri: una piramidale corticale riceve ~10^4 sinapsi; i dendriti sono ~90% della superficie di membrana.") });
  fig(s, "f05_neuron", X0, Y0, CW, 3.2, "c", "Neuron anatomy");
  const cw = (CW - 0.9) / 4;
  [[t("Dendrites", "Dendriti"), t("receive thousands of synaptic inputs (≈10⁴ in a pyramidal cell)", "ricevono migliaia di input sinaptici (≈10⁴ in una piramidale)")],
    [t("Soma", "Soma"), t("cell body: nucleus, metabolism, integration", "corpo cellulare: nucleo, metabolismo, integrazione")],
    [t("Axon hillock", "Monticolo assonale"), t("highest density of Na⁺ channels: where spikes start", "massima densità di canali Na⁺: qui nascono gli spike")],
    [t("Axon & terminals", "Assone e terminali"), t("carry the spike and release neurotransmitter", "conducono lo spike e liberano il neurotrasmettitore")]].forEach(([h, d], i) => {
    const x = X0 + i * (cw + 0.3);
    card(s, x, 5.05, cw, 1.6, i % 2 ? PEACH : TINT);
    text(s, [{ t: "~" + h + "~", align: "center" }, { t: d, align: "center" }], x + 0.15, 5.1, cw - 0.3, 1.5, { sz: 14, after: 4 });
  });
}

// 6 ------------------------------------------------------------ membrana
{
  const s = content(t("The membrane", "La membrana"), t("A thin insulator with gates: the membrane is a capacitor", "Un sottile isolante con cancelli: la membrana è un condensatore"),
    { notes: t("Specific capacitance ≈1 µF/cm² (Hille, Ion Channels of Excitable Membranes).", "Capacità specifica ≈1 µF/cm² (Hille, Ion Channels of Excitable Membranes).") });
  fig(s, "f06_membrane", X0, Y0, 7.4, 3.3, "l", "Lipid bilayer with channels");
  text(s, [B("The ++phospholipid bilayer++ (≈5 nm) does not let ions through: it separates charges → it behaves like a ++capacitor++.", "Il ++doppio strato fosfolipidico++ (≈5 nm) non lascia passare gli ioni: separa le cariche → si comporta come un ++condensatore++."),
    B("*Ion channels* are proteins that form selective pores: they open/close depending on ++voltage++, ++ligands++ or mechanical stimuli.", "I *canali ionici* sono proteine che formano pori selettivi: si aprono/chiudono in base a ++tensione++, ++ligandi++ o stimoli meccanici."),
    B("*Pumps* (Na⁺/K⁺-ATPase) use ATP to keep concentrations different inside and outside.", "Le *pompe* (Na⁺/K⁺-ATPasi) usano ATP per mantenere diverse le concentrazioni dentro e fuori.")], 8.1, Y0 + 0.1, 4.6, 4.8, { sz: 16, after: 12 });
  meta(s, t("the membrane is a ++dam++: the pumps fill the reservoir, the channels are the ++sluice gates++.", "la membrana è una ++diga++: le pompe riempiono il bacino, i canali sono le ++paratoie++."), X0, 5.4, 7.4, 0.9, 17);
}

// 7 ------------------------------------------------------------ concentrazioni
{
  const s = content(t("Ions", "Ioni"), t("Unequal ion concentrations inside and outside", "Concentrazioni ioniche diverse dentro e fuori"),
    { notes: t("Typical mammalian values (Kandel et al., Principles of Neural Science; Hille 2001). E computed with the Nernst equation at 37 °C.", "Valori tipici di mammifero (Kandel et al., Principles of Neural Science; Hille 2001). E calcolati con Nernst a 37 °C.") });
  fig(s, "f07_ions", X0, Y0, 7.0, 4.7, "l", "Ion concentrations");
  text(s, [B("~K⁺~ is concentrated ++inside++ (≈140 vs 5 mM).", "~K⁺~ è concentrato ++dentro++ (≈140 contro 5 mM)."),
    B("~Na⁺~, ~Cl⁻~ and ~Ca²⁺~ are concentrated ++outside++.", "~Na⁺~, ~Cl⁻~ e ~Ca²⁺~ sono concentrati ++fuori++."),
    B("Ca²⁺ inside is ++10 000× lower++: tiny influxes are powerful signals (e.g. transmitter release).", "Il Ca²⁺ interno è ++10 000 volte più basso++: piccoli ingressi sono segnali potenti (es. rilascio del trasmettitore)."),
    B("Each gradient stores energy, like a ++charged battery++.", "Ogni gradiente immagazzina energia, come una ++batteria carica++.")], 7.8, Y0 + 0.3, 4.9, 4.6, { sz: 17, after: 12 });
}

// 8 ------------------------------------------------------------ due forze
{
  const s = content(t("Resting potential (1)", "Potenziale di riposo (1)"), t("Two forces on every ion: diffusion and electricity", "Due forze su ogni ione: diffusione ed elettricità"),
    { notes: t("Thought experiment: membrane permeable only to K⁺. K⁺ leaves → inside becomes negative → electrical attraction pulls K⁺ back. Equilibrium at E_K.", "Esperimento mentale: membrana permeabile solo al K⁺. Il K⁺ esce → l'interno diventa negativo → l'attrazione elettrica lo richiama. Equilibrio a E_K.") });
  fig(s, "f09_two_forces", X0, Y0, 4.6, 4.9, "c", "Diffusion and electric force");
  text(s, [B("If the membrane lets only ~K⁺~ through, K⁺ ++diffuses out++ down its concentration gradient.", "Se la membrana lascia passare solo ~K⁺~, il K⁺ ++diffonde fuori++ secondo il gradiente di concentrazione."),
    B("Every K⁺ that leaves carries a positive charge → the inside becomes ++negative++ → an ++electric force++ pulls K⁺ back.", "Ogni K⁺ che esce porta via una carica positiva → l'interno diventa ++negativo++ → una ++forza elettrica++ richiama il K⁺."),
    B("Equilibrium when the two forces balance: the *equilibrium (Nernst) potential*.", "Equilibrio quando le due forze si bilanciano: il *potenziale di equilibrio (di Nernst)*.")], 5.6, Y0 + 0.1, 7.1, 3.0, { sz: 17, after: 12 });
  formula(s, "$E$_{ion} = ( $R$ $T$ / $z$ $F$ ) · ln ( [ion]_{out} / [ion]_{in} )", 5.9, 4.95, 6.6, 0.8, { sz: 22, fill: PEACH });
  text(s, [{ t: t("At 37 °C, RT/F ≈ 26.7 mV → E_K ≈ −89 mV, E_{Na} ≈ +67 mV.", "A 37 °C, RT/F ≈ 26,7 mV → E_K ≈ −89 mV, E_{Na} ≈ +67 mV."), align: "center", c: MUTED }], 5.6, 5.9, 7.1, 0.5, { sz: 15 });
}

// 9 ------------------------------------------------------------ Goldman e riposo
{
  const s = content(t("Resting potential (2)", "Potenziale di riposo (2)"), t("The resting potential: a weighted vote of the ions", "Il potenziale di riposo: un voto pesato degli ioni"),
    { notes: t("GHK with pK:pNa:pCl = 1:0.05:0.45 gives ≈ −65 mV (Hodgkin & Katz 1949).", "GHK con pK:pNa:pCl = 1:0,05:0,45 dà ≈ −65 mV (Hodgkin & Katz 1949).") });
  fig(s, "f10_scale", X0, Y0, 3.4, 5.0, "c", "Potential scale");
  formula(s, "$V$_{rest} = ( $R$ $T$ / $F$ ) ln [ ( $p$_K [K]_o + $p$_{Na} [Na]_o + $p$_{Cl} [Cl]_i ) / ( $p$_K [K]_i + $p$_{Na} [Na]_i + $p$_{Cl} [Cl]_o ) ]", 4.2, Y0 + 0.1, 8.5, 0.9, { sz: 17, fill: PEACH });
  text(s, [B("*Goldman–Hodgkin–Katz* equation: each ion pulls V toward its own E, ++weighted by its permeability++ p.", "Equazione di *Goldman–Hodgkin–Katz*: ogni ione tira V verso il proprio E, ++pesato per la permeabilità++ p."),
    B("At rest the membrane is mostly permeable to K⁺ (p_K : p_{Na} : p_{Cl} ≈ 1 : 0.05 : 0.45) → V_{rest} ≈ ++−65 mV++, close to E_K.", "A riposo la membrana è permeabile soprattutto al K⁺ (p_K : p_{Na} : p_{Cl} ≈ 1 : 0,05 : 0,45) → V_{riposo} ≈ ++−65 mV++, vicino a E_K."),
    B("Changing permeabilities (opening channels) ++moves V++: this is how neurons signal.", "Cambiando le permeabilità (aprendo canali) ++V si sposta++: è così che i neuroni comunicano."),
    B("The Na⁺/K⁺ pump (3 Na⁺ out, 2 K⁺ in) keeps the gradients in the long run.", "La pompa Na⁺/K⁺ (3 Na⁺ fuori, 2 K⁺ dentro) mantiene i gradienti nel lungo periodo.")], 4.2, 2.95, 8.5, 3.7, { sz: 16, after: 10 });
}

// 10 ----------------------------------------------------------- sezione PA
section(2, "The action potential", "Il potenziale d'azione");

// 11 ----------------------------------------------------------- PA e HH
{
  const s = content(t("Action potential (1)", "Potenziale d'azione (1)"), t("Anatomy of a spike (Hodgkin–Huxley model)", "Anatomia di uno spike (modello di Hodgkin–Huxley)"),
    { notes: t("Simulated with the original HH (1952) squid-axon equations, modern convention (rest −65 mV). Nobel Prize 1963.", "Simulato con le equazioni originali di HH (1952) per l'assone di calamaro, convenzione moderna (riposo −65 mV). Nobel 1963.") });
  fig(s, "f13_ap", X0, Y0, 6.4, 4.9, "l", "Hodgkin-Huxley action potential");
  const ph = [t("Stimulus depolarises the membrane", "Lo stimolo depolarizza la membrana"), t("Threshold: Na⁺ channels open (positive feedback)", "Soglia: si aprono i canali Na⁺ (feedback positivo)"),
    t("Rising phase: Na⁺ rushes in, V → +40 mV", "Fase ascendente: entra Na⁺, V → +40 mV"), t("Na⁺ channels inactivate, K⁺ channels open", "I canali Na⁺ si inattivano, si aprono i K⁺"),
    t("Repolarisation and after-hyperpolarisation (near E_K)", "Ripolarizzazione e iperpolarizzazione postuma (verso E_K)"), t("Refractory period, return to rest", "Periodo refrattario, ritorno al riposo")];
  ph.forEach((p, i) => {
    const y = Y0 + i * 0.8;
    card(s, 7.3, y, 5.4, 0.7, i % 2 ? PEACH : TINT);
    badge(s, i + 1, 7.42, y + 0.12, "C2410C");
    text(s, [p], 8.0, y, 4.6, 0.7, { sz: 14, valign: "middle" });
  });
}

// 12 ----------------------------------------------------------- tutto o nulla
{
  const s = content(t("Action potential (2)", "Potenziale d'azione (2)"), t("All-or-none: information is in the rate, not the size", "Tutto o nulla: conta la frequenza, non l'ampiezza"),
    { notes: t("Same HH model with sustained currents: below ~6 µA/cm² no repetitive firing; above it the rate increases with current.", "Stesso modello HH con correnti costanti: sotto ~6 µA/cm² niente scarica ripetitiva; sopra la frequenza aumenta con la corrente.") });
  fig(s, "f14_fI", X0, Y0, 7.6, 4.6, "l", "Firing vs current");
  text(s, [B("Below threshold: ++no spike++. Above: a stereotyped spike of ≈100 mV and ≈1 ms.", "Sotto soglia: ++nessuno spike++. Sopra: uno spike stereotipato di ≈100 mV e ≈1 ms."),
    B("A stronger input produces ++more spikes++ (rate code), not bigger ones.", "Un input più forte produce ++più spike++ (codice di frequenza), non spike più grandi."),
    B("After a spike, a *refractory period* (≈1–2 ms absolute) limits the maximum rate.", "Dopo uno spike, un *periodo refrattario* (≈1–2 ms assoluto) limita la frequenza massima.")], 8.3, Y0 + 0.2, 4.4, 4.4, { sz: 16, after: 12 });
  meta(s, t("a ++flushing toilet++: press gently and nothing happens; press past the point and the flush is always the same.", "lo ++sciacquone++: premi piano e non succede nulla; oltre un certo punto lo scarico è sempre uguale."), X0, 5.95, CW, 0.75, 16);
}

// 13 ----------------------------------------------------------- propagazione
{
  const s = content(t("Action potential (3)", "Potenziale d'azione (3)"), t("Propagation: continuous and saltatory conduction", "Propagazione: conduzione continua e saltatoria"),
    { notes: t("Conduction velocity: ~0.5–2 m/s unmyelinated C fibres, up to ~120 m/s large myelinated Aα fibres.", "Velocità di conduzione: ~0,5–2 m/s fibre C amieliniche, fino a ~120 m/s grandi fibre mielinizzate Aα.") });
  fig(s, "f15_conduction", X0, Y0, CW, 2.6, "c", "Conduction");
  text(s, [B("The spike regenerates itself along the axon: local currents depolarise the next patch above threshold.", "Lo spike si rigenera lungo l'assone: le correnti locali portano sopra soglia il tratto successivo."),
    B("*Myelin* (oligodendrocytes/Schwann cells) insulates the axon: the spike ++jumps++ from one node of Ranvier to the next → faster and cheaper.", "La *mielina* (oligodendrociti/cellule di Schwann) isola l'assone: lo spike ++salta++ da un nodo di Ranvier al successivo → più veloce ed economico."),
    B("~For EEG~: spikes are fast (≈1 ms) and travel away: they ++contribute little++ to the scalp signal (except high-frequency activity).", "~Per l'EEG~: gli spike sono rapidi (≈1 ms) e si allontanano: ++contribuiscono poco++ al segnale di scalpo (tranne l'attività ad alta frequenza).")], X0, 4.5, CW, 2.3, { sz: 17, after: 10 });
}

// 14 ----------------------------------------------------------- sezione sinapsi
section(3, "Synapses: where the EEG is born", "Sinapsi: dove nasce l'EEG");

// 15 ----------------------------------------------------------- trasmissione sinaptica
{
  const s = content(t("Synapses (1)", "Sinapsi (1)"), t("Chemical synaptic transmission, step by step", "La trasmissione sinaptica chimica, passo per passo"),
    { notes: t("Synaptic delay ≈0.5–1 ms. Ca²⁺ entry triggers vesicle fusion (SNARE proteins).", "Ritardo sinaptico ≈0,5–1 ms. L'ingresso di Ca²⁺ innesca la fusione delle vescicole (proteine SNARE).") });
  fig(s, "f17_synapse", X0, Y0, 5.2, 5.0, "c", "Synapse");
  rows(s, [t("The spike reaches the terminal", "Lo spike arriva al terminale"), t("Voltage-gated ++Ca²⁺ channels++ open, Ca²⁺ enters", "Si aprono i ++canali Ca²⁺++ voltaggio-dipendenti, entra Ca²⁺"),
    t("++Vesicles++ fuse and release neurotransmitter", "Le ++vescicole++ si fondono e liberano il neurotrasmettitore"), t("Transmitter binds postsynaptic ++receptors++ (ion channels)", "Il trasmettitore lega i ++recettori++ postsinaptici (canali ionici)"),
    t("Ions flow → *postsynaptic potential* (PSP) lasting ++10–100 ms++", "Scorrono ioni → *potenziale postsinaptico* (PSP) di ++10–100 ms++")], 6.0, Y0, 6.7, 0.82, 0.16, 16, ACC);
}

// 16 ----------------------------------------------------------- EPSP e IPSP
{
  const s = content(t("Synapses (2)", "Sinapsi (2)"), t("Excitatory and inhibitory synapses", "Sinapsi eccitatorie e inibitorie"),
    { notes: t("Simulated alpha-function PSPs (τ = 6 ms). NMDA and GABA_B components are slower (100+ ms).", "PSP simulati a funzione alfa (τ = 6 ms). Le componenti NMDA e GABA_B sono più lente (100+ ms).") });
  fig(s, "f18_epsp_ipsp", X0, Y0, 7.2, 4.7, "l", "EPSP and IPSP");
  text(s, [B("*Excitatory* (mostly ~glutamate~): cation channels (AMPA, NMDA) → ++depolarisation++ = EPSP, moves V toward threshold.", "*Eccitatorie* (soprattutto ~glutammato~): canali cationici (AMPA, NMDA) → ++depolarizzazione++ = EPSP, avvicina V alla soglia."),
    B("*Inhibitory* (mostly ~GABA~): Cl⁻ (GABA_A) or K⁺ (GABA_B) channels → ++hyperpolarisation++ or shunting = IPSP.", "*Inibitorie* (soprattutto ~GABA~): canali Cl⁻ (GABA_A) o K⁺ (GABA_B) → ++iperpolarizzazione++ o shunting = IPSP."),
    B("PSPs are ++graded++ (size ∝ input) and ++slow++: ideal for summation.", "I PSP sono ++graduati++ (ampiezza ∝ input) e ++lenti++: ideali per sommarsi.")], 7.9, Y0 + 0.2, 4.8, 4.6, { sz: 16, after: 12 });
}

// 17 ----------------------------------------------------------- sommazione temporale e spaziale
{
  const s = content(t("Synapses (3)", "Sinapsi (3)"), t("Integration: temporal and spatial summation", "Integrazione: sommazione temporale e spaziale"),
    { notes: t("Leaky integrator with τ = 15 ms, EPSP = 8 mV, threshold −55 mV: 25 Hz input never fires, 90 Hz does.", "Integratore con perdita τ = 15 ms, EPSP = 8 mV, soglia −55 mV: input a 25 Hz non scarica, a 90 Hz sì.") });
  fig(s, "f19_temporal", X0, Y0, 7.4, 3.2, "l", "Temporal summation");
  fig(s, "f20_spatial", 8.4, Y0, 4.3, 3.6, "c", "Spatial summation");
  text(s, [B("*Temporal*: PSPs arriving close in time pile up before they decay → high input rates reach threshold.", "*Temporale*: PSP ravvicinati si accumulano prima di decadere → frequenze di input elevate raggiungono la soglia."),
    B("*Spatial*: PSPs from different synapses add at the soma; IPSPs subtract.", "*Spaziale*: PSP da sinapsi diverse si sommano al soma; gli IPSP sottraggono."),
    B("The ++axon hillock++ decides: fire or not.", "Il ++monticolo assonale++ decide: scaricare o no.")], X0, 5.1, 7.6, 1.7, { sz: 16, after: 8 });
  meta(s, t("a ++committee vote++: yes (EPSP) and no (IPSP) votes, counted by the chair (axon hillock).", "una ++votazione in commissione++: voti sì (EPSP) e no (IPSP), contati dal presidente (monticolo)."), 8.2, 5.2, 4.5, 1.4, 15);
}

// 18 ----------------------------------------------------------- sezione dalle sinapsi all'EEG
section(4, "From synapses to the scalp EEG", "Dalle sinapsi all'EEG di scalpo");

// 19 ----------------------------------------------------------- PSP generano l'EEG
{
  const s = content(t("Synapses → EEG (1)", "Sinapsi → EEG (1)"), t("Why postsynaptic potentials, not spikes, make the EEG", "Perché l'EEG nasce dai potenziali postsinaptici e non dagli spike"),
    { notes: t("Buzsáki, Anastassiou & Koch (2012); Nunez & Srinivasan (2006). High-gamma (>80 Hz) partly reflects spiking.", "Buzsáki, Anastassiou & Koch (2012); Nunez & Srinivasan (2006). L'high-gamma (>80 Hz) riflette in parte gli spike.") });
  fig(s, "f22_decay", X0, Y0, 5.8, 4.7, "l", "Field decay");
  const cw = 2.95;
  [[t("Postsynaptic potential", "Potenziale postsinaptico"), [t("duration 10–100 ms", "durata 10–100 ms"), t("current dipole: field ∝ 1/r²", "dipolo di corrente: campo ∝ 1/r²"), t("++good++ temporal summation", "sommazione temporale ++buona++")], PEACH],
   [t("Action potential", "Potenziale d'azione"), [t("duration ≈1 ms", "durata ≈1 ms"), t("quadrupole: field ∝ 1/r³", "quadrupolo: campo ∝ 1/r³"), t("++poor++ temporal summation", "sommazione temporale ++scarsa++")], TINT]].forEach(([h, items, fill], i) => {
    const x = 6.6 + i * (cw + 0.3);
    card(s, x, Y0 + 0.1, cw, 3.2, fill);
    text(s, [{ t: "~" + h + "~", align: "center" }, ...items.map(v => ({ t: v, b: true }))], x + 0.2, Y0 + 0.2, cw - 0.4, 3.0, { sz: 15, after: 10 });
  });
  note(s, t("Scalp EEG ≈ summed ++postsynaptic++ (dendritic) currents of many synchronous neurons.", "EEG di scalpo ≈ somma delle correnti ++postsinaptiche++ (dendritiche) di molti neuroni sincroni."), 6.6, 5.0, 6.2, 0.9, 16);
}

// 20 ----------------------------------------------------------- pozzi e sorgenti
{
  const s = content(t("Synapses → EEG (2)", "Sinapsi → EEG (2)"), t("Current sinks and sources: the origin of polarity", "Pozzi e sorgenti di corrente: l'origine della polarità"),
    { notes: t("Classic scheme (e.g. Kandel; Speckmann & Elger). Same scalp polarity from superficial EPSP or deep IPSP: polarity is ambiguous.", "Schema classico (es. Kandel; Speckmann & Elger). Stessa polarità di scalpo da EPSP superficiale o IPSP profondo: la polarità è ambigua.") });
  fig(s, "f23_sinksource", X0, Y0, 4.8, 4.9, "c", "Sink and source");
  text(s, [B("An excitatory synapse on the ++apical dendrite++: positive ions enter → extracellular *sink* (−) near the surface.", "Una sinapsi eccitatoria sul ++dendrite apicale++: entrano ioni positivi → *pozzo* extracellulare (−) vicino alla superficie."),
    B("Current exits along the cell (near the soma) → *source* (+) in depth. The loop closes in the extracellular space.", "La corrente esce lungo la cellula (vicino al soma) → *sorgente* (+) in profondità. Il circuito si chiude nello spazio extracellulare."),
    B("Sink above, source below = a ++current dipole++ → surface electrode sees a ~negative~ potential.", "Pozzo sopra, sorgente sotto = un ++dipolo di corrente++ → l'elettrodo di superficie vede un potenziale ~negativo~."),
    B("⚠ An ++IPSP near the soma++ produces the same pattern! ++Polarity alone cannot tell excitation from inhibition.++", "⚠ Un ++IPSP vicino al soma++ produce lo stesso schema! ++La sola polarità non distingue eccitazione e inibizione.++")], 5.8, Y0 + 0.1, 6.9, 5.0, { sz: 16, after: 11 });
}

// 21 ----------------------------------------------------------- piramidali
{
  const s = content(t("Synapses → EEG (3)", "Sinapsi → EEG (3)"), t("Pyramidal neurons are the main EEG generators", "I neuroni piramidali sono i principali generatori dell'EEG"),
    { notes: t("Pyramidal cells ≈70–80% of neocortical neurons; stellate/interneurons ≈20–30% with closed-field geometry.", "Le piramidali sono ≈70–80% dei neuroni neocorticali; stellate/interneuroni ≈20–30% con geometria a campo chiuso.") });
  const cw = (CW - 0.4) / 2;
  card(s, X0, Y0, cw, 3.4, PEACH);
  text(s, [{ t: "~" + t("Pyramidal cells", "Cellule piramidali") + "~", align: "center" },
    B("≈70–80 % of neocortical neurons", "≈70–80 % dei neuroni neocorticali"), B("long apical dendrites, ++parallel++ to each other", "lunghi dendriti apicali ++paralleli++ tra loro"),
    B("perpendicular to the cortical surface (layers III, V)", "perpendicolari alla superficie corticale (strati III, V)"), B("→ open field: they ++add up++", "→ campo aperto: si ++sommano++")], X0 + 0.25, Y0 + 0.1, cw - 0.5, 3.2, { sz: 16, after: 8 });
  card(s, X0 + cw + 0.4, Y0, cw, 3.4, TINT);
  text(s, [{ t: "~" + t("Stellate cells and interneurons", "Cellule stellate e interneuroni") + "~", align: "center" },
    B("≈20–30 % of neocortical neurons", "≈20–30 % dei neuroni neocorticali"), B("radially symmetric dendrites", "dendriti a simmetria radiale"),
    B("strong metabolic activity (visible in PET/fMRI)", "forte attività metabolica (visibile in PET/fMRI)"), B("→ closed field: ++\"ghosts\"++ for the EEG", "→ campo chiuso: ++\"fantasmi\"++ per l'EEG")], X0 + cw + 0.65, Y0 + 0.1, cw - 0.5, 3.2, { sz: 16, after: 8 });
  note(s, t("Different methods see different cells: EEG ≠ fMRI is not an error, it is ++physiology++.", "Metodi diversi vedono cellule diverse: EEG ≠ fMRI non è un errore, è ++fisiologia++."), X0 + 1.0, 5.5, CW - 2.0, 0.85, 17);
}

// 22 ----------------------------------------------------------- sezione talamo
section(5, "Thalamocortical loops and rhythms", "Anelli talamo-corticali e ritmi");

// 23 ----------------------------------------------------------- anello TC
{
  const s = content(t("Rhythms (1)", "Ritmi (1)"), t("The thalamocortical loop: a rhythm generator", "L'anello talamo-corticale: un generatore di ritmi"),
    { notes: t("Steriade, McCormick & Sejnowski (1993) Science 262:679. TRN = thalamic reticular nucleus, GABAergic.", "Steriade, McCormick & Sejnowski (1993) Science 262:679. TRN = nucleo reticolare del talamo, GABAergico.") });
  fig(s, "f25_loop", X0, Y0, 5.6, 4.6, "c", "Thalamocortical loop");
  text(s, [B("*Thalamocortical (TC)* neurons relay sensory information to the cortex (glutamate).", "I neuroni *talamo-corticali (TC)* inviano l'informazione sensoriale alla corteccia (glutammato)."),
    B("The *thalamic reticular nucleus (TRN)* receives collaterals and ++inhibits++ TC cells (GABA).", "Il *nucleo reticolare del talamo (TRN)* riceve collaterali e ++inibisce++ le cellule TC (GABA)."),
    B("Excitation → inhibition → rebound → excitation: the loop ++oscillates++ and paces large cortical populations.", "Eccitazione → inibizione → rimbalzo → eccitazione: l'anello ++oscilla++ e mette al passo ampie popolazioni corticali."),
    B("The cortex does not \"see\" the thalamus directly, but ++the synchronised cortical PSPs it drives++.", "La corteccia non \"vede\" direttamente il talamo, ma ++i PSP corticali sincronizzati che esso induce++.")], 6.5, Y0 + 0.1, 6.2, 4.8, { sz: 16, after: 12 });
}

// 24 ----------------------------------------------------------- modi tonico e burst
{
  const s = content(t("Rhythms (2)", "Ritmi (2)"), t("Tonic vs burst firing: wake and sleep", "Scarica tonica e a burst: veglia e sonno"),
    { notes: t("Llinás & Jahnsen (1982) Nature 297:406: T-type Ca²⁺ low-threshold spike. Schematic traces.", "Llinás & Jahnsen (1982) Nature 297:406: spike a bassa soglia da canali Ca²⁺ di tipo T. Tracciati schematici.") });
  fig(s, "f25_modes", X0, Y0, 6.4, 4.9, "l", "Tonic and burst modes");
  text(s, [B("~Depolarised~ TC cell (wake, arousal): *tonic* firing, faithful relay of sensory input.", "Cellula TC ~depolarizzata~ (veglia): scarica *tonica*, trasmissione fedele dell'input."),
    B("~Hyperpolarised~ TC cell (drowsiness, sleep): T-type Ca²⁺ channels de-inactivate → *low-threshold spike* crowned by a ++burst++.", "Cellula TC ~iperpolarizzata~ (sonnolenza, sonno): i canali Ca²⁺ di tipo T si de-inattivano → *spike a bassa soglia* con un ++burst++."),
    B("Rhythmic bursts synchronise the cortex → ++sleep spindles++ (≈11–16 Hz) and ++delta++ waves.", "Burst ritmici sincronizzano la corteccia → ++fusi del sonno++ (≈11–16 Hz) e onde ++delta++.")], 7.2, Y0 + 0.1, 5.5, 4.8, { sz: 16, after: 12 });
}

// 25 ----------------------------------------------------------- alfa e inibizione
{
  const s = content(t("Rhythms (3)", "Ritmi (3)"), t("Alpha rhythm: a signature of active inhibition", "Il ritmo alfa: una firma di inibizione attiva"),
    { notes: t("Hughes et al. (2004) Neuron 42:253; Lőrincz et al. (2008) J Neurosci 28:660; Klimesch (2012) TICS 16:606; Jensen & Mazaheri (2010) Front Hum Neurosci 4:186; Womelsdorf et al. (2014) Nat Neurosci 17:1031.", "Hughes et al. (2004) Neuron 42:253; Lőrincz et al. (2008) J Neurosci 28:660; Klimesch (2012) TICS 16:606; Jensen & Mazaheri (2010) Front Hum Neurosci 4:186; Womelsdorf et al. (2014) Nat Neurosci 17:1031.") });
  text(s, [B("In the lateral geniculate nucleus a subset of *high-threshold* TC neurons, coupled by gap junctions, bursts at ++alpha/theta++ frequencies (Hughes et al., 2004).", "Nel nucleo genicolato laterale un sottogruppo di neuroni TC *ad alta soglia*, accoppiati da gap junction, scarica a burst a frequenze ++alfa/theta++ (Hughes et al., 2004)."),
    B("They drive GABAergic interneurons that ++rhythmically inhibit++ relay-mode TC neurons: information passes only in ++windows of the alpha cycle++.", "Pilotano interneuroni GABAergici che ++inibiscono ritmicamente++ i neuroni TC in modalità relay: l'informazione passa solo in ++finestre del ciclo alfa++."),
    B("*Gating-by-inhibition* hypothesis: alpha increases over regions that should be ++ignored++ (e.g. visual cortex with eyes closed, unattended hemifield).", "Ipotesi del *gating per inibizione*: l'alfa aumenta sulle regioni da ++ignorare++ (es. corteccia visiva a occhi chiusi, emicampo non attentivo).")], X0, Y0, 7.6, 4.8, { sz: 17, after: 14 });
  meta(s, t("alpha is a ++traffic light++: while it blinks red, the road (the sensory relay) is closed most of the time.", "l'alfa è un ++semaforo++: finché lampeggia rosso, la strada (il relay sensoriale) è chiusa gran parte del tempo."), 8.4, Y0 + 0.2, 4.3, 2.4, 17);
  note(s, t("Link to Lecture 1: ++Berger's alpha blocking++ = release of inhibition when the eyes open.", "Collegamento con la Lezione 1: il ++blocco dell'alfa di Berger++ = rilascio dell'inibizione quando si aprono gli occhi."), 8.4, 4.9, 4.3, 1.4, 16);
}

// 26 ----------------------------------------------------------- domande
{
  const s = content(t("Check your understanding", "Verifica"), t("Three questions", "Tre domande"),
    { notes: t("(1) E_K shifts toward 0 → depolarisation (hyperkalaemia). (2) PSPs: longer and dipolar; spikes brief and quadrupolar. (3) No: superficial EPSP and deep IPSP give the same sign.", "(1) E_K si sposta verso 0 → depolarizzazione (iperkaliemia). (2) PSP: più lunghi e dipolari; spike brevi e quadrupolari. (3) No: EPSP superficiale e IPSP profondo danno lo stesso segno.") });
  rows(s, [t("Extracellular K⁺ doubles (5 → 10 mM). What happens to E_K and to the resting potential?", "Il K⁺ extracellulare raddoppia (5 → 10 mM). Che cosa succede a E_K e al potenziale di riposo?"),
    t("Give two physical reasons why PSPs, and not spikes, dominate the scalp EEG.", "Dai due ragioni fisiche per cui i PSP, e non gli spike, dominano l'EEG di scalpo."),
    t("A negative wave appears at Fz. Can you conclude that the frontal cortex is excited?", "Compare un'onda negativa in Fz. Puoi concludere che la corteccia frontale è eccitata?")], X0, Y0 + 0.2, CW, 1.2, 0.35, 19, ACC);
}

// 27 ----------------------------------------------------------- take home
{
  const s = content(t("Take-home messages", "Messaggi chiave"), t("Take-home messages", "Messaggi chiave"));
  rows(s, [t("Ion gradients + selective permeability = ++membrane potential++ (Nernst, GHK; rest ≈ −65 mV).", "Gradienti ionici + permeabilità selettiva = ++potenziale di membrana++ (Nernst, GHK; riposo ≈ −65 mV)."),
    t("Spikes are ++all-or-none++, brief (≈1 ms), regenerative (HH).", "Gli spike sono ++tutto-o-nulla++, brevi (≈1 ms), rigenerativi (HH)."),
    t("PSPs are ++graded++ and ++slow++ (10–100 ms): they sum in time and space.", "I PSP sono ++graduati++ e ++lenti++ (10–100 ms): si sommano nel tempo e nello spazio."),
    t("Synchronous PSPs in aligned ++pyramidal++ cells create sink–source ++dipoles++ → EEG. Polarity is ambiguous.", "PSP sincroni in cellule ++piramidali++ allineate creano ++dipoli++ pozzo–sorgente → EEG. La polarità è ambigua."),
    t("++Thalamocortical loops++ pace the cortex: tonic vs burst modes, spindles, delta, alpha.", "Gli ++anelli talamo-corticali++ scandiscono la corteccia: modi tonico e burst, fusi, delta, alfa.")], X0, Y0, CW, 0.85, 0.15, 17);
}

// 28 ----------------------------------------------------------- letture
{
  const s = content(t("Suggested reading", "Letture consigliate"), t("Suggested reading", "Letture consigliate"));
  text(s, [
    { t: "Kandel E.R. et al. (2021) *Principles of Neural Science*, 6th ed. McGraw-Hill — chapters on membrane potential, action potential, synaptic integration.", b: true },
    { t: "Hille B. (2001) *Ion Channels of Excitable Membranes*, 3rd ed. Sinauer.", b: true },
    { t: "Hodgkin A.L., Huxley A.F. (1952) A quantitative description of membrane current… *J Physiol* 117:500–544.", b: true },
    { t: "Buzsáki G., Anastassiou C.A., Koch C. (2012) The origin of extracellular fields and currents. *Nat Rev Neurosci* 13:407–420.", b: true },
    { t: "Steriade M., McCormick D.A., Sejnowski T.J. (1993) Thalamocortical oscillations in the sleeping and aroused brain. *Science* 262:679–685.", b: true },
    { t: "Llinás R., Jahnsen H. (1982) Electrophysiology of mammalian thalamic neurones in vitro. *Nature* 297:406–408.", b: true },
    { t: "Hughes S.W. et al. (2004) Synchronized oscillations at α and θ frequencies in the lateral geniculate nucleus. *Neuron* 42:253–268.", b: true },
    { t: "Klimesch W. (2012) α-band oscillations, attention, and controlled access to stored information. *Trends Cogn Sci* 16:606–617.", b: true },
    { t: "Womelsdorf T. et al. (2014) Dynamic circuit motifs underlying rhythmic gain control, gating and integration. *Nat Neurosci* 17:1031–1039.", b: true }], X0, Y0, CW, 5.0, { sz: 14, after: 7 });
}

save(OUT);
