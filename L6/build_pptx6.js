// EEG – Lecture 6: spectral and time-frequency analysis (bilingue: node build_pptx6.js en|it)
const __R = (function () { const p = require("path"), fs = require("fs"); let d = process.env.COURSE_ROOT || __dirname;
  while (!fs.existsSync(p.join(d, ".course_root")) && p.dirname(d) !== d) d = p.dirname(d); return d; })();
const LANGARG = process.argv[2] || "en";
global.CFG = { lang: LANGARG, fig: __R + "/L6/figpng_" + LANGARG, common: __R + "/common",
  footer: LANGARG === "it" ? "Brain Imaging · EEG · Lezione 6 · Analisi spettrale e tempo-frequenza" : "Brain Imaging · EEG · Lecture 6 · Spectral and time-frequency analysis",
  lezione: LANGARG === "it" ? "Lezione 6" : "Lecture 6",
  titolo: LANGARG === "it" ? "Analisi spettrale\ne tempo-frequenza" : "Spectral and\ntime-frequency analysis", titoloSize: 42 };
const L = require(__R + "/common/pptlib_eeg.js");
const { tr: t, pres, fig, content, text, formula, card, badge, copertina, save } = L;
const { INK, ACC, TEAL, TXT, MUTED, TINT, WHITE, SERIF, SANS, W, H, MX, X0, Y0, CW } = L.C;
const OUT = process.argv[3] || `${__R}/L6/out/EEG_L6_${LANGARG}.pptx`;
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
  const s = content(t("Lecture 6", "Lezione 6"), t("Today: rhythms as numbers", "Oggi: i ritmi diventano numeri"),
    { notes: t("Main reference: Cohen M.X. (2014) Analyzing Neural Time Series Data, MIT Press — with MATLAB code for every method.", "Riferimento principale: Cohen M.X. (2014) Analyzing Neural Time Series Data, MIT Press — con codice MATLAB per ogni metodo.") });
  rows(s, [t("The ++Fourier transform++: resolution, Nyquist, leakage, windows.", "La ++trasformata di Fourier++: risoluzione, Nyquist, leakage, finestre."),
    t("*Power spectrum* estimation: Welch, multitaper, 1/f vs peaks.", "Stima dello *spettro di potenza*: Welch, multitaper, 1/f vs picchi."),
    t("*Time-frequency* analysis: STFT, Morlet wavelets, baseline, ERD/ERS.", "Analisi *tempo-frequenza*: STFT, wavelet di Morlet, baseline, ERD/ERS."),
    t("*Evoked* vs *induced* activity; ++phase++ and ITPC.", "Attività *evocata* vs *indotta*; ++fase++ e ITPC."),
    t("++Cross-frequency coupling++ and common pitfalls.", "++Accoppiamento tra frequenze++ e trappole comuni.")], X0, Y0, CW, 0.85, 0.15, 18);
}

// 3 perché le frequenze
{
  const s = content(t("Why frequency?", "Perché la frequenza?"), t("The EEG speaks in rhythms", "L'EEG parla per ritmi"),
    { notes: t("Buzsáki (2006) Rhythms of the Brain. Oscillations reflect synchronised activity of neural populations (Lecture 3); different bands have different generators and functional correlates.", "Buzsáki (2006) Rhythms of the Brain. Le oscillazioni riflettono attività sincronizzata di popolazioni neurali (Lezione 3); bande diverse hanno generatori e correlati funzionali diversi.") });
  rows(s, [t("Oscillations are ++synchronised population activity++ (Lecture 3): their frequency tells us about the circuit.", "Le oscillazioni sono ++attività sincronizzata di popolazione++ (Lezione 3): la frequenza informa sul circuito."),
    t("Different bands, different ++functions++: alpha and attention, beta and movement, theta and memory, gamma and local processing.", "Bande diverse, ++funzioni++ diverse: alfa e attenzione, beta e movimento, theta e memoria, gamma ed elaborazione locale."),
    t("The spectrum is a ++compact description++ of long recordings (resting state, sleep, clinical EEG).", "Lo spettro è una ++descrizione compatta++ di registrazioni lunghe (riposo, sonno, EEG clinico)."),
    t("Time-frequency shows ++when++ rhythms change: activity ++not phase-locked++ is invisible in the ERP.", "Il tempo-frequenza mostra ++quando++ cambiano i ritmi: l'attività ++non agganciata in fase++ è invisibile nell'ERP.")], X0, Y0, CW, 0.95, 0.15, 17);
  meta(s, t("a ++prism++ splits white light into colours; the Fourier transform splits the EEG into rhythms.", "un ++prisma++ scompone la luce bianca nei colori; la trasformata di Fourier scompone l'EEG nei ritmi."), X0, 6.15, CW, 0.6, 15);
}

section(1, "From time to frequency", "Dal tempo alla frequenza");

