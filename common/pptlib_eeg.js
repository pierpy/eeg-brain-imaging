// Libreria pptx del corso EEG (Brain Imaging – Methods and Applications), bilingue EN/IT
const __R = (function () { const p = require("path"), fs = require("fs"); let d = process.env.COURSE_ROOT || __dirname;
  while (!fs.existsSync(p.join(d, ".course_root")) && p.dirname(d) !== d) d = p.dirname(d); return d; })();
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const CFG = global.CFG;
const FIG = CFG.fig;
const LANG = CFG.lang || "en";
const tr = (en, it) => (LANG === "it" ? it : en);

// ---------------- palette e font (stessi token delle altre lezioni rifatte)
const INK = "16213A", INK2 = "223057", ACC = "E4622B", TEAL = "1F7A8C", DARKOR = "C2410C";
const TXT = "2B2F38", MUTED = "6B7280", TINT = "F2F4F8", LINE = "D8DEE9", WHITE = "FFFFFF";
const SERIF = "Cambria", SANS = "Calibri";
const W = 13.333, H = 7.5, MX = 0.65;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = CFG.footer;
pres.author = "Pierpaolo Croce";

// ---------------- mini-markup per il testo ricco
//  *x*  termine chiave (arancione corsivo)      ~x~  rilievo (teal grassetto)
//  **x** grassetto        ++x++ sottolineato     !x!  simbolo vettoriale (grassetto corsivo serif)
//  $x$  simbolo scalare (corsivo serif)          _x / _{..} pedice      ^x / ^{..} apice
function rich(str, base = {}) {
  const runs = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|~[^~]+~|\+\+[^+]+\+\+|![^!]+!|\$[^$]+\$|_\{[^}]+\}|\^\{[^}]+\}|_[A-Za-z0-9]|\^[A-Za-z0-9])/g;
  let last = 0, m;
  const push = (text, o) => { if (text) runs.push({ text: text.replace(/\u0001/g, "_"), options: Object.assign({}, base, o) }); };
  str = str.replace(/\\_/g, "\u0001");
  while ((m = re.exec(str)) !== null) {
    push(str.slice(last, m.index), {});
    const t = m[0];
    const nest = (inner, o) => runs.push(...rich(inner, Object.assign({}, base, o)));
    if (t.startsWith("**")) nest(t.slice(2, -2), { bold: true });
    else if (t.startsWith("*")) nest(t.slice(1, -1), { color: ACC, italic: true });
    else if (t.startsWith("~")) nest(t.slice(1, -1), { color: TEAL, bold: true });
    else if (t.startsWith("++")) nest(t.slice(2, -2), { underline: { style: "sng" } });
    else if (t.startsWith("!")) push(t.slice(1, -1), { bold: true, italic: true, fontFace: SERIF });
    else if (t.startsWith("$")) push(t.slice(1, -1), { italic: true, fontFace: SERIF });
    else if (t.startsWith("_{")) push(t.slice(2, -1), { subscript: true });
    else if (t.startsWith("^{")) push(t.slice(2, -1), { superscript: true });
    else if (t.startsWith("_")) push(t.slice(1), { subscript: true });
    else if (t.startsWith("^")) push(t.slice(1), { superscript: true });
    last = re.lastIndex;
  }
  push(str.slice(last), {});
  return runs;
}

