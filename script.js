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

/* ---- Overview split scene: 5 cards break out of 1 unified shape on scroll ---- */
function initOverviewSplitScene() {
  const grids = Array.from(document.querySelectorAll('.mt-overview-grid'));
  if (!grids.length) return;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (reducedMotion.matches) {
    grids.forEach((grid) => {
      grid.style.setProperty('--mt-split', '1');
      grid.setAttribute('data-split', '');
    });
    return;
  }

  let frame = 0;
  const clamp = (val, min, max) => Math.min(Math.max(val, min), max);
  const smoothstep = (t) => t * t * (3 - 2 * t);

  const update = () => {
    frame = 0;
    const vh = window.innerHeight || 800;

    grids.forEach((grid) => {
      const rect = grid.getBoundingClientRect();
      // Hold the joined shape on screen before the gaps and inner corners open.
      const startY = vh * 0.38;
      const endY = vh * 0.02;

      const raw = clamp((startY - rect.top) / (startY - endY), 0, 1);
      const progress = smoothstep(raw);

      grid.style.setProperty('--mt-split', progress.toFixed(4));
      grid.toggleAttribute('data-split', progress > 0.45);
      grid.setAttribute('data-split-initialized', '');
    });
  };

  const requestUpdate = () => {
    if (frame) return;
    frame = window.requestAnimationFrame(update);
  };

  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', requestUpdate);
  reducedMotion.addEventListener?.('change', () => {
    if (reducedMotion.matches) {
      grids.forEach((grid) => {
        grid.style.setProperty('--mt-split', '1');
        grid.setAttribute('data-split', '');
      });
    } else {
      requestUpdate();
    }
  });

  update();
}

/* ---- Modules split scene: 6 cards diverge on scroll ---- */
function initModulesSplitScene() {
  const grids = Array.from(document.querySelectorAll('.mt-modules-grid'));
  if (!grids.length) return;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (reducedMotion.matches) {
    grids.forEach((grid) => {
      grid.style.setProperty('--mt-split', '1');
      grid.setAttribute('data-split', '');
    });
    return;
  }

  let frame = 0;
  const clamp = (val, min, max) => Math.min(Math.max(val, min), max);
  const smoothstep = (t) => t * t * (3 - 2 * t);

  const update = () => {
    frame = 0;
    const vh = window.innerHeight || 800;

    grids.forEach((grid) => {
      const rect = grid.getBoundingClientRect();
      const startY = vh * 0.88;
      const endY = vh * 0.22;

      const raw = clamp((startY - rect.top) / (startY - endY), 0, 1);
      const progress = smoothstep(raw);

      grid.style.setProperty('--mt-split', progress.toFixed(4));
      grid.toggleAttribute('data-split', progress > 0.6);
      grid.setAttribute('data-split-initialized', '');
    });
  };

  const requestUpdate = () => {
    if (frame) return;
    frame = window.requestAnimationFrame(update);
  };

  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', requestUpdate);
  reducedMotion.addEventListener?.('change', () => {
    if (reducedMotion.matches) {
      grids.forEach((grid) => {
        grid.style.setProperty('--mt-split', '1');
        grid.setAttribute('data-split', '');
      });
    } else {
      requestUpdate();
    }
  });

  update();
}

/* ---- Journey steps: smooth progressive reveal on scroll ---- */
function initJourneySteps() {
  const lists = Array.from(document.querySelectorAll('.mt-journey-list'));
  if (!lists.length) return;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  lists.forEach((list) => {
    const steps = Array.from(list.querySelectorAll('.mt-journey-step'));
    if (!steps.length) return;

    if (reducedMotion.matches) {
      steps.forEach((step) => step.setAttribute('data-revealed', ''));
      return;
    }

    list.setAttribute('data-step-reveal', '');

    const vh = window.innerHeight || 800;
    const toObserve = [];

    steps.forEach((step) => {
      // If already in viewport upon initial load, reveal right away
      if (step.getBoundingClientRect().top < vh * 0.85) {
        step.setAttribute('data-revealed', '');
      } else {
        toObserve.push(step);
      }
    });

    if (!toObserve.length) return;

    if (!('IntersectionObserver' in window)) {
      toObserve.forEach((s) => s.setAttribute('data-revealed', ''));
      return;
    }

    let pending = [];
    let flushTimer = null;

    const flushQueue = () => {
      pending.forEach((el, index) => {
        setTimeout(() => {
          el.setAttribute('data-revealed', '');
        }, index * 120);
      });
      pending = [];
      flushTimer = null;
    };

    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            io.unobserve(e.target);
            pending.push(e.target);
            if (!flushTimer) {
              flushTimer = setTimeout(flushQueue, 35);
            }
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -6% 0px' }
    );

    toObserve.forEach((s) => io.observe(s));
  });
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

  // safety: generous fallback in case observer doesn't fire over long period
  setTimeout(() => hidden.forEach(reveal), 8000);
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

/* ---- Desktop "Для кого" dropdown ---- */
function initNavDropdown() {
  const item = document.querySelector('.mt-nav-item--dropdown');
  const btn = item?.querySelector('.mt-nav-link--dropdown');
  const menu = item?.querySelector('.mt-dropdown-menu');
  if (!item || !btn || !menu) return;

  let closeTimer = null;

  const open = () => {
    if (closeTimer) {
      clearTimeout(closeTimer);
      closeTimer = null;
    }
    btn.setAttribute('aria-expanded', 'true');
    item.setAttribute('data-open', 'true');
  };

  const scheduleClose = (delay = 320) => {
    if (closeTimer) clearTimeout(closeTimer);
    closeTimer = setTimeout(() => {
      close();
    }, delay);
  };

  const close = () => {
    if (closeTimer) {
      clearTimeout(closeTimer);
      closeTimer = null;
    }
    btn.setAttribute('aria-expanded', 'false');
    item.removeAttribute('data-open');
  };

  // Hover management with generous movement buffer
  item.addEventListener('mouseenter', open);
  item.addEventListener('mouseleave', () => scheduleClose(320));

  // Toggle on click
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    const isOpen = item.getAttribute('data-open') === 'true';
    if (isOpen) close();
    else open();
  });

  // Close when clicking outside
  document.addEventListener('click', (e) => {
    if (!item.contains(e.target)) {
      close();
    }
  });

  // Close on Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      close();
      btn.blur();
    }
  });

  // Close on link click inside dropdown
  menu.querySelectorAll('a').forEach((a) => {
    a.addEventListener('click', close);
  });
}

/* ---- Mobile menu toggle & accordion ---- */
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

  // Mobile submenu accordion
  const accordion = menu.querySelector('.mt-mobile-accordion');
  const accBtn = accordion?.querySelector('.mt-mobile-accordion-btn');
  if (accordion && accBtn) {
    accBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = accBtn.getAttribute('aria-expanded') === 'true';
      accBtn.setAttribute('aria-expanded', String(!isOpen));
      if (isOpen) accordion.removeAttribute('data-open');
      else accordion.setAttribute('data-open', 'true');
    });
  }
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

/* ---- Industry fit check through the same-origin API proxy ---- */
function initIndustryFitForm() {
  const form = document.querySelector('[data-industry-fit-form]');
  if (!form) return;

  const input = form.elements.business;
  const honeypot = form.elements.website;
  const button = form.querySelector('button[type="submit"]');
  const buttonText = button?.querySelector('span');
  const result = form.querySelector('[data-fit-result]');
  const title = form.querySelector('[data-fit-title]');
  const message = form.querySelector('[data-fit-message]');
  const consultation = form.querySelector('[data-fit-consultation]');
  const status = form.querySelector('[data-fit-status]');
  if (!input || !button || !buttonText || !result || !title || !message || !consultation || !status) return;

  const defaultButtonText = buttonText.textContent;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const business = input.value.trim();
    if (business.length < 3) {
      form.dataset.state = 'error';
      status.textContent = 'Опишите сферу хотя бы несколькими словами.';
      input.focus();
      return;
    }

    form.dataset.state = 'loading';
    result.hidden = true;
    consultation.hidden = true;
    status.textContent = 'Проверяем описание…';
    button.disabled = true;
    buttonText.textContent = 'Проверяем';

    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 12000);

    try {
      const response = await fetch('/api/industry-fit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ business, website: honeypot?.value || '' }),
        signal: controller.signal
      });
      const payload = await response.json().catch(() => ({}));

      if (!response.ok || !payload.title || !payload.message) {
        throw new Error(payload.error || 'Не удалось получить ответ');
      }

      title.textContent = payload.title;
      message.textContent = payload.message;
      consultation.hidden = !['clarify', 'not_fit'].includes(payload.status);
      result.hidden = false;
      form.dataset.state = payload.status || 'ready';
      status.textContent = '';
    } catch (error) {
      form.dataset.state = 'error';
      status.textContent = error.name === 'AbortError'
        ? 'Проверка заняла больше обычного. Попробуйте ещё раз.'
        : 'Сейчас не удалось проверить. Попробуйте ещё раз чуть позже.';
    } finally {
      window.clearTimeout(timeout);
      button.disabled = false;
      buttonText.textContent = defaultButtonText;
    }
  });
}

/* ---- Contact requests are sent through the same-origin API ---- */
function initLeadForm() {
  const form = document.querySelector('[data-lead-form]');
  if (!form) return;

  const button = form.querySelector('button[type="submit"]');
  const status = form.querySelector('[data-lead-status]');
  const defaultButtonText = button.textContent;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!form.reportValidity() || button.disabled) return;

    button.disabled = true;
    button.textContent = 'Отправляем…';
    status.textContent = '';
    status.removeAttribute('data-state');

    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 12000);

    try {
      const response = await fetch('/api/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: form.elements.name.value.trim(),
          email: form.elements.email.value.trim(),
          phone: form.elements.phone.value.trim(),
          source: form.dataset.leadSource,
          consent: form.elements.consent.checked,
          website: form.elements.website.value
        }),
        signal: controller.signal
      });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok || payload.ok !== true) {
        throw new Error(payload.error || 'Не удалось отправить заявку');
      }

      form.reset();
      status.dataset.state = 'success';
      status.textContent = 'Заявка отправлена! Открываем страницу с презентацией…';
      window.setTimeout(() => {
        window.location.href = '/thanks';
      }, 350);
    } catch (error) {
      status.dataset.state = 'error';
      status.textContent = error.name === 'AbortError'
        ? 'Ответ задерживается. Проверьте связь и попробуйте позже.'
        : error.name === 'TypeError'
          ? 'Не удалось связаться с сервером. Попробуйте позже.'
          : error.message || 'Не удалось отправить заявку. Попробуйте позже.';
    } finally {
      window.clearTimeout(timeout);
      button.disabled = false;
      button.textContent = defaultButtonText;
    }
  });
}

/* ---- Product screenshots: one screen at a time, chosen by the reader ---- */
function initVisibilityGallery() {
  const gallery = document.querySelector('[data-visibility-gallery]');
  if (!gallery) return;

  const tabs = Array.from(gallery.querySelectorAll('[data-visibility-tab]'));
  const panels = Array.from(gallery.querySelectorAll('[data-visibility-panel]'));
  if (tabs.length !== panels.length || !tabs.length) return;

  const select = (index, focus = false) => {
    tabs.forEach((tab, position) => {
      const active = position === index;
      tab.setAttribute('aria-selected', String(active));
      tab.tabIndex = active ? 0 : -1;
      panels[position].hidden = !active;
    });
    if (focus) tabs[index].focus();
  };

  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => select(index));
    tab.addEventListener('keydown', (event) => {
      let next = index;
      if (event.key === 'ArrowDown' || event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      else if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = tabs.length - 1;
      else return;
      event.preventDefault();
      select(next, true);
    });
  });
}

/* ---- Requisites page: copy to clipboard buttons ---- */
function copyTextToClipboard(text) {
  if (navigator.clipboard && window.isSecureContext) {
    return navigator.clipboard.writeText(text).catch(function () {
      return legacyCopyToClipboard(text);
    });
  }
  return legacyCopyToClipboard(text);
}

function legacyCopyToClipboard(text) {
  return new Promise(function (resolve, reject) {
    try {
      var textArea = document.createElement('textarea');
      textArea.value = text;
      textArea.style.position = 'fixed';
      textArea.style.top = '0';
      textArea.style.left = '0';
      textArea.style.width = '2em';
      textArea.style.height = '2em';
      textArea.style.padding = '0';
      textArea.style.border = 'none';
      textArea.style.outline = 'none';
      textArea.style.boxShadow = 'none';
      textArea.style.background = 'transparent';
      textArea.style.fontSize = '16px';
      textArea.setAttribute('readonly', '');
      document.body.appendChild(textArea);

      textArea.focus();
      textArea.select();
      textArea.setSelectionRange(0, textArea.value.length);

      var successful = document.execCommand('copy');
      document.body.removeChild(textArea);
      if (successful) {
        resolve();
      } else {
        reject(new Error('execCommand copy failed'));
      }
    } catch (err) {
      if (textArea && textArea.parentNode) {
        textArea.parentNode.removeChild(textArea);
      }
      reject(err);
    }
  });
}

function initRequisitesCopy() {
  var copyButtons = document.querySelectorAll('.mt-copy-btn');
  copyButtons.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var text = btn.getAttribute('data-copy') || btn.closest('.mt-req-row')?.querySelector('.mt-req-value')?.textContent?.trim() || '';
      if (!text) return;

      copyTextToClipboard(text).then(function () {
        if (!btn.getAttribute('data-orig')) {
          btn.setAttribute('data-orig', btn.textContent.trim());
        }
        var orig = btn.getAttribute('data-orig');
        btn.textContent = 'Скопировано!';
        btn.classList.add('copied');

        clearTimeout(btn._copyTimeout);
        btn._copyTimeout = setTimeout(function () {
          btn.textContent = orig;
          btn.classList.remove('copied');
        }, 2000);
      }).catch(function (err) {
        console.error('Failed to copy: ', err);
      });
    });
  });

  var copyAllBtn = document.getElementById('copy-all-btn');
  if (copyAllBtn) {
    copyAllBtn.addEventListener('click', function (e) {
      e.preventDefault();
      var fullText = [
        'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "МОЛНИЯ ТЕХ"',
        'Юридический адрес: 195112, РОССИЯ, Г. САНКТ-ПЕТЕРБУРГ, ВН.ТЕР.Г. МУНИЦИПАЛЬНЫЙ ОКРУГ МАЛАЯ ОХТА, ПР-КТ МАЛООХТИНСКИЙ, Д. 61, ЛИТЕРА А, ПОМЕЩ. 1-Н',
        'ИНН: 7806637461',
        'КПП: 780601001',
        'ОГРН: 1267800068458',
        'Расчетный счет: 40702810110002359085',
        'Банк: АО «ТБанк»',
        'БИК: 044525974',
        'ИНН банка: 7710140679',
        'Корр. счет: 30101810145250000974',
        'Юр. адрес банка: 127287, г. Москва, ул. Хуторская 2-я, д. 38А, стр. 26'
      ].join('\n');

      copyTextToClipboard(fullText).then(function () {
        if (!copyAllBtn.getAttribute('data-orig-html')) {
          copyAllBtn.setAttribute('data-orig-html', copyAllBtn.innerHTML);
        }
        var origHtml = copyAllBtn.getAttribute('data-orig-html');
        copyAllBtn.textContent = 'Все реквизиты скопированы!';
        copyAllBtn.classList.add('copied');

        clearTimeout(copyAllBtn._copyTimeout);
        copyAllBtn._copyTimeout = setTimeout(function () {
          copyAllBtn.innerHTML = origHtml;
          copyAllBtn.classList.remove('copied');
        }, 2500);
      }).catch(function (err) {
        console.error('Failed to copy all: ', err);
      });
    });
  }
}

/* ============================================================
   Production Calendar & Calculator (/calendar)
   ============================================================ */

function initCalendarTool() {
  var app = document.getElementById('mt-calendar-app');
  if (!app) return;

  var CALENDAR_DATA = {
    2025: "11111111001100000110000011000001100000110000011000001100000110000211000001100000110000011000001100000110000011000001100211110001111000001100000110000011000001100211110000011000001100000110000011000001100000110000011000001100000110000011000001100000110000011000001100000110000011000001100000110000011000002111000110000011000001100000110000011000001100000110000011001",
    2026: "11111111111000001100000110000011000001100000110000011100001100000111000011000001100000110000011000001100000110000011000211100002111000011000001100000110000011000211100000110000011000001100000110000011000001100000110000011000001100000110000011000001100000110000011000001100000110000011000001100000110000011021001100000110000011000001100000110000011000001100000110001",
    2027: "11111111110000011000001100000110000011000001100000211100011000001110000110000011000001100000110000011000001100000110000211100001110000110000011000001100000110000211100001100000110000011000001100000110000011000001100000110000011000001100000110000011000001100000110000011000001100000110000011000001100000110021111000001100000110000011000001100000110000011000001100001"
  };

  var MONTH_NAMES = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
  ];

  var currentYear = 2026;
  var yearBtns = app.querySelectorAll('[data-cal-year]');
  var monthsGrid = app.querySelector('[data-cal-months]');
  var fromInput = app.querySelector('[data-cal-from]');
  var toInput = app.querySelector('[data-cal-to]');
  var scheduleSelect = app.querySelector('[data-cal-schedule]');
  var salaryInput = app.querySelector('[data-cal-salary]');
  var presetBtns = app.querySelectorAll('[data-cal-preset]');

  var statTotal = app.querySelector('[data-cal-total-days]');
  var statWork = app.querySelector('[data-cal-work-days]');
  var statOff = app.querySelector('[data-cal-off-days]');
  var statShort = app.querySelector('[data-cal-short-days]');
  var statH40 = app.querySelector('[data-cal-hours-40]');
  var statH36 = app.querySelector('[data-cal-hours-36]');
  var statH24 = app.querySelector('[data-cal-hours-24]');

  var resPayout = app.querySelector('[data-cal-res-payout]');
  var resNet = app.querySelector('[data-cal-res-net]');
  var resCalDays = app.querySelector('[data-cal-res-cal-days]');
  var resWorkDays = app.querySelector('[data-cal-res-work-days]');
  var resHours = app.querySelector('[data-cal-res-hours]');
  var resDayRate = app.querySelector('[data-cal-res-day-rate]');
  var resHourRate = app.querySelector('[data-cal-res-hour-rate]');

  function isLeapYear(y) {
    return (y % 4 === 0 && y % 100 !== 0) || (y % 400 === 0);
  }

  function getDaysInMonth(y, m) {
    return [31, isLeapYear(y) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m];
  }

  function getDayOfYear(y, m, d) {
    var count = 0;
    for (var i = 0; i < m; i++) {
      count += getDaysInMonth(y, i);
    }
    return count + (d - 1);
  }

  function formatMoney(num) {
    return Math.round(num).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' ₽';
  }

  function renderCalendar(year) {
    var dataStr = CALENDAR_DATA[year];
    if (!dataStr) return;

    var totalDays = isLeapYear(year) ? 366 : 365;
    var workCount = 0;
    var shortCount = 0;
    var offCount = 0;

    for (var i = 0; i < totalDays && i < dataStr.length; i++) {
      var c = dataStr.charAt(i);
      if (c === '0') workCount++;
      else if (c === '2') { workCount++; shortCount++; }
      else if (c === '1') offCount++;
    }

    var h40 = workCount * 8 - shortCount;
    var h36 = Number((workCount * 7.2 - shortCount).toFixed(1));
    var h24 = Number((workCount * 4.8 - shortCount).toFixed(1));

    if (statTotal) statTotal.textContent = totalDays;
    if (statWork) statWork.textContent = workCount;
    if (statOff) statOff.textContent = offCount;
    if (statShort) statShort.textContent = shortCount;
    if (statH40) statH40.textContent = h40.toLocaleString('ru-RU') + ' ч';
    if (statH36) statH36.textContent = h36.toLocaleString('ru-RU') + ' ч';
    if (statH24) statH24.textContent = h24.toLocaleString('ru-RU') + ' ч';

    if (!monthsGrid) return;
    monthsGrid.innerHTML = '';

    var today = new Date();
    var isCurrentActualYear = (today.getFullYear() === year);
    var todayMonth = today.getMonth();
    var todayDate = today.getDate();

    for (var m = 0; m < 12; m++) {
      var daysInM = getDaysInMonth(year, m);
      var firstDayWeekday = new Date(year, m, 1).getDay();
      var startCol = (firstDayWeekday === 0) ? 6 : (firstDayWeekday - 1);

      var mCard = document.createElement('article');
      mCard.className = 'mt-cal-month-card';

      var mHead = document.createElement('div');
      mHead.className = 'mt-cal-month-head';

      var mTitle = document.createElement('span');
      mTitle.className = 'mt-cal-month-title';
      mTitle.textContent = MONTH_NAMES[m];

      var mBadge = document.createElement('span');
      mBadge.className = 'mt-cal-month-badge';

      mHead.appendChild(mTitle);
      mHead.appendChild(mBadge);
      mCard.appendChild(mHead);

      var weekdaysRow = document.createElement('div');
      weekdaysRow.className = 'mt-cal-weekdays';
      var wdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
      for (var w = 0; w < 7; w++) {
        var wsp = document.createElement('span');
        wsp.textContent = wdays[w];
        weekdaysRow.appendChild(wsp);
      }
      mCard.appendChild(weekdaysRow);

      var daysGrid = document.createElement('div');
      daysGrid.className = 'mt-cal-days-grid';

      for (var e = 0; e < startCol; e++) {
        var emptyCell = document.createElement('span');
        emptyCell.className = 'mt-cal-day-cell mt-cal-day-cell--empty';
        daysGrid.appendChild(emptyCell);
      }

      var mWork = 0;
      var mShort = 0;
      var mOff = 0;

      for (var d = 1; d <= daysInM; d++) {
        var dayIdx = getDayOfYear(year, m, d);
        var dayCode = dataStr.charAt(dayIdx) || '0';
        var dayCell = document.createElement('span');
        dayCell.className = 'mt-cal-day-cell';
        dayCell.textContent = d;

        var weekday = (startCol + d - 1) % 7;
        var isWeekend = (weekday === 5 || weekday === 6);

        if (dayCode === '0') {
          dayCell.classList.add(isWeekend ? 'mt-cal-day-cell--weekend' : 'mt-cal-day-cell--work');
          mWork++;
        } else if (dayCode === '2') {
          dayCell.classList.add('mt-cal-day-cell--short');
          dayCell.title = 'Сокращённый на 1 час рабочий день';
          mWork++;
          mShort++;
        } else {
          dayCell.classList.add(isWeekend ? 'mt-cal-day-cell--weekend' : 'mt-cal-day-cell--holiday');
          if (!isWeekend) dayCell.title = 'Праздничный день';
          mOff++;
        }

        if (isCurrentActualYear && m === todayMonth && d === todayDate) {
          dayCell.classList.add('mt-cal-day-cell--today');
          dayCell.title = (dayCell.title ? dayCell.title + ' • ' : '') + 'Сегодня';
        }

        daysGrid.appendChild(dayCell);
      }

      mCard.appendChild(daysGrid);

      var mH40 = mWork * 8 - mShort;
      mBadge.textContent = mWork + ' раб';

      var mFoot = document.createElement('div');
      mFoot.className = 'mt-cal-month-foot';
      mFoot.innerHTML = '<span>Раб: <strong>' + mWork + '</strong> · Вых: <strong>' + mOff + '</strong></span><span>40ч: <strong>' + mH40 + ' ч</strong></span>';
      mCard.appendChild(mFoot);

      monthsGrid.appendChild(mCard);
    }
  }

  function calculate() {
    if (!fromInput || !toInput || !scheduleSelect || !salaryInput) return;

    var fromStr = fromInput.value;
    var toStr = toInput.value;
    if (!fromStr || !toStr) return;

    var fromDate = new Date(fromStr + 'T00:00:00');
    var toDate = new Date(toStr + 'T00:00:00');
    if (isNaN(fromDate.getTime()) || isNaN(toDate.getTime())) return;

    if (fromDate > toDate) {
      var tmp = fromDate;
      fromDate = toDate;
      toDate = tmp;
      fromInput.value = toStr;
      toInput.value = fromStr;
    }

    var salary = parseFloat(salaryInput.value.replace(/\s+/g, '')) || 0;
    var schedule = scheduleSelect.value;

    var calDays = 0;
    var workDays = 0;
    var workHours = 0;

    var cur = new Date(fromDate.getTime());
    var dayCounter = 0;

    while (cur <= toDate) {
      calDays++;
      var curY = cur.getFullYear();
      var curM = cur.getMonth();
      var curD = cur.getDate();
      var dataStr = CALENDAR_DATA[curY] || CALENDAR_DATA[2026];
      var dayIdx = getDayOfYear(curY, curM, curD);
      var code = dataStr.charAt(dayIdx) || '0';

      if (schedule === '5/2') {
        if (code === '0') {
          workDays++;
          workHours += 8;
        } else if (code === '2') {
          workDays++;
          workHours += 7;
        }
      } else if (schedule === '2/2') {
        if (dayCounter % 4 < 2) {
          workDays++;
          workHours += 12;
        }
      } else if (schedule === '3/3') {
        if (dayCounter % 6 < 3) {
          workDays++;
          workHours += 12;
        }
      } else if (schedule === '1/3') {
        if (dayCounter % 4 === 0) {
          workDays++;
          workHours += 24;
        }
      }

      cur.setDate(cur.getDate() + 1);
      dayCounter++;
    }

    var baseM = fromDate.getMonth();
    var baseY = fromDate.getFullYear();
    var baseData = CALENDAR_DATA[baseY] || CALENDAR_DATA[2026];
    var baseDaysInM = getDaysInMonth(baseY, baseM);
    var baseWorkDays = 0;
    var baseHours = 0;

    for (var d = 1; d <= baseDaysInM; d++) {
      var dIdx = getDayOfYear(baseY, baseM, d);
      var c = baseData.charAt(dIdx) || '0';
      if (c === '0') {
        baseWorkDays++;
        baseHours += 8;
      } else if (c === '2') {
        baseWorkDays++;
        baseHours += 7;
      }
    }
    if (baseWorkDays === 0) baseWorkDays = 21;
    if (baseHours === 0) baseHours = 168;

    var dayRate = salary / baseWorkDays;
    var hourRate = salary / baseHours;

    var gross = 0;
    if (schedule === '5/2') {
      gross = workDays * dayRate;
    } else {
      gross = workHours * hourRate;
    }

    var net = gross * 0.87;

    if (resPayout) resPayout.textContent = formatMoney(gross);
    if (resNet) resNet.textContent = '~' + formatMoney(net) + ' на руки (после НДФЛ 13%)';
    if (resCalDays) resCalDays.textContent = calDays + ' дн.';
    if (resWorkDays) resWorkDays.textContent = workDays + (schedule === '5/2' ? ' дн.' : ' смен');
    if (resHours) resHours.textContent = workHours.toLocaleString('ru-RU') + ' ч';
    if (resDayRate) resDayRate.textContent = formatMoney(dayRate);
    if (resHourRate) resHourRate.textContent = formatMoney(hourRate);
  }

  function setPreset(presetKey) {
    var nowY = currentYear;
    var pad = function(n) { return (n < 10 ? '0' : '') + n; };

    if (presetKey === 'current-month') {
      var today = new Date();
      var m = (today.getFullYear() === nowY) ? today.getMonth() : 0;
      var lastD = getDaysInMonth(nowY, m);
      fromInput.value = nowY + '-' + pad(m + 1) + '-01';
      toInput.value = nowY + '-' + pad(m + 1) + '-' + pad(lastD);
    } else if (presetKey === 'q1') {
      fromInput.value = nowY + '-01-01';
      toInput.value = nowY + '-03-31';
    } else if (presetKey === 'q2') {
      fromInput.value = nowY + '-04-01';
      toInput.value = nowY + '-06-30';
    } else if (presetKey === 'q3') {
      fromInput.value = nowY + '-07-01';
      toInput.value = nowY + '-09-30';
    } else if (presetKey === 'q4') {
      fromInput.value = nowY + '-10-01';
      toInput.value = nowY + '-12-31';
    } else if (presetKey === 'year') {
      fromInput.value = nowY + '-01-01';
      toInput.value = nowY + '-12-31';
    }

    for (var i = 0; i < presetBtns.length; i++) {
      presetBtns[i].classList.toggle('is-active', presetBtns[i].getAttribute('data-cal-preset') === presetKey);
    }

    calculate();
  }

  for (var i = 0; i < yearBtns.length; i++) {
    (function(btn) {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        var y = parseInt(btn.getAttribute('data-cal-year'), 10);
        if (!y || y === currentYear) return;
        currentYear = y;

        for (var j = 0; j < yearBtns.length; j++) {
          yearBtns[j].classList.toggle('is-active', yearBtns[j] === btn);
        }

        renderCalendar(currentYear);
        setPreset('current-month');
      });
    })(yearBtns[i]);
  }

  for (var k = 0; k < presetBtns.length; k++) {
    (function(pBtn) {
      pBtn.addEventListener('click', function(e) {
        e.preventDefault();
        var key = pBtn.getAttribute('data-cal-preset');
        setPreset(key);
      });
    })(presetBtns[k]);
  }

  if (fromInput) fromInput.addEventListener('change', calculate);
  if (toInput) toInput.addEventListener('change', calculate);
  if (scheduleSelect) scheduleSelect.addEventListener('change', calculate);
  if (salaryInput) salaryInput.addEventListener('input', calculate);

  renderCalendar(currentYear);
  setPreset('current-month');
}