// 5 Fourier
{
  const s = content(t("Fourier (1)", "Fourier (1)"), t("Any signal is a sum of sinusoids", "Ogni segnale è una somma di sinusoidi"),
    { notes: t("Fourier (1822). DFT: X(f_k) = Σ_n x(n) e^(−i2πkn/N). Each complex coefficient has an amplitude |X| and a phase ∠X. Power = |X|². In MATLAB: X = fft(x)/N; f = (0:N-1)*fs/N.", "Fourier (1822). DFT: X(f_k) = Σ_n x(n) e^(−i2πkn/N). Ogni coefficiente complesso ha un'ampiezza |X| e una fase ∠X. Potenza = |X|². In MATLAB: X = fft(x)/N; f = (0:N-1)*fs/N.") });
  fig(s, "f05_fourier", X0, Y0, 7.2, 3.8, "l", "Fourier decomposition");
  formula(s, "X(f) = Σ_{n} x(n) · e^{−i2πfn / fs}", 8.0, Y0, 4.7, 0.8, { sz: 20, fill: PEACH });
  text(s, [B("Each frequency has an ++amplitude++ |X(f)| and a ++phase++ ∠X(f).", "Ogni frequenza ha un'++ampiezza++ |X(f)| e una ++fase++ ∠X(f)."),
    B("*Power* = |X(f)|²: how much variance lives at each frequency.", "*Potenza* = |X(f)|²: quanta varianza sta a ogni frequenza."),
    B("The transform is ++linear and invertible++: no information is lost.", "La trasformata è ++lineare e invertibile++: nessuna informazione si perde."),
    B("MATLAB: X = fft(x); P = abs(X).^2.", "MATLAB: X = fft(x); P = abs(X).^2.")], 8.0, 2.6, 4.7, 3.8, { sz: 16, after: 12 });
}

// 6 risoluzione
{
  const s = content(t("Fourier (2)", "Fourier (2)"), t("Frequency resolution: Δf = 1/T", "Risoluzione in frequenza: Δf = 1/T"),
    { notes: t("The frequency spacing of the DFT is fs/N = 1/T. Zero-padding interpolates the spectrum but does not increase the true resolution. Two peaks closer than ~1/T cannot be separated.", "La spaziatura in frequenza della DFT è fs/N = 1/T. Lo zero-padding interpola lo spettro ma non aumenta la vera risoluzione. Due picchi più vicini di ~1/T non si separano.") });
  fig(s, "f06_resolution", X0, Y0, CW, 2.95, "c", "Frequency resolution");
  formula(s, "Δf = 1 / T          f_{max} = f_{s} / 2", X0 + 3.0, 4.85, CW - 6.0, 0.7, { sz: 22, fill: PEACH });
  text(s, [B("Longer windows → ++finer++ frequency resolution; the sampling rate sets only the ++maximum++ frequency.", "Finestre più lunghe → risoluzione ++più fine++; la frequenza di campionamento fissa solo la frequenza ++massima++."),
    B("Zero-padding makes the plot smoother but ++does not add resolution++.", "Lo zero-padding rende il grafico più liscio ma ++non aggiunge risoluzione++.")], X0, 5.7, CW, 1.0, { sz: 16, after: 6 });
}

// 7 leakage
{
  const s = content(t("Fourier (3)", "Fourier (3)"), t("Spectral leakage and tapers", "Leakage spettrale e finestre"),
    { notes: t("Cutting a signal is multiplying it by a rectangular window: in frequency this convolves the spectrum with a sinc, whose side lobes spread power (leakage). Tapers (Hann, Hamming) trade a wider main lobe for much lower side lobes (Harris, 1978).", "Tagliare un segnale equivale a moltiplicarlo per una finestra rettangolare: in frequenza lo spettro viene convoluto con una sinc, i cui lobi laterali disperdono potenza (leakage). Le finestre (Hann, Hamming) scambiano un lobo principale più largo con lobi laterali molto più bassi (Harris, 1978).") });
  fig(s, "f07_leakage", X0, Y0, 7.0, 4.0, "l", "Leakage");
  text(s, [B("A segment ++cut abruptly++ (rectangular window) spreads power to all frequencies: *leakage*.", "Un segmento ++tagliato di netto++ (finestra rettangolare) disperde potenza su tutte le frequenze: *leakage*."),
    B("*Tapers* (Hann, Hamming) fade the edges: side lobes drop by ≈ 30–40 dB, the main peak widens.", "Le *finestre* (Hann, Hamming) sfumano i bordi: i lobi laterali calano di ≈ 30–40 dB, il picco principale si allarga."),
    B("Always taper before the FFT (pwelch does it for you).", "Applicare sempre una finestra prima della FFT (pwelch lo fa per te).")], 7.8, Y0, 4.9, 4.4, { sz: 16, after: 12 });
  meta(s, t("a ++photo with a hard frame++ creates false edges; a soft vignette keeps the attention on the subject.", "una ++foto con cornice netta++ crea falsi bordi; una sfumatura morbida lascia l'attenzione sul soggetto."), X0, 6.2, CW, 0.55, 15);
}

section(2, "Estimating the power spectrum", "Stimare lo spettro di potenza");