// paragrafi: stringa, oppure {t, lvl, b (bullet), n (numero), sz, c (colore), align, after}
function paras(list, dflt = {}) {
  const out = [];
  list.forEach((p, i) => {
    if (typeof p === "string") p = { t: p };
    const sz = p.sz || dflt.sz || 20;
    const base = { fontSize: sz, color: p.c || dflt.c || TXT, fontFace: p.face || dflt.face || SANS };
    if (p.i) base.italic = true;
    const r = (p.raw || dflt.raw) ? [{ text: p.t, options: base }] : rich(p.t, base);
    const po = { paraSpaceAfter: p.after ?? dflt.after ?? 8, align: p.align || dflt.align || "left" };
    const bullet = p.b ?? dflt.b;
    if (bullet) {
      po.bullet = p.lvl ? { characterCode: "2013", indent: 24 } : { characterCode: "25CF", indent: 24 };
      po.indentLevel = p.lvl || 0;
    } else if (p.n) {
      po.bullet = { type: "number", indent: 22 };
    }
    r.forEach((run, k) => { if (k === 0) Object.assign(run.options, po); });
    if (r.length === 0) r.push({ text: " ", options: Object.assign({}, base, po) });
    if (i < list.length - 1) r[r.length - 1].options.breakLine = true;
    out.push(...r);
  });
  return out;
}

// dimensione PNG (per mantenere le proporzioni delle figure)
function pngSize(f) {
  const b = fs.readFileSync(f);
  return [b.readUInt32BE(16), b.readUInt32BE(20)];
}
function fig(slide, name, x, y, w, h, align = "c", alt = "") {
  const f = path.join(FIG, name + ".png");
  const [pw, ph] = pngSize(f);
  const r = Math.min(w / pw, h / ph);
  const iw = pw * r, ih = ph * r;
  let ix = x + (w - iw) / 2, iy = y + (h - ih) / 2;
  if (align.includes("l")) ix = x; if (align.includes("r")) ix = x + w - iw;
  if (align.includes("t")) iy = y;
  slide.addImage({ path: f, x: ix, y: iy, w: iw, h: ih, altText: alt || name });
}

// ---------------- mattoni di layout
let N = 0;
function content(tag, title, opts = {}) {
  const s = pres.addSlide();
  N++;
  s.background = { color: WHITE };
  if (tag) s.addText(tag.toUpperCase(), { x: MX, y: 0.38, w: 9, h: 0.3, fontFace: SANS, fontSize: 12, bold: true,
    color: TEAL, charSpacing: 2, margin: 0, isTextBox: true });
  if (title) s.addText(title, { x: MX, y: 0.66, w: W - 2 * MX, h: 0.8, fontFace: SERIF, fontSize: 34, bold: true,
    color: INK, margin: 0, valign: "top", isTextBox: true });
  s.addText(CFG.footer, { x: MX, y: H - 0.45, w: 6, h: 0.25, fontFace: SANS,
    fontSize: 10, color: MUTED, margin: 0, isTextBox: true });
  s.addText(String(N), { x: W - MX - 1, y: H - 0.45, w: 1, h: 0.25, fontFace: SANS, fontSize: 10, color: MUTED,
    align: "right", margin: 0, isTextBox: true });
  if (opts.hidden) s.hidden = true;
  if (opts.notes) s.addNotes(opts.notes);
  return s;
}
function text(s, list, x, y, w, h, dflt = {}) {
  s.addText(paras(list, dflt), { x, y, w, h, valign: dflt.valign || "top", margin: 0, isTextBox: true,
    fit: "none" });
}
// riquadro formula (motivo ricorrente: card grigio-azzurra con la formula in serif)
function formula(s, str, x, y, w, h, o = {}) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: o.fill || TINT }, line: { color: o.fill || TINT },
    rectRadius: 0.12 });
  const lines = Array.isArray(str) ? str : [str];
  s.addText(paras(lines.map(t => (typeof t === "string" ? { t } : t)),
    { sz: o.sz || 24, face: SERIF, c: o.c || INK, align: o.align || "center", after: o.after ?? 4 }),
    { x: x + 0.2, y, w: w - 0.4, h, valign: "middle", margin: 0, isTextBox: true });
}
function card(s, x, y, w, h, fill = TINT) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: fill }, rectRadius: 0.14 });
}
function badge(s, n, x, y, col = ACC) {
  s.addShape(pres.shapes.OVAL, { x, y, w: 0.46, h: 0.46, fill: { color: col }, line: { color: col } });
  s.addText(String(n), { x, y, w: 0.46, h: 0.46, fontFace: SANS, fontSize: 16, bold: true, color: WHITE, align: "center",
    valign: "middle", margin: 0, isTextBox: true });
}
const X0 = MX, Y0 = 1.75, CW = W - 2 * MX;