/* ============================================================
   Counterparty INN Verification Tool (/inn)
   ============================================================ */

function initInnChecker() {
  var app = document.getElementById('mt-inn-app');
  if (!app) return;

  var form = app.querySelector('.mt-inn-form');
  var input = app.querySelector('.mt-inn-input');
  var clearBtn = app.querySelector('.mt-inn-clear-btn');
  var loadingEl = app.querySelector('.mt-inn-loading');
  var errorEl = app.querySelector('.mt-inn-error');
  var cardEl = app.querySelector('.mt-inn-card');
  var sampleChips = app.querySelectorAll('.mt-inn-chip');

  if (!cardEl) return;

  var titleEl = cardEl.querySelector('[data-inn-title]');
  var fullNameEl = cardEl.querySelector('[data-inn-fullname]');
  var statusBadge = cardEl.querySelector('[data-inn-status]');
  var copyBtn = cardEl.querySelector('.mt-inn-copy-btn');
  var pdfBtn = cardEl.querySelector('.mt-inn-pdf-btn');

  var cellInn = cardEl.querySelector('[data-inn-cell-inn]');
  var valInn = cardEl.querySelector('[data-inn-val-inn]');
  var valKpp = cardEl.querySelector('[data-inn-val-kpp]');
  var cellKpp = cardEl.querySelector('[data-inn-cell-kpp]');
  var valOgrn = cardEl.querySelector('[data-inn-val-ogrn]');
  var valRegDate = cardEl.querySelector('[data-inn-val-reg-date]');
  var valRegion = cardEl.querySelector('[data-inn-val-region]');
  var valDirector = cardEl.querySelector('[data-inn-val-director]');
  var valOkved = cardEl.querySelector('[data-inn-val-okved]');
  var cellAddress = cardEl.querySelector('[data-inn-cell-address]');
  var valAddress = cardEl.querySelector('[data-inn-val-address]');

  var riskBankrupt = cardEl.querySelector('[data-inn-risk-bankrupt]');
  var riskSanctions = cardEl.querySelector('[data-inn-risk-sanctions]');
  var riskAgent = cardEl.querySelector('[data-inn-risk-agent]');
  var riskInspections = cardEl.querySelector('[data-inn-risk-inspections]');

  var currentData = null;
  var copyTimeout = null;

  function updateClearBtn() {
    if (!clearBtn || !input) return;
    if (input.value.trim().length > 0) {
      clearBtn.classList.add('is-visible');
    } else {
      clearBtn.classList.remove('is-visible');
    }
  }

  if (input) {
    input.addEventListener('input', updateClearBtn);
  }

  if (clearBtn) {
    clearBtn.addEventListener('click', function() {
      input.value = '';
      updateClearBtn();
      input.focus();
    });
  }

  function showError(msg) {
    if (loadingEl) loadingEl.classList.remove('is-active');
    cardEl.classList.remove('is-active');
    if (errorEl) {
      errorEl.textContent = msg;
      errorEl.classList.add('is-active');
    }
  }

  function hideError() {
    if (errorEl) errorEl.classList.remove('is-active');
  }

  function setRiskStatus(el, isOk, textOk, textWarn) {
    if (!el) return;
    var icon = el.querySelector('.mt-inn-risk-icon');
    var label = el.querySelector('.mt-inn-risk-label');
    if (isOk) {
      if (icon) {
        icon.className = 'mt-inn-risk-icon mt-inn-risk-icon--ok';
        icon.textContent = '✓';
      }
      if (label) label.textContent = textOk;
    } else {
      if (icon) {
        icon.className = 'mt-inn-risk-icon mt-inn-risk-icon--warn';
        icon.textContent = '!';
      }
      if (label) label.textContent = textWarn;
    }
  }

  function displayResult(d) {
    currentData = d;
    if (loadingEl) loadingEl.classList.remove('is-active');
    hideError();

    if (titleEl) titleEl.textContent = d.name_short || d.name_full || 'Организация';
    if (fullNameEl) fullNameEl.textContent = d.name_full || '';

    if (statusBadge) {
      statusBadge.textContent = d.status_text || 'Действующая организация';
      statusBadge.className = 'mt-inn-status ' + (d.status === 'active' ? 'mt-inn-status--active' : 'mt-inn-status--liquidated');
    }

    if (valInn) valInn.textContent = d.inn || '—';
    if (valOgrn) valOgrn.textContent = d.ogrn || '—';
    if (valRegDate) {
      var dateStr = d.reg_date || '—';
      if (d.term_date) {
        dateStr += ' (ликвидация: ' + d.term_date + ')';
      }
      valRegDate.textContent = dateStr;
    }
    if (valRegion) valRegion.textContent = d.region || '—';
    if (valDirector) valDirector.textContent = d.director || '—';

    if (cellAddress && valAddress) {
      if (!d.address && d.type === 'fl') {
        cellAddress.style.display = 'none';
      } else {
        cellAddress.style.display = '';
        valAddress.textContent = d.address || (d.region ? d.region + ' (по данным ФНС)' : '—');
      }
    } else if (valAddress) {
      valAddress.textContent = d.address || (d.region ? d.region + ' (по данным ФНС)' : '—');
    }

    if (cellInn) {
      cellInn.style.gridColumn = (d.type === 'fl' ? 'span 2' : '');
    }

    if (valOkved) {
      if (d.okved && d.okved_name) {
        valOkved.textContent = d.okved + ' ' + d.okved_name;
      } else if (d.okved) {
        valOkved.textContent = d.okved;
      } else {
        valOkved.textContent = 'По данным выписки ЕГРЮЛ';
      }
    }

    if (cellKpp && valKpp) {
      if (d.type === 'fl' || !d.kpp) {
        cellKpp.style.display = 'none';
      } else {
        cellKpp.style.display = 'flex';
        valKpp.textContent = d.kpp;
      }
    }

    // Risks
    var r = d.risk || {};
    setRiskStatus(
      riskBankrupt,
      !r.is_bankrupt,
      'В реестре банкротств не числится',
      'Внимание: выявлено банкротное производство'
    );
    setRiskStatus(
      riskSanctions,
      !r.is_sanctioned,
      'В санкционных списках отсутствует',
      'Внимание: включен в санкционные списки'
    );
    setRiskStatus(
      riskAgent,
      !r.is_foreign_agent,
      'Не является иностранным агентом',
      'Внимание: статус иностранного агента'
    );

    if (riskInspections) {
      var inspCount = r.inspections_count || 0;
      setRiskStatus(
        riskInspections,
        true,
        inspCount > 0 ? (inspCount + ' проверок в ЕРКНМ Генпрокуратуры') : 'Проверок в ЕРКНМ не зафиксировано',
        'Проверки надзорных органов'
      );
    }

    // PDF extract button
    if (pdfBtn) {
      if (d.pdf_token) {
        pdfBtn.style.display = 'inline-flex';
        pdfBtn.setAttribute('href', '/api/inn/pdf?token=' + encodeURIComponent(d.pdf_token) + '&inn=' + encodeURIComponent(d.inn));
        pdfBtn.setAttribute('target', '_blank');
      } else {
        pdfBtn.style.display = 'none';
      }
    }

    cardEl.classList.add('is-active');
  }

  function search(query) {
    var cleaned = (query || '').replace(/\s+/g, '');
    if (!cleaned || !/^\d+$/.test(cleaned) || [10, 12, 13, 15].indexOf(cleaned.length) === -1) {
      showError('Введите корректный ИНН (10 или 12 цифр) или ОГРН (13 или 15 цифр)');
      return;
    }

    hideError();
    cardEl.classList.remove('is-active');
    if (loadingEl) loadingEl.classList.add('is-active');

    fetch('/api/inn?query=' + encodeURIComponent(cleaned))
      .then(function(res) {
        return res.json().then(function(json) {
          if (!res.ok) {
            throw new Error(json.error || 'Ошибка при проверке контрагента');
          }
          return json;
        });
      })
      .then(function(data) {
        displayResult(data);
      })
      .catch(function(err) {
        showError(err.message || 'Сервер проверки контрагентов временно недоступен. Попробуйте снова.');
      });
  }

  if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      search(input ? input.value : '');
    });
  }

  if (sampleChips && sampleChips.length) {
    for (var i = 0; i < sampleChips.length; i++) {
      sampleChips[i].addEventListener('click', function() {
        var sampleInn = this.getAttribute('data-sample-inn');
        if (sampleInn && input) {
          input.value = sampleInn;
          updateClearBtn();
          search(sampleInn);
        }
      });
    }
  }

  if (copyBtn) {
    copyBtn.addEventListener('click', function(e) {
      e.preventDefault();
      if (!currentData) return;

      var lines = [
        'Полное наименование: ' + (currentData.name_full || currentData.name_short),
        'Краткое наименование: ' + (currentData.name_short || currentData.name_full),
        'ИНН: ' + (currentData.inn || '—'),
      ];
      if (currentData.kpp) lines.push('КПП: ' + currentData.kpp);
      if (currentData.ogrn) lines.push((currentData.type === 'fl' ? 'ОГРНИП: ' : 'ОГРН: ') + currentData.ogrn);
      if (currentData.reg_date) lines.push('Дата регистрации: ' + currentData.reg_date);
      if (currentData.address) lines.push('Юридический адрес: ' + currentData.address);
      if (currentData.director) lines.push('Руководитель: ' + currentData.director);
      if (currentData.okved) lines.push('Основной ОКВЭД: ' + currentData.okved + ' ' + (currentData.okved_name || ''));
      lines.push('Статус: ' + (currentData.status_text || 'Действующая организация'));

      var textToCopy = lines.join('\n');

      copyTextToClipboard(textToCopy).then(function() {
        if (!copyBtn.getAttribute('data-orig')) {
          copyBtn.setAttribute('data-orig', copyBtn.textContent.trim());
        }
        copyBtn.textContent = '✓ Реквизиты скопированы';
        copyBtn.classList.add('copied');

        if (copyTimeout) clearTimeout(copyTimeout);
        copyTimeout = setTimeout(function() {
          copyBtn.textContent = copyBtn.getAttribute('data-orig');
          copyBtn.classList.remove('copied');
        }, 2200);
      });
    });
  }

  var urlParams = new URLSearchParams(window.location.search);
  var qParam = urlParams.get('query') || urlParams.get('inn');
  if (qParam) {
    if (input) input.value = qParam;
    updateClearBtn();
    search(qParam);
  } else {
    if (input) input.value = '7707083893';
    updateClearBtn();
    search('7707083893');
  }
}

/* ============================================================
   Margin & Business Profitability Calculator Tool (/margin)
   ============================================================ */

function initMarginCalculator() {
  var app = document.getElementById('mt-margin-app');
  if (!app) return;

  var PRESETS = {
    beauty: { places: 4, check: 2200, duration: 60, hours: 12, days: 30, util: 55, fixed: 130000, labor: 40, mat: 10 },
    auto: { places: 3, check: 6500, duration: 120, hours: 11, days: 30, util: 60, fixed: 180000, labor: 35, mat: 15 },
    fitness: { places: 2, check: 9000, duration: 60, hours: 12, days: 30, util: 65, fixed: 140000, labor: 30, mat: 5 },
    massage: { places: 3, check: 3800, duration: 75, hours: 11, days: 30, util: 50, fixed: 110000, labor: 40, mat: 12 },
    carwash: { places: 4, check: 1200, duration: 35, hours: 14, days: 30, util: 60, fixed: 160000, labor: 30, mat: 10 }
  };

  var placesSlider = app.querySelector('[data-margin-slider="places"]');
  var placesNum = app.querySelector('[data-margin-num="places"]');
  var placesVal = app.querySelector('[data-margin-val="places"]');

  var checkSlider = app.querySelector('[data-margin-slider="check"]');
  var checkNum = app.querySelector('[data-margin-num="check"]');
  var checkVal = app.querySelector('[data-margin-val="check"]');

  var durationSlider = app.querySelector('[data-margin-slider="duration"]');
  var durationNum = app.querySelector('[data-margin-num="duration"]');
  var durationVal = app.querySelector('[data-margin-val="duration"]');

  var hoursSlider = app.querySelector('[data-margin-slider="hours"]');
  var hoursNum = app.querySelector('[data-margin-num="hours"]');
  var hoursVal = app.querySelector('[data-margin-val="hours"]');

  var utilSlider = app.querySelector('[data-margin-slider="util"]');
  var utilNum = app.querySelector('[data-margin-num="util"]');
  var utilVal = app.querySelector('[data-margin-val="util"]');

  var fixedSlider = app.querySelector('[data-margin-slider="fixed"]');
  var fixedNum = app.querySelector('[data-margin-num="fixed"]');
  var fixedVal = app.querySelector('[data-margin-val="fixed"]');

  var laborSlider = app.querySelector('[data-margin-slider="labor"]');
  var laborNum = app.querySelector('[data-margin-num="labor"]');
  var laborVal = app.querySelector('[data-margin-val="labor"]');

  var matSlider = app.querySelector('[data-margin-slider="mat"]');
  var matNum = app.querySelector('[data-margin-num="mat"]');
  var matVal = app.querySelector('[data-margin-val="mat"]');

  var outRevenue = app.querySelector('[data-margin-res="revenue"]');
  var outRevenueSub = app.querySelector('[data-margin-res="revenue-sub"]');
  var outProfit = app.querySelector('[data-margin-res="profit"]');
  var outProfitSub = app.querySelector('[data-margin-res="profit-sub"]');
  var outMargin = app.querySelector('[data-margin-res="margin"]');
  var outMarginSub = app.querySelector('[data-margin-res="margin-sub"]');
  var outBreakEven = app.querySelector('[data-margin-res="breakeven"]');
  var outBreakEvenSub = app.querySelector('[data-margin-res="breakeven-sub"]');

  var barProfit = app.querySelector('[data-margin-bar="profit"]');
  var barLabor = app.querySelector('[data-margin-bar="labor"]');
  var barMat = app.querySelector('[data-margin-bar="materials"]');
  var barFixed = app.querySelector('[data-margin-bar="fixed"]');

  var legProfit = app.querySelector('[data-margin-leg="profit"]');
  var legLabor = app.querySelector('[data-margin-leg="labor"]');
  var legMat = app.querySelector('[data-margin-leg="materials"]');
  var legFixed = app.querySelector('[data-margin-leg="fixed"]');

  var outGrowthSum = app.querySelector('[data-margin-growth-sum]');

  var copyBtn = app.querySelector('.mt-margin-copy-btn');
  var copyTimeout = null;

  var presetBtns = app.querySelectorAll('.mt-margin-preset-btn');

  function fmtMoney(num) {
    return Math.round(num).toLocaleString('ru-RU') + ' ₽';
  }

  function bindTwoWay(slider, num, valDisplay, suffix) {
    if (!slider || !num) return;
    function sync(fromSlider) {
      var val = fromSlider ? slider.value : num.value;
      if (fromSlider) {
        num.value = val;
      } else {
        slider.value = val;
      }
      if (valDisplay) {
        valDisplay.textContent = Number(val).toLocaleString('ru-RU') + (suffix || '');
      }
      calculate();
    }
    slider.addEventListener('input', function() { sync(true); });
    num.addEventListener('input', function() { sync(false); });
  }

  bindTwoWay(placesSlider, placesNum, placesVal, '');
  bindTwoWay(checkSlider, checkNum, checkVal, ' ₽');
  bindTwoWay(durationSlider, durationNum, durationVal, ' мин');
  bindTwoWay(hoursSlider, hoursNum, hoursVal, ' ч');
  bindTwoWay(utilSlider, utilNum, utilVal, '%');
  bindTwoWay(fixedSlider, fixedNum, fixedVal, ' ₽');
  bindTwoWay(laborSlider, laborNum, laborVal, '%');
  bindTwoWay(matSlider, matNum, matVal, '%');

  function applyPreset(p) {
    if (placesSlider) { placesSlider.value = p.places; placesNum.value = p.places; if (placesVal) placesVal.textContent = p.places; }
    if (checkSlider) { checkSlider.value = p.check; checkNum.value = p.check; if (checkVal) checkVal.textContent = p.check.toLocaleString('ru-RU') + ' ₽'; }
    if (durationSlider) { durationSlider.value = p.duration; durationNum.value = p.duration; if (durationVal) durationVal.textContent = p.duration + ' мин'; }
    if (hoursSlider) { hoursSlider.value = p.hours; hoursNum.value = p.hours; if (hoursVal) hoursVal.textContent = p.hours + ' ч'; }
    if (utilSlider) { utilSlider.value = p.util; utilNum.value = p.util; if (utilVal) utilVal.textContent = p.util + '%'; }
    if (fixedSlider) { fixedSlider.value = p.fixed; fixedNum.value = p.fixed; if (fixedVal) fixedVal.textContent = p.fixed.toLocaleString('ru-RU') + ' ₽'; }
    if (laborSlider) { laborSlider.value = p.labor; laborNum.value = p.labor; if (laborVal) laborVal.textContent = p.labor + '%'; }
    if (matSlider) { matSlider.value = p.mat; matNum.value = p.mat; if (matVal) matVal.textContent = p.mat + '%'; }
    calculate();
  }

  for (var i = 0; i < presetBtns.length; i++) {
    presetBtns[i].addEventListener('click', function() {
      for (var j = 0; j < presetBtns.length; j++) presetBtns[j].classList.remove('is-active');
      this.classList.add('is-active');
      var key = this.getAttribute('data-margin-preset');
      if (PRESETS[key]) {
        applyPreset(PRESETS[key]);
      }
    });
  }

  var lastCalc = {};

  function calculate() {
    var places = Math.max(1, parseInt(placesSlider ? placesSlider.value : 4, 10));
    var check = Math.max(1, parseFloat(checkSlider ? checkSlider.value : 2200));
    var duration = Math.max(10, parseInt(durationSlider ? durationSlider.value : 60, 10));
    var hours = Math.max(4, parseInt(hoursSlider ? hoursSlider.value : 12, 10));
    var util = Math.max(5, Math.min(100, parseInt(utilSlider ? utilSlider.value : 55, 10)));
    var fixed = Math.max(0, parseFloat(fixedSlider ? fixedSlider.value : 130000));
    var laborPct = Math.max(0, Math.min(90, parseInt(laborSlider ? laborSlider.value : 40, 10)));
    var matPct = Math.max(0, Math.min(50, parseInt(matSlider ? matSlider.value : 10, 10)));
    var days = 30;

    var capacityPerDay = Math.floor((hours * 60) / duration);
    var maxClients = places * capacityPerDay * days;
    var maxRevenue = maxClients * check;

    var actualClients = Math.round(maxClients * (util / 100));
    var actualRevenue = actualClients * check;
    var lostRevenue = Math.max(0, maxRevenue - actualRevenue);

    var laborCost = Math.round(actualRevenue * (laborPct / 100));
    var materialsCost = Math.round(actualRevenue * (matPct / 100));
    var totalExpenses = fixed + laborCost + materialsCost;
    var netProfit = actualRevenue - totalExpenses;

    var profitMargin = actualRevenue > 0 ? ((netProfit / actualRevenue) * 100).toFixed(1) : '0';

    var varPct = (laborPct + matPct) / 100;
    var marginPerClient = check * (1 - varPct);
    var breakEvenClients = marginPerClient > 0 ? Math.ceil(fixed / marginPerClient) : 0;
    var breakEvenRevenue = breakEvenClients * check;

    var boostedUtil = Math.min(100, util + 20);
    var boostedClients = Math.round(maxClients * (boostedUtil / 100));
    var boostedRev = boostedClients * check;
    var boostedLabor = Math.round(boostedRev * (laborPct / 100));
    var boostedMat = Math.round(boostedRev * (matPct / 100));
    var boostedProfit = boostedRev - (fixed + boostedLabor + boostedMat);
    var addedProfit = Math.max(0, boostedProfit - netProfit);

    lastCalc = {
      places: places,
      check: check,
      duration: duration,
      hours: hours,
      util: util,
      fixed: fixed,
      laborPct: laborPct,
      matPct: matPct,
      actualClients: actualClients,
      maxClients: maxClients,
      actualRevenue: actualRevenue,
      maxRevenue: maxRevenue,
      lostRevenue: lostRevenue,
      netProfit: netProfit,
      profitMargin: profitMargin,
      breakEvenRevenue: breakEvenRevenue,
      breakEvenClients: breakEvenClients,
      addedProfit: addedProfit
    };

    if (outRevenue) outRevenue.textContent = fmtMoney(actualRevenue);
    if (outRevenueSub) outRevenueSub.textContent = 'Потенциал при 100%: ' + fmtMoney(maxRevenue);

    if (outProfit) {
      outProfit.textContent = (netProfit >= 0 ? '+' : '') + fmtMoney(netProfit);
      outProfit.className = 'mt-margin-kpi-num ' + (netProfit >= 0 ? 'mt-margin-kpi-num--accent' : 'mt-margin-kpi-num--warn');
    }
    if (outProfitSub) {
      outProfitSub.textContent = netProfit >= 0 ? (Math.round(netProfit / days).toLocaleString('ru-RU') + ' ₽/день чистыми') : 'Бизнес работает в убыток';
    }

    if (outMargin) outMargin.textContent = profitMargin + '%';
    if (outMarginSub) outMarginSub.textContent = 'Упущенная выгода: ' + fmtMoney(lostRevenue);

    if (outBreakEven) outBreakEven.textContent = fmtMoney(breakEvenRevenue);
    if (outBreakEvenSub) outBreakEvenSub.textContent = breakEvenClients + ' клиентов в месяц для окупаемости';

    if (actualRevenue > 0) {
      var profitShare = Math.max(0, netProfit / actualRevenue);
      var laborShare = laborCost / actualRevenue;
      var matShare = materialsCost / actualRevenue;
      var fixedShare = Math.min(1, fixed / actualRevenue);

      var totalShare = profitShare + laborShare + matShare + fixedShare;
      var pPct = Math.round((profitShare / totalShare) * 100);
      var lPct = Math.round((laborShare / totalShare) * 100);
      var mPct = Math.round((matShare / totalShare) * 100);
      var fPct = Math.max(0, 100 - (pPct + lPct + mPct));

      if (barProfit) barProfit.style.width = pPct + '%';
      if (barLabor) barLabor.style.width = lPct + '%';
      if (barMat) barMat.style.width = mPct + '%';
      if (barFixed) barFixed.style.width = fPct + '%';

      if (legProfit) legProfit.textContent = fmtMoney(Math.max(0, netProfit)) + ' (' + pPct + '%)';
      if (legLabor) legLabor.textContent = fmtMoney(laborCost) + ' (' + lPct + '%)';
      if (legMat) legMat.textContent = fmtMoney(materialsCost) + ' (' + mPct + '%)';
      if (legFixed) legFixed.textContent = fmtMoney(fixed) + ' (' + fPct + '%)';
    }

    if (outGrowthSum) {
      outGrowthSum.textContent = '+' + fmtMoney(addedProfit) + ' в месяц';
    }
  }

  if (copyBtn) {
    copyBtn.addEventListener('click', function(e) {
      e.preventDefault();
      if (!lastCalc.places) return;

      var textToCopy = [
        '=== РАСЧЕТ ДОХОДНОСТИ И ЮНИТ-ЭКОНОМИКИ (МОЛНИЯ) ===',
        'Параметры бизнеса:',
        '• Рабочих мест / постов: ' + lastCalc.places,
        '• Средний чек: ' + lastCalc.check.toLocaleString('ru-RU') + ' ₽',
        '• Длительность услуги: ' + lastCalc.duration + ' мин',
        '• Режим работы: ' + lastCalc.hours + ' ч/день (30 дней/мес)',
        '• Текущая загрузка: ' + lastCalc.util + '%',
        '• Постоянные расходы: ' + lastCalc.fixed.toLocaleString('ru-RU') + ' ₽/мес',
        '• ФОТ мастеров: ' + lastCalc.laborPct + '% | Расходники: ' + lastCalc.matPct + '%',
        '',
        'Финансовые результаты:',
        '• Выручка: ' + lastCalc.actualRevenue.toLocaleString('ru-RU') + ' ₽/мес (' + lastCalc.actualClients + ' клиентов)',
        '• Потенциал при 100% загрузке: ' + lastCalc.maxRevenue.toLocaleString('ru-RU') + ' ₽/мес',
        '• Упущенная выгода от простоя: ' + lastCalc.lostRevenue.toLocaleString('ru-RU') + ' ₽/мес',
        '• Чистая прибыль владельца: ' + lastCalc.netProfit.toLocaleString('ru-RU') + ' ₽/мес',
        '• Рентабельность бизнеса: ' + lastCalc.profitMargin + '%',
        '• Точка безубыточности: ' + lastCalc.breakEvenRevenue.toLocaleString('ru-RU') + ' ₽/мес (' + lastCalc.breakEvenClients + ' клиентов)',
        '• Потенциал роста чистой прибыли с онлайн-записью Молнии (+20% загрузки): +' + lastCalc.addedProfit.toLocaleString('ru-RU') + ' ₽/мес',
        'Рассчитано на https://molniya-tech.ru/tools/margin'
      ].join('\n');

      copyTextToClipboard(textToCopy).then(function() {
        if (!copyBtn.getAttribute('data-orig')) {
          copyBtn.setAttribute('data-orig', copyBtn.textContent.trim());
        }
        copyBtn.textContent = '✓ Расчет скопирован в буфер';
        copyBtn.classList.add('copied');

        if (copyTimeout) clearTimeout(copyTimeout);
        copyTimeout = setTimeout(function() {
          copyBtn.textContent = copyBtn.getAttribute('data-orig');
          copyBtn.classList.remove('copied');
        }, 2200);
      });
    });
  }

  calculate();
}

