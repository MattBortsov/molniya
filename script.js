/* ============================================================
   Молния Тех — page behavior
   Reveals sections on scroll (IntersectionObserver).
   The hero is static; everything below it fades in on scroll.
   ============================================================ */

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
  initReveal();
  initMobileMenu();
  initStickyCta();
  initCookieBanner();
});