function copertina() {
  const s = pres.addSlide(); N++;
  s.background = { color: INK };
  s.addText(tr("MSC IN COMPUTATIONAL COGNITIVE SCIENCE", "CDS MAGISTRALE IN COMPUTATIONAL COGNITIVE SCIENCE"), { x: 0.9, y: 0.95, w: 11, h: 0.35, fontFace: SANS, fontSize: 14, bold: true,
    color: "9AA3B8", charSpacing: 3, margin: 0, isTextBox: true });
  s.addText("Brain Imaging – Methods and Applications", { x: 0.9, y: 1.35, w: 11.5, h: 0.5,
    fontFace: SANS, fontSize: 22, color: "C9D1E3", margin: 0, isTextBox: true });
  s.addText(tr("Module: Electroencephalography (EEG)", "Modulo: Elettroencefalografia (EEG)"), { x: 0.9, y: 1.85, w: 11, h: 0.45, fontFace: SANS, fontSize: 20,
    color: "C9D1E3", margin: 0, isTextBox: true });
  s.addText(CFG.lezione, { x: 0.9, y: 3.05, w: 8, h: 0.5, fontFace: SANS, fontSize: 20, bold: true, color: ACC, margin: 0, isTextBox: true });
  s.addText(CFG.titolo, { x: 0.9, y: 3.5, w: 8.6, h: 1.8, fontFace: SERIF, fontSize: CFG.titoloSize || 48, bold: true, color: WHITE, margin: 0, isTextBox: true, valign: "top" });
  s.addText("Pierpaolo Croce", { x: 0.9, y: 5.75, w: 6, h: 0.5, fontFace: SANS, fontSize: 22, bold: true, color: WHITE, margin: 0, isTextBox: true });
  s.addText(tr("A.Y. 2026-2027", "A.A. 2026-2027"), { x: 0.9, y: 6.3, w: 4, h: 0.4, fontFace: SANS, fontSize: 18, color: "9AA3B8", margin: 0, isTextBox: true });
  const cov = path.join(CFG.common || __R + "/common", "cover_eeg.png");
  if (fs.existsSync(cov)) s.addImage({ path: cov, x: 8.6, y: 3.2, w: 4.3, h: 4.3 * 0.62 });
}

function licenza() {}
function sezione(n, title) {
  const s = pres.addSlide(); N++;
  s.background = { color: INK };
  s.addText(String(n).padStart(2, "0"), { x: 0.9, y: 2.2, w: 3, h: 1.4, fontFace: SERIF, fontSize: 80, bold: true, color: ACC, margin: 0, isTextBox: true });
  s.addText(title, { x: 0.9, y: 3.7, w: 11, h: 1.2, fontFace: SERIF, fontSize: 40, bold: true, color: WHITE, margin: 0, isTextBox: true });
  s.addText(String(N), { x: W - MX - 1, y: H - 0.45, w: 1, h: 0.25, fontFace: SANS, fontSize: 10, color: "9AA3B8", align: "right", margin: 0, isTextBox: true });
  return s;
}

function save(out) {
  fs.mkdirSync(path.dirname(out), { recursive: true });
  return pres.writeFile({ fileName: out }).then(f => console.log("scritto", f, N, "slide"));
}
module.exports = { sezione, tr, LANG, pres, rich, paras, fig, content, text, formula, card, badge, copertina, licenza, save,
  C: { INK, INK2, ACC, TEAL, DARKOR, TXT, MUTED, TINT, LINE, WHITE, SERIF, SANS, W, H, MX, X0, Y0, CW } };