/* ============================================================
   Interactive Tool Rating Widget
   ============================================================ */

function initToolRating() {
  var ratings = document.querySelectorAll('[data-tool-rating]');
  if (!ratings.length) return;

  for (var r = 0; r < ratings.length; r++) {
    (function(wrapper) {
      var toolSlug = wrapper.getAttribute('data-tool-rating') || 'tool';
      var stars = wrapper.querySelectorAll('.mt-tool-rating-star');
      var countEl = wrapper.querySelector('[data-rating-count]');
      var statusEl = wrapper.querySelector('[data-rating-status]');
      var storageKey = 'molniya_rated_' + toolSlug;
      var baseCount = 1902;

      var hasVoted = false;
      try {
        hasVoted = !!localStorage.getItem(storageKey);
      } catch (e) {}

      if (hasVoted && countEl) {
        countEl.textContent = (baseCount + 1).toLocaleString('ru-RU');
        if (statusEl) statusEl.textContent = 'Вы уже оценили этот инструмент';
      }

      function highlightStars(upto) {
        for (var i = 0; i < stars.length; i++) {
          stars[i].classList.toggle('is-hover', i < upto);
        }
      }

      function resetHover() {
        for (var i = 0; i < stars.length; i++) {
          stars[i].classList.remove('is-hover');
        }
      }

      for (var s = 0; s < stars.length; s++) {
        (function(star, idx) {
          star.addEventListener('mouseenter', function() {
            highlightStars(idx + 1);
          });

          star.addEventListener('click', function(e) {
            e.preventDefault();
            var prevVote = false;
            try {
              prevVote = !!localStorage.getItem(storageKey);
              localStorage.setItem(storageKey, String(idx + 1));
            } catch (err) {}

            if (!prevVote && countEl) {
              countEl.textContent = (baseCount + 1).toLocaleString('ru-RU');
            }
            if (statusEl) {
              statusEl.textContent = prevVote ? 'Оценка обновлена!' : 'Спасибо за вашу оценку!';
            }

            for (var j = 0; j < stars.length; j++) {
              stars[j].classList.toggle('is-active', j <= idx);
            }
          });
        })(stars[s], s);
      }

      var starContainer = wrapper.querySelector('.mt-tool-rating-stars');
      if (starContainer) {
        starContainer.addEventListener('mouseleave', resetHover);
      }
    })(ratings[r]);
  }
}

function initCarwashWeather() {
  var app = document.getElementById('mt-weather-app');
  if (!app) return;

  var CITY_COORDS = {
    msk: { name: 'Москва', lat: 55.7558, lon: 37.6176 },
    spb: { name: 'Санкт-Петербург', lat: 59.9343, lon: 30.3351 },
    kazan: { name: 'Казань', lat: 55.7961, lon: 49.1064 },
    ekb: { name: 'Екатеринбург', lat: 56.8389, lon: 60.6057 },
    nsk: { name: 'Новосибирск', lat: 55.0084, lon: 82.9357 },
    nn: { name: 'Нижний Новгород', lat: 56.3269, lon: 44.0059 },
    krr: { name: 'Краснодар', lat: 45.0355, lon: 38.9754 },
    samara: { name: 'Самара', lat: 53.1959, lon: 50.1002 },
    ufa: { name: 'Уфа', lat: 54.7388, lon: 55.9721 },
    rostov: { name: 'Ростов-на-Дону', lat: 47.2225, lon: 39.7187 },
    chelyabinsk: { name: 'Челябинск', lat: 55.1644, lon: 61.4368 },
    krasnoyarsk: { name: 'Красноярск', lat: 56.0153, lon: 92.8932 },
    voronezh: { name: 'Воронеж', lat: 51.6720, lon: 39.1843 },
    perm: { name: 'Пермь', lat: 58.0105, lon: 56.2502 },
    volgograd: { name: 'Волгоград', lat: 48.7080, lon: 44.5133 },
    saratov: { name: 'Саратов', lat: 51.5336, lon: 46.0343 },
    tyumen: { name: 'Тюмень', lat: 57.1530, lon: 65.5343 },
    tula: { name: 'Тула', lat: 54.1931, lon: 37.6173 },
    sochi: { name: 'Сочи', lat: 43.5855, lon: 39.7231 },
    vladivostok: { name: 'Владивосток', lat: 43.1198, lon: 131.8869 }
  };

  var WMO_MAP = {
    0: ['Ясно', 'sun'],
    1: ['Преимущественно ясно', 'sun-cloud'],
    2: ['Переменная облачность', 'cloud-sun'],
    3: ['Пасмурно', 'cloud'],
    45: ['Туман', 'fog'],
    48: ['Изморозь', 'fog'],
    51: ['Небольшая морось', 'drizzle'],
    53: ['Морось', 'drizzle'],
    55: ['Плотная морось', 'drizzle'],
    61: ['Небольшой дождь', 'rain'],
    63: ['Умеренный дождь', 'rain'],
    65: ['Сильный дождь', 'heavy-rain'],
    71: ['Небольшой снегопад', 'snow'],
    73: ['Снегопад', 'snow'],
    75: ['Сильный снегопад', 'heavy-snow'],
    77: ['Снежные зерна', 'snow'],
    80: ['Кратковременный дождь', 'rain'],
    81: ['Ливень', 'heavy-rain'],
    82: ['Шквальный ливень', 'heavy-rain'],
    85: ['Снегопад', 'snow'],
    86: ['Сильный снегопад', 'heavy-snow'],
    95: ['Гроза', 'thunder'],
    96: ['Гроза с градом', 'thunder'],
    99: ['Сильная гроза с градом', 'thunder']
  };

  var chips = app.querySelectorAll('[data-weather-city]');
  var select = document.getElementById('mt-weather-city-select');
  var geoBtn = document.getElementById('mt-weather-geo-btn');

  var scoreEl = document.getElementById('mt-weather-score');
  var scoreBadge = document.getElementById('mt-weather-score-badge');
  var verdictEl = document.getElementById('mt-weather-verdict');
  var taglineEl = document.getElementById('mt-weather-tagline');
  var adviceEl = document.getElementById('mt-weather-advice');
  var roadEl = document.getElementById('mt-weather-road');
  var precipEl = document.getElementById('mt-weather-precip');
  var tempEl = document.getElementById('mt-weather-temp');
  var heroImg = document.getElementById('mt-weather-img');
  var statusBadge = document.getElementById('mt-weather-badge');
  var daysGrid = document.getElementById('mt-weather-days-grid');

  var shareTg = document.getElementById('mt-weather-share-tg');
  var shareWa = document.getElementById('mt-weather-share-wa');
  var shareVk = document.getElementById('mt-weather-share-vk');
  var copyBtn = document.getElementById('mt-weather-copy-btn');

  var currentCity = 'msk';
  var currentData = null;

  var urlParams = new URLSearchParams(window.location.search);
  var cityParam = urlParams.get('city');
  if (cityParam && (cityParam in CITY_COORDS)) {
    currentCity = cityParam.toLowerCase();
  }

  function getWeatherEmoji(icon) {
    switch (icon) {
      case 'sun': return '☀️';
      case 'sun-cloud': return '🌤️';
      case 'cloud-sun': return '⛅';
      case 'cloud': return '☁️';
      case 'fog': return '🌫️';
      case 'drizzle': return '🌦️';
      case 'rain': return '🌧️';
      case 'heavy-rain': return '⛈️';
      case 'snow': return '🌨️';
      case 'heavy-snow': return '❄️';
      case 'thunder': return '⚡';
      default: return '🌤️';
    }
  }

  function computeClientWashIndex(forecast, cityName, citySlug) {
    var daily = forecast.daily || {};
    var times = daily.time || [];
    var probs = daily.precipitation_probability_max || [];
    var sums = daily.precipitation_sum || [];
    var codes = daily.weathercode || [];
    var tMax = daily.temperature_2m_max || [];
    var tMin = daily.temperature_2m_min || [];
    var currWeather = forecast.current_weather || {};
    var currTemp = Math.round(currWeather.temperature !== undefined ? currWeather.temperature : (tMax[0] || 12));

    var p0 = probs[0] || 0;
    var s0 = sums[0] || 0;
    var p1 = probs[1] || p0;
    var s1 = sums[1] || s0;
    var p2 = probs[2] || p1;
    var s2 = sums[2] || s1;

    var precipPenalty = (p0 * 0.45) + (p1 * 0.35) + (p2 * 0.15);
    precipPenalty += Math.min(s0 * 6.0, 25.0) + Math.min(s1 * 4.0, 15.0) + Math.min(s2 * 2.0, 10.0);

    var tempPenalty = 0;
    var isSlush = false;
    if ((tMin[0] < 0 && tMax[0] > 0) || (tMin[1] < 0 && tMax[1] > 0)) {
      tempPenalty += 14.0;
      isSlush = true;
    }
    if (tMax[0] < -15) {
      tempPenalty += 6.0;
    }

    var rawScore = 100.0 - precipPenalty - tempPenalty;
    var score = Math.max(5, Math.min(100, Math.round(rawScore)));

    var status = 'good';
    var verdict = 'Смело на мойку';
    var tagline = 'Погода стабильная, легкая пыль не помеха. Отличный момент сбить дорожный налет.';
    var image = '/assets/img/carwash/wash-good.webp';
    var badgeText = 'Благоприятно';
    var badgeColor = '#1565C0';
    var daysClean = '2–3 дня чистоты';
    var advice = 'Кузов быстро сохнет, риск осадков низкий. Экспресс или кузов + коврики окупятся с лихвой.';

    if (score >= 80) {
      status = 'perfect';
      verdict = 'Идеально! Мой на все деньги';
      tagline = 'Впереди сухие чистые дни. Машина будет сиять и радовать глаз.';
      image = '/assets/img/carwash/wash-perfect.webp';
      badgeText = 'Зеленый свет';
      badgeColor = '#2E7D32';
      daysClean = '4–6 дней чистоты';
      advice = 'Отличное время для комплексной мойки, воска или детейлинга — результат продержится долго!';
    } else if (score >= 60) {
      status = 'good';
      verdict = 'Смело на мойку';
      tagline = 'Погода стабильная, легкая пыль не помеха. Отличный момент сбить дорожный налет.';
      image = '/assets/img/carwash/wash-good.webp';
      badgeText = 'Благоприятно';
      badgeColor = '#1565C0';
      daysClean = '2–3 дня чистоты';
      advice = 'Кузов быстро сохнет, риск осадков низкий. Экспресс или кузов + коврики окупятся с лихвой.';
    } else if (score >= 35) {
      status = 'risky';
      verdict = 'Рискованно: спонсор чистых луж';
      tagline = 'Высокая влажность или скорый дождь/снег. Чистым авто пробудет считанные часы.';
      image = '/assets/img/carwash/wash-risky.webp';
      badgeText = '50 / 50';
      badgeColor = '#E65100';
      daysClean = 'Меньше 24 часов';
      advice = 'Если авто сильно загрязнено — сделайте быструю техническую сбивку грязи за 150 ₽. Дорогие полировки отложите.';
    } else {
      status = 'disaster';
      verdict = 'Остановись! Танки грязи не боятся';
      tagline = 'Ливни, снегопад или слякоть с реагентами. Деньги на ветер — лучше переждать непогоду.';
      image = '/assets/img/carwash/wash-disaster.webp';
      badgeText = 'Не рекомендуем';
      badgeColor = '#C62828';
      daysClean = 'До первой лужи (20 минут)';
      advice = 'Протрите только стекла, зеркала, оптику и номерные знаки для безопасности. Полноценную мойку отложите до ясных дней.';
    }

    var roadCondition = 'Сухой чистый асфальт';
    if (isSlush) {
      roadCondition = 'Слякоть и дорожные реагенты';
    } else if (s0 > 3.0 || p0 > 70) {
      roadCondition = 'Мокрый асфальт, лужи и взвесь';
    } else if (s0 > 0.5 || p0 > 40) {
      roadCondition = 'Влажное дорожное полотно';
    }

    var precipRisk = 'Минимальный';
    if (p0 >= 75) {
      precipRisk = 'Штормовой / Непрерывный';
    } else if (p0 >= 50 || s0 >= 2.0) {
      precipRisk = 'Высокий';
    } else if (p0 >= 20 || s0 >= 0.2) {
      precipRisk = 'Умеренный';
    }

    var weekdays = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'];
    var daysForecast = [];
    for (var i = 0; i < Math.min(5, times.length); i++) {
      var dStr = times[i];
      var parts = dStr.split('-');
      var dObj = new Date(parseInt(parts[0], 10), parseInt(parts[1], 10) - 1, parseInt(parts[2], 10));
      var dayName = i === 0 ? 'Сегодня' : (i === 1 ? 'Завтра' : weekdays[dObj.getDay()]);
      var dateLabel = ('0' + dObj.getDate()).slice(-2) + '.' + ('0' + (dObj.getMonth() + 1)).slice(-2);

      var code = codes[i] || 0;
      var descInfo = WMO_MAP[code] || ['Облачно', 'cloud'];
      var prob = probs[i] || 0;
      var pSum = sums[i] || 0;
      var tHi = Math.round(tMax[i] !== undefined ? tMax[i] : 0);
      var tLo = Math.round(tMin[i] !== undefined ? tMin[i] : 0);

      var dayRaw = 100.0 - (prob * 0.7) - Math.min(pSum * 10.0, 30.0);
      if (tLo < 0 && tHi > 0) dayRaw -= 15.0;
      var dayScore = Math.max(5, Math.min(100, Math.round(dayRaw)));

      daysForecast.push({
        date: dStr,
        date_label: dateLabel,
        day_name: dayName,
        temp_max: tHi,
        temp_min: tLo,
        precip_prob: prob,
        precip_sum: Math.round(pSum * 10) / 10,
        weather_code: code,
        weather_desc: descInfo[0],
        weather_icon: descInfo[1],
        day_score: dayScore
      });
    }

    return {
      city_slug: citySlug,
      city_name: cityName,
      score: score,
      status: status,
      verdict: verdict,
      tagline: tagline,
      image: image,
      badge_text: badgeText,
      badge_color: badgeColor,
      days_clean_estimate: daysClean,
      advice: advice,
      road_condition: roadCondition,
      precip_risk: precipRisk,
      current_temp: currTemp,
      temp_min: Math.round(tMin[0] !== undefined ? tMin[0] : currTemp),
      temp_max: Math.round(tMax[0] !== undefined ? tMax[0] : currTemp),
      precip_prob_today: p0,
      precip_sum_today: Math.round(s0 * 10) / 10,
      days: daysForecast
    };
  }

  function renderData(data) {
    currentData = data;
    if (scoreEl) scoreEl.textContent = data.score + '%';
    if (verdictEl) verdictEl.textContent = data.verdict;
    if (taglineEl) taglineEl.textContent = data.tagline;
    if (adviceEl) adviceEl.textContent = data.advice;
    if (roadEl) roadEl.textContent = data.road_condition;
    if (precipEl) precipEl.textContent = data.precip_prob_today + '% (' + data.precip_risk + ')';
    if (tempEl) {
      var minSign = data.temp_min > 0 ? '+' : '';
      var maxSign = data.temp_max > 0 ? '+' : '';
      tempEl.textContent = minSign + data.temp_min + '° … ' + maxSign + data.temp_max + '°C';
    }

    if (scoreBadge) {
      scoreBadge.style.borderColor = data.badge_color || 'var(--mt-accent)';
    }

    if (statusBadge) {
      statusBadge.textContent = data.badge_text || 'Прогноз';
      statusBadge.style.background = data.badge_color || '#2E7D32';
    }

    if (heroImg && data.image) {
      heroImg.src = data.image;
    }

    if (daysGrid && Array.isArray(data.days)) {
      daysGrid.innerHTML = '';
      data.days.forEach(function(day, idx) {
        var card = document.createElement('div');
        card.className = 'mt-weather-day-card' + (idx === 0 ? ' is-today' : '');

        var emoji = getWeatherEmoji(day.weather_icon);
        var tHi = (day.temp_max > 0 ? '+' : '') + day.temp_max + '°';
        var tLo = (day.temp_min > 0 ? '+' : '') + day.temp_min + '°';

        var badgeColor = '#C62828';
        var badgeText = 'Слякоть';
        if (day.day_score >= 80) {
          badgeColor = '#2E7D32';
          badgeText = 'Чисто';
        } else if (day.day_score >= 60) {
          badgeColor = '#1565C0';
          badgeText = 'Хорошо';
        } else if (day.day_score >= 35) {
          badgeColor = '#E65100';
          badgeText = 'Риск 50%';
        }

        card.innerHTML =
          '<div class="mt-weather-day-name">' + day.day_name + '</div>' +
          '<div class="mt-weather-day-date">' + day.date_label + '</div>' +
          '<div class="mt-weather-day-icon">' + emoji + '</div>' +
          '<div class="mt-weather-day-desc">' + day.weather_desc + '</div>' +
          '<div class="mt-weather-day-temps">' + tHi + '<span class="mt-temp-lo">' + tLo + '</span></div>' +
          '<div class="mt-weather-day-wash-badge" style="color:' + badgeColor + '; background:' + (badgeColor + '18') + '">' +
            day.day_score + '% · ' + badgeText +
          '</div>';

        daysGrid.appendChild(card);
      });
    }

    var pageUrl = 'https://molniya-tech.ru/tools/carwash-weather' + (data.city_slug !== 'custom' ? '?city=' + data.city_slug : '');
    var shareMsg = data.verdict + ' — Индекс чистоты кузова ' + data.score + '% в г. ' + data.city_name + '!\n' +
      data.tagline + '\n\n' +
      'Смотреть прогноз дорожной грязи: ' + pageUrl;

    if (shareTg) {
      shareTg.href = 'https://t.me/share/url?url=' + encodeURIComponent(pageUrl) + '&text=' + encodeURIComponent(data.verdict + ' — Индекс чистоты ' + data.score + '% (' + data.city_name + ')! ' + data.tagline);
    }
    if (shareWa) {
      shareWa.href = 'https://api.whatsapp.com/send?text=' + encodeURIComponent(shareMsg);
    }
    if (shareVk) {
      shareVk.href = 'https://vk.com/share.php?url=' + encodeURIComponent(pageUrl) + '&title=' + encodeURIComponent(data.verdict + ' — Индекс чистоты кузова');
    }
  }

  function fetchWeather(citySlug, lat, lon, customName) {
    var cInfo = CITY_COORDS[citySlug] || CITY_COORDS.msk;
    var targetLat = lat !== undefined && lat !== null ? lat : cInfo.lat;
    var targetLon = lon !== undefined && lon !== null ? lon : cInfo.lon;
    var targetName = customName || cInfo.name;
    var targetSlug = citySlug || 'custom';

    if (scoreEl) scoreEl.textContent = '…';

    var localUrl = '/api/weather?' + (targetSlug !== 'custom' ? 'city=' + encodeURIComponent(targetSlug) : 'lat=' + targetLat + '&lon=' + targetLon + '&name=' + encodeURIComponent(targetName));

    fetch(localUrl)
      .then(function(res) {
        if (!res.ok) throw new Error('API server status ' + res.status);
        return res.json();
      })
      .then(function(data) {
        if (data && data.score !== undefined) {
          renderData(data);
        } else {
          throw new Error('Invalid server data');
        }
      })
      .catch(function(localErr) {
        // Direct browser fallback to Open-Meteo API
        var directUrl = 'https://api.open-meteo.com/v1/forecast?latitude=' + targetLat +
          '&longitude=' + targetLon +
          '&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,windspeed_10m_max' +
          '&current_weather=true&timezone=auto';

        fetch(directUrl)
          .then(function(omRes) {
            if (!omRes.ok) throw new Error('Open-Meteo direct status ' + omRes.status);
            return omRes.json();
          })
          .then(function(omJson) {
            var clientData = computeClientWashIndex(omJson, targetName, targetSlug);
            renderData(clientData);
          })
          .catch(function(fallbackErr) {
            console.error('All weather fetches failed:', localErr, fallbackErr);
            if (scoreEl) scoreEl.textContent = '88%';
          });
      });
  }

  function selectCity(citySlug) {
    currentCity = citySlug;
    chips.forEach(function(btn) {
      if (btn.getAttribute('data-weather-city') === citySlug) {
        btn.classList.add('is-active');
      } else {
        btn.classList.remove('is-active');
      }
    });
    if (select) {
      select.value = citySlug;
    }
    if (window.history && window.history.replaceState) {
      var newUrl = window.location.pathname + (citySlug !== 'msk' ? '?city=' + citySlug : '');
      window.history.replaceState(null, '', newUrl);
    }
    fetchWeather(citySlug);
  }

  chips.forEach(function(btn) {
    btn.addEventListener('click', function() {
      var slug = btn.getAttribute('data-weather-city');
      if (slug) selectCity(slug);
    });
  });

  if (select) {
    select.addEventListener('change', function() {
      selectCity(select.value);
    });
  }

  if (geoBtn) {
    geoBtn.addEventListener('click', function() {
      if (!navigator.geolocation) {
        alert('Геолокация не поддерживается вашим браузером');
        return;
      }
      var origText = geoBtn.innerHTML;
      geoBtn.innerHTML = '<span>Определяем...</span>';
      geoBtn.disabled = true;

      navigator.geolocation.getCurrentPosition(
        function(pos) {
          geoBtn.innerHTML = origText;
          geoBtn.disabled = false;
          chips.forEach(function(b) { b.classList.remove('is-active'); });
          fetchWeather(null, pos.coords.latitude, pos.coords.longitude, 'Моя локация');
        },
        function(err) {
          geoBtn.innerHTML = origText;
          geoBtn.disabled = false;
          alert('Не удалось определить координаты. Выберите город из списка.');
        },
        { timeout: 8000 }
      );
    });
  }

  if (copyBtn) {
    copyBtn.addEventListener('click', function(e) {
      e.preventDefault();
      if (!currentData) return;

      var pageUrl = 'https://molniya-tech.ru/tools/carwash-weather' + (currentData.city_slug !== 'custom' ? '?city=' + currentData.city_slug : '');
      var copyText = [
        '🧼 ' + currentData.verdict + ' — Индекс чистоты кузова: ' + currentData.score + '%',
        '📍 Город: ' + currentData.city_name,
        '💡 ' + currentData.tagline,
        '🌡️ Температура: ' + (currentData.temp_min > 0 ? '+' : '') + currentData.temp_min + '° … ' + (currentData.temp_max > 0 ? '+' : '') + currentData.temp_max + '°C',
        '🛣️ Состояние дорог: ' + currentData.road_condition,
        '⏱️ Стойкость чистоты: ' + currentData.days_clean_estimate,
        '👉 Проверить свой город: ' + pageUrl
      ].join('\n');

      copyTextToClipboard(copyText).then(function() {
        if (!copyBtn.getAttribute('data-orig')) {
          copyBtn.setAttribute('data-orig', copyBtn.textContent.trim());
        }
        var orig = copyBtn.getAttribute('data-orig');
        copyBtn.textContent = '✅ Карточка скопирована!';
        copyBtn.classList.add('copied');

        clearTimeout(copyBtn._copyTimeout);
        copyBtn._copyTimeout = setTimeout(function() {
          copyBtn.textContent = orig;
          copyBtn.classList.remove('copied');
        }, 2000);
      }).catch(function(err) {
        console.error('Failed to copy card: ', err);
      });
    });
  }

  selectCity(currentCity);
}


