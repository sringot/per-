/* =========================================================
   MARIE MASSAGE — Interactions & animations
   ========================================================= */
(function () {
  'use strict';

  const $  = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1. PRELOADER ---------- */
  const preloader = $('#preloader');
  const start = () => {
    document.body.classList.add('ready');
    setTimeout(() => {
      preloader.classList.add('done');
      setTimeout(() => preloader.remove(), 700);
    }, reduced ? 0 : 400);
  };
  window.addEventListener('load', start);
  // Filet de sécurité si `load` traîne (polices, images lentes)
  setTimeout(() => {
    if (preloader.isConnected && !document.body.classList.contains('ready')) start();
  }, 2500);

  /* ---------- 2. ANNÉE COURANTE ---------- */
  $('#year').textContent = new Date().getFullYear();

  /* ---------- 3. HEADER & BOUTON REMONTER ---------- */
  const header = $('#header');
  const totop  = $('#totop');
  const cue    = $('#cue');

  function onScroll() {
    const y = window.scrollY;
    header.classList.toggle('scrolled', y > 20);
    totop.classList.toggle('show', y > 700);
    if (cue) cue.classList.toggle('gone', y > 90);
  }

  /* ---------- 4. MENU MOBILE ---------- */
  const burger = $('#burger');
  const nav    = $('#nav');

  function closeNav() {
    nav.classList.remove('open');
    burger.classList.remove('open');
    burger.setAttribute('aria-expanded', 'false');
    burger.setAttribute('aria-label', 'Ouvrir le menu');
    document.body.classList.remove('nav-open');
  }

  burger.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    burger.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
    document.body.classList.toggle('nav-open', open);
  });

  $$('.nav a').forEach(a => a.addEventListener('click', closeNav));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeNav(); });
  window.addEventListener('resize', () => { if (window.innerWidth > 860) closeNav(); });

  /* ---------- 5. RÉVÉLATION AU SCROLL ---------- */
  const revealables = $$('[data-reveal]');
  if ('IntersectionObserver' in window && !reduced) {
    const io = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('in');
        obs.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    revealables.forEach(el => io.observe(el));
  } else {
    revealables.forEach(el => el.classList.add('in'));
  }

  /* ---------- 6. COMPTEURS ---------- */
  const counters = $$('.count');
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
  if ('IntersectionObserver' in window && !reduced) {
    const co = new IntersectionObserver((entries, obs) => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        runCounter(e.target);
        obs.unobserve(e.target);
      });
    }, { threshold: 0.6 });
    counters.forEach(el => co.observe(el));
  } else {
    counters.forEach(el => {
      const d = parseInt(el.dataset.decimals || '0', 10);
      el.textContent = parseFloat(el.dataset.count).toFixed(d).replace('.', ',') + (el.dataset.suffix || '');
    });
  }

  /* ---------- 7. NAVIGATION ACTIVE (scrollspy) ---------- */
  const sections = $$('main section[id]');
  const navLinks = $$('.nav__link');
  if ('IntersectionObserver' in window) {
    const so = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        navLinks.forEach(l =>
          l.classList.toggle('active', l.getAttribute('href') === '#' + e.target.id)
        );
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(s => so.observe(s));
  }

  /* ---------- 8. PARALLAXE ---------- */
  const parallaxEls = $$('[data-parallax]');
  function applyParallax() {
    if (reduced) return;
    const vh = window.innerHeight;
    parallaxEls.forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.bottom < -200 || rect.top > vh + 200) return;
      const speed  = parseFloat(el.dataset.parallax);
      const offset = (rect.top + rect.height / 2 - vh / 2) * speed;
      el.style.setProperty('--py', offset.toFixed(1) + 'px');
      el.style.translate = `0 ${offset.toFixed(1)}px`;
    });
  }

  /* ---------- 9. BOUCLE DE SCROLL (rAF) ---------- */
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => { onScroll(); applyParallax(); ticking = false; });
  }, { passive: true });
  window.addEventListener('resize', applyParallax);
  onScroll(); applyParallax();

  /* ---------- 10. DÉFILEMENT INERTIEL ----------
     Le scroll natif est remplacé par une position interpolée : la page
     rattrape le geste au lieu de le suivre au pixel. Uniquement sur
     pointeur fin — le tactile a déjà sa propre inertie, native et
     meilleure que tout ce qu'on pourrait simuler. */
  const fine = window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  let scrollTo = null;

  if (fine && !reduced) {
    // `scroll-behavior:smooth` en CSS animerait aussi nos scrollTo :
    // les deux moteurs se battraient. On rend la main au CSS seulement
    // si ce module ne tourne pas.
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

    // Clavier, barre de défilement, retour arrière : on se resynchronise
    window.addEventListener('scroll', () => {
      if (!running) { target = current = window.scrollY; }
    }, { passive: true });

    window.addEventListener('resize', () => { target = current = window.scrollY; });
  }

  // Les ancres passent par le même moteur, pour une arrivée amortie
  $$('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
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
  });

  /* ---------- 11. BOUTONS MAGNÉTIQUES ----------
     Le bouton se déporte légèrement vers le curseur puis revient :
     ça donne l'impression qu'il vient à la rencontre du geste. */
  if (fine && !reduced) {
    $$('.magnetic').forEach(el => {
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

  /* ---------- 12. INCLINAISON DU VISUEL ---------- */
  const tilt = $('#heroTilt');
  const tiltZone = $('#heroVisual');
  if (tilt && tiltZone && fine && !reduced) {
    tiltZone.addEventListener('pointermove', e => {
      const r = tiltZone.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width  - 0.5;
      const py = (e.clientY - r.top)  / r.height - 0.5;
      tilt.style.setProperty('--ry', (px * 7).toFixed(2) + 'deg');
      tilt.style.setProperty('--rx', (-py * 7).toFixed(2) + 'deg');
    });
    tiltZone.addEventListener('pointerleave', () => {
      tilt.style.setProperty('--ry', '0deg');
      tilt.style.setProperty('--rx', '0deg');
    });
  }

  /* ---------- 13. PASTILLE DE NAVIGATION ---------- */
  const navList = $('#navList');
  const navPill = $('#navPill');
  if (navList && navPill) {
    $$('.nav__link', navList).forEach(link => {
      link.addEventListener('pointerenter', () => {
        navPill.style.setProperty('--x', link.offsetLeft + 'px');
        navPill.style.setProperty('--w', link.offsetWidth + 'px');
      });
    });
  }

  /* ---------- 14. CARROUSEL D'AVIS ---------- */
  const track = $('#revTrack');
  const prev  = $('#revPrev');
  const next  = $('#revNext');
  const dots  = $('#revDots');
  const slides = $$('.review', track);

  let index = 0, perView = 3, pages = 1, autoplay;

  function measure() {
    const w = window.innerWidth;
    perView = w <= 860 ? 1 : w <= 1080 ? 2 : 3;
    pages = Math.max(1, slides.length - perView + 1);
    index = Math.min(index, pages - 1);
    buildDots();
    goTo(index, false);
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

  function goTo(i, animate = true) {
    index = (i + pages) % pages;
    const slide = slides[0];
    if (!slide) return;
    const gap  = parseFloat(getComputedStyle(track).columnGap || getComputedStyle(track).gap) || 0;
    const step = slide.getBoundingClientRect().width + gap;

    track.style.transition = animate ? '' : 'none';
    track.style.transform  = `translate3d(${-index * step}px,0,0)`;
    if (!animate) requestAnimationFrame(() => { track.style.transition = ''; });

    $$('button', dots).forEach((d, n) => d.classList.toggle('active', n === index));
  }

  function startAuto() {
    if (reduced) return;
    stopAuto();
    autoplay = setInterval(() => goTo(index + 1), 5200);
  }
  function stopAuto() { clearInterval(autoplay); }

  if (track && slides.length) {
    prev.addEventListener('click', () => { goTo(index - 1); stopAuto(); });
    next.addEventListener('click', () => { goTo(index + 1); stopAuto(); });
    track.addEventListener('mouseenter', stopAuto);
    track.addEventListener('mouseleave', startAuto);

    // Swipe tactile
    let x0 = null;
    track.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; stopAuto(); }, { passive: true });
    track.addEventListener('touchend', e => {
      if (x0 === null) return;
      const dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 45) goTo(index + (dx < 0 ? 1 : -1));
      x0 = null;
      startAuto();
    });

    window.addEventListener('resize', measure);
    measure();
    startAuto();
  }

  /* ---------- 15. FORMULAIRE ---------- */
  const form = $('#form');
  const note = $('#formNote');
  const submitBtn = $('#submit');

  const rules = {
    nom:     v => v.trim().length >= 2                    || 'Merci d’indiquer votre nom.',
    email:   v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) || 'Adresse email invalide.',
    tel:     v => v === '' || /^[\d\s+().-]{8,}$/.test(v) || 'Numéro de téléphone invalide.',
    soin:    v => v !== ''                                || 'Choisissez un soin.',
    message: v => v.trim().length >= 10                   || 'Votre message est un peu court.'
  };

  function validateField(el) {
    const rule = rules[el.name];
    if (!rule) return true;
    const res = rule(el.value);
    const field = el.closest('.field');
    field.classList.toggle('err', res !== true);
    $('.field__err', field).textContent = res === true ? '' : res;
    return res === true;
  }

  $$('.field input, .field select, .field textarea', form).forEach(el => {
    el.addEventListener('blur', () => validateField(el));
    el.addEventListener('input', () => {
      if (el.closest('.field').classList.contains('err')) validateField(el);
    });
  });

  form.addEventListener('submit', e => {
    e.preventDefault();
    note.className = 'form__note';
    note.textContent = '';

    // On valide toujours les champs d'abord, pour que les erreurs
    // soient visibles même si la case RGPD est décochée.
    const fields = $$('.field input, .field select, .field textarea', form);
    const fieldsOk = fields.map(validateField).every(Boolean);
    const rgpdOk = $('#rgpd').checked;

    if (!fieldsOk || !rgpdOk) {
      note.classList.add('ko');
      note.textContent = !fieldsOk && !rgpdOk
        ? 'Quelques champs sont à corriger, et il faut accepter d’être recontactée.'
        : !fieldsOk
          ? 'Quelques champs sont à corriger.'
          : 'Merci d’accepter d’être recontactée.';
      const first = $('.field.err input, .field.err select, .field.err textarea');
      (first || (rgpdOk ? null : $('#rgpd')))?.focus();
      return;
    }

    // TODO : brancher un service d'envoi (Formspree, Netlify Forms, EmailJS…)
    // Pour l'instant : simulation locale, aucun email n'est réellement envoyé.
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;

    setTimeout(() => {
      submitBtn.classList.remove('loading');
      submitBtn.disabled = false;
      note.classList.add('ok');
      note.textContent = 'Merci ! Votre demande a bien été prise en compte, je vous réponds très vite.';
      form.reset();
      $$('.field', form).forEach(f => f.classList.remove('err'));
    }, 1100);
  });

})();
