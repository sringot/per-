// Rend l'image de partage (1200 × 630) : celle qu'affichent WhatsApp,
// Instagram, Facebook ou un SMS quand on y colle le lien du site.
//
// Elle était faite à la main, et avait divergé du site : ancienne couleur,
// ancien slogan, et surtout « Voisins-le-Bretonneux » — la ville de l'école
// de formation — à la place de Montigny. Elle est maintenant rendue par un
// navigateur à partir des fichiers du site : même police, même fond blanc
// cassé, même terracotta, même photo que l'accueil, mêmes phrases. Si le
// site change, on relance ce script.
//
//     node tools-partage.js

const { chromium } = require('playwright');
const fs = require('fs');
const os = require('os');
const path = require('path');

const RACINE = __dirname;
const SORTIE = path.join(RACINE, 'assets/img/partage.jpg');
const f = p => `file://${path.join(RACINE, p)}`;

const HTML = `<!doctype html><html lang="fr"><head><meta charset="utf-8">
<style>
  @font-face{ font-family:Figtree; src:url(${f('assets/fonts/figtree-400-latin.woff2')}) format('woff2');
              font-weight:300 900; }
  @font-face{ font-family:Figtree; src:url(${f('assets/fonts/figtree-400-latin-ext.woff2')}) format('woff2');
              font-weight:300 900; unicode-range:U+0100-024F; }
  *{ margin:0; box-sizing:border-box; }
  body{ width:1200px; height:630px; display:grid; grid-template-columns:1fr 470px;
        font-family:Figtree, sans-serif; color:#1E1814;
        background:#EBDCC7 url(${f('assets/img/pages/fond.webp')}) center/cover; }
  .texte{ display:flex; flex-direction:column; justify-content:center; gap:26px; padding:0 64px 0 76px; }
  .logo{ width:84px; height:84px; }
  h1{ font-size:74px; font-weight:600; letter-spacing:-.035em; line-height:1; }
  p{ font-size:30px; line-height:1.35; max-width:18ch; }
  .lieu{ display:inline-block; width:fit-content; padding:12px 20px; border-radius:14px;
         font-size:17px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; color:#fff;
         white-space:nowrap;
         background:url(${f('assets/img/pages/terracotta-touche.webp')}) center/cover, #924A31; }
  .photo{ background:url(${f('assets/img/marie-hero-plein.webp')}) 50% 30%/cover; }
</style></head><body>
  <div class="texte">
    <img class="logo" src="${f('assets/img/logo-officiel.webp')}" alt="">
    <h1>marieemassage</h1>
    <p>Une heure pour vous, dans une pièce pensée pour ça.</p>
    <span class="lieu">Montigny-le-Bretonneux · Réservé aux femmes</span>
  </div>
  <div class="photo"></div>
</body></html>`;

(async () => {
  const navigateur = await chromium.launch({ executablePath: process.env.CHROME || undefined });
  const page = await navigateur.newPage({ viewport: { width: 1200, height: 630 } });
  // Une page ouverte depuis un fichier, et non `setContent` : une page
  // vierge n'a pas le droit de charger des fichiers locaux, et le logo, la
  // photo et les textures manquaient.
  const temp = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'partage-')), 'partage.html');
  fs.writeFileSync(temp, HTML);
  await page.goto(`file://${temp}`, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: SORTIE, type: 'jpeg', quality: 86 });
  await navigateur.close();
  console.log('image de partage écrite →', SORTIE);
})();