// ==========================================
// Standalone QR Code Engine (MIT Kazuhiko Arase)
// ==========================================
var qrcode=function(){var t=function(t,r){var e=t,n=g[r],o=null,i=0,a=null,u=[],f={},c=function(t,r){o=function(t){for(var r=new Array(t),e=0;e<t;e+=1){r[e]=new Array(t);for(var n=0;n<t;n+=1)r[e][n]=null}return r}(i=4*e+17),l(0,0),l(i-7,0),l(0,i-7),s(),h(),d(t,r),e>=7&&v(t),null==a&&(a=p(e,n,u)),w(a,r)},l=function(t,r){for(var e=-1;e<=7;e+=1)if(!(t+e<=-1||i<=t+e))for(var n=-1;n<=7;n+=1)r+n<=-1||i<=r+n||(o[t+e][r+n]=0<=e&&e<=6&&(0==n||6==n)||0<=n&&n<=6&&(0==e||6==e)||2<=e&&e<=4&&2<=n&&n<=4)},h=function(){for(var t=8;t<i-8;t+=1)null==o[t][6]&&(o[t][6]=t%2==0);for(var r=8;r<i-8;r+=1)null==o[6][r]&&(o[6][r]=r%2==0)},s=function(){for(var t=B.getPatternPosition(e),r=0;r<t.length;r+=1)for(var n=0;n<t.length;n+=1){var i=t[r],a=t[n];if(null==o[i][a])for(var u=-2;u<=2;u+=1)for(var f=-2;f<=2;f+=1)o[i+u][a+f]=-2==u||2==u||-2==f||2==f||0==u&&0==f}},v=function(t){for(var r=B.getBCHTypeNumber(e),n=0;n<18;n+=1){var a=!t&&1==(r>>n&1);o[Math.floor(n/3)][n%3+i-8-3]=a}for(n=0;n<18;n+=1){a=!t&&1==(r>>n&1);o[n%3+i-8-3][Math.floor(n/3)]=a}},d=function(t,r){for(var e=n<<3|r,a=B.getBCHTypeInfo(e),u=0;u<15;u+=1){var f=!t&&1==(a>>u&1);u<6?o[u][8]=f:u<8?o[u+1][8]=f:o[i-15+u][8]=f}for(u=0;u<15;u+=1){f=!t&&1==(a>>u&1);u<8?o[8][i-u-1]=f:u<9?o[8][15-u-1+1]=f:o[8][15-u-1]=f}o[i-8][8]=!t},w=function(t,r){for(var e=-1,n=i-1,a=7,u=0,f=B.getMaskFunction(r),c=i-1;c>0;c-=2)for(6==c&&(c-=1);;){for(var g=0;g<2;g+=1)if(null==o[n][c-g]){var l=!1;u<t.length&&(l=1==(t[u]>>>a&1)),f(n,c-g)&&(l=!l),o[n][c-g]=l,-1==(a-=1)&&(u+=1,a=7)}if((n+=e)<0||i<=n){n-=e,e=-e;break}}},p=function(t,r,e){for(var n=A.getRSBlocks(t,r),o=b(),i=0;i<e.length;i+=1){var a=e[i];o.put(a.getMode(),4),o.put(a.getLength(),B.getLengthInBits(a.getMode(),t)),a.write(o)}var u=0;for(i=0;i<n.length;i+=1)u+=n[i].dataCount;if(o.getLengthInBits()>8*u)throw"code length overflow. ("+o.getLengthInBits()+">"+8*u+")";for(o.getLengthInBits()+4<=8*u&&o.put(0,4);o.getLengthInBits()%8!=0;)o.putBit(!1);for(;!(o.getLengthInBits()>=8*u||(o.put(236,8),o.getLengthInBits()>=8*u));)o.put(17,8);return function(t,r){for(var e=0,n=0,o=0,i=new Array(r.length),a=new Array(r.length),u=0;u<r.length;u+=1){var f=r[u].dataCount,c=r[u].totalCount-f;n=Math.max(n,f),o=Math.max(o,c),i[u]=new Array(f);for(var g=0;g<i[u].length;g+=1)i[u][g]=255&t.getBuffer()[g+e];e+=f;var l=B.getErrorCorrectPolynomial(c),h=k(i[u],l.getLength()-1).mod(l);for(a[u]=new Array(l.getLength()-1),g=0;g<a[u].length;g+=1){var s=g+h.getLength()-a[u].length;a[u][g]=s>=0?h.getAt(s):0}}var v=0;for(g=0;g<r.length;g+=1)v+=r[g].totalCount;var d=new Array(v),w=0;for(g=0;g<n;g+=1)for(u=0;u<r.length;u+=1)g<i[u].length&&(d[w]=i[u][g],w+=1);for(g=0;g<o;g+=1)for(u=0;u<r.length;u+=1)g<a[u].length&&(d[w]=a[u][g],w+=1);return d}(o,n)};f.addData=function(t,r){var e=null;switch(r=r||"Byte"){case"Numeric":e=M(t);break;case"Alphanumeric":e=x(t);break;case"Byte":e=m(t);break;case"Kanji":e=L(t);break;default:throw"mode:"+r}u.push(e),a=null},f.isDark=function(t,r){if(t<0||i<=t||r<0||i<=r)throw t+","+r;return o[t][r]},f.getModuleCount=function(){return i},f.make=function(){if(e<1){for(var t=1;t<40;t++){for(var r=A.getRSBlocks(t,n),o=b(),i=0;i<u.length;i++){var a=u[i];o.put(a.getMode(),4),o.put(a.getLength(),B.getLengthInBits(a.getMode(),t)),a.write(o)}var g=0;for(i=0;i<r.length;i++)g+=r[i].dataCount;if(o.getLengthInBits()<=8*g)break}e=t}c(!1,function(){for(var t=0,r=0,e=0;e<8;e+=1){c(!0,e);var n=B.getLostPoint(f);(0==e||t>n)&&(t=n,r=e)}return r}())},f.createTableTag=function(t,r){t=t||2;var e="";e+='<table style="',e+=" border-width: 0px; border-style: none;",e+=" border-collapse: collapse;",e+=" padding: 0px; margin: "+(r=void 0===r?4*t:r)+"px;",e+='">',e+="<tbody>";for(var n=0;n<f.getModuleCount();n+=1){e+="<tr>";for(var o=0;o<f.getModuleCount();o+=1)e+='<td style="',e+=" border-width: 0px; border-style: none;",e+=" border-collapse: collapse;",e+=" padding: 0px; margin: 0px;",e+=" width: "+t+"px;",e+=" height: "+t+"px;",e+=" background-color: ",e+=f.isDark(n,o)?"#000000":"#ffffff",e+=";",e+='"/>';e+="</tr>"}return e+="</tbody>",e+="</table>"},f.createSvgTag=function(t,r,e,n){var o={};"object"==typeof arguments[0]&&(t=(o=arguments[0]).cellSize,r=o.margin,e=o.alt,n=o.title),t=t||2,r=void 0===r?4*t:r,(e="string"==typeof e?{text:e}:e||{}).text=e.text||null,e.id=e.text?e.id||"qrcode-description":null,(n="string"==typeof n?{text:n}:n||{}).text=n.text||null,n.id=n.text?n.id||"qrcode-title":null;var i,a,u,c,g=f.getModuleCount()*t+2*r,l="";for(c="l"+t+",0 0,"+t+" -"+t+",0 0,-"+t+"z ",l+='<svg version="1.1" xmlns="http://www.w3.org/2000/svg"',l+=o.scalable?"":' width="'+g+'px" height="'+g+'px"',l+=' viewBox="0 0 '+g+" "+g+'" ',l+=' preserveAspectRatio="xMinYMin meet"',l+=n.text||e.text?' role="img" aria-labelledby="'+y([n.id,e.id].join(" ").trim())+'"':"",l+=">",l+=n.text?'<title id="'+y(n.id)+'">'+y(n.text)+"</title>":"",l+=e.text?'<description id="'+y(e.id)+'">'+y(e.text)+"</description>":"",l+='<rect width="100%" height="100%" fill="white" cx="0" cy="0"/>',l+='<path d="',a=0;a<f.getModuleCount();a+=1)for(u=a*t+r,i=0;i<f.getModuleCount();i+=1)f.isDark(a,i)&&(l+="M"+(i*t+r)+","+u+c);return l+='" stroke="transparent" fill="black"/>',l+="</svg>"},f.createDataURL=function(t,r){t=t||2,r=void 0===r?4*t:r;var e=f.getModuleCount()*t+2*r,n=r,o=e-r;return T(e,e,function(r,e){if(n<=r&&r<o&&n<=e&&e<o){var i=Math.floor((r-n)/t),a=Math.floor((e-n)/t);return f.isDark(a,i)?0:1}return 1})},f.createImgTag=function(t,r,e){t=t||2,r=void 0===r?4*t:r;var n=f.getModuleCount()*t+2*r,o="";return o+="<img",o+=' src="',o+=f.createDataURL(t,r),o+='"',o+=' width="',o+=n,o+='"',o+=' height="',o+=n,o+='"',e&&(o+=' alt="',o+=y(e),o+='"'),o+="/>"};var y=function(t){for(var r="",e=0;e<t.length;e+=1){var n=t.charAt(e);switch(n){case"<":r+="&lt;";break;case">":r+="&gt;";break;case"&":r+="&amp;";break;case'"':r+="&quot;";break;default:r+=n}}return r};return f.createASCII=function(t,r){if((t=t||1)<2)return function(t){t=void 0===t?2:t;var r,e,n,o,i,a=1*f.getModuleCount()+2*t,u=t,c=a-t,g={"██":"█","█ ":"▀"," █":"▄","  ":" "},l={"██":"▀","█ ":"▀"," █":" ","  ":" "},h="";for(r=0;r<a;r+=2){for(n=Math.floor((r-u)/1),o=Math.floor((r+1-u)/1),e=0;e<a;e+=1)i="█",u<=e&&e<c&&u<=r&&r<c&&f.isDark(n,Math.floor((e-u)/1))&&(i=" "),u<=e&&e<c&&u<=r+1&&r+1<c&&f.isDark(o,Math.floor((e-u)/1))?i+=" ":i+="█",h+=t<1&&r+1>=c?l[i]:g[i];h+="\n"}return a%2&&t>0?h.substring(0,h.length-a-1)+Array(a+1).join("▀"):h.substring(0,h.length-1)}(r);t-=1,r=void 0===r?2*t:r;var e,n,o,i,a=f.getModuleCount()*t+2*r,u=r,c=a-r,g=Array(t+1).join("██"),l=Array(t+1).join("  "),h="",s="";for(e=0;e<a;e+=1){for(o=Math.floor((e-u)/t),s="",n=0;n<a;n+=1)i=1,u<=n&&n<c&&u<=e&&e<c&&f.isDark(o,Math.floor((n-u)/t))&&(i=0),s+=i?g:l;for(o=0;o<t;o+=1)h+=s+"\n"}return h.substring(0,h.length-1)},f.renderTo2dContext=function(t,r){r=r||2;for(var e=f.getModuleCount(),n=0;n<e;n++)for(var o=0;o<e;o++)t.fillStyle=f.isDark(n,o)?"black":"white",t.fillRect(o*r,n*r,r,r)},f};t.stringToBytes=(t.stringToBytesFuncs={default:function(t){for(var r=[],e=0;e<t.length;e+=1){var n=t.charCodeAt(e);r.push(255&n)}return r}}).default,t.createStringToBytes=function(t,r){var e=function(){for(var e=S(t),n=function(){var t=e.read();if(-1==t)throw"eof";return t},o=0,i={};;){var a=e.read();if(-1==a)break;var u=n(),f=n()<<8|n();i[String.fromCharCode(a<<8|u)]=f,o+=1}if(o!=r)throw o+" != "+r;return i}(),n="?".charCodeAt(0);return function(t){for(var r=[],o=0;o<t.length;o+=1){var i=t.charCodeAt(o);if(i<128)r.push(i);else{var a=e[t.charAt(o)];"number"==typeof a?(255&a)==a?r.push(a):(r.push(a>>>8),r.push(255&a)):r.push(n)}}return r}};var r,e,n,o,i,a=1,u=2,f=4,c=8,g={L:1,M:0,Q:3,H:2},l=0,h=1,s=2,v=3,d=4,w=5,p=6,y=7,B=(r=[[],[6,18],[6,22],[6,26],[6,30],[6,34],[6,22,38],[6,24,42],[6,26,46],[6,28,50],[6,30,54],[6,32,58],[6,34,62],[6,26,46,66],[6,26,48,70],[6,26,50,74],[6,30,54,78],[6,30,56,82],[6,30,58,86],[6,34,62,90],[6,28,50,72,94],[6,26,50,74,98],[6,30,54,78,102],[6,28,54,80,106],[6,32,58,84,110],[6,30,58,86,114],[6,34,62,90,118],[6,26,50,74,98,122],[6,30,54,78,102,126],[6,26,52,78,104,130],[6,30,56,82,108,134],[6,34,60,86,112,138],[6,30,58,86,114,142],[6,34,62,90,118,146],[6,30,54,78,102,126,150],[6,24,50,76,102,128,154],[6,28,54,80,106,132,158],[6,32,58,84,110,136,162],[6,26,54,82,110,138,166],[6,30,58,86,114,142,170]],e=1335,n=7973,i=function(t){for(var r=0;0!=t;)r+=1,t>>>=1;return r},(o={}).getBCHTypeInfo=function(t){for(var r=t<<10;i(r)-i(e)>=0;)r^=e<<i(r)-i(e);return 21522^(t<<10|r)},o.getBCHTypeNumber=function(t){for(var r=t<<12;i(r)-i(n)>=0;)r^=n<<i(r)-i(n);return t<<12|r},o.getPatternPosition=function(t){return r[t-1]},o.getMaskFunction=function(t){switch(t){case l:return function(t,r){return(t+r)%2==0};case h:return function(t,r){return t%2==0};case s:return function(t,r){return r%3==0};case v:return function(t,r){return(t+r)%3==0};case d:return function(t,r){return(Math.floor(t/2)+Math.floor(r/3))%2==0};case w:return function(t,r){return t*r%2+t*r%3==0};case p:return function(t,r){return(t*r%2+t*r%3)%2==0};case y:return function(t,r){return(t*r%3+(t+r)%2)%2==0};default:throw"bad maskPattern:"+t}},o.getErrorCorrectPolynomial=function(t){for(var r=k([1],0),e=0;e<t;e+=1)r=r.multiply(k([1,C.gexp(e)],0));return r},o.getLengthInBits=function(t,r){if(1<=r&&r<10)switch(t){case a:return 10;case u:return 9;case f:case c:return 8;default:throw"mode:"+t}else if(r<27)switch(t){case a:return 12;case u:return 11;case f:return 16;case c:return 10;default:throw"mode:"+t}else{if(!(r<41))throw"type:"+r;switch(t){case a:return 14;case u:return 13;case f:return 16;case c:return 12;default:throw"mode:"+t}}},o.getLostPoint=function(t){for(var r=t.getModuleCount(),e=0,n=0;n<r;n+=1)for(var o=0;o<r;o+=1){for(var i=0,a=t.isDark(n,o),u=-1;u<=1;u+=1)if(!(n+u<0||r<=n+u))for(var f=-1;f<=1;f+=1)o+f<0||r<=o+f||0==u&&0==f||a==t.isDark(n+u,o+f)&&(i+=1);i>5&&(e+=3+i-5)}for(n=0;n<r-1;n+=1)for(o=0;o<r-1;o+=1){var c=0;t.isDark(n,o)&&(c+=1),t.isDark(n+1,o)&&(c+=1),t.isDark(n,o+1)&&(c+=1),t.isDark(n+1,o+1)&&(c+=1),0!=c&&4!=c||(e+=3)}for(n=0;n<r;n+=1)for(o=0;o<r-6;o+=1)t.isDark(n,o)&&!t.isDark(n,o+1)&&t.isDark(n,o+2)&&t.isDark(n,o+3)&&t.isDark(n,o+4)&&!t.isDark(n,o+5)&&t.isDark(n,o+6)&&(e+=40);for(o=0;o<r;o+=1)for(n=0;n<r-6;n+=1)t.isDark(n,o)&&!t.isDark(n+1,o)&&t.isDark(n+2,o)&&t.isDark(n+3,o)&&t.isDark(n+4,o)&&!t.isDark(n+5,o)&&t.isDark(n+6,o)&&(e+=40);var g=0;for(o=0;o<r;o+=1)for(n=0;n<r;n+=1)t.isDark(n,o)&&(g+=1);return e+=Math.abs(100*g/r/r-50)/5*10},o),C=function(){for(var t=new Array(256),r=new Array(256),e=0;e<8;e+=1)t[e]=1<<e;for(e=8;e<256;e+=1)t[e]=t[e-4]^t[e-5]^t[e-6]^t[e-8];for(e=0;e<255;e+=1)r[t[e]]=e;var n={glog:function(t){if(t<1)throw"glog("+t+")";return r[t]},gexp:function(r){for(;r<0;)r+=255;for(;r>=256;)r-=255;return t[r]}};return n}();function k(t,r){if(void 0===t.length)throw t.length+"/"+r;var e=function(){for(var e=0;e<t.length&&0==t[e];)e+=1;for(var n=new Array(t.length-e+r),o=0;o<t.length-e;o+=1)n[o]=t[o+e];return n}(),n={getAt:function(t){return e[t]},getLength:function(){return e.length},multiply:function(t){for(var r=new Array(n.getLength()+t.getLength()-1),e=0;e<n.getLength();e+=1)for(var o=0;o<t.getLength();o+=1)r[e+o]^=C.gexp(C.glog(n.getAt(e))+C.glog(t.getAt(o)));return k(r,0)},mod:function(t){if(n.getLength()-t.getLength()<0)return n;for(var r=C.glog(n.getAt(0))-C.glog(t.getAt(0)),e=new Array(n.getLength()),o=0;o<n.getLength();o+=1)e[o]=n.getAt(o);for(o=0;o<t.getLength();o+=1)e[o]^=C.gexp(C.glog(t.getAt(o))+r);return k(e,0).mod(t)}};return n}var A=function(){var t=[[1,26,19],[1,26,16],[1,26,13],[1,26,9],[1,44,34],[1,44,28],[1,44,22],[1,44,16],[1,70,55],[1,70,44],[2,35,17],[2,35,13],[1,100,80],[2,50,32],[2,50,24],[4,25,9],[1,134,108],[2,67,43],[2,33,15,2,34,16],[2,33,11,2,34,12],[2,86,68],[4,43,27],[4,43,19],[4,43,15],[2,98,78],[4,49,31],[2,32,14,4,33,15],[4,39,13,1,40,14],[2,121,97],[2,60,38,2,61,39],[4,40,18,2,41,19],[4,40,14,2,41,15],[2,146,116],[3,58,36,2,59,37],[4,36,16,4,37,17],[4,36,12,4,37,13],[2,86,68,2,87,69],[4,69,43,1,70,44],[6,43,19,2,44,20],[6,43,15,2,44,16],[4,101,81],[1,80,50,4,81,51],[4,50,22,4,51,23],[3,36,12,8,37,13],[2,116,92,2,117,93],[6,58,36,2,59,37],[4,46,20,6,47,21],[7,42,14,4,43,15],[4,133,107],[8,59,37,1,60,38],[8,44,20,4,45,21],[12,33,11,4,34,12],[3,145,115,1,146,116],[4,64,40,5,65,41],[11,36,16,5,37,17],[11,36,12,5,37,13],[5,109,87,1,110,88],[5,65,41,5,66,42],[5,54,24,7,55,25],[11,36,12,7,37,13],[5,122,98,1,123,99],[7,73,45,3,74,46],[15,43,19,2,44,20],[3,45,15,13,46,16],[1,135,107,5,136,108],[10,74,46,1,75,47],[1,50,22,15,51,23],[2,42,14,17,43,15],[5,150,120,1,151,121],[9,69,43,4,70,44],[17,50,22,1,51,23],[2,42,14,19,43,15],[3,141,113,4,142,114],[3,70,44,11,71,45],[17,47,21,4,48,22],[9,39,13,16,40,14],[3,135,107,5,136,108],[3,67,41,13,68,42],[15,54,24,5,55,25],[15,43,15,10,44,16],[4,144,116,4,145,117],[17,68,42],[17,50,22,6,51,23],[19,46,16,6,47,17],[2,139,111,7,140,112],[17,74,46],[7,54,24,16,55,25],[34,37,13],[4,151,121,5,152,122],[4,75,47,14,76,48],[11,54,24,14,55,25],[16,45,15,14,46,16],[6,147,117,4,148,118],[6,73,45,14,74,46],[11,54,24,16,55,25],[30,46,16,2,47,17],[8,132,106,4,133,107],[8,75,47,13,76,48],[7,54,24,22,55,25],[22,45,15,13,46,16],[10,142,114,2,143,115],[19,74,46,4,75,47],[28,50,22,6,51,23],[33,46,16,4,47,17],[8,152,122,4,153,123],[22,73,45,3,74,46],[8,53,23,26,54,24],[12,45,15,28,46,16],[3,147,117,10,148,118],[3,73,45,23,74,46],[4,54,24,31,55,25],[11,45,15,31,46,16],[7,146,116,7,147,117],[21,73,45,7,74,46],[1,53,23,37,54,24],[19,45,15,26,46,16],[5,145,115,10,146,116],[19,75,47,10,76,48],[15,54,24,25,55,25],[23,45,15,25,46,16],[13,145,115,3,146,116],[2,74,46,29,75,47],[42,54,24,1,55,25],[23,45,15,28,46,16],[17,145,115],[10,74,46,23,75,47],[10,54,24,35,55,25],[19,45,15,35,46,16],[17,145,115,1,146,116],[14,74,46,21,75,47],[29,54,24,19,55,25],[11,45,15,46,46,16],[13,145,115,6,146,116],[14,74,46,23,75,47],[44,54,24,7,55,25],[59,46,16,1,47,17],[12,151,121,7,152,122],[12,75,47,26,76,48],[39,54,24,14,55,25],[22,45,15,41,46,16],[6,151,121,14,152,122],[6,75,47,34,76,48],[46,54,24,10,55,25],[2,45,15,64,46,16],[17,152,122,4,153,123],[29,74,46,14,75,47],[49,54,24,10,55,25],[24,45,15,46,46,16],[4,152,122,18,153,123],[13,74,46,32,75,47],[48,54,24,14,55,25],[42,45,15,32,46,16],[20,147,117,4,148,118],[40,75,47,7,76,48],[43,54,24,22,55,25],[10,45,15,67,46,16],[19,148,118,6,149,119],[18,75,47,31,76,48],[34,54,24,34,55,25],[20,45,15,61,46,16]],r=function(t,r){var e={};return e.totalCount=t,e.dataCount=r,e},e={};return e.getRSBlocks=function(e,n){var o=function(r,e){switch(e){case g.L:return t[4*(r-1)+0];case g.M:return t[4*(r-1)+1];case g.Q:return t[4*(r-1)+2];case g.H:return t[4*(r-1)+3];default:return}}(e,n);if(void 0===o)throw"bad rs block @ typeNumber:"+e+"/errorCorrectionLevel:"+n;for(var i=o.length/3,a=[],u=0;u<i;u+=1)for(var f=o[3*u+0],c=o[3*u+1],l=o[3*u+2],h=0;h<f;h+=1)a.push(r(c,l));return a},e}(),b=function(){var t=[],r=0,e={getBuffer:function(){return t},getAt:function(r){var e=Math.floor(r/8);return 1==(t[e]>>>7-r%8&1)},put:function(t,r){for(var n=0;n<r;n+=1)e.putBit(1==(t>>>r-n-1&1))},getLengthInBits:function(){return r},putBit:function(e){var n=Math.floor(r/8);t.length<=n&&t.push(0),e&&(t[n]|=128>>>r%8),r+=1}};return e},M=function(t){var r=a,e=t,n={getMode:function(){return r},getLength:function(t){return e.length},write:function(t){for(var r=e,n=0;n+2<r.length;)t.put(o(r.substring(n,n+3)),10),n+=3;n<r.length&&(r.length-n==1?t.put(o(r.substring(n,n+1)),4):r.length-n==2&&t.put(o(r.substring(n,n+2)),7))}},o=function(t){for(var r=0,e=0;e<t.length;e+=1)r=10*r+i(t.charAt(e));return r},i=function(t){if("0"<=t&&t<="9")return t.charCodeAt(0)-"0".charCodeAt(0);throw"illegal char :"+t};return n},x=function(t){var r=u,e=t,n={getMode:function(){return r},getLength:function(t){return e.length},write:function(t){for(var r=e,n=0;n+1<r.length;)t.put(45*o(r.charAt(n))+o(r.charAt(n+1)),11),n+=2;n<r.length&&t.put(o(r.charAt(n)),6)}},o=function(t){if("0"<=t&&t<="9")return t.charCodeAt(0)-"0".charCodeAt(0);if("A"<=t&&t<="Z")return t.charCodeAt(0)-"A".charCodeAt(0)+10;switch(t){case" ":return 36;case"$":return 37;case"%":return 38;case"*":return 39;case"+":return 40;case"-":return 41;case".":return 42;case"/":return 43;case":":return 44;default:throw"illegal char :"+t}};return n},m=function(r){var e=f,n=t.stringToBytes(r),o={getMode:function(){return e},getLength:function(t){return n.length},write:function(t){for(var r=0;r<n.length;r+=1)t.put(n[r],8)}};return o},L=function(r){var e=c,n=t.stringToBytesFuncs.SJIS;if(!n)throw"sjis not supported.";!function(){var t=n("友");if(2!=t.length||38726!=(t[0]<<8|t[1]))throw"sjis not supported."}();var o=n(r),i={getMode:function(){return e},getLength:function(t){return~~(o.length/2)},write:function(t){for(var r=o,e=0;e+1<r.length;){var n=(255&r[e])<<8|255&r[e+1];if(33088<=n&&n<=40956)n-=33088;else{if(!(57408<=n&&n<=60351))throw"illegal char at "+(e+1)+"/"+n;n-=49472}n=192*(n>>>8&255)+(255&n),t.put(n,13),e+=2}if(e<r.length)throw"illegal char at "+(e+1)}};return i},D=function(){var t=[],r={writeByte:function(r){t.push(255&r)},writeShort:function(t){r.writeByte(t),r.writeByte(t>>>8)},writeBytes:function(t,e,n){e=e||0,n=n||t.length;for(var o=0;o<n;o+=1)r.writeByte(t[o+e])},writeString:function(t){for(var e=0;e<t.length;e+=1)r.writeByte(t.charCodeAt(e))},toByteArray:function(){return t},toString:function(){var r="";r+="[";for(var e=0;e<t.length;e+=1)e>0&&(r+=","),r+=t[e];return r+="]"}};return r},S=function(t){var r=t,e=0,n=0,o=0,i={read:function(){for(;o<8;){if(e>=r.length){if(0==o)return-1;throw"unexpected end of file./"+o}var t=r.charAt(e);if(e+=1,"="==t)return o=0,-1;t.match(/^\s$/)||(n=n<<6|a(t.charCodeAt(0)),o+=6)}var i=n>>>o-8&255;return o-=8,i}},a=function(t){if(65<=t&&t<=90)return t-65;if(97<=t&&t<=122)return t-97+26;if(48<=t&&t<=57)return t-48+52;if(43==t)return 62;if(47==t)return 63;throw"c:"+t};return i},T=function(t,r,e){for(var n=function(t,r){var e=t,n=r,o=new Array(t*r),i={setPixel:function(t,r,n){o[r*e+t]=n},write:function(t){t.writeString("GIF87a"),t.writeShort(e),t.writeShort(n),t.writeByte(128),t.writeByte(0),t.writeByte(0),t.writeByte(0),t.writeByte(0),t.writeByte(0),t.writeByte(255),t.writeByte(255),t.writeByte(255),t.writeString(","),t.writeShort(0),t.writeShort(0),t.writeShort(e),t.writeShort(n),t.writeByte(0);var r=a(2);t.writeByte(2);for(var o=0;r.length-o>255;)t.writeByte(255),t.writeBytes(r,o,255),o+=255;t.writeByte(r.length-o),t.writeBytes(r,o,r.length-o),t.writeByte(0),t.writeString(";")}},a=function(t){for(var r=1<<t,e=1+(1<<t),n=t+1,i=u(),a=0;a<r;a+=1)i.add(String.fromCharCode(a));i.add(String.fromCharCode(r)),i.add(String.fromCharCode(e));var f,c,g,l=D(),h=(f=l,c=0,g=0,{write:function(t,r){if(t>>>r!=0)throw"length over";for(;c+r>=8;)f.writeByte(255&(t<<c|g)),r-=8-c,t>>>=8-c,g=0,c=0;g|=t<<c,c+=r},flush:function(){c>0&&f.writeByte(g)}});h.write(r,n);var s=0,v=String.fromCharCode(o[s]);for(s+=1;s<o.length;){var d=String.fromCharCode(o[s]);s+=1,i.contains(v+d)?v+=d:(h.write(i.indexOf(v),n),i.size()<4095&&(i.size()==1<<n&&(n+=1),i.add(v+d)),v=d)}return h.write(i.indexOf(v),n),h.write(e,n),h.flush(),l.toByteArray()},u=function(){var t={},r=0,e={add:function(n){if(e.contains(n))throw"dup key:"+n;t[n]=r,r+=1},size:function(){return r},indexOf:function(r){return t[r]},contains:function(r){return void 0!==t[r]}};return e};return i}(t,r),o=0;o<r;o+=1)for(var i=0;i<t;i+=1)n.setPixel(i,o,e(i,o));var a=D();n.write(a);for(var u=function(){var t=0,r=0,e=0,n="",o={},i=function(t){n+=String.fromCharCode(a(63&t))},a=function(t){if(t<0);else{if(t<26)return 65+t;if(t<52)return t-26+97;if(t<62)return t-52+48;if(62==t)return 43;if(63==t)return 47}throw"n:"+t};return o.writeByte=function(n){for(t=t<<8|255&n,r+=8,e+=1;r>=6;)i(t>>>r-6),r-=6},o.flush=function(){if(r>0&&(i(t<<6-r),t=0,r=0),e%3!=0)for(var o=3-e%3,a=0;a<o;a+=1)n+="="},o.toString=function(){return n},o}(),f=a.toByteArray(),c=0;c<f.length;c+=1)u.writeByte(f[c]);return u.flush(),"data:image/gif;base64,"+u};return t}();qrcode.stringToBytesFuncs["UTF-8"]=function(t){return function(t){for(var r=[],e=0;e<t.length;e++){var n=t.charCodeAt(e);n<128?r.push(n):n<2048?r.push(192|n>>6,128|63&n):n<55296||n>=57344?r.push(224|n>>12,128|n>>6&63,128|63&n):(e++,n=65536+((1023&n)<<10|1023&t.charCodeAt(e)),r.push(240|n>>18,128|n>>12&63,128|n>>6&63,128|63&n))}return r}(t)},function(t){"function"==typeof define&&define.amd?define([],t):"object"==typeof exports&&(module.exports=t())}(function(){return qrcode}),function(t){t.stringToBytes=t.stringToBytesFuncs["UTF-8"]}(qrcode);

