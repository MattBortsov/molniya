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
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}