// 9 Welch
{
  const s = content(t("Spectrum (1)", "Spettro (1)"), t("Welch's method: average to reduce variance", "Metodo di Welch: mediare per ridurre la varianza"),
    { notes: t("Welch (1967) IEEE Trans Audio Electroacoust 15:70. The raw periodogram is an inconsistent estimator: its variance does not decrease with longer data. Averaging K segments reduces variance ~1/K at the cost of resolution (1/segment length).", "Welch (1967) IEEE Trans Audio Electroacoust 15:70. Il periodogramma grezzo è uno stimatore inconsistente: la sua varianza non cala con dati più lunghi. Mediare K segmenti riduce la varianza ~1/K al costo della risoluzione (1/lunghezza del segmento).") });
  fig(s, "f09_welch", X0, Y0, 5.8, 4.6, "l", "Welch");
  text(s, [B("The single periodogram is ++noisy++: its variance does not shrink with longer recordings.", "Il periodogramma singolo è ++rumoroso++: la sua varianza non cala con registrazioni più lunghe."),
    B("*Welch*: cut into overlapping segments (e.g. 2 s, 50 %), taper, FFT each, ++average++ the power.", "*Welch*: tagliare in segmenti sovrapposti (es. 2 s, 50 %), finestrare, FFT di ciascuno, ++mediare++ la potenza."),
    B("Trade-off: shorter segments = ++more averages++ but ++coarser++ resolution.", "Compromesso: segmenti più corti = ++più medie++ ma risoluzione ++più grossolana++."),
    B("MATLAB: [pxx,f] = pwelch(x, hann(2*fs), fs, [], fs);", "MATLAB: [pxx,f] = pwelch(x, hann(2*fs), fs, [], fs);")], 6.7, Y0, 6.0, 4.8, { sz: 16, after: 12 });
}

// 10 multitaper e unità
{
  const s = content(t("Spectrum (2)", "Spettro (2)"), t("Multitaper and units", "Multitaper e unità di misura"),
    { notes: t("Thomson (1982) Proc IEEE 70:1055; Percival & Walden (1993); Prerau et al. (2017) Physiology 32:60 for sleep. dB = 10·log10(P/Pref).", "Thomson (1982) Proc IEEE 70:1055; Percival & Walden (1993); Prerau et al. (2017) Physiology 32:60 per il sonno. dB = 10·log10(P/Pref).") });
  cards(s, [[t("Multitaper", "Multitaper"), t("Several orthogonal tapers (Slepian) on the ++same++ data, averaged: low variance with controlled smoothing ±W Hz (Thomson, 1982). Ideal for gamma and sleep.", "Più finestre ortogonali (Slepian) sugli ++stessi++ dati, mediate: bassa varianza con smoothing controllato ±W Hz (Thomson, 1982). Ideale per gamma e sonno.")],
    [t("Absolute power", "Potenza assoluta"), t("µV²/Hz (density) or µV² (band). Depends on skull, impedance, reference.", "µV²/Hz (densità) o µV² (banda). Dipende da cranio, impedenza, riferimento.")],
    [t("Relative power", "Potenza relativa"), t("band / total power (e.g. 1–40 Hz): removes global scaling but bands become ++interdependent++.", "banda / potenza totale (es. 1–40 Hz): toglie la scala globale ma le bande diventano ++interdipendenti++.")],
    [t("Logarithmic", "Logaritmica"), t("log10 or dB = 10·log10(P/P_{ref}): power is ++skewed++; logs make it closer to Gaussian for statistics.", "log10 o dB = 10·log10(P/P_{ref}): la potenza è ++asimmetrica++; i log la avvicinano alla gaussiana per la statistica.")]], Y0, 3.0, 15);
  note(s, t("Report: method, segment length, overlap, taper, frequency resolution, units. ~Plot spectra on log axes.~", "Riportare: metodo, lunghezza dei segmenti, sovrapposizione, finestra, risoluzione, unità. ~Mostrare gli spettri su assi logaritmici.~"), X0, 4.9, CW, 0.9, 16);
}

// 11 periodico vs aperiodico
{
  const s = content(t("Spectrum (3)", "Spettro (3)"), t("Peaks on a 1/f background", "Picchi su un fondo 1/f"),
    { notes: t("Donoghue et al. (2020) Nat Neurosci 23:1655 — specparam (formerly FOOOF). The aperiodic exponent χ has been linked to excitation/inhibition balance (Gao, Peterson & Voytek, 2017) and changes with age (Voytek et al., 2015).", "Donoghue et al. (2020) Nat Neurosci 23:1655 — specparam (già FOOOF). L'esponente aperiodico χ è stato collegato al bilancio eccitazione/inibizione (Gao, Peterson & Voytek, 2017) e cambia con l'età (Voytek et al., 2015).") });
  fig(s, "f11_fooof", X0, Y0, CW, 2.75, "c", "Aperiodic and periodic");
  formula(s, "log P(f) = b − log(k + f^{χ}) + Σ gaussian peaks", X0 + 2.5, 4.6, CW - 5.0, 0.7, { sz: 20, fill: PEACH });
  text(s, [B("A change in \"band power\" can come from a ++peak++ or from a change of ++slope/offset++ of the background.", "Un cambiamento di \"potenza di banda\" può venire da un ++picco++ o da un cambiamento di ++pendenza/offset++ del fondo."),
    B("*specparam/FOOOF* separates the two (Donoghue et al., 2020); χ has been linked to the ++E/I balance++ and ageing.", "*specparam/FOOOF* separa le due parti (Donoghue et al., 2020); χ è stato collegato al ++bilancio E/I++ e all'invecchiamento.")], X0, 5.45, CW, 1.3, { sz: 16, after: 6 });
}