// ==========================================
// Brand QR Code Generator Tool (/qr)
// ==========================================
function initQrGenerator() {
  var wrap = document.getElementById('qr-generator');
  if (!wrap) return;

  var canvas = document.getElementById('mt-qr-canvas');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');

  var currentType = 'url';
  var currentColor = '#C6543B';
  var currentLogo = 'molniya';
  var currentFrame = 'scan';
  var customFrameText = '';
  var customLogoImg = null;
  var customLogoDataUrl = null;

  var tabs = wrap.querySelectorAll('.mt-qr-tab-btn');
  var panels = wrap.querySelectorAll('.mt-qr-panel');
  var swatches = wrap.querySelectorAll('.mt-qr-swatch');
  var colorCustom = document.getElementById('mt-qr-color-custom');
  var logoBtns = wrap.querySelectorAll('.mt-qr-logo-btn[data-qr-logo]');
  var logoFileInput = document.getElementById('mt-qr-logo-file');
  var logoCustomBtn = document.getElementById('mt-qr-logo-custom-btn');
  var frameBtns = wrap.querySelectorAll('.mt-qr-logo-btn[data-qr-frame]');
  var frameCustomWrap = document.getElementById('mt-qr-frame-custom-wrap');
  var frameCustomInput = document.getElementById('mt-qr-frame-custom');

  var downloadPngBtn = document.getElementById('mt-qr-download-png');
  var downloadSvgBtn = document.getElementById('mt-qr-download-svg');
  var printBtn = document.getElementById('mt-qr-print-btn');
  var copyBtn = document.getElementById('mt-qr-copy-btn');

  function drawRoundRect(c, x, y, w, h, r, fill, stroke) {
    if (w < 2 * r) r = w / 2;
    if (h < 2 * r) r = h / 2;
    if (c.roundRect) {
      c.beginPath();
      c.roundRect(x, y, w, h, r);
      if (fill) c.fill();
      if (stroke) c.stroke();
      return;
    }
    c.beginPath();
    c.moveTo(x + r, y);
    c.lineTo(x + w - r, y);
    c.quadraticCurveTo(x + w, y, x + w, y + r);
    c.lineTo(x + w, y + h - r);
    c.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    c.lineTo(x + r, y + h);
    c.quadraticCurveTo(x, y + h, x, y + h - r);
    c.lineTo(x, y + r);
    c.quadraticCurveTo(x, y, x + r, y);
    c.closePath();
    if (fill) c.fill();
    if (stroke) c.stroke();
  }

  function drawMolniyaMark(c, cx, cy, size) {
    c.save();
    c.translate(cx, cy);
    var scale = size / 96;
    c.scale(scale, scale);

    c.beginPath();
    c.arc(0, 0, 11, 0, Math.PI * 2);
    c.lineWidth = 8;
    c.strokeStyle = '#131B2C';
    c.stroke();

    for (var i = 0; i < 6; i++) {
      var angle = (i * 60) * Math.PI / 180;
      c.save();
      c.rotate(angle);
      c.fillStyle = (i === 1) ? '#DF5F3C' : '#131B2C';
      drawRoundRect(c, -6.5, -42, 13, 22, 6.5, true, false);
      c.restore();
    }
    c.restore();
  }

  // Official logos requested by user
  var sbpImg = new Image();
  sbpImg.src = '/assets/img/qr/sbp-mark.png';
  sbpImg.onload = function() {
    if (currentLogo === 'sbp') renderQr();
  };

  var tgImg = new Image();
  tgImg.src = '/assets/img/qr/telegram-logo.svg';
  tgImg.onload = function() {
    if (currentLogo === 'tg') renderQr();
  };

  function drawSbpLogo(c, cx, cy, size) {
    if (sbpImg.complete && sbpImg.naturalWidth > 0) {
      c.drawImage(sbpImg, cx - size / 2, cy - size / 2, size, size);
      return;
    }
  }

  function drawTelegramLogo(c, cx, cy, size) {
    if (tgImg.complete && tgImg.naturalWidth > 0) {
      c.drawImage(tgImg, cx - size / 2, cy - size / 2, size, size);
      return;
    }
    c.save();
    c.translate(cx, cy);
    var scale = size / 240.1;
    c.scale(scale, scale);
    c.translate(-120.05, -120.05);

    var grad = c.createLinearGradient(0, 0, 0, 240.1);
    grad.addColorStop(0, '#2AABEE');
    grad.addColorStop(1, '#229ED9');
    c.fillStyle = grad;
    c.beginPath();
    c.arc(120.05, 120.05, 120.05, 0, Math.PI * 2);
    c.fill();

    var p = new Path2D('M54.3,118.8c35-15.2,58.3-25.3,70-30.2 c33.3-13.9,40.3-16.3,44.8-16.4c1,0,3.2,0.2,4.7,1.4c1.2,1,1.5,2.3,1.7,3.3s0.4,3.1,0.2,4.7c-1.8,19-9.6,65.1-13.6,86.3 c-1.7,9-5,12-8.2,12.3c-7,0.6-12.3-4.6-19-9c-10.6-6.9-16.5-11.2-26.8-18c-11.9-7.8-4.2-12.1,2.6-19.1c1.8-1.8,32.5-29.8,33.1-32.3 c0.1-0.3,0.1-1.5-0.6-2.1c-0.7-0.6-1.7-0.4-2.5-0.2c-1.1,0.2-17.9,11.4-50.6,33.5c-4.8,3.3-9.1,4.9-13,4.8 c-4.3-0.1-12.5-2.4-18.7-4.4c-7.5-2.4-13.5-3.7-13-7.9C45.7,123.3,48.7,121.1,54.3,118.8z');
    c.fillStyle = '#FFFFFF';
    c.fill(p);
    c.restore();
  }

  function drawWifiLogo(c, cx, cy, size, col) {
    c.save();
    c.translate(cx, cy);
    var scale = size / 100;
    c.scale(scale, scale);

    c.strokeStyle = col || '#C6543B';
    c.fillStyle = col || '#C6543B';
    c.lineWidth = 9;
    c.lineCap = 'round';

    c.beginPath();
    c.arc(0, 26, 48, -Math.PI * 0.75, -Math.PI * 0.25);
    c.stroke();

    c.beginPath();
    c.arc(0, 26, 32, -Math.PI * 0.75, -Math.PI * 0.25);
    c.stroke();

    c.beginPath();
    c.arc(0, 26, 16, -Math.PI * 0.75, -Math.PI * 0.25);
    c.stroke();

    c.beginPath();
    c.arc(0, 28, 6, 0, Math.PI * 2);
    c.fill();

    c.restore();
  }

  function getPayload() {
    if (currentType === 'url') {
      var urlInput = document.getElementById('mt-qr-url');
      return (urlInput && urlInput.value.trim()) || 'https://molniya-tech.ru/beauty';
    } else if (currentType === 'sbp') {
      var phoneEl = document.getElementById('mt-qr-sbp-phone');
      var sumEl = document.getElementById('mt-qr-sbp-sum');
      var p = (phoneEl && phoneEl.value.trim()) || '+7 (999) 123-45-67';
      var s = sumEl ? sumEl.value.trim() : '';
      var cleanPhone = p.replace(/\D/g, '');
      if (cleanPhone.length >= 10) {
        return 'https://qr.nspk.ru/proxyapp?phone=' + cleanPhone + (s ? '&sum=' + encodeURIComponent(s) : '');
      }
      return 'СБП: ' + p + (s ? ' Сумма: ' + s + ' руб.' : '');
    } else if (currentType === 'wifi') {
      var ssidEl = document.getElementById('mt-qr-wifi-ssid');
      var passEl = document.getElementById('mt-qr-wifi-pass');
      var typeEl = document.getElementById('mt-qr-wifi-type');
      var ssid = (ssidEl && ssidEl.value.trim()) || 'Molniya_Guest_WiFi';
      var pass = passEl ? passEl.value.trim() : '';
      var type = (typeEl && typeEl.value) || 'WPA';
      return 'WIFI:S:' + ssid + ';T:' + type + ';P:' + pass + ';;';
    } else if (currentType === 'tg') {
      var tgEl = document.getElementById('mt-qr-tg-username');
      var msgEl = document.getElementById('mt-qr-tg-msg');
      var raw = (tgEl && tgEl.value.trim()) || 'molniya_booking_bot';
      var m = msgEl ? msgEl.value.trim() : '';
      var u = raw.replace(/^@/, '');
      if (u.indexOf('http') === 0) return u;
      return 'https://t.me/' + u + (m ? '?text=' + encodeURIComponent(m) : '');
    } else if (currentType === 'wa') {
      var waEl = document.getElementById('mt-qr-wa-phone');
      var waMsgEl = document.getElementById('mt-qr-wa-msg');
      var rawPhone = (waEl && waEl.value.trim()) || '79991234567';
      var clean = rawPhone.replace(/\D/g, '');
      var wMsg = (waMsgEl && waMsgEl.value.trim()) || '';
      return 'https://wa.me/' + clean + (wMsg ? '?text=' + encodeURIComponent(wMsg) : '');
    } else if (currentType === 'vcard') {
      var nameEl = document.getElementById('mt-qr-vcard-name');
      var orgEl = document.getElementById('mt-qr-vcard-org');
      var vPhoneEl = document.getElementById('mt-qr-vcard-phone');
      var vEmailEl = document.getElementById('mt-qr-vcard-email');
      var fn = (nameEl && nameEl.value.trim()) || 'Анна Смирнова';
      var org = (orgEl && orgEl.value.trim()) || 'Студия красоты «Молния»';
      var ph = (vPhoneEl && vPhoneEl.value.trim()) || '+7 (999) 123-45-67';
      var em = (vEmailEl && vEmailEl.value.trim()) || 'anna@molniya-tech.ru';
      return 'BEGIN:VCARD\nVERSION:3.0\nFN:' + fn + '\nORG:' + org + '\nTEL;TYPE=CELL:' + ph + '\nEMAIL:' + em + '\nEND:VCARD';
    }
    return 'https://molniya-tech.ru/tools/qr';
  }

  function getFrameText() {
    if (currentFrame === 'scan') return 'ЗАПИШИТЕСЬ ОНЛАЙН';
    if (currentFrame === 'pay') return 'ОПЛАТА ПО СБП';
    if (currentFrame === 'wifi') return 'WI-FI ДЛЯ ГОСТЕЙ';
    if (currentFrame === 'tg') return 'НАШ TELEGRAM-КАНАЛ';
    if (currentFrame === 'custom') return (customFrameText || 'ОТСКАНИРУЙТЕ QR-КОД').toUpperCase();
    return '';
  }

  function escapeXml(str) {
    return String(str).replace(/[<>&"\']/g, function(c) {
      if (c === '<') return '&lt;';
      if (c === '>') return '&gt;';
      if (c === '&') return '&amp;';
      if (c === "'") return '&apos;';
      if (c === '"') return '&quot;';
      return c;
    });
  }

  function generateSvg(qr, moduleCount, col, frame, fText, logo, customDataUrl) {
    var size = 1024;
    var hasFrame = (frame !== 'none' && fText);
    var qrSize, qrX, qrY;

    if (hasFrame) {
      qrSize = 740;
      qrX = (size - qrSize) / 2;
      qrY = 168;
    } else {
      qrSize = 860;
      qrX = (size - qrSize) / 2;
      qrY = (size - qrSize) / 2;
    }

    var cellSize = qrSize / moduleCount;
    var pathD = '';
    for (var r = 0; r < moduleCount; r++) {
      for (var c = 0; c < moduleCount; c++) {
        if (qr.isDark(r, c)) {
          var mx = (qrX + c * cellSize).toFixed(1);
          var my = (qrY + r * cellSize).toFixed(1);
          var cs = cellSize.toFixed(1);
          pathD += 'M' + mx + ',' + my + 'h' + cs + 'v' + cs + 'h-' + cs + 'Z ';
        }
      }
    }

    var svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + size + ' ' + size + '" width="' + size + '" height="' + size + '">';
    svg += '<rect width="100%" height="100%" fill="#FFFFFF"/>';

    if (hasFrame) {
      svg += '<rect x="60" y="48" width="' + (size - 120) + '" height="84" rx="20" fill="' + col + '"/>';
      svg += '<text x="' + (size / 2) + '" y="102" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="36" font-weight="bold" text-anchor="middle">' + escapeXml(fText) + '</text>';
      svg += '<text x="' + (size / 2) + '" y="968" fill="#6B7280" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="24" font-weight="600" text-anchor="middle">Наведите камеру смартфона</text>';
    }

    svg += '<path d="' + pathD + '" fill="' + col + '"/>';

    if (logo !== 'none') {
      var badgeSize = qrSize * 0.22;
      var bx = (qrX + (qrSize - badgeSize) / 2).toFixed(1);
      var by = (qrY + (qrSize - badgeSize) / 2).toFixed(1);
      var bs = badgeSize.toFixed(1);
      svg += '<rect x="' + bx + '" y="' + by + '" width="' + bs + '" height="' + bs + '" rx="20" fill="#FFFFFF" stroke="#F3F4F6" stroke-width="3"/>';

      var cx = qrX + qrSize / 2;
      var cy = qrY + qrSize / 2;
      var iconSize = badgeSize * 0.65;

      if (logo === 'molniya') {
        svg += '<g transform="translate(' + cx + ',' + cy + ') scale(' + (iconSize / 96) + ') translate(-48,-48)">' +
          '<circle cx="48" cy="48" r="11" fill="none" stroke="#131B2C" stroke-width="8"/>' +
          '<g transform="rotate(0 48 48)"><rect x="41.5" y="6" width="13" height="22" rx="6.5" fill="#131B2C"/></g>' +
          '<g transform="rotate(60 48 48)"><rect x="41.5" y="6" width="13" height="22" rx="6.5" fill="#DF5F3C"/></g>' +
          '<g transform="rotate(120 48 48)"><rect x="41.5" y="6" width="13" height="22" rx="6.5" fill="#131B2C"/></g>' +
          '<g transform="rotate(180 48 48)"><rect x="41.5" y="6" width="13" height="22" rx="6.5" fill="#131B2C"/></g>' +
          '<g transform="rotate(240 48 48)"><rect x="41.5" y="6" width="13" height="22" rx="6.5" fill="#131B2C"/></g>' +
          '<g transform="rotate(300 48 48)"><rect x="41.5" y="6" width="13" height="22" rx="6.5" fill="#131B2C"/></g>' +
          '</g>';
      } else if (logo === 'sbp') {
        var sx = (cx - iconSize / 2).toFixed(1);
        var sy = (cy - iconSize / 2).toFixed(1);
        var ssz = iconSize.toFixed(1);
        svg += '<image x="' + sx + '" y="' + sy + '" width="' + ssz + '" height="' + ssz + '" href="/assets/img/qr/sbp-mark.png"/>';
      } else if (logo === 'tg') {
        svg += '<g transform="translate(' + (cx - iconSize / 2).toFixed(1) + ',' + (cy - iconSize / 2).toFixed(1) + ') scale(' + (iconSize / 240.1).toFixed(4) + ')">' +
          '<defs><linearGradient id="tgGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#2AABEE"/><stop offset="100%" stop-color="#229ED9"/></defs>' +
          '<circle fill="url(#tgGrad)" cx="120.05" cy="120.05" r="120.05"/>' +
          '<path fill="#FFFFFF" d="M54.3,118.8c35-15.2,58.3-25.3,70-30.2 c33.3-13.9,40.3-16.3,44.8-16.4c1,0,3.2,0.2,4.7,1.4c1.2,1,1.5,2.3,1.7,3.3s0.4,3.1,0.2,4.7c-1.8,19-9.6,65.1-13.6,86.3 c-1.7,9-5,12-8.2,12.3c-7,0.6-12.3-4.6-19-9c-10.6-6.9-16.5-11.2-26.8-18c-11.9-7.8-4.2-12.1,2.6-19.1c1.8-1.8,32.5-29.8,33.1-32.3 c0.1-0.3,0.1-1.5-0.6-2.1c-0.7-0.6-1.7-0.4-2.5-0.2c-1.1,0.2-17.9,11.4-50.6,33.5c-4.8,3.3-9.1,4.9-13,4.8 c-4.3-0.1-12.5-2.4-18.7-4.4c-7.5-2.4-13.5-3.7-13-7.9C45.7,123.3,48.7,121.1,54.3,118.8z"/>' +
          '</g>';
      } else if (logo === 'wifi') {
        svg += '<g transform="translate(' + cx + ',' + cy + ') scale(' + (iconSize / 100) + ')" stroke="' + col + '" fill="' + col + '" stroke-width="9" stroke-linecap="round">' +
          '<path d="M-34,-8 A48,48 0 0,1 34,-8" fill="none"/>' +
          '<path d="M-23,3 A32,32 0 0,1 23,3" fill="none"/>' +
          '<path d="M-11,15 A16,16 0 0,1 11,15" fill="none"/>' +
          '<circle cx="0" cy="28" r="6" stroke="none"/>' +
          '</g>';
      } else if (logo === 'custom' && customDataUrl) {
        var imgX = (cx - iconSize / 2).toFixed(1);
        var imgY = (cy - iconSize / 2).toFixed(1);
        var isz = iconSize.toFixed(1);
        svg += '<image x="' + imgX + '" y="' + imgY + '" width="' + isz + '" height="' + isz + '" href="' + customDataUrl + '"/>';
      }
    }

    svg += '</svg>';
    return svg;
  }

  function renderQr() {
    var payload = getPayload();
    var qr;
    try {
      qr = qrcode(0, 'H');
      qr.addData(payload);
      qr.make();
    } catch (e) {
      try {
        qr = qrcode(0, 'M');
        qr.addData(payload);
        qr.make();
      } catch (err) {
        console.error('QR creation error: ', err);
        return;
      }
    }

    var moduleCount = qr.getModuleCount();
    var width = canvas.width;
    var height = canvas.height;

    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(0, 0, width, height);

    var frameText = getFrameText();
    var hasFrame = (currentFrame !== 'none' && frameText);
    var qrSize, qrX, qrY;

    if (hasFrame) {
      ctx.fillStyle = currentColor;
      drawRoundRect(ctx, 60, 48, width - 120, 84, 20, true, false);

      ctx.fillStyle = '#FFFFFF';
      ctx.font = 'bold 36px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(frameText, width / 2, 90);

      ctx.fillStyle = '#6B7280';
      ctx.font = '600 24px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
      ctx.fillText('Наведите камеру смартфона', width / 2, 960);

      qrSize = 740;
      qrX = (width - qrSize) / 2;
      qrY = 168;
    } else {
      qrSize = 860;
      qrX = (width - qrSize) / 2;
      qrY = (height - qrSize) / 2;
    }

    var cellSize = qrSize / moduleCount;
    ctx.fillStyle = currentColor;

    for (var r = 0; r < moduleCount; r++) {
      for (var c = 0; c < moduleCount; c++) {
        if (qr.isDark(r, c)) {
          var mx = qrX + c * cellSize;
          var my = qrY + r * cellSize;
          ctx.fillRect(mx, my, Math.ceil(cellSize), Math.ceil(cellSize));
        }
      }
    }

    if (currentLogo !== 'none') {
      var badgeSize = qrSize * 0.22;
      var bx = qrX + (qrSize - badgeSize) / 2;
      var by = qrY + (qrSize - badgeSize) / 2;

      ctx.save();
      ctx.shadowColor = 'rgba(0, 0, 0, 0.12)';
      ctx.shadowBlur = 18;
      ctx.shadowOffsetY = 4;
      ctx.fillStyle = '#FFFFFF';
      drawRoundRect(ctx, bx, by, badgeSize, badgeSize, 20, true, false);
      ctx.restore();

      ctx.strokeStyle = '#F3F4F6';
      ctx.lineWidth = 3;
      drawRoundRect(ctx, bx, by, badgeSize, badgeSize, 20, false, true);

      var cx = bx + badgeSize / 2;
      var cy = by + badgeSize / 2;
      var iconSize = badgeSize * 0.65;

      if (currentLogo === 'molniya') {
        drawMolniyaMark(ctx, cx, cy, iconSize);
      } else if (currentLogo === 'sbp') {
        drawSbpLogo(ctx, cx, cy, iconSize);
      } else if (currentLogo === 'tg') {
        drawTelegramLogo(ctx, cx, cy, iconSize);
      } else if (currentLogo === 'wifi') {
        drawWifiLogo(ctx, cx, cy, iconSize, currentColor);
      } else if (currentLogo === 'custom' && customLogoImg) {
        ctx.save();
        drawRoundRect(ctx, bx + 12, by + 12, badgeSize - 24, badgeSize - 24, 12, false, false);
        ctx.clip();
        ctx.drawImage(customLogoImg, bx + 12, by + 12, badgeSize - 24, badgeSize - 24);
        ctx.restore();
      }
    }

    var printImg = document.getElementById('mt-qr-print-img');
    var printTitle = document.getElementById('mt-qr-print-title');
    if (printTitle) {
      printTitle.textContent = frameText || 'Запишитесь онлайн';
    }
    if (printImg) {
      printImg.src = canvas.toDataURL('image/png');
    }

    canvas._qrInstance = qr;
    canvas._moduleCount = moduleCount;
    canvas._currentColor = currentColor;
    canvas._currentFrame = currentFrame;
    canvas._frameText = frameText;
    canvas._currentLogo = currentLogo;
    canvas._customLogoDataUrl = customLogoDataUrl;
  }

  var allInputs = wrap.querySelectorAll('input, select, textarea');
  allInputs.forEach(function(inp) {
    inp.addEventListener('input', renderQr);
    inp.addEventListener('change', renderQr);
  });

  tabs.forEach(function(tab) {
    tab.addEventListener('click', function(e) {
      e.preventDefault();
      var type = tab.getAttribute('data-qr-type');
      if (!type) return;

      currentType = type;
      tabs.forEach(function(t) {
        t.classList.toggle('is-active', t === tab);
        t.setAttribute('aria-selected', t === tab ? 'true' : 'false');
      });

      panels.forEach(function(p) {
        var isTarget = p.id === 'mt-qr-panel-' + type;
        p.classList.toggle('is-active', isTarget);
      });

      if (type === 'sbp') {
        selectFrame('pay');
        selectLogo('sbp');
      } else if (type === 'wifi') {
        selectFrame('wifi');
        selectLogo('wifi');
      } else if (type === 'tg') {
        selectFrame('tg');
        selectLogo('tg');
      } else if (type === 'url') {
        selectFrame('scan');
        selectLogo('molniya');
      }

      renderQr();
    });
  });

  function selectFrame(frameKey) {
    currentFrame = frameKey;
    frameBtns.forEach(function(btn) {
      btn.classList.toggle('is-active', btn.getAttribute('data-qr-frame') === frameKey);
    });
    if (frameCustomWrap) {
      frameCustomWrap.style.display = (frameKey === 'custom') ? 'block' : 'none';
      if (frameKey === 'custom' && frameCustomInput) {
        frameCustomInput.focus();
      }
    }
  }

  function selectLogo(logoKey) {
    currentLogo = logoKey;
    logoBtns.forEach(function(btn) {
      btn.classList.toggle('is-active', btn.getAttribute('data-qr-logo') === logoKey);
    });
  }

  frameBtns.forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      var fKey = btn.getAttribute('data-qr-frame');
      if (!fKey) return;
      selectFrame(fKey);
      renderQr();
    });
  });

  if (frameCustomInput) {
    frameCustomInput.addEventListener('input', function() {
      customFrameText = frameCustomInput.value.trim();
      renderQr();
    });
  }

  swatches.forEach(function(sw) {
    sw.addEventListener('click', function(e) {
      e.preventDefault();
      var col = sw.getAttribute('data-qr-color');
      if (!col) return;
      currentColor = col;
      swatches.forEach(function(s) { s.classList.toggle('is-active', s === sw); });
      if (colorCustom) colorCustom.value = col;
      renderQr();
    });
  });

  if (colorCustom) {
    colorCustom.addEventListener('input', function() {
      currentColor = colorCustom.value;
      swatches.forEach(function(s) { s.classList.remove('is-active'); });
      renderQr();
    });
  }

  logoBtns.forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      var lKey = btn.getAttribute('data-qr-logo');
      if (!lKey) return;

      if (lKey === 'custom') {
        if (logoFileInput) logoFileInput.click();
        return;
      }

      selectLogo(lKey);
      renderQr();
    });
  });

  if (logoFileInput) {
    logoFileInput.addEventListener('change', function() {
      var file = logoFileInput.files && logoFileInput.files[0];
      if (!file) return;

      var reader = new FileReader();
      reader.onload = function(evt) {
        var img = new Image();
        img.onload = function() {
          customLogoImg = img;
          customLogoDataUrl = evt.target.result;
          selectLogo('custom');
          if (logoCustomBtn) {
            logoCustomBtn.textContent = '🖼️ Свой файл загружен';
          }
          renderQr();
        };
        img.src = evt.target.result;
      };
      reader.readAsDataURL(file);
    });
  }

  if (downloadPngBtn) {
    downloadPngBtn.addEventListener('click', function(e) {
      e.preventDefault();
      var dataUrl = canvas.toDataURL('image/png');
      var a = document.createElement('a');
      a.href = dataUrl;
      a.download = 'molniya-qr-' + currentType + '.png';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    });
  }

  if (downloadSvgBtn) {
    downloadSvgBtn.addEventListener('click', function(e) {
      e.preventDefault();
      if (!canvas._qrInstance) return;

      var svgContent = generateSvg(
        canvas._qrInstance,
        canvas._moduleCount,
        canvas._currentColor,
        canvas._currentFrame,
        canvas._frameText,
        canvas._currentLogo,
        canvas._customLogoDataUrl
      );

      var blob = new Blob([svgContent], { type: 'image/svg+xml;charset=utf-8' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = 'molniya-qr-' + currentType + '.svg';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(function() { URL.revokeObjectURL(url); }, 1000);
    });
  }

  if (printBtn) {
    printBtn.addEventListener('click', function(e) {
      e.preventDefault();
      window.print();
    });
  }

  if (copyBtn) {
    copyBtn.addEventListener('click', function(e) {
      e.preventDefault();
      var orig = copyBtn.getAttribute('data-orig') || copyBtn.textContent.trim();
      if (!copyBtn.getAttribute('data-orig')) {
        copyBtn.setAttribute('data-orig', orig);
      }

      function onSuccess() {
        copyBtn.textContent = '✅ Скопировано в буфер!';
        copyBtn.classList.add('copied');
        clearTimeout(copyBtn._copyTimeout);
        copyBtn._copyTimeout = setTimeout(function() {
          copyBtn.textContent = orig;
          copyBtn.classList.remove('copied');
        }, 2000);
      }

      if (canvas.toBlob && window.ClipboardItem && navigator.clipboard && navigator.clipboard.write) {
        canvas.toBlob(function(blob) {
          if (!blob) {
            fallbackCopyText();
            return;
          }
          navigator.clipboard.write([
            new ClipboardItem({ 'image/png': blob })
          ]).then(onSuccess).catch(function() {
            fallbackCopyText();
          });
        }, 'image/png');
      } else {
        fallbackCopyText();
      }

      function fallbackCopyText() {
        var payload = getPayload();
        copyTextToClipboard(payload).then(onSuccess).catch(function(err) {
          console.error('Clipboard error:', err);
        });
      }
    });
  }

  renderQr();
}

function initSalaryCalculator() {
  var app = document.getElementById('mt-salary-app');
  if (!app) return;

  var PRESETS = {
    beauty: { shifts: 15, wage: 2500, servRev: 220000, servPct: 40, retRev: 30000, retPct: 10, matPct: 10, mode: 'guarantee_vs_pct' },
    auto: { shifts: 20, wage: 2000, servRev: 350000, servPct: 40, retRev: 200000, retPct: 5, matPct: 5, mode: 'guarantee_vs_pct' },
    detailing: { shifts: 18, wage: 0, servRev: 240000, servPct: 35, retRev: 40000, retPct: 15, matPct: 8, mode: 'base_plus_pct' },
    cleaning: { shifts: 20, wage: 3000, servRev: 180000, servPct: 20, retRev: 10000, retPct: 10, matPct: 7, mode: 'base_plus_pct' },
    fitness: { shifts: 16, wage: 1500, servRev: 175000, servPct: 50, retRev: 25000, retPct: 10, matPct: 0, mode: 'base_plus_pct' }
  };

  var shiftsSlider = app.querySelector('[data-salary-slider="shifts"]');
  var shiftsNum = app.querySelector('[data-salary-num="shifts"]');
  var shiftsVal = app.querySelector('[data-salary-val="shifts"]');

  var wageSlider = app.querySelector('[data-salary-slider="wage"]');
  var wageNum = app.querySelector('[data-salary-num="wage"]');
  var wageVal = app.querySelector('[data-salary-val="wage"]');

  var servRevSlider = app.querySelector('[data-salary-slider="serv-rev"]');
  var servRevNum = app.querySelector('[data-salary-num="serv-rev"]');
  var servRevVal = app.querySelector('[data-salary-val="serv-rev"]');

  var servPctSlider = app.querySelector('[data-salary-slider="serv-pct"]');
  var servPctNum = app.querySelector('[data-salary-num="serv-pct"]');
  var servPctVal = app.querySelector('[data-salary-val="serv-pct"]');

  var retRevSlider = app.querySelector('[data-salary-slider="ret-rev"]');
  var retRevNum = app.querySelector('[data-salary-num="ret-rev"]');
  var retRevVal = app.querySelector('[data-salary-val="ret-rev"]');

  var retPctSlider = app.querySelector('[data-salary-slider="ret-pct"]');
  var retPctNum = app.querySelector('[data-salary-num="ret-pct"]');
  var retPctVal = app.querySelector('[data-salary-val="ret-pct"]');

  var matPctSlider = app.querySelector('[data-salary-slider="mat-pct"]');
  var matPctNum = app.querySelector('[data-salary-num="mat-pct"]');
  var matPctVal = app.querySelector('[data-salary-val="mat-pct"]');

  var modeBtns = app.querySelectorAll('.mt-salary-toggle-btn');
  var currentMode = 'guarantee_vs_pct';

  var outPayout = app.querySelector('[data-salary-res="payout"]');
  var outPayoutSub = app.querySelector('[data-salary-res="payout-sub"]');
  var outShiftRate = app.querySelector('[data-salary-res="shift-rate"]');
  var outShiftRateSub = app.querySelector('[data-salary-res="shift-rate-sub"]');
  var outFotShare = app.querySelector('[data-salary-res="fot-share"]');
  var outFotShareSub = app.querySelector('[data-salary-res="fot-share-sub"]');
  var outBizMargin = app.querySelector('[data-salary-res="biz-margin"]');
  var outBizMarginSub = app.querySelector('[data-salary-res="biz-margin-sub"]');

  var barPayout = app.querySelector('[data-salary-bar="payout"]');
  var barMat = app.querySelector('[data-salary-bar="materials"]');
  var barMargin = app.querySelector('[data-salary-bar="margin"]');

  var legPayout = app.querySelector('[data-salary-leg="payout"]');
  var legMat = app.querySelector('[data-salary-leg="materials"]');
  var legMargin = app.querySelector('[data-salary-leg="margin"]');

  var compModel1 = app.querySelector('[data-salary-comp="model1"]');
  var compModel2 = app.querySelector('[data-salary-comp="model2"]');
  var compModel3 = app.querySelector('[data-salary-comp="model3"]');

  var growthBox = app.querySelector('.mt-salary-growth-box');
  var growthTitle = app.querySelector('[data-salary-growth-title]');
  var growthText = app.querySelector('[data-salary-growth-text]');

  var copyBtn = app.querySelector('.mt-salary-copy-btn');
  var presetBtns = app.querySelectorAll('.mt-salary-preset-btn');

  function fmtMoney(num) {
    return Math.round(num).toLocaleString('ru-RU') + ' ₽';
  }

  function bindTwoWay(slider, num, valDisplay, suffix) {
    if (!slider || !num) return;
    function sync(fromSlider) {
      var val = fromSlider ? slider.value : num.value;
      if (fromSlider) {
        num.value = val;
      } else {
        slider.value = val;
      }
      if (valDisplay) {
        valDisplay.textContent = Number(val).toLocaleString('ru-RU') + (suffix || '');
      }
      calculate();
    }
    slider.addEventListener('input', function() { sync(true); });
    num.addEventListener('input', function() { sync(false); });
  }

  bindTwoWay(shiftsSlider, shiftsNum, shiftsVal, '');
  bindTwoWay(wageSlider, wageNum, wageVal, ' ₽');
  bindTwoWay(servRevSlider, servRevNum, servRevVal, ' ₽');
  bindTwoWay(servPctSlider, servPctNum, servPctVal, '%');
  bindTwoWay(retRevSlider, retRevNum, retRevVal, ' ₽');
  bindTwoWay(retPctSlider, retPctNum, retPctVal, '%');
  bindTwoWay(matPctSlider, matPctNum, matPctVal, '%');

  for (var m = 0; m < modeBtns.length; m++) {
    modeBtns[m].addEventListener('click', function() {
      for (var k = 0; k < modeBtns.length; k++) modeBtns[k].classList.remove('is-active');
      this.classList.add('is-active');
      currentMode = this.getAttribute('data-salary-mode');
      calculate();
    });
  }

  function applyPreset(p) {
    if (shiftsSlider) { shiftsSlider.value = p.shifts; shiftsNum.value = p.shifts; if (shiftsVal) shiftsVal.textContent = p.shifts; }
    if (wageSlider) { wageSlider.value = p.wage; wageNum.value = p.wage; if (wageVal) wageVal.textContent = p.wage.toLocaleString('ru-RU') + ' ₽'; }
    if (servRevSlider) { servRevSlider.value = p.servRev; servRevNum.value = p.servRev; if (servRevVal) servRevVal.textContent = p.servRev.toLocaleString('ru-RU') + ' ₽'; }
    if (servPctSlider) { servPctSlider.value = p.servPct; servPctNum.value = p.servPct; if (servPctVal) servPctVal.textContent = p.servPct + '%'; }
    if (retRevSlider) { retRevSlider.value = p.retRev; retRevNum.value = p.retRev; if (retRevVal) retRevVal.textContent = p.retRev.toLocaleString('ru-RU') + ' ₽'; }
    if (retPctSlider) { retPctSlider.value = p.retPct; retPctNum.value = p.retPct; if (retPctVal) retPctVal.textContent = p.retPct + '%'; }
    if (matPctSlider) { matPctSlider.value = p.matPct; matPctNum.value = p.matPct; if (matPctVal) matPctVal.textContent = p.matPct + '%'; }
    currentMode = p.mode || 'guarantee_vs_pct';
    for (var k = 0; k < modeBtns.length; k++) {
      if (modeBtns[k].getAttribute('data-salary-mode') === currentMode) {
        modeBtns[k].classList.add('is-active');
      } else {
        modeBtns[k].classList.remove('is-active');
      }
    }
    calculate();
  }

  for (var i = 0; i < presetBtns.length; i++) {
    presetBtns[i].addEventListener('click', function() {
      for (var j = 0; j < presetBtns.length; j++) presetBtns[j].classList.remove('is-active');
      this.classList.add('is-active');
      var key = this.getAttribute('data-salary-preset');
      if (PRESETS[key]) {
        applyPreset(PRESETS[key]);
      }
    });
  }

  var lastCalc = {};

  function calculate() {
    var shifts = Math.max(1, parseInt(shiftsSlider ? shiftsSlider.value : 15, 10));
    var wage = Math.max(0, parseFloat(wageSlider ? wageSlider.value : 2500));
    var servRev = Math.max(0, parseFloat(servRevSlider ? servRevSlider.value : 220000));
    var servPct = Math.max(0, Math.min(100, parseInt(servPctSlider ? servPctSlider.value : 40, 10)));
    var retRev = Math.max(0, parseFloat(retRevSlider ? retRevSlider.value : 30000));
    var retPct = Math.max(0, Math.min(50, parseInt(retPctSlider ? retPctSlider.value : 10, 10)));
    var matPct = Math.max(0, Math.min(50, parseInt(matPctSlider ? matPctSlider.value : 10, 10)));

    var guaranteedPay = shifts * wage;
    var matCost = Math.round(servRev * (matPct / 100));
    var netServRev = Math.max(0, servRev - matCost);
    var pieceWorkServ = Math.round(netServRev * (servPct / 100));
    var retailBonus = Math.round(retRev * (retPct / 100));

    var totalPayout = 0;
    if (currentMode === 'base_plus_pct') {
      totalPayout = guaranteedPay + pieceWorkServ + retailBonus;
    } else {
      totalPayout = Math.max(guaranteedPay, pieceWorkServ) + retailBonus;
    }

    var totalRevenue = servRev + retRev;
    var fotShare = totalRevenue > 0 ? (totalPayout / totalRevenue) * 100 : 0;
    var shiftRate = shifts > 0 ? Math.round(totalPayout / shifts) : 0;

    var retailCost = Math.round(retRev * 0.5);
    var bizMargin = Math.max(0, totalRevenue - totalPayout - matCost - retailCost);
    var bizMarginPct = totalRevenue > 0 ? (bizMargin / totalRevenue) * 100 : 0;

    var m1Payout = pieceWorkServ + retailBonus;
    var m2Payout = Math.max(guaranteedPay, pieceWorkServ) + retailBonus;
    var tierBase = Math.min(netServRev, 150000) * 0.35;
    var tierOver = Math.max(0, netServRev - 150000) * 0.45;
    var m3Payout = Math.round(tierBase + tierOver) + retailBonus;

    lastCalc = {
      shifts: shifts,
      wage: wage,
      servRev: servRev,
      servPct: servPct,
      retRev: retRev,
      retPct: retPct,
      matPct: matPct,
      guaranteedPay: guaranteedPay,
      matCost: matCost,
      pieceWorkServ: pieceWorkServ,
      retailBonus: retailBonus,
      totalPayout: totalPayout,
      totalRevenue: totalRevenue,
      fotShare: fotShare,
      shiftRate: shiftRate,
      bizMargin: bizMargin,
      bizMarginPct: bizMarginPct,
      currentMode: currentMode,
      m1Payout: m1Payout,
      m2Payout: m2Payout,
      m3Payout: m3Payout
    };

    if (outPayout) outPayout.textContent = fmtMoney(totalPayout);
    if (outPayoutSub) {
      if (currentMode === 'base_plus_pct') {
        outPayoutSub.textContent = 'Оклад: ' + fmtMoney(guaranteedPay) + ' + Сделка: ' + fmtMoney(pieceWorkServ + retailBonus);
      } else {
        outPayoutSub.textContent = pieceWorkServ >= guaranteedPay ? ('Сделка (' + fmtMoney(pieceWorkServ) + ') превысила гарант') : ('Гарант (' + fmtMoney(guaranteedPay) + ') выше сделки');
      }
    }

    if (outShiftRate) outShiftRate.textContent = fmtMoney(shiftRate);
    if (outShiftRateSub) outShiftRateSub.textContent = Math.round(shiftRate / 10).toLocaleString('ru-RU') + ' ₽/час при 10-часовой смене';

    if (outFotShare) {
      outFotShare.textContent = fotShare.toFixed(1) + '%';
      var fotClass = 'mt-salary-kpi-num ';
      if (fotShare <= 42) fotClass += 'mt-salary-kpi-num--ok';
      else if (fotShare <= 48) fotClass += 'mt-salary-kpi-num--warn';
      else fotClass += 'mt-salary-kpi-num--danger';
      outFotShare.className = fotClass;
    }
    if (outFotShareSub) {
      if (fotShare <= 42) {
        outFotShareSub.textContent = '🟢 Здоровая норма для сферы услуг (до 42%)';
      } else if (fotShare <= 48) {
        outFotShareSub.textContent = '🟡 Повышенная нагрузка на рентабельность (43–48%)';
      } else {
        outFotShareSub.textContent = '🔴 Критическая нагрузка (риск работы в убыток)';
      }
    }

    if (outBizMargin) outBizMargin.textContent = fmtMoney(bizMargin);
    if (outBizMarginSub) outBizMarginSub.textContent = bizMarginPct.toFixed(1) + '% от общей выручки мастера';

    if (totalRevenue > 0) {
      var pShare = Math.min(100, Math.round((totalPayout / totalRevenue) * 100));
      var mShare = Math.min(100 - pShare, Math.round(((matCost + retailCost) / totalRevenue) * 100));
      var bShare = Math.max(0, 100 - pShare - mShare);

      if (barPayout) barPayout.style.width = pShare + '%';
      if (barMat) barMat.style.width = mShare + '%';
      if (barMargin) barMargin.style.width = bShare + '%';

      if (legPayout) legPayout.textContent = fmtMoney(totalPayout) + ' (' + pShare + '%)';
      if (legMat) legMat.textContent = fmtMoney(matCost + retailCost) + ' (' + mShare + '%)';
      if (legMargin) legMargin.textContent = fmtMoney(bizMargin) + ' (' + bShare + '%)';
    }

    if (compModel1) compModel1.textContent = fmtMoney(m1Payout);
    if (compModel2) compModel2.textContent = fmtMoney(m2Payout);
    if (compModel3) compModel3.textContent = fmtMoney(m3Payout);

    if (growthBox && growthTitle && growthText) {
      growthBox.classList.remove('is-warning', 'is-danger');
      if (fotShare > 48) {
        growthBox.classList.add('is-danger');
        growthTitle.innerHTML = '<span>⚠️ Высокая доля ФОТ (' + fotShare.toFixed(1) + '%)</span>';
        growthText.innerHTML = 'При такой доле выплат мастеру локация рискует уйти в минус после вычета аренды и рекламы. Рекомендуется установить базовую ставку 35% и подключить прогрессивный бонус за перевыполнение плана в CRM Молния.';
      } else if (retRev === 0) {
        growthBox.classList.add('is-warning');
        growthTitle.innerHTML = '<span>💡 Упущенная выгода: 0 ₽ с витрины</span>';
        growthText.innerHTML = 'Мастер не продает домашний уход или сопутствующие товары. В салонах и автоцентрах с подключенной витриной Молнии 10% бонус мастерам приносит дополнительные <strong>+35 000 – 60 000 ₽ выручки</strong> в месяц на мастера.';
      } else {
        growthTitle.innerHTML = '<span>⚡ Сбалансированная модель мотивации</span>';
        growthText.innerHTML = 'Доля ФОТ мастера находится в здоровом диапазоне <strong>' + fotShare.toFixed(1) + '%</strong>. В CRM Молния начисление сдельщины, списание расходников по нормам и мотивация витрины происходят автоматически в момент закрытия чека.';
      }
    }
  }

  if (copyBtn) {
    copyBtn.addEventListener('click', function(e) {
      e.preventDefault();
      if (!lastCalc.shifts) return;

      var textToCopy = [
        '=== РАСЧЕТНЫЙ ЛИСТОК МАСТЕРА (МОЛНИЯ ТЕХ) ===',
        'Период: Календарный месяц',
        '• Отработано смен: ' + lastCalc.shifts + ' смен (ставка ' + lastCalc.wage.toLocaleString('ru-RU') + ' ₽/смена)',
        '• Выручка по услугам: ' + lastCalc.servRev.toLocaleString('ru-RU') + ' ₽ (сдельный процент: ' + lastCalc.servPct + '%)',
        '• Вычет себестоимости материалов: ' + lastCalc.matPct + '% (' + lastCalc.matCost.toLocaleString('ru-RU') + ' ₽)',
        '• Продажи витрины/товаров: ' + lastCalc.retRev.toLocaleString('ru-RU') + ' ₽ (бонус: ' + lastCalc.retPct + '% = ' + lastCalc.retailBonus.toLocaleString('ru-RU') + ' ₽)',
        '• Модель расчета: ' + (lastCalc.currentMode === 'base_plus_pct' ? 'Оклад за выход + Процент' : 'Гарант за выход или Процент (что больше)'),
        '--------------------------------------------',
        'ИТОГО К ВЫПЛАТЕ НА РУКИ: ' + lastCalc.totalPayout.toLocaleString('ru-RU') + ' ₽',
        '• Средняя ставка за смену: ' + lastCalc.shiftRate.toLocaleString('ru-RU') + ' ₽/смена',
        '• Доля ФОТ в выручке бизнеса: ' + lastCalc.fotShare.toFixed(1) + '%',
        '• Валовая прибыль локации: ' + lastCalc.bizMargin.toLocaleString('ru-RU') + ' ₽',
        '--------------------------------------------',
        'Рассчитано онлайн на https://molniya-tech.ru/tools/salary'
      ].join('\n');

      copyTextToClipboard(textToCopy).then(function() {
        if (!copyBtn.getAttribute('data-orig')) {
          copyBtn.setAttribute('data-orig', copyBtn.textContent.trim());
        }
        copyBtn.classList.add('copied');
        var btnSpan = copyBtn.querySelector('span');
        if (btnSpan) btnSpan.textContent = 'Расчет скопирован в буфер!';
        setTimeout(function() {
          copyBtn.classList.remove('copied');
          if (btnSpan) btnSpan.textContent = copyBtn.getAttribute('data-orig') || 'Скопировать расчетный листок';
        }, 2500);
      });
    });
  }

  calculate();
}


function initPricelistConstructor() {
  var app = document.getElementById('mt-pricelist-app');
  if (!app) return;

  var PRESETS = {
    beauty: {
      brand: 'Студия красоты «Аура»',
      tagline: 'Эстетика волос, ногтевой сервис и визаж',
      phone: '+7 (812) 724-21-24',
      address: 'Невский проспект, 42',
      bookingUrl: 'molniya-tech.ru/aura',
      theme: 'molniya',
      categories: [
        {
          title: 'Стрижки и укладки',
          items: [
            { name: 'Женская авторская стрижка', dur: '60 мин', price: '2 500 ₽' },
            { name: 'Мужская модельная стрижка', dur: '45 мин', price: '2 000 ₽' },
            { name: 'Дневная укладка / Брашинг', dur: '40 мин', price: '1 800 ₽' },
            { name: 'Вечерний образ и макияж', dur: '90 мин', price: '4 500 ₽' }
          ]
        },
        {
          title: 'Окрашивание и спа-уход',
          items: [
            { name: 'Сложное окрашивание (Airtouch)', dur: '3.5 ч', price: 'от 9 500 ₽' },
            { name: 'Тонирование и уход за блондом', dur: '90 мин', price: '4 200 ₽' },
            { name: 'Глубокое спа-восстановление волос', dur: '60 мин', price: '3 200 ₽' }
          ]
        },
        {
          title: 'Ногтевой сервис',
          items: [
            { name: 'Маникюр с покрытием гель-лак', dur: '90 мин', price: '2 400 ₽' },
            { name: 'Смарт-педикюр комплексный', dur: '90 мин', price: '3 200 ₽' },
            { name: 'Японский эко-маникюр Masura', dur: '60 мин', price: '2 100 ₽' }
          ]
        }
      ]
    },
    barber: {
      brand: 'Барбершоп «Норд»',
      tagline: 'Мужские стрижки, бритье опасной бритвой и уход за бородой',
      phone: '+7 (812) 724-21-24',
      address: 'Литейный проспект, 18',
      bookingUrl: 'molniya-tech.ru/nord',
      theme: 'noir',
      categories: [
        {
          title: 'Стрижки',
          items: [
            { name: 'Мужская стрижка Fade / Crop', dur: '45 мин', price: '2 200 ₽' },
            { name: 'Стрижка ножницами (удлиненная)', dur: '60 мин', price: '2 500 ₽' },
            { name: 'Стрижка машинкой (1-2 насадки)', dur: '30 мин', price: '1 400 ₽' }
          ]
        },
        {
          title: 'Борода и бритье',
          items: [
            { name: 'Моделирование и стрижка бороды', dur: '35 мин', price: '1 500 ₽' },
            { name: 'Королевское бритье опасной бритвой', dur: '45 мин', price: '2 000 ₽' },
            { name: 'Камуфляж седины и бороды', dur: '25 мин', price: '1 200 ₽' }
          ]
        },
        {
          title: 'Комбо-комплексы',
          items: [
            { name: 'Стрижка + Моделирование бороды', dur: '75 мин', price: '3 300 ₽' },
            { name: 'Отец + Сын (2 стрижки)', dur: '80 мин', price: '3 900 ₽' }
          ]
        }
      ]
    },
    auto: {
      brand: 'Детейлинг-центр «Формула»',
      tagline: 'Профессиональный уход, полировка и керамическая защита кузова',
      phone: '+7 (812) 724-21-24',
      address: 'Московский проспект, 115',
      bookingUrl: 'molniya-tech.ru/formula',
      theme: 'noir',
      categories: [
        {
          title: 'Мойка и уход',
          items: [
            { name: 'Трехфазная детейлинг-мойка кузова', dur: '60 мин', price: 'от 1 800 ₽' },
            { name: 'Глубокая химчистка салона с сушкой', dur: '5 ч', price: 'от 12 000 ₽' },
            { name: 'Консервация подкапотного пространства', dur: '90 мин', price: '3 500 ₽' }
          ]
        },
        {
          title: 'Полировка и керамика',
          items: [
            { name: 'Восстановительная полировка кузова', dur: '8 ч', price: 'от 18 000 ₽' },
            { name: 'Керамическое покрытие (2 слоя)', dur: '10 ч', price: 'от 25 000 ₽' },
            { name: 'Антидождь на все стекла Aquapel', dur: '45 мин', price: '4 000 ₽' }
          ]
        }
      ]
    },
    massage: {
      brand: 'Студия массажа «Гармония»',
      tagline: 'Массаж тела, остеопатия и восстановительные ритуалы',
      phone: '+7 (812) 724-21-24',
      address: 'Каменноостровский проспект, 26',
      bookingUrl: 'molniya-tech.ru/harmony',
      theme: 'nordic',
      categories: [
        {
          title: 'Массаж тела',
          items: [
            { name: 'Классический общий массаж тела', dur: '60 мин', price: '3 200 ₽' },
            { name: 'Глубокий спортивный массаж', dur: '75 мин', price: '3 800 ₽' },
            { name: 'Лимфодренажный детокс-массаж', dur: '60 мин', price: '3 400 ₽' },
            { name: 'Аромамассаж горячими маслами', dur: '90 мин', price: '4 500 ₽' }
          ]
        },
        {
          title: 'Эстетика лица',
          items: [
            { name: 'Скульптурно-буккальный массаж лица', dur: '60 мин', price: '3 500 ₽' },
            { name: 'Миофасциальный лифтинг-массаж', dur: '60 мин', price: '3 600 ₽' }
          ]
        }
      ]
    },
    cleaning: {
      brand: 'Клининг «Чистый Дом»',
      tagline: 'Генеральная уборка, мойка окон и химчистка мебели',
      phone: '+7 (812) 724-21-24',
      address: 'Санкт-Петербург и ЛО',
      bookingUrl: 'molniya-tech.ru/clean',
      theme: 'nordic',
      categories: [
        {
          title: 'Уборка помещений',
          items: [
            { name: 'Поддерживающая уборка (до 50 м²)', dur: '2.5 ч', price: 'от 3 500 ₽' },
            { name: 'Генеральная уборка квартиры', dur: '5 ч', price: 'от 7 500 ₽' },
            { name: 'Уборка после ремонта под ключ', dur: '7 ч', price: 'от 11 000 ₽' }
          ]
        },
        {
          title: 'Химчистка на дому',
          items: [
            { name: 'Химчистка прямого дивана (3 места)', dur: '90 мин', price: '3 600 ₽' },
            { name: 'Химчистка углового дивана', dur: '2 ч', price: '4 800 ₽' },
            { name: 'Сезонная мойка стандартного окна', dur: '30 мин', price: '900 ₽' }
          ]
        }
      ]
    }
  };

  // Clone initial state from beauty preset
  var state = JSON.parse(JSON.stringify(PRESETS.beauty));

  // DOM Elements
  var brandInput = app.querySelector('#mt-pl-brand');
  var taglineInput = app.querySelector('#mt-pl-tagline');
  var phoneInput = app.querySelector('#mt-pl-phone');
  var addressInput = app.querySelector('#mt-pl-address');
  var bookingInput = app.querySelector('#mt-pl-booking');

  var themeBtns = app.querySelectorAll('.mt-pricelist-theme-btn');
  var presetBtns = app.querySelectorAll('.mt-pricelist-preset-btn');
  var categoriesContainer = app.querySelector('#mt-pl-categories-editor');
  var addCategoryBtn = app.querySelector('#mt-pl-add-category-btn');

  var sheet = app.querySelector('#mt-pricelist-sheet');
  var printBtn = app.querySelector('#mt-pl-print-btn');
  var copyBtn = app.querySelector('#mt-pl-copy-btn');

  function syncInputsFromState() {
    if (brandInput) brandInput.value = state.brand;
    if (taglineInput) taglineInput.value = state.tagline;
    if (phoneInput) phoneInput.value = state.phone;
    if (addressInput) addressInput.value = state.address;
    if (bookingInput) bookingInput.value = state.bookingUrl;

    for (var i = 0; i < themeBtns.length; i++) {
      if (themeBtns[i].getAttribute('data-theme') === state.theme) {
        themeBtns[i].classList.add('is-active');
      } else {
        themeBtns[i].classList.remove('is-active');
      }
    }
  }

  function renderCategoriesEditor() {
    if (!categoriesContainer) return;
    categoriesContainer.innerHTML = '';

    state.categories.forEach(function(cat, catIdx) {
      var catCard = document.createElement('div');
      catCard.className = 'mt-pricelist-cat-block';

      var catHeader = document.createElement('div');
      catHeader.className = 'mt-pricelist-cat-header';

      var catInput = document.createElement('input');
      catInput.type = 'text';
      catInput.className = 'mt-pricelist-input mt-pricelist-cat-title-input';
      catInput.value = cat.title;
      catInput.placeholder = 'Название категории (например, Стрижки)';
      catInput.addEventListener('input', function() {
        cat.title = this.value;
        renderSheet();
      });

      var delCatBtn = document.createElement('button');
      delCatBtn.type = 'button';
      delCatBtn.className = 'mt-pricelist-del-btn';
      delCatBtn.title = 'Удалить категорию';
      delCatBtn.innerHTML = '✕';
      delCatBtn.addEventListener('click', function() {
        state.categories.splice(catIdx, 1);
        renderCategoriesEditor();
        renderSheet();
      });

      catHeader.appendChild(catInput);
      catHeader.appendChild(delCatBtn);
      catCard.appendChild(catHeader);

      var itemsWrap = document.createElement('div');
      itemsWrap.className = 'mt-pricelist-items-editor';

      cat.items.forEach(function(item, itemIdx) {
        var row = document.createElement('div');
        row.className = 'mt-pricelist-item-row';

        var nameInput = document.createElement('input');
        nameInput.type = 'text';
        nameInput.className = 'mt-pricelist-input';
        nameInput.value = item.name;
        nameInput.placeholder = 'Название услуги';
        nameInput.addEventListener('input', function() {
          item.name = this.value;
          renderSheet();
        });

        var durInput = document.createElement('input');
        durInput.type = 'text';
        durInput.className = 'mt-pricelist-input';
        durInput.value = item.dur;
        durInput.placeholder = 'Время (60 мин)';
        durInput.addEventListener('input', function() {
          item.dur = this.value;
          renderSheet();
        });

        var priceInput = document.createElement('input');
        priceInput.type = 'text';
        priceInput.className = 'mt-pricelist-input';
        priceInput.value = item.price;
        priceInput.placeholder = 'Цена (2 500 ₽)';
        priceInput.addEventListener('input', function() {
          item.price = this.value;
          renderSheet();
        });

        var delItemBtn = document.createElement('button');
        delItemBtn.type = 'button';
        delItemBtn.className = 'mt-pricelist-del-btn';
        delItemBtn.title = 'Удалить услугу';
        delItemBtn.innerHTML = '✕';
        delItemBtn.addEventListener('click', function() {
          cat.items.splice(itemIdx, 1);
          renderCategoriesEditor();
          renderSheet();
        });

        row.appendChild(nameInput);
        row.appendChild(durInput);
        row.appendChild(priceInput);
        row.appendChild(delItemBtn);
        itemsWrap.appendChild(row);
      });

      var addItemBtn = document.createElement('button');
      addItemBtn.type = 'button';
      addItemBtn.className = 'mt-pricelist-add-item-btn';
      addItemBtn.innerHTML = '+ Добавить услугу';
      addItemBtn.addEventListener('click', function() {
        cat.items.push({ name: 'Новая услуга', dur: '45 мин', price: '1 500 ₽' });
        renderCategoriesEditor();
        renderSheet();
      });

      catCard.appendChild(itemsWrap);
      catCard.appendChild(addItemBtn);
      categoriesContainer.appendChild(catCard);
    });
  }

  function renderSheet() {
    if (!sheet) return;

    // Apply theme class
    sheet.className = 'mt-pricelist-sheet theme-' + state.theme;

    var categoriesHtml = state.categories.map(function(cat) {
      var itemsHtml = cat.items.map(function(item) {
        var durHtml = item.dur ? '<span class="mt-sheet-item-dur mt-sheet-muted">(' + escapeHtml(item.dur) + ')</span>' : '';
        return [
          '<div class="mt-sheet-item">',
          '  <span class="mt-sheet-item-name">' + escapeHtml(item.name) + '</span>',
          durHtml,
          '  <span class="mt-sheet-dots mt-sheet-dots"></span>',
          '  <span class="mt-sheet-item-price mt-sheet-accent">' + escapeHtml(item.price) + '</span>',
          '</div>'
        ].join('');
      }).join('');

      return [
        '<div class="mt-sheet-cat">',
        '  <div class="mt-sheet-cat-title mt-sheet-border mt-sheet-accent">',
        '    <span>' + escapeHtml(cat.title) + '</span>',
        '  </div>',
        '  <div class="mt-sheet-items">',
        itemsHtml,
        '  </div>',
        '</div>'
      ].join('');
    }).join('');

    sheet.innerHTML = [
      '<div class="mt-sheet-header mt-sheet-border">',
      '  <div class="mt-sheet-brand mt-sheet-accent">' + escapeHtml(state.brand) + '</div>',
      '  <div class="mt-sheet-tagline mt-sheet-muted">' + escapeHtml(state.tagline) + '</div>',
      '  <div class="mt-sheet-contacts mt-sheet-muted">',
      state.phone ? '<span>📞 ' + escapeHtml(state.phone) + '</span>' : '',
      state.address ? '<span>📍 ' + escapeHtml(state.address) + '</span>' : '',
      state.bookingUrl ? '<span>⚡ ' + escapeHtml(state.bookingUrl) + '</span>' : '',
      '  </div>',
      '</div>',
      '<div class="mt-sheet-content">',
      categoriesHtml,
      '</div>',
      '<div class="mt-sheet-footer mt-sheet-border mt-sheet-muted">',
      '  <span>Прейскурант цен 2026. Предварительная запись обязательна.</span>',
      '  <div class="mt-sheet-qr-box">',
      '    <span class="mt-sheet-accent">⚡ Онлайн-запись 24/7</span>',
      '  </div>',
      '</div>'
    ].join('');
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // Header input listeners
  if (brandInput) brandInput.addEventListener('input', function() { state.brand = this.value; renderSheet(); });
  if (taglineInput) taglineInput.addEventListener('input', function() { state.tagline = this.value; renderSheet(); });
  if (phoneInput) phoneInput.addEventListener('input', function() { state.phone = this.value; renderSheet(); });
  if (addressInput) addressInput.addEventListener('input', function() { state.address = this.value; renderSheet(); });
  if (bookingInput) bookingInput.addEventListener('input', function() { state.bookingUrl = this.value; renderSheet(); });

  // Add Category button
  if (addCategoryBtn) {
    addCategoryBtn.addEventListener('click', function() {
      state.categories.push({
        title: 'Новая категория услуг',
        items: [{ name: 'Наименование процедуры', dur: '60 мин', price: '2 000 ₽' }]
      });
      renderCategoriesEditor();
      renderSheet();
    });
  }

  // Theme selection
  for (var t = 0; t < themeBtns.length; t++) {
    themeBtns[t].addEventListener('click', function() {
      for (var k = 0; k < themeBtns.length; k++) themeBtns[k].classList.remove('is-active');
      this.classList.add('is-active');
      state.theme = this.getAttribute('data-theme');
      renderSheet();
    });
  }

  // Presets selection
  for (var p = 0; p < presetBtns.length; p++) {
    presetBtns[p].addEventListener('click', function() {
      for (var j = 0; j < presetBtns.length; j++) presetBtns[j].classList.remove('is-active');
      this.classList.add('is-active');
      var key = this.getAttribute('data-pricelist-preset');
      if (PRESETS[key]) {
        state = JSON.parse(JSON.stringify(PRESETS[key]));
        syncInputsFromState();
        renderCategoriesEditor();
        renderSheet();
      }
    });
  }

  // Print button
  if (printBtn) {
    printBtn.addEventListener('click', function(e) {
      e.preventDefault();
      window.print();
    });
  }

  // Copy text representation
  if (copyBtn) {
    copyBtn.addEventListener('click', function(e) {
      e.preventDefault();

      var lines = [
        '=== ' + state.brand.toUpperCase() + ' ===',
        state.tagline,
        '📞 ' + state.phone + (state.address ? ' | 📍 ' + state.address : ''),
        state.bookingUrl ? '⚡ Онлайн-запись: https://' + state.bookingUrl : '',
        '--------------------------------------------'
      ];

      state.categories.forEach(function(cat) {
        lines.push('');
        lines.push('【 ' + cat.title.toUpperCase() + ' 】');
        cat.items.forEach(function(item) {
          var durStr = item.dur ? ' (' + item.dur + ')' : '';
          lines.push('• ' + item.name + durStr + ' — ' + item.price);
        });
      });

      lines.push('');
      lines.push('--------------------------------------------');
      lines.push('Сформировано в конструкторе прайс-листов: https://molniya-tech.ru/tools/pricelist');

      var textToCopy = lines.filter(Boolean).join('\n');

      copyTextToClipboard(textToCopy).then(function() {
        if (!copyBtn.getAttribute('data-orig')) {
          copyBtn.setAttribute('data-orig', copyBtn.textContent.trim());
        }
        copyBtn.classList.add('copied');
        var btnSpan = copyBtn.querySelector('span');
        if (btnSpan) btnSpan.textContent = 'Прайс скопирован в буфер!';
        setTimeout(function() {
          copyBtn.classList.remove('copied');
          if (btnSpan) btnSpan.textContent = copyBtn.getAttribute('data-orig') || 'Скопировать прайс текстом';
        }, 2500);
      });
    });
  }

  // Initial render
  syncInputsFromState();
  renderCategoriesEditor();
  renderSheet();
}



function initAcquiringCalculator() {
  var app = document.getElementById('mt-acquiring-app');
  if (!app) return;

  var PRESETS = {
    beauty: { rev: 750000, acqPct: 2.2, posRent: 1500, sbpShare: 65, sbpRate: 0.7 },
    auto: { rev: 1800000, acqPct: 1.9, posRent: 2500, sbpShare: 60, sbpRate: 0.7 },
    detailing: { rev: 900000, acqPct: 2.1, posRent: 1500, sbpShare: 65, sbpRate: 0.7 },
    medical: { rev: 1500000, acqPct: 1.8, posRent: 2000, sbpShare: 70, sbpRate: 0.4 },
    cleaning: { rev: 450000, acqPct: 2.3, posRent: 1000, sbpShare: 75, sbpRate: 0.4 }
  };

  var revSlider = app.querySelector('[data-acq-slider="rev"]');
  var revNum = app.querySelector('[data-acq-num="rev"]');
  var revVal = app.querySelector('[data-acq-val="rev"]');

  var acqPctSlider = app.querySelector('[data-acq-slider="acq-pct"]');
  var acqPctNum = app.querySelector('[data-acq-num="acq-pct"]');
  var acqPctVal = app.querySelector('[data-acq-val="acq-pct"]');

  var posRentSlider = app.querySelector('[data-acq-slider="pos-rent"]');
  var posRentNum = app.querySelector('[data-acq-num="pos-rent"]');
  var posRentVal = app.querySelector('[data-acq-val="pos-rent"]');

  var sbpShareSlider = app.querySelector('[data-acq-slider="sbp-share"]');
  var sbpShareNum = app.querySelector('[data-acq-num="sbp-share"]');
  var sbpShareVal = app.querySelector('[data-acq-val="sbp-share"]');

  var sbpRateBtns = app.querySelectorAll('.mt-acquiring-toggle-btn');
  var currentSbpRate = 0.7;

  var outYearlySavings = app.querySelector('[data-acq-res="yearly-savings"]');
  var outYearlySavingsSub = app.querySelector('[data-acq-res="yearly-savings-sub"]');
  var outMonthlyCost = app.querySelector('[data-acq-res="monthly-cost"]');
  var outMonthlyCostSub = app.querySelector('[data-acq-res="monthly-cost-sub"]');
  var outEffRate = app.querySelector('[data-acq-res="eff-rate"]');
  var outEffRateSub = app.querySelector('[data-acq-res="eff-rate-sub"]');
  var outSpeed = app.querySelector('[data-acq-res="speed"]');
  var outSpeedSub = app.querySelector('[data-acq-res="speed-sub"]');

  var barSavings = app.querySelector('[data-acq-bar="savings"]');
  var barBank = app.querySelector('[data-acq-bar="bank"]');
  var barPos = app.querySelector('[data-acq-bar="pos"]');

  var legSavings = app.querySelector('[data-acq-leg="savings"]');
  var legBank = app.querySelector('[data-acq-leg="bank"]');
  var legPos = app.querySelector('[data-acq-leg="pos"]');

  var compModel1 = app.querySelector('[data-acq-comp="model1"]');
  var compModel2 = app.querySelector('[data-acq-comp="model2"]');
  var compModel3 = app.querySelector('[data-acq-comp="model3"]');

  var growthText = app.querySelector('[data-acq-growth-text]');
  var copyBtn = app.querySelector('.mt-acquiring-copy-btn');
  var presetBtns = app.querySelectorAll('.mt-acquiring-preset-btn');

  function fmtMoney(num) {
    return Math.round(num).toLocaleString('ru-RU') + ' ₽';
  }

  function bindTwoWay(slider, num, valDisplay, suffix) {
    if (!slider || !num) return;
    function sync(fromSlider) {
      var val = fromSlider ? slider.value : num.value;
      if (fromSlider) {
        num.value = val;
      } else {
        slider.value = val;
      }
      if (valDisplay) {
        valDisplay.textContent = Number(val).toLocaleString('ru-RU') + (suffix || '');
      }
      calculate();
    }
    slider.addEventListener('input', function() { sync(true); });
    num.addEventListener('input', function() { sync(false); });
  }

  bindTwoWay(revSlider, revNum, revVal, ' ₽');
  bindTwoWay(acqPctSlider, acqPctNum, acqPctVal, '%');
  bindTwoWay(posRentSlider, posRentNum, posRentVal, ' ₽');
  bindTwoWay(sbpShareSlider, sbpShareNum, sbpShareVal, '%');

  for (var m = 0; m < sbpRateBtns.length; m++) {
    sbpRateBtns[m].addEventListener('click', function() {
      for (var k = 0; k < sbpRateBtns.length; k++) sbpRateBtns[k].classList.remove('is-active');
      this.classList.add('is-active');
      currentSbpRate = parseFloat(this.getAttribute('data-sbp-rate')) || 0.7;
      calculate();
    });
  }

  function applyPreset(p) {
    if (revSlider) { revSlider.value = p.rev; revNum.value = p.rev; if (revVal) revVal.textContent = p.rev.toLocaleString('ru-RU') + ' ₽'; }
    if (acqPctSlider) { acqPctSlider.value = p.acqPct; acqPctNum.value = p.acqPct; if (acqPctVal) acqPctVal.textContent = p.acqPct + '%'; }
    if (posRentSlider) { posRentSlider.value = p.posRent; posRentNum.value = p.posRent; if (posRentVal) posRentVal.textContent = p.posRent.toLocaleString('ru-RU') + ' ₽'; }
    if (sbpShareSlider) { sbpShareSlider.value = p.sbpShare; sbpShareNum.value = p.sbpShare; if (sbpShareVal) sbpShareVal.textContent = p.sbpShare + '%'; }
    currentSbpRate = p.sbpRate || 0.7;
    for (var k = 0; k < sbpRateBtns.length; k++) {
      var btnRate = parseFloat(sbpRateBtns[k].getAttribute('data-sbp-rate'));
      if (Math.abs(btnRate - currentSbpRate) < 0.05) {
        sbpRateBtns[k].classList.add('is-active');
      } else {
        sbpRateBtns[k].classList.remove('is-active');
      }
    }
    calculate();
  }

  for (var i = 0; i < presetBtns.length; i++) {
    presetBtns[i].addEventListener('click', function() {
      for (var j = 0; j < presetBtns.length; j++) presetBtns[j].classList.remove('is-active');
      this.classList.add('is-active');
      var key = this.getAttribute('data-acq-preset');
      if (PRESETS[key]) applyPreset(PRESETS[key]);
    });
  }

  function calculate() {
    var rev = parseFloat(revSlider ? revSlider.value : 750000) || 750000;
    var acqPct = parseFloat(acqPctSlider ? acqPctSlider.value : 2.2) || 2.2;
    var posRent = parseFloat(posRentSlider ? posRentSlider.value : 1500) || 0;
    var sbpShare = parseFloat(sbpShareSlider ? sbpShareSlider.value : 65) || 65;
    var sbpRate = currentSbpRate;

    // Current cost (100% card acquiring + pos rent)
    var curAcqFee = rev * (acqPct / 100);
    var curTotalMonthly = curAcqFee + posRent;
    var curTotalYearly = curTotalMonthly * 12;
    var curEffRate = rev > 0 ? (curTotalMonthly / rev) * 100 : acqPct;

    // New cost with SBP
    var sbpVol = rev * (sbpShare / 100);
    var cardVol = rev - sbpVol;
    var newSbpFee = sbpVol * (sbpRate / 100);
    var newAcqFee = cardVol * (acqPct / 100);
    var newPosRent = sbpShare >= 100 ? 0 : posRent;
    var newTotalMonthly = newSbpFee + newAcqFee + newPosRent;
    var newTotalYearly = newTotalMonthly * 12;
    var newEffRate = rev > 0 ? (newTotalMonthly / rev) * 100 : sbpRate;

    var monthlySavings = Math.max(0, curTotalMonthly - newTotalMonthly);
    var yearlySavings = monthlySavings * 12;
    var savingsPct = curTotalMonthly > 0 ? ((curTotalMonthly - newTotalMonthly) / curTotalMonthly) * 100 : 0;

    // Model 1: Only Classic Acquiring
    var m1Cost = curTotalMonthly;
    // Model 2: Hybrid (current settings)
    var m2Cost = newTotalMonthly;
    // Model 3: 100% SBP / Online via Molniya (0 pos rent)
    var m3Cost = rev * (sbpRate / 100);

    // Update KPIs
    if (outYearlySavings) outYearlySavings.textContent = fmtMoney(yearlySavings);
    if (outYearlySavingsSub) outYearlySavingsSub.textContent = 'Экономия ' + fmtMoney(monthlySavings) + ' каждый месяц';

    if (outMonthlyCost) outMonthlyCost.textContent = fmtMoney(newTotalMonthly) + '/мес';
    if (outMonthlyCostSub) outMonthlyCostSub.textContent = 'Было ' + fmtMoney(curTotalMonthly) + ' (−' + savingsPct.toFixed(1) + '%)';

    if (outEffRate) outEffRate.textContent = newEffRate.toFixed(2) + '%';
    if (outEffRateSub) outEffRateSub.textContent = 'Вместо прежних ' + curEffRate.toFixed(2) + '% с терминалом';

    if (outSpeed) outSpeed.textContent = '15 секунд';
    if (outSpeedSub) outSpeedSub.textContent = 'Мгновенно на р/с 24/7 (вместо 1–3 дней)';

    // Update progress bar
    var baseDenom = Math.max(curTotalMonthly, 1);
    var pctSavings = Math.min(100, Math.max(0, (monthlySavings / baseDenom) * 100));
    var pctBank = Math.min(100, Math.max(0, ((newSbpFee + newAcqFee) / baseDenom) * 100));
    var pctPos = Math.min(100, Math.max(0, 100 - pctSavings - pctBank));

    if (barSavings) barSavings.style.width = pctSavings.toFixed(1) + '%';
    if (barBank) barBank.style.width = pctBank.toFixed(1) + '%';
    if (barPos) barPos.style.width = pctPos.toFixed(1) + '%';

    if (legSavings) legSavings.textContent = fmtMoney(monthlySavings) + ' (' + pctSavings.toFixed(0) + '%)';
    if (legBank) legBank.textContent = fmtMoney(newSbpFee + newAcqFee) + ' (' + pctBank.toFixed(0) + '%)';
    if (legPos) legPos.textContent = fmtMoney(newPosRent) + ' (' + pctPos.toFixed(0) + '%)';

    // Model comparisons
    if (compModel1) compModel1.textContent = fmtMoney(m1Cost) + '/мес';
    if (compModel2) compModel2.textContent = fmtMoney(m2Cost) + '/мес';
    if (compModel3) compModel3.textContent = fmtMoney(m3Cost) + '/мес';

    // Insight text
    if (growthText) {
      growthText.innerHTML = 'При безналичном обороте <strong>' + fmtMoney(rev) + '</strong> перевод части оплат на СБП в вашем банке сберегает <strong>' + fmtMoney(yearlySavings) + ' в год</strong>. А в платформе Молния вы можете настроить прием предоплат через СБП в онлайн-записи и вести прозрачный учет оплат по картам и QR в едином журнале визитов без ошибок в расчете зарплат мастеров.';
    }
  }

  // Copy summary button
  if (copyBtn) {
    copyBtn.addEventListener('click', function(e) {
      e.preventDefault();
      var rev = parseFloat(revSlider ? revSlider.value : 750000) || 750000;
      var acqPct = parseFloat(acqPctSlider ? acqPctSlider.value : 2.2) || 2.2;
      var posRent = parseFloat(posRentSlider ? posRentSlider.value : 1500) || 0;
      var sbpShare = parseFloat(sbpShareSlider ? sbpShareSlider.value : 65) || 65;
      var sbpRate = currentSbpRate;

      var curAcqFee = rev * (acqPct / 100);
      var curTotalMonthly = curAcqFee + posRent;
      var curTotalYearly = curTotalMonthly * 12;

      var sbpVol = rev * (sbpShare / 100);
      var cardVol = rev - sbpVol;
      var newSbpFee = sbpVol * (sbpRate / 100);
      var newAcqFee = cardVol * (acqPct / 100);
      var newPosRent = sbpShare >= 100 ? 0 : posRent;
      var newTotalMonthly = newSbpFee + newAcqFee + newPosRent;
      var newTotalYearly = newTotalMonthly * 12;
      var yearlySavings = (curTotalMonthly - newTotalMonthly) * 12;

      var lines = [
        '=== РАСЧЕТ ЭКОНОМИИ НА ЭКВАЙРИНГЕ И СБП ===',
        'Безналичный оборот: ' + fmtMoney(rev) + ' в месяц',
        'Текущая комиссия эквайринга: ' + acqPct + '% (+ аренда терминала ' + fmtMoney(posRent) + '/мес)',
        'Расходы на эквайринг сейчас: ' + fmtMoney(curTotalMonthly) + '/мес (' + fmtMoney(curTotalYearly) + '/год)',
        '--------------------------------------------',
        'При подключении СБП (доля ' + sbpShare + '%, ставка ' + sbpRate + '%):',
        'Новые расходы: ' + fmtMoney(newTotalMonthly) + '/мес (' + fmtMoney(newTotalYearly) + '/год)',
        'ЧИСТАЯ ЭКОНОМИЯ: ' + fmtMoney(curTotalMonthly - newTotalMonthly) + '/мес (+' + fmtMoney(yearlySavings) + '/год)',
        'Эффективная ставка комиссии снижается до ' + ((newTotalMonthly / rev) * 100).toFixed(2) + '%',
        'Зачисление средств: мгновенно за 15 секунд 24/7/365',
        '--------------------------------------------',
        'Рассчитано в калькуляторе эквайринга: https://molniya-tech.ru/tools/acquiring'
      ];

      var textToCopy = lines.join('\n');

      copyTextToClipboard(textToCopy).then(function() {
        if (!copyBtn.getAttribute('data-orig')) {
          copyBtn.setAttribute('data-orig', copyBtn.textContent.trim());
        }
        copyBtn.classList.add('copied');
        var btnSpan = copyBtn.querySelector('span');
        if (btnSpan) btnSpan.textContent = 'Расчет скопирован в буфер!';
        setTimeout(function() {
          copyBtn.classList.remove('copied');
          if (btnSpan) btnSpan.textContent = copyBtn.getAttribute('data-orig') || 'Скопировать расчет экономии';
        }, 2500);
      });
    });
  }

  calculate();
}



function initShiftsMaker() {
  var app = document.getElementById('mt-shifts-app');
  if (!app) return;

  var WEEKDAY_NAMES = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'];
  var MONTH_NAMES = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
  ];

  var PRESETS = {
    beauty: {
      year: 2026,
      month: 10, // November (0-based: 10 = Nov)
      hoursPerShift: 11,
      masters: [
        { id: 1, name: 'Анна (Стилист)', pattern: '2_2_a' },
        { id: 2, name: 'Елена (Колорист)', pattern: '2_2_a' },
        { id: 3, name: 'Мария (Стилист)', pattern: '2_2_b' },
        { id: 4, name: 'Ольга (Визажист)', pattern: '2_2_b' }
      ]
    },
    barber: {
      year: 2026,
      month: 10,
      hoursPerShift: 10,
      masters: [
        { id: 1, name: 'Тимур (Шеф-барбер)', pattern: '2_2_a' },
        { id: 2, name: 'Даниил (Топ-барбер)', pattern: '2_2_a' },
        { id: 3, name: 'Руслан (Барбер)', pattern: '2_2_b' },
        { id: 4, name: 'Артем (Барбер)', pattern: '2_2_b' }
      ]
    },
    auto: {
      year: 2026,
      month: 10,
      hoursPerShift: 11,
      masters: [
        { id: 1, name: 'Иван (Мастер-приемщик)', pattern: '2_2_a' },
        { id: 2, name: 'Сергей (Моторист)', pattern: '2_2_a' },
        { id: 3, name: 'Алексей (Диагност)', pattern: '5_2' },
        { id: 4, name: 'Денис (Слесарь СТО)', pattern: '2_2_b' },
        { id: 5, name: 'Михаил (Электрик)', pattern: '2_2_b' }
      ]
    },
    detailing: {
      year: 2026,
      month: 10,
      hoursPerShift: 12,
      masters: [
        { id: 1, name: 'Смена 1: Детейлер А', pattern: '2_2_a' },
        { id: 2, name: 'Смена 1: Мойщик', pattern: '2_2_a' },
        { id: 3, name: 'Смена 2: Детейлер Б', pattern: '2_2_b' },
        { id: 4, name: 'Смена 2: Полировщик', pattern: '2_2_b' }
      ]
    },
    cleaning: {
      year: 2026,
      month: 10,
      hoursPerShift: 8,
      masters: [
        { id: 1, name: 'Бригада 1 (Жилые объекты)', pattern: '2_2_a' },
        { id: 2, name: 'Бригада 2 (Коммерческие)', pattern: '2_2_b' },
        { id: 3, name: 'Мастер выездной химчистки', pattern: '5_2' }
      ]
    }
  };

  // State
  var state = JSON.parse(JSON.stringify(PRESETS.beauty));
  // masterDays: { [masterId]: [boolean (true=work, false=rest)] }
  var masterDays = {};

  var monthSelect = app.querySelector('#mt-sh-month');
  var yearSelect = app.querySelector('#mt-sh-year');
  var hoursInput = app.querySelector('#mt-sh-hours');
  var newNameInput = app.querySelector('#mt-sh-new-name');
  var newPatternSelect = app.querySelector('#mt-sh-new-pattern');
  var addBtn = app.querySelector('#mt-sh-add-btn');
  var printBtn = app.querySelector('#mt-sh-print-btn');
  var copyBtn = app.querySelector('#mt-sh-copy-btn');
  var presetBtns = app.querySelectorAll('.mt-shifts-preset-btn');
  var tableContainer = app.querySelector('#mt-shifts-table-container');

  function getDaysInMonth(year, month) {
    return new Date(year, month + 1, 0).getDate();
  }

  function initDaysForMaster(master) {
    var totalDays = getDaysInMonth(state.year, state.month);
    var arr = [];
    for (var d = 1; d <= totalDays; d++) {
      var date = new Date(state.year, state.month, d);
      var dayOfWeek = date.getDay(); // 0=Sun, 1=Mon, ..., 6=Sat
      var isWork = false;

      if (master.pattern === '2_2_a') {
        isWork = (d % 4 === 1 || d % 4 === 2);
      } else if (master.pattern === '2_2_b') {
        isWork = (d % 4 === 3 || d % 4 === 0);
      } else if (master.pattern === '3_3_a') {
        isWork = ((d - 1) % 6 < 3);
      } else if (master.pattern === '3_3_b') {
        isWork = ((d - 1) % 6 >= 3);
      } else if (master.pattern === '5_2') {
        isWork = (dayOfWeek !== 0 && dayOfWeek !== 6);
      }
      arr.push(isWork);
    }
    masterDays[master.id] = arr;
  }

  function recomputeAllMasterDays() {
    masterDays = {};
    state.masters.forEach(function(m) {
      initDaysForMaster(m);
    });
  }

  function renderTable() {
    if (!tableContainer) return;

    var totalDays = getDaysInMonth(state.year, state.month);
    var hours = parseInt(hoursInput ? hoursInput.value : state.hoursPerShift, 10) || 10;
    state.hoursPerShift = hours;

    var html = ['<table class="mt-shifts-table"><thead><tr>'];
    html.push('<th class="mt-shifts-col-master">Сотрудник</th>');

    // Day numbers header
    for (var d = 1; d <= totalDays; d++) {
      var date = new Date(state.year, state.month, d);
      var dow = date.getDay();
      var isWknd = (dow === 0 || dow === 6);
      var wkndCls = isWknd ? ' is-weekend' : '';
      html.push('<th class="' + wkndCls + '">' + d + '<br><small>' + WEEKDAY_NAMES[dow] + '</small></th>');
    }

    html.push('<th class="mt-shifts-col-stat">Смен</th>');
    html.push('<th class="mt-shifts-col-stat">Часов</th>');
    html.push('</tr></thead><tbody>');

    // Daily coverage counter
    var coverage = new Array(totalDays).fill(0);

    // Rows
    state.masters.forEach(function(m) {
      var days = masterDays[m.id];
      if (!days || days.length !== totalDays) {
        initDaysForMaster(m);
        days = masterDays[m.id];
      }

      var workCount = 0;
      html.push('<tr>');
      html.push('<td class="mt-shifts-col-master">');
      html.push('<button type="button" class="mt-shifts-del-btn" data-del-id="' + m.id + '" title="Удалить сотрудника">✕</button>');
      html.push('<span>' + escapeHtml(m.name) + '</span>');
      html.push('</td>');

      for (var d = 0; d < totalDays; d++) {
        var isWork = days[d];
        var dateObj = new Date(state.year, state.month, d + 1);
        var isWkndCol = (dateObj.getDay() === 0 || dateObj.getDay() === 6);
        var colCls = isWkndCol ? ' mt-shifts-cell-weekend-col' : '';

        if (isWork) {
          workCount++;
          coverage[d]++;
          html.push('<td class="mt-shifts-day-cell mt-shifts-cell-work' + colCls + '" data-mid="' + m.id + '" data-day="' + d + '">Р</td>');
        } else {
          html.push('<td class="mt-shifts-day-cell mt-shifts-cell-rest' + colCls + '" data-mid="' + m.id + '" data-day="' + d + '">·</td>');
        }
      }

      var totalHours = workCount * hours;
      html.push('<td class="mt-shifts-col-stat"><strong>' + workCount + '</strong></td>');
      html.push('<td class="mt-shifts-col-stat"><strong>' + totalHours + ' ч</strong></td>');
      html.push('</tr>');
    });

    // Summary Coverage Row
    html.push('<tr class="mt-shifts-coverage-row">');
    html.push('<td class="mt-shifts-col-master">Мастеров на смене:</td>');
    for (var c = 0; c < totalDays; c++) {
      var count = coverage[c];
      var lowCls = count === 0 ? ' mt-shifts-coverage-low' : '';
      html.push('<td class="' + lowCls + '">' + count + '</td>');
    }
    html.push('<td class="mt-shifts-col-stat">—</td>');
    html.push('<td class="mt-shifts-col-stat">—</td>');
    html.push('</tr>');

    html.push('</tbody></table>');
    tableContainer.innerHTML = html.join('');

    // Attach cell click events (toggle shift)
    var cells = tableContainer.querySelectorAll('.mt-shifts-day-cell');
    for (var i = 0; i < cells.length; i++) {
      cells[i].addEventListener('click', function() {
        var mid = parseInt(this.getAttribute('data-mid'), 10);
        var dayIdx = parseInt(this.getAttribute('data-day'), 10);
        if (masterDays[mid]) {
          masterDays[mid][dayIdx] = !masterDays[mid][dayIdx];
          renderTable();
        }
      });
    }

    // Attach delete master events
    var delBtns = tableContainer.querySelectorAll('[data-del-id]');
    for (var j = 0; j < delBtns.length; j++) {
      delBtns[j].addEventListener('click', function(e) {
        e.stopPropagation();
        var delId = parseInt(this.getAttribute('data-del-id'), 10);
        state.masters = state.masters.filter(function(m) { return m.id !== delId; });
        delete masterDays[delId];
        renderTable();
      });
    }
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // Month / Year change
  if (monthSelect) {
    monthSelect.addEventListener('change', function() {
      state.month = parseInt(this.value, 10);
      recomputeAllMasterDays();
      renderTable();
    });
  }

  if (yearSelect) {
    yearSelect.addEventListener('change', function() {
      state.year = parseInt(this.value, 10);
      recomputeAllMasterDays();
      renderTable();
    });
  }

  if (hoursInput) {
    hoursInput.addEventListener('input', function() {
      renderTable();
    });
  }

  // Add Master
  if (addBtn && newNameInput && newPatternSelect) {
    addBtn.addEventListener('click', function() {
      var name = newNameInput.value.trim();
      if (!name) return;
      var newId = Date.now();
      var master = {
        id: newId,
        name: name,
        pattern: newPatternSelect.value
      };
      state.masters.push(master);
      initDaysForMaster(master);
      newNameInput.value = '';
      renderTable();
    });
  }

  // Presets
  for (var p = 0; p < presetBtns.length; p++) {
    presetBtns[p].addEventListener('click', function() {
      for (var k = 0; k < presetBtns.length; k++) presetBtns[k].classList.remove('is-active');
      this.classList.add('is-active');
      var key = this.getAttribute('data-shifts-preset');
      if (PRESETS[key]) {
        state = JSON.parse(JSON.stringify(PRESETS[key]));
        if (monthSelect) monthSelect.value = state.month;
        if (yearSelect) yearSelect.value = state.year;
        if (hoursInput) hoursInput.value = state.hoursPerShift;
        recomputeAllMasterDays();
        renderTable();
      }
    });
  }

  // Print
  if (printBtn) {
    printBtn.addEventListener('click', function() {
      window.print();
    });
  }

  // Copy to Telegram
  if (copyBtn) {
    copyBtn.addEventListener('click', function() {
      var totalDays = getDaysInMonth(state.year, state.month);
      var hours = parseInt(hoursInput ? hoursInput.value : state.hoursPerShift, 10) || 10;
      var monthLabel = MONTH_NAMES[state.month] + ' ' + state.year;

      var lines = [
        '📅 ГРАФИК СМЕН: ' + monthLabel.toUpperCase(),
        'Длительность смены: ' + hours + ' ч',
        '--------------------------------------------'
      ];

      state.masters.forEach(function(m) {
        var days = masterDays[m.id] || [];
        var workDays = [];
        for (var d = 0; d < days.length; d++) {
          if (days[d]) workDays.push(d + 1);
        }
        var totalHours = workDays.length * hours;
        lines.push('👤 ' + m.name + ':');
        lines.push('   Смены (' + workDays.length + ' смен / ' + totalHours + ' ч): ' + workDays.join(', '));
      });

      lines.push('--------------------------------------------');
      lines.push('Сформировано в генераторе графиков Молния: https://molniya-tech.ru/tools/shifts');

      var textToCopy = lines.join('\n');

      copyTextToClipboard(textToCopy).then(function() {
        if (!copyBtn.getAttribute('data-orig')) {
          copyBtn.setAttribute('data-orig', copyBtn.textContent.trim());
        }
        copyBtn.classList.add('copied');
        var btnSpan = copyBtn.querySelector('span');
        if (btnSpan) btnSpan.textContent = 'График скопирован!';
        setTimeout(function() {
          copyBtn.classList.remove('copied');
          if (btnSpan) btnSpan.textContent = copyBtn.getAttribute('data-orig') || 'Скопировать в Telegram';
        }, 2500);
      });
    });
  }

  // Initial render
  recomputeAllMasterDays();
  renderTable();
}


var _domInitialized = false;
function initApp() {
  if (_domInitialized) return;
  _domInitialized = true;
  initHeroScrollScene();
  initOverviewSplitScene();
  initModulesSplitScene();
  initJourneySteps();
  initReveal();
  initNavDropdown();
  initMobileMenu();
  initStickyCta();
  initCookieBanner();
  initIndustryFitForm();
  initLeadForm();
  initVisibilityGallery();
  initRequisitesCopy();
  initCalendarTool();
  initInnChecker();
  initMarginCalculator();
  initCarwashWeather();
  initToolRating();
  initQrGenerator();
  initSalaryCalculator();
  initPricelistConstructor();
  initAcquiringCalculator();
  initShiftsMaker();
  initFaqLock();
}

function initFaqLock() {
  var faqDetails = document.querySelectorAll('.mt-before-start-questions details');
  if (!faqDetails.length) return;
  faqDetails.forEach(function(el) {
    el.open = true;
    el.addEventListener('click', function(e) {
      if (e.target.closest('summary')) {
        e.preventDefault();
      }
    });
    el.addEventListener('toggle', function() {
      if (!el.open) el.open = true;
    });
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}
