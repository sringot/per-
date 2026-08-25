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
  // La barre de navigation n'en fait **pas** partie : c'est tout l'intérêt
  // de l'avoir sortie de `.scene`. Elle reste au-dessus du panneau ouvert,
  // atteignable au doigt comme à la tabulation, et c'est par elle qu'on
  // passe d'une rubrique à l'autre sans refermer.
  const fond = [$('.scene'), $('.pied'), $('.evitement')].filter(Boolean);
  /* ---------- D'où vient le focus ----------
     `:focus-visible` est censé ne montrer l'anneau qu'au clavier. Les
     moteurs ne s'accordent pas sur le cas qui nous concerne : ouvrir un
     panneau pose le focus sur la fermeture par script, et le refermer le
     repose sur la bulle. Chromium n'affiche alors rien après un appui au
     doigt ; Safari, si — l'anneau restait sur le bouton après l'avoir
     touché.

     On tranche donc nous-mêmes, plutôt que de s'en remettre à l'heuristique
     de chacun : `data-pointeur` marque une interaction au doigt ou à la
     souris, et le CSS masque l'anneau tant qu'il est là. Une touche de
     navigation le retire — `keydown` précède le déplacement du focus, la
     bulle suivante retrouve donc son anneau. */
  const racine = document.documentElement;
  const CLAVIER = new Set(['Tab', 'ArrowUp', 'ArrowDown', 'ArrowLeft',
                           'ArrowRight', 'Home', 'End', 'Enter', ' ']);
  addEventListener('pointerdown', () => racine.setAttribute('data-pointeur', ''), true);
  addEventListener('keydown', e => {
    if (CLAVIER.has(e.key)) racine.removeAttribute('data-pointeur');
  }, true);

  let ouvert = null;          // panneau affiché, ou null
  let declencheur = null;     // bulle d'où il est parti, pour y revenir
  let aPousse = false;        // a-t-on ajouté une entrée d'historique ?

  /* Les descriptions du tableau des tarifs se replient quand on quitte le
     panneau : on retrouve la liste des prix telle qu'on l'avait découverte,
     pas l'état où on l'avait laissée. */
  function replie(p) {
    $$('.t-info[aria-expanded="true"]', p).forEach(b => {
      b.setAttribute('aria-expanded', 'false');
      const d = document.getElementById(b.getAttribute('aria-controls'));
      if (d) d.hidden = true;
    });
  }

  /* ---------- Ouvrir / fermer ---------- */

  function ouvrir(id, bulle) {
    const p = document.getElementById(id);
    // Seuls les panneaux s'ouvrent. Sans ce filtre, une adresse pointant
    // sur n'importe quel `id` de la page — #bulles, la cible du lien
    // d'évitement — arrivait ici, ne trouvait pas de bouton de fermeture,
    // et l'erreur emportait tout le reste du script.
    if (!p || !p.classList.contains('panneau') || ouvert === p) return;
    // Passer d'une rubrique à l'autre ne doit pas empiler une entrée de
    // plus : avec une barre toujours là, on en change souvent, et le bouton
    // « retour » aurait rejoué la visite rubrique par rubrique au lieu de
    // ramener à l'accueil. On remplace l'entrée courante.
    const changement = ouvert !== null;
    if (ouvert) fermer();

    // Le disque part du centre de la bulle : sans ces coordonnées,
    // l'ouverture se ferait depuis le milieu de l'écran et le geste
    // perdrait son lien avec ce qu'on vient de toucher.
    if (bulle) {
      const r = bulle.querySelector('.bulle__rond').getBoundingClientRect();
      p.style.setProperty('--x', `${r.left + r.width / 2}px`);
      p.style.setProperty('--y', `${r.top + r.height / 2}px`);
    }

    // Les images du panneau n'ont d'adresse qu'à partir d'ici : tant qu'il
    // est fermé, elles ne coûtent rien.
    $$('img[data-src]', p).forEach(img => {
      img.src = img.dataset.src;
      img.removeAttribute('data-src');
    });

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
    replie(p);

    racine.classList.add('a-panneau');

    if (location.hash !== '#' + id) {
      if (changement) remplace('#' + id);
      else { memorise({ panneau: id }, '#' + id); aPousse = true; }
    }
  }

  function fermer(opts = {}) {
    if (!ouvert) return;
    ouvert.classList.remove('ouvert');
    ouvert.setAttribute('inert', '');
    replie(ouvert);
    // Le fond redevient atteignable **avant** qu'on y remette le focus.
    fond.forEach(e => e.removeAttribute('inert'));
    bulles.forEach(b => b.setAttribute('aria-expanded', 'false'));

    // Le focus revient sur la bulle d'origine : sans cela il retombe
    // en tête de document et l'on perd sa place.
    if (declencheur) declencheur.focus({ preventScroll: true });
    ouvert = null;
    declencheur = null;
    racine.classList.remove('a-panneau');
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


  /* ---------- La place que prend la barre ----------
     Mesurée plutôt que devinée : elle dépend de la taille des libellés, qui
     suit celle du texte choisie dans le système. Le pied de page et le
     contenu des panneaux s'arrêtent au-dessus grâce à cette valeur ; une
     constante écrite dans la feuille de style aurait menti dès qu'on
     agrandit le texte, et la dernière ligne serait passée sous la barre. */
  const barre = $('.bulles');
  if (barre) {
    const mesure = () => racine.style.setProperty(
      '--barre', `${Math.round(barre.getBoundingClientRect().height)}px`);
    mesure();
    if (window.ResizeObserver) new ResizeObserver(mesure).observe(barre);
    else addEventListener('resize', mesure);
  }

  /* ---------- L'économie des forfaits ----------
     Jamais écrite : elle se déduit du prix à la séance, du nombre de
     séances et du prix du lot. Un tarif qui change met le gain à jour tout
     seul, et une addition fausse devient impossible. */
  $$('.t-l[data-prix]').forEach(f => {
    const u = parseFloat(f.dataset.unite);
    const n = parseFloat(f.dataset.lot);
    const p = parseFloat(f.dataset.prix);
    if ([u, n, p].some(isNaN) || u * n <= p) return;
    // « au lieu de 180 € » plutôt que « −30 € » : la remise brute posée à
    // côté d'un prix ne dit pas ce qu'elle est — remise ? acompte ? part
    // par séance ? Le prix de référence, lui, se comprend sans notice.
    const cible = $('.t-avant', f);
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
  /* Le « i » de chaque soin : la description est dans la page, on ne fait
     que la montrer. `aria-expanded` porte l'état, `aria-controls` désigne la
     ligne — un lecteur d'écran annonce donc l'un et trouve l'autre. */
  $$('.t-info').forEach(bouton => {
    bouton.addEventListener('click', () => {
      const d = document.getElementById(bouton.getAttribute('aria-controls'));
      if (!d) return;
      const ouvre = bouton.getAttribute('aria-expanded') !== 'true';
      bouton.setAttribute('aria-expanded', String(ouvre));
      d.hidden = !ouvre;
    });
  });


})();
