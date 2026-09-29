# Brain Imaging – Methods and Applications · Modulo EEG

**CdS Magistrale in Computational Cognitive Science** — Università G. d'Annunzio Chieti-Pescara
Docente: **Pierpaolo Croce** · A.A. 2026-2027

Corso di 20 ore (10 lezioni × 2 h) sull'elettroencefalografia, in **italiano e inglese**.
Ogni lezione esiste in due forme: slide PowerPoint "statiche" e slide animate con [manim](https://www.manim.community/) + [manim-slides](https://github.com/jeertmans/manim-slides), con animazioni in loop continuo per i fenomeni fisici.

| # | Lezione | Contenuti |
|---|---------|-----------|
| 1 | Storia e cosa misura l'EEG | dai pionieri a oggi, scale spazio-temporali, cosa "vede" l'EEG |
| 2 | Basi cellulari | membrana, potenziale d'azione, sinapsi, PSP, sorgenti del segnale |
| 3 | Dai neuroni allo scalpo | dipoli, conduzione di volume, montaggi, ritmi |
| 4 | Registrare l'EEG | elettrodi, 10-20, amplificatori, campionamento, filtri, artefatti |
| 5 | Pre-elaborazione e ICA | pipeline, canali cattivi, riferimento, epoche, ICA, ICLabel |
| 6 | Analisi spettrale e tempo-frequenza | Fourier, Welch, 1/f, wavelet, ERD/ERS, ITPC, PAC |
| 7 | Potenziali evento-correlati | media, componenti, misure, permutazioni a cluster |
| 8 | Analisi spaziale e microstati | GFP, GMD, k-means modificato, back-fitting, applicazioni |
| 9 | Sorgenti e connettività | forward/inverse, MNE/sLORETA/beamformer, wPLI, Granger, grafi |
| 10 | Decoding e applicazioni | MVPA, cross-validation, Haufe, generalizzazione temporale, BCI, EEG–fMRI |

Tutti i dati nelle figure sono **simulati** con modelli fisiologicamente plausibili.

## Struttura

```
common/         librerie condivise (figure, stile pptx, base manim, script di build)
L1 … L10/       una cartella per lezione
  figsK.py        figure (oggetti manim, esportate anche in PNG)
  build_pptxK.js  slide PowerPoint (EN/IT)
  figpng_en|it/   PNG delle figure usate dai pptx
  manim/          scene animate (sKa.py, sKb.py) + en/ it/ (link)
pptx/EN|IT/     slide PowerPoint finali, pronte all'uso
```

## Rigenerare

Requisiti: Python ≥ 3.11, Node ≥ 18, LaTeX (per le formule manim), ffmpeg, LibreOffice (solo per le anteprime QA).

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
npm install

# figure PNG di una lezione (lingua: en | it)
EEG_LANG=it python common/render_static.py L4 figs4
# slide PowerPoint EN + IT della lezione 4  → L4/out/EEG_L4_{en,it}.pptx
bash common/build_pptx.sh 4
# animazioni manim (bassa risoluzione, per controllo)
cd L4/manim/it && EEG_LANG=it manim-slides render -ql s4a.py A4_Catena
# animazioni in HD + esportazione HTML/pptx in final_en, final_it
bash common/hq_lecture.sh 4 "EEG Lecture 4 - Recording the EEG (manim)" "EEG Lezione 4 - Registrare l'EEG (manim)" A4_Catena B4_Digitale
```

Gli script trovano da soli la radice della repository (file `.course_root`); in alternativa si può impostare `COURSE_ROOT`.

Le versioni manim esportate (HTML con video, pptx con video) non sono versionate perché pesanti (centinaia di MB): si rigenerano con `hq_lecture.sh` oppure si possono allegare a una *Release* di GitHub.

## Aggiornare

```bash
git add -A && git commit -m "L6: nuova slide su FOOOF" && git push
```

© 2026 Pierpaolo Croce — tutti i diritti riservati (uso didattico interno).
