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
        'Рассчитано на https://molniya-tech.ru/margin'
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

    var pageUrl = 'https://molniya-tech.ru/carwash-weather' + (data.city_slug !== 'custom' ? '?city=' + data.city_slug : '');
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

      var pageUrl = 'https://molniya-tech.ru/carwash-weather' + (currentData.city_slug !== 'custom' ? '?city=' + currentData.city_slug : '');
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
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}
