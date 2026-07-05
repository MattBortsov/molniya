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

document.addEventListener('DOMContentLoaded', function () {
  initReveal();
  initMobileMenu();
});