// 12 potenza di banda e IAF
{
  const s = content(t("Spectrum (4)", "Spettro (4)"), t("Band power and individual frequencies", "Potenza di banda e frequenze individuali"),
    { notes: t("Klimesch (1999) Brain Res Rev 29:169 — individual alpha frequency (IAF) and adjusted bands. Corcoran et al. (2018) Psychophysiology 55:e13064 — automated IAF estimation. Alpha asymmetry: Allen et al. (2004).", "Klimesch (1999) Brain Res Rev 29:169 — frequenza alfa individuale (IAF) e bande adattate. Corcoran et al. (2018) Psychophysiology 55:e13064 — stima automatica della IAF. Asimmetria alfa: Allen et al. (2004).") });
  formula(s, "P_{band} = Σ_{f ∈ band} P(f) · Δf", X0 + 3.2, Y0, CW - 6.4, 0.75, { sz: 22, fill: PEACH });
  rows(s, [t("Fixed bands (δ, θ, α, β, γ) are ++conventions++: people differ (IAF ≈ 8–12 Hz, decreasing with age).", "Le bande fisse (δ, θ, α, β, γ) sono ++convenzioni++: le persone differiscono (IAF ≈ 8–12 Hz, cala con l'età)."),
    t("*Individual alpha frequency* (peak or centre of gravity) → ++individually adjusted bands++ (Klimesch, 1999).", "*Frequenza alfa individuale* (picco o baricentro) → ++bande adattate all'individuo++ (Klimesch, 1999)."),
    t("Ratios (θ/β, α asymmetry) are popular but ++fragile++: check both numerator and denominator.", "I rapporti (θ/β, asimmetria α) sono diffusi ma ++fragili++: controllare numeratore e denominatore."),
    t("Always ++look at the spectrum++ before extracting numbers.", "~Guardare sempre lo spettro~ prima di estrarre numeri.")], X0, 2.5, CW, 0.85, 0.15, 17);
}

section(3, "Time-frequency analysis", "Analisi tempo-frequenza");

// 14 STFT
{
  const s = content(t("Time-frequency (1)", "Tempo-frequenza (1)"), t("STFT and the time–frequency trade-off", "STFT e il compromesso tempo–frequenza"),
    { notes: t("Gabor (1946): Δt·Δf ≥ 1/(4π). A window cannot be sharp in both time and frequency. The STFT uses the same window for all frequencies; wavelets adapt it.", "Gabor (1946): Δt·Δf ≥ 1/(4π). Una finestra non può essere nitida sia nel tempo sia in frequenza. La STFT usa la stessa finestra per tutte le frequenze; le wavelet la adattano.") });
  fig(s, "f14_stft", X0, Y0, CW, 3.4, "c", "STFT");
  formula(s, "Δt · Δf ≥ 1 / 4π", X0 + 4.3, 5.15, CW - 8.6, 0.65, { sz: 22, fill: PEACH });
  text(s, [B("Slide a window, FFT each position: ++short++ windows localise bursts, ++long++ windows separate frequencies.", "Far scorrere una finestra e fare la FFT in ogni posizione: finestre ++corte++ localizzano i burst, finestre ++lunghe++ separano le frequenze.")], X0, 6.0, CW, 0.6, { sz: 16, align: "center" });
}

// 15 Morlet
{
  const s = content(t("Time-frequency (2)", "Tempo-frequenza (2)"), t("Morlet wavelets: a window that scales with frequency", "Wavelet di Morlet: una finestra che scala con la frequenza"),
    { notes: t("Complex Morlet wavelet: w(t) = exp(i2πft)·exp(−t²/2σ²), σ = n/(2πf). Convolution of the signal with w gives a complex time series: |·|² = power, angle = phase. Cohen (2019) NeuroImage 199:81 recommends defining wavelets by their FWHM.", "Wavelet di Morlet complessa: w(t) = exp(i2πft)·exp(−t²/2σ²), σ = n/(2πf). La convoluzione del segnale con w dà una serie complessa: |·|² = potenza, angolo = fase. Cohen (2019) NeuroImage 199:81 raccomanda di definire le wavelet tramite la FWHM.") });
  fig(s, "f15_morlet", X0, Y0, CW, 2.2, "c", "Morlet wavelets");
  formula(s, "w(t) = e^{i2πft} · e^{−t²/2σ²},    σ_{t} = n / 2πf", X0 + 2.0, 4.05, CW - 4.0, 0.7, { sz: 21, fill: PEACH });
  text(s, [B("A *Morlet wavelet* is a sine wave under a Gaussian: n cycles at every frequency → ++short at high f, long at low f++.", "Una *wavelet di Morlet* è una sinusoide sotto una gaussiana: n cicli a ogni frequenza → ++corta alle alte f, lunga alle basse f++."),
    B("*Convolution* with the complex wavelet → at each time: ++power++ = |z|², ++phase++ = ∠z.", "*Convoluzione* con la wavelet complessa → in ogni istante: ++potenza++ = |z|², ++fase++ = ∠z."),
    B("Fast in practice: multiply in the frequency domain (FFT) and invert.", "Veloce in pratica: moltiplicare nel dominio delle frequenze (FFT) e invertire.")], X0, 4.95, CW, 1.8, { sz: 16, after: 8 });
}

