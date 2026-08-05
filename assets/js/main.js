/* =========================================================
   MARIE MASSAGE — Interactions & animations

   Deux étages :
     · initShell()  — une seule fois : en-tête, menu, moteur de
                      défilement, transitions entre pages.
     · initPage()   — à chaque contenu : révélations, compteurs,
                      synthèse des avis, carrousel, héros.

   La séparation permet de rebrancher un contenu remplacé sans
   réinstaller les écouteurs globaux, qui s'accumuleraient sinon.
   ========================================================= */
(function () {
  'use strict';

  const $  = (sel, ctx = document) => (ctx || document).querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from((ctx || document).querySelectorAll(sel));
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine    = window.matchMedia('(hover:hover) and (pointer:fine)').matches;

  /* état rafraîchi à chaque page */
  let cue = null, parallaxEls = [], carousel = null;
  /* posé par initShell, consommé par l'aperçu (voir plus bas) */
  let fermerMenu = () => {};

  /* =====================================================
     BLOC CONTENU
     ===================================================== */

  /* ---------- Révélations au scroll ---------- */
  function initReveals(root) {
    const els = $$('[data-reveal]', root);
    if (!('IntersectionObserver' in window) || reduced) {
      els.forEach(el => el.classList.add('in'));
      return;
    }
    const io = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('in');
        obs.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    els.forEach(el => io.observe(el));
  }

  /* ---------- Compteurs ---------- */
  function runCounter(el) {
    const target   = parseFloat(el.dataset.count);
    const decimals = parseInt(el.dataset.decimals || '0', 10);
    const suffix   = el.dataset.suffix || '';
    const dur = 1500, t0 = performance.now();

    (function step(now) {
      const p = Math.min((now - t0) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);          // easeOutCubic
      el.textContent = (target * eased).toFixed(decimals).replace('.', ',') + suffix;
      if (p < 1) requestAnimationFrame(step);
    })(t0);
  }

  function initCounters(root) {
    const els = $$('.count', root);
    if (!('IntersectionObserver' in window) || reduced) {
      els.forEach(el => {
        const d = parseInt(el.dataset.decimals || '0', 10);
        el.textContent = parseFloat(el.dataset.count).toFixed(d).replace('.', ',')
                       + (el.dataset.suffix || '');
      });
      return;
    }
    const co = new IntersectionObserver((entries, obs) => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        runCounter(e.target);
        obs.unobserve(e.target);
      });
    }, { threshold: 0.6 });
    els.forEach(el => co.observe(el));
  }

  /* ---------- Boutons magnétiques ----------
     Le bouton se déporte vers le curseur puis revient : il donne
     l'impression de venir à la rencontre du geste. */
  function initMagnetic(root) {
    if (!fine || reduced) return;
    $$('.magnetic', root).forEach(el => {
      if (el.dataset.magnetic) return;               // déjà branché
      el.dataset.magnetic = '1';
      let raf = null, tx = 0, ty = 0, cx = 0, cy = 0;

      const loop = () => {
        cx += (tx - cx) * 0.16;
        cy += (ty - cy) * 0.16;
        el.style.translate = `${cx.toFixed(2)}px ${cy.toFixed(2)}px`;
        raf = (Math.abs(tx - cx) > 0.1 || Math.abs(ty - cy) > 0.1)
          ? requestAnimationFrame(loop) : null;
      };
      const kick = () => { if (!raf) raf = requestAnimationFrame(loop); };

      el.addEventListener('pointermove', e => {
        const r = el.getBoundingClientRect();
        tx = (e.clientX - (r.left + r.width / 2)) * 0.28;
        ty = (e.clientY - (r.top + r.height / 2)) * 0.42;
        kick();
      });
      el.addEventListener('pointerleave', () => { tx = ty = 0; kick(); });
    });
  }

  /* ---------- Inclinaison du visuel du héros ---------- */
  function initTilt(root) {
    const tilt = $('#heroTilt', root);
    const zone = $('#heroVisual', root);
    if (!tilt || !zone || !fine || reduced) return;

    zone.addEventListener('pointermove', e => {
      const r = zone.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width  - 0.5;
      const py = (e.clientY - r.top)  / r.height - 0.5;
      tilt.style.setProperty('--ry', (px * 7).toFixed(2) + 'deg');
      tilt.style.setProperty('--rx', (-py * 7).toFixed(2) + 'deg');
    });
    zone.addEventListener('pointerleave', () => {
      tilt.style.setProperty('--ry', '0deg');
      tilt.style.setProperty('--rx', '0deg');
    });
  }

  /* ---------- Carrousel d'avis ---------- */
  function initCarousel(root) {
    carousel = null;
    const track = $('#revTrack', root);
    if (!track) return;

    const prev = $('#revPrev', root), next = $('#revNext', root), dots = $('#revDots', root);
    const slides = $$('.review', track);
    if (!slides.length || !dots) return;

    let index = 0, pages = 1, autoplay = null;

    function goTo(i, animate = true) {
      index = (i + pages) % pages;
      const gap = parseFloat(getComputedStyle(track).columnGap
                          || getComputedStyle(track).gap) || 0;
      const stepPx = slides[0].getBoundingClientRect().width + gap;
      track.style.transition = animate ? '' : 'none';
      track.style.transform  = `translate3d(${-index * stepPx}px,0,0)`;
      if (!animate) requestAnimationFrame(() => { track.style.transition = ''; });
      $$('button', dots).forEach((d, n) => d.classList.toggle('active', n === index));
    }

    function buildDots() {
      dots.innerHTML = '';
      for (let i = 0; i < pages; i++) {
        const b = document.createElement('button');
        b.setAttribute('role', 'tab');
        b.setAttribute('aria-label', `Avis ${i + 1}`);
        b.addEventListener('click', () => { goTo(i); stopAuto(); });
        dots.appendChild(b);
      }
    }

    function measure() {
      const w = window.innerWidth;
      const perView = w <= 860 ? 1 : w <= 1080 ? 2 : 3;
      pages = Math.max(1, slides.length - perView + 1);
      index = Math.min(index, pages - 1);
      buildDots();
      goTo(index, false);
    }

    function startAuto() {
      if (reduced) return;
      stopAuto();
      autoplay = setInterval(() => goTo(index + 1), 5200);
    }
    function stopAuto() { clearInterval(autoplay); }

    if (prev) prev.addEventListener('click', () => { goTo(index - 1); stopAuto(); });
    if (next) next.addEventListener('click', () => { goTo(index + 1); stopAuto(); });
    track.addEventListener('mouseenter', stopAuto);
    track.addEventListener('mouseleave', startAuto);

    let x0 = null;
    track.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; stopAuto(); }, { passive: true });
    track.addEventListener('touchend', e => {
      if (x0 === null) return;
      const dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 45) goTo(index + (dx < 0 ? 1 : -1));
      x0 = null;
      startAuto();
    });

    measure();
    startAuto();
    carousel = { measure };
  }

  /* ---------- Page avis : synthèse + « voir tous les avis » ----------
     La moyenne et le nombre ne sont jamais écrits en dur : ils sont
     recalculés à partir des avis réellement présents dans la page.
     Ajouter ou retirer un <figure class="rev" data-note="…"> suffit,
     la synthèse suit. */
  function initReviews(root) {
    const grid = $('#revGrid', root);
    if (!grid) return;

    const notes = $$('.rev[data-note]', grid)
      .map(el => parseFloat(el.dataset.note))
      .filter(n => !isNaN(n));
    if (!notes.length) return;

    const moy = notes.reduce((a, b) => a + b, 0) / notes.length;
    const arrondi = Math.round(moy * 10) / 10;

    const elMoy = $('#revMoy', root);
    if (elMoy) {
      elMoy.dataset.count = arrondi;
      // Une moyenne pleine s'écrit « 5 », pas « 5,0 ».
      elMoy.dataset.decimals = Number.isInteger(arrondi) ? 0 : 1;
      elMoy.classList.add('count');
    }
    const elStars = $('#revStars', root);
    if (elStars) {
      const pleines = Math.round(moy);
      elStars.textContent = '★'.repeat(pleines) + '☆'.repeat(5 - pleines);
    }
    const elNb = $('#revNb', root);
    if (elNb) {
      elNb.dataset.count = notes.length;
      elNb.classList.add('count');
    }
    /* Les avis au-delà des six premiers restent repliés : la page garde
       une hauteur raisonnable et le bouton fait le reste. */
    const extras = $$('.rev--extra', grid);
    const btn = $('#revMore', root);
    if (!btn) return;

    if (!extras.length) { btn.hidden = true; return; }

    const libelle = () => {
      const ouvert = btn.getAttribute('aria-expanded') === 'true';
      btn.textContent = ouvert
        ? 'Voir moins d’avis'
        : `Voir tous les avis (${notes.length})`;
    };
    libelle();

    btn.addEventListener('click', () => {
      const ouvert = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!ouvert));
      extras.forEach((el, i) => {
        el.hidden = ouvert;
        // Masqué, l'élément ne croise jamais l'observateur de révélation :
        // on le déclenche à la main, en cascade.
        if (!ouvert) {
          el.style.setProperty('--d', (i * 0.08).toFixed(2) + 's');
          requestAnimationFrame(() => el.classList.add('in'));
        } else {
          el.classList.remove('in');
        }
      });
      libelle();
    });
  }

  /* ---------- Bandeau d'avis (accueil) ---------- */
  let tickerTimer = null;
  function initTicker(root) {
    clearInterval(tickerTimer);
    const stage = $('#tickerStage', root);
    if (!stage) return;
    const items = $$('.ticker__item', stage);
    if (items.length < 2) return;

    let i = 0;
    const step = () => {
      const sortant = items[i];
      i = (i + 1) % items.length;
      sortant.classList.replace('is-on', 'is-out');
      items[i].classList.add('is-on');
      // La ligne sortante est remise en bas une fois hors champ,
      // sinon elle réapparaîtrait par le haut au tour suivant.
      setTimeout(() => sortant.classList.remove('is-out'), 650);
    };
    if (!reduced) tickerTimer = setInterval(step, 12000);
  }

  /* ---------- Point d'entrée « contenu » ---------- */
  function initPage(root) {
    root = root || document;
    cue = $('#cue', root);
    parallaxEls = $$('[data-parallax]', root);
    initReveals(root);
    initReviews(root);   // avant les compteurs : il leur pose les valeurs
    initCounters(root);
    initMagnetic(root);
    initTilt(root);
    initCarousel(root);
    initTicker(root);
    applyParallax();
    onScroll();
  }

  /* =====================================================
     BLOC COQUILLE — installé une seule fois
     ===================================================== */

  const header = $('#header');
  const totop  = $('#totop');

  function onScroll() {
    const y = window.scrollY;
    if (header) header.classList.toggle('scrolled', y > 20);
    if (totop)  totop.classList.toggle('show', y > 700);
    if (cue)    cue.classList.toggle('gone', y > 90);
  }

  function applyParallax() {
    if (reduced) return;
    const vh = window.innerHeight;
    parallaxEls.forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.bottom < -200 || rect.top > vh + 200) return;
      const offset = (rect.top + rect.height / 2 - vh / 2) * parseFloat(el.dataset.parallax);
      el.style.translate = `0 ${offset.toFixed(1)}px`;
    });
  }

  function initShell() {
    /* --- Préchargeur : accueil uniquement --- */
    const preloader = $('#preloader');
    const ready = () => document.body.classList.add('ready');

    // Le préchargeur ne sert qu'à la toute première arrivée. Revenir sur
    // l'accueil depuis un onglet le rejouait, ajoutant une seconde à
    // chaque retour — pour masquer un chargement déjà terminé.
    let dejaVu = false;
    try { dejaVu = sessionStorage.getItem('mm-vu') === '1'; } catch (_) {}

    if (preloader && !dejaVu) {
      const start = () => {
        ready();
        try { sessionStorage.setItem('mm-vu', '1'); } catch (_) {}
        setTimeout(() => {
          preloader.classList.add('done');
          setTimeout(() => preloader.remove(), 500);
        }, reduced ? 0 : 260);
      };
      window.addEventListener('load', start);
      // Filet de sécurité si `load` traîne (polices, images lentes)
      setTimeout(() => {
        if (preloader.isConnected && !document.body.classList.contains('ready')) start();
      }, 2500);
    } else {
      if (preloader) preloader.remove();
      requestAnimationFrame(ready);
    }

    const year = $('#year');
    if (year) year.textContent = new Date().getFullYear();

    /* --- Photos : décourager l'enregistrement ---
       Le CSS écarte déjà le glisser-déposer et le clic droit sur l'image
       elle-même ; ici on bloque le menu contextuel sur les conteneurs de
       visuels, pour couvrir le cas où le clic droit vise le cadre.
       Cela décourage — cela n'empêche pas : capture d'écran et inspecteur
       restent hors de portée de toute page web. */
    document.addEventListener('contextmenu', e => {
      if (e.target.closest('.ill, .hero__photo, .about__main, .card__media')) e.preventDefault();
    });
    document.addEventListener('dragstart', e => {
      if (e.target.tagName === 'IMG') e.preventDefault();
    });

    /* --- Menu mobile --- */
    const burger = $('#burger'), nav = $('#nav');
    if (burger && nav) {
      // Le fond est figé en passant <body> en position fixe, décalé de la
      // hauteur déjà défilée. `overflow:hidden` ne suffisait pas : c'est
      // <html> qui défile. Il faut donc mémoriser la position et la rendre.
      let scrollGele = 0;

      const setNav = open => {
        nav.classList.toggle('open', open);
        burger.classList.toggle('open', open);
        burger.setAttribute('aria-expanded', String(open));
        burger.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');

        if (open) {
          scrollGele = window.scrollY;
          document.body.style.top = `-${scrollGele}px`;
          document.body.classList.add('nav-open');
        } else if (document.body.classList.contains('nav-open')) {
          document.body.classList.remove('nav-open');
          document.body.style.top = '';
          // `instant` explicitement : `scroll-behavior:smooth` s'applique
          // aussi aux défilements du script, et la page serait revenue à sa
          // position en glissant, à vue.
          window.scrollTo({ top: scrollGele, behavior: 'instant' });
        }
      };
      const closeNav = () => setNav(false);
      // Exposé : l'aperçu en fichier unique intercepte les clics en phase
      // de capture et les stoppe net, si bien que le gestionnaire ci-dessous
      // n'est jamais atteint. Son routeur ferme donc le tiroir lui-même.
      fermerMenu = closeNav;

      burger.addEventListener('click', () => setNav(!nav.classList.contains('open')));

      // Depuis le tiroir ouvert, on referme *puis* on navigue. Sans cela la
      // navigation part si vite que le tiroir n'a pas une image pour sortir :
      // il reste figé ouvert pendant tout le chargement. L'attente est courte
      // et couvre le début du chargement, qui se fait pendant la sortie.
      $$('.nav a').forEach(a => a.addEventListener('click', e => {
        if (!nav.classList.contains('open')) return;
        const url = a.getAttribute('href');
        closeNav();
        if (!url || url.startsWith('#') || a.target) return;
        e.preventDefault();
        setTimeout(() => { location.href = a.href; }, 200);
      }));
      document.addEventListener('keydown', e => { if (e.key === 'Escape') closeNav(); });

      // Le voile est un pseudo-élément de <body> : un appui dessus vise
      // donc <body>. C'est le geste attendu pour refermer un tiroir.
      document.addEventListener('click', e => {
        if (!document.body.classList.contains('nav-open')) return;
        if (e.target.closest('#nav, #burger')) return;
        closeNav();
      });

      // Le tiroir n'existe qu'en dessous de 1000 px — le seuil du CSS.
      // À 860, le menu se refermait tout seul entre 861 et 1000 px.
      window.addEventListener('resize', () => { if (window.innerWidth > 1000) closeNav(); });
    }

    /* --- Pastille de navigation --- */
    const navList = $('#navList'), navPill = $('#navPill');
    if (navList && navPill) {
      $$('.nav__link', navList).forEach(link => {
        link.addEventListener('pointerenter', () => {
          navPill.style.setProperty('--x', link.offsetLeft + 'px');
          navPill.style.setProperty('--w', link.offsetWidth + 'px');
        });
      });
    }

    initMagnetic(header);

    /* --- Boucle de scroll --- */
    let ticking = false;
    window.addEventListener('scroll', () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => { onScroll(); applyParallax(); ticking = false; });
    }, { passive: true });
    window.addEventListener('resize', () => {
      applyParallax();
      if (carousel) carousel.measure();
    });

    /* --- Défilement inertiel ----------------------------------------
       La page rattrape le geste au lieu de le suivre au pixel.
       Pointeur fin seulement : le tactile a déjà sa propre inertie,
       native et meilleure que tout ce qu'on pourrait simuler. */
    let scrollTo = null;
    if (fine && !reduced) {
      // `scroll-behavior:smooth` en CSS animerait aussi nos scrollTo :
      // les deux moteurs se battraient.
      document.documentElement.classList.add('js-smooth');

      let target = window.scrollY, current = window.scrollY, running = false;
      const max = () => document.documentElement.scrollHeight - window.innerHeight;

      const step = () => {
        const diff = target - current;
        if (Math.abs(diff) < 0.4) {
          current = target;
          window.scrollTo(0, current);
          running = false;
          return;
        }
        current += diff * 0.11;                  // plus bas = plus glissant
        window.scrollTo(0, current);
        requestAnimationFrame(step);
      };
      const kick = () => { if (!running) { running = true; requestAnimationFrame(step); } };
      scrollTo = y => { target = Math.max(0, Math.min(max(), y)); kick(); };

      window.addEventListener('wheel', e => {
        if (e.ctrlKey) return;                                   // zoom navigateur
        if (document.body.classList.contains('nav-open')) return;
        if (e.target.closest('textarea, select')) return;        // zones défilables
        e.preventDefault();
        target = Math.max(0, Math.min(max(), target + e.deltaY));
        kick();
      }, { passive: false });

      window.addEventListener('scroll', () => {
        if (!running) { target = current = window.scrollY; }
      }, { passive: true });
      window.addEventListener('resize', () => { target = current = window.scrollY; });
    }

    /* --- Ancres internes (délégué : survit au remplacement du contenu) --- */
    document.addEventListener('click', e => {
      const a = e.target.closest('a[href^="#"]');
      if (!a) return;
      const id = a.getAttribute('href');
      if (id.length < 2) return;
      const dest = document.querySelector(id);
      if (!dest) return;
      e.preventDefault();
      const headerH = parseFloat(
        getComputedStyle(document.documentElement).getPropertyValue('--header-h')) || 86;
      const top = dest.getBoundingClientRect().top + window.scrollY - headerH - 14;
      if (scrollTo) scrollTo(top);
      else window.scrollTo({ top, behavior: reduced ? 'auto' : 'smooth' });
    });

    /* --- Transition entre pages ----------------------------------
       Il n'y en a plus. Le clic retenait la navigation 280 ms pour
       jouer un fondu de sortie : autant d'attente ajoutée avant même
       que le navigateur commence à charger. L'entrée se fait par une
       animation CSS courte, qui ne bloque rien. */
  }

  initShell();
  initPage();

  // Point d'entrée pour rebrancher un contenu remplacé (aperçu multi-pages)
  window.marieMassage = { initPage, fermerMenu: () => fermerMenu() };
})();
