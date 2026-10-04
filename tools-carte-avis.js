// Rend la carte « Laissez un avis » à poser dans la salle de massage :
// un A6 (105 × 148 mm) avec le QR code qui mène à marieemassage.com/avis/,
// la page qui renvoie vers le formulaire d'avis Google.
//
// Le QR vise la page du site, pas Google directement : si le lien d'avis
// change, on le corrige dans avis/index.html et la carte imprimée reste
// bonne. Le QR lui-même est dans sources/carte-avis-qr.svg (fabriqué une
// fois avec segno, en Python : `segno.make('https://marieemassage.com/avis/',
// error='m')`). Mêmes police et fond que le site.
//
//     node tools-carte-avis.js     → carte-avis.pdf (à imprimer) et carte-avis.png

const { chromium } = require('playwright');
const fs = require('fs');
const os = require('os');
const path = require('path');

const RACINE = __dirname;
const f = p => `file://${path.join(RACINE, p)}`;
const QR = fs.readFileSync(path.join(RACINE, 'sources/carte-avis-qr.svg'), 'utf8')
  .replace(/width="\d+" height="\d+"/, 'viewBox="0 0 29 29" shape-rendering="crispEdges"');

const HTML = `<!doctype html><html lang="fr"><head><meta charset="utf-8">
<style>
  @font-face{ font-family:Figtree; src:url(${f('assets/fonts/figtree-400-latin.woff2')}) format('woff2'); font-weight:300 900; }
  @font-face{ font-family:Figtree; src:url(${f('assets/fonts/figtree-400-latin-ext.woff2')}) format('woff2');
              font-weight:300 900; unicode-range:U+0100-024F; }
  @page{ size:105mm 148mm; margin:0; }
  *{ margin:0; box-sizing:border-box; }
  html,body{ width:105mm; height:148mm; }
  body{ font-family:Figtree, sans-serif; color:#2A2320; text-align:center;
        background:#EBDCC7 url(${f('assets/img/pages/fond.webp')}) center/cover;
        display:flex; flex-direction:column; align-items:center; justify-content:space-between;
        padding:11mm 9mm 0; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  .haut{ display:flex; flex-direction:column; align-items:center; gap:2.2mm; }
  .logo{ width:14mm; height:14mm; }
  .marque{ font-size:7pt; font-weight:500; letter-spacing:.22em; text-transform:uppercase; color:#6A2F3C; }
  h1{ font-size:24pt; font-weight:600; line-height:1.02; letter-spacing:-.035em; margin-top:1mm; }
  .mot{ font-size:9.5pt; line-height:1.45; color:#4A423D; max-width:72mm; }
  .qr{ width:46mm; height:46mm; padding:4mm; background:#FDF8F1; border-radius:5mm;
       box-shadow:0 2mm 5mm -3mm rgba(40,20,10,.45); }
  .qr svg{ width:100%; height:100%; display:block; }
  .adresse{ font-size:8pt; color:#4A423D; margin-top:2.5mm; letter-spacing:.02em; }
  /* Le mot de la fin, sur le fond comme le reste : un bandeau terracotta
     tranchait avec le prune du logo. Un simple filet le sépare du QR. */
  .bas{ align-self:center; margin-bottom:10mm; padding-top:4mm; min-width:52mm;
        border-top:.3mm solid rgba(42,35,32,.18);
        color:#2A2320; font-size:10pt; font-weight:500; }
</style></head><body>
  <div class="haut">
    <img class="logo" src="${f('assets/img/logo-officiel.webp')}" alt="">
    <p class="marque">marieemassage</p>
    <h1>Votre avis<br>compte</h1>
    <p class="mot">Scannez pour laisser un avis sur Google&nbsp;: il aide d'autres femmes à me trouver.</p>
  </div>
  <div>
    <div class="qr">${QR}</div>
    <p class="adresse">marieemassage.com/avis</p>
  </div>
  <p class="bas">Merci, et à bientôt — Marie</p>
</body></html>`;

(async () => {
  const navigateur = await chromium.launch({ executablePath: process.env.CHROME || undefined });
  const page = await navigateur.newPage({ viewport: { width: 397, height: 559 }, deviceScaleFactor: 4 });
  // Depuis un fichier, comme tools-partage.js : une page vierge ne peut pas
  // charger les polices et les images locales.
  const temp = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'carte-')), 'carte.html');
  fs.writeFileSync(temp, HTML);
  await page.goto(`file://${temp}`, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: path.join(RACINE, 'carte-avis.pdf'), width: '105mm', height: '148mm', printBackground: true });
  await page.screenshot({ path: path.join(RACINE, 'carte-avis.png') });
  await navigateur.close();
  console.log('carte écrite → carte-avis.pdf, carte-avis.png');
})();