// 16 numero di cicli
{
  const s = content(t("Time-frequency (3)", "Tempo-frequenza (3)"), t("How many cycles?", "Quanti cicli?"),
    { notes: t("Typical choice: n increasing from 3 (low f) to 10 (high f), log-spaced frequencies. Report FWHM in time and frequency (Cohen, 2019). Edge effects: epochs must be longer than the analysis window by ~1.5 wavelet lengths on each side.", "Scelta tipica: n crescente da 3 (basse f) a 10 (alte f), frequenze spaziate logaritmicamente. Riportare la FWHM in tempo e in frequenza (Cohen, 2019). Effetti di bordo: le epoche devono superare la finestra d'analisi di ~1,5 lunghezze della wavelet per lato.") });
  cards(s, [[t("n ≈ 3", "n ≈ 3"), t("good ++temporal++ precision, poor frequency precision: transient events.", "buona precisione ++temporale++, scarsa in frequenza: eventi transitori.")],
    [t("n ≈ 7", "n ≈ 7"), t("balanced: the usual compromise for 4–40 Hz.", "bilanciato: il compromesso abituale per 4–40 Hz.")],
    [t("n ≈ 12+", "n ≈ 12+"), t("good ++frequency++ precision, blurred in time: sustained rhythms, SSVEP.", "buona precisione in ++frequenza++, sfocato nel tempo: ritmi sostenuti, SSVEP.")]], Y0, 2.0, 16);
  rows(s, [t("Common choice: frequencies ++log-spaced++, cycles increasing ++3 → 10++ with frequency.", "Scelta comune: frequenze ++spaziate logaritmicamente++, cicli crescenti ++3 → 10++ con la frequenza."),
    t("Report the ++FWHM++ in time and frequency, not only \"n cycles\" (Cohen, 2019).", "Riportare la ++FWHM++ in tempo e frequenza, non solo \"n cicli\" (Cohen, 2019)."),
    t("*Edge effects*: epochs must extend ≈ 1.5 wavelet lengths beyond the window of interest.", "*Effetti di bordo*: le epoche devono estendersi ≈ 1,5 lunghezze di wavelet oltre la finestra d'interesse.")], X0, 3.8, CW, 0.8, 0.15, 16, ACC);
}

// 17 mappa TF e baseline
{
  const s = content(t("Time-frequency (4)", "Tempo-frequenza (4)"), t("The time-frequency map and baseline normalisation", "La mappa tempo-frequenza e la normalizzazione alla baseline"),
    { notes: t("Pfurtscheller & Lopes da Silva (1999) Clin Neurophysiol 110:1842 (ERD/ERS). Raw power is dominated by low frequencies (1/f): normalise to a pre-stimulus baseline. dB: 10·log10(P/Pbase); percentage: 100·(P−Pbase)/Pbase; z-score. Grandchamp & Delorme (2011) Front Psychol 2:236 on single-trial normalisation.", "Pfurtscheller & Lopes da Silva (1999) Clin Neurophysiol 110:1842 (ERD/ERS). La potenza grezza è dominata dalle basse frequenze (1/f): normalizzare a una baseline pre-stimolo. dB: 10·log10(P/Pbase); percentuale: 100·(P−Pbase)/Pbase; z-score. Grandchamp & Delorme (2011) Front Psychol 2:236 sulla normalizzazione a singolo trial.") });
  fig(s, "f17_tfmap", X0, Y0, 7.2, 4.4, "l", "Time-frequency map");
  formula(s, "dB(t,f) = 10 · log_{10} [ P(t,f) / P_{base}(f) ]", 7.8, Y0, 4.9, 0.8, { sz: 17, fill: PEACH });
  text(s, [B("Raw power follows ++1/f++: normalise each frequency to a pre-stimulus *baseline*.", "La potenza grezza segue ++1/f++: normalizzare ogni frequenza a una *baseline* pre-stimolo."),
    B("*ERD* (decrease, blue) and *ERS* (increase, red): e.g. alpha/beta ERD during movement, beta rebound after it.", "*ERD* (diminuzione, blu) ed *ERS* (aumento, rosso): es. ERD alfa/beta durante il movimento, rebound beta dopo."),
    B("dB, % change or z-score: choose one and report it.", "dB, variazione % o z-score: sceglierne uno e riportarlo.")], 7.8, 2.6, 4.9, 3.8, { sz: 15, after: 10 });
}

// 18 evocato vs indotto
{
  const s = content(t("Time-frequency (5)", "Tempo-frequenza (5)"), t("Evoked versus induced activity", "Attività evocata e indotta"),
    { notes: t("Tallon-Baudry & Bertrand (1999) Trends Cogn Sci 3:151. Total power = average of single-trial power; evoked power = power of the ERP; induced ≈ total − evoked (or power after subtracting the ERP from each trial).", "Tallon-Baudry & Bertrand (1999) Trends Cogn Sci 3:151. Potenza totale = media della potenza dei singoli trial; potenza evocata = potenza dell'ERP; indotta ≈ totale − evocata (o potenza dopo aver sottratto l'ERP da ogni trial).") });
  fig(s, "f18_evoked_induced", X0, Y0, 7.6, 4.6, "l", "Evoked vs induced");
  text(s, [B("*Evoked*: same latency and ++phase++ in every trial → survives averaging (ERP).", "*Evocata*: stessa latenza e ++fase++ in ogni trial → sopravvive alla media (ERP)."),
    B("*Induced*: time-locked but ++phase-jittered++ → cancels in the ERP, visible only in ++single-trial power++.", "*Indotta*: agganciata nel tempo ma con ++fase variabile++ → si cancella nell'ERP, visibile solo nella ++potenza dei singoli trial++."),
    B("Order matters: ++power then average++ (total) ≠ ++average then power++ (evoked).", "L'ordine conta: ++potenza poi media++ (totale) ≠ ++media poi potenza++ (evocata).")], 8.3, Y0, 4.4, 4.8, { sz: 15, after: 12 });
}

