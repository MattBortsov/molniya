/* ============================================================
   Молния Тех — page behavior
   Scroll-shaped hero, section reveals and shared page controls.
   ============================================================ */

/* ---- Hero scene: turn the full-width nav and iPad into inset cards on scroll ---- */
function initHeroScrollScene() {
  const hero = document.querySelector('[data-mt-hero-scene]');
  const nav = document.querySelector('.mt-nav');
  if (!hero || !nav) return;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let frame = 0;

  const clamp = (value, min, max) => Math.min(Math.max(value, min), max);
  const smoothstep = (value) => value * value * (3 - 2 * value);
  const easeOut = (value) => 1 - Math.pow(1 - value, 3);

  const update = () => {
    frame = 0;

    const viewportHeight = window.innerHeight || 800;
    const viewportWidth = window.innerWidth || 1280;
    const sceneStart = hero.offsetTop - nav.offsetHeight;
    const sceneScroll = Math.max(0, window.scrollY - sceneStart);

    const navDistance = clamp(viewportHeight * .24, 160, 300);
    const mediaDistance = clamp(viewportHeight * .34, 280, 460);
    const navRaw = clamp(sceneScroll / navDistance, 0, 1);
    const mediaRaw = clamp((sceneScroll - viewportHeight * .24) / mediaDistance, 0, 1);

    const navProgress = reducedMotion.matches ? (navRaw > 0 ? 1 : 0) : easeOut(navRaw);
    const mediaProgress = reducedMotion.matches ? (mediaRaw > 0 ? 1 : 0) : smoothstep(mediaRaw);
    const compact = viewportWidth <= 720;

    const navInset = navProgress * (compact ? 10 : Math.min(24, viewportWidth * .018));
    const navScale = 1 - (navInset * 2 / viewportWidth);
    const navTop = navProgress * (compact ? 10 : 18);
    const navRadius = navProgress * (compact ? 14 : 18);
    const mediaScale = 1 - mediaProgress * (compact ? .06 : .3);
    const mediaOffset = mediaProgress * (compact ? 12 : 150);

    nav.style.setProperty('--mt-nav-scale-x', navScale.toFixed(5));
    nav.style.setProperty('--mt-nav-top', navTop.toFixed(2) + 'px');
    nav.style.setProperty('--mt-nav-radius', navRadius.toFixed(2) + 'px');
    nav.toggleAttribute('data-scrolled', navRaw > .04);

    hero.style.setProperty('--mt-hero-media-scale', mediaScale.toFixed(5));
    hero.style.setProperty('--mt-hero-media-offset', mediaOffset.toFixed(2) + 'px');
  };

  const requestUpdate = () => {
    if (frame) return;
    frame = window.requestAnimationFrame(update);
  };

  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', requestUpdate);
  reducedMotion.addEventListener?.('change', requestUpdate);
  update();
}

/* ---- Scroll reveal ---- */
function initReveal() {
  const els = Array.from(document.querySelectorAll('[data-mt-reveal]'));
  if (!els.length) return;

  const reveal = (el) => {
    el.style.opacity = '1';
    el.style.transform = 'none';
  };
  const vh = window.innerHeight || 800;
  const hidden = [];

  els.forEach((el) => {
    el.style.transition =
      'opacity .75s cubic-bezier(.22,1,.36,1), transform .75s cubic-bezier(.22,1,.36,1)';
    const d = parseInt(el.getAttribute('data-mt-delay') || '0', 10);
    if (d) el.style.transitionDelay = d / 1000 + 's';
    // reveal anything already in (or near) the viewport immediately; animate only what's below
    if (el.getBoundingClientRect().top < vh * 0.9) {
      reveal(el);
      return;
    }
    el.style.opacity = '0';
    el.style.transform = 'translateY(28px)';
    hidden.push(el);
  });

  if (hidden.length && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            reveal(e.target);
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -7% 0px' }
    );
    hidden.forEach((el) => io.observe(el));
  } else {
    hidden.forEach(reveal);
  }

  // safety: reveal everything after 1.6s in case the observer never fires
  setTimeout(() => hidden.forEach(reveal), 1600);
}

/* ---- Sticky CTA: hidden over the hero and the final CTA/footer (which have their own CTA),
   shown only for the stretch of the page in between ---- */
function initStickyCta() {
  const sticky = document.querySelector('.mt-btn-sticky');
  const hero = document.querySelector('.mt-hero');
  const finalCta = document.querySelector('.mt-section--final-cta');
  const footer = document.querySelector('.mt-footer');
  if (!sticky || !hero) return;

  if ('IntersectionObserver' in window) {
    const guarded = new Set();
    const sync = () => {
      sticky.toggleAttribute('data-visible', guarded.size === 0);
    };
    const observe = (el, margin) => {
      if (!el) return;
      const io = new IntersectionObserver(
        (entries) => {
          entries.forEach((e) => {
            if (e.isIntersecting) guarded.add(el);
            else guarded.delete(el);
          });
          sync();
        },
        { rootMargin: margin }
      );
      io.observe(el);
    };
    observe(hero, '-64px 0px 0px 0px');
    observe(finalCta, '0px 0px -64px 0px');
    observe(footer, '0px 0px -64px 0px');
  } else {
    sticky.setAttribute('data-visible', 'true');
  }
}

/* ---- Mobile menu toggle ---- */
function initMobileMenu() {
  const burger = document.querySelector('.mt-nav-burger');
  const menu = document.getElementById('mt-mobile-menu');
  if (!burger || !menu) return;

  const close = () => {
    burger.setAttribute('aria-expanded', 'false');
    menu.removeAttribute('data-open');
  };
  const toggle = () => {
    const open = burger.getAttribute('aria-expanded') === 'true';
    burger.setAttribute('aria-expanded', String(!open));
    if (open) menu.removeAttribute('data-open');
    else menu.setAttribute('data-open', 'true');
  };

  burger.addEventListener('click', toggle);
  menu.querySelectorAll('a').forEach((a) => a.addEventListener('click', close));
}

/* ---- Cookie notice: show once until accepted, then remember in localStorage ---- */
function initCookieBanner() {
  const banner = document.getElementById('mt-cookie-banner');
  const accept = document.getElementById('mt-cookie-accept');
  if (!banner || !accept) return;

  const STORAGE_KEY = 'mt_cookie_consent';
  try {
    if (localStorage.getItem(STORAGE_KEY) === 'accepted') return;
  } catch (e) {
    // localStorage unavailable (private mode, blocked) — show banner every visit
  }

  banner.setAttribute('data-visible', 'true');

  accept.addEventListener('click', function () {
    try {
      localStorage.setItem(STORAGE_KEY, 'accepted');
    } catch (e) {
      // ignore — banner will just reappear next visit
    }
    banner.removeAttribute('data-visible');
  });
}

document.addEventListener('DOMContentLoaded', function () {
  initHeroScrollScene();
  initReveal();
  initMobileMenu();
  initStickyCta();
  initCookieBanner();
});
