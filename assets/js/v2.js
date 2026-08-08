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
  const remplace = (url) => {
    try { history.replaceState(null, '', url); } catch (e) { /* sans gravité */ }
  };

  const bulles   = $$('.bulle');
  const panneaux = $$('.panneau');
  // Ce qui doit disparaître du clavier et des lecteurs d'écran quand un
  // panneau couvre l'écran. `clip-path` ne masque qu'à l'œil : sans cela,
  // la tabulation sortait du panneau et parcourait la page en dessous.
  const fond = [$('.scene'), $('.pied'), $('.evitement')].filter(Boolean);
  let ouvert = null;          // panneau affiché, ou null
  let declencheur = null;     // bulle d'où il est parti, pour y revenir
  let aPousse = false;        // a-t-on ajouté une entrée d'historique ?

  /* ---------- Ouvrir / fermer ---------- */

  function ouvrir(id, bulle) {
    const p = document.getElementById(id);
    // Seuls les panneaux s'ouvrent. Sans ce filtre, une adresse pointant
    // sur n'importe quel `id` de la page — #bulles, la cible du lien
    // d'évitement — arrivait ici, ne trouvait pas de bouton de fermeture,
    // et l'erreur emportait tout le reste du script.
    if (!p || !p.classList.contains('panneau') || ouvert === p) return;
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
    fond.forEach(e => e.setAttribute('inert', ''));
    ouvert = p;
    declencheur = bulle || null;
    if (bulle) bulle.setAttribute('aria-expanded', 'true');

    // Le focus part sur la fermeture : c'est la sortie, et cela ancre
    // la navigation au clavier dans le panneau.
    p.querySelector('.fermer').focus({ preventScroll: true });
    p.scrollTop = 0;
    cartes(p).forEach(c => c.setAttribute('aria-expanded', 'false'));
    amorcer(p);

    if (location.hash !== '#' + id) {
      memorise({ panneau: id }, '#' + id);
      aPousse = true;
    }
  }

  function fermer(opts = {}) {
    if (!ouvert) return;
    ouvert.classList.remove('ouvert');
    ouvert.setAttribute('inert', '');
    // Les cartes retournées reviennent à l'endroit : rouvrir « Massages »
    // et les retrouver sur le dos donnerait l'impression d'un état en plan.
    cartes(ouvert).forEach(c => c.setAttribute('aria-expanded', 'false'));
    // Le fond redevient atteignable **avant** qu'on y remette le focus.
    fond.forEach(e => e.removeAttribute('inert'));
    bulles.forEach(b => b.setAttribute('aria-expanded', 'false'));

    // Le focus revient sur la bulle d'origine : sans cela il retombe
    // en tête de document et l'on perd sa place.
    if (declencheur) declencheur.focus({ preventScroll: true });
    ouvert = null;
    declencheur = null;
  }

  // Fermeture demandée par l'utilisateur (croix, Échap, voile).
  // On **revient en arrière** au lieu d'empiler une entrée de plus :
  // sinon le bouton « retour » du téléphone rouvrait le panneau qu'on
  // venait de fermer, et l'historique grossissait de deux entrées par
  // aller-retour — cinq rubriques visitées, onze retours pour sortir.
  function demandeFermeture() {
    if (!ouvert) return;
    if (aPousse) {
      aPousse = false;
      history.back();          // le popstate ci-dessous referme
    } else {
      remplace(location.pathname);
      fermer();
    }
  }

  /* ---------- Branchements ---------- */

  bulles.forEach(b => {
    b.addEventListener('click', () => ouvrir(b.dataset.ouvre, b));
  });

  panneaux.forEach(p => {
    p.querySelector('.fermer').addEventListener('click', demandeFermeture);
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && ouvert) demandeFermeture();
  });

  // Bouton « retour » du téléphone : il doit refermer le panneau,
  // pas quitter le site.
  window.addEventListener('popstate', () => {
    const id = location.hash.slice(1);
    const p = id && document.getElementById(id);
    if (p && p.classList.contains('panneau')) {
      aPousse = false;
      ouvrir(id, bulles.find(b => b.dataset.ouvre === id));
    } else {
      aPousse = false;
      fermer();
    }
  });

  // Arrivée directe sur une adresse partagée (…/#massages). Aucune entrée
  // n'a été empilée : `aPousse` reste faux, et la fermeture nettoiera
  // l'adresse au lieu de tenter un retour qui sortirait du site.
  const depart = location.hash.slice(1);
  if (depart) ouvrir(depart, bulles.find(b => b.dataset.ouvre === depart));

  /* ---------- Les cartes de soins ----------
     Un appui retourne la carte. Tout l'état tient dans `aria-expanded` :
     le CSS s'en sert pour la rotation, et un lecteur d'écran y lit la
     même chose que ce qu'on voit. Deux sources de vérité pour un seul
     état, c'est une de trop.

     `cartes()` et `amorcer()` sont appelées depuis `ouvrir()` et
     `fermer()`, et non branchées sur la croix et sur la bulle : accrochées
     aux déclencheurs, elles se taisaient dès qu'on fermait autrement — par
     le bouton « retour », ou en arrivant sur une adresse partagée. */
  function cartes(p) { return $$('.soin__carte', p); }

  let amorceFaite = false;
  function amorcer(p) {
    const carte = p.querySelector('.soin__carte');
    if (!carte || amorceFaite) return;
    amorceFaite = true;
    // Une carte entrouvre son dos puis se referme. Sur un écran tactile il
    // n'y a pas de survol : rien d'autre ne dirait qu'une carte se
    // retourne. Une seule fois, sur une seule carte — le geste doit se
    // remarquer, pas s'imposer.
    setTimeout(() => carte.classList.add('amorce', 'envol'), 500);
    setTimeout(() => carte.classList.remove('amorce', 'envol'), 1250);
  }

  $$('.soin__carte').forEach(carte => {
    let repos = null;
    carte.addEventListener('click', () => {
      // L'amorce vise le même `transform` : la retirer ici évite qu'elle
      // reprenne la main si l'on appuie pendant qu'elle joue.
      carte.classList.remove('amorce');
      const ouverte = carte.getAttribute('aria-expanded') === 'true';
      carte.setAttribute('aria-expanded', String(!ouverte));

      // L'envol monte puis redescend : deux états, donc une classe posée
      // puis retirée à mi-parcours. Une transition ne sait aller que d'un
      // point à un autre — elle ne peut pas culminer en chemin.
      clearTimeout(repos);
      carte.classList.add('envol');
      repos = setTimeout(() => carte.classList.remove('envol'), 310);
    });
  });

  /* ---------- L'économie des forfaits ----------
     Jamais écrite : elle se déduit du prix à la séance, du nombre de
     séances et du prix du lot. Un tarif qui change met le gain à jour tout
     seul, et une addition fausse devient impossible. */
  $$('.offre--forfait').forEach(f => {
    const u = parseFloat(f.dataset.unite);
    const n = parseFloat(f.dataset.lot);
    const p = parseFloat(f.dataset.prix);
    if ([u, n, p].some(isNaN) || u * n <= p) return;
    // « au lieu de 180 € » plutôt que « −30 € » : la remise brute posée à
    // côté d'un prix ne dit pas ce qu'elle est — remise ? acompte ? part
    // par séance ? Le prix de référence, lui, se comprend sans notice.
    const cible = $('.offre__avant', f);
    if (cible) cible.textContent = `au lieu de ${u * n} €`;
  });

  /* ---------- Synthèse des avis ----------
     Jamais écrite en dur : la moyenne et le nombre viennent des avis
     présents dans la page. Ajouter un <li data-note="…"> suffit. */
  (function synthese() {
    const liste = $('#avis-liste');
    if (!liste) return;
    const notes = $$('li[data-note]', liste)
      .map(li => parseFloat(li.dataset.note))
      .filter(n => n >= 0 && n <= 5);
    if (!notes.length) return;

    const moy = notes.reduce((a, b) => a + b, 0) / notes.length;
    const arrondi = Math.round(moy * 10) / 10;
    $('#note-moy').textContent = Number.isInteger(arrondi)
      ? String(arrondi)
      : arrondi.toFixed(1).replace('.', ',');
    // Bornée : les avis sont destinés à être remplacés à la main, et une
    // note saisie hors barème (« 55 », ou un barème sur 10) rendait
    // `repeat()` négatif — l'exception emportait le reste du script.
    const pleines = Math.max(0, Math.min(5, Math.round(moy)));
    $('#note-etoiles').textContent = '★'.repeat(pleines) + '☆'.repeat(5 - pleines);
    $('#note-nb').textContent = notes.length;
  })();

  /* ---------- Année du pied de page ---------- */
  const an = $('#annee');
  if (an) an.textContent = new Date().getFullYear();
})();