section(4, "Phase and coupling", "Fase e accoppiamento");

// 20 Hilbert
{
  const s = content(t("Phase (1)", "Fase (1)"), t("Band-pass + Hilbert: amplitude and phase over time", "Passa-banda + Hilbert: ampiezza e fase nel tempo"),
    { notes: t("The analytic signal z(t) = x(t) + i·H[x](t). Meaningful only for narrow-band signals: filter first. Equivalent in practice to complex wavelet convolution (Bruns, 2004).", "Il segnale analitico z(t) = x(t) + i·H[x](t). Ha senso solo per segnali a banda stretta: prima filtrare. In pratica equivalente alla convoluzione con wavelet complesse (Bruns, 2004).") });
  fig(s, "f21_hilbert", X0, Y0, CW, 3.0, "c", "Hilbert transform");
  formula(s, "z(t) = x(t) + i·H[x](t) = A(t) · e^{iφ(t)}", X0 + 2.8, 4.95, CW - 5.6, 0.7, { sz: 21, fill: PEACH });
  text(s, [B("Filter in a ++narrow band++, then the *analytic signal* gives the instantaneous ++amplitude++ (envelope) and ++phase++.", "Filtrare in una ++banda stretta++, poi il *segnale analitico* dà ++ampiezza++ (inviluppo) e ++fase++ istantanee.")], X0, 5.8, CW, 0.7, { sz: 16, align: "center" });
}

// 21 ITPC
{
  const s = content(t("Phase (2)", "Fase (2)"), t("Inter-trial phase coherence", "Coerenza di fase tra trial"),
    { notes: t("ITPC (also phase-locking factor, PLF): Tallon-Baudry et al. (1996) J Neurosci 16:4240. Biased by the number of trials: expected value under the null ≈ 1/√N. Compare conditions with equal trial numbers or use Rayleigh's Z = N·ITPC².", "ITPC (o phase-locking factor, PLF): Tallon-Baudry et al. (1996) J Neurosci 16:4240. Distorta dal numero di trial: valore atteso sotto l'ipotesi nulla ≈ 1/√N. Confrontare condizioni con lo stesso numero di trial o usare la Z di Rayleigh = N·ITPC².") });
  fig(s, "f20_itpc", X0, Y0, 6.4, 3.6, "l", "ITPC");
  formula(s, "ITPC(t,f) = | (1/N) Σ_{k} e^{iφk(t,f)} |", 7.2, Y0, 5.5, 0.8, { sz: 19, fill: PEACH });
  text(s, [B("Each trial's phase is a ++unit vector++; average them: length 0 = random, 1 = perfectly aligned.", "La fase di ogni trial è un ++vettore unitario++; mediarli: lunghezza 0 = casuale, 1 = perfettamente allineata."),
    B("Independent of power: measures ++phase resetting / locking++ by the stimulus.", "Indipendente dalla potenza: misura il ++reset / aggancio di fase++ dovuto allo stimolo."),
    B("⚠ Biased by the number of trials (null ≈ 1/√N): ++equalise trial counts++.", "⚠ Distorta dal numero di trial (nullo ≈ 1/√N): ++pareggiare il numero di trial++.")], 7.2, 2.6, 5.5, 3.6, { sz: 16, after: 12 });
  meta(s, t("a ++rowing crew++: each rower has strength (amplitude), but the boat moves only if strokes are in phase.", "un ++equipaggio di canottaggio++: ogni rematore ha la sua forza (ampiezza), ma la barca va solo se le remate sono in fase."), X0, 6.2, CW, 0.55, 15);
}

