// Rend l'affiche en PDF A4 et en aperçu PNG, via Chromium.
//
// Appelé par `python3 tools-affiche.py --pdf`. Séparé du script Python parce
// que seul un vrai navigateur applique la feuille d'impression : marges de
// page, `print-color-adjust`, polices. Une conversion HTML→PDF maison
// donnerait un rendu différent de ce que Marie verra en imprimant.

const { chromium } = require('playwright');

const RACINE = __dirname;
const SOURCE = `file://${RACINE}/affiche-tarifs.html`;
const PDF = `${RACINE}/affiche-tarifs.pdf`;
const APERCU = process.env.APERCU_AFFICHE || `${RACINE}/affiche-apercu.png`;

(async () => {
  const navigateur = await chromium.launch();
  const page = await navigateur.newPage({
    viewport: { width: 1000, height: 1400 },
    deviceScaleFactor: 2,
  });

  const erreurs = [];
  page.on('pageerror', e => erreurs.push(String(e)));

  await page.goto(SOURCE, { waitUntil: 'networkidle' });
  await page.emulateMedia({ media: 'print' });

  const feuille = page.locator('.feuille');
  await feuille.screenshot({ path: APERCU });
  await page.pdf({
    path: PDF,
    format: 'A4',
    printBackground: true,
    margin: { top: 0, bottom: 0, left: 0, right: 0 },
  });

  // Le débord est le seul défaut qui ne se voit pas sur l'aperçu : le PDF
  // coupe simplement le bas. On le mesure donc plutôt que de le regarder.
  const mesure = await page.evaluate(() => {
    const f = document.querySelector('.feuille');
    return { contenu: f.scrollHeight, feuille: f.clientHeight };
  });

  const boite = await feuille.boundingBox();
  console.log(
    `feuille ${Math.round(boite.width)}×${Math.round(boite.height)} px · `
    + `contenu ${mesure.contenu} / ${mesure.feuille} px · `
    + `erreurs : ${erreurs.join(' | ') || 'aucune'}`
  );

  await navigateur.close();

  if (mesure.contenu > mesure.feuille) {
    console.error(`débord de ${mesure.contenu - mesure.feuille} px — le PDF sera coupé`);
    process.exit(1);
  }
})();
