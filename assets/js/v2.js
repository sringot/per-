/* =========================================================
   MARIE MASSAGE — V2

   Un seul écran, cinq panneaux. Le panneau s'ouvre *depuis* la
   bulle qu'on a touchée : son disque grandit jusqu'à remplir
   l'écran. D'où le besoin de connaître, au moment du clic, où se
   trouve la bulle — c'est tout ce que fait ce fichier, avec la
   gestion du clavier et de l'historique.
   ========================================================= */
(function () {
  'use strict';

  const $  = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));

  // Certains contextes (aperçu en bac à sable, fichier ouvert en local)
  // refusent d'écrire dans l'historique. L'adresse partageable est un
  // confort : elle ne doit pas pouvoir emporter le reste du script.
  const memorise = (etat, hash) => {
    try { history.pushState(etat, '', hash); } catch (e) { /* sans gravité */ }
  };

  const bulles   = $$('.bulle');
  const panneaux = $$('.panneau');
  let ouvert = null;          // panneau affiché, ou null
  let declencheur = null;     // bulle d'où il est parti, pour y revenir

  /* ---------- Ouvrir / fermer ---------- */

  function ouvrir(id, bulle) {
    const p = document.getElementById(id);
    if (!p || ouvert === p) return;
    if (ouvert) fermer({ silencieux: true });

    // Le disque part du centre de la bulle : sans ces coordonnées,
    // l'ouverture se ferait depuis le milieu de l'écran et le geste
    // perdrait son lien avec ce qu'on vient de toucher.
    if (bulle) {
      const r = bulle.querySelector('.bulle__rond').getBoundingClientRect();
      p.style.setProperty('--x', `${r.left + r.width / 2}px`);
      p.style.setProperty('--y', `${r.top + r.height / 2}px`);
    }

    p.removeAttribute('inert');
    p.classList.add('ouvert');
    document.body.classList.add('panneau-ouvert');
    ouvert = p;
    declencheur = bulle || null;
    if (bulle) bulle.setAttribute('aria-expanded', 'true');

    // Le focus part sur la fermeture : c'est la sortie, et cela ancre
    // la navigation au clavier dans le panneau.
    p.querySelector('.fermer').focus({ preventScroll: true });
    p.scrollTop = 0;

    if (location.hash !== '#' + id) memorise({ panneau: id }, '#' + id);
  }

  function fermer(opts = {}) {
    if (!ouvert) return;
    ouvert.classList.remove('ouvert');
    ouvert.setAttribute('inert', '');
    document.body.classList.remove('panneau-ouvert');
    bulles.forEach(b => b.setAttribute('aria-expanded', 'false'));

    // Le focus revient sur la bulle d'origine : sans cela il retombe
    // en tête de document et l'on perd sa place.
    if (declencheur) declencheur.focus({ preventScroll: true });
    ouvert = null;
    declencheur = null;

    if (!opts.silencieux && location.hash) memorise(null, location.pathname);
  }

  /* ---------- Branchements ---------- */

  bulles.forEach(b => {
    b.addEventListener('click', () => ouvrir(b.dataset.ouvre, b));
  });

  panneaux.forEach(p => {
    p.querySelector('.fermer').addEventListener('click', () => fermer());
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && ouvert) fermer();
  });

  // Bouton « retour » du téléphone : il doit refermer le panneau,
  // pas quitter le site.
  window.addEventListener('popstate', () => {
    const id = location.hash.slice(1);
    if (id && document.getElementById(id)) {
      ouvrir(id, bulles.find(b => b.dataset.ouvre === id));
    } else {
      fermer({ silencieux: true });
    }
  });

  // Arrivée directe sur une adresse partagée (…/#massages).
  const depart = location.hash.slice(1);
  if (depart && document.getElementById(depart)) {
    ouvrir(depart, bulles.find(b => b.dataset.ouvre === depart));
  }

  /* ---------- Synthèse des avis ----------
     Jamais écrite en dur : la moyenne et le nombre viennent des avis
     présents dans la page. Ajouter un <li data-note="…"> suffit. */
  (function synthese() {
    const liste = $('#avis-liste');
    if (!liste) return;
    const notes = $$('li[data-note]', liste)
      .map(li => parseFloat(li.dataset.note))
      .filter(n => !isNaN(n));
    if (!notes.length) return;

    const moy = notes.reduce((a, b) => a + b, 0) / notes.length;
    const arrondi = Math.round(moy * 10) / 10;
    $('#note-moy').textContent = Number.isInteger(arrondi)
      ? String(arrondi)
      : arrondi.toFixed(1).replace('.', ',');
    const pleines = Math.round(moy);
    $('#note-etoiles').textContent = '★'.repeat(pleines) + '☆'.repeat(5 - pleines);
    $('#note-nb').textContent = notes.length;
  })();

  /* ---------- Année du pied de page ---------- */
  const an = $('#annee');
  if (an) an.textContent = new Date().getFullYear();
})();