// 22 PAC
{
  const s = content(t("Phase (3)", "Fase (3)"), t("Cross-frequency coupling: phase–amplitude", "Accoppiamento tra frequenze: fase–ampiezza"),
    { notes: t("Canolty et al. (2006) Science 313:1626; Tort et al. (2010) J Neurophysiol 104:1195 (modulation index). Pitfalls: non-sinusoidal waveforms and sharp edges produce spurious PAC (Aru et al., 2015 Curr Opin Neurobiol; Cole & Voytek, 2017 Trends Cogn Sci).", "Canolty et al. (2006) Science 313:1626; Tort et al. (2010) J Neurophysiol 104:1195 (indice di modulazione). Trappole: forme d'onda non sinusoidali e fronti ripidi producono PAC spurio (Aru et al., 2015 Curr Opin Neurobiol; Cole & Voytek, 2017 Trends Cogn Sci).") });
  fig(s, "f22_pac", X0, Y0, CW, 3.1, "c", "Phase-amplitude coupling");
  text(s, [B("*PAC*: the ++amplitude++ of a fast rhythm (gamma) depends on the ++phase++ of a slow one (theta) (Canolty et al., 2006).", "*PAC*: l'++ampiezza++ di un ritmo veloce (gamma) dipende dalla ++fase++ di uno lento (theta) (Canolty et al., 2006)."),
    B("Quantified by the *modulation index* (Tort et al., 2010): how far the amplitude-by-phase histogram is from flat.", "Quantificato dall'*indice di modulazione* (Tort et al., 2010): quanto l'istogramma ampiezza-per-fase si discosta dal piatto."),
    B("⚠ Sharp, non-sinusoidal waves create ++spurious PAC++: inspect the raw waveform (Cole & Voytek, 2017).", "⚠ Onde ripide e non sinusoidali creano ++PAC spurio++: ispezionare la forma d'onda grezza (Cole & Voytek, 2017).")], X0, 4.9, CW, 1.8, { sz: 16, after: 8 });
}

// 23 MATLAB
{
  const s = content(t("In MATLAB", "In MATLAB"), t("Welch spectrum and Morlet wavelet convolution", "Spettro di Welch e convoluzione con wavelet di Morlet"),
    { notes: t("Adapted from Cohen (2014) Analyzing Neural Time Series Data, ch. 12–13 and 19. EEG is an EEGLAB structure with epochs; chan = channel index. FieldTrip equivalent: ft_freqanalysis with cfg.method = 'wavelet' or 'mtmconvol'.", "Adattato da Cohen (2014) Analyzing Neural Time Series Data, cap. 12–13 e 19. EEG è una struttura EEGLAB a epoche; chan = indice del canale. Equivalente FieldTrip: ft_freqanalysis con cfg.method = 'wavelet' o 'mtmconvol'.") });
  card(s, X0, Y0, CW, 5.1, TINT);
  const code = [
    "fs = EEG.srate;  x = squeeze(EEG.data(chan,:,:));            % time x trials",
    "[pxx, f] = pwelch(x(:), hann(2*fs), fs, [], fs);             % Welch: 2-s Hann, 50% overlap",
    "frex = logspace(log10(2), log10(40), 30);                    % 2-40 Hz, log-spaced",
    "ncyc = logspace(log10(3), log10(10), 30);                    % 3 -> 10 cycles",
    "wt = -2:1/fs:2;  half = floor(numel(wt)/2);",
    "nConv = numel(x) + numel(wt) - 1;  X = fft(x(:).', nConv);",
    "tf = zeros(numel(frex), size(x,1));  itpc = tf;",
    "for fi = 1:numel(frex)",
    "    s  = ncyc(fi) / (2*pi*frex(fi));",
    "    W  = fft(exp(2i*pi*frex(fi)*wt) .* exp(-wt.^2/(2*s^2)), nConv);",
    "    as = ifft(X .* W ./ max(W));  as = reshape(as(half+1:end-half), size(x));",
    "    tf(fi,:)   = mean(abs(as).^2, 2);                         % total power",
    "    itpc(fi,:) = abs(mean(exp(1i*angle(as)), 2));            % phase coherence",
    "end",
    "bl = EEG.times >= -400 & EEG.times <= -100;",
    "tfdB = 10*log10(tf ./ mean(tf(:,bl), 2));                    % baseline in dB"];
  text(s, code.map(c => ({ t: c })), X0 + 0.25, Y0 + 0.15, CW - 0.5, 4.8, { raw: true, sz: 12, face: "Consolas", after: 3 });
}

// 24 trappole
{
  const s = content(t("Pitfalls", "Trappole"), t("Six ways to fool yourself with frequencies", "Sei modi di ingannarsi con le frequenze"),
    { notes: t("Muscle: Whitham et al. (2007); microsaccades: Yuval-Greenberg et al. (2008); multiple comparisons: Maris & Oostenveld (2007) J Neurosci Methods 164:177 (cluster-based permutation). Non-sinusoidal waveforms: Cole & Voytek (2017).", "Muscolo: Whitham et al. (2007); microsaccadi: Yuval-Greenberg et al. (2008); confronti multipli: Maris & Oostenveld (2007) J Neurosci Methods 164:177 (permutazioni a cluster). Forme d'onda non sinusoidali: Cole & Voytek (2017).") });
  rows(s, [t("A \"band power\" change that is really a ++1/f slope++ change.", "Un cambiamento di \"potenza di banda\" che è in realtà un cambiamento di ++pendenza 1/f++."),
    t("\"Gamma\" that is ++muscle++ or ++microsaccades++.", "\"Gamma\" che è ++muscolo++ o ++microsaccadi++."),
    t("Oscillations created by ++filters++, ++edges++ or sharp ERPs.", "Oscillazioni create da ++filtri++, ++bordi++ o ERP ripidi."),
    t("An oscillation where there is only a ++transient++: bursts ≠ sustained rhythms.", "Un'oscillazione dove c'è solo un ++transitorio++: burst ≠ ritmi sostenuti."),
    t("Thousands of time × frequency × channel tests: use ++cluster-based permutation++ (Maris & Oostenveld, 2007).", "Migliaia di test tempo × frequenza × canale: usare ++permutazioni a cluster++ (Maris & Oostenveld, 2007)."),
    t("ITPC and coherence ++biased++ by unequal trial numbers.", "ITPC e coerenza ++distorte++ da numeri di trial diversi.")], X0, Y0, CW, 0.72, 0.12, 16, ACC);
}

// 25 domande
{
  const s = content(t("Check your understanding", "Verifica"), t("Three questions", "Tre domande"),
    { notes: t("(1) Δf = 1/T = 2 Hz: 10 and 11 Hz cannot be separated; use ≥ 1 s. (2) At 4 Hz, 7 cycles ≈ 1.75 s of wavelet: epochs must be longer. (3) Induced: power after averaging (ERP) removes non-phase-locked activity.", "(1) Δf = 1/T = 2 Hz: 10 e 11 Hz non si separano; servono ≥ 1 s. (2) A 4 Hz, 7 cicli ≈ 1,75 s di wavelet: le epoche devono essere più lunghe. (3) Indotta: la potenza dopo la media (ERP) toglie l'attività non agganciata in fase.") });
  rows(s, [t("With 500-ms windows, can you separate individual alpha peaks at 10 and 11 Hz? Why?", "Con finestre di 500 ms puoi separare picchi alfa individuali a 10 e 11 Hz? Perché?"),
    t("You want 4-Hz power with 7-cycle wavelets in −200…800 ms epochs. What is the problem?", "Vuoi la potenza a 4 Hz con wavelet a 7 cicli in epoche −200…800 ms. Qual è il problema?"),
    t("A gamma burst is visible in single-trial power but not in the TF map of the ERP. Why?", "Un burst gamma è visibile nella potenza dei singoli trial ma non nella mappa TF dell'ERP. Perché?")], X0, Y0 + 0.2, CW, 1.2, 0.35, 18, ACC);
}

// 26 take home
{
  const s = content(t("Take-home messages", "Messaggi chiave"), t("Take-home messages", "Messaggi chiave"));
  rows(s, [t("Δf = 1/T: ++resolution needs time++; taper to avoid leakage.", "Δf = 1/T: ++la risoluzione richiede tempo++; finestrare per evitare il leakage."),
    t("Average (Welch, multitaper) to get ++stable spectra++; show them on log axes.", "Mediare (Welch, multitaper) per spettri ++stabili++; mostrarli su assi log."),
    t("Separate ++peaks++ from the ++1/f++ background.", "Separare i ++picchi++ dal fondo ++1/f++."),
    t("Wavelets: ++cycles control the time–frequency trade-off++; normalise to baseline.", "Wavelet: ++i cicli regolano il compromesso tempo–frequenza++; normalizzare alla baseline."),
    t("Evoked ≠ induced; ITPC measures ++phase locking++; PAC needs care.", "Evocata ≠ indotta; l'ITPC misura l'++aggancio di fase++; il PAC richiede cautela.")], X0, Y0, CW, 0.85, 0.15, 17);
}

// 27 letture
{
  const s = content(t("Suggested reading", "Letture consigliate"), t("Suggested reading", "Letture consigliate"));
  text(s, [
    { t: "Cohen M.X. (2014) *Analyzing Neural Time Series Data: Theory and Practice*. MIT Press (MATLAB code).", b: true },
    { t: "Cohen M.X. (2019) A better way to define and describe Morlet wavelets for time-frequency analysis. *NeuroImage* 199:81–86.", b: true },
    { t: "Welch P. (1967) The use of fast Fourier transform for the estimation of power spectra. *IEEE Trans Audio Electroacoust* 15:70–73.", b: true },
    { t: "Thomson D.J. (1982) Spectrum estimation and harmonic analysis. *Proc IEEE* 70:1055–1096.", b: true },
    { t: "Donoghue T. et al. (2020) Parameterizing neural power spectra into periodic and aperiodic components. *Nat Neurosci* 23:1655–1665.", b: true },
    { t: "Klimesch W. (1999) EEG alpha and theta oscillations reflect cognitive and memory performance. *Brain Res Rev* 29:169–195.", b: true },
    { t: "Pfurtscheller G., Lopes da Silva F.H. (1999) Event-related EEG/MEG synchronization and desynchronization. *Clin Neurophysiol* 110:1842–1857.", b: true },
    { t: "Tallon-Baudry C., Bertrand O. (1999) Oscillatory gamma activity in humans and its role in object representation. *Trends Cogn Sci* 3:151–162.", b: true },
    { t: "Canolty R.T. et al. (2006) High gamma power is phase-locked to theta oscillations in human neocortex. *Science* 313:1626–1628.", b: true },
    { t: "Tort A.B.L. et al. (2010) Measuring phase-amplitude coupling between neuronal oscillations of different frequencies. *J Neurophysiol* 104:1195–1210.", b: true },
    { t: "Cole S.R., Voytek B. (2017) Brain oscillations and the importance of waveform shape. *Trends Cogn Sci* 21:137–149.", b: true },
    { t: "Maris E., Oostenveld R. (2007) Nonparametric statistical testing of EEG- and MEG-data. *J Neurosci Methods* 164:177–190.", b: true }], X0, Y0, CW, 5.2, { sz: 12, after: 5 });
}

save(OUT);
