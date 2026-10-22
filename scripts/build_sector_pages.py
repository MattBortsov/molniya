#!/usr/bin/env python3
"""
scripts/build_sector_pages.py
Generates sector landing pages (starting with /auto) adhering to strict DRY principles.
Shares exact navigation, atmosphere, footer, and styling system across all pages.
Also synchronizes the navigation dropdown into index.html and blog/index.html.
"""

from __future__ import annotations
import html
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_HTML = ROOT_DIR / "index.html"
BLOG_INDEX_HTML = ROOT_DIR / "blog" / "index.html"
SITEMAP_XML = ROOT_DIR / "sitemap.xml"
BLOG_PY = ROOT_DIR / "api" / "blog.py"

SECTORS = [
    {
        "id": "auto",
        "slug": "auto",
        "title": "Автобизнес",
        "desc": "Автомойки, детейлинг, автосервисы, шиномонтаж",
        "icon": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/></svg>',
        "emoji": "🚗",
        "active": True,
        "badge": "Решение",
        "badge_class": "mt-dropdown-badge--active",
    },
    {
        "id": "beauty",
        "slug": "beauty",
        "title": "Красота",
        "desc": "Салоны красоты, барбершопы, ногтевые студии",
        "icon": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/><line x1="8.12" y1="8.12" x2="12" y2="12"/></svg>',
        "emoji": "✂️",
        "active": True,
        "badge": "Решение",
        "badge_class": "mt-dropdown-badge--active",
    },
    {
        "id": "health",
        "slug": "health",
        "title": "Здоровье",
        "desc": "Клиники, массаж, частные кабинеты, спа",
        "icon": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="M12 9v4"/><path d="M10 11h4"/></svg>',
        "emoji": "🩺",
        "active": True,
        "badge": "Решение",
        "badge_class": "mt-dropdown-badge--active",
    },
    {
        "id": "spaces",
        "slug": "spaces",
        "title": "Аренда пространств",
        "desc": "Коворкинги, спортивные площадки, залы, лофты",
        "icon": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M7 3v4M17 3v4M3 10h18M8 15h3M15 15h1"/></svg>',
        "emoji": "🏟️",
        "active": True,
        "badge": "Решение",
        "badge_class": "mt-dropdown-badge--active",
    },
    {
        "id": "photostudios",
        "slug": "photostudios",
        "title": "Фотостудии",
        "desc": "Интерьерные студии, циклорамы, видеопавильоны, гримерки",
        "icon": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg>',
        "emoji": "📸",
        "active": True,
        "badge": "Решение",
        "badge_class": "mt-dropdown-badge--active",
    },
    {
        "id": "cleaning",
        "slug": "cleaning",
        "title": "Клининг",
        "desc": "Уборка квартир и офисов, химчистка мебели, мойка окон",
        "icon": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/><path d="M5 3v4M3 5h4M19 17v4M17 19h4"/></svg>',
        "emoji": "✨",
        "active": True,
        "badge": "Решение",
        "badge_class": "mt-dropdown-badge--active",
    },
    {
        "id": "education",
        "slug": "education",
        "title": "Образование",
        "desc": "Курсы, студии танцев, языковые школы, секции",
        "icon": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>',
        "emoji": "🎓",
        "active": True,
        "badge": "Решение",
        "badge_class": "mt-dropdown-badge--active",
    },
    {
        "id": "pets",
        "slug": "pets",
        "title": "Груминг-салоны",
        "desc": "Запись к грумерам, карточки питомцев, расписание",
        "icon": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="4" r="2"/><circle cx="18" cy="8" r="2"/><circle cx="4" cy="11" r="2"/><circle cx="7" cy="19" r="2"/><path d="M12 10a4 4 0 0 0-4 4c0 2.2 1.8 4 4 4s4-1.8 4-4a4 4 0 0 0-4-4z"/></svg>',
        "emoji": "🐾",
        "active": True,
        "badge": "Решение",
        "badge_class": "mt-dropdown-badge--active",
    },
    {
        "id": "repair",
        "slug": "repair",
        "title": "Ремонт и сервис",
        "desc": "Сервисные центры, ремонт техники, ателье",
        "icon": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="2" width="12" height="20" rx="2"/><path d="M10 5h4M11 19h2M13 8l-3 3 3 2-4 4 2 2"/></svg>',
        "mobile_icon": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="2" width="12" height="20" rx="2"/><path d="M10 5h4M11 19h2M13 8l-3 3 3 2-4 4 2 2"/></svg>',
        "emoji": "🛠️",
        "active": True,
        "badge": "Решение",
        "badge_class": "mt-dropdown-badge--active",
    },
]

BRAND_MARK_SVG = '<svg width="56" height="56" viewBox="0 0 96 96" fill="none" aria-hidden="true"><circle cx="48" cy="48" r="11" fill="none" stroke="#131B2C" stroke-width="8"/><g transform="rotate(0 48 48)"><rect x="41.5" y="6" width="13" height="22" rx="6.5" fill="#131B2C"/></g><g transform="rotate(60 48 48)"><rect x="41.5" y="6" width="13" height="22" rx="6.5" fill="#DF5F3C"/></g><g transform="rotate(120 48 48)"><rect x="41.5" y="6" width="13" height="22" rx="6.5" fill="#131B2C"/></g><g transform="rotate(180 48 48)"><rect x="41.5" y="6" width="13" height="22" rx="6.5" fill="#131B2C"/></g><g transform="rotate(240 48 48)"><rect x="41.5" y="6" width="13" height="22" rx="6.5" fill="#131B2C"/></g><g transform="rotate(300 48 48)"><rect x="41.5" y="6" width="13" height="22" rx="6.5" fill="#131B2C"/></g></svg>'


def render_nav_html(active_item: str = "", asset_prefix: str = "", beta_cta: bool = False) -> str:
    """Builds the single source of truth for navigation across all pages."""
    logo_path = f"{asset_prefix}assets/img/logo/molniya-logo-horizontal.svg" if asset_prefix else "/assets/img/logo/molniya-logo-horizontal.svg"

    # Build dropdown grid
    grid_items = []
    mobile_items = []
    for s in SECTORS:
        href = f"/{s['slug']}"
        active_cls = " mt-dropdown-card--active" if s["slug"] == active_item else ""
        card_tag = "a" if s["active"] else "div"
        card_attrs = f' href="{href}" role="menuitem"' if s["active"] else ' aria-disabled="true"'
        soon_cls = "" if s["active"] else " mt-dropdown-card--soon"
        badge = "" if s["active"] else f'<span class="mt-dropdown-badge {s["badge_class"]}">{html.escape(s["badge"])}</span>'
        grid_items.append(f'''              <{card_tag} class="mt-dropdown-card{active_cls}{soon_cls}"{card_attrs}>
                <div class="mt-dropdown-icon">{s["icon"]}</div>
                <div class="mt-dropdown-info">
                  <div class="mt-dropdown-title">{html.escape(s["title"])}{badge}</div>
                  <div class="mt-dropdown-desc">{html.escape(s["desc"])}</div>
                </div>
              </{card_tag}>''')

        m_highlight = " mt-mobile-sublink--highlight" if s["slug"] == active_item else ""
        mobile_tag = "a" if s["active"] else "div"
        mobile_attrs = f' href="{href}"' if s["active"] else ' aria-disabled="true"'
        mobile_icon = s.get("mobile_icon", s["emoji"])
        mobile_desc = s["desc"] if s["active"] else f'Скоро · {s["desc"]}'
        mobile_items.append(f'''            <{mobile_tag} class="mt-mobile-sublink{m_highlight}"{mobile_attrs}>
              <span class="mt-mobile-sublink-icon">{mobile_icon}</span>
              <span class="mt-mobile-sublink-info">
                <strong>{html.escape(s["title"])}</strong>
                <small>{html.escape(mobile_desc)}</small>
              </span>
            </{mobile_tag}>''')

    cards_markup = "\n".join(grid_items)
    mobile_markup = "\n".join(mobile_items)

    blog_active = ' aria-current="page"' if active_item == "blog" else ''
    pricing_active = ' aria-current="page"' if active_item == "pricing" else ''
    about_active = ' aria-current="page"' if active_item == "about" else ''
    cta_href = "/#beta" if beta_cta else "https://t.me/molniya_tex"
    cta_attrs = "" if beta_cta else ' target="_blank" rel="noopener"'
    cta_label = "Бета-тест" if beta_cta else "Подписаться"
    cta_mobile_label = "Участвовать в бета-тесте" if beta_cta else "Подписаться в мессенджере"
    cta_nav_icon = ('<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                    '<path d="M5 12h14m-6-6 6 6-6 6"/></svg>' if beta_cta else
                    '<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>')
    cta_mobile_icon = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                       'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                       '<path d="M5 12h14m-6-6 6 6-6 6"/></svg>' if beta_cta else
                       '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>')

    return f'''      <!-- NAV -->
      <nav class="mt-nav">
        <div class="mt-nav-inner">
          <a class="mt-brand" href="/">
            <img class="mt-brand-logo" src="{logo_path}" width="327" height="96" alt="Молния Тех">
          </a>

          <ul class="mt-nav-links">
            <li class="mt-nav-item mt-nav-item--dropdown">
              <button class="mt-nav-link mt-nav-link--dropdown" type="button" aria-expanded="false" aria-haspopup="true">
                Для кого
                <svg class="mt-nav-chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>
              </button>
              <div class="mt-dropdown-menu" role="menu">
                <div class="mt-dropdown-grid">
{cards_markup}
                </div>
                <div class="mt-dropdown-footer">
                  <div class="mt-dropdown-footer-text">
                    <span class="mt-dropdown-footer-icon">⚡</span>
                    <span>Не нашли свою сферу? Молния гибко адаптируется под любой бизнес</span>
                  </div>
                  <a class="mt-dropdown-footer-link" href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в мессенджер →</a>
                </div>
              </div>
            </li>
            <li><a class="mt-nav-link" href="/#how-it-works">Как это работает</a></li>
            <li><a class="mt-nav-link" href="/#features">Функции</a></li>
            <li><a class="mt-nav-link" href="/pricing"{pricing_active}>Тарифы</a></li>
            <li><a class="mt-nav-link" href="/about"{about_active}>О компании</a></li>
            <li><a class="mt-nav-link" href="/blog"{blog_active}>Блог</a></li>
          </ul>

          <a class="mt-btn mt-btn-nav" href="{cta_href}"{cta_attrs}>
            {cta_nav_icon}
            {cta_label}
          </a>

          <button class="mt-nav-burger" type="button" aria-label="Открыть меню" aria-expanded="false" aria-controls="mt-mobile-menu">
            <span></span><span></span><span></span>
          </button>
        </div>

        <div id="mt-mobile-menu" class="mt-mobile-menu">
          <div class="mt-mobile-accordion">
            <button class="mt-mobile-accordion-btn" type="button" aria-expanded="false">
              <span>Для кого</span>
              <svg class="mt-nav-chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>
            </button>
            <div class="mt-mobile-accordion-body">
{mobile_markup}
            </div>
          </div>
          <a class="mt-mobile-link" href="/#how-it-works">Как это работает</a>
          <a class="mt-mobile-link" href="/#features">Функции</a>
          <a class="mt-mobile-link" href="/pricing">Тарифы</a>
          <a class="mt-mobile-link" href="/about">О компании</a>
          <a class="mt-mobile-link" href="/blog">Блог</a>
          <a class="mt-btn mt-btn-hero mt-mobile-cta" href="{cta_href}"{cta_attrs}>
            {cta_mobile_icon}
            {cta_mobile_label}
          </a>
        </div>
      </nav>'''


def render_sticky_cta_html() -> str:
    """Render the sticky floating CTA button across all pages."""
    return '''    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>'''


def render_footer_nav_html() -> str:
    """Link the footer to published sections and active sector pages."""
    sector_links = "\n".join(
        f'              <a class="mt-footer-link" href="/{html.escape(sector["slug"], quote=True)}">{html.escape(sector["title"])}</a>'
        for sector in SECTORS if sector["active"]
    )
    return f'''          <nav class="mt-footer-nav" aria-label="Разделы сайта">
            <div class="mt-footer-nav-group">
              <h3>Для кого</h3>
{sector_links}
            </div>
            <div class="mt-footer-nav-group">
              <h3>Компания</h3>
              <a class="mt-footer-link" href="/#how-it-works">Как это работает</a>
              <a class="mt-footer-link" href="/#features">Функции</a>
              <a class="mt-footer-link" href="/pricing">Тарифы</a>
              <a class="mt-footer-link" href="/about">О компании</a>
              <a class="mt-footer-link" href="/#beta">Бета-тестирование</a>
              <a class="mt-footer-link" href="/blog">Блог</a>
            </div>
            <div class="mt-footer-nav-group">
              <h3>Информация</h3>
              <a class="mt-footer-link" href="/requisites">Реквизиты</a>
              <a class="mt-footer-link" href="/privacy">Конфиденциальность</a>
            </div>
            <div class="mt-footer-nav-group">
              <h3>Контакты</h3>
              <a class="mt-footer-link mt-footer-contact-item" href="tel:+78127242124">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2a1 1 0 011.02-.24c1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
                <span>8 (812) 724-21-24</span>
              </a>
              <a class="mt-footer-link mt-footer-contact-item" href="mailto:info@molniya-tech.ru">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
                <span>info@molniya-tech.ru</span>
              </a>
              <div class="mt-footer-socials" aria-label="Социальные сети">
                <a class="mt-footer-social-btn" href="https://t.me/molniya_tex" target="_blank" rel="noopener" aria-label="Telegram" title="Telegram @molniya_tex">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
                </a>
                <a class="mt-footer-social-btn" href="https://www.linkedin.com/company/molniya-tech" target="_blank" rel="noopener" aria-label="LinkedIn" title="LinkedIn">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 8.76a1.68 1.68 0 0 0 0-3.36 1.68 1.68 0 0 0 0 3.36m1.39 9.74v-8.37H5.07v8.37z"/></svg>
                </a>
              </div>
            </div>
          </nav>'''


def render_footer_html(asset_prefix: str = "", home_variant: bool = False, dikidi_variant: bool = False, yclients_variant: bool = False, pricing_variant: bool = False) -> str:
    footer_nav_html = render_footer_nav_html()
    if pricing_variant:
        return f'''      <!-- FOOTER -->
      <footer class="mt-footer mt-footer--home" id="contact" aria-labelledby="contact-title">
        <div class="mt-footer-showcase">
          <div class="mt-footer-intro">
            <div class="mt-footer-signup">
              <h2 id="contact-title">Подключите Молнию <em>на выгодных условиях</em></h2>
              <form class="mt-lead-form mt-footer-beta-form" data-lead-form data-lead-source="pricing">
                <div class="mt-lead-fields">
                  <label class="mt-lead-field" for="pricing-name">Имя<input id="pricing-name" name="name" type="text" autocomplete="name" minlength="2" maxlength="80" placeholder="Как к вам обращаться" required></label>
                  <label class="mt-lead-field" for="pricing-phone">Телефон<input id="pricing-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="32" placeholder="+7 999 123-45-67" required></label>
                  <label class="mt-lead-field" for="pricing-email">Почта<input id="pricing-email" name="email" type="email" autocomplete="email" maxlength="254" placeholder="name@example.com" required></label>
                </div>
                <div class="mt-lead-honeypot" aria-hidden="true"><label for="pricing-website">Сайт</label><input id="pricing-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
                <label class="mt-lead-consent"><input name="consent" type="checkbox" required><span>Я даю своё согласие на обработку персональных данных в соответствии с <a href="/privacy" target="_blank" rel="noopener">политикой конфиденциальности</a>.</span></label>
                <button class="mt-btn mt-btn-cta mt-lead-submit" type="submit">Подключить бесплатно</button>
                <p class="mt-lead-status" data-lead-status role="status" aria-live="polite"></p>
              </form>
            </div>
            <div class="mt-footer-process">
              <p class="mt-footer-process-intro">14 дней бесплатного доступа. Бесплатно перенесём базу из любой системы за 15 минут.</p>
              <ol>
                <li><span>01</span><div><strong>Быстрый старт за 15 минут</strong><p>Поможем настроить услуги, графики мастеров и онлайн-запись.</p></div></li>
                <li><span>02</span><div><strong>14 дней без оплаты</strong><p>Тестируйте тариф «Бизнес» в реальной работе без ограничений и без ввода карты.</p></div></li>
                <li><span>03</span><div><strong>Экономия с первого дня</strong><p>Бесплатные Боты в мессенджерах вместо SMS и никаких доплат за каждого нового мастера.</p></div></li>
              </ol>
            </div>
          </div>
          <div class="mt-footer-gallery" aria-label="Молния в работе сервисного бизнеса">
            <figure class="mt-footer-photo">
              <img src="/assets/img/footer/booking.webp" alt="Администратор встречает клиента и проверяет запись на планшете" width="1536" height="1024" loading="lazy" decoding="async">
              <figcaption><span>01 / Запись</span><strong>Простая Онлайн-запись</strong></figcaption>
            </figure>
            <figure class="mt-footer-photo">
              <img src="/assets/img/footer/team-auto.webp" alt="Команда сервиса сверяет рабочее расписание на планшете" width="1536" height="1024" loading="lazy" decoding="async">
              <figcaption><span>02 / Команда</span><strong>Ясная загрузка дня</strong></figcaption>
            </figure>
            <figure class="mt-footer-photo">
              <img src="/assets/img/footer/insights-studio.webp" alt="Владелица студии занятий просматривает рабочие показатели за ноутбуком" width="1536" height="1024" loading="lazy" decoding="async">
              <figcaption><span>03 / Показатели</span><strong>Данные для роста</strong></figcaption>
            </figure>
          </div>
        </div>
        <div class="mt-footer-inner">
          <div class="mt-footer-brand-col">
            <div class="mt-footer-brand">
              <img class="mt-footer-brand-logo" src="/assets/img/logo/molniya-logo-horizontal-white.svg" width="327" height="96" alt="Молния Тех">
            </div>
            <p class="mt-footer-sub">Заряжает ваш бизнес на генерацию заработка</p>
            <p class="mt-footer-legal">ООО «МОЛНИЯ ТЕХ» · ИНН 7806637461 · ОГРН 1267800068458 · Санкт-Петербург</p>
          </div>
{footer_nav_html}
        </div>
        <div class="mt-footer-bottom">
          <p class="mt-footer-copy">© 2026 ООО «МОЛНИЯ ТЕХ»</p>
        </div>
      </footer>'''
    if yclients_variant:
        return f'''      <!-- FOOTER -->
      <footer class="mt-footer mt-footer--home" id="contact" aria-labelledby="contact-title">
        <div class="mt-footer-showcase">
          <div class="mt-footer-intro">
            <div class="mt-footer-signup">
              <h2 id="contact-title">Получите 3 месяца бесплатно <em>при переходе с YCLIENTS</em></h2>
              <form class="mt-lead-form mt-footer-beta-form" data-lead-form data-lead-source="yclients">
                <div class="mt-lead-fields">
                  <label class="mt-lead-field" for="yclients-name">Имя<input id="yclients-name" name="name" type="text" autocomplete="name" minlength="2" maxlength="80" placeholder="Как к вам обращаться" required></label>
                  <label class="mt-lead-field" for="yclients-phone">Телефон<input id="yclients-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="32" placeholder="+7 999 123-45-67" required></label>
                  <label class="mt-lead-field" for="yclients-email">Почта<input id="yclients-email" name="email" type="email" autocomplete="email" maxlength="254" placeholder="name@example.com" required></label>
                </div>
                <div class="mt-lead-honeypot" aria-hidden="true"><label for="yclients-website">Сайт</label><input id="yclients-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
                <label class="mt-lead-consent"><input name="consent" type="checkbox" required><span>Я даю своё согласие на обработку персональных данных в соответствии с <a href="/privacy" target="_blank" rel="noopener">политикой конфиденциальности</a>.</span></label>
                <button class="mt-btn mt-btn-cta mt-lead-submit" type="submit">Получить 3 месяца бесплатно</button>
                <p class="mt-lead-status" data-lead-status role="status" aria-live="polite"></p>
              </form>
            </div>
            <div class="mt-footer-process">
              <p class="mt-footer-process-intro">Бесплатно перенесём базу из YCLIENTS и настроим Молнию под ваш бизнес за 15 минут.</p>
              <ol>
                <li><span>01</span><div><strong>Выгрузка из YCLIENTS</strong><p>Экспортируйте базу клиентов, историю и прайс в Excel/CSV в 2 клика.</p></div></li>
                <li><span>02</span><div><strong>Служба заботы переносит всё за вас</strong><p>Бережно импортируем базу без пауз в приёме клиентов и потери данных.</p></div></li>
                <li><span>03</span><div><strong>3 месяца бесплатно</strong><p>Работайте на максимальном тарифе без ограничений и экономьте на SMS с первого дня.</p></div></li>
              </ol>
            </div>
          </div>
          <div class="mt-footer-gallery" aria-label="Молния в работе сервисного бизнеса">
            <figure class="mt-footer-photo">
              <img src="/assets/img/footer/booking.webp" alt="Администратор встречает клиента и проверяет запись на планшете" width="1536" height="1024" loading="lazy" decoding="async">
              <figcaption><span>01 / Запись</span><strong>Простая Онлайн-запись</strong></figcaption>
            </figure>
            <figure class="mt-footer-photo">
              <img src="/assets/img/footer/team-auto.webp" alt="Команда сервиса сверяет рабочее расписание на планшете" width="1536" height="1024" loading="lazy" decoding="async">
              <figcaption><span>02 / Команда</span><strong>Ясная загрузка дня</strong></figcaption>
            </figure>
            <figure class="mt-footer-photo">
              <img src="/assets/img/footer/insights-studio.webp" alt="Владелица студии занятий просматривает рабочие показатели за ноутбуком" width="1536" height="1024" loading="lazy" decoding="async">
              <figcaption><span>03 / Показатели</span><strong>Данные для роста</strong></figcaption>
            </figure>
          </div>
        </div>
        <div class="mt-footer-inner">
          <div class="mt-footer-brand-col">
            <div class="mt-footer-brand">
              <img class="mt-footer-brand-logo" src="/assets/img/logo/molniya-logo-horizontal-white.svg" width="327" height="96" alt="Молния Тех">
            </div>
            <p class="mt-footer-sub">Заряжает ваш бизнес на генерацию заработка</p>
            <p class="mt-footer-legal">ООО «МОЛНИЯ ТЕХ» · ИНН 7806637461 · ОГРН 1267800068458 · Санкт-Петербург</p>
          </div>
{footer_nav_html}
        </div>
        <div class="mt-footer-bottom">
          <p class="mt-footer-copy">© 2026 ООО «МОЛНИЯ ТЕХ»</p>
        </div>
      </footer>'''
    if dikidi_variant:
        return f'''      <!-- FOOTER -->
      <footer class="mt-footer mt-footer--home" id="contact" aria-labelledby="contact-title">
        <div class="mt-footer-showcase">
          <div class="mt-footer-intro">
            <div class="mt-footer-signup">
              <h2 id="contact-title">Получите 3 месяца бесплатно <em>при переходе с DIKIDI</em></h2>
              <form class="mt-lead-form mt-footer-beta-form" data-lead-form data-lead-source="dikidi">
                <div class="mt-lead-fields">
                  <label class="mt-lead-field" for="dikidi-name">Имя<input id="dikidi-name" name="name" type="text" autocomplete="name" minlength="2" maxlength="80" placeholder="Как к вам обращаться" required></label>
                  <label class="mt-lead-field" for="dikidi-phone">Телефон<input id="dikidi-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="32" placeholder="+7 999 123-45-67" required></label>
                  <label class="mt-lead-field" for="dikidi-email">Почта<input id="dikidi-email" name="email" type="email" autocomplete="email" maxlength="254" placeholder="name@example.com" required></label>
                </div>
                <div class="mt-lead-honeypot" aria-hidden="true"><label for="dikidi-website">Сайт</label><input id="dikidi-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
                <label class="mt-lead-consent"><input name="consent" type="checkbox" required><span>Я даю своё согласие на обработку персональных данных в соответствии с <a href="/privacy" target="_blank" rel="noopener">политикой конфиденциальности</a>.</span></label>
                <button class="mt-btn mt-btn-cta mt-lead-submit" type="submit">Получить 3 месяца бесплатно</button>
                <p class="mt-lead-status" data-lead-status role="status" aria-live="polite"></p>
              </form>
            </div>
            <div class="mt-footer-process">
              <p class="mt-footer-process-intro">Бесплатно перенесём базу из DIKIDI и настроим Молнию под ваш бизнес за 15 минут.</p>
              <ol>
                <li><span>01</span><div><strong>Выгрузка из DIKIDI</strong><p>Скачайте базу клиентов, историю и прайс в Excel в 1 клик.</p></div></li>
                <li><span>02</span><div><strong>Служба заботы переносит всё за вас</strong><p>Бережно импортируем базу без пауз в приёме клиентов и потери данных.</p></div></li>
                <li><span>03</span><div><strong>3 месяца бесплатно</strong><p>Работайте на максимальном тарифе без ограничений и экономьте на SMS с первого дня.</p></div></li>
              </ol>
            </div>
          </div>
          <div class="mt-footer-gallery" aria-label="Молния в работе сервисного бизнеса">
            <figure class="mt-footer-photo">
              <img src="/assets/img/footer/booking.webp" alt="Администратор встречает клиента и проверяет запись на планшете" width="1536" height="1024" loading="lazy" decoding="async">
              <figcaption><span>01 / Запись</span><strong>Простая Онлайн-запись</strong></figcaption>
            </figure>
            <figure class="mt-footer-photo">
              <img src="/assets/img/footer/team-auto.webp" alt="Команда сервиса сверяет рабочее расписание на планшете" width="1536" height="1024" loading="lazy" decoding="async">
              <figcaption><span>02 / Команда</span><strong>Ясная загрузка дня</strong></figcaption>
            </figure>
            <figure class="mt-footer-photo">
              <img src="/assets/img/footer/insights-studio.webp" alt="Владелица студии занятий просматривает рабочие показатели за ноутбуком" width="1536" height="1024" loading="lazy" decoding="async">
              <figcaption><span>03 / Показатели</span><strong>Данные для роста</strong></figcaption>
            </figure>
          </div>
        </div>
        <div class="mt-footer-inner">
          <div class="mt-footer-brand-col">
            <div class="mt-footer-brand">
              <img class="mt-footer-brand-logo" src="/assets/img/logo/molniya-logo-horizontal-white.svg" width="327" height="96" alt="Молния Тех">
            </div>
            <p class="mt-footer-sub">Заряжает ваш бизнес на генерацию заработка</p>
            <p class="mt-footer-legal">ООО «МОЛНИЯ ТЕХ» · ИНН 7806637461 · ОГРН 1267800068458 · Санкт-Петербург</p>
          </div>
{footer_nav_html}
        </div>
        <div class="mt-footer-bottom">
          <p class="mt-footer-copy">© 2026 ООО «МОЛНИЯ ТЕХ»</p>
        </div>
      </footer>'''
    if home_variant:
        return f'''      <!-- FOOTER -->
      <footer class="mt-footer mt-footer--home" id="beta" aria-labelledby="beta-title">
        <div class="mt-footer-showcase">
          <div class="mt-footer-intro">
            <div class="mt-footer-signup">
              <h2 id="beta-title">Попробуйте Молнию <em>в своём бизнесе</em></h2>
              <form class="mt-lead-form mt-footer-beta-form" data-lead-form data-lead-source="beta">
                <div class="mt-lead-fields">
                  <label class="mt-lead-field" for="beta-name">Имя<input id="beta-name" name="name" type="text" autocomplete="name" minlength="2" maxlength="80" placeholder="Как к вам обращаться" required></label>
                  <label class="mt-lead-field" for="beta-phone">Телефон<input id="beta-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="32" placeholder="+7 999 123-45-67" required></label>
                  <label class="mt-lead-field" for="beta-email">Почта<input id="beta-email" name="email" type="email" autocomplete="email" maxlength="254" placeholder="name@example.com" required></label>
                </div>
                <div class="mt-lead-honeypot" aria-hidden="true"><label for="beta-website">Сайт</label><input id="beta-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
                <label class="mt-lead-consent"><input name="consent" type="checkbox" required><span>Я даю своё согласие на обработку персональных данных в соответствии с <a href="/privacy" target="_blank" rel="noopener">политикой конфиденциальности</a>.</span></label>
                <button class="mt-btn mt-btn-cta mt-lead-submit" type="submit">Подать заявку на бета-тестирование</button>
                <p class="mt-lead-status" data-lead-status role="status" aria-live="polite"></p>
              </form>
            </div>
            <div class="mt-footer-process">
              <p class="mt-footer-process-intro">Дадим тестовый доступ, проведём демонстрацию и поможем настроить Молнию.</p>
              <ol>
                <li><span>01</span><div><strong>Начинаем вместе</strong><p>Покажем продукт и поможем настроить его под ваши задачи.</p></div></li>
                <li><span>02</span><div><strong>Вы работаете — мы слушаем</strong><p>Пользуйтесь Молнией в реальной работе. Мы изучаем технические логи и созваниваемся 1–2 раза в неделю на 15–30 минут: что удобно, что мешает, чего не хватает.</p></div></li>
                <li><span>03</span><div><strong>Помогаем и улучшаем</strong><p>Отвечаем на вопросы, исправляем ошибки и даём небольшой бонус за найденные баги.</p></div></li>
              </ol>
            </div>
          </div>
          <div class="mt-footer-gallery" aria-label="Молния в работе сервисного бизнеса">
            <figure class="mt-footer-photo">
              <img src="/assets/img/footer/booking.webp" alt="Администратор встречает клиента и проверяет запись на планшете" width="1536" height="1024" loading="lazy" decoding="async">
              <figcaption><span>01 / Запись</span><strong>Простая Онлайн-запись</strong></figcaption>
            </figure>
            <figure class="mt-footer-photo">
              <img src="/assets/img/footer/team-auto.webp" alt="Команда автосервиса сверяет рабочее расписание на планшете" width="1536" height="1024" loading="lazy" decoding="async">
              <figcaption><span>02 / Команда</span><strong>Ясная загрузка дня</strong></figcaption>
            </figure>
            <figure class="mt-footer-photo">
              <img src="/assets/img/footer/insights-studio.webp" alt="Владелица студии занятий просматривает рабочие показатели за ноутбуком" width="1536" height="1024" loading="lazy" decoding="async">
              <figcaption><span>03 / Показатели</span><strong>Данные для роста</strong></figcaption>
            </figure>
          </div>
        </div>
        <div class="mt-footer-inner">
          <div class="mt-footer-brand-col">
            <div class="mt-footer-brand">
              <img class="mt-footer-brand-logo" src="/assets/img/logo/molniya-logo-horizontal-white.svg" width="327" height="96" alt="Молния Тех">
            </div>
            <p class="mt-footer-sub">Заряжает ваш бизнес на генерацию заработка</p>
            <p class="mt-footer-legal">ООО «МОЛНИЯ ТЕХ» · ИНН 7806637461 · ОГРН 1267800068458 · Санкт-Петербург</p>
          </div>
{footer_nav_html}
        </div>
        <div class="mt-footer-bottom">
          <p class="mt-footer-copy">© 2026 ООО «МОЛНИЯ ТЕХ»</p>
        </div>
      </footer>'''
    logo_path = f"{asset_prefix}assets/img/logo/molniya-logo-horizontal.svg" if asset_prefix else "/assets/img/logo/molniya-logo-horizontal.svg"
    return f'''      <!-- FOOTER -->
      <footer class="mt-footer">
        <div class="mt-footer-inner">
          <div class="mt-footer-brand-col">
            <div class="mt-footer-brand">
              <img class="mt-footer-brand-logo" src="{logo_path}" width="327" height="96" alt="Молния Тех">
            </div>
            <p class="mt-footer-sub">Заряжает ваш бизнес на генерацию заработка</p>
            <p class="mt-footer-legal">ООО «МОЛНИЯ ТЕХ» · ИНН 7806637461 · ОГРН 1267800068458 · Санкт-Петербург</p>
          </div>
{footer_nav_html}
        </div>
        <div class="mt-footer-bottom">
          <p class="mt-footer-copy">© 2026 ООО «МОЛНИЯ ТЕХ»</p>
        </div>
      </footer>'''


def render_lead_form_html(source: str, title_html: str, description: str) -> str:
    """Render the same contact form on every product landing page."""
    source = html.escape(source, quote=True)
    description = html.escape(description)
    return f'''      <!-- LEAD FORM -->
      <section class="mt-section mt-section--lead mt-reveal" id="contact" data-screen-label="Бесплатный доступ" data-mt-reveal>
        <div class="mt-lead">
          <h2 class="mt-lead-title">{title_html}</h2>
          <p class="mt-lead-sub">{description}</p>
          <form class="mt-lead-form" data-lead-form data-lead-source="{source}">
            <div class="mt-lead-fields">
              <label class="mt-lead-field" for="lead-name">Имя<input id="lead-name" name="name" type="text" autocomplete="name" minlength="2" maxlength="80" placeholder="Как к вам обращаться" required></label>
              <label class="mt-lead-field" for="lead-email">Почта<input id="lead-email" name="email" type="email" autocomplete="email" maxlength="254" placeholder="name@example.com" required></label>
              <label class="mt-lead-field" for="lead-phone">Телефон<input id="lead-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="32" placeholder="+7 999 123-45-67" required></label>
            </div>
            <div class="mt-lead-honeypot" aria-hidden="true"><label for="lead-website">Сайт</label><input id="lead-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
            <label class="mt-lead-consent"><input name="consent" type="checkbox" required><span>Я даю своё согласие на обработку персональных данных в соответствии с <a href="/privacy" target="_blank" rel="noopener">политикой конфиденциальности</a>.</span></label>
            <button class="mt-btn mt-btn-cta mt-lead-submit" type="submit">Получить бесплатный доступ</button>
            <p class="mt-lead-status" data-lead-status role="status" aria-live="polite"></p>
          </form>
        </div>
      </section>'''


def build_auto_page() -> str:
    """Builds the complete auto landing page matching the exact design system."""
    nav_html = render_nav_html(active_item="auto", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")
    lead_html = render_lead_form_html(
        "auto",
        'Получите <span class="mt-hero-accent">бесплатный доступ навсегда</span> для автобизнеса',
        "Оставьте контакты — поможем запустить Молнию для автомойки, детейлинга или автосервиса.",
    )

    title = "Программа для автомойки: CRM и онлайн-запись | Молния"
    description = "Молния — программа и CRM для автомойки: онлайн-запись клиентов, расписание боксов, учёт услуг и зарплат сотрудников. Подходит для детейлинг-студий."
    canonical = "https://molniya-tech.ru/auto"

    faq_items = [
        {
            "q": "Подходит ли программа для небольшой автомойки на 2–3 бокса или компактного СТО?",
            "a": "Да. Молния одинаково эффективна как для компактных автомоек на 2 поста, так и для крупных детейлинг-центров и СТО с десятками постов и мастеров. Вы настраиваете количество боксов, перечень услуг и нормативы за 15 минут."
        },
        {
            "q": "Как программа учитывает класс автомобиля (седан, кроссовер, внедорожник)?",
            "a": "В Молнии встроен классификатор автомобилей. Вы один раз привязываете длительность и цену услуги к категории авто (седан, кроссовер, рамный джип, микроавтобус). При онлайн-записи система автоматически бронирует в расписании бокса нужное окно."
        },
        {
            "q": "Как рассчитывается сдельная зарплата автомойщиков, детейлеров и механиков?",
            "a": "В карточке каждого сотрудника настраивается персональная схема: процент от чека (например, мойка 30%, полировка 40%), фиксированная ставка за операцию или нормочасы. После выдачи авто выработка начисляется мгновенно на баланс смены."
        },
        {
            "q": "Как работает электронный заказ-наряд и фотоосмотр повреждений кузова?",
            "a": "Мастер открывает электронный заказ-наряд на смартфоне или планшете перед заездом авто, делает фото царапин, сколов и уровня топлива и сохраняет в карточке заказа. Это надёжная защита от необоснованных претензий клиентов при выдаче."
        },
        {
            "q": "Как клиенты записываются на автомойку и получают уведомления в мессенджере?",
            "a": "Клиенты записываются онлайн через виджет на сайте, по ссылке в соцсетях или QR-коду. Сервисный бот в мессенджере автоматически присылает подтверждение бронирования, напоминание за 2 часа до визита и оповещение «Ваш автомобиль готов к выдаче» со ссылкой на чек."
        },
        {
            "q": "Подходит ли программа для шиномонтажа в период сезонного ажиотажа?",
            "a": "Да, Молния идеально справляется с пиковыми сезонными нагрузками шиномонтажа: плотная запись без накладок, учет диаметра колес (R15–R22), сезонное хранение шин и оперативное распределение авто по постам переобувки."
        },
        {
            "q": "Как бесплатно перенести базу клиентов и историю авто из другой программы или Excel?",
            "a": "Наша служба заботы бесплатно помогает импортировать базу клиентов, историю визитов, прайс-лист и автомобили при подключении. Вы начинаете работу без остановки сервиса и потери постоянных клиентов."
        }
    ]

    faq_html = "\n".join(
        f'            <details><summary>{html.escape(item["q"])}</summary><p>{html.escape(item["a"])}</p></details>'
        for item in faq_items
    )

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Молния — CRM для автомойки",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web, iOS, Android",
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "RUB"
            },
            "description": description,
            "url": canonical
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Главная",
                    "item": "https://molniya-tech.ru/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Для кого",
                    "item": "https://molniya-tech.ru/#origin"
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": "Автобизнес",
                    "item": canonical
                }
            ]
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item["q"],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": item["a"]
                    }
                }
                for item in faq_items
            ]
        }
    ]

    json_ld_str = json.dumps(json_ld, ensure_ascii=False).replace("<", "\\u003c")

    page_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="{canonical}">
  <meta name="theme-color" content="#FFFEFD">

  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- HERO -->
      <section class="mt-hero" data-screen-label="Герой" data-mt-hero-scene>

        <div class="mt-hero-lead">
          <h1 class="mt-hero-title">
            CRM для автомойки,<br><span class="mt-hero-accent">детейлинга и автосервиса</span>
          </h1>

          <div class="mt-hero-bottom">
            <div class="mt-hero-intro">
              <p class="mt-hero-sub">Онлайн-запись, расписание, электронные заказ-наряды и прозрачный расчет зарплат</p>
              <a class="mt-btn mt-btn-hero" href="#contact">Получить бесплатный доступ</a>
            </div>

            <ul class="mt-facets mt-facets--full" aria-label="Преимущества для автобизнеса">
              <li class="mt-facet">
                <span class="mt-facet-name">Боксы и посты</span>
                <span class="mt-facet-note">онлайн-запись и учет габаритов авто</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Сдельная оплата</span>
                <span class="mt-facet-note">нормочасы и % от чека за смену</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Электронный заказ-наряд</span>
                <span class="mt-facet-note">фотофиксация дефектов до заезда</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name mt-facet-name--soon">AI & Сезон</span>
                <span class="mt-facet-note">прогноз очередей и динамический прайс</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <div class="mt-tablet">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для автомойки и автосервиса: расписание боксов и электронный журнал записи" width="1710" height="983" fetchpriority="high">
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </div>
            <p class="mt-hero-media-caption">Электронный журнал записи и загрузка боксов автомойки в реальном времени</p>
          </div>
        </div>

      </section>

      <!-- LIVE BAYS STATUS -->
      <section class="mt-section mt-reveal" data-screen-label="Загрузка боксов" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Все посты, боксы и заказ-наряды <span class="mt-overview-hook">под полным контролем</span></h2>
          <p class="mt-section-sub">Администратор и мастера видят статус каждого бокса, закреплённого мастера, марку авто и сумму заказ-наряда в одну секунду на любом устройстве.</p>
        </div>

        <div class="mt-auto-bays">
          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Бокс 1 · Мойка</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В работе</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">BMW X5 (М 777 АА)</div>
                <div class="mt-auto-car-tier">II класс · Внедорожник</div>
              </div>
              <span class="mt-dropdown-footer-icon">🚗</span>
            </div>
            <div class="mt-auto-service">
              <span>Комплекс «Люкс»</span>
              <span class="mt-auto-price">3 400 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Бокс 2 · Детейлинг</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В работе</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Porsche Cayenne</div>
                <div class="mt-auto-car-tier">II класс · Кроссовер</div>
              </div>
              <span class="mt-dropdown-footer-icon">✨</span>
            </div>
            <div class="mt-auto-service">
              <span>Полировка + Керамика</span>
              <span class="mt-auto-price">14 500 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Пост 3 · СТО</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--done">Готово</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Geely Monjaro</div>
                <div class="mt-auto-car-tier">Заказ-наряд #1428 · ТО</div>
              </div>
              <span class="mt-dropdown-footer-icon">🔧</span>
            </div>
            <div class="mt-auto-service">
              <span>Замена масла + ТО</span>
              <span class="mt-auto-price">7 800 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Пост 4 · Шины</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--wait">Ожидание</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Zeekr 001 (14:30)</div>
                <div class="mt-auto-car-tier">Сезонная смена шин</div>
              </div>
              <span class="mt-dropdown-footer-icon">🛞</span>
            </div>
            <div class="mt-auto-service">
              <span>Шиномонтаж R21</span>
              <span class="mt-auto-price">5 200 ₽</span>
            </div>
          </div>
        </div>
      </section>

      <!-- AUTO OVERVIEW VALUE GRID -->
      <section class="mt-section mt-section--overview mt-reveal" data-screen-label="Функции для автобизнеса" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Ведите автобизнес <span class="mt-overview-hook">от заезда до чистой прибыли</span></h2>
          <p class="mt-section-sub">Программа для учета на автомойке, в детейлинге и автосервисе: расписание боксов, акты осмотра кузова, нормативы по классам авто и сдельные зарплаты без рутины в Excel.</p>
        </div>

        <div class="mt-overview-grid">
          <article class="mt-overview-card">
            <h3><span class="mt-overview-hook">Журнал записи</span> по боксам и постам</h3>
            <p>Клиенты записываются онлайн 24/7, а администратор распределяет авто по постам мойки, детейлинга или слесарного цеха СТО. Программа исключает накладки и простой оборудования.</p>
            <div class="mt-overview-preview mt-overview-preview--schedule" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Расписание боксов</span><span>Сегодня</span></div>
              <div class="mt-overview-calendar"><span>09:00</span><div></div><span>10:00</span><div class="mt-overview-slot">Бокс 1 <small>BMW X5 · Комплекс</small></div><span>11:30</span><div class="mt-overview-slot mt-overview-slot--light">Бокс 2 <small>Porsche · Полировка</small></div></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3><span class="mt-overview-hook">Акт осмотра и фото кузова</span> до начала работ</h3>
            <p>Электронный заказ-наряд с фотофиксацией со смартфона за 60 секунд: сколы, царапины, состояние дисков и салона. Чек-лист сохраняется в CRM и защищает от спорных претензий при выдаче.</p>
            <div class="mt-overview-preview mt-overview-preview--process" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Чек-лист приёмки</span><span>Бокс 1</span></div>
              <div class="mt-overview-stages"><span>Осмотр</span><i></i><span>В работе</span><i></i><span>Выдача</span></div>
              <div class="mt-overview-check">✓ <span>Фото кузова по кругу (4 фото)</span></div>
              <div class="mt-overview-check">✓ <span>Скол на капоте зафиксирован</span></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Нормативы и прайс <span class="mt-overview-hook">по классам автомобилей</span></h3>
            <p>Молния автоматически пересчитывает длительность и стоимость услуг: седан (40 мин), кроссовер (55 мин), рамный внедорожник (70 мин). Поддержка динамических тарифов в часы пик и непогоду.</p>
            <div class="mt-overview-preview mt-overview-preview--prices" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Прайс по классам</span><span>Мойка «Люкс»</span></div>
              <div class="mt-overview-price-row"><span>I класс (Седан)</span><strong>2 200 ₽ · 40 мин</strong></div>
              <div class="mt-overview-price-row"><span>II класс (Кроссовер)</span><strong>2 700 ₽ · 55 мин</strong></div>
              <div class="mt-overview-price-tag">Выходные · Часы пик · Праздники</div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Уведомления в мессенджер <span class="mt-overview-hook">и клиентская база</span></h3>
            <p>Клиент получает подтверждение бронирования, напоминание за 2 часа и уведомление «Автомобиль готов к выдаче» со ссылкой на электронный чек. Вся история визитов и ТО сохраняется в карточке авто.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Статус готовности</span><span>Мессенджер</span></div>
              <div class="mt-overview-message">
                Ваш Porsche Macan готов к выдаче в Боксе №2. Сумма к оплате: 4 500 ₽.
                <span class="mt-overview-reaction">🚗</span>
              </div>
              <div class="mt-overview-client-row"><span>База клиентов CRM</span><strong>История визитов и ТО →</strong></div>
            </div>
          </article>

          <article class="mt-overview-card mt-overview-card--featured">
            <h3>Сдельная оплата <span class="mt-overview-hook">мойщиков и мастеров</span></h3>
            <p>Автоматический расчет зарплаты мойщиков, детейлеров и автомехаников: процент от чека или ставка за операцию начисляются сразу после закрытия заказ-наряда. Мастера видят баланс смены в телефоне.</p>
            <div class="mt-overview-preview mt-overview-preview--metrics" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Выработка за смену</span><span>Смена №1</span></div>
              <div class="mt-overview-metrics"><span>Мойка<b>30%</b></span><span>Детейлинг<b>40%</b></span><span>Баланс<b>₽</b></span></div>
              <div class="mt-overview-chart"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            </div>
          </article>
        </div>

        <div class="mt-overview-action">
          <a class="mt-btn mt-btn-cta" href="#contact">Получить бесплатный доступ</a>
        </div>
      </section>

      <!-- AUTO JOURNEY -->
      <section class="mt-section mt-journey" data-screen-label="Путь визита авто">
        <div class="mt-section-head mt-section-head--center" data-mt-reveal>
          <h2 class="mt-section-title">Один заезд авто. <span class="mt-hero-accent">Полный контроль в Молнии.</span></h2>
          <p class="mt-section-sub">Посмотрите, как специализированная программа автоматизирует обслуживание автомобиля от онлайн-записи до выдачи ключей и начисления сдельной зарплаты.</p>
        </div>

        <div class="mt-journey-example" aria-label="Пример прохождения записи" data-mt-reveal data-mt-delay="80">
          <span>Пример</span><strong>Комплексная мойка + Твёрдый воск</strong><span>Geely Monjaro · Бокс №1</span>
        </div>

        <div class="mt-journey-list">
          <article class="mt-journey-step">
            <div class="mt-journey-index">01</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Клиент</span>
              <h3>Онлайн-запись с автоматическим учетом класса авто</h3>
              <p>Клиент выбирает марку, тип кузова и комплекс услуг на сайте или через мессенджер. Программа сразу резервирует окно нужной длительности (55 минут вместо 40) с учетом габаритов кроссовера.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--booking" aria-label="Пример онлайн-записи">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Онлайн-запись</span>
                <span class="mt-journey-proof-badge">Подтверждена</span>
              </div>
              <div class="mt-journey-proof-row"><span>Автомобиль</span><strong>Geely Monjaro (II класс)</strong></div>
              <div class="mt-journey-proof-row"><span>Услуга</span><strong>Комплекс + Воск</strong></div>
              <div class="mt-journey-proof-row"><span>Бокс</span><strong>Бокс №1 (мойка)</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">02</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Администратор / Мастер</span>
              <h3>Заезд в бокс и электронный заказ-наряд с фото</h3>
              <p>Мастер открывает электронный заказ-наряд со смартфона и за 60 секунд фотографирует сколы на капоте и дисках. Акт осмотра прикрепляется к заказу до начала работ.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--process" aria-label="Чек-лист приёмки">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Заказ-наряд #1428</span>
                <span class="mt-journey-proof-badge">Осмотр пройден</span>
              </div>
              <div class="mt-journey-proof-row"><span>Фотофиксация</span><strong>4 фото сохранены</strong></div>
              <div class="mt-journey-proof-row"><span>Ценные вещи</span><strong>В салоне отсутствуют</strong></div>
              <div class="mt-journey-proof-row"><span>Мастер</span><strong>Александр В. (смена 1)</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">03</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Мастер</span>
              <h3>Выполнение работ и допродажа услуг в 1 тап</h3>
              <p>Мастер заметил битумные пятна на порогах и добавил удаление битума (900 ₽) прямо в электронный заказ-наряд со смартфона. Сумма автоматически пересчиталась.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--order" aria-label="Состав заказа">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Выполненные работы</span>
                <span class="mt-journey-proof-badge">Готово к выдаче</span>
              </div>
              <div class="mt-journey-proof-row"><span>Комплекс «Люкс»</span><strong>2 700 ₽</strong></div>
              <div class="mt-journey-proof-row"><span>Антидождь лобового</span><strong>1 200 ₽</strong></div>
              <div class="mt-journey-proof-row"><span>Итого заказ-наряд</span><strong>3 900 ₽</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">04</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Система & Владелец</span>
              <h3>Выдача авто, чек в мессенджер и расчет зарплаты мастеров</h3>
              <p>Клиент получает оповещение о готовности и ссылку на чек в мессенджере. Программа моментально начисляет мастеру 35% (1 365 ₽) на баланс смены — без ручных записей и споров.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--payout" aria-label="Финансовый расчёт">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Расчёт мастера</span>
                <span class="mt-journey-proof-badge">Начислено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Александр В. (35%)</span><strong>+1 365 ₽</strong></div>
              <div class="mt-journey-proof-row"><span>Выручка автомойки</span><strong>+2 535 ₽</strong></div>
              <div class="mt-journey-proof-row"><span>Статус в мессенджере</span><strong>«Автомобиль выдан»</strong></div>
            </div>
          </article>
        </div>
      </section>

      <!-- REAL-WORLD CASE STUDY -->
      <section class="mt-case-section mt-reveal" data-screen-label="Кейс детейлинга" data-mt-reveal>
        <div class="mt-case-card">
          <div class="mt-case-header">
            <div class="mt-case-tag">⚡ Кейс автоматизации автобизнеса</div>
            <h2 class="mt-case-title">Детейлинг-студия «Вектор», 4 поста</h2>
            <blockquote class="mt-case-quote">
              «Раньше каждый вечер уходил час на сведение тетради с мойщиками, а по выходным была давка из-за джипов, которые не влезали по времени. В CRM Молния мы настроили онлайн-запись и нормативы по классам авто — расписание боксов стало идеальным, а выработка мастеров прозрачной.»
            </blockquote>
            <div class="mt-case-author">
              Алексей Смирнов <span>· Руководитель детейлинг-центра, <span style="white-space:nowrap">Санкт-Петербург</span></span>
            </div>
          </div>
          <div class="mt-case-stats">
            <div class="mt-case-stat">
              <span class="mt-case-num">+35%</span>
              <span class="mt-case-label">Рост выручки автомойки за счёт плотной сетки записи</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">-86%</span>
              <span class="mt-case-label">Снижение неявок благодаря напоминаниям в мессенджере</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">0 <small>мин</small></span>
              <span class="mt-case-label">На подсчёт зарплат и выработки мастеров</span>
            </div>
          </div>
        </div>
      </section>

      <!-- AUTO FAQ -->
      <section id="faq" class="mt-section mt-reveal" data-screen-label="Вопросы и ответы" data-mt-reveal>
        <div class="mt-section-head">
          <h2 class="mt-section-title">Вопросы о программе для автомойки, детейлинга и автосервиса</h2>
        </div>
        <div class="mt-before-start-grid">
          <article class="mt-before-start-highlight">
            <h3>Попробуйте CRM Молния для своего автобизнеса</h3>
            <p>Бесплатно поможем перенести базу клиентов из тетради или Excel, настроить боксы, прайс по классам авто и зарплаты мастеров. Начните работу без пауз в сервисе.</p>
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в мессенджер ↗</a>
          </article>
          <div class="mt-before-start-questions">
{faq_html}
          </div>
        </div>
        <p class="mt-before-start-privacy">Как мы обрабатываем данные — в <a href="/privacy">политике конфиденциальности</a>.</p>
      </section>

{lead_html}

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
'''
    return page_html


def build_beauty_page() -> str:
    """Builds the complete beauty salon landing page matching the exact design system."""
    nav_html = render_nav_html(active_item="beauty", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")
    lead_html = render_lead_form_html(
        "beauty",
        'Получите <span class="mt-hero-accent">бесплатный доступ навсегда</span> для салона красоты',
        "Оставьте контакты — поможем настроить запись, расписание мастеров и услуги.",
    )

    title = "CRM для салона красоты: онлайн-запись и учёт | Молния"
    description = "Молния — CRM для салона красоты: онлайн-запись клиентов, расписание мастеров, учёт материалов и расчёт зарплаты. Подходит барбершопам и студиям маникюра."
    canonical = "https://molniya-tech.ru/beauty"

    faq_items = [
        {
            "q": "Подходит ли программа для небольшого кабинета мастера или бьюти-коворкинга?",
            "a": "Да. Молния одинаково удобна как для частного мастера или кабинета на 1–2 кресла, так и для сетевого салона красоты или барбершопа с десятками мастеров. Настройка расписания, списка услуг и мастеров занимает всего 15 минут."
        },
        {
            "q": "Как работает учет красителей, оксидов и расходников по техкартам?",
            "a": "В Молнии к каждой услуге можно привязать норму расхода материалов (например, краситель 40 г, оксид 60 мл, фольга, воротнички). При закрытии визита материалы автоматически списываются со склада, а система предупредит, если запасы подходят к концу."
        },
        {
            "q": "Как рассчитывается сдельная зарплата мастеров, администраторов и аренда кресел?",
            "a": "Для каждого сотрудника настраиваются персональные условия: процент от чека за услуги (например, 40%), процент от продажи домашнего ухода (например, 10%), фиксированная ставка за смену или вычет фиксированной стоимости аренды рабочего места."
        },
        {
            "q": "Можно ли бесплатно перенести базу клиентов из YClients, DIKIDI, Altegio или Excel?",
            "a": "Да! Наша служба заботы бесплатно помогает перенести базу клиентов с номерами телефонов, историей визитов, прайс-листом и данными мастеров. Вы переходите на Молнию без потери постоянных клиентов и пауз в работе салона."
        },
        {
            "q": "Как клиенты записываются онлайн и получают напоминания в мессенджер?",
            "a": "Клиенты переходят по ссылке в соцсетях, на сайте или по QR-коду и выбирают удобное время и любимого мастера. Сервисный бот в мессенджере автоматически подтверждает запись, напоминает о визите за 24 и 2 часа, снижая неявки на 85%."
        },
        {
            "q": "Сохраняются ли формулы окрашивания и фото работ в карточке клиента?",
            "a": "Да. Мастер прямо со смартфона может прикрепить фото «до/после» и записать точную формулу красителя (номера тонов, пропорции, время выдержки). При следующем визите клиента вся история доступна за 2 секунды."
        },
        {
            "q": "Нужно ли устанавливать отдельное приложение на компьютер или планшет?",
            "a": "Нет. Молния работает как быстрое веб-приложение в любом браузере на смартфоне, планшете или ноутбуке. Администратор может вести журнал на ресепшене с планшета, а мастера смотрят своё расписание в телефоне."
        }
    ]

    faq_html = "\n".join(
        f'            <details><summary>{html.escape(item["q"])}</summary><p>{html.escape(item["a"])}</p></details>'
        for item in faq_items
    )

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Молния — CRM для салона красоты",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web, iOS, Android",
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "RUB"
            },
            "description": description,
            "url": canonical
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Главная",
                    "item": "https://molniya-tech.ru/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Для кого",
                    "item": "https://molniya-tech.ru/#origin"
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": "Красота",
                    "item": canonical
                }
            ]
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item["q"],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": item["a"]
                    }
                }
                for item in faq_items
            ]
        }
    ]

    json_ld_str = json.dumps(json_ld, ensure_ascii=False).replace("<", "\\u003c")

    page_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="{canonical}">
  <meta name="theme-color" content="#FFFEFD">

  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- HERO -->
      <section class="mt-hero" data-screen-label="Герой" data-mt-hero-scene>

        <div class="mt-hero-lead">
          <h1 class="mt-hero-title">
            CRM для салона красоты,<br><span class="mt-hero-accent">барбершопа и студии маникюра</span>
          </h1>

          <div class="mt-hero-bottom">
            <div class="mt-hero-intro">
              <p class="mt-hero-sub">Онлайн-запись 24/7, расписание мастеров, расчет зарплат и прозрачный учет материалов</p>
              <a class="mt-btn mt-btn-hero" href="#contact">Получить бесплатный доступ</a>
            </div>

            <ul class="mt-facets mt-facets--full" aria-label="Преимущества для салона красоты">
              <li class="mt-facet">
                <span class="mt-facet-name">Журнал мастеров</span>
                <span class="mt-facet-note">онлайн-запись 24/7 без накладок</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Зарплата и %</span>
                <span class="mt-facet-note">автоматический расчёт выработки за смену</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Учёт материалов</span>
                <span class="mt-facet-note">списание красителей и расходников</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name mt-facet-name--soon">AI & Возвраты</span>
                <span class="mt-facet-note">Напоминания в мессенджер и повторные визиты</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <div class="mt-tablet">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для салона красоты: расписание мастеров и электронный журнал записи" width="1710" height="983" fetchpriority="high">
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </div>
            <p class="mt-hero-media-caption">Электронный журнал записи и загрузка мастеров салона в реальном времени</p>
          </div>
        </div>

      </section>

      <!-- LIVE WORKPLACES STATUS -->
      <section class="mt-section mt-reveal" data-screen-label="Загрузка кресел и мастеров" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Все кресла, кабинеты и мастера <span class="mt-overview-hook">под полным контролем</span></h2>
          <p class="mt-section-sub">Администратор и управляющий видят статус каждого рабочего места, закреплённого мастера, текущую процедуру и сумму чека в реальном времени на любом устройстве.</p>
        </div>

        <div class="mt-auto-bays">
          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Кресло 1 · Стилист</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В работе</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Елена К. (Анна С.)</div>
                <div class="mt-auto-car-tier">Airtouch + Уход</div>
              </div>
              <span class="mt-dropdown-footer-icon">✂️</span>
            </div>
            <div class="mt-auto-service">
              <span>Сложное окрашивание</span>
              <span class="mt-auto-price">8 500 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Пост 2 · Маникюр</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В работе</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Мария Д. (Екатерина М.)</div>
                <div class="mt-auto-car-tier">Маникюр + SMART</div>
              </div>
              <span class="mt-dropdown-footer-icon">💅</span>
            </div>
            <div class="mt-auto-service">
              <span>Снятие + Покрытие</span>
              <span class="mt-auto-price">4 200 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Кресло 3 · Барбер</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--done">Готово</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Артур Б. (Дмитрий В.)</div>
                <div class="mt-auto-car-tier">Стрижка + Борода</div>
              </div>
              <span class="mt-dropdown-footer-icon">💈</span>
            </div>
            <div class="mt-auto-service">
              <span>Стрижка + Моделирование</span>
              <span class="mt-auto-price">2 800 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Пост 4 · Косметолог</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--wait">Ожидание</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Ольга Н. (15:00)</div>
                <div class="mt-auto-car-tier">Уход за лицом</div>
              </div>
              <span class="mt-dropdown-footer-icon">✨</span>
            </div>
            <div class="mt-auto-service">
              <span>Пилинг + Массаж</span>
              <span class="mt-auto-price">5 600 ₽</span>
            </div>
          </div>
        </div>
      </section>

      <!-- BEAUTY OVERVIEW VALUE GRID -->
      <section class="mt-section mt-section--overview mt-reveal" data-screen-label="Функции для салона красоты" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Управляйте бьюти-бизнесом <span class="mt-overview-hook">от первой записи до чистой прибыли</span></h2>
          <p class="mt-section-sub">Программа для учета в салоне красоты, барбершопе и студии маникюра: расписание мастеров, карточки клиентов с формулами окрашивания, списание материалов и зарплаты без тетрадей.</p>
        </div>

        <div class="mt-overview-grid">
          <article class="mt-overview-card">
            <h3><span class="mt-overview-hook">Журнал записи</span> и расписание мастеров</h3>
            <p>Клиенты записываются онлайн через сайт, соцсети или мессенджер 24/7. Администратор управляет загрузкой кресел и кабинетов в один клик. Программа предотвращает накладки и «окна» между визитами.</p>
            <div class="mt-overview-preview mt-overview-preview--schedule" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Расписание мастеров</span><span>Сегодня</span></div>
              <div class="mt-overview-calendar"><span>10:00</span><div></div><span>11:30</span><div class="mt-overview-slot">Кресло 1 <small>Елена · Airtouch</small></div><span>13:00</span><div class="mt-overview-slot mt-overview-slot--light">Кабинет 2 <small>Мария · SMART-маникюр</small></div></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Карточка клиента и <span class="mt-overview-hook">история окрашиваний</span></h3>
            <p>Вся история процедур, любимые мастера и точные формулы красителей (пропорции, граммовка, оксиды) сохраняются в карточке клиента. Новый мастер сразу видит историю волос или пожелания по ногтям.</p>
            <div class="mt-overview-preview mt-overview-preview--process" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Карточка клиента</span><span>Анна Смирнова</span></div>
              <div class="mt-overview-stages"><span>Консультация</span><i></i><span>Процедура</span><i></i><span>Расчёт</span></div>
              <div class="mt-overview-check">✓ <span>Формула: 8.1 (30г) + 9.16 (15г) + 3%</span></div>
              <div class="mt-overview-check">✓ <span>Фото до окрашивания сохранено</span></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Складской учёт и <span class="mt-overview-hook">списание материалов</span></h3>
            <p>Молния автоматически списывает красители, оксиды, уходы и одноразовые расходники по техкартам после каждой услуги. Точные остатки на складе и оповещения, когда краска заканчивается.</p>
            <div class="mt-overview-preview mt-overview-preview--prices" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Остатки на складе</span><span>Красители и оксиды</span></div>
              <div class="mt-overview-price-row"><span>Краситель L'Oreal #8.1</span><strong>140 г на складе</strong></div>
              <div class="mt-overview-price-row"><span>Оксид 6% (Diactivateur)</span><strong>820 мл · В норме</strong></div>
              <div class="mt-overview-price-tag">Автосписание по техкартам</div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Уведомления в мессенджер <span class="mt-overview-hook">и возвращаемость</span></h3>
            <p>Сервисные напоминания в мессенджер за 24 и 2 часа снижают процент неявок до 85%. Автоматические приглашения на повторный визит через 3–4 недели стабильно возвращают клиентов без спама.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Статус записи</span><span>Мессенджер</span></div>
              <div class="mt-overview-message">
                Анна, напоминаем о записи к стилисту Елене завтра в 14:00. Ждём вас в студии!
                <span class="mt-overview-reaction">💇‍♀️</span>
              </div>
              <div class="mt-overview-client-row"><span>База клиентов CRM</span><strong>История визитов и формул →</strong></div>
            </div>
          </article>

          <article class="mt-overview-card mt-overview-card--featured">
            <h3>Сдельная зарплата мастеров <span class="mt-overview-hook">и аренда кресел</span></h3>
            <p>Гибкая настройка мотивации: процент от чека за услугу, процент от продажи косметики, фиксированная ставка за выход или учёт стоимости аренды кресла. Мастера видят выработку в телефоне в реальном времени.</p>
            <div class="mt-overview-preview mt-overview-preview--metrics" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Выработка мастера</span><span>Елена К. (Смена)</span></div>
              <div class="mt-overview-metrics"><span>Услуги<b>40%</b></span><span>Косметика<b>10%</b></span><span>Баланс<b>₽</b></span></div>
              <div class="mt-overview-chart"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            </div>
          </article>
        </div>

        <div class="mt-overview-action">
          <a class="mt-btn mt-btn-cta" href="#contact">Получить бесплатный доступ</a>
        </div>
      </section>

      <!-- BEAUTY JOURNEY -->
      <section class="mt-section mt-journey" data-screen-label="Путь визита клиента">
        <div class="mt-section-head mt-section-head--center" data-mt-reveal>
          <h2 class="mt-section-title">Один визит клиента. <span class="mt-hero-accent">Полный порядок в салоне.</span></h2>
          <p class="mt-section-sub">Посмотрите, как Молния автоматизирует работу студии красоты: от бронирования слота до фиксации формулы окрашивания, списания красителя и расчета зарплаты.</p>
        </div>

        <div class="mt-journey-example" aria-label="Пример прохождения записи" data-mt-reveal data-mt-delay="80">
          <span>Пример</span><strong>Сложное окрашивание + Уход</strong><span>Стилист Елена К. · Кресло №1</span>
        </div>

        <div class="mt-journey-list">
          <article class="mt-journey-step">
            <div class="mt-journey-index">01</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Клиент</span>
              <h3>Онлайн-запись к любимому мастеру в удобное время</h3>
              <p>Клиент выбирает услугу, мастера и время за 30 секунд в виджете онлайн-записи. Программа сразу бронирует окно в расписании, не допуская накладок, и присылает подтверждение в мессенджер.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--booking" aria-label="Пример онлайн-записи">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Онлайн-запись</span>
                <span class="mt-journey-proof-badge">Подтверждена</span>
              </div>
              <div class="mt-journey-proof-row"><span>Клиент</span><strong>Анна Смирнова</strong></div>
              <div class="mt-journey-proof-row"><span>Услуга</span><strong>Airtouch + Тонирование</strong></div>
              <div class="mt-journey-proof-row"><span>Мастер</span><strong>Елена К. (Кресло №1)</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">02</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Мастер / Администратор</span>
              <h3>Встреча клиента и фиксация формулы окрашивания</h3>
              <p>Мастер открывает карточку визита в телефоне, смотрит историю прошлых процедур и записывает формулу красителя и примечания прямо во время консультации.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--process" aria-label="Карточка визита">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Визит #2841</span>
                <span class="mt-journey-proof-badge">В процессе</span>
              </div>
              <div class="mt-journey-proof-row"><span>Формула</span><strong>8.1 (30г) + 9.16 (15г) + 3%</strong></div>
              <div class="mt-journey-proof-row"><span>Фото «До»</span><strong>Прикреплено к карточке</strong></div>
              <div class="mt-journey-proof-row"><span>Пожелания</span><strong>Кофе с овсяным молоком</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">03</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Мастер</span>
              <h3>Оказание услуги и допродажа домашнего ухода</h3>
              <p>Мастер порекомендовал бессульфатный шампунь и маску для сохранения холодного блонда. Администратор добавил средства в чек в 1 клик — они сразу списались со склада.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--order" aria-label="Состав заказа">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Состав чека</span>
                <span class="mt-journey-proof-badge">К оплате</span>
              </div>
              <div class="mt-journey-proof-row"><span>Airtouch + Тонирование</span><strong>8 500 ₽</strong></div>
              <div class="mt-journey-proof-row"><span>Шампунь для блонда</span><strong>2 400 ₽</strong></div>
              <div class="mt-journey-proof-row"><span>Итого чек</span><strong>10 900 ₽</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">04</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Система & Владелец</span>
              <h3>Оплата, расчёт зарплаты и напоминание на следующий визит</h3>
              <p>Клиент получает электронный чек в мессенджере. Программа начисляет мастеру 40% за услугу (3 400 ₽) и 10% за уход (240 ₽). Через 4 недели клиент получит автоприглашение на обновление цвета.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--payout" aria-label="Финансовый расчёт">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Расчёт мастера</span>
                <span class="mt-journey-proof-badge">Начислено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Елена К. (выработка)</span><strong>+3 640 ₽</strong></div>
              <div class="mt-journey-proof-row"><span>Списание со склада</span><strong>Краситель -45г</strong></div>
              <div class="mt-journey-proof-row"><span>Автоприглашение в мессенджере</span><strong>Запланировано через 28 дн</strong></div>
            </div>
          </article>
        </div>
      </section>

      <!-- REAL-WORLD CASE STUDY -->
      <section class="mt-case-section mt-reveal" data-screen-label="Кейс салона красоты" data-mt-reveal>
        <div class="mt-case-card">
          <div class="mt-case-header">
            <div class="mt-case-tag">⚡ Кейс автоматизации бьюти-студии</div>
            <h2 class="mt-case-title">Студия красоты и колористики «Lumière», 6 рабочих мест</h2>
            <blockquote class="mt-case-quote">
              «До Молнии вели запись в бумажном ежедневнике, а красители списывали раз в месяц «на глаз» с постоянными недостачами. В Молнии мы настроили онлайн-запись, техкарты расхода и автоматический процент стилистам. Мастера больше не спорят о зарплате, а запись заполнена на две недели вперёд.»
            </blockquote>
            <div class="mt-case-author">
              Ирина Васильева <span>· Основательница студии красоты, <span style="white-space:nowrap">Санкт-Петербург</span></span>
            </div>
          </div>
          <div class="mt-case-stats">
            <div class="mt-case-stat">
              <span class="mt-case-num">+42%</span>
              <span class="mt-case-label">Рост повторных записей через Напоминания в мессенджер</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">-90%</span>
              <span class="mt-case-label">Снижение неявок благодаря автоматическому подтверждению</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">0 <small>мин</small></span>
              <span class="mt-case-label">На ручной расчёт зарплат мастеров и учёт красителей</span>
            </div>
          </div>
        </div>
      </section>

      <!-- BEAUTY FAQ -->
      <section id="faq" class="mt-section mt-reveal" data-screen-label="Вопросы и ответы" data-mt-reveal>
        <div class="mt-section-head">
          <h2 class="mt-section-title">Вопросы о программе для салона красоты, барбершопа и студии маникюра</h2>
        </div>
        <div class="mt-before-start-grid">
          <article class="mt-before-start-highlight">
            <h3>Попробуйте CRM Молния для своего салона красоты</h3>
            <p>Бесплатно поможем перенести базу клиентов из тетради, Excel или старой CRM, настроить расписание мастеров, прайс-лист и схему зарплаты. Начните работу без пауз в сервисе.</p>
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в мессенджер ↗</a>
          </article>
          <div class="mt-before-start-questions">
{faq_html}
          </div>
        </div>
        <p class="mt-before-start-privacy">Как мы обрабатываем данные — в <a href="/privacy">политике конфиденциальности</a>.</p>
      </section>

{lead_html}

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
'''
    return page_html


def build_health_page() -> str:
    """Builds the complete health landing page matching the exact design system."""
    nav_html = render_nav_html(active_item="health", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")
    lead_html = render_lead_form_html(
        "health",
        'Получите <span class="mt-hero-accent">бесплатный доступ навсегда</span> для клиники',
        "Оставьте контакты — расскажем о записи и расписании для вашей клиники или кабинета.",
    )

    title = "CRM для клиники, студии массажа и стоматологии — программа учета пациентов и онлайн-записи Молния"
    description = (
        "Программа и CRM для медицинских центров, студий массажа, клиник и частных кабинетов: "
        "онлайн-запись пациентов 24/7, расписание кабинетов и врачей, электронная карта пациента, "
        "расчёт сдельной зарплаты и учет расходников."
    )
    canonical = "https://molniya-tech.ru/health"

    json_ld = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Молния Тех — CRM для клиник, студий массажа и медицинских центров",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Web, iOS, Android, macOS, Windows",
        "url": canonical,
        "description": description,
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "RUB",
            "description": "Бесплатный демо-доступ и перенос базы пациентов"
        },
        "publisher": {
            "@type": "Organization",
            "name": "ООО «МОЛНИЯ ТЕХ»",
            "url": "https://molniya-tech.ru"
        }
    }
    json_ld_str = json.dumps(json_ld, ensure_ascii=False)

    faqs = [
        (
            "Подходит ли программа для частной клиники, массажной студии и стоматологии?",
            "Да. В Молнии гибко настраивается профиль работы: кабинеты врачей, массажные кушетки, стоматологические кресла или процедурные кабинеты. Вы задаете длительность процедур, привязку аппаратов к кабинетам и правила записи пациентов."
        ),
        (
            "Как защищаются персональные данные пациентов (152-ФЗ)?",
            "Система соответствует требованиям 152-ФЗ: все данные хранятся на защищенных серверах в дата-центрах на территории РФ с шифрованием. Доступ строго разграничен по ролям: врачи видят медицинские карты своих пациентов, администраторы — журнал записи и оплату."
        ),
        (
            "Можно ли настраивать разную длительность приемов для разных специалистов?",
            "Да. Для каждой специальности и услуги задается индивидуальный хронометраж: например, первичный прием терапевта — 40 минут, повторный — 20 минут, сеанс массажа спины — 60 минут. При онлайн-записи система автоматически бронирует правильное окно в расписании."
        ),
        (
            "Как учитываются курсы процедур и абонементы (например, курс массажа)?",
            "Программа ведет автоматический учет визитов по курсам и абонементам. Администратор и специалист видят номер текущего сеанса (например, 4 из 10), остаток оплаченных процедур и дату рекомендованного следующего визита."
        ),
        (
            "Как происходит расчет зарплаты врачей и медицинского персонала?",
            "В системе настраивается любая схема мотивации: процент от стоимости приема, фиксированная ставка за смену/выход, процент от назначенных процедур или учет стоимости аренды кабинета. Выработка рассчитывается автоматически в реальном времени."
        ),
        (
            "Как бесплатно перенести базу пациентов и историю приемов из старой программы или Excel?",
            "Служба заботы Молнии бесплатно помогает перенести контакты пациентов, историю визитов, каталог услуг, прайс-лист и график специалистов. Вы начинаете работу без остановки приема и без потери данных."
        ),
    ]

    faq_html = "\n".join(
        f'            <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
        for q, a in faqs
    )

    page_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#FAF7F2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#12100E" media="(prefers-color-scheme: dark)">
  <link rel="canonical" href="{canonical}">

  <!-- Favicons -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- HERO -->
      <section class="mt-hero" data-screen-label="Герой" data-mt-hero-scene>

        <div class="mt-hero-lead">
          <h1 class="mt-hero-title">
            CRM для клиники,<br><span class="mt-hero-accent">студии массажа и частной практики</span>
          </h1>

          <div class="mt-hero-bottom">
            <div class="mt-hero-intro">
              <p class="mt-hero-sub">Онлайн-запись 24/7, расписание кабинетов, электронная карта пациента и сдельный расчет зарплат</p>
              <a class="mt-btn mt-btn-hero" href="#contact">Получить бесплатный доступ</a>
            </div>

            <ul class="mt-facets mt-facets--full" aria-label="Преимущества для медицины и оздоровления">
              <li class="mt-facet">
                <span class="mt-facet-name">Врачи и кабинеты</span>
                <span class="mt-facet-note">онлайн-запись и учет длительности приемов</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Карта пациента</span>
                <span class="mt-facet-note">протоколы осмотров, история и анализы</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Зарплата и %</span>
                <span class="mt-facet-note">сдельная оплата за прием и процедуры</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name mt-facet-name--soon">AI & Профилактика</span>
                <span class="mt-facet-note">Напоминания в мессенджер и повторные визиты</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <div class="mt-tablet">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для клиники и медицинского центра: расписание врачей и электронный журнал записи" width="1710" height="983" fetchpriority="high">
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </div>
            <p class="mt-hero-media-caption">Электронный журнал записи и загрузка кабинетов клиники в реальном времени</p>
          </div>
        </div>

      </section>

      <!-- LIVE CABINETS STATUS -->
      <section class="mt-section mt-reveal" data-screen-label="Загрузка кабинетов и врачей" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Все кабинеты, врачи и пациенты <span class="mt-overview-hook">под полным контролем</span></h2>
          <p class="mt-section-sub">Администратор и главный врач видят статус каждого кабинета, принимающего специалиста, процедуру и сумму чека в реальном времени на любом устройстве.</p>
        </div>

        <div class="mt-auto-bays">
          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Каб. 1 · Терапевт</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В работе</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Сергей В. (Анна М.)</div>
                <div class="mt-auto-car-tier">Первичный прием + ЭКГ</div>
              </div>
              <span class="mt-dropdown-footer-icon">🩺</span>
            </div>
            <div class="mt-auto-service">
              <span>Консультация + ЭКГ</span>
              <span class="mt-auto-price">3 500 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Каб. 2 · Стоматолог</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В работе</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Марина К. (Игорь Д.)</div>
                <div class="mt-auto-car-tier">Терапия + Снимок</div>
              </div>
              <span class="mt-dropdown-footer-icon">🦷</span>
            </div>
            <div class="mt-auto-service">
              <span>Лечение кариеса</span>
              <span class="mt-auto-price">6 800 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Зал 3 · Массаж</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--done">Готово</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Павел Р. (Михаил С.)</div>
                <div class="mt-auto-car-tier">Курс (сеанс 4 из 10)</div>
              </div>
              <span class="mt-dropdown-footer-icon">💆‍♂️</span>
            </div>
            <div class="mt-auto-service">
              <span>Спортивный массаж</span>
              <span class="mt-auto-price">4 200 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Каб. 4 · УЗИ</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--wait">Ожидание</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Ольга Н. (15:30)</div>
                <div class="mt-auto-car-tier">УЗИ органов брюшной</div>
              </div>
              <span class="mt-dropdown-footer-icon">📋</span>
            </div>
            <div class="mt-auto-service">
              <span>УЗИ-скрининг</span>
              <span class="mt-auto-price">4 500 ₽</span>
            </div>
          </div>
        </div>
      </section>

      <!-- HEALTH OVERVIEW VALUE GRID -->
      <section class="mt-section mt-section--overview mt-reveal" data-screen-label="Функции для медицины и клиник" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Ведите медицинский бизнес <span class="mt-overview-hook">от первого обращения до выздоровления</span></h2>
          <p class="mt-section-sub">Программа для учета в медицинском центре, студии массажа и стоматологии: электронное расписание кабинетов, амбулаторные карты пациентов, списание расходников и прозрачные зарплаты без рутины в бумажных журналах.</p>
        </div>

        <div class="mt-overview-grid">
          <article class="mt-overview-card">
            <h3><span class="mt-overview-hook">Журнал записи</span> и расписание кабинетов</h3>
            <p>Пациенты записываются онлайн через сайт, соцсети или мессенджер 24/7. Администратор управляет загрузкой кабинетов, аппаратов и врачей в один клик. Программа предотвращает пересечения специалистов и простой оборудования.</p>
            <div class="mt-overview-preview mt-overview-preview--schedule" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Расписание приемов</span><span>Сегодня</span></div>
              <div class="mt-overview-calendar"><span>09:00</span><div></div><span>10:30</span><div class="mt-overview-slot">Каб. 1 <small>Терапевт · Прием + ЭКГ</small></div><span>12:00</span><div class="mt-overview-slot mt-overview-slot--light">Зал 3 <small>Массаж · Спина (курс)</small></div></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Электронная карта пациента <span class="mt-overview-hook">и протоколы приемов</span></h3>
            <p>История визитов, анамнез, назначения, протоколы приемов и прикрепленные результаты анализов или снимков хранятся в защищенной карте пациента. Врач мгновенно видит динамику лечения перед началом консультации.</p>
            <div class="mt-overview-preview mt-overview-preview--process" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Карточка пациента</span><span>Сергей Васильев</span></div>
              <div class="mt-overview-stages"><span>Осмотр</span><i></i><span>Протокол</span><i></i><span>Назначения</span></div>
              <div class="mt-overview-check">✓ <span>Диагноз: Первичная консультация (здоров)</span></div>
              <div class="mt-overview-check">✓ <span>Протокол осмотра и ЭКГ прикреплены</span></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Складской учёт медикаментов <span class="mt-overview-hook">и расходников</span></h3>
            <p>Молния автоматически списывает одноразовые расходники, перчатки, простыни, ампулы и массажные масла по стандартам каждой услуги. Полный контроль остатков и уведомления, когда препараты на исходе.</p>
            <div class="mt-overview-preview mt-overview-preview--prices" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Остатки на складе</span><span>Медикаменты и расходники</span></div>
              <div class="mt-overview-price-row"><span>Стерильные перчатки (L)</span><strong>420 пар · В норме</strong></div>
              <div class="mt-overview-price-row"><span>Масло массажное базовое</span><strong>1 450 мл на складе</strong></div>
              <div class="mt-overview-price-tag">Автосписание по протоколу услуги</div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Напоминания в мессенджер <span class="mt-overview-hook">и повторные приемы</span></h3>
            <p>Автоматические напоминания в мессенджер за 24 и 2 часа снижают долю пропущенных приемов до 88%. Система вовремя напоминает пациентам о плановых осмотрах, вакцинациях и повторных сеансах курса массажа.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Статус визита</span><span>Мессенджер</span></div>
              <div class="mt-overview-message">
                Сергей, напоминаем о приеме у терапевта завтра в 10:30. Кабинет №1. Пожалуйста, подтвердите визит.
                <span class="mt-overview-reaction">🩺</span>
              </div>
              <div class="mt-overview-client-row"><span>База пациентов клиники</span><strong>История визитов и карты →</strong></div>
            </div>
          </article>

          <article class="mt-overview-card mt-overview-card--featured">
            <h3>Сдельная зарплата врачей <span class="mt-overview-hook">и учет выработки</span></h3>
            <p>Гибкая мотивация: процент от стоимости приема, фикс за смену, доплата за проведенные процедуры или учет аренды кабинета. Врачи и массажисты видят свою выработку прямо в телефоне без споров и задержек.</p>
            <div class="mt-overview-preview mt-overview-preview--metrics" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Выработка врача</span><span>Анна М. (Смена)</span></div>
              <div class="mt-overview-metrics"><span>Приемы<b>40%</b></span><span>Процедуры<b>15%</b></span><span>Баланс<b>₽</b></span></div>
              <div class="mt-overview-chart"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            </div>
          </article>
        </div>

        <div class="mt-overview-action">
          <a class="mt-btn mt-btn-cta" href="#contact">Получить бесплатный доступ</a>
        </div>
      </section>

      <!-- HEALTH SUB-NICHES & PRIVATE PRACTICE -->
      <section class="mt-section mt-reveal" data-screen-label="Частная практика" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Готовые решения <span class="mt-overview-hook">для студий и специалистов</span></h2>
          <p class="mt-section-sub">Если вы ведёте профильную студию или индивидуальный приём, используйте готовые страницы записи Молнии с регламентом слотов, буфером на отдых и анкетами приёма.</p>
        </div>

        <div class="mt-subniche-grid">
          <a class="mt-subniche-card" href="/psychologist">
            <div class="mt-subniche-icon">🧠</div>
            <div class="mt-subniche-content">
              <div class="mt-subniche-title">Психологи и психотерапевты <span class="mt-subniche-arrow">→</span></div>
              <div class="mt-subniche-desc">Персональная страница записи 24/7, свободные слоты по 50 минут с буфером на заметки, формы приёма с вопросами под услугу и защищённый профиль клиента.</div>
            </div>
          </a>
          <a class="mt-subniche-card" href="/stretching">
            <div class="mt-subniche-icon">🧘‍♀️</div>
            <div class="mt-subniche-content">
              <div class="mt-subniche-title">Студии растяжки и стретчинга <span class="mt-subniche-arrow">→</span></div>
              <div class="mt-subniche-desc">Онлайн-расписание тренировок 24/7, учёт залов и вместимости групп, контроль абонементов и автонапоминания ученикам без рутины в чатах.</div>
            </div>
          </a>
          <a class="mt-subniche-card" href="/yoga">
            <div class="mt-subniche-icon">🌿</div>
            <div class="mt-subniche-content">
              <div class="mt-subniche-title">Студии йоги и пилатеса <span class="mt-subniche-arrow">→</span></div>
              <div class="mt-subniche-desc">Сетка утренних и вечерних практик, бронь ковриков и реформеров, запись в мини-группы и автосписание занятий по абонементам.</div>
            </div>
          </a>
          <a class="mt-subniche-card" href="/trainers">
            <div class="mt-subniche-icon">💪</div>
            <div class="mt-subniche-content">
              <div class="mt-subniche-title">Персональные тренеры и нутрициологи <span class="mt-subniche-arrow">→</span></div>
              <div class="mt-subniche-desc">Персональный календарь тренировок, пакеты занятий, замеры прогресса, автонапоминания клиентам и ведение базы без блокнотов.</div>
            </div>
          </a>
          <a class="mt-subniche-card" href="/martial-arts">
            <div class="mt-subniche-icon">🥊</div>
            <div class="mt-subniche-content">
              <div class="mt-subniche-title">Клубы единоборств и бокса <span class="mt-subniche-arrow">→</span></div>
              <div class="mt-subniche-desc">Расписание рингов и татами, детские и взрослые группы, лимиты мест, учёт абонементов и заморозок на время сборов.</div>
            </div>
          </a>
        </div>
      </section>

      <!-- HEALTH JOURNEY -->
      <section class="mt-section mt-journey" data-screen-label="Путь визита пациента">
        <div class="mt-section-head mt-section-head--center" data-mt-reveal>
          <h2 class="mt-section-title">Один визит пациента. <span class="mt-hero-accent">Полный контроль в клинике.</span></h2>
          <p class="mt-section-sub">Посмотрите, как специализированная программа автоматизирует прием: от бронирования слота до фиксации протокола осмотра, автосписания медикаментов и прозрачного расчета зарплаты специалиста.</p>
        </div>

        <div class="mt-journey-example" aria-label="Пример прохождения записи" data-mt-reveal data-mt-delay="80">
          <span>Пример</span><strong>Первичная консультация + ЭКГ</strong><span>Терапевт Анна М. · Кабинет №1</span>
        </div>

        <div class="mt-journey-list">
          <article class="mt-journey-step">
            <div class="mt-journey-index">01</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Пациент</span>
              <h3>Онлайн-запись на прием без звонков администратору</h3>
              <p>Пациент выбирает специальность, врача и удобный интервал за 30 секунд через мессенджер или на сайте. Программа бронирует кабинет и временной слот нужной длительности с учетом регламента приема.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--booking" aria-label="Пример онлайн-записи">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Онлайн-запись</span>
                <span class="mt-journey-proof-badge">Подтверждена</span>
              </div>
              <div class="mt-journey-proof-row"><span>Пациент</span><strong>Сергей Васильев</strong></div>
              <div class="mt-journey-proof-row"><span>Специалист</span><strong>Терапевт Анна М.</strong></div>
              <div class="mt-journey-proof-row"><span>Кабинет</span><strong>Кабинет №1</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">02</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Врач / Специалист</span>
              <h3>Электронная карта и протокол осмотра за 2 минуты</h3>
              <p>Врач открывает электронную карту пациента со смартфона или планшета, изучает анамнез и вносит протокол осмотра и назначения в единую защищенную систему без бумажной рутины.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--process" aria-label="Карточка визита">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Прием #3124</span>
                <span class="mt-journey-proof-badge">Протокол заполнен</span>
              </div>
              <div class="mt-journey-proof-row"><span>Диагноз</span><strong>Первичный осмотр (здоров)</strong></div>
              <div class="mt-journey-proof-row"><span>ЭКГ</span><strong>Пленка сохранена в карте</strong></div>
              <div class="mt-journey-proof-row"><span>Врач</span><strong>Анна М. (высшая категория)</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">03</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Процедурный кабинет</span>
              <h3>Оказание услуг и автоматическое списание материалов</h3>
              <p>Во время приема проведены забор анализов и снятие ЭКГ. Программа автоматически списывает электроды, одноразовые простыни и антисептик со склада отделения по стандарту услуги.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--order" aria-label="Состав заказа">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Состав приема</span>
                <span class="mt-journey-proof-badge">К оплате</span>
              </div>
              <div class="mt-journey-proof-row"><span>Прием терапевта</span><strong>2 500 ₽</strong></div>
              <div class="mt-journey-proof-row"><span>Снятие и расшифровка ЭКГ</span><strong>1 000 ₽</strong></div>
              <div class="mt-journey-proof-row"><span>Итого прием</span><strong>3 500 ₽</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">04</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Система & Главврач</span>
              <h3>Оплата, памятка в мессенджер и начисление зарплаты врача</h3>
              <p>Пациент получает электронный чек и рекомендации врача в мессенджере. Программа моментально начисляет терапевту 40% (1 400 ₽) за прием — выработка рассчитывается без ручных таблиц и споров.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--payout" aria-label="Финансовый расчёт">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Расчёт врача</span>
                <span class="mt-journey-proof-badge">Начислено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Анна М. (40%)</span><strong>+1 400 ₽</strong></div>
              <div class="mt-journey-proof-row"><span>Списание со склада</span><strong>Расходники списаны</strong></div>
              <div class="mt-journey-proof-row"><span>Памятка в мессенджере</span><strong>«Рекомендации отправлены»</strong></div>
            </div>
          </article>
        </div>
      </section>

      <!-- REAL-WORLD CASE STUDY -->
      <section class="mt-case-section mt-reveal" data-screen-label="Кейс медицинского центра" data-mt-reveal>
        <div class="mt-case-card">
          <div class="mt-case-header">
            <div class="mt-case-tag">⚡ Кейс автоматизации клиники</div>
            <h2 class="mt-case-title">Медицинский центр «Гармония», 5 кабинетов</h2>
            <blockquote class="mt-case-quote">
              «Раньше администраторы путались в накладках врачей, а пациенты забывали о приемах. В Молнии мы настроили четкое расписание по кабинетам, электронные карты и Напоминания в мессенджер. Неявки снизились практически до нуля, а учет процедур и зарплат стал полностью автоматическим.»
            </blockquote>
            <div class="mt-case-author">
              Елена Романова <span>· Главный врач и управляющая, <span style="white-space:nowrap">Санкт-Петербург</span></span>
            </div>
          </div>
          <div class="mt-case-stats">
            <div class="mt-case-stat">
              <span class="mt-case-num">+38%</span>
              <span class="mt-case-label">Рост загрузки кабинетов благодаря плотной сетке записи</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">-88%</span>
              <span class="mt-case-label">Снижение пропусков приемов благодаря напоминаниям в мессенджере</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">0 <small>мин</small></span>
              <span class="mt-case-label">На ручной расчет зарплат врачей и сведение кассы смены</span>
            </div>
          </div>
        </div>
      </section>

      <!-- HEALTH FAQ -->
      <section id="faq" class="mt-section mt-reveal" data-screen-label="Вопросы и ответы" data-mt-reveal>
        <div class="mt-section-head">
          <h2 class="mt-section-title">Вопросы о программе для клиник, массажных студий и частных кабинетов</h2>
        </div>
        <div class="mt-before-start-grid">
          <article class="mt-before-start-highlight">
            <h3>Попробуйте CRM Молния для своей клиники или студии</h3>
            <p>Бесплатно поможем перенести базу пациентов из Excel или старой МИС, настроить расписание кабинетов, прайс-лист и схему зарплаты врачей. Начните прием без пауз в работе.</p>
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в мессенджер ↗</a>
          </article>
          <div class="mt-before-start-questions">
{faq_html}
          </div>
        </div>
        <p class="mt-before-start-privacy">Как мы обрабатываем данные — в <a href="/privacy">политике конфиденциальности</a>.</p>
      </section>

{lead_html}

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
'''
    return page_html


def build_spaces_page() -> str:
    """Builds the complete spaces landing page matching the exact design system."""
    nav_html = render_nav_html(active_item="spaces", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")
    lead_html = render_lead_form_html(
        "spaces",
        'Получите <span class="mt-hero-accent">бесплатный доступ навсегда</span> для своего пространства',
        "Оставьте контакты — поможем настроить онлайн-бронирование, сетку залов и шахматку для вашей площадки.",
    )

    title = "CRM для аренды пространств, коворкингов и залов — онлайн-бронирование и расписание Молния"
    description = (
        "Программа и CRM для аренды пространств, коворкингов, спортивных площадок, лофтов и фотостудий: "
        "онлайн-бронирование 24/7, интерактивная шахматка залов, учет предоплат и депозитов без овербукинга."
    )
    canonical = "https://molniya-tech.ru/spaces"

    faqs = [
        (
            "Подходит ли Молния для коворкингов, спортивных площадок, фотостудий и лофтов?",
            "Да. Система гибко настраивается под любой формат помещений: почасовая аренда залов, бронирование переговорных комнат, спортивных полей, рабочих мест в коворкинге или фотозон. Вы задаете собственные правила бронирования, минимальный шаг времени (например, 30 минут, 1 час или смена) и доступность оборудования.",
        ),
        (
            "Как система защищает от двойных бронирований (овербукинга)?",
            "Все бронирования — с сайта, из мессенджера, соцсетей или внесенные администратором вручную — мгновенно попадают в единый календарь в реальном времени. Если слот занят, клиент физически не может выбрать это время в виджете, что полностью исключает накладки и конфликты.",
        ),
        (
            "Можно ли настроить разные тарифы для разного времени суток и выходных дней?",
            "Да. В Молнии настраивается динамическое ценообразование: утренние часы со скидкой, вечерний прайм-тайм, повышенные тарифы на выходные и праздничные дни, а также специальные цены для постоянных резидентов и оптовых бронирований.",
        ),
        (
            "Как учитывается дополнительное оборудование и услуги (свет, проекторы, кейтеринг)?",
            "При бронировании площадки клиент или администратор может добавить к заказу нужное оборудование: звуковую аппаратуру, проектор, студийный свет, спортивный инвентарь или клининг. Система проверяет доступность оборудования и автоматически добавляет его стоимость к общему чеку.",
        ),
        (
            "Можно ли настроить буферное время на уборку и проветривание между бронями?",
            "Да. Вы можете задать обязательный технический перерыв (например, 15 или 30 минут) после каждой аренды. Система автоматически добавит это окно в расписание, чтобы персонал успел провести влажную уборку, проветрить зал или переставить мебель перед следующими гостями.",
        ),
        (
            "Как работает контроль предоплат, залогов и правил отмены?",
            "Программа фиксирует статус оплаты каждой брони: предоплата, остаток при входе, обеспечительный депозит (залог за имущество) или постоплата для корпоративных клиентов. В системе легко настроить политику отмен с автоматическим удержанием аванса при позднем отказе.",
        ),
        (
            "Как бесплатно перенести текущее расписание и базу клиентов из Excel или другой CRM?",
            "Служба заботы Молнии бесплатно помогает перенести данные постоянных резидентов, список залов, прайс-лист и текущую сетку броней из Google Таблиц, Excel или сторонних сервисов. Вы начнете работу в Молнии без остановки приёма заказов и без потери клиентов.",
        ),
    ]

    faq_html = "\n".join(
        f'            <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
        for q, a in faqs
    )

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://molniya-tech.ru/"},
                {"@type": "ListItem", "position": 2, "name": "Аренда пространств", "item": canonical},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Молния Тех — CRM и онлайн-бронирование пространств, коворкингов и залов",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web, iOS, Android, macOS, Windows",
            "url": canonical,
            "description": description,
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "RUB",
                "description": "Бесплатный демо-доступ и настройка расписания площадок",
            },
            "publisher": {
                "@type": "Organization",
                "name": "ООО «МОЛНИЯ ТЕХ»",
                "url": "https://molniya-tech.ru",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a,
                    },
                }
                for q, a in faqs
            ],
        },
    ]
    json_ld_str = json.dumps(json_ld, ensure_ascii=False)

    page_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#FAF7F2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#12100E" media="(prefers-color-scheme: dark)">
  <link rel="canonical" href="{canonical}">

  <!-- Favicons -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- HERO -->
      <section class="mt-hero" data-screen-label="Герой" data-mt-hero-scene>

        <div class="mt-hero-lead">
          <h1 class="mt-hero-title">
            CRM для аренды пространств,<br><span class="mt-hero-accent">коворкингов, площадок и залов</span>
          </h1>

          <div class="mt-hero-bottom">
            <div class="mt-hero-intro">
              <p class="mt-hero-sub">Онлайн-бронирование 24/7, интерактивная шахматка залов, учет предоплат и защита от двойных броней</p>
              <a class="mt-btn mt-btn-hero" href="#contact">Получить бесплатный доступ</a>
            </div>

            <ul class="mt-facets mt-facets--full" aria-label="Преимущества для аренды пространств">
              <li class="mt-facet">
                <span class="mt-facet-name">Залы и зоны</span>
                <span class="mt-facet-note">почасовое онлайн-бронирование 24/7</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Без овербукинга</span>
                <span class="mt-facet-note">единый календарь и защита от накладок</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Депозиты и чеки</span>
                <span class="mt-facet-note">учет предоплат, залогов и оборудования</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name mt-facet-name--soon">AI & Комьюнити</span>
                <span class="mt-facet-note">Напоминания в мессенджер и повторные брони</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <div class="mt-tablet">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для аренды пространств и залов: шахматка броней и электронное расписание" width="1710" height="983" fetchpriority="high">
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </div>
            <p class="mt-hero-media-caption">Интерактивная шахматка броней и загрузка площадок в реальном времени</p>
          </div>
        </div>

      </section>

      <!-- LIVE SPACES STATUS -->
      <section class="mt-section mt-reveal" data-screen-label="Загрузка залов и площадок" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Все залы, слоты и арендаторы <span class="mt-overview-hook">под полным контролем</span></h2>
          <p class="mt-section-sub">Администратор и управляющий видят текущий статус каждого зала, имя арендатора, заказанное оборудование и сумму чека в реальном времени на любом устройстве.</p>
        </div>

        <div class="mt-auto-bays">
          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Зал 1 · Фотостудия «Лофт»</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В аренде</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Екатерина В. (14:00–17:00)</div>
                <div class="mt-auto-car-tier">Съемка лукбука · Циклорама + Свет</div>
              </div>
              <span class="mt-dropdown-footer-icon">📸</span>
            </div>
            <div class="mt-auto-service">
              <span>Аренда 3ч + Оборудование</span>
              <span class="mt-auto-price">8 400 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Поле 1 · Футбольная арена</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В игре</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">ФК «Метеор» (18:30–20:00)</div>
                <div class="mt-auto-car-tier">Матч 8×8 · Судейство + Инвентарь</div>
              </div>
              <span class="mt-dropdown-footer-icon">⚽</span>
            </div>
            <div class="mt-auto-service">
              <span>Поле 1.5ч + Раздевалки</span>
              <span class="mt-auto-price">6 500 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Зал 2 · Лекторий & Коворкинг</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--done">Готово</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Product Club (11:00–13:30)</div>
                <div class="mt-auto-car-tier">Митап 40 мест · Проектор + Звук</div>
              </div>
              <span class="mt-dropdown-footer-icon">🎤</span>
            </div>
            <div class="mt-auto-service">
              <span>Конференц-зал (оплачено)</span>
              <span class="mt-auto-price">14 000 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Зал 3 · Танцевальный зал</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--wait">Ожидание</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Анна С. (20:00–21:30)</div>
                <div class="mt-auto-car-tier">Репетиция соло · Зеркала + Звук</div>
              </div>
              <span class="mt-dropdown-footer-icon">💃</span>
            </div>
            <div class="mt-auto-service">
              <span>Аренда зала (аванс 50%)</span>
              <span class="mt-auto-price">3 000 ₽</span>
            </div>
          </div>
        </div>
      </section>

      <!-- SPACES OVERVIEW VALUE GRID -->
      <section class="mt-section mt-section--overview mt-reveal" data-screen-label="Функции для аренды пространств" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Управляйте арендой площадок <span class="mt-overview-hook">от первой заявки до сдачи зала</span></h2>
          <p class="mt-section-sub">Программа для учета бронирования залов, коворкингов, спортивных площадок и лофтов: интерактивная шахматка броней, онлайн-виджет, учет залогов и доп. оборудования без ручных таблиц.</p>
        </div>

        <div class="mt-overview-grid">
          <article class="mt-overview-card">
            <h3><span class="mt-overview-hook">Шахматка броней</span> и расписание залов</h3>
            <p>Наглядная календарная сетка по залам и часам. Бронирование в один клик, легкий перенос времени drag-and-drop и разделение по статусам: предоплата, подтверждено, завершено. Овербукинг исключен.</p>
            <div class="mt-overview-preview mt-overview-preview--schedule" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Шахматка залов</span><span>Сегодня</span></div>
              <div class="mt-overview-calendar"><span>09:00</span><div></div><span>11:00</span><div class="mt-overview-slot">Зал «Лофт» <small>Фотосессия · 11:00–14:00</small></div><span>15:00</span><div class="mt-overview-slot mt-overview-slot--light">Лекторий <small>Семинар · 15:00–18:00</small></div></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Онлайн-виджет бронирования <span class="mt-overview-hook">и бот в мессенджере</span></h3>
            <p>Клиенты сами видят свободные окна и бронируют слоты на сайте или в мессенджере 24/7. Никаких бесконечных переписок в мессенджерах: система сама покажет фото зала, стоимость и правила аренды.</p>
            <div class="mt-overview-preview mt-overview-preview--process" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Онлайн-бронь</span><span>Зал «Циклорама»</span></div>
              <div class="mt-overview-stages"><span>Выбор зала</span><i></i><span>Слот</span><i></i><span>Предоплата</span></div>
              <div class="mt-overview-check">✓ <span>Слот зарезервирован на 3 часа</span></div>
              <div class="mt-overview-check">✓ <span>Предоплата 50% внесена онлайн</span></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Учет оборудования, света <span class="mt-overview-hook">и инвентаря</span></h3>
            <p>Сдавайте вместе с залом проекторы, микрофоны, импульсный свет, мячи или наборы для кофе-брейка. Молния контролирует доступность техники и предотвращает двойную аренду одного аппарата.</p>
            <div class="mt-overview-preview mt-overview-preview--prices" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Оборудование и опции</span><span>Доступно к аренде</span></div>
              <div class="mt-overview-price-row"><span>Студийный свет Profoto (2 шт.)</span><strong>В наличии · Зал 1</strong></div>
              <div class="mt-overview-price-row"><span>Лазерный проектор 4K</span><strong>Свободен</strong></div>
              <div class="mt-overview-price-tag">Автопроверка занятости оборудования</div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Напоминания в мессенджер арендаторам <span class="mt-overview-hook">и правила отмены</span></h3>
            <p>Бот отправляет гостям код от двери или схему проезда, напоминает о времени визита за 24 и 2 часа и запрашивает подтверждение. Неявки снижаются на 85%, а отмены происходят строго по регламенту.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Напоминание арендатору</span><span>Мессенджер</span></div>
              <div class="mt-overview-message">
                Екатерина, напоминаем о брони зала «Лофт» завтра в 14:00. Код от домофона: 4821#. Пожалуйста, подтвердите визит.
                <span class="mt-overview-reaction">🏟️</span>
              </div>
              <div class="mt-overview-client-row"><span>База резидентов и гостей</span><strong>История броней и депозиты →</strong></div>
            </div>
          </article>

          <article class="mt-overview-card mt-overview-card--featured">
            <h3>Контроль предоплат, депозитов <span class="mt-overview-hook">и прозрачные отчёты</span></h3>
            <p>Полный финансовый учет: авансы, остатки при входе, обеспечительные залоги за сохранность интерьера и почасовая выработка администраторов смен. Вся аналитика загрузки площадок на одном экране.</p>
            <div class="mt-overview-preview mt-overview-preview--metrics" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Загрузка площадки</span><span>Недельный отчет</span></div>
              <div class="mt-overview-metrics"><span>Занятость<b>78%</b></span><span>Предоплаты<b>100%</b></span><span>Выручка<b>₽</b></span></div>
              <div class="mt-overview-chart"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            </div>
          </article>
        </div>

        <div class="mt-overview-action">
          <a class="mt-btn mt-btn-cta" href="#contact">Получить бесплатный доступ</a>
        </div>
      </section>

      <!-- SPACES JOURNEY -->
      <section class="mt-section mt-journey" data-screen-label="Путь бронирования пространства">
        <div class="mt-section-head mt-section-head--center" data-mt-reveal>
          <h2 class="mt-section-title">Одна бронь площадки. <span class="mt-hero-accent">Полный порядок в пространстве.</span></h2>
          <p class="mt-section-sub">Посмотрите, как система автоматизирует работу администратора: от выбора слота в виджете до подготовки зала, сдачи оборудования и возврата страхового депозита.</p>
        </div>

        <div class="mt-journey-example" aria-label="Пример прохождения бронирования" data-mt-reveal data-mt-delay="80">
          <span>Пример</span><strong>Аренда фотостудии на 3 часа</strong><span>Зал «Лофт» · Екатерина В.</span>
        </div>

        <div class="mt-journey-list">
          <article class="mt-journey-step">
            <div class="mt-journey-index">01</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Арендатор</span>
              <h3>Онлайн-бронирование слота за 60 секунд</h3>
              <p>Клиент выбирает нужный зал, дату, время и дополнительный комплект света через онлайн-виджет. Слот мгновенно блокируется в расписании, исключая накладки.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--booking" aria-label="Пример онлайн-бронирования">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Онлайн-бронирование</span>
                <span class="mt-journey-proof-badge">Подтверждено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Арендатор</span><strong>Екатерина Васильева</strong></div>
              <div class="mt-journey-proof-row"><span>Пространство</span><strong>Зал «Лофт» (3 часа)</strong></div>
              <div class="mt-journey-proof-row"><span>Оборудование</span><strong>Комплект Profoto + Циклорама</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">02</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Администратор</span>
              <h3>Внесение предоплаты и подготовка помещения</h3>
              <p>Арендатор вносит предоплату, а администратор видит бронь в шахматке и автоматически получает список необходимого оборудования к назначенному времени.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--process" aria-label="Карточка бронирования">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Бронь #1842</span>
                <span class="mt-journey-proof-badge">Предоплата 50%</span>
              </div>
              <div class="mt-journey-proof-row"><span>Сумма заказа</span><strong>8 400 ₽ (аванс 4 200 ₽)</strong></div>
              <div class="mt-journey-proof-row"><span>Чек-лист зала</span><strong>Свет установлен, чисто</strong></div>
              <div class="mt-journey-proof-row"><span>Статус</span><strong>Готов к приему гостей</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">03</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Администратор & Гость</span>
              <h3>Встреча гостей, доплата и залог за сохранность</h3>
              <p>Гость прибывает на площадку. Администратор отмечает приход в один тап на планшете, принимает доплату и фиксирует залог за сохранность интерьера.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--order" aria-label="Фиксация расчёта">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Оплата на входе</span>
                <span class="mt-journey-proof-badge">Оплачено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Доплата за аренду</span><strong>4 200 ₽</strong></div>
              <div class="mt-journey-proof-row"><span>Страховой депозит</span><strong>5 000 ₽ (на удержании)</strong></div>
              <div class="mt-journey-proof-row"><span>Итого принято</span><strong>9 200 ₽</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">04</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Система & Управляющий</span>
              <h3>Освобождение зала, возврат залога и финансовый отчёт</h3>
              <p>Администратор проверяет зал, закрывает бронь и возвращает депозит. Система автоматически закладывает 20 минут буфера на клининг и начисляет смену администратору.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--payout" aria-label="Завершение заказа">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Завершение брони</span>
                <span class="mt-journey-proof-badge">Успешно</span>
              </div>
              <div class="mt-journey-proof-row"><span>Депозит 5 000 ₽</span><strong>Возвращен клиенту</strong></div>
              <div class="mt-journey-proof-row"><span>Выручка площадки</span><strong>+8 400 ₽ в кассу</strong></div>
              <div class="mt-journey-proof-row"><span>Буфер на клининг</span><strong>20 мин (до 17:20)</strong></div>
            </div>
          </article>
        </div>
      </section>

      <!-- REAL-WORLD CASE STUDY -->
      <section class="mt-case-section mt-reveal" data-screen-label="Кейс аренды пространств" data-mt-reveal>
        <div class="mt-case-card">
          <div class="mt-case-header">
            <div class="mt-case-tag">⚡ Кейс автоматизации пространства</div>
            <h2 class="mt-case-title">Креативный кластер «Среда», 4 зала и лекторий</h2>
            <blockquote class="mt-case-quote">
              «Раньше мы теряли клиентов по ночам и по выходным: люди писали в WhatsApp, а администраторы отвечали через несколько часов. После перехода на Молнию гости сами бронируют слоты и вносят предоплату на сайте. Накладки прекратились, а полезная загрузка залов выросла более чем на 40%.»
            </blockquote>
            <div class="mt-case-author">
              Максим Ковалёв <span>· Управляющий пространством, <span style="white-space:nowrap">Москва</span></span>
            </div>
          </div>
          <div class="mt-case-stats">
            <div class="mt-case-stat">
              <span class="mt-case-num">+42%</span>
              <span class="mt-case-label">Рост полезной загрузки залов благодаря круглосуточному онлайн-виджету</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">0</span>
              <span class="mt-case-label">Двойных бронирований и конфликтов по времени за всё время работы</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">15 <small>мин</small></span>
              <span class="mt-case-label">На перенос расписания, настройку тарифов и запуск системы в работу</span>
            </div>
          </div>
        </div>
      </section>

      <!-- SPACES FAQ -->
      <section id="faq" class="mt-section mt-reveal" data-screen-label="Вопросы и ответы" data-mt-reveal>
        <div class="mt-section-head">
          <h2 class="mt-section-title">Вопросы о программе для аренды пространств, коворкингов и залов</h2>
        </div>
        <div class="mt-before-start-grid">
          <article class="mt-before-start-highlight">
            <h3>Попробуйте CRM Молния для своего пространства</h3>
            <p>Бесплатно поможем настроить календарную сетку залов, тарифы по часам и дням недели, каталог оборудования и правила предоплаты. Начните принимать онлайн-брони уже сегодня.</p>
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в мессенджер ↗</a>
          </article>
          <div class="mt-before-start-questions">
{faq_html}
          </div>
        </div>
        <p class="mt-before-start-privacy">Как мы обрабатываем данные — в <a href="/privacy">политике конфиденциальности</a>.</p>
      </section>

{lead_html}

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
'''
    return page_html


def build_photostudios_page() -> str:
    """Builds the complete photostudios landing page matching the exact design system."""
    nav_html = render_nav_html(active_item="photostudios", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")
    lead_html = render_lead_form_html(
        "photostudios",
        'Получите <span class="mt-hero-accent">бесплатный доступ навсегда</span> для своей фотостудии',
        "Оставьте контакты — поможем настроить онлайн-бронирование залов, циклорам, гримерок и каталог света.",
    )

    title = "CRM для фотостудий и видеопавильонов — онлайн-бронирование залов и расписание Молния"
    description = (
        "Программа и CRM для фотостудий, циклорам, видеопавильонов и аренды оборудования: "
        "онлайн-бронирование 24/7, шахматка залов, учет света и предоплат без овербукинга."
    )
    canonical = "https://molniya-tech.ru/photostudios"

    faqs = [
        (
            "Подходит ли Молния для интерьерных фотостудий, циклорам и видеопавильонов?",
            "Да. Система спроектирована специально под студийный бизнес: почасовое бронирование съемочных залов, отдельных гримёрных мест, хромакей-павильонов и подкастных студий. Вы можете задать минимальный порог брони (от 1 или 2 часов), шаг времени (30 или 60 минут), правила использования оборудования и расценки на ночные смены.",
        ),
        (
            "Как система исключает овербукинг и двойные бронирования залов?",
            "Все бронирования — с сайта, через виджет онлайн-записи, из соцсетей, Telegram или созданные администратором вручную — мгновенно попадают в единую шахматку в реальном времени. Если слот занят или забронирован под технический перерыв, клиент физически не сможет его выбрать. Овербукинг исключен на 100%.",
        ),
        (
            "Можно ли бронировать гримёрку отдельно или до начала съемки?",
            "Да. Гримёрные столы можно настроить как самостоятельный ресурс с отдельным тарифом или предлагать как бесплатную опцию за 1–2 часа до начала брони зала. Администратор всегда видит на шахматке, занята ли гримёрка и к какому съемочному залу привязана фотосессия.",
        ),
        (
            "Как устроен учет аренды студийного света, насадок и расходников (бумажные фоны)?",
            "При бронировании зала фотограф может добавить импульсные моноблоки, постоянный свет, цветные фильтры, насадки, дым-машину, отпариватель или раскатку бумажного фона. Система автоматически проверяет наличие техники на складе, исключает выдачу одного прибора в два разных зала и включает стоимость в общий чек.",
        ),
        (
            "Можно ли настроить разные цены на будни, выходные, прайм-тайм и ночные смены?",
            "Да. В Молнии настраивается гибкое динамическое ценообразование: повышенные тарифы на вечерние часы и выходные дни, пакетные предложения на ночные съемки (пакет 6–8 часов), скидки на утренние слоты и спеццены для постоянных фотографов и фотошкол.",
        ),
        (
            "Как контролируются онлайн-предоплаты, правила отмены брони и штрафы?",
            "Система автоматически фиксирует онлайн-предоплату (например, 50% или 100%) при бронировании через виджет. Вы задаете правила бесплатной отмены (например, не позднее чем за 72 часа). При поздней отмене система удерживает аванс по регламенту студии. Также можно учитывать обеспечительный депозит на случай загрязнения циклорамы.",
        ),
        (
            "Как бесплатно перенести расписание и базу фотографов из AppEvent, YClients или Excel?",
            "Служба заботы Молнии бесплатно перенесет базу постоянных фотографов, список съемочных залов, прайс-лист техники и текущую сетку броней из Google Таблиц, AppEvent, YClients или других сервисов. Перенос займет около 15 минут, и вы начнете работу без потери бронирований.",
        ),
    ]

    faq_html = "\n".join(
        f'            <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
        for q, a in faqs
    )

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://molniya-tech.ru/"},
                {"@type": "ListItem", "position": 2, "name": "Фотостудии", "item": canonical},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Молния Тех — CRM и онлайн-бронирование для фотостудий и видеопавильонов",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web, iOS, Android, macOS, Windows",
            "url": canonical,
            "description": description,
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "RUB",
                "description": "Бесплатный демо-доступ и настройка расписания студии",
            },
            "publisher": {
                "@type": "Organization",
                "name": "ООО «МОЛНИЯ ТЕХ»",
                "url": "https://molniya-tech.ru",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a,
                    },
                }
                for q, a in faqs
            ],
        },
    ]
    json_ld_str = json.dumps(json_ld, ensure_ascii=False)

    page_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#FAF7F2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#12100E" media="(prefers-color-scheme: dark)">
  <link rel="canonical" href="{canonical}">

  <!-- Favicons -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- HERO -->
      <section class="mt-hero" data-screen-label="Герой" data-mt-hero-scene>

        <div class="mt-hero-lead">
          <h1 class="mt-hero-title">
            CRM для фотостудий,<br><span class="mt-hero-accent">видеопавильонов и аренды залов</span>
          </h1>

          <div class="mt-hero-bottom">
            <div class="mt-hero-intro">
              <p class="mt-hero-sub">Онлайн-бронирование 24/7, интерактивная шахматка залов, учет света и техники, напоминания арендаторам и защита от накладок</p>
              <a class="mt-btn mt-btn-hero" href="#contact">Получить бесплатный доступ</a>
            </div>

            <ul class="mt-facets mt-facets--full" aria-label="Преимущества для фотостудий">
              <li class="mt-facet">
                <span class="mt-facet-name">Залы и циклорамы</span>
                <span class="mt-facet-note">почасовое онлайн-бронирование 24/7</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Без овербукинга</span>
                <span class="mt-facet-note">шахматка в реальном времени и защита от накладок</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Свет и гримерки</span>
                <span class="mt-facet-note">учет приборов, насадок, фонов и гримёрных мест</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name mt-facet-name--soon">AI & Напоминания</span>
                <span class="mt-facet-note">автосообщения в мессенджер с кодом двери и правилами</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <div class="mt-tablet">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для фотостудий: шахматка броней съемочных залов и расписание" width="1710" height="983" fetchpriority="high">
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </div>
            <p class="mt-hero-media-caption">Интерактивная шахматка броней студии и загрузка залов в реальном времени</p>
          </div>
        </div>

      </section>

      <!-- LIVE STUDIOS STATUS -->
      <section class="mt-section mt-reveal" data-screen-label="Загрузка залов студии" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Все залы, циклорамы и свет <span class="mt-overview-hook">под полным контролем</span></h2>
          <p class="mt-section-sub">Администратор видит текущий статус каждого зала, имя фотографа, заказанный свет, насадки и сумму оплаты в реальном времени на компьютере или смартфоне.</p>
        </div>

        <div class="mt-auto-bays">
          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Зал 1 · Циклорама White (65 м²)</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В аренде</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Алина В. (13:00–16:00)</div>
                <div class="mt-auto-car-tier">Съемка каталога · 3× Profoto D2 + Октобокс 150</div>
              </div>
              <span class="mt-dropdown-footer-icon">📸</span>
            </div>
            <div class="mt-auto-service">
              <span>Циклорама 3ч + Оборудование</span>
              <span class="mt-auto-price">7 800 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Зал 2 · Интерьерный «Лофт» (80 м²)</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В аренде</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Михаил Т. (15:00–17:00)</div>
                <div class="mt-auto-car-tier">Семейная съемка · Естественный свет + Отражатель</div>
              </div>
              <span class="mt-dropdown-footer-icon">🛋️</span>
            </div>
            <div class="mt-auto-service">
              <span>Зал «Лофт» 2ч + Гримерка</span>
              <span class="mt-auto-price">5 400 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Зал 3 · Хромакей & Видеопавильон</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--done">Готово</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Production Hub (10:00–13:00)</div>
                <div class="mt-auto-car-tier">Запись подкаста · 3× Aputure 300d + Петлички</div>
              </div>
              <span class="mt-dropdown-footer-icon">🎬</span>
            </div>
            <div class="mt-auto-service">
              <span>Видеостудия 3ч (оплачено)</span>
              <span class="mt-auto-price">13 500 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Зал 4 · Темный зал & Неон (50 м²)</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--wait">Ожидание</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Роман С. (18:00–21:00)</div>
                <div class="mt-auto-car-tier">Клип / Арт · Nanlite Pavotube + Дым-машина</div>
              </div>
              <span class="mt-dropdown-footer-icon">💡</span>
            </div>
            <div class="mt-auto-service">
              <span>Темный зал (аванс 100%)</span>
              <span class="mt-auto-price">9 000 ₽</span>
            </div>
          </div>
        </div>
      </section>

      <!-- PHOTOSTUDIOS OVERVIEW VALUE GRID -->
      <section class="mt-section mt-section--overview mt-reveal" data-screen-label="Функции для фотостудий" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Управляйте фотостудией <span class="mt-overview-hook">от первой заявки до сдачи зала</span></h2>
          <p class="mt-section-sub">Программа для учета бронирования залов фотостудии: интерактивная шахматка броней, онлайн-виджет, учет света, насадок и предоплат без ручных блокнотов и таблиц.</p>
        </div>

        <div class="mt-overview-grid">
          <article class="mt-overview-card">
            <h3><span class="mt-overview-hook">Шахматка броней</span> и расписание залов</h3>
            <p>Наглядная календарная сетка по залам и часам. Бронирование в один клик, легкий перенос времени drag-and-drop и цветовые статусы: предоплата, подтверждено, завершено. Овербукинг исключен.</p>
            <div class="mt-overview-preview mt-overview-preview--schedule" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Шахматка студии</span><span>Сегодня</span></div>
              <div class="mt-overview-calendar"><span>10:00</span><div></div><span>12:00</span><div class="mt-overview-slot">Циклорама <small>Лукбук · 12:00–15:00</small></div><span>16:00</span><div class="mt-overview-slot mt-overview-slot--light">Зал «Лофт» <small>Фотосессия · 16:00–18:00</small></div></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Онлайн-виджет бронирования <span class="mt-overview-hook">и бот в мессенджере</span></h3>
            <p>Фотографы и заказчики сами выбирают свободные слоты на сайте или в Telegram 24/7. Никаких ночных переписок: система покажет интерьер зала, свободные окна, доступный свет и примет предоплату.</p>
            <div class="mt-overview-preview mt-overview-preview--process" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Онлайн-бронь</span><span>Зал «Циклорама White»</span></div>
              <div class="mt-overview-stages"><span>Выбор даты</span><i></i><span>Слот</span><i></i><span>Свет</span><i></i><span>Оплата</span></div>
              <div class="mt-overview-check">✓ <span>Слот 13:00–16:00 зарезервирован</span></div>
              <div class="mt-overview-check">✓ <span>Предоплата 50% принята автоматически</span></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Учет оборудования, света <span class="mt-overview-hook">и гримерных мест</span></h3>
            <p>Сдавайте вместе с залом импульсные моноблоки, постоянный свет, цветные фильтры, насадки, дым-машину или гримерку. Молния контролирует склад и предотвращает выдачу одного прибора в два зала.</p>
            <div class="mt-overview-preview mt-overview-preview--prices" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Склад студии</span><span>Свет и оборудование</span></div>
              <div class="mt-overview-price-row"><span>Profoto D2 500 AirTTL (3 шт.)</span><strong>Забронировано · Зал 1</strong></div>
              <div class="mt-overview-price-row"><span>Aputure 300d II + Софтбокс</span><strong>Свободно · Склад</strong></div>
              <div class="mt-overview-price-tag">Автоконтроль занятости приборов</div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Напоминания арендаторам <span class="mt-overview-hook">и правила студии</span></h3>
            <p>Бот отправляет фотографу код от двери, правила сменной обуви и схему проезда, напоминает о визите за 24 и 2 часа. Неявки снижаются на 85%, а отмены происходят строго по регламенту студии.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Сообщение фотографу</span><span>Мессенджер</span></div>
              <div class="mt-overview-message">
                Алина, ждем вас на съемку в зал «Циклорама» завтра в 13:00. Код от домофона: 2914#. Напоминаем о сменной обуви.
                <span class="mt-overview-reaction">📸</span>
              </div>
              <div class="mt-overview-client-row"><span>База фотографов</span><strong>История броней и скидки →</strong></div>
            </div>
          </article>

          <article class="mt-overview-card mt-overview-card--featured">
            <h3>Контроль предоплат, депозитов <span class="mt-overview-hook">и финансовые отчёты</span></h3>
            <p>Полный финансовый учет: авансы, доплата на входе, депозиты за покраску циклорамы, учет раскатки бумажных фонов и зарплата администраторов смен. Вся аналитика загрузки залов на одном экране.</p>
            <div class="mt-overview-preview mt-overview-preview--metrics" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Загрузка фотостудии</span><span>Недельный отчет</span></div>
              <div class="mt-overview-metrics"><span>Занятость<b>82%</b></span><span>Предоплаты<b>100%</b></span><span>Выручка<b>₽</b></span></div>
              <div class="mt-overview-chart"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            </div>
          </article>
        </div>

        <div class="mt-overview-action">
          <a class="mt-btn mt-btn-cta" href="#contact">Получить бесплатный доступ</a>
        </div>
      </section>

      <!-- PHOTOSTUDIOS JOURNEY -->
      <section class="mt-section mt-journey" data-screen-label="Путь бронирования фотостудии">
        <div class="mt-section-head mt-section-head--center" data-mt-reveal>
          <h2 class="mt-section-title">Одна бронь студии. <span class="mt-hero-accent">Полный порядок в съемочных залах.</span></h2>
          <p class="mt-section-sub">Посмотрите, как система автоматизирует работу администратора: от выбора слота в виджете до подготовки света, встречи команды и сдачи зала без задержек.</p>
        </div>

        <div class="mt-journey-example" aria-label="Пример прохождения бронирования" data-mt-reveal data-mt-delay="80">
          <span>Пример</span><strong>Аренда циклорамы на 3 часа</strong><span>Зал White · Алина В.</span>
        </div>

        <div class="mt-journey-list">
          <article class="mt-journey-step">
            <div class="mt-journey-index">01</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Фотограф</span>
              <h3>Онлайн-бронирование зала и света за 60 секунд</h3>
              <p>Клиент выбирает нужный зал, дату, время и необходимый комплект источников света через онлайн-виджет. Слот мгновенно блокируется в расписании, исключая накладки.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--booking" aria-label="Пример онлайн-бронирования">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Онлайн-бронирование</span>
                <span class="mt-journey-proof-badge">Подтверждено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Арендатор</span><strong>Алина Васильева</strong></div>
              <div class="mt-journey-proof-row"><span>Съемочный зал</span><strong>Циклорама White (3 часа)</strong></div>
              <div class="mt-journey-proof-row"><span>Оборудование</span><strong>3× Profoto D2 + Октобокс 150</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">02</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Администратор</span>
              <h3>Подтверждение предоплаты и подготовка зала</h3>
              <p>Фотограф вносит предоплату, а администратор видит бронь в шахматке и заранее готовит зал: выкатывает моноблоки, насадки, стойки и проверяет чистоту циклорамы.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--process" aria-label="Карточка бронирования">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Бронь #2419</span>
                <span class="mt-journey-proof-badge">Предоплата 50%</span>
              </div>
              <div class="mt-journey-proof-row"><span>Сумма заказа</span><strong>7 800 ₽ (аванс 3 900 ₽)</strong></div>
              <div class="mt-journey-proof-row"><span>Чек-лист зала</span><strong>Циклорама чистая, свет собран</strong></div>
              <div class="mt-journey-proof-row"><span>Статус</span><strong>Зал готов к съемке</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">03</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Администратор & Съемочная группа</span>
              <h3>Встреча команды, доплата и запуск таймера съемки</h3>
              <p>Команда прибывает на площадку. Администратор отмечает приход в один тап на планшете, принимает доплату и фиксирует стартовое состояние зала и циклорамы.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--order" aria-label="Фиксация расчёта">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Оплата на ресепшн</span>
                <span class="mt-journey-proof-badge">Оплачено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Доплата за зал</span><strong>3 900 ₽</strong></div>
              <div class="mt-journey-proof-row"><span>Раскатка фона</span><strong>1 000 ₽ (1 метр)</strong></div>
              <div class="mt-journey-proof-row"><span>Итого принято</span><strong>4 900 ₽</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">04</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Система & Управляющий</span>
              <h3>Сдача оборудования, буфер на клининг и финансовый отчёт</h3>
              <p>Администратор проверяет технику, закрывает бронь и система закладывает обязательный буфер 15 минут на уборку и проветривание перед следующей съемкой.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--payout" aria-label="Завершение заказа">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Завершение съемки</span>
                <span class="mt-journey-proof-badge">Успешно</span>
              </div>
              <div class="mt-journey-proof-row"><span>Оборудование</span><strong>Сдано без повреждений</strong></div>
              <div class="mt-journey-proof-row"><span>Выручка с брони</span><strong>+8 800 ₽ в кассу</strong></div>
              <div class="mt-journey-proof-row"><span>Буфер на клининг</span><strong>15 мин (до 16:15)</strong></div>
            </div>
          </article>
        </div>
      </section>

      <!-- REAL-WORLD CASE STUDY -->
      <section class="mt-case-section mt-reveal" data-screen-label="Кейс фотостудии" data-mt-reveal>
        <div class="mt-case-card">
          <div class="mt-case-header">
            <div class="mt-case-tag">⚡ Кейс автоматизации фотостудии</div>
            <h2 class="mt-case-title">Фотостудия «Монохром», 4 съемочных зала и видеопавильон</h2>
            <blockquote class="mt-case-quote">
              «До Молнии мы вели запись через переписки в Telegram и WhatsApp, тратя по 4 часа в день на согласование свободных слотов. Из-за путаницы случались накладки по оборудованию: один октобокс обещали двум фотографам. С переходом на Молнию 80% броней приходят через круглосуточный виджет с моментальной предоплатой. Накладки исчезли полностью, а выручка выросла на 38%.»
            </blockquote>
            <div class="mt-case-author">
              Артем Лебедев <span>· Совладелец студии «Монохром», <span style="white-space:nowrap">Санкт-Петербург</span></span>
            </div>
          </div>
          <div class="mt-case-stats">
            <div class="mt-case-stat">
              <span class="mt-case-num">+38%</span>
              <span class="mt-case-label">Рост выручки студии благодаря круглосуточному онлайн-виджету без потерь заявок</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">0</span>
              <span class="mt-case-label">Накладок по залам и задвоенных бронирований света за всё время работы</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">15 <small>мин</small></span>
              <span class="mt-case-label">На перенос базы фотографов, настройку каталога техники и запуск в работу</span>
            </div>
          </div>
        </div>
      </section>

      <!-- PHOTOSTUDIOS FAQ -->
      <section id="faq" class="mt-section mt-reveal" data-screen-label="Вопросы и ответы" data-mt-reveal>
        <div class="mt-section-head">
          <h2 class="mt-section-title">Вопросы о программе для фотостудий и видеопавильонов</h2>
        </div>
        <div class="mt-before-start-grid">
          <article class="mt-before-start-highlight">
            <h3>Попробуйте CRM Молния для своей фотостудии</h3>
            <p>Бесплатно поможем настроить календарную шахматку залов, тарифы по часам и дням недели, каталог света и правила предоплаты. Начните принимать онлайн-брони уже сегодня.</p>
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в мессенджер ↗</a>
          </article>
          <div class="mt-before-start-questions">
{faq_html}
          </div>
        </div>
        <p class="mt-before-start-privacy">Как мы обрабатываем данные — в <a href="/privacy">политике конфиденциальности</a>.</p>
      </section>

{lead_html}

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
'''
    return page_html


def build_cleaning_page() -> str:
    """Builds the complete cleaning landing page matching the exact design system."""
    nav_html = render_nav_html(active_item="cleaning", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")
    lead_html = render_lead_form_html(
        "cleaning",
        'Получите <span class="mt-hero-accent">бесплатный доступ навсегда</span> для клининговой компании',
        "Оставьте контакты — поможем настроить калькулятор уборки, расписание выездных бригад и расчет зарплат.",
    )

    title = "CRM для клининга и выездных бригад — программа учета уборок и онлайн-запись Молния"
    description = (
        "Программа и CRM для клининговых компаний, выездных бригад, уборки квартир и химчистки: "
        "онлайн-запись 24/7, расписание клинеров, калькулятор метража и сдельная зарплата."
    )
    canonical = "https://molniya-tech.ru/cleaning"

    faqs = [
        (
            "Подходит ли Молния для уборки квартир, офисов, химчистки мебели и мытья окон?",
            "Да. Система универсально подходит для любых форматов клининга: поддерживающая, генеральная и послеремонтная уборка, мойка окон и фасадов, выездная химчистка мягкой мебели и ковров, а также регулярный B2B-клининг коммерческих помещений. Вы можете настроить расчет стоимости по квадратным метрам, комнатам или фиксированным пакетам.",
        ),
        (
            "Как система рассчитывает стоимость уборки и время работы бригады?",
            "В онлайн-виджете клиент указывает тип уборки, площадь или количество комнат и санузлов, а также выбирает дополнительные опции (мытье духовки, холодильника, окон, глажка). Молния мгновенно рассчитывает точную стоимость и нормочасы работы, автоматически бронируя нужное окно в графике выездных бригад.",
        ),
        (
            "Как устроен сдельный расчет зарплаты клинеров и бригадиров?",
            "Для каждого клинера можно задать индивидуальные условия оплаты: процент от суммы выполненного заказа (например, 35–45%), фиксированную ставку за смену или доплату за сложные опции. Программа автоматически рассчитывает зарплату каждого сотрудника сразу после закрытия заказ-наряда и формирует ведомости на выплату.",
        ),
        (
            "Как исключить опоздания и накладки в расписании выездных бригад?",
            "Система учитывает время на дорогу между адресами в одном районе и автоматически закладывает технический буфер между заказами. Бригадир видит маршрутный лист, адрес, контактные данные клиента и список необходимых расходников прямо со смартфона, что сводит задержки к минимуму.",
        ),
        (
            "Можно ли вести учет профессиональной химии, расходников и инвентаря?",
            "Да. В Молнии есть модуль склада: вы можете списывать химию и расходные материалы по технологическим картам на каждую уборку (например, салфетки, перчатки, спецсредства), а также контролировать закрепление дорогостоящей техники (экстракторы, строительные пылесосы, парогенераторы) за конкретными бригадами.",
        ),
        (
            "Как работают напоминания клиентам и контроль качества уборки?",
            "Сервисный Telegram-бот автоматически отправляет клиенту напоминание накануне визита, сообщает статус «Бригада выехала к вам», а после завершения уборки запрашивает оценку качества по 5-балльной шкале. Клиенты могут оставить отзыв и отправить чаевые клинерам.",
        ),
        (
            "Как бесплатно перенести базу клиентов и историю уборок из Excel или другой CRM?",
            "Служба заботы Молнии бесплатно помогает перенести базу постоянных клиентов с их адресами и примечаниями, прайс-лист услуг и список сотрудников из Google Таблиц, Excel или сторонних программ. Перенос занимает около 15 минут без остановки приема текущих заказов.",
        ),
    ]

    faq_html = "\n".join(
        f'            <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
        for q, a in faqs
    )

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://molniya-tech.ru/"},
                {"@type": "ListItem", "position": 2, "name": "Клининг", "item": canonical},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Молния Тех — CRM и программа учета для клининга и выездных бригад",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web, iOS, Android, macOS, Windows",
            "url": canonical,
            "description": description,
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "RUB",
                "description": "Бесплатный демо-доступ и настройка калькулятора клининга",
            },
            "publisher": {
                "@type": "Organization",
                "name": "ООО «МОЛНИЯ ТЕХ»",
                "url": "https://molniya-tech.ru",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a,
                    },
                }
                for q, a in faqs
            ],
        },
    ]
    json_ld_str = json.dumps(json_ld, ensure_ascii=False)

    page_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#FAF7F2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#12100E" media="(prefers-color-scheme: dark)">
  <link rel="canonical" href="{canonical}">

  <!-- Favicons -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- HERO -->
      <section class="mt-hero" data-screen-label="Герой" data-mt-hero-scene>

        <div class="mt-hero-lead">
          <h1 class="mt-hero-title">
            CRM для клининга,<br><span class="mt-hero-accent">выездных бригад и химчистки</span>
          </h1>

          <div class="mt-hero-bottom">
            <div class="mt-hero-intro">
              <p class="mt-hero-sub">Онлайн-запись клиентов 24/7, интерактивное расписание выездов, калькулятор уборки по метражу, сдельный расчет зарплат клинеров и контроль заказов</p>
              <a class="mt-btn mt-btn-hero" href="#contact">Получить бесплатный доступ</a>
            </div>

            <ul class="mt-facets mt-facets--full" aria-label="Преимущества для клининга">
              <li class="mt-facet">
                <span class="mt-facet-name">Выездные бригады</span>
                <span class="mt-facet-note">расписание смен и распределение по районам</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Калькулятор уборки</span>
                <span class="mt-facet-note">авторасчет стоимости от комнат, площади и опций</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Сдельная зарплата</span>
                <span class="mt-facet-note">прозрачный процент клинерам за каждый заказ</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name mt-facet-name--soon">AI & Напоминания</span>
                <span class="mt-facet-note">автосообщения клиентам о выезде бригады и оценка</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <div class="mt-tablet">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для клининга: расписание выездных бригад и журнал заказов" width="1710" height="983" fetchpriority="high">
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </div>
            <p class="mt-hero-media-caption">Интерактивное расписание выездных бригад и контроль заказов в реальном времени</p>
          </div>
        </div>

      </section>

      <!-- LIVE TEAMS STATUS -->
      <section class="mt-section mt-reveal" data-screen-label="Загрузка клининговых бригад" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Все выездные бригады, заказы и адреса <span class="mt-overview-hook">под полным контролем</span></h2>
          <p class="mt-section-sub">Диспетчер и руководитель видят статус каждой бригады, адрес клиента, площадь помещений, заказанные услуги и сумму оплаты в реальном времени на любом устройстве.</p>
        </div>

        <div class="mt-auto-bays">
          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Бригада 1 · Уборка квартиры (85 м²)</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В работе</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Елена М. (10:00–14:30)</div>
                <div class="mt-auto-car-tier">ЖК «Приморский», ул. Савушкина · Генеральная + Окна</div>
              </div>
              <span class="mt-dropdown-footer-icon">🧹</span>
            </div>
            <div class="mt-auto-service">
              <span>Генеральная 85 м² + Окна</span>
              <span class="mt-auto-price">8 900 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Бригада 2 · Химчистка мебели</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В работе</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Алексей С. (12:00–14:00)</div>
                <div class="mt-auto-car-tier">пр. Энгельса · Диван угловой + 2 кресла (экстрактор)</div>
              </div>
              <span class="mt-dropdown-footer-icon">🛋️</span>
            </div>
            <div class="mt-auto-service">
              <span>Химчистка на дому</span>
              <span class="mt-auto-price">6 200 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Бригада 3 · Офисный клининг (220 м²)</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--done">Готово</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Digital Agency (08:00–10:30)</div>
                <div class="mt-auto-car-tier">БЦ «Сенатор» · Поддерживающая уборка + санузлы</div>
              </div>
              <span class="mt-dropdown-footer-icon">🏢</span>
            </div>
            <div class="mt-auto-service">
              <span>Контракт B2B (оплачено)</span>
              <span class="mt-auto-price">14 500 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Бригада 4 · После ремонта (54 м²)</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--wait">Ожидание</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Игорь Д. (15:00–19:30)</div>
                <div class="mt-auto-car-tier">ЖК «Чистое Небо» · Обеспыливание + строительный пылесос</div>
              </div>
              <span class="mt-dropdown-footer-icon">🧽</span>
            </div>
            <div class="mt-auto-service">
              <span>После ремонта (аванс 50%)</span>
              <span class="mt-auto-price">11 200 ₽</span>
            </div>
          </div>
        </div>
      </section>

      <!-- CLEANING OVERVIEW VALUE GRID -->
      <section class="mt-section mt-section--overview mt-reveal" data-screen-label="Функции для клининга" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Управляйте клининговой службой <span class="mt-overview-hook">от заявки до сияющей чистоты</span></h2>
          <p class="mt-section-sub">Программа для клининговых компаний: интерактивное расписание бригад, онлайн-калькулятор на сайте, сдельная зарплата и учет расходников без ручных блокнотов и таблиц.</p>
        </div>

        <div class="mt-overview-grid">
          <article class="mt-overview-card">
            <h3><span class="mt-overview-hook">Расписание бригад</span> и маршруты выездов</h3>
            <p>Наглядная сетка смен по бригадам и часам. Учет времени на дорогу между адресами, распределение по районам города и легкий перенос заказов drag-and-drop. Опоздания исключены.</p>
            <div class="mt-overview-preview mt-overview-preview--schedule" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Расписание смен</span><span>Приморский район</span></div>
              <div class="mt-overview-calendar"><span>10:00</span><div></div><span>10:30</span><div class="mt-overview-slot">Бригада 1 <small>Генеральная · 85 м²</small></div><span>15:30</span><div class="mt-overview-slot mt-overview-slot--light">Бригада 1 <small>Поддерживающая · 45 м²</small></div></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Онлайн-калькулятор уборки <span class="mt-overview-hook">и бот в мессенджере</span></h3>
            <p>Клиенты сами выбирают тип уборки, вводят метраж или количество комнат и добавляют доп. опции на сайте или в Telegram 24/7. Точный расчет стоимости без долгих звонков диспетчеру.</p>
            <div class="mt-overview-preview mt-overview-preview--process" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Онлайн-калькулятор</span><span>3-комн. квартира</span></div>
              <div class="mt-overview-stages"><span>Метраж 85 м²</span><i></i><span>Окна 3 шт.</span><i></i><span>Духовка</span><i></i><span>Заказ</span></div>
              <div class="mt-overview-check">✓ <span>Длительность: 4.5 часа (2 клинера)</span></div>
              <div class="mt-overview-check">✓ <span>Точная стоимость: 8 900 ₽</span></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Сдельная зарплата клинеров <span class="mt-overview-hook">и расчет мотивации</span></h3>
            <p>Автоматический расчет процентов за каждый выполненный заказ (например, 40% бригаде, 10% бригадиру), надбавки за сложные загрязнения и мытье окон. Прозрачные ведомости на выплату в один клик.</p>
            <div class="mt-overview-preview mt-overview-preview--prices" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Расчет смены</span><span>Бригада 1</span></div>
              <div class="mt-overview-price-row"><span>Заказ 8 900 ₽ (генеральная)</span><strong>Клинерам: 3 560 ₽ (40%)</strong></div>
              <div class="mt-overview-price-row"><span>Заказ 4 200 ₽ (поддерживающая)</span><strong>Клинерам: 1 680 ₽ (40%)</strong></div>
              <div class="mt-overview-price-tag">Выработка за день: 5 240 ₽</div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Уведомления клиентам <span class="mt-overview-hook">и контроль качества</span></h3>
            <p>Бот сообщает клиенту: «Бригада выехала, ориентир прибытия 10:00». После уборки система запрашивает оценку качества работы и отправляет электронный чек. Повторные заказы растут на 35%.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Сообщение клиенту</span><span>Мессенджер</span></div>
              <div class="mt-overview-message">
                Елена, бригада №1 завершила генеральную уборку. Оцените, пожалуйста, качество работы клинеров по шкале от 1 до 5.
                <span class="mt-overview-reaction">✨</span>
              </div>
              <div class="mt-overview-client-row"><span>База клиентов</span><strong>История уборок и адреса →</strong></div>
            </div>
          </article>

          <article class="mt-overview-card mt-overview-card--featured">
            <h3>Склад профессиональной химии <span class="mt-overview-hook">и инвентаря</span></h3>
            <p>Списание моющих средств и расходников по технологическим картам, закрепление экстракторов, пароочистителей и стремянок за бригадами. Предотвращение потерь дорогостоящего оборудования.</p>
            <div class="mt-overview-preview mt-overview-preview--metrics" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Склад и техника</span><span>Контроль инвентаря</span></div>
              <div class="mt-overview-metrics"><span>Экстракторы<b>4 в работе</b></span><span>Химия<b>Норма</b></span><span>Выручка<b>₽</b></span></div>
              <div class="mt-overview-chart"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            </div>
          </article>
        </div>

        <div class="mt-overview-action">
          <a class="mt-btn mt-btn-cta" href="#contact">Получить бесплатный доступ</a>
        </div>
      </section>

      <!-- CLEANING JOURNEY -->
      <section class="mt-section mt-journey" data-screen-label="Путь выполнения заказа уборки">
        <div class="mt-section-head mt-section-head--center" data-mt-reveal>
          <h2 class="mt-section-title">Один заказ на клининг. <span class="mt-hero-accent">Полный контроль от заявки до чистоты.</span></h2>
          <p class="mt-section-sub">Посмотрите, как система автоматизирует работу диспетчера: от расчета в онлайн-калькуляторе до выезда бригады, чек-листа помещений и расчета зарплаты.</p>
        </div>

        <div class="mt-journey-example" aria-label="Пример прохождения заказа уборки" data-mt-reveal data-mt-delay="80">
          <span>Пример</span><strong>Генеральная уборка квартиры 85 м²</strong><span>ЖК «Приморский» · Елена М.</span>
        </div>

        <div class="mt-journey-list">
          <article class="mt-journey-step">
            <div class="mt-journey-index">01</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Клиент</span>
              <h3>Онлайн-расчет стоимости и вызов бригады за 60 секунд</h3>
              <p>Клиент указывает 3 комнаты, площадь 85 м² и мытье окон. Виджет показывает точную цену 8 900 ₽ и предлагает свободные окна. Заказ мгновенно появляется в системе.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--booking" aria-label="Пример онлайн-заказа">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Онлайн-заказ</span>
                <span class="mt-journey-proof-badge">Подтверждено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Клиент</span><strong>Елена Васильева</strong></div>
              <div class="mt-journey-proof-row"><span>Адрес</span><strong>ул. Савушкина, 124, кв. 82</strong></div>
              <div class="mt-journey-proof-row"><span>Услуга</span><strong>Генеральная 85 м² + Окна 3 шт.</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">02</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Диспетчер</span>
              <h3>Назначение бригады и комплектация инвентаря</h3>
              <p>Система предлагает свободную бригаду в Приморском районе. Диспетчер подтверждает назначение, а клинеры получают маршрутный лист и список химии на смартфон.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--process" aria-label="Карточка назначения бригады">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Заказ #3108</span>
                <span class="mt-journey-proof-badge">Бригада назначена</span>
              </div>
              <div class="mt-journey-proof-row"><span>Исполнители</span><strong>Бригада №1 (Ольга + Анна)</strong></div>
              <div class="mt-journey-proof-row"><span>Инвентарь</span><strong>Пылесос Kärcher + Набор химии</strong></div>
              <div class="mt-journey-proof-row"><span>Время выезда</span><strong>Завтра, 10:00–14:30</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">03</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Бригада клинеров</span>
              <h3>Выезд на объект, чек-лист комнат и выполнение уборки</h3>
              <p>Клиент получает уведомление «Бригада выехала». На объекте клинеры отмечают этапы уборки по чек-листу (обеспыливание, санузлы, мытье окон) прямо в мобильном интерфейсе.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--order" aria-label="Выполнение уборки">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Чек-лист уборки</span>
                <span class="mt-journey-proof-badge">В процессе (80%)</span>
              </div>
              <div class="mt-journey-proof-row"><span>Комнаты и кухня</span><strong>Обеспылено, вымыто ✓</strong></div>
              <div class="mt-journey-proof-row"><span>Санузлы</span><strong>Дезинфекция проведена ✓</strong></div>
              <div class="mt-journey-proof-row"><span>Окна</span><strong>Мытье стекол и рам</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">04</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Система & Руководитель</span>
              <h3>Приемка, электронная оплата и сдельная выплата</h3>
              <p>Клиент подписывает акт на экране смартфона, вносит оплату, а система мгновенно начисляет 3 560 ₽ в ведомость клинеров и списывает расходную химию со склада.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--payout" aria-label="Завершение заказа">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Заказ закрыт</span>
                <span class="mt-journey-proof-badge">Успешно</span>
              </div>
              <div class="mt-journey-proof-row"><span>Выручка</span><strong>+8 900 ₽ в кассу</strong></div>
              <div class="mt-journey-proof-row"><span>Зарплата бригаде</span><strong>3 560 ₽ (начислено)</strong></div>
              <div class="mt-journey-proof-row"><span>Оценка клиента</span><strong>5 из 5 (отзыв получен)</strong></div>
            </div>
          </article>
        </div>
      </section>

      <!-- REAL-WORLD CASE STUDY -->
      <section class="mt-case-section mt-reveal" data-screen-label="Кейс клининговой компании" data-mt-reveal>
        <div class="mt-case-card">
          <div class="mt-case-header">
            <div class="mt-case-tag">⚡ Кейс автоматизации клининга</div>
            <h2 class="mt-case-title">Клининговая компания «Чистый Вектор», 14 выездных бригад</h2>
            <blockquote class="mt-case-quote">
              «Раньше координаторы вручную считали метраж, согласовывали время в WhatsApp и путались, какая бригада свободна в нужном районе. После внедрения Молнии клиенты сами выбирают услуги в онлайн-калькуляторе, а система распределяет заказы и автоматически начисляет сдельную зарплату клинерам. Потери заявок прекратились, а выручка выросла на 44%.»
            </blockquote>
            <div class="mt-case-author">
              Екатерина Громова <span>· Операционный директор «Чистый Вектор», <span style="white-space:nowrap">Санкт-Петербург</span></span>
            </div>
          </div>
          <div class="mt-case-stats">
            <div class="mt-case-stat">
              <span class="mt-case-num">+44%</span>
              <span class="mt-case-label">Рост выполненных уборок благодаря онлайн-калькулятору без раздувания диспетчеров</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">0</span>
              <span class="mt-case-label">Потерянных заявок и накладок по времени выезда бригад за всё время работы</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">15 <small>мин</small></span>
              <span class="mt-case-label">На перенос базы клиентов, настройку калькулятора услуг и запуск в работу</span>
            </div>
          </div>
        </div>
      </section>

      <!-- CLEANING FAQ -->
      <section id="faq" class="mt-section mt-reveal" data-screen-label="Вопросы и ответы" data-mt-reveal>
        <div class="mt-section-head">
          <h2 class="mt-section-title">Вопросы о программе для клининга и выездных бригад</h2>
        </div>
        <div class="mt-before-start-grid">
          <article class="mt-before-start-highlight">
            <h3>Попробуйте CRM Молния для клининговой службы</h3>
            <p>Бесплатно поможем настроить калькулятор метража, расписание смен выездных бригад, каталог услуг и правила сдельной оплаты. Начните принимать онлайн-заказы уже сегодня.</p>
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в мессенджер ↗</a>
          </article>
          <div class="mt-before-start-questions">
{faq_html}
          </div>
        </div>
        <p class="mt-before-start-privacy">Как мы обрабатываем данные — в <a href="/privacy">политике конфиденциальности</a>.</p>
      </section>

{lead_html}

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
'''
    return page_html


def build_psychologist_page() -> str:
    """Builds the complete psychologist micro-landing page matching the exact presentation features."""
    nav_html = render_nav_html(active_item="health", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")
    lead_html = render_lead_form_html(
        "psychologist",
        'Получите <span class="mt-hero-accent">бесплатный доступ навсегда</span> для частной практики',
        "Оставьте контакты — покажем Молнию на примере вашей практики и поможем настроить персональную страницу записи.",
    )

    title = "Подключить онлайн-запись для психолога — CRM и расписание"
    description = (
        "Программа и онлайн-запись для частнопрактикующих психологов и психотерапевтов: "
        "персональная страница 24/7, слоты по 50 минут с буфером на отдых, формы приёма и профиль клиента с личными заметками."
    )
    canonical = "https://molniya-tech.ru/psychologist"

    faqs = [
        (
            "Как клиенты записываются на консультации через Молнию?",
            "Вы получаете персональную страницу записи с вашим брендом и короткой ссылкой для соцсетей, мессенджеров или визиток (также виджет можно встроить на личный сайт). Клиенты заходят с любого устройства без установки приложений, видят свободные слоты, отвечают на ваши вводные вопросы и сразу получают подтверждение.",
        ),
        (
            "Как настроить буфер между сессиями на отдых и заметки?",
            "Вы задаете длительность консультации (например, 50 минут) и обязательный буфер после нее (например, 10 или 15 минут). Программа автоматически бронирует слот с запасом — клиенты физически не смогут записаться встык, и у вас всегда будет время выпить чай и внести мысли в карточку.",
        ),
        (
            "Как работают напоминания клиентам о предстоящей сессии?",
            "Система автоматически отправляет клиенту мгновенное подтверждение сразу после записи, а накануне визита — дружеское напоминание по E-mail, в мессенджер или по SMS (на выбор). Клиент точно знает дату, время и формат (ссылку на звонок или адрес кабинета), что снижает неявки до минимума.",
        ),
        (
            "Можно ли задавать клиенту вопросы до сессии (запрос, формат, согласие)?",
            "Да. В Молнии настраиваются формы приёма под каждую услугу: контакты, первичный запрос, согласие с правилами отмены или анкета. Вы видите все ответы в карточке записи и приходите на встречу уже подготовленным.",
        ),
        (
            "Где сохраняются заметки по клиентам и конфиденциальна ли эта информация?",
            "У каждого клиента формируется единый централизованный профиль: история прошлых и будущих встреч, формы приёма и ваши личные заметки. Доступ строго разграничен и защищен по 152-ФЗ — ваши заметки видите только вы со своего смартфона или компьютера.",
        ),
        (
            "Подходит ли программа для совмещения онлайн-консультаций и очных приёмов в кабинете?",
            "Да. Вы настраиваете разные типы встреч (онлайн-сессия в Zoom/Телемосте или очный приём в кабинете). В расписании можно гибко задавать часы приёма для разных локаций и быстро переносить встречи перетаскиванием (drag-and-drop).",
        ),
        (
            "Как бесплатно перенести базу клиентов и историю встреч в Молнию?",
            "Служба заботы Молнии бесплатно помогает перенести контакты клиентов, заметки и график из таблиц Excel, блокнотов или сторонних программ. Вы начнете работу в единой системе без остановки консультаций.",
        ),
    ]

    faq_html = "\n".join(
        f'            <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
        for q, a in faqs
    )

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://molniya-tech.ru/"},
                {"@type": "ListItem", "position": 2, "name": "Здоровье и медицина", "item": "https://molniya-tech.ru/health"},
                {"@type": "ListItem", "position": 3, "name": "Онлайн-запись для психологов", "item": canonical},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Молния Тех — онлайн-запись и CRM для психологов",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web, iOS, Android, macOS, Windows",
            "url": canonical,
            "description": description,
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "RUB",
                "description": "Бесплатный демо-доступ и настройка персональной страницы записи",
            },
            "publisher": {
                "@type": "Organization",
                "name": "ООО «МОЛНИЯ ТЕХ»",
                "url": "https://molniya-tech.ru",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a,
                    },
                }
                for q, a in faqs
            ],
        },
    ]
    json_ld_str = json.dumps(json_ld, ensure_ascii=False)

    page_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#FAF7F2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#12100E" media="(prefers-color-scheme: dark)">
  <link rel="canonical" href="{canonical}">

  <!-- Favicons -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- HERO -->
      <section class="mt-hero" data-screen-label="Герой" data-mt-hero-scene>

        <div class="mt-hero-lead">
          <h1 class="mt-hero-title">
            Онлайн-запись и CRM<br><span class="mt-hero-accent">для частной практики психолога</span>
          </h1>

          <div class="mt-hero-bottom">
            <div class="mt-hero-intro">
              <p class="mt-hero-sub">Персональная страница записи 24/7, свободные слоты по 50 минут с буфером на отдых, формы приёма и профиль клиента с личными заметками</p>
              <a class="mt-btn mt-btn-hero" href="#contact">Получить бесплатный доступ</a>
            </div>

            <ul class="mt-facets mt-facets--full" aria-label="Преимущества для психологов и терапевтов">
              <li class="mt-facet">
                <span class="mt-facet-name">Слоты 50 + 10 мин</span>
                <span class="mt-facet-note">автоматический буфер между сессиями</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Доступно 24/7</span>
                <span class="mt-facet-note">персональная страница без приложений</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Формы приёма</span>
                <span class="mt-facet-note">вопросы под услугу и история обращений</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name mt-facet-name--soon">Напоминания</span>
                <span class="mt-facet-note">E-mail, мессенджер или SMS на выбор</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <div class="mt-tablet">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для психолога: расписание сессий и электронный журнал записей" width="1710" height="983" fetchpriority="high">
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </div>
            <p class="mt-hero-media-caption">Электронное расписание консультаций и свободные слоты специалиста в реальном времени</p>
          </div>
        </div>

      </section>

      <!-- LIVE SESSIONS STATUS -->
      <section class="mt-section mt-reveal" data-screen-label="Расписание сессий" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Каждая консультация, клиент и время <span class="mt-overview-hook">под вашим контролем</span></h2>
          <p class="mt-section-sub">Вы видите статус каждой записи, формат встречи (онлайн или очный приём в кабинете), ответы на вводные вопросы и контактные данные клиента прямо в смартфоне.</p>
        </div>

        <div class="mt-auto-bays">
          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">10:00 · Индивидуальная сессия</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">Онлайн</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Анна К. (Онлайн-звонок)</div>
                <div class="mt-auto-car-tier">Первичная консультация · 50 мин</div>
              </div>
              <span class="mt-dropdown-footer-icon">💻</span>
            </div>
            <div class="mt-auto-service">
              <span>Сессия 50 мин (Zoom)</span>
              <span class="mt-auto-price">4 000 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">11:00 · Личная терапия</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">Кабинет</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Михаил В. (Очно)</div>
                <div class="mt-auto-car-tier">Кабинет №4 · Повторная сессия</div>
              </div>
              <span class="mt-dropdown-footer-icon">🛋️</span>
            </div>
            <div class="mt-auto-service">
              <span>Прием в кабинете</span>
              <span class="mt-auto-price">5 000 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">12:00 · Перерыв и заметки</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--wait">Буфер</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Личное время специалиста</div>
                <div class="mt-auto-car-tier">Заполнение карточек, отдых</div>
              </div>
              <span class="mt-dropdown-footer-icon">☕</span>
            </div>
            <div class="mt-auto-service">
              <span>Буферное время</span>
              <span class="mt-auto-price">В графике</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">13:00 · Семейная консультация</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--done">Подтверждено</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Дмитрий и Ольга (Парная)</div>
                <div class="mt-auto-car-tier">Семейная встреча · 90 мин</div>
              </div>
              <span class="mt-dropdown-footer-icon">👥</span>
            </div>
            <div class="mt-auto-service">
              <span>Консультация пары</span>
              <span class="mt-auto-price">7 500 ₽</span>
            </div>
          </div>
        </div>
      </section>

      <!-- PSYCHOLOGIST OVERVIEW VALUE GRID -->
      <section class="mt-section mt-section--overview mt-reveal" data-screen-label="Функции для психологов" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Ведите психологическую практику <span class="mt-overview-hook">без рутины и перегрузок</span></h2>
          <p class="mt-section-sub">Один сервис вместо телефона, мессенджеров, таблиц и блокнотов: персональная страница бронирования 24/7, буферы между сессиями, профиль клиента с личными заметками и дружеские напоминания.</p>
        </div>

        <div class="mt-overview-grid">
          <article class="mt-overview-card">
            <h3>Свободные слоты <span class="mt-overview-hook">и буфер на отдых и подготовку</span></h3>
            <p>Задайте часы приёма, длительность консультаций и обязательный буфер (10–15 минут) на отдых, чай и фиксацию инсайтов. Программа не позволит клиентам записаться впритык или вне графика — вы защищены от перегрузок.</p>
            <div class="mt-overview-preview mt-overview-preview--schedule" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Расписание консультаций</span><span>Свободно / Буфер</span></div>
              <div class="mt-overview-calendar"><span>10:00</span><div class="mt-overview-slot">Анна К. <small>Индивидуальная (50 мин)</small></div><span>11:00</span><div class="mt-overview-slot mt-overview-slot--light">Михаил В. <small>Кабинет №4 (50 мин)</small></div><span>12:00</span><div></div></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Персональная страница записи <span class="mt-overview-hook">в вашем фирменном стиле</span></h3>
            <p>Короткая ссылка для соцсетей, визиток, шапки профиля или встраиваемый виджет на сайт. Страница с вашим описанием и услугами работает 24/7 с любого устройства — телефона, планшета или компьютера без установки приложений.</p>
            <div class="mt-overview-preview mt-overview-preview--prices" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Страница бронирования</span><span>Доступно 24/7</span></div>
              <div class="mt-overview-price-row"><span>Индивидуальная консультация</span><strong>50 мин · Выбор слота</strong></div>
              <div class="mt-overview-price-row"><span>Удобная короткая ссылка</span><strong>Для соцсетей и мессенджеров</strong></div>
              <div class="mt-overview-price-tag">Клиенты записываются сами в любое время</div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Напоминания без лишних действий <span class="mt-overview-hook">и меньше неявок</span></h3>
            <p>Клиент получает мгновенное подтверждение сразу после бронирования, а накануне визита — автоматическое дружеское напоминание по E-mail, в мессенджер или по SMS (на выбор). Вам не приходится отправлять повторные сообщения вручную.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Автоматические напоминания</span><span>Без рутины</span></div>
              <div class="mt-overview-message">
                Анна, напоминаем о консультации завтра в 10:00. Ссылка на подключение отправлена на вашу почту.
                <span class="mt-overview-reaction">⚡</span>
              </div>
              <div class="mt-overview-client-row"><span>E-mail, мессенджер или SMS</span><strong>На выбор клиента →</strong></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Формы приёма и единый профиль <span class="mt-overview-hook">с личными заметками</span></h3>
            <p>Настройте вводные вопросы под услугу: запрос, контакты, согласие. В централизованном профиле клиента сохраняются история встреч, динамика и ваши конфиденциальные заметки для персонального ведения терапии.</p>
            <div class="mt-overview-preview mt-overview-preview--process" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Карточка клиента</span><span>Анна К. (Конфиденциально)</span></div>
              <div class="mt-overview-stages"><span>Контакты</span><i></i><span>Запрос</span><i></i><span>Заметки</span></div>
              <div class="mt-overview-check">✓ <span>Форма приёма заполнена клиентом</span></div>
              <div class="mt-overview-check">✓ <span>Личные заметки доступны только вам</span></div>
            </div>
          </article>

          <article class="mt-overview-card mt-overview-card--featured">
            <h3>Гибкое управление календарём <span class="mt-overview-hook">с любого устройства</span></h3>
            <p>Перетаскивайте встречи для быстрой перепланировки в один клик. Проверяйте и меняйте расписание из кабинета, дома или в пути со смартфона — день перестроится мгновенно без ручных правок.</p>
            <div class="mt-overview-preview mt-overview-preview--metrics" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Управление расписанием</span><span>Drag & Drop</span></div>
              <div class="mt-overview-metrics"><span>Перенос<b>1 клик</b></span><span>Устройства<b>iOS / Android</b></span><span>Контроль<b>24/7</b></span></div>
              <div class="mt-overview-chart"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            </div>
          </article>
        </div>

        <div class="mt-overview-action">
          <a class="mt-btn mt-btn-cta" href="#contact">Получить бесплатный доступ</a>
        </div>
      </section>

      <!-- PSYCHOLOGIST JOURNEY -->
      <section class="mt-section mt-journey" data-screen-label="Путь клиента к психологу">
        <div class="mt-section-head mt-section-head--center" data-mt-reveal>
          <h2 class="mt-section-title">Один клиент частной практики. <span class="mt-hero-accent">Полный порядок в расписании.</span></h2>
          <p class="mt-section-sub">Посмотрите, как Молния автоматизирует запись к психологу: от выбора времени на странице бронирования до ответов на вводные вопросы, автонапоминаний и сохранения заметок.</p>
        </div>

        <div class="mt-journey-example" aria-label="Пример прохождения консультации" data-mt-reveal data-mt-delay="80">
          <span>Пример</span><strong>Индивидуальная консультация</strong><span>Длительность 50 минут + 10 минут буфер на заметки</span>
        </div>

        <div class="mt-journey-list">
          <article class="mt-journey-step">
            <div class="mt-journey-index">01</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Клиент</span>
              <h3>Выбор услуги и удобного слота на странице записи 24/7</h3>
              <p>Клиент переходит по вашей короткой ссылке в соцсетях или мессенджере, выбирает онлайн-консультацию или очный приём и видит только актуальные свободные слоты.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--booking" aria-label="Пример бронирования консультации">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Бронирование сессии</span>
                <span class="mt-journey-proof-badge">Слот выбран</span>
              </div>
              <div class="mt-journey-proof-row"><span>Клиент</span><strong>Анна К.</strong></div>
              <div class="mt-journey-proof-row"><span>Услуга</span><strong>Индивидуальная консультация (50 мин)</strong></div>
              <div class="mt-journey-proof-row"><span>Время</span><strong>Среда, 10:00 – 10:50</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">02</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Форма приёма</span>
              <h3>Ответы на вводные вопросы и мгновенное подтверждение</h3>
              <p>Клиент указывает контактные данные, кратко описывает свой запрос и сразу получает подтверждение записи. Слот автоматически блокируется в вашем календаре.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--process" aria-label="Анкета записи">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Запись #4912</span>
                <span class="mt-journey-proof-badge">Подтверждена</span>
              </div>
              <div class="mt-journey-proof-row"><span>Формат</span><strong>Онлайн-звонок (Zoom)</strong></div>
              <div class="mt-journey-proof-row"><span>Запрос</span><strong>Тревожность и выгорание</strong></div>
              <div class="mt-journey-proof-row"><span>Статус</span><strong>Внесено в расписание</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">03</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Система</span>
              <h3>Дружеские автонапоминания накануне консультации</h3>
              <p>Система заблаговременно отправляет клиенту напоминание по E-mail, в мессенджер или по SMS с деталями встречи (ссылка на видеозвонок или схема прохода в кабинет).</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--order" aria-label="Сообщение с напоминанием">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Напоминание</span>
                <span class="mt-journey-proof-badge">Отправлено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Канал</span><strong>Мессенджер / E-mail / SMS</strong></div>
              <div class="mt-journey-proof-row"><span>Ссылка</span><strong>zoom.us/j/molniya-4912</strong></div>
              <div class="mt-journey-proof-row"><span>Результат</span><strong>Клиент знает, где и когда быть</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">04</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Психолог</span>
              <h3>Сессия, личные заметки в буфер и история встреч</h3>
              <p>Вы спокойно проводите сессию, фиксируете важные тезисы в карточке клиента во время 10-минутного буфера. Вся история обращений доступна в едином окне в любой момент.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--payout" aria-label="Результат сессии">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Завершение встречи</span>
                <span class="mt-journey-proof-badge">Успешно</span>
              </div>
              <div class="mt-journey-proof-row"><span>Тайминг</span><strong>50 мин сессия + 10 мин буфер</strong></div>
              <div class="mt-journey-proof-row"><span>Заметки</span><strong>Сохранены в профиле клиента</strong></div>
              <div class="mt-journey-proof-row"><span>Следующий шаг</span><strong>Клиент записан на повторный приём</strong></div>
            </div>
          </article>
        </div>
      </section>

      <!-- REAL-WORLD CASE STUDY -->
      <section class="mt-case-section mt-reveal" data-screen-label="Кейс частной практики" data-mt-reveal>
        <div class="mt-case-card">
          <div class="mt-case-header">
            <div class="mt-case-tag">⚡ Кейс частной психологической практики</div>
            <h2 class="mt-case-title">Дарья Соколова, частнопрактикующий психолог</h2>
            <blockquote class="mt-case-quote">
              «Раньше до 2 часов в день уходило на бесконечные переписки в WhatsApp с согласованием времени и напоминаниями. С Молнией у меня появилась персональная страница записи: клиенты сами выбирают свободные слоты в удобное время. Больше никаких накладок, а буфер между консультациями позволяет спокойно вести заметки и не выгорать.»
            </blockquote>
            <div class="mt-case-author">
              Дарья Соколова <span>· Клинический психолог, КПТ-терапевт, <span style="white-space:nowrap">Москва</span></span>
            </div>
          </div>
          <div class="mt-case-stats">
            <div class="mt-case-stat">
              <span class="mt-case-num">0</span>
              <span class="mt-case-label">Накладок в расписании благодаря автоматическим буферам между сессиями</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">2 ч</span>
              <span class="mt-case-label">В день сэкономлено на ручной координации и переписках о времени</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">100%</span>
              <span class="mt-case-label">Записей и заметок по клиентам хранятся в одном удобном профиле</span>
            </div>
          </div>
        </div>
      </section>

      <!-- PSYCHOLOGIST FAQ -->
      <section id="faq" class="mt-section mt-reveal" data-screen-label="Вопросы и ответы" data-mt-reveal>
        <div class="mt-section-head">
          <h2 class="mt-section-title">Вопросы об онлайн-записи и программе для психологов</h2>
        </div>
        <div class="mt-before-start-grid">
          <article class="mt-before-start-highlight">
            <h3>Попробуйте Молнию для своей частной практики</h3>
            <p>Бесплатно поможем настроить персональную страницу записи, буферные интервалы между сессиями, форму приёма под ваши консультации и перенести базу клиентов.</p>
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в мессенджер ↗</a>
          </article>
          <div class="mt-before-start-questions">
{faq_html}
          </div>
        </div>
        <p class="mt-before-start-privacy">Как мы обрабатываем данные — в <a href="/privacy">политике конфиденциальности</a>.</p>
      </section>

{lead_html}

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
'''
    return page_html


def build_stretching_page() -> str:
    """Builds the complete stretching and flexibility studio micro-landing page."""
    nav_html = render_nav_html(active_item="health", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")
    lead_html = render_lead_form_html(
        "stretching",
        'Получите <span class="mt-hero-accent">бесплатный доступ навсегда</span> для студии растяжки',
        "Оставьте контакты — покажем Молнию на примере вашей студии и поможем настроить расписание залов и форму записи учеников.",
    )

    title = "Подключить онлайн-запись для студии растяжки и стретчинга — расписание и CRM"
    description = (
        "Программа и онлайн-запись для студий растяжки, стретчинга и аэройоги: "
        "наглядное расписание залов 24/7, учёт абонементов, запись в группы и напоминания ученикам."
    )
    canonical = "https://molniya-tech.ru/stretching"

    faqs = [
        (
            "Как клиенты записываются на тренировки по растяжке через Молнию?",
            "Вы получаете персональную страницу записи студии с вашим логотипом и описанием направлений (шпагат, здоровая спина, аэройога, МФР). Ссылка размещается в соцсетях, мессенджерах или виджетом на сайте. Ученик видит актуальную сетку залов, оставшиеся места в группах и записывается за минуту с любого устройства без установки приложений.",
        ),
        (
            "Как настраивается лимит мест в группе и бронь оборудования (коврики, гамаки)?",
            "Для каждого зала и направления вы указываете максимальную вместимость (например, 8 ковриков в малом зале или 6 гамаков в зале аэройоги). Как только лимит исчерпан, программа блокирует запись на этот слот, предотвращая переполнение и накладки.",
        ),
        (
            "Как вести учёт абонементов (на 8, 12 занятий) и пробных уроков?",
            "В профиле каждого ученика фиксируется тип визита: разовое занятие, пробная тренировка или абонемент с количеством оставшихся визитов. При каждой отметке прихода система автоматически списывает занятие и показывает остаток.",
        ),
        (
            "Можно ли настроить буфер между тренировками на проветривание зала и смену инвентаря?",
            "Да. Вы задаете обязательный технический буфер (например, 15 минут) между занятиями. Система автоматически учитывает его в расписании: группы не сталкиваются в дверях, а тренеры успевают подготовить зал и инвентарь к следующему уроку.",
        ),
        (
            "Как работают напоминания ученикам о предстоящей тренировке?",
            "Сразу после бронирования ученик получает подтверждение, а накануне визита — автоматическое сообщение по E-mail, в мессенджер или по SMS (на выбор). Это практически исключает ситуации, когда клиент забыл о тренировке или перепутал зал.",
        ),
        (
            "Где фиксируются противопоказания и пожелания ученика перед первой тренировкой?",
            "В форму записи можно включить вводные вопросы: уровень растяжки, прошлые травмы или ограничения по здоровью. Тренер видит ответы в карточке записи до начала занятия и подбирает безопасные упражнения.",
        ),
        (
            "Как бесплатно перенести базу учеников и расписание из другой CRM или Excel?",
            "Служба заботы Молнии бесплатно помогает перенести базу клиентов, остатки по действующим абонементам и график тренеров из Google Таблиц, Excel или сторонних сервисов. Перенос проходит за 15 минут и без остановки работы студии.",
        ),
    ]

    faq_html = "\n".join(
        f'            <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
        for q, a in faqs
    )

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://molniya-tech.ru/"},
                {"@type": "ListItem", "position": 2, "name": "Здоровье и медицина", "item": "https://molniya-tech.ru/health"},
                {"@type": "ListItem", "position": 3, "name": "Онлайн-запись для студий растяжки", "item": canonical},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Молния Тех — онлайн-запись и CRM для студий растяжки и стретчинга",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web, iOS, Android, macOS, Windows",
            "url": canonical,
            "description": description,
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "RUB",
                "description": "Бесплатный демо-доступ и настройка расписания залов студии",
            },
            "publisher": {
                "@type": "Organization",
                "name": "ООО «МОЛНИЯ ТЕХ»",
                "url": "https://molniya-tech.ru",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a,
                    },
                }
                for q, a in faqs
            ],
        },
    ]
    json_ld_str = json.dumps(json_ld, ensure_ascii=False)

    page_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#FAF7F2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#12100E" media="(prefers-color-scheme: dark)">
  <link rel="canonical" href="{canonical}">

  <!-- Favicons -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- HERO -->
      <section class="mt-hero" data-screen-label="Герой" data-mt-hero-scene>

        <div class="mt-hero-lead">
          <h1 class="mt-hero-title">
            Онлайн-запись и расписание<br><span class="mt-hero-accent">для студий растяжки и стретчинга</span>
          </h1>

          <div class="mt-hero-bottom">
            <div class="mt-hero-intro">
              <p class="mt-hero-sub">Персональная страница записи 24/7, наглядное расписание залов и тренеров, учёт абонементов и напоминания ученикам без рутины в чатах</p>
              <a class="mt-btn mt-btn-hero" href="#contact">Получить бесплатный доступ</a>
            </div>

            <ul class="mt-facets mt-facets--full" aria-label="Преимущества для студий растяжки и стретчинга">
              <li class="mt-facet">
                <span class="mt-facet-name">Лимиты залов</span>
                <span class="mt-facet-note">контроль мест по коврикам и гамакам</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Доступно 24/7</span>
                <span class="mt-facet-note">страница записи без приложений</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Абонементы</span>
                <span class="mt-facet-note">разовые уроки, пакеты и сгорающие визиты</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name mt-facet-name--soon">Напоминания</span>
                <span class="mt-facet-note">E-mail, мессенджер или SMS на выбор</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <div class="mt-tablet">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для студии растяжки: расписание тренировок и залов" width="1710" height="983" fetchpriority="high">
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </div>
            <p class="mt-hero-media-caption">Электронное расписание тренировок и загрузка залов студии в реальном времени</p>
          </div>
        </div>

      </section>

      <!-- LIVE SCHEDULE STATUS -->
      <section class="mt-section mt-reveal" data-screen-label="Расписание тренировок" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Каждая тренировка, зал и тренер <span class="mt-overview-hook">под вашим контролем</span></h2>
          <p class="mt-section-sub">Администратор и тренеры видят занятость залов, статус групп и число оставшихся мест в реальном времени с любого устройства.</p>
        </div>

        <div class="mt-auto-bays">
          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">10:00 · Шпагат и гибкость</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В зале</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Алина В. · Зал 2 (Классика)</div>
                <div class="mt-auto-car-tier">Групповая тренировка · 8 из 8 мест</div>
              </div>
              <span class="mt-dropdown-footer-icon">🧘‍♀️</span>
            </div>
            <div class="mt-auto-service">
              <span>Группа по шпагату</span>
              <span class="mt-auto-price">По абонементу</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">11:30 · Аэройога (Гамаки)</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--done">Подтверждено</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Екатерина С. · Зал 1 (Аэро)</div>
                <div class="mt-auto-car-tier">Занятие в гамаках · 6 из 6 мест</div>
              </div>
              <span class="mt-dropdown-footer-icon">🎪</span>
            </div>
            <div class="mt-auto-service">
              <span>Аэростретчинг</span>
              <span class="mt-auto-price">Пробный урок</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">13:00 · Проветривание и подготовка</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--wait">Буфер</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Технический перерыв</div>
                <div class="mt-auto-car-tier">Смена ковриков, дезинфекция гамаков</div>
              </div>
              <span class="mt-dropdown-footer-icon">✨</span>
            </div>
            <div class="mt-auto-service">
              <span>Буферное время</span>
              <span class="mt-auto-price">В расписании</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">14:00 · Персональная растяжка</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--done">Подтверждено</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Полина М. · Зал 3 (Индивидуальный)</div>
                <div class="mt-auto-car-tier">Мария Д. · Индивидуальное занятие</div>
              </div>
              <span class="mt-dropdown-footer-icon">⭐</span>
            </div>
            <div class="mt-auto-service">
              <span>Индивидуальный стретчинг</span>
              <span class="mt-auto-price">2 500 ₽</span>
            </div>
          </div>
        </div>
      </section>

      <!-- STRETCHING OVERVIEW VALUE GRID -->
      <section class="mt-section mt-section--overview mt-reveal" data-screen-label="Функции для студий растяжки" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Управляйте студией растяжки <span class="mt-overview-hook">без накладок и путаницы в чатах</span></h2>
          <p class="mt-section-sub">Один сервис вместо блокнотов, таблиц и бесконечных сообщений: онлайн-расписание 24/7, контроль вместимости залов, учёт абонементов и автоматические напоминания ученикам.</p>
        </div>

        <div class="mt-overview-grid">
          <article class="mt-overview-card">
            <h3>Сетка тренировок и лимиты залов <span class="mt-overview-hook">без переполнения групп</span></h3>
            <p>Задайте точное число мест под размер каждого зала или количество гамаков. Система автоматически блокирует запись на полный слот, защищая от перегрузки залов и обеспечивая комфорт учеников.</p>
            <div class="mt-overview-preview mt-overview-preview--schedule" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Расписание залов</span><span>Вместимость</span></div>
              <div class="mt-overview-calendar"><span>10:00</span><div class="mt-overview-slot">Зал 2: Шпагат <small>8 из 8 мест</small></div><span>11:30</span><div class="mt-overview-slot mt-overview-slot--light">Зал 1: Аэройога <small>6 из 6 мест</small></div><span>13:00</span><div></div></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Персональная страница записи <span class="mt-overview-hook">в вашем фирменном стиле</span></h3>
            <p>Короткая ссылка для соцсетей, Telegram или встраиваемый виджет на сайт студии. Ученики сами выбирают направление (шпагат, спина, аэройога), тренера и удобный слот за 1 минуту без ожидания ответа администратора.</p>
            <div class="mt-overview-preview mt-overview-preview--prices" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Страница бронирования</span><span>Доступно 24/7</span></div>
              <div class="mt-overview-price-row"><span>Групповой стретчинг</span><strong>55 мин · Выбор зала</strong></div>
              <div class="mt-overview-price-row"><span>Удобная короткая ссылка</span><strong>Для соцсетей и мессенджеров</strong></div>
              <div class="mt-overview-price-tag">Ученики записываются сами в любое время</div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Автоматические напоминания <span class="mt-overview-hook">и меньше пропусков тренировок</span></h3>
            <p>Ученик получает мгновенное подтверждение после бронирования, а накануне тренировки — напоминание по E-mail, в мессенджер или по SMS. Он успеет предупредить об отмене, и место достанется другому клиенту.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Автоматические напоминания</span><span>Без рутины</span></div>
              <div class="mt-overview-message">
                Мария, напоминаем о тренировке по стретчингу завтра в 10:00 в Зале 2. Не забудьте удобную форму!
                <span class="mt-overview-reaction">⚡</span>
              </div>
              <div class="mt-overview-client-row"><span>E-mail, мессенджер или SMS</span><strong>На выбор клиента →</strong></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Учёт абонементов и история занятий <span class="mt-overview-hook">в профиле ученика</span></h3>
            <p>Фиксируйте разовые тренировки, пробные уроки и пакетные абонементы на 8 или 12 занятий. В централизованном профиле сохраняются история визитов, цели ученика и противопоказания по здоровью.</p>
            <div class="mt-overview-preview mt-overview-preview--process" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Карточка ученика</span><span>Мария Д. (Абонемент)</span></div>
              <div class="mt-overview-stages"><span>Пробный</span><i></i><span>Абонемент 8</span><i></i><span>Остаток: 5</span></div>
              <div class="mt-overview-check">✓ <span>Абонемент активен (списание по факту)</span></div>
              <div class="mt-overview-check">✓ <span>История визитов и цели сохранены</span></div>
            </div>
          </article>

          <article class="mt-overview-card mt-overview-card--featured">
            <h3>Табель смен и зарплаты тренеров <span class="mt-overview-hook">в один клик</span></h3>
            <p>Программа фиксирует проведенные занятия и смены каждого тренера. В конце периода табель автоматически готов к расчету сдельной зарплаты — без споров и ручного пересчёта бумажных журналов.</p>
            <div class="mt-overview-preview mt-overview-preview--metrics" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Учёт работы команды</span><span>Цифровой табель</span></div>
              <div class="mt-overview-metrics"><span>Залы<b>3</b></span><span>Тренеры<b>6 в смене</b></span><span>Учёт<b>100%</b></span></div>
              <div class="mt-overview-chart"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            </div>
          </article>
        </div>

        <div class="mt-overview-action">
          <a class="mt-btn mt-btn-cta" href="#contact">Получить бесплатный доступ</a>
        </div>
      </section>

      <!-- STRETCHING JOURNEY -->
      <section class="mt-section mt-journey" data-screen-label="Путь ученика в студию">
        <div class="mt-section-head mt-section-head--center" data-mt-reveal>
          <h2 class="mt-section-title">Один визит на растяжку. <span class="mt-hero-accent">Полный порядок в студии.</span></h2>
          <p class="mt-section-sub">Посмотрите, как Молния автоматизирует запись в студию растяжки: от выбора направления на странице бронирования до списания занятия с абонемента и отметки прихода в зал.</p>
        </div>

        <div class="mt-journey-example" aria-label="Пример прохождения занятия" data-mt-reveal data-mt-delay="80">
          <span>Пример</span><strong>Групповая тренировка по шпагату</strong><span>Длительность 55 минут + 15 минут буфер на проветривание зала</span>
        </div>

        <div class="mt-journey-list">
          <article class="mt-journey-step">
            <div class="mt-journey-index">01</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Ученик</span>
              <h3>Выбор направления и удобного времени на странице записи 24/7</h3>
              <p>Клиент переходит по вашей короткой ссылке в соцсетях или мессенджере, выбирает тренировку (шпагат, аэройога, здоровая спина) и видит только реальные свободные места.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--booking" aria-label="Пример бронирования тренировки">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Бронирование тренировки</span>
                <span class="mt-journey-proof-badge">Место забронировано</span>
              </div>
              <div class="mt-journey-proof-row"><span>Ученик</span><strong>Мария Д.</strong></div>
              <div class="mt-journey-proof-row"><span>Направление</span><strong>Шпагат и гибкость (55 мин)</strong></div>
              <div class="mt-journey-proof-row"><span>Зал и время</span><strong>Зал 2 · Вторник, 10:00 – 10:55</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">02</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Форма приёма</span>
              <h3>Выбор типа занятия и фиксация ограничений по здоровью</h3>
              <p>Ученик указывает контакты, выбирает абонемент или пробный урок и отмечает противопоказания. Слот автоматически фиксируется в расписании студии.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--process" aria-label="Анкета записи">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Запись #5120</span>
                <span class="mt-journey-proof-badge">Подтверждена</span>
              </div>
              <div class="mt-journey-proof-row"><span>Тип визита</span><strong>Абонемент на 8 занятий</strong></div>
              <div class="mt-journey-proof-row"><span>Цель / Опыт</span><strong>Сесть на шпагат с нуля</strong></div>
              <div class="mt-journey-proof-row"><span>Статус</span><strong>Место в группе закреплено</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">03</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Система</span>
              <h3>Дружеские автонапоминания накануне тренировки</h3>
              <p>Система заблаговременно отправляет ученику напоминание по E-mail, в мессенджер или по SMS с деталями урока (зал, форма одежды, адрес студии).</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--order" aria-label="Сообщение с напоминанием">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Напоминание</span>
                <span class="mt-journey-proof-badge">Отправлено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Канал</span><strong>Мессенджер / E-mail / SMS</strong></div>
              <div class="mt-journey-proof-row"><span>Инфо</span><strong>Зал 2, тренер Алина В.</strong></div>
              <div class="mt-journey-proof-row"><span>Результат</span><strong>Ученик помнит о занятии</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">04</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Тренер</span>
              <h3>Отметка прихода в зале и автосписание занятия</h3>
              <p>Тренер отмечает явку учеников в приложении. Занятие списывается с абонемента автоматически, а 15-минутный буфер позволяет подготовить зал к следующей группе.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--payout" aria-label="Результат визита">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Итог тренировки</span>
                <span class="mt-journey-proof-badge">Успешно</span>
              </div>
              <div class="mt-journey-proof-row"><span>Абонемент</span><strong>Осталось 5 из 8 занятий</strong></div>
              <div class="mt-journey-proof-row"><span>Табель тренера</span><strong>Занятие учтено в смене</strong></div>
              <div class="mt-journey-proof-row"><span>Следующий шаг</span><strong>Запись на следующее занятие</strong></div>
            </div>
          </article>
        </div>
      </section>

      <!-- REAL-WORLD CASE STUDY -->
      <section class="mt-case-section mt-reveal" data-screen-label="Кейс студии растяжки" data-mt-reveal>
        <div class="mt-case-card">
          <div class="mt-case-header">
            <div class="mt-case-tag">⚡ Кейс студии стретчинга</div>
            <h2 class="mt-case-title">Евгения Морозова, основатель студии «Стретч Лаб»</h2>
            <blockquote class="mt-case-quote">
              «Раньше администраторы целый день сидели в переписках Telegram и WhatsApp, вручную сверяя свободные коврики и гамаки. С Молнией ученики записываются сами за 1 минуту по ссылке в профиле, сразу видя доступные места. Мы полностью избавились от переполненных групп, а учёт абонементов и расчет выплат тренерам теперь автоматизированы.»
            </blockquote>
            <div class="mt-case-author">
              Евгения Морозова <span>· Основатель студии растяжки и аэройоги, <span style="white-space:nowrap">Москва</span></span>
            </div>
          </div>
          <div class="mt-case-stats">
            <div class="mt-case-stat">
              <span class="mt-case-num">0</span>
              <span class="mt-case-label">Накладок в залах и переполнения групп благодаря строгому лимиту мест</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">3 ч</span>
              <span class="mt-case-label">В день сэкономлено администратором на ручной записи и ответах в чатах</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">100%</span>
              <span class="mt-case-label">Абонементов и смен тренеров учтены без бумажных табелей</span>
            </div>
          </div>
        </div>
      </section>

      <!-- STRETCHING FAQ -->
      <section id="faq" class="mt-section mt-reveal" data-screen-label="Вопросы и ответы" data-mt-reveal>
        <div class="mt-section-head">
          <h2 class="mt-section-title">Вопросы об онлайн-записи и программе для студий растяжки</h2>
        </div>
        <div class="mt-before-start-grid">
          <article class="mt-before-start-highlight">
            <h3>Попробуйте Молнию для своей студии растяжки</h3>
            <p>Бесплатно поможем настроить расписание залов, лимиты мест, направления тренировок, форму онлайн-записи и перенести базу постоянных учеников.</p>
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в мессенджер ↗</a>
          </article>
          <div class="mt-before-start-questions">
{faq_html}
          </div>
        </div>
        <p class="mt-before-start-privacy">Как мы обрабатываем данные — в <a href="/privacy">политике конфиденциальности</a>.</p>
      </section>

{lead_html}

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
'''
    return page_html




def build_yoga_page() -> str:
    """Builds the complete yoga and pilates studio micro-landing page."""
    nav_html = render_nav_html(active_item="health", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")
    lead_html = render_lead_form_html(
        "yoga",
        'Получите <span class="mt-hero-accent">бесплатный доступ навсегда</span> для студии йоги и пилатеса',
        "Оставьте контакты — покажем Молнию на примере вашей студии и поможем настроить расписание залов, реформеров и форму записи учеников.",
    )

    title = "Подключить онлайн-запись для студии йоги и пилатеса — расписание и CRM"
    description = (
        "Программа и онлайн-запись для студий йоги и пилатеса: "
        "наглядное расписание залов 24/7, бронь ковриков и реформеров, учёт абонементов и напоминания ученикам."
    )
    canonical = "https://molniya-tech.ru/yoga"

    faqs = [
        (
            "Как ученики записываются на практики йоги и пилатеса через Молнию?",
            "Вы получаете персональную страницу записи студии с вашим логотипом, фотографиями залов и перечнем направлений (хатха-йога, аштанга, виньяса, пилатес на матах и реформерах, здоровая спина, медитации). Ссылка размещается в соцсетях, мессенджерах или виджетом на сайте. Ученик видит актуальную сетку практик, оставшиеся коврики или реформеры и записывается за 1 минуту без скачивания приложений.",
        ),
        (
            "Как настраивается лимит мест на ковриках и пилатес-реформерах?",
            "Для каждого зала и направления вы указываете точную вместимость (например, 10–12 ковриков в большом зале или строго 6 реформеров в студии пилатеса). Как только все места заняты, программа закрывает запись на этот слот, предотвращая овербукинг и нехватку оборудования.",
        ),
        (
            "Как работает лист ожидания, если в группе закончились места?",
            "Если все коврики или реформеры заняты, ученик может записаться в лист ожидания. Если кто-то из записавшихся отменяет визит накануне, система автоматически предлагает освободившееся место следующему по очереди или отправляет быстрое уведомление.",
        ),
        (
            "Как вести учёт абонементов (пакетных, утренних, безлимитных) и заморозок?",
            "В карточке ученика фиксируется тип абонемента (разовое занятие, 4, 8, 12 практик или безлимит на месяц), срок действия и правила заморозки. При отметке посещения тренировка автоматически списывается с баланса, а ученик видит количество оставшихся занятий.",
        ),
        (
            "Можно ли настроить буфер между практиками на проветривание зала и смену инвентаря?",
            "Да. Вы задаёте обязательный технический перерыв (например, 15–20 минут) между уроками. Система автоматически учитывает его в сетке: группы не сталкиваются у входа, инструктор успевает подготовить реформеры, продезинфицировать коврики и зажечь благовония к следующей практике.",
        ),
        (
            "Где фиксируются ограничения по здоровью, травмы и уровень подготовки ученика?",
            "В форму онлайн-записи можно включить вопросы анкеты: опыт практики (новичок/продолжающий), травмы суставов, боли в пояснице, беременность. Преподаватель видит эти заметки в карточке записи до начала занятия и адаптирует асаны или упражнения на реформере.",
        ),
        (
            "Как бесплатно перенести базу учеников и расписание из другой CRM или Excel?",
            "Служба заботы Молнии бесплатно переносит базу учеников, действующие абонементы с остатком занятий и график преподавателей из Excel, Google Таблиц или сторонних систем (YClients, Dikidi, Fitbase и др.). Перенос занимает 15 минут и проходит без прерывания расписания студии.",
        ),
    ]

    faq_html = "\n".join(
        f'            <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
        for q, a in faqs
    )

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://molniya-tech.ru/"},
                {"@type": "ListItem", "position": 2, "name": "Здоровье и медицина", "item": "https://molniya-tech.ru/health"},
                {"@type": "ListItem", "position": 3, "name": "Онлайн-запись для студий йоги и пилатеса", "item": canonical},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Молния Тех — онлайн-запись и CRM для студий йоги и пилатеса",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web, iOS, Android, macOS, Windows",
            "url": canonical,
            "description": description,
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "RUB",
                "description": "Бесплатный демо-доступ и настройка расписания залов студии",
            },
            "publisher": {
                "@type": "Organization",
                "name": "ООО «МОЛНИЯ ТЕХ»",
                "url": "https://molniya-tech.ru",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a,
                    },
                }
                for q, a in faqs
            ],
        },
    ]
    json_ld_str = json.dumps(json_ld, ensure_ascii=False)

    page_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#FAF7F2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#12100E" media="(prefers-color-scheme: dark)">
  <link rel="canonical" href="{canonical}">

  <!-- Favicons -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- HERO -->
      <section class="mt-hero" data-screen-label="Герой" data-mt-hero-scene>

        <div class="mt-hero-lead">
          <h1 class="mt-hero-title">
            Онлайн-запись и расписание<br><span class="mt-hero-accent">для студий йоги и пилатеса</span>
          </h1>

          <div class="mt-hero-bottom">
            <div class="mt-hero-intro">
              <p class="mt-hero-sub">Персональная страница записи 24/7, наглядное расписание залов и реформеров, учёт абонементов и напоминания ученикам без рутины в чатах</p>
              <a class="mt-btn mt-btn-hero" href="#contact">Получить бесплатный доступ</a>
            </div>

            <ul class="mt-facets mt-facets--full" aria-label="Преимущества для студий йоги и пилатеса">
              <li class="mt-facet">
                <span class="mt-facet-name">Лимиты залов</span>
                <span class="mt-facet-note">контроль мест по коврикам и реформерам</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Доступно 24/7</span>
                <span class="mt-facet-note">страница записи без приложений</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Абонементы</span>
                <span class="mt-facet-note">разовые практики, пакеты и безлимиты</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name mt-facet-name--soon">Напоминания</span>
                <span class="mt-facet-note">E-mail, мессенджер или SMS на выбор</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <div class="mt-tablet">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для студии йоги и пилатеса: расписание практик и залов" width="1710" height="983" fetchpriority="high">
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </div>
            <p class="mt-hero-media-caption">Электронное расписание практик и загрузка залов студии в реальном времени</p>
          </div>
        </div>

      </section>

      <!-- LIVE SCHEDULE STATUS -->
      <section class="mt-section mt-reveal" data-screen-label="Расписание практик" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Каждая практика, зал и реформер <span class="mt-overview-hook">под вашим контролем</span></h2>
          <p class="mt-section-sub">Администратор и преподаватели видят занятость залов, статус групп и число оставшихся мест в реальном времени с любого устройства.</p>
        </div>

        <div class="mt-auto-bays">
          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">08:30 · Хатха-йога: Утренний флоу</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В зале</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Дарья К. · Зал 1 «Лотос»</div>
                <div class="mt-auto-car-tier">Групповая практика · 10 из 10 ковриков</div>
              </div>
              <span class="mt-dropdown-footer-icon">🌿</span>
            </div>
            <div class="mt-auto-service">
              <span>Утренняя хатха</span>
              <span class="mt-auto-price">По абонементу</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">10:15 · Пилатес на реформерах</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--done">Подтверждено</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Максим В. · Зал 2 «Реформер»</div>
                <div class="mt-auto-car-tier">Мини-группа · 5 из 6 реформеров</div>
              </div>
              <span class="mt-dropdown-footer-icon">⚡</span>
            </div>
            <div class="mt-auto-service">
              <span>Пилатес Reformer</span>
              <span class="mt-auto-price">Пробный урок</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">11:30 · Проветривание и подготовка</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--wait">Буфер</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Технический перерыв</div>
                <div class="mt-auto-car-tier">Дезинфекция ковриков, настройка пружин</div>
              </div>
              <span class="mt-dropdown-footer-icon">✨</span>
            </div>
            <div class="mt-auto-service">
              <span>Буферное время</span>
              <span class="mt-auto-price">В расписании</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">12:00 · Здоровая спина и йогатерапия</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--done">Подтверждено</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Елена М. · Зал 1 «Лотос»</div>
                <div class="mt-auto-car-tier">Мягкая терапевтическая практика · 8 из 8 ковриков</div>
              </div>
              <span class="mt-dropdown-footer-icon">🧘</span>
            </div>
            <div class="mt-auto-service">
              <span>Йогатерапия</span>
              <span class="mt-auto-price">По абонементу</span>
            </div>
          </div>
        </div>
      </section>

      <!-- YOGA OVERVIEW VALUE GRID -->
      <section class="mt-section mt-section--overview mt-reveal" data-screen-label="Функции для студий йоги и пилатеса" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Управляйте студией йоги и пилатеса <span class="mt-overview-hook">без накладок и путаницы в чатах</span></h2>
          <p class="mt-section-sub">Один сервис вместо блокнотов, таблиц и бесконечных сообщений: онлайн-расписание 24/7, контроль вместимости залов, бронь реформеров, учёт абонементов и автоматические напоминания ученикам.</p>
        </div>

        <div class="mt-overview-grid">
          <article class="mt-overview-card">
            <h3>Сетка практик и лимиты оборудования <span class="mt-overview-hook">без переполнения групп</span></h3>
            <p>Задайте точное число мест под размер каждого зала или количество реформеров. Система автоматически блокирует запись на полный слот, защищая от перегрузки залов и обеспечивая комфорт практики.</p>
            <div class="mt-overview-preview mt-overview-preview--schedule" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Расписание залов</span><span>Вместимость</span></div>
              <div class="mt-overview-calendar"><span>08:30</span><div class="mt-overview-slot">Зал 1: Хатха-йога <small>10 из 10 мест</small></div><span>10:15</span><div class="mt-overview-slot mt-overview-slot--light">Зал 2: Реформер <small>5 из 6 мест</small></div><span>11:30</span><div></div></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Персональная страница записи <span class="mt-overview-hook">в вашем фирменном стиле</span></h3>
            <p>Короткая ссылка для соцсетей, Telegram или встраиваемый виджет на сайт студии. Ученики сами выбирают практику (хатха, аштанга, пилатес, медитация), преподавателя и удобный слот за 1 минуту без ожидания ответа в директ.</p>
            <div class="mt-overview-preview mt-overview-preview--prices" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Страница бронирования</span><span>Доступно 24/7</span></div>
              <div class="mt-overview-price-row"><span>Классический пилатес</span><strong>55 мин · Выбор реформера</strong></div>
              <div class="mt-overview-price-row"><span>Удобная короткая ссылка</span><strong>Для соцсетей и мессенджеров</strong></div>
              <div class="mt-overview-price-tag">Ученики записываются сами в любое время</div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Автоматические напоминания <span class="mt-overview-hook">и меньше пропусков практик</span></h3>
            <p>Ученик получает мгновенное подтверждение после бронирования, а накануне практики — напоминание по E-mail, в мессенджер или по SMS. Он успеет предупредить об отмене, и место освободится для ученика из листа ожидания.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Автоматические напоминания</span><span>Без рутины</span></div>
              <div class="mt-overview-message">
                Ольга, напоминаем о практике хатха-йоги завтра в 08:30 в Зале «Лотос». Ждём вас за 10 минут до начала!
                <span class="mt-overview-reaction">🌿</span>
              </div>
              <div class="mt-overview-client-row"><span>E-mail, мессенджер или SMS</span><strong>На выбор клиента →</strong></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Учёт абонементов, пакетов и заморозок <span class="mt-overview-hook">в профиле ученика</span></h3>
            <p>Фиксируйте разовые практики, пробные визиты, пакетные абонементы на 4, 8 или 12 занятий и безлимиты. В централизованном профиле сохраняются история визитов, противопоказания по здоровью и остаток тренировок.</p>
            <div class="mt-overview-preview mt-overview-preview--process" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Карточка ученика</span><span>Ольга С. (Абонемент)</span></div>
              <div class="mt-overview-stages"><span>Пробный</span><i></i><span>Абонемент 12</span><i></i><span>Остаток: 7</span></div>
              <div class="mt-overview-check">✓ <span>Абонемент активен (списание по факту)</span></div>
              <div class="mt-overview-check">✓ <span>История практик и противопоказания учтены</span></div>
            </div>
          </article>

          <article class="mt-overview-card mt-overview-card--featured">
            <h3>Табель смен и зарплаты преподавателей <span class="mt-overview-hook">в один клик</span></h3>
            <p>Программа фиксирует проведенные групповые и индивидуальные классы каждого инструктора. В конце периода табель автоматически готов к расчету сдельной оплаты — без споров и ручного пересчёта бумажных журналов.</p>
            <div class="mt-overview-preview mt-overview-preview--metrics" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Учёт работы команды</span><span>Цифровой табель</span></div>
              <div class="mt-overview-metrics"><span>Залы<b>3</b></span><span>Инструкторы<b>8 в смене</b></span><span>Учёт<b>100%</b></span></div>
              <div class="mt-overview-chart"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            </div>
          </article>
        </div>

        <div class="mt-overview-action">
          <a class="mt-btn mt-btn-cta" href="#contact">Получить бесплатный доступ</a>
        </div>
      </section>

      <!-- YOGA JOURNEY -->
      <section class="mt-section mt-journey" data-screen-label="Путь ученика в студию">
        <div class="mt-section-head mt-section-head--center" data-mt-reveal>
          <h2 class="mt-section-title">Один визит на практику. <span class="mt-hero-accent">Полный порядок в студии.</span></h2>
          <p class="mt-section-sub">Посмотрите, как Молния автоматизирует запись в студию йоги и пилатеса: от выбора практики на странице бронирования до списания занятия с абонемента и отметки прихода в зал.</p>
        </div>

        <div class="mt-journey-example" aria-label="Пример прохождения практики" data-mt-reveal data-mt-delay="80">
          <span>Пример</span><strong>Пилатес на реформерах (мини-группа)</strong><span>Длительность 55 минут + 15 минут буфер на дезинфекцию и подготовку зала</span>
        </div>

        <div class="mt-journey-list">
          <article class="mt-journey-step">
            <div class="mt-journey-index">01</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Ученик</span>
              <h3>Выбор практики и удобного времени на странице записи 24/7</h3>
              <p>Клиент переходит по вашей короткой ссылке в соцсетях или мессенджере, выбирает направление (хатха, аштанга, реформер, спина) и видит только реальные свободные места.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--booking" aria-label="Пример бронирования практики">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Бронирование практики</span>
                <span class="mt-journey-proof-badge">Место забронировано</span>
              </div>
              <div class="mt-journey-proof-row"><span>Ученик</span><strong>Ольга С.</strong></div>
              <div class="mt-journey-proof-row"><span>Практика</span><strong>Пилатес на реформерах (55 мин)</strong></div>
              <div class="mt-journey-proof-row"><span>Зал и время</span><strong>Зал 2 «Реформер» · Среда, 10:15 – 11:10</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">02</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Форма приёма</span>
              <h3>Выбор типа абонемента и фиксация ограничений по здоровью</h3>
              <p>Ученик указывает контакты, выбирает абонемент или пробное занятие и отмечает ограничения (боли в спине, суставы). Слот автоматически фиксируется в расписании студии.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--process" aria-label="Анкета записи">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Запись #6240</span>
                <span class="mt-journey-proof-badge">Подтверждена</span>
              </div>
              <div class="mt-journey-proof-row"><span>Тип визита</span><strong>Абонемент на 12 практик</strong></div>
              <div class="mt-journey-proof-row"><span>Опыт / Здоровье</span><strong>Продолжающий · Внимание на поясницу</strong></div>
              <div class="mt-journey-proof-row"><span>Статус</span><strong>Реформер №3 закреплён</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">03</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Система</span>
              <h3>Дружеские автонапоминания накануне практики</h3>
              <p>Система заблаговременно отправляет ученику напоминание по E-mail, в мессенджер или по SMS с деталями визита (зал, форма одежды, код домофона студии).</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--order" aria-label="Сообщение с напоминанием">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Напоминание</span>
                <span class="mt-journey-proof-badge">Отправлено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Канал</span><strong>Мессенджер / E-mail / SMS</strong></div>
              <div class="mt-journey-proof-row"><span>Инфо</span><strong>Зал «Реформер», инструктор Максим В.</strong></div>
              <div class="mt-journey-proof-row"><span>Результат</span><strong>Ученик вовремя на практике</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">04</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Инструктор</span>
              <h3>Отметка прихода в зале и автосписание занятия</h3>
              <p>Преподаватель отмечает явку учеников в приложении. Занятие списывается с абонемента автоматически, а 15-минутный буфер позволяет подготовить зал к следующей группе.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--payout" aria-label="Результат визита">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Итог практики</span>
                <span class="mt-journey-proof-badge">Успешно</span>
              </div>
              <div class="mt-journey-proof-row"><span>Абонемент</span><strong>Осталось 7 из 12 практик</strong></div>
              <div class="mt-journey-proof-row"><span>Табель инструктора</span><strong>Практика учтена в смене</strong></div>
              <div class="mt-journey-proof-row"><span>Следующий шаг</span><strong>Запись на пятничный класс</strong></div>
            </div>
          </article>
        </div>
      </section>

      <!-- REAL-WORLD CASE STUDY -->
      <section class="mt-case-section mt-reveal" data-screen-label="Кейс студии йоги и пилатеса" data-mt-reveal>
        <div class="mt-case-card">
          <div class="mt-case-header">
            <div class="mt-case-tag">⚡ Кейс студии йоги и пилатеса</div>
            <h2 class="mt-case-title">Мария Соколова, сооснователь студии «Асана & Реформер»</h2>
            <blockquote class="mt-case-quote">
              «Раньше администраторы целый день сидели в переписках WhatsApp, вручную распределяя коврики и реформеры на пилатес. С Молнией ученики сами бронируют место за 1 минуту по ссылке в профиле, видя реальный остаток мест в группе. Мы полностью избавились от овербукинга, а учет абонементов и смен инструкторов теперь занимает секунды.»
            </blockquote>
            <div class="mt-case-author">
              Мария Соколова <span>· Сооснователь студии йоги и пилатеса на реформерах, <span style="white-space:nowrap">Санкт-Петербург</span></span>
            </div>
          </div>
          <div class="mt-case-stats">
            <div class="mt-case-stat">
              <span class="mt-case-num">0</span>
              <span class="mt-case-label">Овербукингов и накладок на реформерах благодаря строгому лимиту мест</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">3.5 ч</span>
              <span class="mt-case-label">В день сэкономлено администратором на ответах в чатах и ручной записи</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">100%</span>
              <span class="mt-case-label">Абонементов и проведенных практик учтены без бумажных журналов</span>
            </div>
          </div>
        </div>
      </section>

      <!-- YOGA FAQ -->
      <section id="faq" class="mt-section mt-reveal" data-screen-label="Вопросы и ответы" data-mt-reveal>
        <div class="mt-section-head">
          <h2 class="mt-section-title">Вопросы об онлайн-записи и программе для студий йоги и пилатеса</h2>
        </div>
        <div class="mt-before-start-grid">
          <article class="mt-before-start-highlight">
            <h3>Попробуйте Молнию для своей студии йоги и пилатеса</h3>
            <p>Бесплатно поможем настроить расписание залов, лимиты ковриков и реформеров, форму онлайн-записи и перенести базу постоянных учеников.</p>
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в мессенджер ↗</a>
          </article>
          <div class="mt-before-start-questions">
{faq_html}
          </div>
        </div>
        <p class="mt-before-start-privacy">Как мы обрабатываем данные — в <a href="/privacy">политике конфиденциальности</a>.</p>
      </section>

{lead_html}

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
'''
    return page_html

def build_thanks_page() -> str:
    """Builds the branded Thank You page with direct presentation download."""
    nav_html = render_nav_html(active_item="", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Спасибо за заявку — Молния Тех</title>
  <meta name="description" content="Спасибо за обращение в Молнию! Ваша заявка успешно принята. Скачайте подробную презентацию возможностей платформы.">
  <meta name="robots" content="noindex, follow">
  <meta name="theme-color" content="#FAF7F2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#12100E" media="(prefers-color-scheme: dark)">
  <link rel="canonical" href="https://molniya-tech.ru/thanks">

  <!-- Favicons -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- THANKS MAIN -->
      <main class="mt-404-main">
        <div class="mt-404-container">
          <div class="mt-404-spark" aria-hidden="true" style="margin-bottom: 20px;">
            <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#D2634A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          </div>
          <h1 class="mt-404-title">Спасибо! Ваша заявка принята</h1>
          <p class="mt-404-desc">
            Мы свяжемся с вами в ближайшее время по указанным контактам.
            А пока изучите подробную презентацию: как устроена онлайн-запись 24/7, управление расписанием и единая база клиентов.
          </p>

          <div class="mt-404-actions" style="display:flex; flex-direction:column; gap:16px; align-items:center;">
            <a class="mt-btn mt-btn-hero" href="/assets/docs/molniya-presentation.pdf" download="Презентация Молния Тех.pdf" style="display:inline-flex; align-items:center; gap:10px;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              Скачать презентацию Молнии (PDF, 1.3 МБ)
            </a>
            <a href="/" class="mt-link-subtle" style="font-size:14px; text-decoration:none;">Вернуться на главную страницу →</a>
          </div>

          <div class="mt-404-help" style="margin-top:36px;">
            Срочный вопрос или хотите начать быстрее?
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener" class="mt-link-accent">Напишите нам в Telegram напрямую →</a>
          </div>
        </div>
      </main>

{footer_html}

    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
"""


def build_education_page() -> str:
    """Builds the complete education landing page matching the exact design system."""
    nav_html = render_nav_html(active_item="education", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")
    lead_html = render_lead_form_html(
        "education",
        'Получите <span class="mt-hero-accent">бесплатный доступ навсегда</span> для учебного центра',
        "Оставьте контакты — поможем настроить расписание групп, учет абонементов и онлайн-запись на уроки.",
    )

    title = "CRM для учебных центров, школ танцев и курсов — онлайн-запись и расписание Молния"
    description = (
        "Программа и CRM для образовательных центров, студий танцев, языковых школ и секций: "
        "учет абонементов и посещаемости, расписание групп и преподавателей, онлайн-запись на пробные уроки."
    )
    canonical = "https://molniya-tech.ru/education"

    faqs = [
        (
            "Подходит ли Молния для языковых школ, танцевальных студий и спортивных секций?",
            "Да. Система идеально адаптируется под любой формат обучения: групповые занятия, индивидуальные уроки с репетитором, мастер-классы и курсы. Вы настраиваете направления, длительность уроков, вместимость залов и типы абонементов.",
        ),
        (
            "Как работает автоматический учет абонементов и списание занятий?",
            "При отметке визита ученика в журнале занятие автоматически списывается с его баланса в 1 клик. Программа отслеживает срок действия абонемента, остаток уроков и заблаговременно напоминает родителям или ученику о продлении через мессенджер.",
        ),
        (
            "Можно ли настроить заморозку абонементов и перерасчет по справкам?",
            "Да. Администратор может заморозить абонемент ученика на нужный срок (например, по болезни или на время каникул). Срок действия абонемента автоматически продлевается без потери оплаченных занятий и без путаницы в таблицах.",
        ),
        (
            "Как программа предотвращает накладки преподавателей и пересечение аудиторий?",
            "Шахматка Молнии учитывает сразу несколько ограничений: занятость конкретного преподавателя, доступность нужного зала или аудитории и вместимость группы. Назначить двух педагогов в один кабинет или переполнить группу технически невозможно.",
        ),
        (
            "Как происходит расчет сдельной зарплаты преподавателей и тренеров?",
            "В системе настраивается любая схема мотивации: фиксированная ставка за проведенный урок, процент от стоимости абонементов группы, доплата за каждого фактически пришедшего ученика или ставка за индивидуальные уроки. Начисления происходят автоматически в реальном времени.",
        ),
        (
            "Как ученики и родители получают напоминания о занятиях?",
            "Сервисный бот в мессенджере отправляет автоматические уведомления за 24 и за 2 часа до урока: напоминает время, кабинет и тему занятия. Это снижает число пропусков без уважительной причины на 80% и избавляет администраторов от ручных обзвонов.",
        ),
        (
            "Как бесплатно перенести базу учеников и историю абонементов из Excel или старой CRM?",
            "Служба заботы Молнии бесплатно помогает перенести список учеников, контактные данные родителей, действующие абонементы, каталог предметов и график преподавателей. Вы начнете работу без срыва учебного процесса и без потери данных.",
        ),
    ]

    faq_html = "\n".join(
        f'            <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
        for q, a in faqs
    )

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://molniya-tech.ru/"},
                {"@type": "ListItem", "position": 2, "name": "Образование", "item": canonical},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Молния Тех — CRM для учебных центров, школ танцев и курсов",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web, iOS, Android, macOS, Windows",
            "url": canonical,
            "description": description,
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "RUB",
                "description": "Бесплатный демо-доступ и настройка расписания групп",
            },
            "publisher": {
                "@type": "Organization",
                "name": "ООО «МОЛНИЯ ТЕХ»",
                "url": "https://molniya-tech.ru",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a,
                    },
                }
                for q, a in faqs
            ],
        },
    ]
    json_ld_str = json.dumps(json_ld, ensure_ascii=False)

    page_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#FAF7F2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#12100E" media="(prefers-color-scheme: dark)">
  <link rel="canonical" href="{canonical}">

  <!-- Favicons -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- HERO -->
      <section class="mt-hero" data-screen-label="Герой" data-mt-hero-scene>

        <div class="mt-hero-lead">
          <h1 class="mt-hero-title">
            CRM для учебных центров,<br><span class="mt-hero-accent">школ танцев и курсов</span>
          </h1>

          <div class="mt-hero-bottom">
            <div class="mt-hero-intro">
              <p class="mt-hero-sub">Учет абонементов и посещаемости, онлайн-запись на пробные уроки, расписание преподавателей и залов</p>
              <a class="mt-btn mt-btn-hero" href="#contact">Получить бесплатный доступ</a>
            </div>

            <ul class="mt-facets mt-facets--full" aria-label="Преимущества для образовательных центров">
              <li class="mt-facet">
                <span class="mt-facet-name">Группы и индивидуально</span>
                <span class="mt-facet-note">расписание преподавателей и аудиторий</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Умные абонементы</span>
                <span class="mt-facet-note">автосписание занятий, заморозки и остатки</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Зарплата педагогов</span>
                <span class="mt-facet-note">сдельная ставка за ученика или группу</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name mt-facet-name--soon">AI & Забота</span>
                <span class="mt-facet-note">Напоминания в мессенджер об уроках и продлениях</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <div class="mt-tablet">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для учебных центров и курсов: расписание групп и электронный журнал посещаемости" width="1710" height="983" fetchpriority="high">
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </div>
            <p class="mt-hero-media-caption">Электронное расписание занятий и загрузка аудиторий в реальном времени</p>
          </div>
        </div>

      </section>

      <!-- LIVE CLASSROOMS STATUS -->
      <section class="mt-section mt-reveal" data-screen-label="Загрузка аудиторий и групп" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Все аудитории, группы и преподаватели <span class="mt-overview-hook">под полным контролем</span></h2>
          <p class="mt-section-sub">Администратор и руководитель видят статус каждой аудитории, текущую группу, число учеников и тему занятия в реальном времени на любом устройстве.</p>
        </div>

        <div class="mt-auto-bays">
          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Ауд. 1 · Английский</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В уроке</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Teens B1 (Ольга К.)</div>
                <div class="mt-auto-car-tier">Past Perfect · Присутствует 8/8</div>
              </div>
              <span class="mt-dropdown-footer-icon">🇬🇧</span>
            </div>
            <div class="mt-auto-service">
              <span>Групповой урок 90 мин</span>
              <span class="mt-auto-price">7 200 ₽ (списано)</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Зал 2 · Студия танцев</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">Идет урок</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Contemporary (Михаил Д.)</div>
                <div class="mt-auto-car-tier">Постановка номера · 12 учеников</div>
              </div>
              <span class="mt-dropdown-footer-icon">🩰</span>
            </div>
            <div class="mt-auto-service">
              <span>Абонементы (12 уроков)</span>
              <span class="mt-auto-price">9 600 ₽ (списано)</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Ауд. 3 · Робототехника</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--done">Готово</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Младшая группа (19:00)</div>
                <div class="mt-auto-car-tier">Lego WeDo 2.0 · 6 мест занято</div>
              </div>
              <span class="mt-dropdown-footer-icon">🤖</span>
            </div>
            <div class="mt-auto-service">
              <span>Практикум по сборке</span>
              <span class="mt-auto-price">5 400 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Каб. 4 · Репетитор</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--wait">Ожидание</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Артём В. (19:30)</div>
                <div class="mt-auto-car-tier">Пробный урок · Подготовка к ОГЭ</div>
              </div>
              <span class="mt-dropdown-footer-icon">📐</span>
            </div>
            <div class="mt-auto-service">
              <span>Индивидуальное занятие</span>
              <span class="mt-auto-price">1 800 ₽</span>
            </div>
          </div>
        </div>
      </section>

      <!-- EDUCATION OVERVIEW VALUE GRID -->
      <section class="mt-section mt-section--overview mt-reveal" data-screen-label="Функции для учебных центров" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Ведите учебный процесс <span class="mt-overview-hook">от пробного урока до выпуска группы</span></h2>
          <p class="mt-section-sub">Программа для учета в учебном центре, языковой школе и студии танцев: электронный журнал, баланс абонементов, контроль посещаемости и автоматический расчет выработки педагогов.</p>
        </div>

        <div class="mt-overview-grid">
          <article class="mt-overview-card">
            <h3><span class="mt-overview-hook">Расписание групп</span> и аудиторий</h3>
            <p>Наглядная шахматка по преподавателям, аудиториям и предметам. Удобный перенос занятий в один клик, учет вместимости классов и исключение накладок в расписании.</p>
            <div class="mt-overview-preview mt-overview-preview--schedule" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Расписание занятий</span><span>Сегодня</span></div>
              <div class="mt-overview-calendar"><span>15:00</span><div></div><span>16:30</span><div class="mt-overview-slot">Ауд. 1 <small>Английский · Группа B1 Teens</small></div><span>18:00</span><div class="mt-overview-slot mt-overview-slot--light">Зал 2 <small>Танцы · Contemporary Kids</small></div></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Учет абонементов, баланса <span class="mt-overview-hook">и заморозок</span></h3>
            <p>Автоматическое списание уроков при отметке в журнале. Программа отслеживает срок действия абонементов, считает остаток уроков, оформляет заморозки по справкам и напоминает о продлении.</p>
            <div class="mt-overview-preview mt-overview-preview--prices" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Карточка абонемента</span><span>Артём Васильев</span></div>
              <div class="mt-overview-price-row"><span>Абонемент «Курс 8 уроков»</span><strong>Осталось 5 из 8 · Активен</strong></div>
              <div class="mt-overview-price-row"><span>Срок действия</span><strong>до 28 октября · Без долгов</strong></div>
              <div class="mt-overview-price-tag">Автосписание при отметке в журнале</div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Онлайн-запись на пробные <span class="mt-overview-hook">и виджет для сайта</span></h3>
            <p>Родители и ученики записываются на бесплатные или платные пробные уроки прямо с сайта и из соцсетей 24/7. Заявка мгновенно попадает в CRM, закрепляя слот за учеником без звонков.</p>
            <div class="mt-overview-preview mt-overview-preview--process" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Онлайн-запись на урок</span><span>Английский язык</span></div>
              <div class="mt-overview-stages"><span>Курс</span><i></i><span>Группа</span><i></i><span>Запись</span></div>
              <div class="mt-overview-check">✓ <span>Пробный урок забронирован на 19:00</span></div>
              <div class="mt-overview-check">✓ <span>Анкета ученика добавлена в CRM</span></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Напоминания в мессенджер ученикам <span class="mt-overview-hook">и родителям</span></h3>
            <p>Сервисный бот предупреждает о занятии за 24 и 2 часа, напоминает взять сменную обувь или форму, а родителям отправляет отчет об успеваемости и напоминание о скором окончании абонемента.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Уведомление в мессенджер</span><span>Школа «Ритм»</span></div>
              <div class="mt-overview-message">
                Елена, напоминаем: сегодня в 18:30 у Софии урок танцев в Зале №2. Пожалуйста, не забудьте чешки.
                <span class="mt-overview-reaction">🩰</span>
              </div>
              <div class="mt-overview-client-row"><span>База учеников и групп</span><strong>Посещаемость и баланс абонементов →</strong></div>
            </div>
          </article>

          <article class="mt-overview-card mt-overview-card--featured">
            <h3>Сдельная зарплата преподавателей <span class="mt-overview-hook">и тренеров</span></h3>
            <p>Гибкая мотивация преподавателей: ставка за урок, процент от собранных абонементов, доплата за каждого присутствующего ученика или фикс за отработанные часы. Баланс рассчитывается автоматически.</p>
            <div class="mt-overview-preview mt-overview-preview--metrics" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Выработка преподавателя</span><span>Ольга К. (Неделя)</span></div>
              <div class="mt-overview-metrics"><span>Уроки<b>18</b></span><span>Ученики<b>144</b></span><span>Баланс<b>₽</b></span></div>
              <div class="mt-overview-chart"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            </div>
          </article>
        </div>

        <div class="mt-overview-action">
          <a class="mt-btn mt-btn-cta" href="#contact">Получить бесплатный доступ</a>
        </div>
      </section>

      <!-- EDUCATION JOURNEY -->
      <section class="mt-section mt-journey" data-screen-label="Путь ученика">
        <div class="mt-section-head mt-section-head--center" data-mt-reveal>
          <h2 class="mt-section-title">Один новый ученик. <span class="mt-hero-accent">Полный порядок в школе.</span></h2>
          <p class="mt-section-sub">Посмотрите, как Молния автоматизирует путь от первой заявки на пробный урок до регулярных посещений, автосписания занятий и прозрачного начисления зарплаты педагогу.</p>
        </div>

        <div class="mt-journey-example" aria-label="Пример прохождения записи на курс" data-mt-reveal data-mt-delay="80">
          <span>Пример</span><strong>Запись на курс английского языка</strong><span>Группа Teens B1 · Артём В.</span>
        </div>

        <div class="mt-journey-list">
          <article class="mt-journey-step">
            <div class="mt-journey-index">01</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Родитель / Ученик</span>
              <h3>Онлайн-запись на пробный урок за 1 минуту</h3>
              <p>Родитель выбирает направление, удобный филиал и время пробного занятия через виджет на сайте или в мессенджере. Слот в группе резервируется автоматически.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--booking" aria-label="Пример онлайн-записи">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Онлайн-запись</span>
                <span class="mt-journey-proof-badge">Подтверждено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Ученик</span><strong>Артём Васильев (14 лет)</strong></div>
              <div class="mt-journey-proof-row"><span>Направление</span><strong>Английский язык (Teens)</strong></div>
              <div class="mt-journey-proof-row"><span>Формат</span><strong>Пробный урок (бесплатно)</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">02</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Администратор</span>
              <h3>Встреча в центре и отметка в электронном журнале</h3>
              <p>Администратор встречает ученика, открывает карточку в планшете и отмечает приход в 1 тап. Преподаватель сразу видит нового студента в составе группы.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--process" aria-label="Карточка занятия">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Визит #2940</span>
                <span class="mt-journey-proof-badge">Присутствует</span>
              </div>
              <div class="mt-journey-proof-row"><span>Группа</span><strong>Teens B1 · Ауд. 1</strong></div>
              <div class="mt-journey-proof-row"><span>Преподаватель</span><strong>Ольга Ковалёва</strong></div>
              <div class="mt-journey-proof-row"><span>Статус</span><strong>Пробный урок пройден</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">03</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Преподаватель</span>
              <h3>Проведение занятия и комментарий по уровню знаний</h3>
              <p>После занятия педагог оставляет короткую заметку в карточке ученика со смартфона: уровень знаний, рекомендации по учебным материалам и подходящая группа.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--order" aria-label="Итоги урока">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Итог урока</span>
                <span class="mt-journey-proof-badge">Рекомендовано</span>
              </div>
              <div class="mt-journey-proof-row"><span>Уровень</span><strong>Intermediate (B1.1)</strong></div>
              <div class="mt-journey-proof-row"><span>Группа</span><strong>Вторник / Четверг 18:00</strong></div>
              <div class="mt-journey-proof-row"><span>Заметка</span><strong>«Отличная грамматика, готов к B1»</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">04</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Система & Руководитель</span>
              <h3>Оплата абонемента, расчет педагога и автонапоминания</h3>
              <p>Родитель оплачивает абонемент на 8 занятий. Программа автоматически начисляет ставку преподавателю, формирует график уроков и отправляет памятку в мессенджере.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--payout" aria-label="Финансовый расчет">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Абонемент активирован</span>
                <span class="mt-journey-proof-badge">Оплачено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Абонемент</span><strong>8 уроков (6 400 ₽)</strong></div>
              <div class="mt-journey-proof-row"><span>Начислено педагогу</span><strong>+800 ₽ за урок</strong></div>
              <div class="mt-journey-proof-row"><span>Бот в мессенджере</span><strong>«График уроков отправлен»</strong></div>
            </div>
          </article>
        </div>
      </section>

      <!-- REAL-WORLD CASE STUDY -->
      <section class="mt-case-section mt-reveal" data-screen-label="Кейс школы танцев и языковых курсов" data-mt-reveal>
        <div class="mt-case-card">
          <div class="mt-case-header">
            <div class="mt-case-tag">⚡ Кейс школы танцев и языковых курсов</div>
            <h2 class="mt-case-title">Школа современных искусств и языков «Ритм», 3 филиала</h2>
            <blockquote class="mt-case-quote">
              «Раньше администраторы тратили полдня на сверку бумажных абонементов, перерасчет пропусков по справкам и ручной подсчет ставок тренеров. В Молнии списание уроков, заморозки и зарплаты происходят в 1 клик. Доходимость до пробных выросла на 80%, а споры о списаниях прекратились.»
            </blockquote>
            <div class="mt-case-author">
              Анастасия Белова <span>· Основательница и директор, <span style="white-space:nowrap">Санкт-Петербург</span></span>
            </div>
          </div>
          <div class="mt-case-stats">
            <div class="mt-case-stat">
              <span class="mt-case-num">+35%</span>
              <span class="mt-case-label">Рост конверсии из пробного урока в покупку постоянного абонемента</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">0</span>
              <span class="mt-case-label">Спорных списаний занятий и потерянных уроков за всё время работы</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">15 <small>мин</small></span>
              <span class="mt-case-label">На перенос базы учеников, настройку групп и запуск расписания в работу</span>
            </div>
          </div>
        </div>
      </section>

      <!-- EDUCATION FAQ -->
      <section id="faq" class="mt-section mt-reveal" data-screen-label="Вопросы и ответы" data-mt-reveal>
        <div class="mt-section-head">
          <h2 class="mt-section-title">Вопросы о программе для учебных центров, курсов и студий танцев</h2>
        </div>
        <div class="mt-before-start-grid">
          <article class="mt-before-start-highlight">
            <h3>Попробуйте CRM Молния для своего учебного центра</h3>
            <p>Бесплатно поможем настроить расписание групп, типы абонементов, правила заморозок и формулы зарплат педагогов. Запустите центр без пауз в учебном процессе.</p>
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в мессенджер ↗</a>
          </article>
          <div class="mt-before-start-questions">
{faq_html}
          </div>
        </div>
        <p class="mt-before-start-privacy">Как мы обрабатываем данные — в <a href="/privacy">политике конфиденциальности</a>.</p>
      </section>

{lead_html}

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
'''
    return page_html


def build_pets_page() -> str:
    """Builds the complete pets landing page matching the exact design system."""
    nav_html = render_nav_html(active_item="pets", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")
    lead_html = render_lead_form_html(
        "pets",
        'Получите <span class="mt-hero-accent">бесплатный доступ навсегда</span> для груминг-салона',
        "Оставьте контакты — поможем настроить расписание столов, карточки питомцев с породами и онлайн-запись.",
    )

    title = "CRM для груминг-салона: запись и расписание | Молния"
    description = (
        "CRM для груминг-салона: онлайн-запись, карточки питомцев, расписание столов и мастеров, "
        "напоминания клиентам и расчет зарплат грумеров."
    )
    canonical = "https://molniya-tech.ru/pets"

    faqs = [
        (
            "Учитывает ли Молния разную длительность процедур для мелких и крупных пород?",
            "Да. В каталоге услуг можно настроить индивидуальный хронометраж и стоимость для каждой категории: от йорка (1.5 часа) до самоеда или хаски (3–3.5 часа). При записи система автоматически резервирует правильный слот в расписании мастера, исключая накладки и задержки следующих клиентов.",
        ),
        (
            "Можно ли вести подробную карточку питомца с историей стрижек и особенностями поведения?",
            "Конечно. В карточке питомца сохраняются кличка, порода, вес, дата рождения, отметки о характере (боязнь фена, агрессия, чувствительная кожа), аллергии на косметику и история всех визитов с фотографиями «до и после».",
        ),
        (
            "Как рассчитывается сдельная зарплата грумеров?",
            "Молния автоматически рассчитывает вознаграждение мастеров по гибким правилам: процент от стоимости стрижки или комплекса (например, 40–50%), надбавки за агрессию или вычес колтунов, вычет себестоимости премиальной косметики или фиксированная ставка за смену. Баланс мастера обновляется сразу после закрытия визита.",
        ),
        (
            "Как работает онлайн-запись для владельцев питомцев?",
            "Виджет онлайн-записи устанавливается на сайт, в соцсети и мессенджеры. Владелец выбирает вид животного (собака, кошка), породу, вес и нужный комплекс (стрижка, экспресс-линька, гигиена, чистка зубов), после чего выбирает мастера и удобное время. Запись мгновенно резервирует стол в салоне 24/7.",
        ),
        (
            "Как отправляются напоминания владельцам и уведомление о готовности питомца?",
            "Сервисный бот в мессенджере напоминает владельцу о визите за 24 и за 2 часа, а во время процедуры мастер или администратор в 1 клик отправляет уведомление: «Ваш питомец готов, можно забирать!». А через 4–6 недель система заботливо приглашает на регулярный уход, возвращая постоянных клиентов.",
        ),
        (
            "Можно ли распределять записи между грумерами и столами?",
            "Да. В расписании видна занятость мастеров и столов. При записи администратор выбирает подходящего грумера, длительность процедуры и свободное время, чтобы избежать пересечений.",
        ),
        (
            "Как бесплатно перенести базу клиентов и питомцев из Excel или другой программы?",
            "Служба заботы Молнии бесплатно помогает перенести базу владельцев, клички и породы питомцев, историю посещений, каталог услуг и график работы мастеров. Перенос выполняется за 1 день без остановки работы салона.",
        ),
    ]

    faq_html = "\n".join(
        f'            <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
        for q, a in faqs
    )

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://molniya-tech.ru/"},
                {"@type": "ListItem", "position": 2, "name": "Груминг-салоны", "item": canonical},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Молния Тех — CRM для груминг-салонов",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web, iOS, Android, macOS, Windows",
            "url": canonical,
            "description": description,
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "RUB",
                "description": "Бесплатный демо-доступ и настройка расписания столов груминга",
            },
            "publisher": {
                "@type": "Organization",
                "name": "ООО «МОЛНИЯ ТЕХ»",
                "url": "https://molniya-tech.ru",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a,
                    },
                }
                for q, a in faqs
            ],
        },
    ]
    json_ld_str = json.dumps(json_ld, ensure_ascii=False)

    page_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#FAF7F2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#12100E" media="(prefers-color-scheme: dark)">
  <link rel="canonical" href="{canonical}">

  <!-- Favicons -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- HERO -->
      <section class="mt-hero" data-screen-label="Герой" data-mt-hero-scene>

        <div class="mt-hero-lead">
          <h1 class="mt-hero-title">
            CRM для груминг-салонов:<br><span class="mt-hero-accent">запись и расписание</span>
          </h1>

          <div class="mt-hero-bottom">
            <div class="mt-hero-intro">
              <p class="mt-hero-sub">Учет питомцев по породам и весу, онлайн-запись 24/7, расписание столов и мастеров, расчет зарплат и напоминания о регулярном груминге</p>
              <a class="mt-btn mt-btn-hero" href="#contact">Получить бесплатный доступ</a>
            </div>

            <ul class="mt-facets mt-facets--full" aria-label="Преимущества для зообизнеса">
              <li class="mt-facet">
                <span class="mt-facet-name">Породы и вес</span>
                <span class="mt-facet-note">авторасчет времени процедуры под породу</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Карточка питомца</span>
                <span class="mt-facet-note">повадки, аллергии, ветпаспорт и история визитов</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Зарплата мастеров</span>
                <span class="mt-facet-note">сдельный расчет % от услуг с вычетом косметики</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name mt-facet-name--soon">AI & Забота</span>
                <span class="mt-facet-note">Напоминания в мессенджер о повторной стрижке через 4 недели</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <div class="mt-tablet">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для груминг-салонов: электронное расписание столов и запись питомцев" width="1710" height="983" fetchpriority="high">
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </div>
            <p class="mt-hero-media-caption">Электронное расписание столов и мастеров груминга в реальном времени</p>
          </div>
        </div>

      </section>

      <!-- LIVE STATIONS STATUS -->
      <section class="mt-section mt-reveal" data-screen-label="Загрузка столов и мастеров" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Все столы груминга, мастера и пушистые гости <span class="mt-overview-hook">под полным контролем</span></h2>
          <p class="mt-section-sub">Администратор и руководитель видят статус каждого стола, текущую породу, назначенного мастера и этап процедуры в реальном времени на любом устройстве.</p>
        </div>

        <div class="mt-auto-bays">
          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Стол 1 · Комплексный груминг</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В работе</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Йоркширский терьер «Микки»</div>
                <div class="mt-auto-car-tier">Мастер: Анна В. · Модельная стрижка + гигиена</div>
              </div>
              <span class="mt-dropdown-footer-icon">🐶</span>
            </div>
            <div class="mt-auto-service">
              <span>Комплекс для мелких пород</span>
              <span class="mt-auto-price">3 200 ₽ (в работе)</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Стол 2 · Экспресс-линька</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В работе</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Самоедская собака «Буран»</div>
                <div class="mt-auto-car-tier">Мастер: Денис С. · Вычес + турбосушка (28 кг)</div>
              </div>
              <span class="mt-dropdown-footer-icon">🐕</span>
            </div>
            <div class="mt-auto-service">
              <span>Экспресс-линька крупных пород</span>
              <span class="mt-auto-price">6 500 ₽ (в работе)</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Ванная зона · Спа и гигиена</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--done">Готово</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Мейн-кун «Барс» (16:30)</div>
                <div class="mt-auto-car-tier">Вычес + мытье без седации · Готов к выдаче</div>
              </div>
              <span class="mt-dropdown-footer-icon">🐱</span>
            </div>
            <div class="mt-auto-service">
              <span>Комплексный уход за кошкой</span>
              <span class="mt-auto-price">4 000 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Стол 3 · Стрижка и уход</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--wait">Ожидание</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Французский бульдог «Оскар» (17:00)</div>
                <div class="mt-auto-car-tier">Владелец: Дмитрий · Стрижка по породе</div>
              </div>
              <span class="mt-dropdown-footer-icon">🐶</span>
            </div>
            <div class="mt-auto-service">
              <span>Стрижка + уход за когтями</span>
              <span class="mt-auto-price">2 400 ₽</span>
            </div>
          </div>
        </div>
      </section>

      <!-- PETS OVERVIEW VALUE GRID -->
      <section class="mt-section mt-section--overview mt-reveal" data-screen-label="Функции для зообизнеса" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Ведите заботливый зообизнес <span class="mt-overview-hook">от первого щенка до постоянного клиента</span></h2>
          <p class="mt-section-sub">Программа для учета в груминг-салоне: расписание столов и мастеров, карточки питомцев, расчет зарплаты грумеров и автоматические напоминания владельцам.</p>
        </div>

        <div class="mt-overview-grid">
          <article class="mt-overview-card">
            <h3>Умный тайминг под породу <span class="mt-overview-hook">и вес питомца</span></h3>
            <p>Наглядная шахматка по столам, ваннам и мастерам. Система автоматически резервирует нужное время: от 1.5 часов для йорка до 3.5 часов для самоеда. Никаких накладок и задержек клиентов.</p>
            <div class="mt-overview-preview mt-overview-preview--schedule" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Расписание столов</span><span>Сегодня</span></div>
              <div class="mt-overview-calendar"><span>14:00</span><div></div><span>15:30</span><div class="mt-overview-slot">Стол 1 <small>Йорк Микки · Комплекс 90 мин</small></div><span>17:00</span><div class="mt-overview-slot mt-overview-slot--light">Стол 2 <small>Самоед Буран · Экспресс-линька</small></div></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Карточка питомца: <span class="mt-overview-hook">повадки, аллергии и фото</span></h3>
            <p>Карточка каждого питомца: порода, вес, аллергии на косметику, отметки о боязни фена или стрессе и фото стрижек «до и после» для сохранения пожеланий владельца.</p>
            <div class="mt-overview-preview mt-overview-preview--prices" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Карточка питомца</span><span>Померанский шпиц «Марси»</span></div>
              <div class="mt-overview-price-row"><span>Порода и вес</span><strong>Шпиц мини · 3.2 кг</strong></div>
              <div class="mt-overview-price-row"><span>Особенности</span><strong>Боится громкого фена · Косметика Hydra</strong></div>
              <div class="mt-overview-price-tag">История 8 визитов · Фотострижки в профиле</div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Онлайн-запись 24/7 <span class="mt-overview-hook">с выбором породы</span></h3>
            <p>Владельцы записывают собак и кошек прямо с сайта и канала в мессенджере. Форма сама предлагает выбрать породу, вес и допуслуги (чистка зубов, стрижка когтей), показывая точную стоимость.</p>
            <div class="mt-overview-preview mt-overview-preview--process" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Онлайн-запись в салон</span><span>Груминг собак</span></div>
              <div class="mt-overview-stages"><span>Порода</span><i></i><span>Услуга</span><i></i><span>Запись</span></div>
              <div class="mt-overview-check">✓ <span>Питомец: Померанский шпиц (стрижка «Модерн»)</span></div>
              <div class="mt-overview-check">✓ <span>Запись подтверждена: Сегодня 15:30</span></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Напоминания в мессенджер <span class="mt-overview-hook">и «Питомец готов!»</span></h3>
            <p>Сервисный бот предупреждает о записи за 24 и 2 часа, отправляет уведомление в 1 клик, когда питомца можно забирать, и заботливо приглашает на повторный груминг через 4–6 недель.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Уведомление в мессенджер</span><span>Салон «Лапки»</span></div>
              <div class="mt-overview-message">
                Ольга, здравствуйте! Стрижка Марси завершена, питомец помыт и расчесан. Ждем вас в салоне до 18:00!
                <span class="mt-overview-reaction">🐾</span>
              </div>
              <div class="mt-overview-client-row"><span>База клиентов и питомцев</span><strong>Цикл повторных визитов 4–5 недель →</strong></div>
            </div>
          </article>

          <article class="mt-overview-card mt-overview-card--featured">
            <h3>Сдельная зарплата мастеров <span class="mt-overview-hook">и расход косметики</span></h3>
            <p>Автоматический расчет зарплаты грумеров: процент от стоимости стрижки, доплаты за вычес колтунов и работу с тревожными питомцами, учет стоимости премиум-косметики. Баланс считается мгновенно.</p>
            <div class="mt-overview-preview mt-overview-preview--metrics" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Выработка мастера</span><span>Анна В. (Топ-грумер)</span></div>
              <div class="mt-overview-metrics"><span>Визиты<b>24</b></span><span>Питомцы<b>24</b></span><span>Зарплата<b>₽</b></span></div>
              <div class="mt-overview-chart"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            </div>
          </article>
        </div>

        <div class="mt-overview-action">
          <a class="mt-btn mt-btn-cta" href="#contact">Получить бесплатный доступ</a>
        </div>
      </section>

      <!-- PETS JOURNEY -->
      <section class="mt-section mt-journey" data-screen-label="Путь пушистого гостя">
        <div class="mt-section-head mt-section-head--center" data-mt-reveal>
          <h2 class="mt-section-title">Один пушистый клиент. <span class="mt-hero-accent">Полный порядок в салоне.</span></h2>
          <p class="mt-section-sub">Посмотрите, как Молния автоматизирует путь от онлайн-записи с выбором породы до приема в салоне, груминга, отправки фото хозяину и начисления зарплаты мастеру.</p>
        </div>

        <div class="mt-journey-example" aria-label="Пример прохождения записи в салон груминга" data-mt-reveal data-mt-delay="80">
          <span>Пример</span><strong>Комплексный уход за шпицем</strong><span>Померанский шпиц «Марси» (3.2 кг)</span>
        </div>

        <div class="mt-journey-list">
          <article class="mt-journey-step">
            <div class="mt-journey-index">01</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Владелец питомца</span>
              <h3>Онлайн-запись с выбором породы за 1 минуту</h3>
              <p>Хозяйка выбирает породу собаки, комплекс «Полный уход + экспресс-линька» и удобное время в виджете онлайн-записи. Слот на столе груминга бронируется автоматически.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--booking" aria-label="Пример онлайн-записи">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Онлайн-запись</span>
                <span class="mt-journey-proof-badge">Подтверждено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Питомец</span><strong>Шпиц «Марси» (3.2 кг)</strong></div>
              <div class="mt-journey-proof-row"><span>Комплекс</span><strong>Полный уход + вычес</strong></div>
              <div class="mt-journey-proof-row"><span>Слот</span><strong>Сегодня, 15:30 (Стол 1)</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">02</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Администратор</span>
              <h3>Прием питомца, осмотр шерсти и фиксация пожеланий</h3>
              <p>Администратор встречает владельца с собакой, открывает карточку питомца в планшете, отмечает наличие колтунов и индивидуальные пожелания по длине шерсти.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--process" aria-label="Карточка приема питомца">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Визит #1842</span>
                <span class="mt-journey-proof-badge">В работе</span>
              </div>
              <div class="mt-journey-proof-row"><span>Мастер</span><strong>Анна В. (Топ-грумер)</strong></div>
              <div class="mt-journey-proof-row"><span>Особенности</span><strong>Колтуны за ушами, боится фена</strong></div>
              <div class="mt-journey-proof-row"><span>Косметика</span><strong>Линейка Hydra Sensitive</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">03</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Грумер</span>
              <h3>Проведение процедур и фото результата «до/после»</h3>
              <p>Мастер выполняет вычес, гигиенический уход, купание и породную стрижку. В завершение делает фото питомца для карточки и нажимает кнопку «Готово».</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--order" aria-label="Итоги ухода">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Уход завершен</span>
                <span class="mt-journey-proof-badge">Готово к выдаче</span>
              </div>
              <div class="mt-journey-proof-row"><span>Процедуры</span><strong>Стрижка по породе, чистка ушей</strong></div>
              <div class="mt-journey-proof-row"><span>Время работы</span><strong>1 час 45 минут</strong></div>
              <div class="mt-journey-proof-row"><span>Фотоотчет</span><strong>2 фото сохранены в CRM</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">04</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Система & Владелец</span>
              <h3>Кнопка «Готово!», оплата и расчет мастера</h3>
              <p>Хозяйка мгновенно получает сообщение в мессенджере: «Марси готова!». Администратор принимает оплату по карте или СБП, грумер видит начисленный %, а бот ставит напоминание на визит через месяц.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--analytics" aria-label="Расчет визита">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Расчет визита</span>
                <span class="mt-journey-proof-badge">Оплачено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Сумма</span><strong>3 800 ₽ (карта / СБП)</strong></div>
              <div class="mt-journey-proof-row"><span>Зарплата грумера</span><strong>1 710 ₽ (45% начислено)</strong></div>
              <div class="mt-journey-proof-row"><span>Мессенджер</span><strong>«Марси готова!» отправлено</strong></div>
            </div>
          </article>
        </div>
      </section>

      <!-- CASE STUDY -->
      <section class="mt-section mt-case" data-screen-label="Кейс груминга" data-mt-reveal>
        <div class="mt-case-card">
          <div class="mt-case-head">
            <span class="mt-eyebrow">Реальный кейс внедрения</span>
            <h2 class="mt-section-title">Как салон «Лапки & Хвостики» устранил накладки в расписании и увеличил повторные визиты на 35%</h2>
            <p class="mt-section-sub">Сеть студий груминга «Лапки & Хвостики» (3 филиала, 12 рабочих столов) внедрила Молнию для управления записью, учета пород и расчета зарплат мастеров.</p>
          </div>

          <div class="mt-case-stats">
            <div class="mt-case-stat">
              <strong>0 накладок</strong>
              <span>авторасчет тайминга по породе и весу питомца</span>
            </div>
            <div class="mt-case-stat">
              <strong>+35% визитов</strong>
              <span>автонапоминания в мессенджер через 4–6 недель</span>
            </div>
            <div class="mt-case-stat">
              <strong>2 минуты</strong>
              <span>вместо 4 часов на еженедельный расчет зарплат мастеров</span>
            </div>
          </div>

          <blockquote class="mt-case-quote">
            <p>«Раньше администраторы постоянно ошибались с длительностью записи: ставили хаски и шпица на одно и то же время, из-за чего мастера задерживались и нервничали. В Молнии система точно знает время под каждую породу, а кнопка "Питомец готов" с автосообщением в мессенджере избавила наш холл от толпы ожидающих хозяев».</p>
            <cite>Анастасия Белова · Основательница сети «Лапки & Хвостики»</cite>
          </blockquote>
        </div>
      </section>

      <!-- PETS FAQ -->
      <section id="faq" class="mt-section mt-reveal" data-screen-label="Вопросы и ответы" data-mt-reveal>
        <div class="mt-section-head">
          <h2 class="mt-section-title">Вопросы о программе для груминг-салонов</h2>
        </div>
        <div class="mt-before-start-grid">
          <article class="mt-before-start-highlight">
            <h3>Попробуйте Молнию для своего груминг-салона</h3>
            <p>Бесплатно поможем настроить расписание столов и ванн, прайс-лист по породам, зарплаты мастеров и перенести базу хвостатых клиентов.</p>
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в мессенджер ↗</a>
          </article>
          <div class="mt-before-start-questions">
{faq_html}
          </div>
        </div>
        <p class="mt-before-start-privacy">Как мы обрабатываем данные — в <a href="/privacy">политике конфиденциальности</a>.</p>
      </section>

      <!-- LEAD FORM -->
{lead_html}

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
'''
    return page_html


def build_repair_page() -> str:
    """Builds the complete repair and service center landing page matching the exact design system."""
    nav_html = render_nav_html(active_item="repair", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")
    lead_html = render_lead_form_html(
        "repair",
        'Получите <span class="mt-hero-accent">бесплатный доступ навсегда</span> для сервисного центра',
        "Оставьте контакты — поможем настроить учет заказов, склад запчастей, рабочие места инженеров и онлайн-запись.",
    )

    title = "CRM для сервисного центра: учет ремонтов и заказов | Молния"
    description = (
        "Программа и CRM для сервисного центра: учет заказ-нарядов, склад запчастей, статусы ремонта, "
        "печать квитанций, Уведомления в мессенджер клиентам и расчет зарплат инженеров."
    )
    canonical = "https://molniya-tech.ru/repair"

    faqs = [
        (
            "Подходит ли Молния для сервисных центров электроники, бытовой техники и мастерских?",
            "Да. Молния универсально настраивается под любой профиль: ремонт смартфонов и ноутбуков, бытовой техники, инструмента, часов, а также ателье и ремонт одежды. Для каждого направления можно задать свои типы устройств, этапы диагностики и технологические операции.",
        ),
        (
            "Как устроен учет заказ-нарядов и печать квитанций клиентам?",
            "При приеме устройства в ремонт администратор оформляет заказ-наряд за 1 минуту: фиксирует модель, серийный номер/IMEI, комплектность, внешние дефекты и причину обращения. Система автоматически печатает квитанцию с QR-кодом для клиента и маркировку на само устройство.",
        ),
        (
            "Как работает склад запчастей и списание деталей в заказ?",
            "Молния ведет учет остатков запчастей, расходников и аксессуаров. При проведении ремонта инженер прикрепляет нужную деталь к заказ-наряду — деталь списывается со склада автоматически, а ее себестоимость учитывается при расчете маржинальности заказа.",
        ),
        (
            "Как клиенты узнают о завершении диагностики и готовности устройства?",
            "Сервисный бот в мессенджере отправляет автоматические уведомления: «Устройство принято в диагностику», «Согласование стоимости» и «Ваш заказ готов, можно забирать!». Клиенту больше не нужно звонить в сервис, а администратор экономит до 3 часов в день на звонках.",
        ),
        (
            "Как рассчитывается сдельная зарплата мастеров и инженеров по ремонту?",
            "Молния автоматически считает зарплату мастеров: процент от стоимости выполненных работ (за вычетом себестоимости запчастей), фиксированную ставку за смену или надбавки за сложную пайку/BGA. Начисления прозрачно видны инженеру и руководителю сразу после закрытия заказ-наряда.",
        ),
        (
            "Можно ли контролировать гарантийные сроки и повторные обращения?",
            "Да. В карточке заказа сохраняется гарантийный срок на работы и установленные запчасти. При повторном обращении клиента система по номеру телефона, серийному номеру или IMEI мгновенно находит предыдущий заказ и показывает, действует ли гарантия.",
        ),
        (
            "Как бесплатно перенести базу клиентов, остатки склада и каталог услуг из Excel или другой CRM?",
            "Служба заботы Молнии бесплатно помогает перенести базу клиентов, прайс-лист работ, номенклатуру запчастей и остатки склада из Excel, Google Таблиц, RemOnline или другой системы за 1 день без остановки работы сервиса.",
        ),
    ]

    faq_html = "\n".join(
        f'            <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
        for q, a in faqs
    )

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://molniya-tech.ru/"},
                {"@type": "ListItem", "position": 2, "name": "Ремонт и сервис", "item": canonical},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Молния Тех — CRM для сервисного центра и ремонта",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web, iOS, Android, macOS, Windows",
            "url": canonical,
            "description": description,
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "RUB",
                "description": "Бесплатный демо-доступ и настройка учета ремонтов",
            },
            "publisher": {
                "@type": "Organization",
                "name": "ООО «МОЛНИЯ ТЕХ»",
                "url": "https://molniya-tech.ru",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a,
                    },
                }
                for q, a in faqs
            ],
        },
    ]
    json_ld_str = json.dumps(json_ld, ensure_ascii=False)

    page_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#FAF7F2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#12100E" media="(prefers-color-scheme: dark)">
  <link rel="canonical" href="{canonical}">

  <!-- Favicons -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- HERO -->
      <section class="mt-hero" data-screen-label="Герой" data-mt-hero-scene>

        <div class="mt-hero-lead">
          <h1 class="mt-hero-title">
            CRM для сервисного центра:<br><span class="mt-hero-accent">учет ремонтов и склад</span>
          </h1>

          <div class="mt-hero-bottom">
            <div class="mt-hero-intro">
              <p class="mt-hero-sub">Учет заказ-нарядов от приемки до выдачи, склад запчастей, рабочие места инженеров, уведомления клиентов в мессенджер и прозрачный расчет сдельной зарплаты мастеров.</p>
              <a class="mt-btn mt-btn-hero" href="#contact">Получить бесплатный доступ</a>
            </div>

            <ul class="mt-facets mt-facets--full" aria-label="Преимущества для сервисного центра">
              <li class="mt-facet">
                <span class="mt-facet-name">Заказ-наряды</span>
                <span class="mt-facet-note">приемка за 1 мин с печатью квитанции и QR-кодом</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Склад запчастей</span>
                <span class="mt-facet-note">автосписание деталей и контроль себестоимости</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Зарплата инженеров</span>
                <span class="mt-facet-note">сдельный расчет % от работ без рутины в Excel</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name mt-facet-name--soon">Мессенджеры & Статусы</span>
                <span class="mt-facet-note">автосообщения клиенту «Устройство готово!»</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <div class="mt-tablet">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для сервисного центра: учет заказ-нарядов и расписание инженеров" width="1710" height="983" fetchpriority="high">
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </div>
            <p class="mt-hero-media-caption">Электронный журнал заказов и статус рабочих мест инженеров в реальном времени</p>
          </div>
        </div>

      </section>

      <!-- LIVE STATIONS STATUS -->
      <section class="mt-section mt-reveal" data-screen-label="Загрузка столов и инженеров" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Все рабочие места инженеров и техника <span class="mt-overview-hook">под полным контролем</span></h2>
          <p class="mt-section-sub">Администратор и руководитель видят статус каждого устройства, назначенного инженера, этап ремонта и сумму сметы в реальном времени на любом устройстве.</p>
        </div>

        <div class="mt-auto-bays">
          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Стол 1 · Модульный ремонт</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В работе</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">iPhone 14 Pro · Артем С.</div>
                <div class="mt-auto-car-tier">Инженер: Александр П. · Замена дисплея + проклейка</div>
              </div>
              <span class="mt-dropdown-footer-icon">📱</span>
            </div>
            <div class="mt-auto-service">
              <span>Замена дисплейного модуля</span>
              <span class="mt-auto-price">7 800 ₽ (в работе)</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Стол 2 · Пайка и BGA</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В работе</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">MacBook Pro 14 M1 · Екатерина М.</div>
                <div class="mt-auto-car-tier">Инженер: Сергей К. · Цепь питания Type-C (нет заряда)</div>
              </div>
              <span class="mt-dropdown-footer-icon">💻</span>
            </div>
            <div class="mt-auto-service">
              <span>Компонентный ремонт платы</span>
              <span class="mt-auto-price">14 500 ₽ (в работе)</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Зона диагностики</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--wait">Ожидание</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Roborock S7 · Денис В. (14:30)</div>
                <div class="mt-auto-car-tier">Инженер: Михаил Т. · Ошибка лидара, не строит карту</div>
              </div>
              <span class="mt-dropdown-footer-icon">⚙️</span>
            </div>
            <div class="mt-auto-service">
              <span>Диагностика датчиков</span>
              <span class="mt-auto-price">1 200 ₽ (согласование)</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Зона выдачи заказов</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--done">Готово</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">PlayStation 5 · Роман К. (16:00)</div>
                <div class="mt-auto-car-tier">Администратор: Ольга · Чистка + замена жидкого металла</div>
              </div>
              <span class="mt-dropdown-footer-icon">🎮</span>
            </div>
            <div class="mt-auto-service">
              <span>Комплексная профилактика</span>
              <span class="mt-auto-price">4 500 ₽ (готов к выдаче)</span>
            </div>
          </div>
        </div>
      </section>

      <!-- REPAIR OVERVIEW VALUE GRID -->
      <section class="mt-section mt-section--overview mt-reveal" data-screen-label="Функции для сервисного центра" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Ведите прозрачный учет ремонтов <span class="mt-overview-hook">от приемки до закрытия гарантии</span></h2>
          <p class="mt-section-sub">Программа для учета в сервисном центре: заказ-наряды, склад деталей, зарплаты инженеров, онлайн-запись и оповещения клиентов в мессенджере.</p>
        </div>

        <div class="mt-overview-grid">
          <article class="mt-overview-card">
            <h3>Заказ-наряды и статусы <span class="mt-overview-hook">от приемки до выдачи</span></h3>
            <p>Прозрачная цепочка этапов: Принят → Диагностика → Согласование → В работе → Готов → Выдан. Печать квитанций с QR-кодом для клиента и наклеек со штрихкодом на само устройство за 1 минуту.</p>
            <div class="mt-overview-preview mt-overview-preview--schedule" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Заказ-наряд #2841</span><span>iPhone 14 Pro</span></div>
              <div class="mt-overview-calendar"><span>Прием</span><div></div><span>14:00</span><div class="mt-overview-slot">Диагностика <small>Инженер Александр П.</small></div><span>16:30</span><div class="mt-overview-slot mt-overview-slot--light">Готов к выдаче <small>Счет 7 800 ₽</small></div></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Склад запчастей: <span class="mt-overview-hook">автосписание под заказ</span></h3>
            <p>Партионный учет запчастей, контроль остатков дисплеев, аккумуляторов и расходников. Детали списываются прямо в заказ-наряд при выполнении ремонта с расчетом точной себестоимости.</p>
            <div class="mt-overview-preview mt-overview-preview--prices" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Складской остаток</span><span>Дисплеи Apple</span></div>
              <div class="mt-overview-price-row"><span>Дисплей iPhone 14 Pro (Orig)</span><strong>3 шт на складе</strong></div>
              <div class="mt-overview-price-row"><span>Проклейка корпуса водостойкая</span><strong>18 шт · В норме</strong></div>
              <div class="mt-overview-price-tag">Автосписание при закрытии наряда</div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Онлайн-запись и <span class="mt-overview-hook">проверка статуса заказа</span></h3>
            <p>Клиенты бронируют удобное время для визита прямо с сайта и карт. А по номеру квитанции или QR-коду могут в любой момент проверить статус готовности устройства онлайн без звонков в сервис.</p>
            <div class="mt-overview-preview mt-overview-preview--process" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Статус ремонта</span><span>Заказ #2841</span></div>
              <div class="mt-overview-stages"><span>Принят</span><i></i><span>В работе</span><i></i><span>Готов</span></div>
              <div class="mt-overview-check">✓ <span>Устройство: Apple iPhone 14 Pro (Замена экрана)</span></div>
              <div class="mt-overview-check">✓ <span>Статус: Готов к выдаче · Гарантия 90 дней</span></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Уведомления в мессенджер: <span class="mt-overview-hook">«Ваш заказ готов!»</span></h3>
            <p>Сервисный бот в мессенджере бесплатно уведомляет клиента о результатах диагностики, согласовывает смету ремонта и сообщает о готовности к выдаче. Экономия до 3 часов в день на звонках администратора.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Уведомление в мессенджер</span><span>Сервис «ТехноФикс»</span></div>
              <div class="mt-overview-message">
                Артем, добрый день! Ремонт iPhone 14 Pro завершен, устройство протестировано. Ждем вас на выдаче с 10:00 до 20:00!
                <span class="mt-overview-reaction">⚡</span>
              </div>
              <div class="mt-overview-client-row"><span>Экономия на звонках</span><strong>до 70% входящих вопросов о статусе →</strong></div>
            </div>
          </article>

          <article class="mt-overview-card mt-overview-card--featured">
            <h3>Сдельная зарплата инженеров <span class="mt-overview-hook">и маржинальность</span></h3>
            <p>Автоматический расчет зарплаты мастеров: процент от стоимости работы за вычетом себестоимости деталей, оклады, надбавки за сложную BGA-пайку. Руководитель видит чистую прибыль с каждого ремонта.</p>
            <div class="mt-overview-preview mt-overview-preview--metrics" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Выработка инженера</span><span>Сергей К. (Пайка)</span></div>
              <div class="mt-overview-metrics"><span>Заказы<b>18</b></span><span>Работы<b>84 000 ₽</b></span><span>Зарплата<b>₽</b></span></div>
              <div class="mt-overview-chart"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            </div>
          </article>
        </div>

        <div class="mt-overview-action">
          <a class="mt-btn mt-btn-cta" href="#contact">Получить бесплатный доступ</a>
        </div>
      </section>

      <!-- REPAIR JOURNEY -->
      <section class="mt-section mt-journey" data-screen-label="Путь заказа в ремонте">
        <div class="mt-section-head mt-section-head--center" data-mt-reveal>
          <h2 class="mt-section-title">Один заказ на ремонт. <span class="mt-hero-accent">Полный контроль каждого этапа.</span></h2>
          <p class="mt-section-sub">Посмотрите, как Молния автоматизирует путь от приемки разбитого устройства до согласования сметы, списания детали со склада, выдачи клиенту и начисления зарплаты инженеру.</p>
        </div>

        <div class="mt-journey-example" aria-label="Пример прохождения заказа в сервисном центре" data-mt-reveal data-mt-delay="80">
          <span>Пример</span><strong>Замена дисплея iPhone 15 Pro</strong><span>Apple iPhone 15 Pro (IMEI 3548...)</span>
        </div>

        <div class="mt-journey-list">
          <article class="mt-journey-step">
            <div class="mt-journey-index">01</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Клиент & Приемщик</span>
              <h3>Оформление заказ-наряда и квитанция с QR-кодом</h3>
              <p>Администратор принимает устройство, отмечает пароль разблокировки, сколы на корпусе и причину обращения. Клиент получает квитанцию с QR-кодом, а на телефон наклеивается штрихкод.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--booking" aria-label="Пример оформления заказ-наряда">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Заказ-наряд #3105</span>
                <span class="mt-journey-proof-badge">Принят</span>
              </div>
              <div class="mt-journey-proof-row"><span>Устройство</span><strong>iPhone 15 Pro (Титановый)</strong></div>
              <div class="mt-journey-proof-row"><span>Неисправность</span><strong>Разбит дисплей, нет изо</strong></div>
              <div class="mt-journey-proof-row"><span>Комплект</span><strong>Устройство, без кабеля</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">02</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Инженер</span>
              <h3>Диагностика и согласование сметы в мессенджере</h3>
              <p>Мастер проводит первичный осмотр, проверяет Face ID и системную плату, формирует смету в программе. Клиент мгновенно получает смету в мессенджер и подтверждает ремонт в один клик.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--process" aria-label="Диагностика и согласование">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Диагностика #3105</span>
                <span class="mt-journey-proof-badge">Согласовано</span>
              </div>
              <div class="mt-journey-proof-row"><span>Инженер</span><strong>Александр П. (Стол 1)</strong></div>
              <div class="mt-journey-proof-row"><span>Результат</span><strong>Плата цела, требуется экран</strong></div>
              <div class="mt-journey-proof-row"><span>Смета</span><strong>11 500 ₽ (деталь + работа)</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">03</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Мастер & Склад</span>
              <h3>Модульный ремонт и списание детали со склада</h3>
              <p>Инженер устанавливает новый дисплейный модуль, переносит True Tone и восстанавливает влагозащитную проклейку. Деталь автоматически списывается с остатков склада сервиса.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--order" aria-label="Выполнение ремонта">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Ремонт завершен</span>
                <span class="mt-journey-proof-badge">Тестирование</span>
              </div>
              <div class="mt-journey-proof-row"><span>Запчасть</span><strong>Дисплей 15 Pro (Оригинал)</strong></div>
              <div class="mt-journey-proof-row"><span>Расходники</span><strong>Водостойкая проклейка 3M</strong></div>
              <div class="mt-journey-proof-row"><span>Тесты</span><strong>Тачскрин, 120 Гц, Face ID — ОК</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">04</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Система & Выдача</span>
              <h3>Кнопка «Готово!», оплата, гарантия и зарплата мастера</h3>
              <p>Клиент получает сообщение в мессенджере: «Ваш iPhone готов!». При выдаче печатается гарантийный талон на 90 дней, клиент оплачивает заказ, а мастеру начисляется процент за выполненную работу.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--analytics" aria-label="Выдача и расчет">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Выдача заказа</span>
                <span class="mt-journey-proof-badge">Оплачено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Оплата</span><strong>11 500 ₽ (терминал / СБП)</strong></div>
              <div class="mt-journey-proof-row"><span>Зарплата мастера</span><strong>2 400 ₽ (начислено)</strong></div>
              <div class="mt-journey-proof-row"><span>Гарантия</span><strong>Акт выдан на 90 дней</strong></div>
            </div>
          </article>
        </div>
      </section>

      <!-- CASE STUDY -->
      <section class="mt-section mt-case" data-screen-label="Кейс сервисного центра" data-mt-reveal>
        <div class="mt-case-card">
          <div class="mt-case-head">
            <span class="mt-eyebrow">Реальный кейс внедрения</span>
            <h2 class="mt-section-title">Как сервисный центр «FixLab» избавился от потери деталей и сократил звонки о статусе ремонта на 70%</h2>
            <p class="mt-section-sub">Сеть сервисных центров по ремонту цифровой и бытовой техники «FixLab» (3 филиала, 11 инженеров) перешла на Молнию для наведения порядка в складе и заказ-нарядах.</p>
          </div>

          <div class="mt-case-stats">
            <div class="mt-case-stat">
              <strong>0 потерь</strong>
              <span>запчастей благодаря точному учету списаний в заказ</span>
            </div>
            <div class="mt-case-stat">
              <strong>-70% звонков</strong>
              <span>«что с моим заказом» благодаря уведомлениям в мессенджере</span>
            </div>
            <div class="mt-case-stat">
              <strong>15 минут</strong>
              <span>на еженедельный расчет зарплаты инженеров вместо 6 часов</span>
            </div>
          </div>

          <blockquote class="mt-case-quote">
            <p>«Раньше запчасти списывались кое-как в блокнотах, к концу месяца недостачи достигали десятков тысяч рублей. Плюс администраторы целыми днями висели на телефоне, отвечая клиентам о готовности. В Молнии каждый винтик привязан к заказу, а бот в мессенджере сам сообщает клиентам о готовности. Управляющий теперь видит реальную чистую прибыль по каждому мастеру за секунды».</p>
            <cite>Артем Смирнов · Совладелец сети «FixLab», Екатеринбург</cite>
          </blockquote>
        </div>
      </section>

      <!-- REPAIR FAQ -->
      <section id="faq" class="mt-section mt-reveal" data-screen-label="Вопросы и ответы" data-mt-reveal>
        <div class="mt-section-head">
          <h2 class="mt-section-title">Вопросы о программе для сервисных центров и мастерских</h2>
        </div>
        <div class="mt-before-start-grid">
          <article class="mt-before-start-highlight">
            <h3>Попробуйте Молнию для своего сервисного центра</h3>
            <p>Бесплатно поможем настроить журнал заказов, статусы ремонта, печать квитанций и перенести базу постоянных клиентов.</p>
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в мессенджер ↗</a>
          </article>
          <div class="mt-before-start-questions">
{faq_html}
          </div>
        </div>
        <p class="mt-before-start-privacy">Как мы обрабатываем данные — в <a href="/privacy">политике конфиденциальности</a>.</p>
      </section>

      <!-- LEAD FORM -->
{lead_html}

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
'''
    return page_html


def build_pricing_page() -> str:
    """Builds the dedicated product pricing page: /pricing."""
    nav_html = render_nav_html(active_item="pricing", asset_prefix="", beta_cta=True)
    footer_html = render_footer_html(asset_prefix="", pricing_variant=True)

    title = "Тарифы CRM Молния — 3 000 ₽/мес | Честные цены без переплат за мастеров"
    description = "Прозрачные тарифы CRM Молния для сферы услуг. Базовый тариф 3 000 ₽/мес включает журнал визитов, онлайн-запись, базу клиентов и лояльность без доплат за сотрудников (до 1000 мастеров). Подключаемые блоки: ЗП, склад, аналитика, ИИ, CRM, касса."
    canonical = "https://molniya-tech.ru/pricing"

    faq_items = [
        {
            "q": "Сколько стоит основной тариф и что в него входит?",
            "a": "Стоимость основного тарифа — 3 000 ₽ в месяц. В него входит полный ключевой контур для ежедневной работы: электронный журнал визитов, круглосуточная онлайн-запись 24/7, единая база клиентов с историей посещений, программа лояльности (бонусы, скидки), защита базы от выгрузки и сервисные уведомления клиентам в мессенджере за 0 ₽."
        },
        {
            "q": "Правда ли, что нет доплаты за сотрудников?",
            "a": "Да, абсолютно! В Молнии нет искусственных комиссий или доплат за каждого добавленного сотрудника. Даже на базовом тарифе вы можете подключить хоть до 1 000 сотрудников и мастеров — стоимость подписки от этого не увеличивается."
        },
        {
            "q": "Как работают подключаемые блоки (ЗП, склад, аналитика, ИИ, CRM, касса)?",
            "a": "Молния построена по модульной архитектуре: вы платите только за то, что реально используете. Если вам нужен автоматический расчет сдельной зарплаты мастеров, складской учет с автосписанием по техкартам, управленческая аналитика, ИИ-ассистент, CRM-автоворонки или интеграция с онлайн-кассой 54-ФЗ — нужный блок активируется в один клик."
        },
        {
            "q": "Есть ли бесплатный пробный период?",
            "a": "Да, каждому новому клиенту доступно 14 дней полноценного бесплатного доступа без привязки банковской карты. Наша служба заботы бесплатно поможет настроить расписание и перенести вашу базу."
        },
        {
            "q": "Сколько стоят уведомления клиентам и как работает бот в мессенджере?",
            "a": "Все подтверждения записей, напоминания за 24 и 2 часа до визита, ссылки на перенос и отмену, а также электронные чеки отправляются через фирменного бота в мессенджере абсолютно бесплатно (0 ₽). Вы можете полностью отказаться от платных SMS и экономить десятки тысяч рублей в месяц."
        },
        {
            "q": "Как происходит перенос данных при переходе с YCLIENTS или DIKIDI?",
            "a": "Наша служба заботы бесплатно поможет с переездом из другой системы: перенесет базу клиентов, историю визитов, прайс-лист и сотрудников за 15–20 минут без остановки рабочих процессов. Кроме того, при переходе мы дарим 3 месяца работы в подарок!"
        },
        {
            "q": "Соответствует ли Молния закону о персональных данных № 152-ФЗ?",
            "a": "Да, на 100%. Сервера и базы данных физически размещены на территории Российской Федерации (ООО «ТАЙМВЭБ.КЛАУД»), передача данных защищена TLS-шифрованием, а безопасность персональных данных подтверждена нормативной документацией."
        }
    ]

    faq_html = "\n".join(
        f'            <details><summary>{html.escape(item["q"])}</summary><p>{html.escape(item["a"])}</p></details>'
        for item in faq_items
    )

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "CRM Молния — Тарифы",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web, iOS, Android, macOS, Windows",
            "description": description,
            "url": canonical,
            "offers": [
                {
                    "@type": "Offer",
                    "name": "Основной тариф",
                    "price": "3000",
                    "priceCurrency": "RUB",
                    "description": "Хоть до 1 000 сотрудников без доплат, онлайн-запись 24/7, журнал визитов, клиентская база, программа лояльности, сервисные уведомления в мессенджере за 0 ₽"
                },
                {
                    "@type": "Offer",
                    "name": "Подключаемые блоки",
                    "description": "Зарплата (ЗП), складской учет, аналитика и отчеты, ИИ-ассистент, CRM и автоворонки, касса 54-ФЗ"
                }
            ]
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Главная",
                    "item": "https://molniya-tech.ru/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Тарифы",
                    "item": canonical
                }
            ]
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item["q"],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": item["a"]
                    }
                }
                for item in faq_items
            ]
        }
    ]

    json_ld_str = json.dumps(json_ld, ensure_ascii=False).replace("<", "\\u003c")

    check_icon = '<svg class="mt-pricing-feature-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>'
    table_check = '<span class="mt-compare-check"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg> Включено</span>'
    table_dash = '<span style="color:var(--mt-text-muted)">—</span>'

    page_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(description)}">
  <meta name="keywords" content="тарифы crm молния, стоимость молния тех, цена crm для салона, сколько стоит онлайн запись, альтернатива yclients тарифы, dikidi цены, crm без доплат за мастеров">
  <link rel="canonical" href="{canonical}">

  <!-- Favicon -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- HERO -->
      <section class="mt-hero mt-hero--pricing" data-screen-label="Тарифы">

        <div class="mt-hero-lead mt-hero-lead--pricing">
          <h1 class="mt-hero-title mt-hero-title--center">Тарифы Молнии</h1>
        </div>

      </section>

      <!-- PRICING CORE PLAN -->
      <section id="plans" class="mt-section mt-reveal" data-screen-label="Основной тариф" data-mt-reveal style="padding-top:0">
        <div class="mt-section-head mt-section-head--center">
          <p class="mt-section-sub">Прозрачные условия без звездочек и неожиданных списаний. Тестовый период 14 дней полного доступа включен для всех новых пользователей.</p>
        </div>

        <article class="mt-pricing-core-card">
          <div class="mt-pricing-core-info">
            <div class="mt-pricing-staff-badge">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
              <span>0 ₽ за персонал · Хоть до 1 000 сотрудников без доплат</span>
            </div>
            <h2 class="mt-pricing-tier-name" style="font-size:28px">Основной тариф</h2>
            <p class="mt-pricing-tier-desc" style="min-height:auto;font-size:15px;margin-bottom:16px">Всё необходимое для ежедневной работы бизнеса в сфере услуг. Единая подписка без скрытых платежей за расширение команды.</p>

            <ul class="mt-pricing-core-features">
              <li class="mt-pricing-feature">{check_icon}<span><strong>Хоть до 1 000 сотрудников</strong> без наценок и доплат</span></li>
              <li class="mt-pricing-feature">{check_icon}<span><strong>Электронный журнал визитов</strong> и расписание мастеров</span></li>
              <li class="mt-pricing-feature">{check_icon}<span><strong>Онлайн-запись 24/7</strong> (виджет, прямая ссылка, карты)</span></li>
              <li class="mt-pricing-feature">{check_icon}<span><strong>Единая база клиентов</strong> с историей посещений</span></li>
              <li class="mt-pricing-feature">{check_icon}<span><strong>Программа лояльности</strong> (бонусы, скидки, карты)</span></li>
              <li class="mt-pricing-feature">{check_icon}<span><strong>Уведомления в мессенджере за 0 ₽</strong> (подтверждения и чеки)</span></li>
              <li class="mt-pricing-feature">{check_icon}<span><strong>Защита клиентской базы</strong> от копирования персоналом</span></li>
            </ul>
          </div>

          <div class="mt-pricing-core-action">
            <div class="mt-pricing-price-wrap">
              <span class="mt-pricing-price">3 000 ₽</span>
              <span class="mt-pricing-period">/ месяц</span>
            </div>
            <p style="font-size:13.5px;color:var(--mt-text-muted);margin:0 0 20px;line-height:1.4">14 дней полного доступа бесплатно<br>без привязки банковской карты</p>
            <a class="mt-btn mt-pricing-btn" href="#contact">Подключить бесплатно</a>
            <div style="margin-top:14px;font-size:12.5px;color:var(--mt-text-body-2);line-height:1.4">Поможем с переездом из другой системы.</div>
          </div>
        </article>

      </section>

      <!-- ADD-ON MODULES SECTION -->
      <section id="modules" class="mt-section mt-reveal" data-screen-label="Подключаемые блоки" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Подключаемые <span class="mt-hero-accent">блоки</span></h2>
          <p class="mt-section-sub">Расширяйте возможности вашей CRM по мере роста. Подключайте только те инструменты, которые действительно нужны вашему бизнесу.</p>
        </div>

        <div class="mt-modules-grid" aria-label="Подключаемые блоки">

          <!-- Module 1: Зарплата -->
          <article class="mt-module-card">
            <div class="mt-module-header">
              <div class="mt-module-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
              </div>
              <h3 class="mt-module-title">Зарплата (ЗП)</h3>
            </div>
            <p class="mt-module-desc">Автоматический расчет сдельной зарплаты, процентов от услуг и товаров, окладов и премий.</p>
            <ul class="mt-module-features">
              <li class="mt-module-feature">{check_icon}<span>Индивидуальные ставки и проценты для каждого мастера</span></li>
              <li class="mt-module-feature">{check_icon}<span>Авторасчет премий, штрафов, чаевых и KPI</span></li>
              <li class="mt-module-feature">{check_icon}<span>Детализированные расчетные ведомости в 1 клик</span></li>
            </ul>
            <a class="mt-btn mt-btn-secondary mt-module-btn" href="#contact">Подключить</a>
          </article>

          <!-- Module 2: Аналитика -->
          <article class="mt-module-card">
            <div class="mt-module-header">
              <div class="mt-module-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
              </div>
              <h3 class="mt-module-title">Аналитика</h3>
            </div>
            <p class="mt-module-desc">Глубокая финансовая и управленческая аналитика в реальном времени без ручных таблиц.</p>
            <ul class="mt-module-features">
              <li class="mt-module-feature">{check_icon}<span>Отчеты по чистой выручке, марже и среднему чеку</span></li>
              <li class="mt-module-feature">{check_icon}<span>Загрузка рабочих мест, кабинетов и выработка мастеров</span></li>
              <li class="mt-module-feature">{check_icon}<span>Когортный анализ и динамика возвращаемости клиентов</span></li>
            </ul>
            <a class="mt-btn mt-btn-secondary mt-module-btn" href="#contact">Подключить</a>
          </article>

          <!-- Module 3: Склад -->
          <article class="mt-module-card">
            <div class="mt-module-header">
              <div class="mt-module-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
              </div>
              <h3 class="mt-module-title">Склад</h3>
            </div>
            <p class="mt-module-desc">Прозрачный учет материалов и товаров для домашнего ухода с защитой от недостач.</p>
            <ul class="mt-module-features">
              <li class="mt-module-feature">{check_icon}<span>Автосписание материалов по технологическим картам визита</span></li>
              <li class="mt-module-feature">{check_icon}<span>Контроль минимальных остатков и оповещения о закупках</span></li>
              <li class="mt-module-feature">{check_icon}<span>Учет себестоимости, партий и быстрая инвентаризация</span></li>
            </ul>
            <a class="mt-btn mt-btn-secondary mt-module-btn" href="#contact">Подключить</a>
          </article>

          <!-- Module 4: ИИ -->
          <article class="mt-module-card">
            <div class="mt-module-header">
              <div class="mt-module-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
              </div>
              <h3 class="mt-module-title">ИИ (Искусственный интеллект)</h3>
            </div>
            <p class="mt-module-desc">Умный AI-ассистент для оптимизации расписания, прогнозирования нагрузки и удержания клиентов.</p>
            <ul class="mt-module-features">
              <li class="mt-module-feature">{check_icon}<span>Предиктивное прогнозирование пиковой загрузки и свободных окон</span></li>
              <li class="mt-module-feature">{check_icon}<span>AI-подсказки по выводу мастеров и специальным предложениям</span></li>
              <li class="mt-module-feature">{check_icon}<span>Автогенерация ответов на отзывы и сервисных сообщений</span></li>
            </ul>
            <a class="mt-btn mt-btn-secondary mt-module-btn" href="#contact">Подключить</a>
          </article>

          <!-- Module 5: CRM -->
          <article class="mt-module-card">
            <div class="mt-module-header">
              <div class="mt-module-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
              </div>
              <h3 class="mt-module-title">CRM и маркетинг</h3>
            </div>
            <p class="mt-module-desc">Умная сегментация базы, автоворонки повторных продаж и возврат «уснувших» клиентов.</p>
            <ul class="mt-module-features">
              <li class="mt-module-feature">{check_icon}<span>Автоматическая RFM-сегментация (новички, постоянные, спящие)</span></li>
              <li class="mt-module-feature">{check_icon}<span>Триггерные цепочки реактивации потерянных клиентов</span></li>
              <li class="mt-module-feature">{check_icon}<span>Сквозной учет источников записей и возврат инвестиций в рекламу</span></li>
            </ul>
            <a class="mt-btn mt-btn-secondary mt-module-btn" href="#contact">Подключить</a>
          </article>

          <!-- Module 6: Касса и платежи -->
          <article class="mt-module-card">
            <div class="mt-module-header">
              <div class="mt-module-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>
              </div>
              <h3 class="mt-module-title">Касса и платежи (54-ФЗ)</h3>
            </div>
            <p class="mt-module-desc">Прием безналичных оплат, эквайринг, онлайн-чеки по 54-ФЗ и предоплата при онлайн-записи.</p>
            <ul class="mt-module-features">
              <li class="mt-module-feature">{check_icon}<span>Подключение онлайн-касс (Атол, Эвотор) и фискализация</span></li>
              <li class="mt-module-feature">{check_icon}<span>Предоплата и депозиты через СБП и карты в онлайн-записи</span></li>
              <li class="mt-module-feature">{check_icon}<span>Раздельный учет: безнал, наличные, подарочные сертификаты</span></li>
            </ul>
            <a class="mt-btn mt-btn-secondary mt-module-btn" href="#contact">Подключить</a>
          </article>

        </div>

        <!-- MIGRATION SPECIAL OFFER BANNER -->
        <div class="mt-pricing-banner">
          <div class="mt-pricing-banner-info">
            <h3>Переходите с другой CRM? Дарим 3 месяца в подарок!</h3>
            <p>Если вы уже используете YCLIENTS, DIKIDI или другую систему — бесплатно перенесём базу клиентов, историю визитов, прайс-лист и сотрудников за 15 минут и активируем 3 месяца максимального тарифа без оплаты.</p>
          </div>
          <div class="mt-pricing-banner-cta" style="display:flex;gap:12px;flex-wrap:wrap">
            <a class="mt-btn mt-btn-secondary" href="/yclients">Переход с YCLIENTS →</a>
            <a class="mt-btn mt-btn-secondary" href="/dikidi">Переход с DIKIDI →</a>
          </div>
        </div>

      </section>

      <!-- COST COMPARISON & SAVINGS CARD -->
      <section id="savings" class="mt-section mt-reveal" data-screen-label="Экономия с Молнией" data-mt-reveal>
        <div class="mt-pricing-savings-card">
          <div class="mt-section-head" style="margin-bottom:0">
            <h2 class="mt-section-title">Сколько вы экономите с Молнией каждый год?</h2>
            <p class="mt-section-sub">Сравнение реальных годовых расходов для салона на 8 мастеров с базой 1 500 активных клиентов:</p>
          </div>

          <div class="mt-pricing-savings-grid">

            <div class="mt-pricing-calc-box mt-pricing-calc-box--other">
              <h3 class="mt-pricing-calc-title">Другие CRM (YCLIENTS / DIKIDI с платными опциями)</h3>
              <div class="mt-pricing-calc-row"><span>Базовый тариф CRM в год:</span><strong>36 000 ₽</strong></div>
              <div class="mt-pricing-calc-row"><span>Доплата за мастеров (свыше 5):</span><strong>~28 800 ₽</strong></div>
              <div class="mt-pricing-calc-row"><span>SMS-напоминания (1 500 кл. × 2 SMS × 4.5 ₽):</span><strong>162 000 ₽</strong></div>
              <div class="mt-pricing-calc-row"><span>Платные модули и WhatsApp-шлюзы:</span><strong>~36 000 ₽</strong></div>
              <div class="mt-pricing-calc-total"><span>Итоговые расходы в год:</span><span style="color:#B8442E">~262 800 ₽ / год</span></div>
            </div>

            <div class="mt-pricing-calc-box mt-pricing-calc-box--molniya">
              <h3 class="mt-pricing-calc-title">CRM Молния (Основной тариф)</h3>
              <div class="mt-pricing-calc-row"><span>Основной тариф (3 000 ₽ × 12 мес):</span><strong>36 000 ₽</strong></div>
              <div class="mt-pricing-calc-row"><span>Доплата за сотрудников:</span><strong style="color:#2e7d32">0 ₽ (хоть до 1 000 сотрудников)</strong></div>
              <div class="mt-pricing-calc-row"><span>Уведомления в мессенджер клиентам:</span><strong style="color:#2e7d32">0 ₽ (неограниченно)</strong></div>
              <div class="mt-pricing-calc-row"><span>Визиты, онлайн-запись, база, лояльность:</span><strong style="color:#2e7d32">0 ₽ (включено в тариф)</strong></div>
              <div class="mt-pricing-calc-total"><span>Итоговые расходы в год:</span><span style="color:#2e7d32">36 000 ₽ / год</span></div>
            </div>

          </div>

          <div style="margin-top:28px;padding:18px 24px;background:rgba(46,125,50,.08);border-radius:var(--mt-radius-xl);text-align:center">
            <span style="font-size:18px;font-weight:800;color:#2e7d32">Ваша чистая выгода: более 220 000 ₽ в год чистой экономии без скрытых переплат!</span>
          </div>
        </div>
      </section>

      <!-- FEATURE COMPARISON TABLE -->
      <section id="features" class="mt-compare-section mt-reveal" data-screen-label="Сравнение тарифов" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Сравнение возможностей <span class="mt-hero-accent">по блокам</span></h2>
          <p class="mt-section-sub">Вся базовая функциональность включена по умолчанию. Подключайте платные блоки под конкретные задачи.</p>
        </div>

        <div class="mt-compare-wrap" aria-label="Таблица возможностей тарифа Молнии">
          <table class="mt-compare-table">
            <thead>
              <tr>
                <th style="width:40%">Возможность</th>
                <th style="width:30%;color:var(--mt-accent-strong);background:rgba(198,84,59,.08)">Основной тариф</th>
                <th style="width:30%">С подключаемыми блоками</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Стоимость в месяц</td>
                <td><strong style="color:var(--mt-accent-strong)">3 000 ₽</strong></td>
                <td><strong>3 000 ₽ + выбранные блоки</strong></td>
              </tr>
              <tr>
                <td>Количество сотрудников и мастеров</td>
                <td><span class="mt-compare-star">★ Хоть до 1 000 сотрудников</span></td>
                <td><span class="mt-compare-star">★ Хоть до 1 000 сотрудников</span></td>
              </tr>
              <tr>
                <td>Доплата за расширение команды</td>
                <td><span class="mt-compare-check">✓ 0 ₽ (без доплат)</span></td>
                <td><span class="mt-compare-check">✓ 0 ₽ (без доплат)</span></td>
              </tr>
              <tr>
                <td>Электронный журнал визитов и расписание</td>
                <td>{table_check}</td>
                <td>{table_check}</td>
              </tr>
              <tr>
                <td>Онлайн-запись 24/7 (виджет, прямая ссылка, карты)</td>
                <td>{table_check}</td>
                <td>{table_check}</td>
              </tr>
              <tr>
                <td>Единая клиентская база с историей визитов</td>
                <td>{table_check}</td>
                <td>{table_check}</td>
              </tr>
              <tr>
                <td>Программа лояльности (скидки, бонусы, баллы)</td>
                <td>{table_check}</td>
                <td>{table_check}</td>
              </tr>
              <tr>
                <td>Сервисные уведомления в мессенджере клиентам</td>
                <td><span class="mt-compare-check">✓ 0 ₽ (без лимитов)</span></td>
                <td><span class="mt-compare-check">✓ 0 ₽ (без лимитов)</span></td>
              </tr>
              <tr>
                <td>Защита базы от копирования мастерами</td>
                <td>{table_check}</td>
                <td>{table_check}</td>
              </tr>
              <tr>
                <td>Расчет зарплаты (ЗП) мастеров и ведомости</td>
                <td><span style="color:var(--mt-text-muted)">Подключаемый блок</span></td>
                <td>{table_check}</td>
              </tr>
              <tr>
                <td>Управленческая аналитика и финансовые отчеты</td>
                <td>Базовая</td>
                <td><span class="mt-compare-check">✓ Блок «Аналитика»</span></td>
              </tr>
              <tr>
                <td>Складской учет и автосписание по техкартам</td>
                <td>{table_dash}</td>
                <td><span class="mt-compare-check">✓ Блок «Склад»</span></td>
              </tr>
              <tr>
                <td>ИИ-ассистент и предиктивное расписание</td>
                <td>{table_dash}</td>
                <td><span class="mt-compare-check">✓ Блок «ИИ»</span></td>
              </tr>
              <tr>
                <td>CRM, сегментация базы и автоворонки возврата</td>
                <td>{table_dash}</td>
                <td><span class="mt-compare-check">✓ Блок «CRM»</span></td>
              </tr>
              <tr>
                <td>Касса, 54-ФЗ и безналичные платежи</td>
                <td>{table_dash}</td>
                <td><span class="mt-compare-check">✓ Блок «Касса»</span></td>
              </tr>
              <tr>
                <td>Техническая поддержка и помощь с миграцией</td>
                <td>В чате 7 дней в неделю</td>
                <td>Приоритетная линия + персональный менеджер</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- FAQ -->
      <section id="faq" class="mt-section mt-reveal" data-screen-label="Вопросы о тарифах" data-mt-reveal>
        <div class="mt-section-head">
          <h2 class="mt-section-title">Часто задаваемые вопросы о тарифах</h2>
        </div>
        <div class="mt-before-start-grid">
          <article class="mt-before-start-highlight">
            <h3>14 дней тест-драйва без привязки карты</h3>
            <p>Попробуйте полную версию Молнии в реальной работе. Наша служба заботы бесплатно перенесет базу и обучит команду.</p>
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Задать вопрос в мессенджере ↗</a>
          </article>
          <div class="mt-before-start-questions">
{faq_html}
          </div>
        </div>
        <p class="mt-before-start-privacy">Как мы обрабатываем данные — в <a href="/privacy">политике конфиденциальности</a>.</p>
      </section>

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261015-split6"></script>
</body>
</html>
'''
    return page_html


def build_dikidi_page() -> str:
    """Builds the dedicated competitor migration landing page: /dikidi."""
    nav_html = render_nav_html(active_item="dikidi", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="", dikidi_variant=True)

    title = "Переходите с DIKIDI на Молнию: 3 месяца бесплатно | Молния Тех"
    description = "Специальные условия перехода с DIKIDI Business на Молнию: 3 месяца в подарок, бесплатный перенос базы клиентов, расписания и прайса за 15 минут. Без дорогих SMS и с полной защитой базы."
    canonical = "https://molniya-tech.ru/dikidi"

    faq_items = [
        {
            "q": "Как получить 3 месяца бесплатно при переходе с DIKIDI Business?",
            "a": "Просто оставьте заявку на этой странице или напишите в нашу службу заботы. Мы бесплатно поможем перенести вашу базу клиентов, историю визитов, прайс-лист и сотрудников из DIKIDI в Молнию и сразу активируем 3 месяца бесплатной работы на максимальном тарифе без ограничений."
        },
        {
            "q": "Не потеряются ли контакты клиентов, история визитов и прайс-лист?",
            "a": "Нет, перенос происходит со 100% точностью. Вы выгружаете стандартный экспорт из DIKIDI (в Excel), а наши специалисты переносят номера телефонов, имена клиентов, историю записей, формулы, остатки на складе и перечень услуг. Ни один контакт или комментарий не пропадёт."
        },
        {
            "q": "Сколько времени занимает миграция и нужно ли останавливать приём клиентов?",
            "a": "Перенос занимает в среднем 15–20 минут. Вам не нужно закрывать салон или делать паузу в работе: пока наши специалисты импортируют базу, вы продолжаете принимать клиентов в штатном режиме, а затем сразу переходите в Молнию."
        },
        {
            "q": "Как работает онлайн-запись и сохранятся ли ссылки для клиентов?",
            "a": "Вы получаете прямую ссылку на виджет онлайн-записи и готовые кнопки для сайта, мессенджеров, группы ВКонтакте и профилей на Яндекс и 2ГИС Картах. Клиенты смогут записываться круглосуточно, выбирая услугу, мастера и время, но теперь запись ведёт строго на ваш салон — без чужих агрегаторов и рекламы конкурентов."
        },
        {
            "q": "Как отправляются напоминания клиентам и действительно ли они бесплатны?",
            "a": "Да! В Молнию встроен сервисный бот в мессенджере, который автоматически присылает подтверждения, напоминания за 24 и 2 часа до визита, а также электронные чеки. Вы не платите за пакеты SMS или WhatsApp (которые в DIKIDI обходятся в тысячи рублей каждый месяц) — расходы на сервисные уведомления равны 0 ₽."
        },
        {
            "q": "Смогут ли сотрудники и мастера пользоваться расписанием со смартфонов?",
            "a": "Да. Молния работает как быстрое веб-приложение на любом устройстве: смартфонах мастеров (iOS и Android), планшетах администратора и компьютерах. Мастера видят только своё расписание и выработку в реальном времени, а управляющий контролирует всю картину."
        },
        {
            "q": "Что произойдёт по окончании 3 месяцев бесплатного периода?",
            "a": "Никаких скрытых списаний и привязок банковских карт при старте. По истечении 3 месяцев вы сможете выбрать прозрачный тариф обслуживания без скрытых платежей за уведомления. Если решите не продолжать — вся база останется у вас с возможностью выгрузки в 1 клик."
        }
    ]

    faq_html = "\n".join(
        f'            <details><summary>{html.escape(item["q"])}</summary><p>{html.escape(item["a"])}</p></details>'
        for item in faq_items
    )

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Молния — Переход с DIKIDI Business",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web, iOS, Android",
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "RUB"
            },
            "description": description,
            "url": canonical
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Главная",
                    "item": "https://molniya-tech.ru/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Переход с DIKIDI",
                    "item": canonical
                }
            ]
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item["q"],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": item["a"]
                    }
                }
                for item in faq_items
            ]
        }
    ]

    json_ld_str = json.dumps(json_ld, ensure_ascii=False).replace("<", "\\u003c")

    page_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="{canonical}">
  <meta name="theme-color" content="#FFFEFD">

  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- HERO -->
      <section class="mt-hero" data-screen-label="Герой" data-mt-hero-scene>

        <div class="mt-hero-lead">
          <div class="mt-sector-badge">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
            Специальное предложение · Миграция с DIKIDI
          </div>

          <h1 class="mt-hero-title">
            Переходите с DIKIDI на Молнию:<br><span class="mt-hero-accent">3 месяца работы в подарок</span>
          </h1>

          <div class="mt-hero-bottom">
            <div class="mt-hero-intro">
              <p class="mt-hero-sub">Все привычные возможности DIKIDI Business — онлайн-запись, журнал, расчет зарплат и склад — в сверхбыстрой CRM. Бесплатный перенос базы за 15 минут, уведомления в мессенджер за 0 ₽ и надёжная защита от ухода клиентов к конкурентам.</p>
              <a class="mt-btn mt-btn-hero" href="#contact">Получить 3 месяца бесплатно</a>
            </div>

            <ul class="mt-facets mt-facets--full" aria-label="Преимущества перехода с DIKIDI">
              <li class="mt-facet">
                <span class="mt-facet-name">3 месяца в подарок</span>
                <span class="mt-facet-note">максимальный тариф при переходе</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Перенос за 15 минут</span>
                <span class="mt-facet-note">клиенты, история визитов и прайс</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">0 ₽ за уведомления</span>
                <span class="mt-facet-note">сервисный мессенджер вместо платных SMS</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name mt-facet-name--soon">База только ваша</span>
                <span class="mt-facet-note">прямая запись без каталогов с конкурентами</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <div class="mt-tablet">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Молния CRM: электронный журнал расписания и онлайн-запись клиентов" width="1710" height="983" fetchpriority="high">
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </div>
            <p class="mt-hero-media-caption">Электронный журнал записи и загрузка мастеров в реальном времени</p>
          </div>
        </div>

      </section>

      <!-- LIVE WORKPLACES STATUS -->
      <section class="mt-section mt-reveal" data-screen-label="Загрузка мастеров и рабочих мест" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Все мастера, рабочие места и слоты <span class="mt-overview-hook">под полным контролем</span></h2>
          <p class="mt-section-sub">Администратор и управляющий видят статус каждого рабочего места, мастера, текущую процедуру и сумму чека в реальном времени на смартфонах, планшетах и компьютерах.</p>
        </div>

        <div class="mt-auto-bays">
          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Кресло 1 · Стилист</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В работе</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Елена К. (Анна С.)</div>
                <div class="mt-auto-car-tier">Airtouch + Уход</div>
              </div>
              <span class="mt-dropdown-footer-icon">✂️</span>
            </div>
            <div class="mt-auto-service">
              <span>Сложное окрашивание</span>
              <span class="mt-auto-price">8 500 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Пост 2 · Маникюр</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В работе</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Мария Д. (Екатерина М.)</div>
                <div class="mt-auto-car-tier">Маникюр + SMART</div>
              </div>
              <span class="mt-dropdown-footer-icon">💅</span>
            </div>
            <div class="mt-auto-service">
              <span>Снятие + Покрытие</span>
              <span class="mt-auto-price">4 200 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Кресло 3 · Барбер</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--done">Готово</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Артур Б. (Дмитрий В.)</div>
                <div class="mt-auto-car-tier">Стрижка + Борода</div>
              </div>
              <span class="mt-dropdown-footer-icon">💈</span>
            </div>
            <div class="mt-auto-service">
              <span>Стрижка + Моделирование</span>
              <span class="mt-auto-price">2 800 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Пост 4 · Косметолог</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--wait">Ожидание</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Ольга Н. (15:00)</div>
                <div class="mt-auto-car-tier">Уход за лицом</div>
              </div>
              <span class="mt-dropdown-footer-icon">✨</span>
            </div>
            <div class="mt-auto-service">
              <span>Пилинг + Массаж</span>
              <span class="mt-auto-price">5 600 ₽</span>
            </div>
          </div>
        </div>
      </section>

      <!-- OVERVIEW VALUE GRID -->
      <section class="mt-section mt-section--overview mt-reveal" data-screen-label="Возможности Молнии для пользователей DIKIDI" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Все функции DIKIDI Business, <span class="mt-overview-hook">но быстрее и без скрытых расходов</span></h2>
          <p class="mt-section-sub">Онлайн-запись, расписание мастеров, учет клиентов, зарплаты и склад: переходите на платформу нового поколения с бесплатным переносом базы и 3 месяцами в подарок.</p>
        </div>

        <div class="mt-overview-grid">
          <article class="mt-overview-card">
            <h3>Уведомления в мессенджер <span class="mt-overview-hook">за 0 ₽ вместо дорогих SMS</span></h3>
            <p>В DIKIDI рассылки и напоминания требуют платных пакетов SMS (от 4–6 ₽ за сообщение), которые быстро съедают десятки тысяч рублей. В Молнии сервисный бот в мессенджере отправляет напоминания и чеки совершенно бесплатно.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Сервисный бот в мессенджере</span><span>0 ₽ / без лимитов</span></div>
              <div class="mt-overview-message">
                Анна, напоминаем о записи завтра в 14:00 к мастеру Елене. Ждём вас!
                <span class="mt-overview-reaction">👍</span>
              </div>
              <div class="mt-overview-client-row"><span>Экономия на SMS</span><strong>до 25 000 ₽ / мес →</strong></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Клиентская база <span class="mt-overview-hook">без подмешивания конкурентов</span></h3>
            <p>В мобильном каталоге DIKIDI Online ваши клиенты видят соседние салоны, акции и скидки других мастеров. В Молнии прямые ссылки и виджет принадлежат только вам: вы укрепляете свой бренд, а не чужой маркетплейс.</p>
            <div class="mt-overview-preview mt-overview-preview--process" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Прямая онлайн-запись</span><span>Ваш бренд</span></div>
              <div class="mt-overview-stages"><span>Ваш сайт</span><i></i><span>Соцсети</span><i></i><span>Карты</span></div>
              <div class="mt-overview-check">✓ <span>Клиенты не видят предложений конкурентов</span></div>
              <div class="mt-overview-check">✓ <span>Прямой переход в ваше расписание</span></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Онлайн-запись 24/7 <span class="mt-overview-hook">по прямым ссылкам и на картах</span></h3>
            <p>Клиенты бронируют слоты в 1 клик с вашего сайта, из мессенджеров, группы ВКонтакте и профилей в Яндекс и 2ГИС Картах. Программа автоматически проверяет занятость и предотвращает накладки и пустые окна.</p>
            <div class="mt-overview-preview mt-overview-preview--schedule" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Электронный журнал</span><span>Без накладок</span></div>
              <div class="mt-overview-calendar"><span>10:00</span><div></div><span>11:30</span><div class="mt-overview-slot">Кресло 1 <small>Елена · Airtouch</small></div><span>13:00</span><div class="mt-overview-slot mt-overview-slot--light">Кабинет 2 <small>Мария · SMART-уход</small></div></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Складской учёт и <span class="mt-overview-hook">автосписание по техкартам</span></h3>
            <p>Молния автоматически списывает красители, косметику и расходные материалы по нормам сразу после закрытия визита. Точный учет остатков на складе, прозрачные инвентаризации и оповещения о закупках.</p>
            <div class="mt-overview-preview mt-overview-preview--prices" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Остатки на складе</span><span>Красители и уход</span></div>
              <div class="mt-overview-price-row"><span>Краситель L'Oreal #8.1</span><strong>140 г на складе</strong></div>
              <div class="mt-overview-price-row"><span>Оксид 6% (Diactivateur)</span><strong>820 мл · В норме</strong></div>
              <div class="mt-overview-price-tag">Автосписание при закрытии чека</div>
            </div>
          </article>

          <article class="mt-overview-card mt-overview-card--featured">
            <h3>Зарплаты мастеров и <span class="mt-overview-hook">AI-аналитика выручки</span></h3>
            <p>Любые схемы мотивации: процент от чека за услугу, процент от продажи витрины, оклады, ставка за смену или аренда кресел. Мастера видят свой доход в телефоне, а ИИ прогнозирует выручку и загрузку филиалов.</p>
            <div class="mt-overview-preview mt-overview-preview--metrics" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Выработка мастера</span><span>Елена К. (Смена)</span></div>
              <div class="mt-overview-metrics"><span>Услуги<b>40%</b></span><span>Косметика<b>10%</b></span><span>Баланс<b>₽</b></span></div>
              <div class="mt-overview-chart"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            </div>
          </article>
        </div>

        <div class="mt-overview-action">
          <a class="mt-btn mt-btn-cta" href="#contact">Получить 3 месяца бесплатно</a>
        </div>
      </section>

      <!-- COMPARISON TABLE -->
      <section class="mt-compare-section mt-reveal" data-screen-label="Сравнение DIKIDI и Молнии" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Честное сравнение: <span class="mt-hero-accent">DIKIDI Business и Молния</span></h2>
          <p class="mt-section-sub">Все привычные возможности автоматизации, но на космической скорости, без скрытых платежей за уведомления и с защитой вашей клиентской базы.</p>
        </div>

        <div class="mt-compare-wrap" aria-label="Таблица сравнения DIKIDI Business и Молнии">
          <table class="mt-compare-table">
            <thead>
              <tr>
                <th>Возможность</th>
                <th>DIKIDI Business</th>
                <th>Молния Тех</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Специальное предложение</td>
                <td>Стандартные тарифы</td>
                <td><span class="mt-compare-star">★ 3 месяца бесплатно при переходе</span></td>
              </tr>
              <tr>
                <td>Онлайн-запись 24/7</td>
                <td>Есть (каталог, ссылки, виджет)</td>
                <td><span class="mt-compare-check">✓ Есть (прямые ссылки, сайт, соцсети, карты, мессенджеры)</span></td>
              </tr>
              <tr>
                <td>Уведомления и напоминания</td>
                <td><span class="mt-compare-warn">⚠ Платные SMS и WhatsApp (от 5 000 до 30 000 ₽/мес)</span></td>
                <td><span class="mt-compare-check">✓ Бесплатный бот в мессенджере (0 ₽/мес без лимитов)</span></td>
              </tr>
              <tr>
                <td>Защита клиентской базы</td>
                <td><span class="mt-compare-warn">⚠ Клиенты видят соседние салоны в DIKIDI Online</span></td>
                <td><span class="mt-compare-check">✓ 100% фокус на вашем бренде, без каталогов конкурентов</span></td>
              </tr>
              <tr>
                <td>Журнал записей и расписание</td>
                <td>Есть (стандартный календарь)</td>
                <td><span class="mt-compare-check">✓ Есть (без накладок, умное распределение постов и кресел)</span></td>
              </tr>
              <tr>
                <td>Расчет зарплат сотрудников</td>
                <td>Есть (базовые схемы)</td>
                <td><span class="mt-compare-check">✓ Есть (проценты от услуг и продаж, оклады, аренда, нормочасы)</span></td>
              </tr>
              <tr>
                <td>Склад и автосписание</td>
                <td>Есть</td>
                <td><span class="mt-compare-check">✓ Есть (автосписание по техкартам при закрытии чека)</span></td>
              </tr>
              <tr>
                <td>Скорость работы интерфейса</td>
                <td>Замедляется при росте базы</td>
                <td><span class="mt-compare-star">★ Мгновенный отклик за 0.3 сек на любом устройстве</span></td>
              </tr>
              <tr>
                <td>Перенос базы и запуск</td>
                <td>Самостоятельно по инструкциям</td>
                <td><span class="mt-compare-check">✓ Бесплатно под ключ за 15 минут нашей службой заботы</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- MIGRATION SECTION -->
      <section class="mt-migration mt-reveal" data-screen-label="Перенос базы из DIKIDI" data-mt-reveal>
        <div class="mt-migration-inner">
          <div class="mt-migration-head">
            <h2 class="mt-section-title">Переезжайте с <span class="mt-hero-accent">DIKIDI на Молнию за 15 минут</span></h2>
            <p class="mt-section-sub">Никаких остановок в записи и ручного ввода. Наша служба заботы бесплатно импортирует вашу базу, а вы получаете 3 месяца работы в подарок.</p>
          </div>

          <div class="mt-migration-layout">
            <div class="mt-migration-visual">
              <div class="mt-migration-source">
                <div class="mt-migration-window-bar">
                  <span class="mt-migration-window-dots"><i></i><i></i><i></i></span>
                  <span>DIKIDI Business / Экспорт</span>
                  <span>100% данных</span>
                </div>
                <div class="mt-migration-sheet-row"><span>Клиентская база и телефоны</span><b>✓ Готово к импорту</b></div>
                <div class="mt-migration-sheet-row"><span>История визитов и чеки</span><b>✓ Без потерь</b></div>
                <div class="mt-migration-sheet-row"><span>Сотрудники, смены и прайс</span><b>✓ Сохранено</b></div>
              </div>

              <div class="mt-migration-transfer">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14m-7-7 7 7 7-7"/></svg>
                <span>Мгновенный перенос</span>
              </div>

              <div class="mt-migration-destination">
                <div class="mt-migration-destination-head">
                  <div class="mt-migration-destination-icon">
                    <img src="/assets/img/logo/molniya-mark-mono-white-32.png" alt="Молния">
                  </div>
                  <div>
                    <strong>Молния CRM</strong>
                    <small>3 месяца бесплатного обслуживания</small>
                  </div>
                </div>
                <div class="mt-migration-settings">
                  <span>Онлайн-запись</span>
                  <span>Боты в мессенджерах 0 ₽</span>
                  <span>Расчёт зарплат</span>
                  <span>Склад и техкарты</span>
                  <span>AI-аналитика</span>
                </div>
              </div>
            </div>

            <div class="mt-migration-flow">
              <ol class="mt-migration-steps">
                <li>
                  <div class="mt-migration-number">01</div>
                  <div>
                    <h3>Выгружаете данные из DIKIDI в один клик</h3>
                    <p>В личном кабинете DIKIDI экспортируете базу клиентов, список сотрудников и прайс-лист в Excel. Это занимает ровно 2 минуты.</p>
                  </div>
                </li>
                <li>
                  <div class="mt-migration-number">02</div>
                  <div>
                    <h3>Служба заботы переносит всё за вас</h3>
                    <p>Отправляете файл нашему специалисту — мы аккуратно загрузим клиентов, историю визитов, прайс и графики мастеров за 15 минут.</p>
                  </div>
                </li>
                <li>
                  <div class="mt-migration-number">03</div>
                  <div>
                    <h3>3 месяца работы в подарок</h3>
                    <p>Вы сразу начинаете работать в сверхбыстрой Молнии без пауз в сервисе и экономите бюджет с первого дня.</p>
                  </div>
                </li>
              </ol>

              <a class="mt-btn mt-migration-cta" href="#contact">
                <span>Оставить заявку на перенос</span>
                <span class="mt-migration-switch"><span></span></span>
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- REAL-WORLD CASE STUDY -->
      <section class="mt-case-section mt-reveal" data-screen-label="Кейс миграции с DIKIDI" data-mt-reveal>
        <div class="mt-case-card">
          <div class="mt-case-header">
            <div class="mt-case-tag">⚡ Кейс миграции с DIKIDI</div>
            <h2 class="mt-case-title">Студия красоты и колористики «Mon Amie», 8 мастеров</h2>
            <blockquote class="mt-case-quote">
              «Мы три года вели запись в DIKIDI, но постоянные расходы на SMS и ощущение, что клиенты уходят к конкурентам через приложение-каталог, подтолкнули нас к смене CRM. Переход на Молнию занял меньше получаса: ребята бережно перенесли 4 500 контактов и всю историю. В первый же месяц мы сэкономили 19 000 рублей на рассылках, а мастера в восторге от скорости расписания.»
            </blockquote>
            <div class="mt-case-author">
              Алёна Григорьева <span>· Владелица студии красоты, Москва</span>
            </div>
          </div>
          <div class="mt-case-stats">
            <div class="mt-case-stat">
              <span class="mt-case-num">0 ₽</span>
              <span class="mt-case-label">За напоминания в мессенджер вместо 19 000 ₽ на SMS</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">15 <small>мин</small></span>
              <span class="mt-case-label">На полный перенос базы и запуск работы</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">+38%</span>
              <span class="mt-case-label">Рост повторных визитов за счёт ботов в мессенджерах</span>
            </div>
          </div>
        </div>
      </section>

      <!-- FAQ -->
      <section id="faq" class="mt-section mt-reveal" data-screen-label="Вопросы и ответы о переходе" data-mt-reveal>
        <div class="mt-section-head">
          <h2 class="mt-section-title">Вопросы о переходе с DIKIDI Business на Молнию</h2>
        </div>
        <div class="mt-before-start-grid">
          <article class="mt-before-start-highlight">
            <h3>3 месяца бесплатно и бережный перенос базы</h3>
            <p>Поможем выгрузить данные из DIKIDI, перенести клиентов, историю визитов, прайс и мастеров. Начните экономить на SMS уже сегодня.</p>
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в мессенджер ↗</a>
          </article>
          <div class="mt-before-start-questions">
{faq_html}
          </div>
        </div>
        <p class="mt-before-start-privacy">Как мы обрабатываем данные — в <a href="/privacy">политике конфиденциальности</a>.</p>
      </section>

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
'''
    return page_html


def build_yclients_page() -> str:
    """Builds the dedicated competitor migration landing page: /yclients."""
    nav_html = render_nav_html(active_item="yclients", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="", yclients_variant=True)

    title = "Аналог YCLIENTS: быстрый переход на Молнию — 3 месяца бесплатно | Альтернатива YCLIENTS"
    description = "Ищете современный аналог YCLIENTS? Переходите на CRM Молнию: 3 месяца работы в подарок, бесплатный перенос базы клиентов за 15 минут, уведомления в мессенджер за 0 ₽ вместо дорогих SMS."
    canonical = "https://molniya-tech.ru/yclients"

    faq_items = [
        {
            "q": "Как получить 3 месяца бесплатно при переходе с YCLIENTS?",
            "a": "Оставьте заявку на этой странице или свяжитесь с нашей службой заботы. Мы бесплатно поможем перенести вашу базу клиентов, историю визитов, прайс-лист и сотрудников из YCLIENTS в Молнию и сразу активируем 3 месяца бесплатной работы на максимальном тарифе без ограничений."
        },
        {
            "q": "Почему Молния — выгодная альтернатива YCLIENTS?",
            "a": "Молния решает главные проблемы пользователей YCLIENTS: отправка сервисных уведомлений в мессенджере за 0 ₽ вместо дорогих SMS (экономия до 35 000 ₽/мес), чистый и быстрый интерфейс без перегруженных меню (время отклика 0.2 сек) и прозрачный тариф без наценок за каждого нового мастера в штате."
        },
        {
            "q": "Не потеряются ли контакты клиентов, история визитов и прайс-лист?",
            "a": "Перенос происходит со 100% точностью. Вы выгружаете стандартный файл экспорта из YCLIENTS (раздел «Клиенты» → «Выгрузить в Excel/CSV»), а наши специалисты бережно переносят контакты, комментарии, скидки, историю записей, формулы и перечень услуг. Ни один контакт не потеряется."
        },
        {
            "q": "Сколько времени занимает миграция и нужно ли останавливать салон?",
            "a": "Перенос базы занимает в среднем 15–20 минут. Вам не нужно закрывать салон или делать паузу в работе: пока наши специалисты импортируют базу, вы продолжаете принимать гостей в штатном режиме, а затем сразу переходите в Молнию без простоев."
        },
        {
            "q": "Как работает онлайн-запись и сохранятся ли ссылки для клиентов?",
            "a": "Вы получаете прямую ссылку на стильный виджет онлайн-записи и готовые кнопки для сайта, мессенджеров, группы ВКонтакте и профилей на Яндекс и 2ГИС Картах. Клиенты бронируют удобное время в 1 клик со смартфона, выбирая услугу и любимого мастера. Интерфейс онлайн-записи прост и интуитивен."
        },
        {
            "q": "Как отправляются напоминания клиентам и действительно ли они бесплатны?",
            "a": "Да! В Молнию встроен сервисный бот в мессенджере, который автоматически присылает подтверждения, напоминания за 24 и 2 часа до визита, а также электронные чеки. Вы не платите за пакеты SMS или сторонние шлюзы WhatsApp (Wahelp, ChatApp), которые в YCLIENTS обходятся в круглую сумму."
        },
        {
            "q": "Что произойдёт по окончании 3 месяцев бесплатного периода?",
            "a": "Никаких скрытых списаний и привязок банковских карт при старте. По истечении 3 месяцев вы сможете продолжить работу по прозрачному фиксированному тарифу без скрытых доплат за мастеров и уведомления. Если решите не продолжать — вся база останется у вас с возможностью выгрузки в 1 клик."
        }
    ]

    faq_html = "\n".join(
        f'            <details><summary>{html.escape(item["q"])}</summary><p>{html.escape(item["a"])}</p></details>'
        for item in faq_items
    )

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Молния — Быстрый аналог YCLIENTS",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web, iOS, Android, macOS, Windows",
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "RUB"
            },
            "description": description,
            "url": canonical
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Главная",
                    "item": "https://molniya-tech.ru/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Аналог YCLIENTS",
                    "item": canonical
                }
            ]
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item["q"],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": item["a"]
                    }
                }
                for item in faq_items
            ]
        }
    ]

    json_ld_str = json.dumps(json_ld, ensure_ascii=False).replace("<", "\\u003c")

    page_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(description)}">
  <meta name="keywords" content="аналог yclients, альтернатива yclients, замена yclients, переход с yclients, чем заменить yclients, crm для салона красоты вместо yclients, онлайн запись аналог yclients">
  <link rel="canonical" href="{canonical}">

  <!-- Favicon -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- HERO -->
      <section class="mt-hero" data-screen-label="Герой" data-mt-hero-scene>

        <div class="mt-hero-lead">
          <div class="mt-sector-badge">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
            Специальное предложение · Миграция с YCLIENTS
          </div>

          <h1 class="mt-hero-title">
            Быстрый аналог YCLIENTS:<br><span class="mt-hero-accent">3 месяца работы в подарок</span>
          </h1>

          <div class="mt-hero-bottom">
            <div class="mt-hero-intro">
              <p class="mt-hero-sub">Все привычные возможности YCLIENTS — онлайн-запись, журнал мастеров, склад и расчет зарплат — в лёгкой и современной CRM. Бесплатный перенос базы за 15 минут, уведомления в мессенджер за 0 ₽ и честный тариф без доплат за каждого нового сотрудника.</p>
              <a class="mt-btn mt-btn-hero" href="#contact">Получить 3 месяца бесплатно</a>
            </div>

            <ul class="mt-facets mt-facets--full" aria-label="Преимущества перехода с YCLIENTS">
              <li class="mt-facet">
                <span class="mt-facet-name">3 месяца в подарок</span>
                <span class="mt-facet-note">максимальный тариф при переходе</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Перенос за 15 минут</span>
                <span class="mt-facet-note">клиенты, история визитов и прайс</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">0 ₽ за уведомления</span>
                <span class="mt-facet-note">сервисный мессенджер вместо платных SMS</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name mt-facet-name--soon">Честный тариф</span>
                <span class="mt-facet-note">без наценки за количество мастеров</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <div class="mt-tablet">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Молния CRM: электронный журнал расписания и онлайн-запись клиентов" width="1710" height="983" fetchpriority="high">
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </div>
            <p class="mt-hero-media-caption">Электронный журнал записи и загрузка мастеров в реальном времени</p>
          </div>
        </div>

      </section>

      <!-- LIVE WORKPLACES STATUS -->
      <section class="mt-section mt-reveal" data-screen-label="Загрузка мастеров и рабочих мест" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Все мастера, рабочие места и слоты <span class="mt-overview-hook">под полным контролем</span></h2>
          <p class="mt-section-sub">Администратор и управляющий видят статус каждого рабочего места, мастера, текущую процедуру и сумму чека в реальном времени на смартфонах, планшетах и компьютерах.</p>
        </div>

        <div class="mt-auto-bays">
          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Кресло 1 · Стилист</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В работе</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Елена К. (Анна С.)</div>
                <div class="mt-auto-car-tier">Airtouch + Уход</div>
              </div>
              <span class="mt-dropdown-footer-icon">✂️</span>
            </div>
            <div class="mt-auto-service">
              <span>Сложное окрашивание</span>
              <span class="mt-auto-price">8 500 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Пост 2 · Маникюр</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В работе</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Мария Д. (Екатерина М.)</div>
                <div class="mt-auto-car-tier">Маникюр + SMART</div>
              </div>
              <span class="mt-dropdown-footer-icon">💅</span>
            </div>
            <div class="mt-auto-service">
              <span>Снятие + Покрытие</span>
              <span class="mt-auto-price">4 200 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Кресло 3 · Барбер</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--done">Готово</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Артур Б. (Дмитрий В.)</div>
                <div class="mt-auto-car-tier">Стрижка + Борода</div>
              </div>
              <span class="mt-dropdown-footer-icon">💈</span>
            </div>
            <div class="mt-auto-service">
              <span>Стрижка + Моделирование</span>
              <span class="mt-auto-price">2 800 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Пост 4 · Косметолог</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--wait">Ожидание</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Ольга Н. (15:00)</div>
                <div class="mt-auto-car-tier">Уход за лицом</div>
              </div>
              <span class="mt-dropdown-footer-icon">✨</span>
            </div>
            <div class="mt-auto-service">
              <span>Пилинг + Массаж</span>
              <span class="mt-auto-price">5 600 ₽</span>
            </div>
          </div>
        </div>
      </section>

      <!-- OVERVIEW VALUE GRID -->
      <section class="mt-section mt-section--overview mt-reveal" data-screen-label="Возможности Молнии для пользователей YCLIENTS" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Все функции YCLIENTS, <span class="mt-overview-hook">но быстрее и без скрытых расходов</span></h2>
          <p class="mt-section-sub">Онлайн-запись, расписание мастеров, учет клиентов, зарплаты и склад: переходите на платформу нового поколения с бесплатным переносом базы и 3 месяцами в подарок.</p>
        </div>

        <div class="mt-overview-grid">
          <article class="mt-overview-card">
            <h3>Уведомления в мессенджер <span class="mt-overview-hook">за 0 ₽ вместо дорогих SMS</span></h3>
            <p>В YCLIENTS рассылки и напоминания требуют платных пакетов SMS (от 4–7 ₽ за сообщение) или сторонних ботов (от 3 000 до 6 000 ₽/мес). Салон на 1 500 записей тратит на SMS до 35 000 ₽ ежемесячно. В Молнии сервисный бот в мессенджере отправляет напоминания и чеки совершенно бесплатно.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Сервисный бот в мессенджере</span><span>0 ₽ / без лимитов</span></div>
              <div class="mt-overview-message">
                Анна, напоминаем о записи завтра в 14:00 к мастеру Елене. Ждём вас!
                <span class="mt-overview-reaction">👍</span>
              </div>
              <div class="mt-overview-client-row"><span>Экономия на SMS</span><strong>до 35 000 ₽ / мес →</strong></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Простой интерфейс <span class="mt-overview-hook">вместо перегруженного комбайна</span></h3>
            <p>YCLIENTS строился более 10 лет и перегружен сотнями вкладок, микрокнопок и сложных меню. Новый администратор путается и учится неделями. В Молнии интерфейс интуитивно понятен с первой минуты — команда начинает работать без долгого обучения и ошибок в расписании.</p>
            <div class="mt-overview-preview mt-overview-preview--process" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Интуитивный экран</span><span>Старт за 1 день</span></div>
              <div class="mt-overview-stages"><span>Запись</span><i></i><span>Визит</span><i></i><span>Расчёт</span></div>
              <div class="mt-overview-check">✓ <span>Без лишних окон и запутанных вкладок</span></div>
              <div class="mt-overview-check">✓ <span>Обучение администратора за 15 минут</span></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Честный тариф <span class="mt-overview-hook">без наценки за число мастеров</span></h3>
            <p>В YCLIENTS стоимость лицензии увеличивается с каждым добавленным сотрудником. В Молнии нет искусственных штрафов за расширение команды: нанимайте мастеров и расширяйте филиалы без роста абонентской платы.</p>
            <div class="mt-overview-preview mt-overview-preview--schedule" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Прозрачная подписка</span><span>Любой штат</span></div>
              <div class="mt-overview-calendar"><span>3 мастера</span><div></div><span>10 мастеров</span><div class="mt-overview-slot">Без доплат</div><span>20 мастеров</span><div class="mt-overview-slot mt-overview-slot--light">Единая цена</div></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Складской учёт и <span class="mt-overview-hook">автосписание по техкартам</span></h3>
            <p>Молния автоматически списывает красители, косметику и расходные материалы по нормам сразу после закрытия визита. Точный учет остатков на складе, прозрачные инвентаризации и оповещения о закупках.</p>
            <div class="mt-overview-preview mt-overview-preview--prices" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Остатки на складе</span><span>Красители и уход</span></div>
              <div class="mt-overview-price-row"><span>Краситель L'Oreal #8.1</span><strong>140 г на складе</strong></div>
              <div class="mt-overview-price-row"><span>Оксид 6% (Diactivateur)</span><strong>820 мл · В норме</strong></div>
              <div class="mt-overview-price-tag">Автосписание при закрытии чека</div>
            </div>
          </article>

          <article class="mt-overview-card mt-overview-card--featured">
            <h3>Зарплаты мастеров и <span class="mt-overview-hook">AI-аналитика выручки</span></h3>
            <p>Любые схемы мотивации: процент от чека за услугу, процент от продажи витрины, оклады, ставка за смену или аренда кресел. Мастера видят свой доход в телефоне, а ИИ прогнозирует выручку и загрузку филиалов.</p>
            <div class="mt-overview-preview mt-overview-preview--metrics" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Выработка мастера</span><span>Елена К. (Смена)</span></div>
              <div class="mt-overview-metrics"><span>Услуги<b>40%</b></span><span>Косметика<b>10%</b></span><span>Баланс<b>₽</b></span></div>
              <div class="mt-overview-chart"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            </div>
          </article>
        </div>

        <div class="mt-overview-action">
          <a class="mt-btn mt-btn-cta" href="#contact">Получить 3 месяца бесплатно</a>
        </div>
      </section>

      <!-- COMPARISON TABLE -->
      <section class="mt-compare-section mt-reveal" data-screen-label="Сравнение YCLIENTS и Молнии" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Честное сравнение: <span class="mt-hero-accent">YCLIENTS и Молния</span></h2>
          <p class="mt-section-sub">Все привычные возможности автоматизации, но на космической скорости, без скрытых платежей за уведомления и с защитой вашей клиентской базы.</p>
        </div>

        <div class="mt-compare-wrap" aria-label="Таблица сравнения YCLIENTS и Молнии">
          <table class="mt-compare-table">
            <thead>
              <tr>
                <th>Возможность</th>
                <th>YCLIENTS</th>
                <th>Молния Тех</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Специальное предложение</td>
                <td>Стандартные тарифы</td>
                <td><span class="mt-compare-star">★ 3 месяца бесплатно при переходе</span></td>
              </tr>
              <tr>
                <td>Тарификация сотрудников</td>
                <td><span class="mt-compare-warn">⚠ Доплата за каждого нового мастера</span></td>
                <td><span class="mt-compare-star">★ Единый честный тариф без штрафа за рост команды</span></td>
              </tr>
              <tr>
                <td>Уведомления и напоминания</td>
                <td><span class="mt-compare-warn">⚠ Платные SMS и боты (от 10 000 до 35 000 ₽/мес)</span></td>
                <td><span class="mt-compare-check">✓ Бесплатный бот в мессенджере (0 ₽/мес без лимитов)</span></td>
              </tr>
              <tr>
                <td>Простота интерфейса</td>
                <td><span class="mt-compare-warn">⚠ Перегружен функциями, долгое обучение</span></td>
                <td><span class="mt-compare-check">✓ Интуитивный экран, команда работает в 1-й же день</span></td>
              </tr>
              <tr>
                <td>Онлайн-запись 24/7</td>
                <td>Есть (виджет, интеграции)</td>
                <td><span class="mt-compare-check">✓ Есть (прямые ссылки, сайт, соцсети, карты, мессенджеры)</span></td>
              </tr>
              <tr>
                <td>Журнал записей и расписание</td>
                <td>Есть (календарь)</td>
                <td><span class="mt-compare-check">✓ Есть (без накладок, умное распределение постов и кресел)</span></td>
              </tr>
              <tr>
                <td>Расчет зарплат сотрудников</td>
                <td>Есть</td>
                <td><span class="mt-compare-check">✓ Есть (проценты от услуг и витрины, оклады, аренда, смены)</span></td>
              </tr>
              <tr>
                <td>Склад и автосписание</td>
                <td>Есть</td>
                <td><span class="mt-compare-check">✓ Есть (автосписание по техкартам при закрытии чека)</span></td>
              </tr>
              <tr>
                <td>Скорость работы интерфейса</td>
                <td>Замедляется при росте базы</td>
                <td><span class="mt-compare-star">★ Мгновенный отклик за 0.2 сек на любом устройстве</span></td>
              </tr>
              <tr>
                <td>Перенос базы и запуск</td>
                <td>Самостоятельно по инструкциям</td>
                <td><span class="mt-compare-check">✓ Бесплатно под ключ за 15 минут нашей службой заботы</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- MIGRATION SECTION -->
      <section class="mt-migration mt-reveal" data-screen-label="Перенос базы из YCLIENTS" data-mt-reveal>
        <div class="mt-migration-inner">
          <div class="mt-migration-head">
            <h2 class="mt-section-title">Переезжайте с <span class="mt-hero-accent">YCLIENTS на Молнию за 15 минут</span></h2>
            <p class="mt-section-sub">Никаких остановок в записи и ручного ввода. Наша служба заботы бесплатно импортирует вашу базу, а вы получаете 3 месяца работы в подарок.</p>
          </div>

          <div class="mt-migration-layout">
            <div class="mt-migration-visual">
              <div class="mt-migration-source">
                <div class="mt-migration-window-bar">
                  <span class="mt-migration-window-dots"><i></i><i></i><i></i></span>
                  <span>YCLIENTS / Экспорт</span>
                  <span>100% данных</span>
                </div>
                <div class="mt-migration-sheet-row"><span>Клиентская база и телефоны</span><b>✓ Готово к импорту</b></div>
                <div class="mt-migration-sheet-row"><span>История визитов и чеки</span><b>✓ Без потерь</b></div>
                <div class="mt-migration-sheet-row"><span>Сотрудники, смены и прайс</span><b>✓ Сохранено</b></div>
              </div>

              <div class="mt-migration-transfer">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14m-7-7 7 7 7-7"/></svg>
                <span>Мгновенный перенос</span>
              </div>

              <div class="mt-migration-destination">
                <div class="mt-migration-destination-head">
                  <div class="mt-migration-destination-icon">
                    <img src="/assets/img/logo/molniya-mark-mono-white-32.png" alt="Молния">
                  </div>
                  <div>
                    <strong>Молния CRM</strong>
                    <small>3 месяца бесплатного обслуживания</small>
                  </div>
                </div>
                <div class="mt-migration-settings">
                  <span>Онлайн-запись</span>
                  <span>Боты в мессенджерах 0 ₽</span>
                  <span>Расчёт зарплат</span>
                  <span>Склад и техкарты</span>
                  <span>AI-аналитика</span>
                </div>
              </div>
            </div>

            <div class="mt-migration-flow">
              <ol class="mt-migration-steps">
                <li>
                  <div class="mt-migration-number">01</div>
                  <div>
                    <h3>Выгружаете данные из YCLIENTS в два клика</h3>
                    <p>В меню YCLIENTS экспортируете базу клиентов, список сотрудников и прайс-лист в Excel/CSV. Это занимает ровно 2 минуты.</p>
                  </div>
                </li>
                <li>
                  <div class="mt-migration-number">02</div>
                  <div>
                    <h3>Служба заботы переносит всё за вас</h3>
                    <p>Отправляете файл нашему специалисту — мы аккуратно загрузим клиентов, историю визитов, прайс и графики мастеров за 15 минут.</p>
                  </div>
                </li>
                <li>
                  <div class="mt-migration-number">03</div>
                  <div>
                    <h3>3 месяца работы в подарок</h3>
                    <p>Вы сразу начинаете работать в сверхбыстрой Молнии без пауз в сервисе и экономите десятки тысяч рублей на SMS с первого дня.</p>
                  </div>
                </li>
              </ol>

              <a class="mt-btn mt-migration-cta" href="#contact">
                <span>Оставить заявку на перенос</span>
                <span class="mt-migration-switch"><span></span></span>
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- REAL-WORLD CASE STUDY -->
      <section class="mt-case-section mt-reveal" data-screen-label="Кейс миграции с YCLIENTS" data-mt-reveal>
        <div class="mt-case-card">
          <div class="mt-case-header">
            <div class="mt-case-tag">⚡ Кейс миграции с YCLIENTS</div>
            <h2 class="mt-case-title">Студия красоты и барбершоп «Artisan & Co», 12 мастеров</h2>
            <blockquote class="mt-case-quote">
              «Мы более 4 лет вели запись в YCLIENTS. Главная статья расходов была не подписка, а счета за SMS и ботов: салон отдавал по 28 000–33 000 рублей каждый месяц только за рассылку напоминаний! Плюс при добавлении новых мастеров рос тариф. Переход на Молнию занял всего 20 минут: ребята бесплатно перенесли базу на 6 200 клиентов со всей историей. В первый же месяц расходы на SMS упали до 0 рублей, а администраторы перестали путаться в календаре.»
            </blockquote>
            <div class="mt-case-author">
              Дмитрий Васильев <span>· Совладелец сети салонов, Санкт-Петербург</span>
            </div>
          </div>
          <div class="mt-case-stats">
            <div class="mt-case-stat">
              <span class="mt-case-num">0 ₽</span>
              <span class="mt-case-label">За напоминания в мессенджер вместо 31 000 ₽ на SMS</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">15 <small>мин</small></span>
              <span class="mt-case-label">На полный перенос базы и запуск работы</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">100%</span>
              <span class="mt-case-label">Сохранность клиентской базы и истории визитов</span>
            </div>
          </div>
        </div>
      </section>

      <!-- FAQ -->
      <section id="faq" class="mt-section mt-reveal" data-screen-label="Вопросы и ответы о переходе" data-mt-reveal>
        <div class="mt-section-head">
          <h2 class="mt-section-title">Вопросы о переходе с YCLIENTS на Молнию</h2>
        </div>
        <div class="mt-before-start-grid">
          <article class="mt-before-start-highlight">
            <h3>3 месяца бесплатно и бережный перенос базы</h3>
            <p>Поможем выгрузить данные из YCLIENTS, перенести клиентов, историю визитов, прайс и мастеров. Начните экономить на SMS уже сегодня.</p>
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в мессенджер ↗</a>
          </article>
          <div class="mt-before-start-questions">
{faq_html}
          </div>
        </div>
        <p class="mt-before-start-privacy">Как мы обрабатываем данные — в <a href="/privacy">политике конфиденциальности</a>.</p>
      </section>

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
'''
    return page_html




def sync_navigation_to_index():
    """Syncs the DRY nav, footer, cookie banner, and sticky CTA into index.html."""
    content = INDEX_HTML.read_text(encoding="utf-8")
    nav_html = render_nav_html(active_item="", asset_prefix="", beta_cta=True)

    start_marker = "<!-- NAV -->"
    end_marker = "</nav>"
    if start_marker in content and end_marker in content:
        before = content.split(start_marker, 1)[0].rstrip(" \t")
        after = content.split(end_marker, 1)[1]
        content = before + nav_html + after

    footer_html = render_footer_html(asset_prefix="", home_variant=True)
    f_start = "<!-- FOOTER -->"
    f_end = "</footer>"
    if f_start in content and f_end in content:
        before = content.split(f_start, 1)[0].rstrip(" \t")
        after = content.split(f_end, 1)[1]
        content = before + footer_html + after

    old_cookie_link = '<a href="/cookies" class="mt-link-accent">политике cookie</a>'
    new_cookie_link = '<a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>'
    content = content.replace(old_cookie_link, new_cookie_link)

    sticky_start = "<!-- sticky floating CTA -->"
    if sticky_start in content:
        before_s = content.split(sticky_start, 1)[0].rstrip(" \t\n")
        after_s = content.split(sticky_start, 1)[1].split("</a>", 1)[1]
        content = before_s + "\n\n" + render_sticky_cta_html().strip() + after_s

    INDEX_HTML.write_text(content, encoding="utf-8")
    print("Updated navigation, footer, and banner in index.html")


def sync_navigation_to_blog():
    """Syncs the DRY nav, footer, cookie banner, and sticky CTA into blog/index.html."""
    content = BLOG_INDEX_HTML.read_text(encoding="utf-8")
    nav_html = render_nav_html(active_item="blog", asset_prefix="../")

    start_marker = "<!-- NAV -->"
    end_marker = "</nav>"
    if start_marker in content and end_marker in content:
        before = content.split(start_marker, 1)[0].rstrip(" \t")
        after = content.split(end_marker, 1)[1]
        content = before + nav_html + after

    footer_html = render_footer_html(asset_prefix="../")
    f_start = "<!-- FOOTER -->"
    f_end = "</footer>"
    if f_start in content and f_end in content:
        before = content.split(f_start, 1)[0].rstrip(" \t")
        after = content.split(f_end, 1)[1]
        content = before + footer_html + after

    old_cookie_link = '<a href="/cookies" class="mt-link-accent">политике cookie</a>'
    new_cookie_link = '<a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>'
    content = content.replace(old_cookie_link, new_cookie_link)

    sticky_start = "<!-- sticky floating CTA -->"
    if sticky_start in content:
        before_s = content.split(sticky_start, 1)[0].rstrip(" \t\n")
        after_s = content.split(sticky_start, 1)[1].split("</a>", 1)[1]
        content = before_s + "\n\n" + render_sticky_cta_html().strip() + after_s

    BLOG_INDEX_HTML.write_text(content, encoding="utf-8")
    print("Updated navigation, footer, and banner in blog/index.html")


def sync_sitemap():
    """Ensures /auto and /requisites are in sitemap.xml."""
    content = SITEMAP_XML.read_text(encoding="utf-8")
    changed = False

    # Clean up old .html variant if present
    if "https://molniya-tech.ru/requisites.html" in content:
        content = content.replace("https://molniya-tech.ru/requisites.html", "https://molniya-tech.ru/requisites")
        changed = True

    if "https://molniya-tech.ru/auto" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/auto</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /auto to sitemap.xml")

    if "https://molniya-tech.ru/requisites" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/requisites</loc>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /requisites to sitemap.xml")

    if "https://molniya-tech.ru/beauty" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/beauty</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /beauty to sitemap.xml")

    if "https://molniya-tech.ru/health" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/health</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /health to sitemap.xml")

    if "https://molniya-tech.ru/psychologist" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/psychologist</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /psychologist to sitemap.xml")

    if "https://molniya-tech.ru/stretching" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/stretching</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /stretching to sitemap.xml")

    if "https://molniya-tech.ru/yoga" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/yoga</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /yoga to sitemap.xml")

    if "https://molniya-tech.ru/trainers" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/trainers</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /trainers to sitemap.xml")

    if "https://molniya-tech.ru/martial-arts" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/martial-arts</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /martial-arts to sitemap.xml")

    if "https://molniya-tech.ru/spaces" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/spaces</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /spaces to sitemap.xml")

    if "https://molniya-tech.ru/photostudios" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/photostudios</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /photostudios to sitemap.xml")

    if "https://molniya-tech.ru/cleaning" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/cleaning</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /cleaning to sitemap.xml")

    if "https://molniya-tech.ru/education" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/education</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /education to sitemap.xml")

    if "https://molniya-tech.ru/pets" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/pets</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /pets to sitemap.xml")

    if "https://molniya-tech.ru/repair" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/repair</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /repair to sitemap.xml")

    if "https://molniya-tech.ru/dikidi" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/dikidi</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /dikidi to sitemap.xml")

    if "https://molniya-tech.ru/yclients" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/yclients</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /yclients to sitemap.xml")

    if "https://molniya-tech.ru/pricing.html" in content:
        content = content.replace("https://molniya-tech.ru/pricing.html", "https://molniya-tech.ru/pricing")
        changed = True

    if "https://molniya-tech.ru/pricing" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/pricing</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /pricing to sitemap.xml")

    if "https://molniya-tech.ru/about.html" in content:
        content = content.replace("https://molniya-tech.ru/about.html", "https://molniya-tech.ru/about")
        changed = True

    if "https://molniya-tech.ru/about" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/about</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /about to sitemap.xml")

    # Clean up old .html variant if present
    if "https://molniya-tech.ru/privacy.html" in content:
        content = content.replace("https://molniya-tech.ru/privacy.html", "https://molniya-tech.ru/privacy")
        changed = True

    if "https://molniya-tech.ru/privacy" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/privacy</loc>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        changed = True
        print("Added /privacy to sitemap.xml")

    if changed:
        SITEMAP_XML.write_text(content, encoding="utf-8")


def build_about_page() -> str:
    """Builds the dedicated company about page: /about."""
    nav_html = render_nav_html(active_item="about", asset_prefix="", beta_cta=True)
    footer_html = render_footer_html(asset_prefix="")

    title = "О компании Молния Тех — разработчик CRM платформы для сервисного бизнеса"
    description = "«Молния Тех» создаёт операционную платформу для сферы услуг. Онлайн-запись, расписание, процессы, склад, расчет зарплат и AI-прогноз бизнеса связаны в одном приложении."
    canonical = "https://molniya-tech.ru/about"

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">
  <meta name="theme-color" content="#FFFEFD">

  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "AboutPage",
        "@id": "https://molniya-tech.ru/about#webpage",
        "url": "https://molniya-tech.ru/about",
        "name": "О компании ООО «МОЛНИЯ ТЕХ»",
        "description": "«Молния Тех» создаёт операционно-аналитическую платформу для сервисного бизнеса.",
        "isPartOf": {{
          "@id": "https://molniya-tech.ru/#website"
        }}
      }},
      {{
        "@type": "Organization",
        "@id": "https://molniya-tech.ru/#organization",
        "name": "Молния Тех",
        "legalName": "Общество с ограниченной ответственностью «МОЛНИЯ ТЕХ»",
        "url": "https://molniya-tech.ru/",
        "logo": "https://molniya-tech.ru/assets/img/logo/molniya-logo-horizontal.svg",
        "sameAs": [
          "https://t.me/molniya_tex",
          "https://www.linkedin.com/company/molniya-tech"
        ],
        "taxID": "7806637461",
        "telephone": "+7-812-724-21-24",
        "email": "info@molniya-tech.ru",
        "address": {{
          "@type": "PostalAddress",
          "streetAddress": "пр-кт Малоохтинский, д. 61, литера А, помещ. 1-Н",
          "addressLocality": "Санкт-Петербург",
          "postalCode": "195112",
          "addressCountry": "RU"
        }}
      }}
    ]
  }}
  </script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
    <linearGradient id="mtgrad2" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#B8442E"></stop><stop offset="1" stop-color="#D2634A"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <main class="mt-main" id="main-content">

        <!-- ABOUT HERO -->
        <section class="mt-section mt-hero--about mt-reveal" data-screen-label="О компании" data-mt-reveal>
          <div class="mt-about-hero-full">
            <h1 class="mt-about-hero-title">Молния Тех: наводим порядок в операциях сервисного бизнеса</h1>
            <p class="mt-about-hero-anchor">Онлайн-запись, расписание, процесс работ, склад, расчёт зарплат и AI-прогноз будущего бизнеса связаны в одном приложении.</p>
            <p class="mt-about-hero-lead">«Молния Тех» создаёт операционно-аналитическую платформу для сервисного бизнеса: автосервисов, детейлинга, салонов красоты, клиник, груминга и аренды пространств. Мы убрали перегруженные меню, зависания и скрытые доплаты за мастеров, чтобы команды управляли записью, процессами и финансами на высокой скорости и с полным контролем.</p>
          </div>
        </section>

        <!-- MISSION & PRINCIPLES -->
        <section class="mt-section mt-reveal" data-mt-reveal>
          <div class="mt-section-head">
            <h2 class="mt-section-title">Каким должен быть софт для сферы услуг</h2>
            <p class="mt-section-sub">Сервисный бизнес зарабатывает на качестве и внимании к клиентам, а не на борьбе с медленными программами.</p>
          </div>
          <div class="mt-overview-grid mt-overview-grid--split-3">
            <article class="mt-overview-card">
              <h3>Скорость отклика <span class="mt-overview-hook">0.2 секунды</span></h3>
              <p>Программа мгновенно открывается в браузере любого устройства — на смартфонах мастеров, планшетах администраторов и ноутбуках. Никаких подвисаний в часы пик.</p>
            </article>
            <article class="mt-overview-card">
              <h3>Честные тарифы <span class="mt-overview-hook">без скрытых доплат</span></h3>
              <p>Фиксированная стоимость без поборов за каждого нового мастера в штате и наценок на SMS — сервисные уведомления клиентам уходят в мессенджер бесплатно.</p>
            </article>
            <article class="mt-overview-card">
              <h3>Единая система <span class="mt-overview-hook">вместо десятка сервисов</span></h3>
              <p>Запись, этапы выполнения работ, списание материалов со склада по себестоимости и расчёт зарплат объединены без ручных таблиц и костылей.</p>
            </article>
          </div>
        </section>

        <!-- PRODUCT OVERVIEW -->
        <section class="mt-section mt-reveal" data-mt-reveal>
          <div class="mt-section-head">
            <h2 class="mt-section-title">Что умеет платформа Молния</h2>
            <p class="mt-section-sub">Все ключевые инструменты для управления записью, процессами и финансами.</p>
          </div>
          <div class="mt-overview-grid mt-overview-grid--split-6">
            <article class="mt-overview-card">
              <h3><span class="mt-overview-hook">Онлайн-запись</span> и календарь</h3>
              <p>Удобный виджет 24/7 для сайта, карт и соцсетей. Клиенты сами бронируют слоты, а расписание защищено от накладок и пустых окон.</p>
            </article>
            <article class="mt-overview-card">
              <h3>Уведомления <span class="mt-overview-hook">в мессенджер</span></h3>
              <p>Автоматические подтверждения и напоминания о визите за 24 и 2 часа без платных пакетов SMS (0 ₽ за отправку сообщений).</p>
            </article>
            <article class="mt-overview-card">
              <h3>Этапы и <span class="mt-overview-hook">чек-листы работ</span></h3>
              <p>Кастомные цепочки статусов под ваше направление: от фотофиксации при приёмке до чек-листа мастера и контроля качества при выдаче.</p>
            </article>
            <article class="mt-overview-card">
              <h3>Склад и <span class="mt-overview-hook">расходные материалы</span></h3>
              <p>Автоматическое списание запчастей и материалов со склада по себестоимости в момент закрытия заказ-наряда.</p>
            </article>
            <article class="mt-overview-card">
              <h3>Расчёт зарплат <span class="mt-overview-hook">и мотивация</span></h3>
              <p>Гибкие сдельные ставки, проценты от услуг и продаж. Прозрачные начисления рассчитываются автоматически за смену.</p>
            </article>
            <article class="mt-overview-card">
              <h3>AI-прогнозирование <span class="mt-overview-hook">и аналитика</span></h3>
              <p>Умная оценка плотности загрузки по часам, прогноз выручки и заблаговременное предупреждение о кассовых разрывах.</p>
            </article>
          </div>
        </section>

        <!-- SECTORS -->
        <section class="mt-section mt-reveal" data-mt-reveal>
          <div class="mt-section-head">
            <h2 class="mt-section-title">Решения под особенности вашего бизнеса</h2>
            <p class="mt-section-sub">Каждая отрасль получает готовую конфигурацию с нужными статусами и спецификой.</p>
          </div>
          <div class="mt-about-grid-4">
            <a class="mt-about-card" href="/auto">
              <h3><span class="mt-overview-hook">Автобизнес →</span></h3>
              <p>Детейлинг, автомойки, автосервисы и шиномонтаж: учет боксов, чек-листы кузова, склад автозапчастей и нормы времени.</p>
            </a>
            <a class="mt-about-card" href="/beauty">
              <h3><span class="mt-overview-hook">Красота →</span></h3>
              <p>Салоны красоты, барбершопы, ногтевые студии: график мастеров, карточки гостей, формулы окрашивания и списание косметики.</p>
            </a>
            <a class="mt-about-card" href="/health">
              <h3><span class="mt-overview-hook">Здоровье →</span></h3>
              <p>Клиники, стоматологии, массажные центры: электронные медкарты, протоколы приемов и учет расходных материалов.</p>
            </a>
            <a class="mt-about-card" href="/spaces">
              <h3><span class="mt-overview-hook">Аренда пространств →</span></h3>
              <p>Коворкинги, лофты, спортивные залы: интерактивная шахматка броней, учет залогов и доп. оборудования без накладок.</p>
            </a>
            <a class="mt-about-card" href="/photostudios">
              <h3><span class="mt-overview-hook">Фотостудии →</span></h3>
              <p>Интерьерные фотостудии, циклорамы, видеопавильоны: интерактивная шахматка залов, учет света, насадок и предоплат.</p>
            </a>
            <a class="mt-about-card" href="/cleaning">
              <h3><span class="mt-overview-hook">Клининг →</span></h3>
              <p>Уборка квартир, офисов, химчистка мебели: расписание выездных бригад, калькулятор метража и сдельная зарплата клинеров.</p>
            </a>
            <a class="mt-about-card" href="/education">
              <h3><span class="mt-overview-hook">Образование →</span></h3>
              <p>Курсы, студии танцев, языковые школы: расписание аудиторий, учет абонементов, посещаемость и зарплаты преподавателей.</p>
            </a>
            <a class="mt-about-card" href="/pets">
              <h3><span class="mt-overview-hook">Груминг →</span></h3>
              <p>Груминг-салоны: учет питомцев, пород, расписание столов и мастеров, автонапоминания владельцам о повторной стрижке.</p>
            </a>
            <a class="mt-about-card" href="/repair">
              <h3><span class="mt-overview-hook">Ремонт техники →</span></h3>
              <p>Сервисные центры: заказ-наряды с актами дефектовки, склад деталей, зарплаты инженеров и печать гарантийных талонов.</p>
            </a>
            <a class="mt-about-card mt-about-card--cta" href="#beta">
              <h3><span class="mt-overview-hook">Другие сферы →</span></h3>
              <p>Гибкая настройка этапов работ, статусов заказов, склада и расчета зарплат под специфику любого сервисного бизнеса.</p>
            </a>
          </div>
        </section>

        <!-- SOCIAL NETWORKS -->
        <section class="mt-section mt-reveal" data-mt-reveal>
          <div class="mt-section-head">
            <h2 class="mt-section-title">Социальные сети и сообщество</h2>
            <p class="mt-section-sub">Следите за обновлениями продукта, кейсами внедрения и развитием экосистемы Молнии на наших официальных страницах.</p>
          </div>
          <div class="mt-about-social-grid">
            <a class="mt-about-social-card" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
              <div class="mt-about-social-icon mt-about-social-icon--tg">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
              </div>
              <div class="mt-about-social-info">
                <div class="mt-about-social-header">
                  <h3>Telegram-канал</h3>
                  <span class="mt-about-social-arrow">→</span>
                </div>
                <p>Анонсы обновлений, разборы кейсов автоматизации сервисного бизнеса, инсайты от разработчиков и спецпредложения.</p>
                <span class="mt-about-social-handle">@molniya_tex</span>
              </div>
            </a>

            <a class="mt-about-social-card" href="https://www.linkedin.com/company/molniya-tech" target="_blank" rel="noopener">
              <div class="mt-about-social-icon mt-about-social-icon--in">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 8.76a1.68 1.68 0 0 0 0-3.36 1.68 1.68 0 0 0 0 3.36m1.39 9.74v-8.37H5.07v8.37z"/></svg>
              </div>
              <div class="mt-about-social-info">
                <div class="mt-about-social-header">
                  <h3>LinkedIn</h3>
                  <span class="mt-about-social-arrow">→</span>
                </div>
                <p>Официальная страница компании: новости разработки, архитектура сервиса, карьера и корпоративные B2B-партнёрства.</p>
                <span class="mt-about-social-handle">molniya-tech</span>
              </div>
            </a>
          </div>
        </section>

        <!-- LEAD CAPTURE FORM -->
        <section class="mt-section mt-lead mt-reveal" id="beta" data-mt-reveal>
          <div class="mt-lead-container">
            <div class="mt-section-head mt-section-head--center">
              <h2 class="mt-section-title">Попробуйте Молнию в деле</h2>
              <p class="mt-section-sub">14 дней бесплатного доступа. Бесплатно перенесём вашу базу из любой системы за 15 минут.</p>
            </div>
            <form class="mt-lead-form" data-lead-form data-lead-source="about">
              <div class="mt-lead-fields">
                <label class="mt-lead-field" for="about-name">Имя<input id="about-name" name="name" type="text" autocomplete="name" minlength="2" maxlength="80" placeholder="Как к вам обращаться" required></label>
                <label class="mt-lead-field" for="about-phone">Телефон<input id="about-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="32" placeholder="+7 999 123-45-67" required></label>
                <label class="mt-lead-field" for="about-email">Почта<input id="about-email" name="email" type="email" autocomplete="email" maxlength="254" placeholder="name@example.com" required></label>
              </div>
              <div class="mt-lead-honeypot" aria-hidden="true"><label for="about-website">Сайт</label><input id="about-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
              <label class="mt-lead-consent"><input name="consent" type="checkbox" required><span>Я даю своё согласие на обработку персональных данных в соответствии с <a href="/privacy" target="_blank" rel="noopener">политикой конфиденциальности</a>.</span></label>
              <button class="mt-btn mt-btn-cta mt-lead-submit" type="submit">Получить бесплатный доступ</button>
              <p class="mt-lead-status" data-lead-status role="status" aria-live="polite"></p>
            </form>
          </div>
        </section>

        <!-- LEGAL & REQUISITES -->
        <section class="mt-section mt-reveal" data-mt-reveal>
          <div class="mt-section-head mt-about-legal-head">
            <h2 class="mt-section-title">Юридическая информация</h2>
          </div>
          <div class="mt-requisites-card">
            <table class="mt-requisites-table">
              <tbody>
                <tr><td>Организация</td><td>ООО «МОЛНИЯ ТЕХ»</td></tr>
                <tr><td>ИНН / КПП</td><td>7806637461 / 780601001</td></tr>
                <tr><td>ОГРН</td><td>1267800068458</td></tr>
                <tr><td>Юридический адрес</td><td>195112, г. Санкт-Петербург, вн.тер.г. муниципальный округ Малая Охта, пр-кт Малоохтинский, д. 61, литера А, помещ. 1-Н, ком. 4-48</td></tr>
                <tr><td>Телефон</td><td><a href="tel:+78127242124" class="mt-link-accent">8 (812) 724-21-24</a></td></tr>
                <tr><td>Электронная почта</td><td><a href="mailto:info@molniya-tech.ru" class="mt-link-accent">info@molniya-tech.ru</a></td></tr>
              </tbody>
            </table>
            <div style="margin-top:1.25rem">
              <a href="/requisites" class="mt-link-accent">Все банковские и юридические реквизиты →</a>
            </div>
          </div>
        </section>

      </main>

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
"""


def build_404_page() -> str:
    """Builds the branded 404 error page matching the exact design system."""
    nav_html = render_nav_html(active_item="", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>404 — Страница не найдена — Молния Тех</title>
  <meta name="description" content="Запрошенная страница не существует или была перемещена. Перейдите на главную страницу или в базу знаний Молнии.">
  <meta name="robots" content="noindex, follow">
  <meta name="theme-color" content="#FFFEFD">

  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="404 — Страница не найдена — Молния Тех">
  <meta property="og:description" content="Запрошенная страница не найдена. Перейдите на главную страницу Молнии.">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
    <linearGradient id="mtgrad2" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#B8442E"></stop><stop offset="1" stop-color="#D2634A"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- 404 HERO -->
      <main class="mt-404-main">
        <div class="mt-404-container">
          <div class="mt-404-code-wrap">
            <span class="mt-404-code">404</span>
            <div class="mt-404-spark" aria-hidden="true">
              <svg width="44" height="44" viewBox="0 0 24 24" fill="url(#mtgrad)"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/></svg>
            </div>
          </div>
          <div class="mt-eyebrow mt-404-eyebrow">Ошибка 404 · Связь потеряна</div>
          <h1 class="mt-404-title">Страница не найдена</h1>
          <p class="mt-404-desc">
            Похоже, ссылка устарела или в адресе опечатка.
            Не переживайте: расписание, онлайн-запись и база знаний Молнии работают штатно.
          </p>

          <div class="mt-404-actions">
            <a class="mt-btn mt-btn-cta" href="/">На главную страницу →</a>
          </div>

          <div class="mt-404-help">
            Искали что-то конкретное или нашли битую ссылку?
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener" class="mt-link-accent">Напишите нам в мессенджер →</a>
          </div>
        </div>
      </main>

{footer_html}

    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
"""


def build_requisites_page() -> str:
    """Builds the official company requisites page for ООО 'МОЛНИЯ ТЕХ'."""
    nav_html = render_nav_html(active_item="", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")

    title = "Реквизиты компании ООО «МОЛНИЯ ТЕХ» — Молния"
    description = "Официальные банковские и юридические реквизиты ООО «МОЛНИЯ ТЕХ» (ИНН 7806637461, ОГРН 1267800068458) для договоров, счетов и безналичной оплаты."
    canonical = "https://molniya-tech.ru/requisites"

    json_ld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Молния Тех",
        "legalName": "Общество с ограниченной ответственностью «МОЛНИЯ ТЕХ»",
        "url": "https://molniya-tech.ru/",
        "logo": "https://molniya-tech.ru/assets/img/logo/molniya-logo-horizontal.svg",
        "sameAs": [
            "https://t.me/molniya_tex",
            "https://www.linkedin.com/company/molniya-tech"
        ],
        "taxID": "7806637461",
        "telephone": "+7-812-724-21-24",
        "email": "info@molniya-tech.ru",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "пр-кт Малоохтинский, д. 61, литера А, помещ. 1-Н",
            "addressLocality": "Санкт-Петербург",
            "postalCode": "195112",
            "addressCountry": "RU"
        }
    }
    json_ld_str = json.dumps(json_ld, ensure_ascii=False).replace("<", "\\u003c")

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="{canonical}">
  <meta name="theme-color" content="#FFFEFD">

  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <main class="mt-requisites-main">
        <div class="mt-requisites-header">
          <a href="/" class="mt-back-link">← На главную</a>
          <h1 class="mt-requisites-title">Реквизиты компании</h1>
          <p class="mt-requisites-sub">Официальные реквизиты ООО «МОЛНИЯ ТЕХ» для заключения договоров, выставления счетов и безналичных расчетов.</p>
          <div class="mt-requisites-actions">
            <a class="mt-btn-download" href="/assets/docs/molniya-requisites.pdf" download="Реквизиты_ООО_МОЛНИЯ_ТЕХ.pdf">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              Скачать карточку реквизитов (PDF)
            </a>
            <button class="mt-btn-copy-all" type="button" id="copy-all-btn">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
              Скопировать все реквизиты
            </button>
          </div>
        </div>

        <div class="mt-requisites-layout">
          <div class="mt-req-content">
            <!-- Сведения об организации -->
            <section class="mt-requisites-card">
              <h2 class="mt-requisites-card-title">Сведения об организации</h2>
              <div class="mt-requisites-table">
                <div class="mt-req-row">
                  <span class="mt-req-label">Полное наименование организации</span>
                  <div class="mt-req-val-wrap">
                    <span class="mt-req-value">ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "МОЛНИЯ ТЕХ"</span>
                    <button class="mt-copy-btn" type="button" data-copy='ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "МОЛНИЯ ТЕХ"'>Скопировать</button>
                  </div>
                </div>
                <div class="mt-req-row">
                  <span class="mt-req-label">Сокращенное наименование</span>
                  <div class="mt-req-val-wrap">
                    <span class="mt-req-value">ООО «МОЛНИЯ ТЕХ»</span>
                    <button class="mt-copy-btn" type="button" data-copy="ООО «МОЛНИЯ ТЕХ»">Скопировать</button>
                  </div>
                </div>
                <div class="mt-req-row">
                  <span class="mt-req-label">Юридический адрес</span>
                  <div class="mt-req-val-wrap">
                    <span class="mt-req-value">195112, РОССИЯ, Г. САНКТ-ПЕТЕРБУРГ, ВН.ТЕР.Г. МУНИЦИПАЛЬНЫЙ ОКРУГ МАЛАЯ ОХТА, ПР-КТ МАЛООХТИНСКИЙ, Д. 61, ЛИТЕРА А, ПОМЕЩ. 1-Н</span>
                    <button class="mt-copy-btn" type="button" data-copy="195112, РОССИЯ, Г. САНКТ-ПЕТЕРБУРГ, ВН.ТЕР.Г. МУНИЦИПАЛЬНЫЙ ОКРУГ МАЛАЯ ОХТА, ПР-КТ МАЛООХТИНСКИЙ, Д. 61, ЛИТЕРА А, ПОМЕЩ. 1-Н">Скопировать</button>
                  </div>
                </div>
                <div class="mt-req-row">
                  <span class="mt-req-label">ИНН</span>
                  <div class="mt-req-val-wrap">
                    <span class="mt-req-value">7806637461</span>
                    <button class="mt-copy-btn" type="button" data-copy="7806637461">Скопировать</button>
                  </div>
                </div>
                <div class="mt-req-row">
                  <span class="mt-req-label">КПП</span>
                  <div class="mt-req-val-wrap">
                    <span class="mt-req-value">780601001</span>
                    <button class="mt-copy-btn" type="button" data-copy="780601001">Скопировать</button>
                  </div>
                </div>
                <div class="mt-req-row">
                  <span class="mt-req-label">ОГРН</span>
                  <div class="mt-req-val-wrap">
                    <span class="mt-req-value">1267800068458</span>
                    <button class="mt-copy-btn" type="button" data-copy="1267800068458">Скопировать</button>
                  </div>
                </div>
                <div class="mt-req-row">
                  <span class="mt-req-label">Телефон</span>
                  <div class="mt-req-val-wrap">
                    <span class="mt-req-value">8 (812) 724-21-24</span>
                    <button class="mt-copy-btn" type="button" data-copy="8 (812) 724-21-24">Скопировать</button>
                  </div>
                </div>
                <div class="mt-req-row">
                  <span class="mt-req-label">Электронная почта</span>
                  <div class="mt-req-val-wrap">
                    <span class="mt-req-value">info@molniya-tech.ru</span>
                    <button class="mt-copy-btn" type="button" data-copy="info@molniya-tech.ru">Скопировать</button>
                  </div>
                </div>
              </div>
            </section>

            <!-- Банковские реквизиты -->
            <section class="mt-requisites-card">
              <h2 class="mt-requisites-card-title">Банковские реквизиты</h2>
              <div class="mt-requisites-table">
                <div class="mt-req-row">
                  <span class="mt-req-label">Расчетный счет</span>
                  <div class="mt-req-val-wrap">
                    <span class="mt-req-value">40702810110002359085</span>
                    <button class="mt-copy-btn" type="button" data-copy="40702810110002359085">Скопировать</button>
                  </div>
                </div>
                <div class="mt-req-row">
                  <span class="mt-req-label">Банк</span>
                  <div class="mt-req-val-wrap">
                    <span class="mt-req-value">АО «ТБанк»</span>
                    <button class="mt-copy-btn" type="button" data-copy="АО «ТБанк»">Скопировать</button>
                  </div>
                </div>
                <div class="mt-req-row">
                  <span class="mt-req-label">БИК банка</span>
                  <div class="mt-req-val-wrap">
                    <span class="mt-req-value">044525974</span>
                    <button class="mt-copy-btn" type="button" data-copy="044525974">Скопировать</button>
                  </div>
                </div>
                <div class="mt-req-row">
                  <span class="mt-req-label">ИНН банка</span>
                  <div class="mt-req-val-wrap">
                    <span class="mt-req-value">7710140679</span>
                    <button class="mt-copy-btn" type="button" data-copy="7710140679">Скопировать</button>
                  </div>
                </div>
                <div class="mt-req-row">
                  <span class="mt-req-label">Корреспондентский счет</span>
                  <div class="mt-req-val-wrap">
                    <span class="mt-req-value">30101810145250000974</span>
                    <button class="mt-copy-btn" type="button" data-copy="30101810145250000974">Скопировать</button>
                  </div>
                </div>
                <div class="mt-req-row">
                  <span class="mt-req-label">Юридический адрес банка</span>
                  <div class="mt-req-val-wrap">
                    <span class="mt-req-value">127287, г. Москва, ул. Хуторская 2-я, д. 38А, стр. 26</span>
                    <button class="mt-copy-btn" type="button" data-copy="127287, г. Москва, ул. Хуторская 2-я, д. 38А, стр. 26">Скопировать</button>
                  </div>
                </div>
              </div>
            </section>
          </div>

          <!-- SIDEBAR: QR CODE -->
          <aside class="mt-req-sidebar">
            <div class="mt-qr-card">
              <div class="mt-qr-title">Оплата по QR-коду</div>
              <div class="mt-qr-img-wrap">
                <img class="mt-qr-img" src="/assets/img/molniya-payment-qr.png" width="190" height="190" alt="QR-код для оплаты счета ООО МОЛНИЯ ТЕХ">
              </div>
              <p class="mt-qr-desc">Отсканируйте камерой смартфона или в приложении банка для моментального перевода по реквизитам счета без ручного ввода.</p>
              <div class="mt-qr-bank">
                <span class="mt-qr-bank-logo">Т</span>
                <span>АО «ТБанк»</span>
              </div>
            </div>
          </aside>
        </div>
      </main>

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
"""


def build_privacy_page() -> str:
    """Builds the official privacy policy page for ООО 'МОЛНИЯ ТЕХ' matching 152-FZ."""
    nav_html = render_nav_html(active_item="", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")

    title = "Политика обработки персональных данных — Молния"
    description = "Официальная политика обработки персональных данных ООО «МОЛНИЯ ТЕХ» (molniya-tech.ru) в соответствии с 152-ФЗ. Цели обработки, порядок реализации прав и защита данных."
    canonical = "https://molniya-tech.ru/privacy"

    json_ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Политика обработки персональных данных",
        "description": "Официальная политика обработки персональных данных ООО «МОЛНИЯ ТЕХ» в соответствии с Федеральным законом № 152-ФЗ «О персональных данных».",
        "url": "https://molniya-tech.ru/privacy",
        "publisher": {
            "@type": "Organization",
            "name": "ООО «МОЛНИЯ ТЕХ»",
            "url": "https://molniya-tech.ru/",
            "logo": "https://molniya-tech.ru/assets/img/logo/molniya-logo-horizontal.svg"
        }
    }
    json_ld_str = json.dumps(json_ld, ensure_ascii=False).replace("<", "\\u003c")

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="{canonical}">
  <meta name="theme-color" content="#FFFEFD">

  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <main class="mt-privacy-main">
        <div class="mt-privacy-header">
          <a href="/" class="mt-back-link">← На главную</a>
          <div class="mt-eyebrow" style="margin-top:20px">Юридическая информация</div>
          <h1 class="mt-hero-title" style="font-size:clamp(28px,4.5vw,44px);margin-top:14px;line-height:1.18">Политика обработки персональных данных</h1>
          <p class="mt-privacy-date">Редакция введена в действие: 2 октября 2026 г. · ООО «МОЛНИЯ ТЕХ»</p>
        </div>

        <div class="mt-privacy-callout">
          <p>
            Настоящая Политика определяет цели, устанавливает порядок и условия обработки персональных данных пользователей сайта <strong>https://molniya-tech.ru/</strong>, меры, направленные на защиту персональных данных, а также содержит информацию о правах лиц, к которым относятся соответствующие персональные данные, использующих функционал сайта, в соответствии с Федеральным законом от 27.07.2006 г. №&nbsp;152-ФЗ «О&nbsp;персональных данных».
          </p>
          <p style="font-size:14px;color:var(--mt-text-muted)">
            Оператор: <strong>ООО «МОЛНИЯ ТЕХ»</strong> (ИНН 7806637461) · Контакт для оперативной связи: <a href="mailto:privacy@molniya-tech.ru" class="mt-link-accent">privacy@molniya-tech.ru</a>
          </p>
        </div>

        <section class="mt-privacy-section mt-privacy-section--first">
          <h2>Общие положения и термины</h2>
          <p>Политика обработки персональных данных (далее — Политика) определяет цели, устанавливает порядок и условия обработки персональных данных, меры, направленные на защиту персональных данных, а также содержит информацию о правах лиц, к которым относятся соответствующие персональные данные, использующих функционал сайта <a href="https://molniya-tech.ru/" class="mt-link-accent">https://molniya-tech.ru/</a> (далее — Сайт).</p>

          <p>В Политике вы можете встретить следующие термины:</p>
          <ul>
            <li><strong>Персональные данные (ПДн)</strong> — любая информация, относящаяся к прямо или косвенно определенному или определяемому физическому лицу (субъекту персональных данных);</li>
            <li><strong>Оператор</strong> — юридическое лицо, самостоятельно или совместно с другими лицами организующее и (или) осуществляющее обработку персональных данных, а также определяющее цели обработки персональных данных, состав персональных данных, подлежащих обработке, действия (операции), совершаемые с персональными данными — <strong>ООО «Молния Тех»</strong>;</li>
            <li><strong>Обработка персональных данных (обработка ПДн)</strong> — совершение с персональными данными действий (операций) или совокупности действий (операций) с использованием средств автоматизации и без использования таких средств, включая сбор, запись, систематизацию, накопление, хранение, уточнение (обновление, изменение), извлечение, использование, передачу (предоставление, доступ), обезличивание, блокирование, удаление, уничтожение персональных данных.</li>
          </ul>

          <p>Иные термины, не упомянутые выше, употребляются в значении, установленном нормативными правовыми актами Российской Федерации.</p>

          <p>Обработка персональных данных осуществляется Оператором в соответствии с требованиями Федерального закона от 27.07.2006 г. № 152-ФЗ «О персональных данных» и иными нормативными правовыми актами Российской Федерации, регулирующими правоотношения в сфере обработки персональных данных.</p>

          <p>Действие Политики распространяется на все персональные данные субъектов персональных данных, обрабатываемые Оператором с применением средств автоматизации и без применения таких средств. Также действие Политики распространяется на персональные данные, полученные Оператором как до, так и после ввода в действие Политики.</p>

          <p>Обработка персональных данных субъекта персональных данных осуществляется с согласия субъекта персональных данных на обработку его персональных данных, а также без получения согласия в случаях, предусмотренных законодательством Российской Федерации.</p>

          <p>В случае, если субъект персональных данных возражает против обработки своих персональных данных Оператором в соответствии с Политикой, он вправе отказаться от использования Сайта и (или) направить соответствующее обращение в адрес Оператора. В таком случае предоставление отдельных элементов функционала Сайта осуществляться не будет.</p>

          <div class="mt-privacy-contact-badge">
            <strong>Контакт для оперативной связи с Оператором по поводу обработки персональных данных:</strong><br>
            <a href="mailto:privacy@molniya-tech.ru" class="mt-link-accent">privacy@molniya-tech.ru</a>
          </div>
        </section>

        <section class="mt-privacy-section">
          <h2>1. Права субъектов персональных данных при обработке персональных данных</h2>
          <p>В соответствии с Федеральным законом от 27.07.2006 г. № 152-ФЗ «О персональных данных», субъект персональных данных имеет право:</p>

          <div class="mt-privacy-table-wrap">
            <table class="mt-privacy-table">
              <thead>
                <tr>
                  <th style="width:36%">Право субъекта ПДн</th>
                  <th>Содержание права</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>На доступ к персональным данным</strong></td>
                  <td>Субъект ПДн вправе запросить копию персональных данных, которые есть у Оператора относительно него.</td>
                </tr>
                <tr>
                  <td><strong>На уточнение персональных данных</strong></td>
                  <td>Субъект ПДн вправе потребовать у Оператора исправления/дополнения неточных и (или) неполных персональных данных.</td>
                </tr>
                <tr>
                  <td><strong>На блокирование и удаление персональных данных</strong></td>
                  <td>Субъект ПДн вправе запросить удаление персональных данных, которые есть у Оператора относительно него, за исключением случаев, когда Оператор обязан хранить эти данные в соответствии с действующим законодательством.</td>
                </tr>
                <tr>
                  <td><strong>На отзыв согласия на обработку персональных данных</strong></td>
                  <td>Субъект ПДн вправе отозвать свое согласие на обработку персональных данных в любой момент.</td>
                </tr>
                <tr>
                  <td><strong>На обжалование действий и (или) бездействий Оператора</strong></td>
                  <td>Субъект ПДн вправе обратиться к Оператору, если посчитает, что он нарушает его права при обработке персональных данных.</td>
                </tr>
                <tr>
                  <td><strong>На обжалование решений, принятых на основании исключительно автоматизированной обработки персональных данных</strong></td>
                  <td>Субъект ПДн вправе обратиться к Оператору, если посчитает, что решение, принятое в ходе исключительно автоматизированной обработки персональных данных, является неверным или нарушающим его права.</td>
                </tr>
              </tbody>
            </table>
          </div>

          <p>Субъект персональных данных также вправе обратиться к Оператору для уточнения порядка реализации иных прав, предусмотренных Федеральным законом от 27.07.2006 г. № 152-ФЗ «О персональных данных».</p>
        </section>

        <section class="mt-privacy-section">
          <h2>2. Порядок реализации прав субъектом персональных данных</h2>
          <p>Субъект персональных данных вправе реализовать свои права, предусмотренные разделом 1 Политики и законодательством Российской Федерации, регулирующим правоотношения в сфере обработки персональных данных, следующими способами:</p>
          <ul>
            <li>Отправить запрос на e-mail: <a href="mailto:privacy@molniya-tech.ru" class="mt-link-accent">privacy@molniya-tech.ru</a> в форме электронного документа, подписанного в соответствии с положениями законодательства Российской Федерации об электронной подписи;</li>
            <li>Отправить письменный запрос по юридическому адресу Оператора: <strong>195112, РОССИЯ, Г. САНКТ-ПЕТЕРБУРГ, ВН.ТЕР.Г. МУНИЦИПАЛЬНЫЙ ОКРУГ МАЛАЯ ОХТА, ПР-КТ МАЛООХТИНСКИЙ, Д. 61, ЛИТЕРА А, ПОМЕЩ. 1-Н</strong>;</li>
            <li>Также субъект персональных данных вправе обжаловать действия или бездействие Оператора в территориальном органе Роскомнадзора или суде.</li>
          </ul>
        </section>

        <section class="mt-privacy-section">
          <h2>3. Цели обработки персональных данных, категории обрабатываемых ПДн, порядок и условия обработки ПДн</h2>
          <p>Для достижения нижеперечисленных целей Оператор вправе собирать, записывать, систематизировать, накапливать, хранить, уточнять (обновлять, изменять), извлекать, использовать, передавать (предоставлять, обеспечивать доступ), блокировать, удалять, уничтожать персональные данные субъектов персональных данных.</p>

          <p><strong>Целями обработки персональных данных являются:</strong></p>
          <ul>
            <li>оказание услуг;</li>
            <li>обеспечение функционирования и развития Сервисов;</li>
            <li>проведение аналитических и маркетинговых исследований (в обезличенной форме).</li>
          </ul>

          <p>Перечисленные в настоящей Политике персональные данные могут передаваться Оператором третьим лицам для сбора информации, необходимой для исследования рынка товаров и услуг, которые в том числе будут производить оценку спроса и предложения, способствовать продвижению товаров и услуг, анализу эффективности проведённых информационных, рекламных и маркетинговых кампаний путём формирования обезличенной аналитической информации на основе данных об использовании Субъектом сервисов Оператора.</p>

          <p>Оператор вправе поручить обработку персональных данных или отдельные действия, связанные с персональными данными, третьим лицам — обработчикам — на основании заключаемых с этими лицами договоров и при наличии соответствующего правового основания. В частности, Оператор вправе поручать обработку персональных данных операторам платежных систем, операторам облачных серверов, а также юридическим лицам, осуществляющим доставку товаров, а именно:</p>
          <ul>
            <li><strong>ООО «ТАЙМВЭБ.КЛАУД»</strong></li>
          </ul>

          <p>В случае, если Оператор поручает обработку персональных данных другому лицу, ответственность перед субъектом ПДн за действия указанного лица несет Оператор. Лицо, осуществляющее обработку персональных данных по поручению Оператора, несет ответственность за безопасность персональных данных и выполнение требований законодательства перед Оператором.</p>

          <p>Персональные данные уничтожаются путем удаления из информационных систем Оператора с помощью встроенных средств информационных систем.</p>
        </section>

        <section class="mt-privacy-section">
          <h2>4. Заполнение анкеты и использование Сайта</h2>
          <p>Для использования полного функционала Сайта и записи для получения услуг или товаров субъект персональных данных дает согласие на обработку его ПДн посредством проставления галочки напротив соответствующей графы при заполнении формы.</p>

          <p><strong>В форме необходимо указать следующие персональные данные:</strong></p>
          <ul>
            <li>Фамилия, имя, отчество;</li>
            <li>Номер мобильного телефона;</li>
            <li>Адрес электронной почты.</li>
          </ul>

          <p>Основанием для обработки персональных данных субъекта ПДн в данном случае является согласие на обработку персональных данных. Согласие на обработку ПДн действует в течение срока использования субъектом ПДн Сайта.</p>

          <p>Обработка ПДн в указанной цели прекращается в течение 30 дней с момента получения от субъекта ПДн отзыва согласия на обработку персональных данных и запроса на удаление личного кабинета в свободной форме в соответствии с п. 5 ст. 21 Федерального закона от 27.07.2006 г. № 152-ФЗ «О персональных данных».</p>

          <p>После отзыва субъектом ПДн согласия на обработку ПДн Оператор вправе обрабатывать персональные данные в течение сроков, определенных в соответствии с законодательством (процессуальным, налоговым, гражданским, о бухгалтерском учете, пр.), для выполнения возложенных на него обязанностей, предупреждения и пресечения нарушений законов, наших правил, защиты пользователей от мошеннических и иных недобросовестных действий, а также для предоставления ответов на обращения.</p>
        </section>

        <section class="mt-privacy-section">
          <h2>5. Заявка на доступ и консультацию</h2>
          <p>Для обработки заявки на доступ к Молнии и связи с заявителем субъект персональных данных дает согласие на обработку его ПДн посредством проставления галочки при заполнении формы на главной странице или на страницах отраслевых решений сайта.</p>

          <p><strong>В форме необходимо указать следующие персональные данные:</strong></p>
          <ul>
            <li>Имя;</li>
            <li>Номер мобильного телефона;</li>
            <li>Адрес электронной почты.</li>
          </ul>

          <p>Заявка, отметка о согласии, время её получения и действовавшая редакция Политики сохраняются в базе данных Оператора. Уведомление о заявке также направляется через мессенджер в указанный Оператором канал для обработки заявки и ответа заявителю.</p>
          <p>Основанием для обработки персональных данных субъекта ПДн в данном случае является согласие на обработку персональных данных. Согласие на обработку ПДн действует в течение срока использования субъектом ПДн Сайта и услуг Оператора.</p>

          <p>Обработка ПДн в указанной цели прекращается в течение 30 дней с момента истечения срока действия согласия на обработку ПДн. Также субъект ПДн вправе отозвать свое согласие на обработку его персональных данных. В таком случае обработка ПДн в указанной цели прекращается в течение 30 дней с момента получения от субъекта ПДн отзыва согласия на обработку персональных данных в свободной форме в соответствии с п. 5 ст. 21 Федерального закона от 27.07.2006 г. № 152-ФЗ «О персональных данных».</p>

          <p>После прекращения обработки ПДн в указанной цели Оператор вправе обрабатывать персональные данные в течение сроков, определенных в соответствии с законодательством (процессуальным, налоговым, гражданским, о бухгалтерском учете, пр.), для выполнения возложенных на него обязанностей, предупреждения и пресечения нарушений законов, наших правил, защиты пользователей от мошеннических и иных недобросовестных действий, а также для предоставления ответов на обращения.</p>
        </section>

        <section class="mt-privacy-section">
          <h2>6. Получение информационной и рекламной рассылки</h2>
          <p>Для получения рассылки новостей и рекламных сообщений (включая, но не ограничиваясь, информации о спецпредложениях, скидках и акциях) субъект ПДн должен поставить галочку напротив соответствующей графы при заполнении формы.</p>

          <p>Основанием для обработки персональных данных субъекта ПДн в данном случае является согласие на обработку персональных данных.</p>

          <p>Обработка ПДн в указанной цели прекращается в течение 30 дней с момента отписки субъекта ПДн от рассылки или с момента прекращения распространения рассылки Оператором в соответствии с ч. 4-5 ст. 21 Федерального закона от 27.07.2006 г. № 152-ФЗ «О персональных данных» — в зависимости от того, что наступит раньше.</p>

          <p>После отзыва субъектом ПДн согласия на обработку ПДн Оператор вправе обрабатывать персональные данные в течение сроков, определенных в соответствии с законодательством (процессуальным, налоговым, гражданским, о бухгалтерском учете, пр.), для выполнения возложенных на него обязанностей, предупреждения и пресечения нарушений законов, наших правил, защиты пользователей от мошеннических и иных недобросовестных действий, а также для предоставления ответов на обращения.</p>
        </section>

        <section class="mt-privacy-section" id="cookies">
          <h2>7. Cookie-файлы</h2>
          <p>На Сайте могут использоваться следующие cookie-файлы:</p>

          <div class="mt-privacy-table-wrap">
            <table class="mt-privacy-table">
              <thead>
                <tr>
                  <th style="width:26%">Вид</th>
                  <th style="width:36%">Описание</th>
                  <th>Цель использования</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Необходимые cookie-файлы</strong></td>
                  <td>Обеспечивают надлежащую работу Сайта</td>
                  <td>Для обеспечения надлежащего отображения интерфейсов и их интерактивных компонентов</td>
                </tr>
                <tr>
                  <td><strong>Функциональные cookie-файлы</strong></td>
                  <td>Сохраняют предпочтения в отношении настроек Сайта</td>
                  <td>Для упрощения использования Сайта, лучшего пользовательского опыта</td>
                </tr>
                <tr>
                  <td><strong>Аналитические cookie-файлы</strong></td>
                  <td>Сохраняют агрегированную информацию об использовании Сайта и его отдельных элементов</td>
                  <td>Для дальнейшего улучшения интерфейсов, планирования развития Сайта</td>
                </tr>
                <tr>
                  <td><strong>Маркетинговые cookie-файлы</strong></td>
                  <td>Сохраняют информацию о том, как используется Сайт, то есть предпочтения в отношении использования Сайта</td>
                  <td>Для персонализации Сайта, оптимизации рекламных коммуникаций, оценки эффективности персонализации</td>
                </tr>
              </tbody>
            </table>
          </div>

          <p>Для отказа от использования cookie-файлов субъект ПДн может воспользоваться настройками браузера, где можно отключить использование cookie-файлов, а также в интерфейсе Сайта, если применимо. Полное отключение cookie-файлов может привести к ограничению функционала Сайта.</p>

          <p>Подробные инструкции по отключению cookie-файлов доступны по внешним ссылкам:</p>
          <ul>
            <li><a href="https://support.google.com/chrome/answer/95647" target="_blank" rel="noopener" class="mt-link-accent">Google Chrome</a></li>
            <li><a href="https://support.apple.com/ru-ru/guide/safari/sfri11471/mac" target="_blank" rel="noopener" class="mt-link-accent">Safari</a></li>
            <li><a href="https://browser.yandex.ru/help/personal-data-protection/cookies.html" target="_blank" rel="noopener" class="mt-link-accent">Яндекс Браузер</a></li>
            <li><a href="https://support.microsoft.com/ru-ru/microsoft-edge/удаление-файлов-cookie-в-microsoft-edge-63947406-40ac-c3b8-57b9-2a946a29ae09" target="_blank" rel="noopener" class="mt-link-accent">Microsoft Edge</a></li>
            <li><a href="https://support.mozilla.org/ru/kb/uluchshennaya-zashita-ot-otslezhivaniya-v-firefox-dlya-dekstopa" target="_blank" rel="noopener" class="mt-link-accent">Mozilla Firefox</a></li>
          </ul>
        </section>

        <section class="mt-privacy-section">
          <h2>8. Безопасность персональных данных</h2>
          <p>Персональные данные, обрабатываемые Оператором, признаются конфиденциальной информацией. Они защищены от потери, изменения и несанкционированного доступа согласно законодательству Российской Федерации в области персональных данных. Оператор применяет необходимые организационные меры и использует технические средства в соответствии со ст. 18, 18.1, 19 Федерального закона от 27.07.2006 г. № 152-ФЗ «О персональных данных».</p>

          <p>Оператор не передает персональные данные субъектов ПДн третьим лицам без их согласия, за исключением случаев, когда такая обязанность установлена для Оператора законом. В частности, Оператор вправе передавать персональные данные субъекта ПДн в ответ на официальный запрос со стороны государственных органов.</p>
        </section>

        <section class="mt-privacy-section">
          <h2>9. Изменения Политики</h2>
          <p>Отдельные бизнес-процессы Оператора могут изменяться, в связи с чем Политика будет актуализироваться и в нее будут вноситься изменения. Изменения Политики отслеживаются субъектом ПДн самостоятельно.</p>
        </section>

        <section class="mt-privacy-section" style="border-top:1px solid var(--mt-border);padding-top:28px">
          <h2>Оператор персональных данных</h2>
          <p><strong>ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ «МОЛНИЯ ТЕХ» (ООО «МОЛНИЯ ТЕХ»)</strong></p>
          <p>ИНН 7806637461 · КПП 780601001 · ОГРН 1267800068458</p>
          <p>Юридический адрес: 195112, Россия, г. Санкт-Петербург, вн.тер.г. Муниципальный округ Малая Охта, пр-кт Малоохтинский, д. 61, литера А, помещ. 1-Н</p>
          <p>Адрес электронной почты для обращений: <a href="mailto:privacy@molniya-tech.ru" class="mt-link-accent">privacy@molniya-tech.ru</a></p>
          <p style="margin-top:14px"><a href="/requisites" class="mt-link-accent">Официальные реквизиты компании →</a></p>
        </section>

      </main>

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261021-thanks"></script>
</body>
</html>
"""




def build_trainers_page() -> str:
    """Builds the complete personal trainers and nutritionists micro-landing page."""
    nav_html = render_nav_html(active_item="health", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")
    lead_html = render_lead_form_html(
        "trainers",
        'Получите <span class="mt-hero-accent">бесплатный доступ навсегда</span> для персонального тренера',
        "Оставьте контакты — покажем Молнию на примере вашей практики и поможем настроить страницу записи подопечных, баланс пакетов и расписание тренировок.",
    )

    title = "Онлайн-запись для персонального тренера: CRM и расписание тренировок"
    description = (
        "Программа для персональных фитнес-тренеров и нутрициологов: "
        "онлайн-запись подопечных 24/7, учёт пакетов тренировок, замеры тела и расписание без хаоса в чатах."
    )
    canonical = "https://molniya-tech.ru/trainers"

    faqs = [
        (
            "Как подопечные записываются на персональные тренировки через Молнию?",
            "Вы получаете персональную ссылку на расписание с вашим фото, квалификацией и перечнем услуг (разовая тренировка, сплит на двоих, пакет занятий, ведение по питанию). Ссылку можно закрепить в шапке профиля соцсетей, отправить в Telegram или закрепить в переписке. Клиент видит только открытые свободные слоты и бронирует удобный час за 30 секунд без установки приложений.",
        ),
        (
            "Как система ведёт учёт пакетов тренировок (блоков на 8, 10 или 12 занятий)?",
            "При оформлении пакета вы указываете количество занятий и срок действия блока. После каждой проведённой тренировки система списывает 1 занятие из баланса. Подопечный и тренер всегда видят актуальный остаток (например, «Осталось 3 из 10»), а перед последней тренировкой программа предупреждает о необходимости продления.",
        ),
        (
            "Что происходит, если подопечный отменяет занятие в последний момент?",
            "Вы сами устанавливаете регламент отмены — например, не позднее чем за 12 или 24 часа до тренировки. Если клиент отменяет визит вовремя, слот мгновенно освобождается для других желающих. Если отмена происходит позже установленного срока, занятие автоматически отмечается как списанное из пакета, защищая ваше рабочее время и доход.",
        ),
        (
            "Можно ли настроить буфер между тренировками на отдых и заполнение дневника?",
            "Да. Вы задаёте автоматический интервал (например, 15 минут) между записями. Система не позволит забронировать слоты впритык: у вас всегда будет время перевести дух, выпить воды, подготовить снаряды и зафиксировать в карточке подопечного рабочие веса и выполненные подходы.",
        ),
        (
            "Подходит ли программа для нутрициологов и ведения клиентов онлайн?",
            "Да. В списке услуг можно разделить очные тренировки в зале и онлайн-консультации по видеосвязи. Для нутрициологических сессий можно настроить анкету сбора данных: вес, объёмы, пищевые привычки, аллергии и цели клиента, чтобы вы получили вводные данные ещё до начала созвона.",
        ),
        (
            "Что делать, если я тренирую в нескольких разных фитнес-клубах или на выезде?",
            "В расписании Молнии можно создать несколько локаций — например, «Зал на Ленина», «Студия на Мира» или «Выездные тренировки». Для каждого дня вы указываете, в каком клубе работаете. Подопечный выбирает нужный зал и видит свободные часы только для этой локации.",
        ),
        (
            "Сколько стоит использование Молнии для индивидуального тренера?",
            "Для персональных фитнес-тренеров и нутрициологов действует бесплатный доступ со всеми возможностями: онлайн-расписание, карточки подопечных, учёт баланса пакетов и автоматические напоминания. Никаких скрытых платежей и комиссий с ваших клиентов.",
        ),
    ]

    faq_html = "\n".join(
        f'            <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
        for q, a in faqs
    )

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://molniya-tech.ru/"},
                {"@type": "ListItem", "position": 2, "name": "Здоровье и фитнес", "item": "https://molniya-tech.ru/health"},
                {"@type": "ListItem", "position": 3, "name": "Онлайн-запись для персонального тренера", "item": canonical},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Молния Тех — онлайн-запись и CRM для персональных тренеров",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web, iOS, Android, macOS, Windows",
            "url": canonical,
            "description": description,
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "RUB",
                "description": "Бесплатный демо-доступ и настройка расписания тренировок",
            },
            "publisher": {
                "@type": "Organization",
                "name": "ООО «МОЛНИЯ ТЕХ»",
                "url": "https://molniya-tech.ru",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a,
                    },
                }
                for q, a in faqs
            ],
        },
    ]
    json_ld_str = json.dumps(json_ld, ensure_ascii=False)

    page_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#FAF7F2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#12100E" media="(prefers-color-scheme: dark)">
  <link rel="canonical" href="{canonical}">

  <!-- Favicons -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- HERO -->
      <section class="mt-hero" data-screen-label="Герой" data-mt-hero-scene>

        <div class="mt-hero-lead">
          <h1 class="mt-hero-title">
            Онлайн-запись и расписание<br><span class="mt-hero-accent">для персональных тренеров</span>
          </h1>

          <div class="mt-hero-bottom">
            <div class="mt-hero-intro">
              <p class="mt-hero-sub">Персональная страница записи 24/7, учёт пакетов тренировок, замеры прогресса и напоминания подопечным без хаоса в мессенджерах</p>
              <a class="mt-btn mt-btn-hero" href="#contact">Получить бесплатный доступ</a>
            </div>

            <ul class="mt-facets mt-facets--full" aria-label="Преимущества для персональных тренеров">
              <li class="mt-facet">
                <span class="mt-facet-name">Пакеты занятий</span>
                <span class="mt-facet-note">автоучёт остатка тренировок и продлений</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Доступно 24/7</span>
                <span class="mt-facet-note">онлайн-запись подопечных без звонков</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Замеры и цели</span>
                <span class="mt-facet-note">динамика веса, объёмов и рабочие веса</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name mt-facet-name--soon">Напоминания</span>
                <span class="mt-facet-note">E-mail, мессенджер или SMS подопечным</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <div class="mt-tablet">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для персонального тренера: расписание тренировок и учет подопечных" width="1710" height="983" fetchpriority="high">
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </div>
            <p class="mt-hero-media-caption">Электронное расписание персональных тренировок и учет подопечных в реальном времени</p>
          </div>
        </div>

      </section>

      <!-- LIVE SCHEDULE STATUS -->
      <section class="mt-section mt-reveal" data-screen-label="Расписание тренировок" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Каждый подопечный, слот и пакет <span class="mt-overview-hook">под вашим контролем</span></h2>
          <p class="mt-section-sub">Вы видите занятость времени, статус тренировок и количество оставшихся занятий у каждого подопечного с любого устройства.</p>
        </div>

        <div class="mt-auto-bays">
          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">08:00 · Силовая зона · Сплит грудь/трицепс</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В зале</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Михаил Р. · Пакет 8 из 10</div>
                <div class="mt-auto-car-tier">Жим 95 кг 4х6 · Замеры объёмов в пятницу</div>
              </div>
              <span class="mt-dropdown-footer-icon">🏋️‍♂️</span>
            </div>
            <div class="mt-auto-service">
              <span>Персональная тренировка (60 мин)</span>
              <span class="mt-auto-price">По пакету</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">12:00 · Функционал & Кардио · Кор и баланс</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--ready">Подтверждено</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Екатерина Д. · Пакет 2 из 10</div>
                <div class="mt-auto-car-tier">Круговой тренинг + МФР ролл · Пульс до 145</div>
              </div>
              <span class="mt-dropdown-footer-icon">⏱️</span>
            </div>
            <div class="mt-auto-service">
              <span>Функциональный тренинг</span>
              <span class="mt-auto-price">По пакету</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">17:00 · Силовая зона · Присед и жим ногами</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--hold">Продление</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Максим Т. · Пакет 10 из 10 (финал)</div>
                <div class="mt-auto-car-tier">Присед 120 кг · Напомнить об оплате блока</div>
              </div>
              <span class="mt-dropdown-footer-icon">🎯</span>
            </div>
            <div class="mt-auto-service">
              <span>Силовая тренировка</span>
              <span class="mt-auto-price">Оплата блока</span>
            </div>
          </div>
        </div>
      </section>

      <!-- TRAINERS OVERVIEW VALUE GRID -->
      <section class="mt-section mt-section--overview mt-reveal" data-screen-label="Функции для тренера" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Всё для работы персонального тренера <span class="mt-overview-hook">в одной удобной системе</span></h2>
          <p class="mt-section-sub">Один сервис вместо блокнотов, заметок в телефоне и бесконечных переписок: онлайн-расписание 24/7, учёт баланса пакетов тренировок, замеры прогресса и автоматические напоминания подопечным.</p>
        </div>

        <div class="mt-overview-grid">
          <article class="mt-overview-card">
            <h3>Персональный календарь и слоты <span class="mt-overview-hook">без переписок в WhatsApp</span></h3>
            <p>Клиенты переходят по прямой ссылке на ваше расписание и бронируют свободные часы в один клик. Система автоматически добавляет 15 минут буфера между тренировками и исключает накладки.</p>
            <div class="mt-overview-preview mt-overview-preview--schedule" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Календарь слотов</span><span>Буфер 15 мин</span></div>
              <div class="mt-overview-calendar"><span>08:00</span><div class="mt-overview-slot">Михаил Р.: Сплит <small>Пакет 8/10</small></div><span>10:30</span><div class="mt-overview-slot mt-overview-slot--light">Павел В.: Тяга <small>Пакет 4/12</small></div><span>12:00</span><div></div></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Персональная страница тренера <span class="mt-overview-hook">в вашем фирменном стиле</span></h3>
            <p>Короткая ссылка для шапки профиля соцсетей и Telegram: фото, квалификация, описание услуг (разовое занятие, блоки тренировок, план питания) и прямой выбор удобного времени.</p>
            <div class="mt-overview-preview mt-overview-preview--prices" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Страница бронирования</span><span>Доступно 24/7</span></div>
              <div class="mt-overview-price-row"><span>Блок 10 персональных тренировок</span><strong>60 мин · Срок 35 дней</strong></div>
              <div class="mt-overview-price-row"><span>Удобная короткая ссылка</span><strong>Для соцсетей и Telegram</strong></div>
              <div class="mt-overview-price-tag">Подопечные бронируют слоты сами без звонков</div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Автоматические напоминания <span class="mt-overview-hook">и защита от неявок в зал</span></h3>
            <p>Подопечный получает мгновенное подтверждение после бронирования, а накануне и за 2 часа до тренировки — напоминание в Telegram или по SMS. Он успеет предупредить об отмене вовремя.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Telegram-напоминание</span><span>Без рутины</span></div>
              <div class="mt-overview-message">
                Артём, напоминаем о тренировке сегодня в 17:00 в Силовой зоне. Ждём в зале вовремя, не забудьте форму и воду!
                <span class="mt-overview-reaction">🏋️‍♂️</span>
              </div>
              <div class="mt-overview-client-row"><span>Telegram, E-mail или SMS</span><strong>На выбор подопечного →</strong></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Учёт пакетов тренировок и отмен <span class="mt-overview-hook">в профиле подопечного</span></h3>
            <p>Молния сама списывает занятие из блока (8, 10 или 12) при отметке в зале. Если клиент отменяет тренировку позже регламента (за 12 часов), занятие автоматически списывается из баланса.</p>
            <div class="mt-overview-preview mt-overview-preview--process" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Карточка подопечного</span><span>Михаил Р. (Пакет 10)</span></div>
              <div class="mt-overview-stages"><span>Блок 10</span><i></i><span>Проведено: 8</span><i></i><span>Остаток: 2</span></div>
              <div class="mt-overview-check">✓ <span>Списание по факту тренировки</span></div>
              <div class="mt-overview-check">✓ <span>Регламент отмены за 12 часов активен</span></div>
            </div>
          </article>

          <article class="mt-overview-card mt-overview-card--featured">
            <h3>Замеры тела, цели и динамика весов <span class="mt-overview-hook">в одном месте</span></h3>
            <p>Фиксируйте замеры талии, бёдер, процент жира, противопоказания (протрузии, колени) и историю рабочих весов в подходах. Профиль доступен со смартфона перед каждым подходом.</p>
            <div class="mt-overview-preview mt-overview-preview--metrics" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Динамика прогресса</span><span>Дневник подопечного</span></div>
              <div class="mt-overview-metrics"><span>Вес<b>-4.2 кг</b></span><span>Талия<b>-5 см</b></span><span>Жим<b>95 кг</b></span></div>
              <div class="mt-overview-chart"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            </div>
          </article>
        </div>

        <div class="mt-overview-action">
          <a class="mt-btn mt-btn-cta" href="#contact">Получить бесплатный доступ</a>
        </div>
      </section>

      <!-- TRAINERS JOURNEY -->
      <section class="mt-section mt-journey" data-screen-label="Путь подопечного на тренировку">
        <div class="mt-section-head mt-section-head--center" data-mt-reveal>
          <h2 class="mt-section-title">Один визит на тренировку. <span class="mt-hero-accent">Полный контроль в расписании.</span></h2>
          <p class="mt-section-sub">Посмотрите, как Молния автоматизирует тренировочный процесс: от выбора слота на персональной странице до списания занятия из пакета и фиксации замеров.</p>
        </div>

        <div class="mt-journey-example" aria-label="Пример персональной тренировки" data-mt-reveal data-mt-delay="80">
          <span>Пример</span><strong>Персональная тренировка (Силовой сплит)</strong><span>Длительность 60 минут + 15 минут буфер на отдых и фиксацию весов</span>
        </div>

        <div class="mt-journey-list">
          <article class="mt-journey-step">
            <div class="mt-journey-index">01</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Подопечный</span>
              <h3>Выбор удобного окна тренировки на странице записи 24/7</h3>
              <p>Клиент открывает персональную ссылку тренера в Telegram или браузере, выбирает свободный слот и мгновенно закрепляет время за собой.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--booking" aria-label="Пример бронирования">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Бронирование слота</span>
                <span class="mt-journey-proof-badge">Подтверждено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Подопечный</span><strong>Артём Л.</strong></div>
              <div class="mt-journey-proof-row"><span>Услуга</span><strong>Персональная тренировка (60 мин)</strong></div>
              <div class="mt-journey-proof-row"><span>Время</span><strong>Вторник, 17:00 – 18:00 · Силовая зона</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">02</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Карточка</span>
              <h3>Учёт пакета занятий и фиксация ограничений по здоровью</h3>
              <p>Система проверяет баланс блока тренировок, напоминает о скором продлении и выводит тренеру заметки по противопоказаниям клиента.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--process" aria-label="Анкета записи">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Тренировка #8410</span>
                <span class="mt-journey-proof-badge">Пакет 10/10</span>
              </div>
              <div class="mt-journey-proof-row"><span>Баланс</span><strong>10-е занятие (пора продлевать)</strong></div>
              <div class="mt-journey-proof-row"><span>Здоровье</span><strong>Протрузия L5-S1 · Исключить осевую</strong></div>
              <div class="mt-journey-proof-row"><span>Статус</span><strong>Запись в календаре зафиксирована</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">03</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Система</span>
              <h3>Автоматические напоминания накануне занятия</h3>
              <p>Сервисный бот заблаговременно присылает сообщение в Telegram с напоминанием о времени тренировки, номере зала и форме одежды.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--order" aria-label="Сообщение с напоминанием">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Напоминание</span>
                <span class="mt-journey-proof-badge">Отправлено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Канал</span><strong>Telegram-бот / E-mail / SMS</strong></div>
              <div class="mt-journey-proof-row"><span>Инфо</span><strong>Силовая зона, тренер Денис К.</strong></div>
              <div class="mt-journey-proof-row"><span>Результат</span><strong>Подопечный вовремя на тренировке</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">04</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Тренер</span>
              <h3>Отметка в зале, списание занятия и фиксация весов</h3>
              <p>Тренер отмечает проведённую тренировку, вносит рабочие веса в дневник и видит автоматическое списание занятия из баланса пакета.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--payout" aria-label="Результат тренировки">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Итог тренировки</span>
                <span class="mt-journey-proof-badge">Завершено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Пакет</span><strong>Блок закрыт · Заявка на продление</strong></div>
              <div class="mt-journey-proof-row"><span>Рабочий вес</span><strong>Присед 120 кг 4х8 зафиксирован</strong></div>
              <div class="mt-journey-proof-row"><span>Следующий слот</span><strong>Четверг, 17:00 забронирован</strong></div>
            </div>
          </article>
        </div>
      </section>

      <!-- REAL-WORLD CASE STUDY -->
      <section class="mt-case-section mt-reveal" data-screen-label="Кейс персонального тренера" data-mt-reveal>
        <div class="mt-case-card">
          <div class="mt-case-header">
            <div class="mt-case-tag">⚡ Кейс персонального тренера</div>
            <h2 class="mt-case-title">Александр Волков, персональный тренер и нутрициолог</h2>
            <blockquote class="mt-case-quote">
              «Раньше каждый вечер уходил на бесконечные переписки в WhatsApp: кто-то заболел, кто-то перенёс, кто-то спорит, сколько тренировок осталось в оплаченном блоке. С Молнией я просто закрепил ссылку на расписание в Telegram. Подопечные сами бронируют свободные слоты, система списывает тренировки и напоминает об оплате нового пакета. Я экономлю минимум два часа в день.»
            </blockquote>
            <div class="mt-case-author">
              Александр Волков <span>· Персональный тренер высшей категории, <span style="white-space:nowrap">Москва</span></span>
            </div>
          </div>
          <div class="mt-case-stats">
            <div class="mt-case-stat">
              <span class="mt-case-num">0</span>
              <span class="mt-case-label">Споров об остатке оплаченных тренировок благодаря прозрачному балансу</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">2.5 ч</span>
              <span class="mt-case-label">В день сэкономлено на рутинных ответах в чатах и согласовании времени</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">100%</span>
              <span class="mt-case-label">Оплаченных пакетов и тренировок учтены без бумажных блокнотов</span>
            </div>
          </div>
        </div>
      </section>

      <!-- TRAINERS FAQ -->
      <section id="faq" class="mt-section mt-reveal" data-screen-label="Вопросы и ответы" data-mt-reveal>
        <div class="mt-section-head">
          <h2 class="mt-section-title">Вопросы об онлайн-записи и программе для персональных тренеров</h2>
        </div>
        <div class="mt-before-start-grid">
          <article class="mt-before-start-highlight">
            <h3>Попробуйте Молнию в своей работе тренера</h3>
            <p>Бесплатно поможем настроить календарь тренировок, баланс пакетов занятий, персональную страницу записи и перенести базу подопечных.</p>
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в мессенджер ↗</a>
          </article>
          <div class="mt-before-start-questions">
{faq_html}
          </div>
        </div>
        <p class="mt-before-start-privacy">Как мы обрабатываем данные — в <a href="/privacy">политике конфиденциальности</a>.</p>
      </section>

{lead_html}

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261022-flatstyle"></script>
</body>
</html>
'''
    return page_html



def build_martial_arts_page() -> str:
    """Builds the complete martial arts and boxing clubs micro-landing page."""
    nav_html = render_nav_html(active_item="health", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")
    lead_html = render_lead_form_html(
        "martial-arts",
        'Получите <span class="mt-hero-accent">бесплатный доступ навсегда</span> для клуба единоборств',
        "Оставьте контакты — покажем Молнию на примере вашего зала и поможем настроить сетку татами, рингов, учет детских и взрослых групп и абонементов.",
    )

    title = "Онлайн-запись в клуб единоборств и секцию бокса: CRM и расписание"
    description = (
        "Программа для клубов единоборств, секций бокса и MMA: "
        "онлайн-запись спортсменов 24/7, расписание рингов и татами, учёт абонементов и напоминания."
    )
    canonical = "https://molniya-tech.ru/martial-arts"

    faqs = [
        (
            "Как спортсмены и родители записываются на тренировки через Молнию?",
            "Вы получаете персональную страницу записи клуба с вашим логотипом, фотографиями залов и перечнем направлений (классический бокс, кикбоксинг, тайский бокс/муай-тай, ММА, самбо, дзюдо, BJJ и грэпплинг). Ссылку можно разместить в Telegram, ВК, на сайте или отправить в родительские чаты. Спортсмен или родитель видит актуальное расписание, возрастные группы и записывается за 1 минуту без скачивания приложений.",
        ),
        (
            "Как настраиваются лимиты мест в группах на татами и в ринге?",
            "Для каждого направления и зала вы задаёте максимальное количество участников (например, строго 12 человек в ринговой зоне или 16 спортсменов на татами). Как только лимит исчерпан, запись на этот слот блокируется, что предотвращает давку на снарядах и травмоопасную скученность во время спаррингов.",
        ),
        (
            "Как вести учёт абонементов (на 8, 12 тренировок, безлимит) и заморозок на время сборов?",
            "В карточке спортсмена отображается тариф: разовое посещение, абонемент на количество занятий или безлимитная карта на месяц/год. При каждой отметке прихода тренировка списывается автоматически. Если боец уезжает на спортивные сборы, соревнования или заболел, администратор может заморозить абонемент в один клик на нужный срок.",
        ),
        (
            "Можно ли вести учёт детских групп с контактами родителей и медицинскими справками?",
            "Да. В профиле юного спортсмена фиксируются ФИО и телефоны обоих родителей, дата рождения, весовая категория, а также отметка о наличии действующей медицинской справки (допуска к контактным видам спорта) и согласия на участие в спаррингах.",
        ),
        (
            "Как разделить индивидуальные тренировки тренеров и групповые занятия?",
            "В расписании наглядно разграничены групповые тренировки по расписанию и персональная аренда ринга/ковра для индивидуальной работы с тренером на лапах или снарядах. Тренеры видят свои персональные слоты в личном календаре на смартфоне.",
        ),
        (
            "Как работают автоматические напоминания перед тренировкой?",
            "Накануне занятия спортсмен (или родитель ребёнка) получает автоматическое уведомление в Telegram, E-mail или по SMS с указанием времени тренировки, зала и напоминанием взять необходимую экипировку (бинты, капу, перчатки, щитки). Это снижает число пропусков и опозданий.",
        ),
        (
            "Как быстро перенести базу бойцов и абонементы из другой CRM или Excel?",
            "Служба заботы Молнии бесплатно помогает перенести список спортсменов, действующие абонементы с остатком тренировок и график тренеров из Excel, Google Таблиц или других CRM (YClients, Мой Класс, 1С). Перенос занимает 15 минут и не прерывает тренировочный процесс зала.",
        ),
    ]

    faq_html = "\n".join(
        f'            <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
        for q, a in faqs
    )

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://molniya-tech.ru/"},
                {"@type": "ListItem", "position": 2, "name": "Здоровье и спорт", "item": "https://molniya-tech.ru/health"},
                {"@type": "ListItem", "position": 3, "name": "Онлайн-запись в клуб единоборств", "item": canonical},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Молния Тех — онлайн-запись и CRM для клубов единоборств и секций бокса",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web, iOS, Android, macOS, Windows",
            "url": canonical,
            "description": description,
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "RUB",
                "description": "Бесплатный демо-доступ и настройка расписания залов единоборств",
            },
            "publisher": {
                "@type": "Organization",
                "name": "ООО «МОЛНИЯ ТЕХ»",
                "url": "https://molniya-tech.ru",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a,
                    },
                }
                for q, a in faqs
            ],
        },
    ]
    json_ld_str = json.dumps(json_ld, ensure_ascii=False)

    page_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#FAF7F2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#12100E" media="(prefers-color-scheme: dark)">
  <link rel="canonical" href="{canonical}">

  <!-- Favicons -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo/molniya-mark-theme.svg?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-32.png?v=20260930">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/logo/molniya-mark-mono-white-32.png?v=20260930" media="(prefers-color-scheme: dark)">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/logo/molniya-mark-180.png?v=20260930">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <script type="application/ld+json">{json_ld_str}</script>

  <link rel="preload" href="/fonts/onest-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261022-flatstyle">
  <script src="/metrika.js" defer></script>
</head>
<body>

  <!-- shared SVG gradients used across icons -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <linearGradient id="mtgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D2634A"></stop><stop offset="1" stop-color="#B8442E"></stop></linearGradient>
  </defs></svg>

  <div class="mt-page">

    <!-- background atmosphere -->
    <div class="mt-atmosphere mt-atmosphere--glow" aria-hidden="true"></div>
    <div class="mt-atmosphere mt-atmosphere--grid" aria-hidden="true"></div>

    <div class="mt-content">

{nav_html}

      <!-- HERO -->
      <section class="mt-hero" data-screen-label="Герой" data-mt-hero-scene>

        <div class="mt-hero-lead">
          <h1 class="mt-hero-title">
            Онлайн-запись и расписание<br><span class="mt-hero-accent">для клубов единоборств и бокса</span>
          </h1>

          <div class="mt-hero-bottom">
            <div class="mt-hero-intro">
              <p class="mt-hero-sub">Персональная страница записи 24/7, сетка рингов и татами, учёт детских и взрослых групп, контроль абонементов и напоминания бойцам без рутины в чатах</p>
              <a class="mt-btn mt-btn-hero" href="#contact">Получить бесплатный доступ</a>
            </div>

            <ul class="mt-facets mt-facets--full" aria-label="Преимущества для клубов единоборств">
              <li class="mt-facet">
                <span class="mt-facet-name">Лимиты залов</span>
                <span class="mt-facet-note">контроль мест на татами и в ринге</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Доступно 24/7</span>
                <span class="mt-facet-note">онлайн-запись бойцов без звонков</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Абонементы</span>
                <span class="mt-facet-note">пакеты тренировок, безлимиты и заморозки</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name mt-facet-name--soon">Напоминания</span>
                <span class="mt-facet-note">E-mail, мессенджер или SMS спортсменам</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <div class="mt-tablet">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для клуба единоборств: расписание рингов, татами и учет спортсменов" width="1710" height="983" fetchpriority="high">
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </div>
            <p class="mt-hero-media-caption">Электронное расписание тренировок бойцовского клуба и загрузка залов в реальном времени</p>
          </div>
        </div>

      </section>

      <!-- LIVE SCHEDULE STATUS -->
      <section class="mt-section mt-reveal" data-screen-label="Расписание рингов и татами" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Каждый ринг, татами и группа <span class="mt-overview-hook">под вашим контролем</span></h2>
          <p class="mt-section-sub">Администратор и тренеры видят наполняемость групп, статус абонементов и свободные места на снарядах с любого устройства.</p>
        </div>

        <div class="mt-auto-bays">
          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">09:00 · Ринг 1 · Персональный бокс: Лапы & Снаряды</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--work">В ринге</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Артём В. · Тренер: Денис К.</div>
                <div class="mt-auto-car-tier">Постановка удара и защита · Разовое занятие</div>
              </div>
              <span class="mt-dropdown-footer-icon">🥊</span>
            </div>
            <div class="mt-auto-service">
              <span>Персональная тренировка</span>
              <span class="mt-auto-price">Оплачено</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">16:30 · Татами 1 · Самбо и дзюдо (Дети 8–12 лет)</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--ready">Полная группа</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Группа: Самбо Дети · Тренер: Руслан Б.</div>
                <div class="mt-auto-car-tier">12 из 12 спортсменов · Справки проверены</div>
              </div>
              <span class="mt-dropdown-footer-icon">🥋</span>
            </div>
            <div class="mt-auto-service">
              <span>Детская секция</span>
              <span class="mt-auto-price">По абонементу</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">19:30 · Октагон & Татами 2 · BJJ No-Gi & Грэпплинг</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--hold">Осталось 2 места</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Взрослая группа · Тренер: Мурад А.</div>
                <div class="mt-auto-car-tier">16 из 18 мест · Борьба в партере</div>
              </div>
              <span class="mt-dropdown-footer-icon">🤼‍♂️</span>
            </div>
            <div class="mt-auto-service">
              <span>Вечерняя группа</span>
              <span class="mt-auto-price">По абонементу</span>
            </div>
          </div>
        </div>
      </section>

      <!-- MARTIAL ARTS OVERVIEW VALUE GRID -->
      <section class="mt-section mt-section--overview mt-reveal" data-screen-label="Функции для клуба единоборств" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Управляйте клубом единоборств и бокса <span class="mt-overview-hook">без бумажной рутины</span></h2>
          <p class="mt-section-sub">Один сервис вместо блокнотов и таблиц: расписание татами и рингов 24/7, лимиты спортсменов в группах, учёт абонементов, заморозки на время сборов и напоминания в Telegram.</p>
        </div>

        <div class="mt-overview-grid">
          <article class="mt-overview-card">
            <h3>Сетка рингов, татами и снарядов <span class="mt-overview-hook">без давки в залах</span></h3>
            <p>Задайте точное число мест для каждой зоны (ринг, ковёр, мешки). Система автоматически блокирует запись при заполнении слота, защищая от скученности и травм во время спаррингов.</p>
            <div class="mt-overview-preview mt-overview-preview--schedule" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Сетка залов</span><span>Вместимость</span></div>
              <div class="mt-overview-calendar"><span>16:30</span><div class="mt-overview-slot">Татами 1: Самбо Дети <small>12 из 12 мест</small></div><span>18:00</span><div class="mt-overview-slot mt-overview-slot--light">Ринг: Бокс Взрослые <small>14 из 16 мест</small></div><span>19:30</span><div></div></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Страница записи клуба <span class="mt-overview-hook">в вашем фирменном стиле</span></h3>
            <p>Удобная ссылка для соцсетей, Telegram или сайта клуба. Спортсмены и родители сами выбирают направление (бокс, кикбоксинг, самбо, BJJ, ММА), тренера и группу без ожидания ответов в директ.</p>
            <div class="mt-overview-preview mt-overview-preview--prices" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Страница бронирования</span><span>Доступно 24/7</span></div>
              <div class="mt-overview-price-row"><span>Абонемент на 12 тренировок</span><strong>Бокс / ММА / BJJ · Месяц</strong></div>
              <div class="mt-overview-price-row"><span>Удобная короткая ссылка</span><strong>Для соцсетей и родительских чатов</strong></div>
              <div class="mt-overview-price-tag">Спортсмены записываются сами в любое время</div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Автоматические напоминания <span class="mt-overview-hook">и меньше пропусков тренировок</span></h3>
            <p>Боец или родитель ребёнка получает мгновенное подтверждение после бронирования, а накануне тренировки — напоминание по Telegram или SMS с напоминанием взять бинты, капу и перчатки.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Напоминание бойцу</span><span>Без рутины</span></div>
              <div class="mt-overview-message">
                Артём, напоминаем о тренировке по боксу завтра в 18:00 в Ринговой зоне. Не забудьте капу, бинты и сменную обувь!
                <span class="mt-overview-reaction">🥊</span>
              </div>
              <div class="mt-overview-client-row"><span>Telegram, E-mail или SMS</span><strong>На выбор спортсмена →</strong></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Учёт абонементов, безлимитов и заморозок <span class="mt-overview-hook">в профиле бойца</span></h3>
            <p>Фиксируйте разовые тренировки, блоки на 8/12 занятий и безлимитные карты. Если спортсмен уезжает на соревнования, сборы или заболел, администратор замораживает карту в один клик.</p>
            <div class="mt-overview-preview mt-overview-preview--process" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Профиль спортсмена</span><span>Артём В. (Абонемент)</span></div>
              <div class="mt-overview-stages"><span>Абонемент 12</span><i></i><span>Проведено: 9</span><i></i><span>Остаток: 3</span></div>
              <div class="mt-overview-check">✓ <span>Карта активна (списание при входе)</span></div>
              <div class="mt-overview-check">✓ <span>Справка от врача и согласие проверены</span></div>
            </div>
          </article>

          <article class="mt-overview-card mt-overview-card--featured">
            <h3>Детские группы, весовые и допуски <span class="mt-overview-hook">в едином реестре</span></h3>
            <p>Раздельный учёт детских секций (6–9, 10–14 лет), любителей и сборной клуба. В карточке спортсмена сохраняются контакты родителей, медицинские допуски и весовая категория.</p>
            <div class="mt-overview-preview mt-overview-preview--metrics" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Статистика клуба</span><span>Сводный табель</span></div>
              <div class="mt-overview-metrics"><span>Залы<b>3 зоны</b></span><span>Группы<b>12 в расписании</b></span><span>Учёт<b>100%</b></span></div>
              <div class="mt-overview-chart"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            </div>
          </article>
        </div>

        <div class="mt-overview-action">
          <a class="mt-btn mt-btn-cta" href="#contact">Получить бесплатный доступ</a>
        </div>
      </section>

      <!-- MARTIAL ARTS JOURNEY -->
      <section class="mt-section mt-journey" data-screen-label="Путь бойца в клуб">
        <div class="mt-section-head mt-section-head--center" data-mt-reveal>
          <h2 class="mt-section-title">Один визит на татами. <span class="mt-hero-accent">Полный порядок в клубе.</span></h2>
          <p class="mt-section-sub">Посмотрите, как Молния автоматизирует работу бойцовского клуба: от записи на тренировку до проверки допуска, списания занятия и учёта нагрузки тренера.</p>
        </div>

        <div class="mt-journey-example" aria-label="Пример тренировки" data-mt-reveal data-mt-delay="80">
          <span>Пример</span><strong>Групповая тренировка: Классический бокс</strong><span>Длительность 90 минут (разминка, снаряды, работа в парах, заминка)</span>
        </div>

        <div class="mt-journey-list">
          <article class="mt-journey-step">
            <div class="mt-journey-index">01</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Спортсмен</span>
              <h3>Выбор направления и группы на странице записи 24/7</h3>
              <p>Боец или родитель ребёнка переходит по ссылке клуба, выбирает вид спорта (бокс, кикбоксинг, самбо, BJJ) и видит свободные места в группе.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--booking" aria-label="Пример бронирования">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Бронирование тренировки</span>
                <span class="mt-journey-proof-badge">Место забронировано</span>
              </div>
              <div class="mt-journey-proof-row"><span>Спортсмен</span><strong>Артём В.</strong></div>
              <div class="mt-journey-proof-row"><span>Направление</span><strong>Классический бокс (Взрослые, 90 мин)</strong></div>
              <div class="mt-journey-proof-row"><span>Зал и время</span><strong>Ринг 1 · Вторник, 18:00 – 19:30</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">02</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Форма записи</span>
              <h3>Выбор абонемента и отметка медицинской справки</h3>
              <p>Спортсмен указывает контакты, выбирает клубный абонемент или разовый визит. Для детей фиксируются телефоны родителей и допуск врача.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--process" aria-label="Анкета записи">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Запись #7310</span>
                <span class="mt-journey-proof-badge">Подтверждена</span>
              </div>
              <div class="mt-journey-proof-row"><span>Тип визита</span><strong>Абонемент на 12 занятий</strong></div>
              <div class="mt-journey-proof-row"><span>Допуск / Врач</span><strong>Справка до 12.2026 активна</strong></div>
              <div class="mt-journey-proof-row"><span>Статус</span><strong>Место на снарядах зафиксировано</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">03</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Система</span>
              <h3>Автоматические напоминания бойцу накануне спаррингов</h3>
              <p>Сервисный Telegram-бот отправляет напоминание с деталями визита: зал, тренер, форма одежды и напоминание взять защитную экипировку.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--order" aria-label="Сообщение с напоминанием">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Напоминание</span>
                <span class="mt-journey-proof-badge">Отправлено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Канал</span><strong>Telegram / E-mail / SMS</strong></div>
              <div class="mt-journey-proof-row"><span>Инфо</span><strong>Ринг 1, тренер Денис К.</strong></div>
              <div class="mt-journey-proof-row"><span>Результат</span><strong>Спортсмен вовремя на разминке</strong></div>
            </div>
          </article>

          <article class="mt-journey-step">
            <div class="mt-journey-index">04</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Тренер</span>
              <h3>Отметка прихода на ковёр и автосписание занятия</h3>
              <p>Тренер отмечает явку в приложении. Занятие списывается с абонемента автоматически, а система учитывает проведённую тренировку в табеле смены.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--payout" aria-label="Результат тренировки">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Итог тренировки</span>
                <span class="mt-journey-proof-badge">Успешно</span>
              </div>
              <div class="mt-journey-proof-row"><span>Абонемент</span><strong>Осталось 3 из 12 занятий</strong></div>
              <div class="mt-journey-proof-row"><span>Табель тренера</span><strong>Группа учтена в смене</strong></div>
              <div class="mt-journey-proof-row"><span>Следующий шаг</span><strong>Запись на спарринги в четверг</strong></div>
            </div>
          </article>
        </div>
      </section>

      <!-- REAL-WORLD CASE STUDY -->
      <section class="mt-case-section mt-reveal" data-screen-label="Кейс бойцовского клуба" data-mt-reveal>
        <div class="mt-case-card">
          <div class="mt-case-header">
            <div class="mt-case-tag">⚡ Кейс бойцовского клуба</div>
            <h2 class="mt-case-title">Руслан Багиров, главный тренер клуба единоборств «Спарта»</h2>
            <blockquote class="mt-case-quote">
              «Раньше учёт групп вели в бумажных журналах: кто пришёл, у кого закончился абонемент, кто на сборах. Из-за переполнения татами на вечерних тренировках было тесно и травмоопасно. С Молнией мы настроили лимит 16 человек на ковер — запись закрывается сама. Родители детей получают напоминания в Telegram, а учёт заморозок и оплат стал полностью прозрачным.»
            </blockquote>
            <div class="mt-case-author">
              Руслан Багиров <span>· Мастер спорта, основатель бойцовского клуба, <span style="white-space:nowrap">Санкт-Петербург</span></span>
            </div>
          </div>
          <div class="mt-case-stats">
            <div class="mt-case-stat">
              <span class="mt-case-num">0</span>
              <span class="mt-case-label">Случаев переполнения татами благодаря автоматическому лимиту мест</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">3 ч</span>
              <span class="mt-case-label">В день сэкономлено администратором на подтверждениях и ручной записи групп</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">100%</span>
              <span class="mt-case-label">Прозрачный учёт заморозок абонементов на период спортивных сборов</span>
            </div>
          </div>
        </div>
      </section>

      <!-- MARTIAL ARTS FAQ -->
      <section id="faq" class="mt-section mt-reveal" data-screen-label="Вопросы и ответы" data-mt-reveal>
        <div class="mt-section-head">
          <h2 class="mt-section-title">Вопросы об онлайн-записи и программе для клубов единоборств</h2>
        </div>
        <div class="mt-before-start-grid">
          <article class="mt-before-start-highlight">
            <h3>Попробуйте Молнию для своего бойцовского клуба</h3>
            <p>Бесплатно поможем настроить расписание татами и рингов, лимиты мест в группах, форму онлайн-записи и перенести базу спортсменов.</p>
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в мессенджер ↗</a>
          </article>
          <div class="mt-before-start-questions">
{faq_html}
          </div>
        </div>
        <p class="mt-before-start-privacy">Как мы обрабатываем данные — в <a href="/privacy">политике конфиденциальности</a>.</p>
      </section>

{lead_html}

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"/></svg>
      Обновления в ТГ-канале
    </a>

  </div>

  <script src="/script.js?v=20261022-flatstyle"></script>
</body>
</html>
'''
    return page_html



def main():
    print("Building sector landing page: /auto...")
    auto_html = build_auto_page()
    (ROOT_DIR / "auto.html").write_text(auto_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'auto.html'}")

    print("Building sector landing page: /beauty...")
    beauty_html = build_beauty_page()
    (ROOT_DIR / "beauty.html").write_text(beauty_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'beauty.html'}")

    print("Building sector landing page: /health...")
    health_html = build_health_page()
    (ROOT_DIR / "health.html").write_text(health_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'health.html'}")

    print("Building sector landing page: /spaces...")
    spaces_html = build_spaces_page()
    (ROOT_DIR / "spaces.html").write_text(spaces_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'spaces.html'}")

    print("Building sector landing page: /photostudios...")
    photostudios_html = build_photostudios_page()
    (ROOT_DIR / "photostudios.html").write_text(photostudios_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'photostudios.html'}")

    print("Building sector landing page: /cleaning...")
    cleaning_html = build_cleaning_page()
    (ROOT_DIR / "cleaning.html").write_text(cleaning_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'cleaning.html'}")

    print("Building sector landing page: /stretching...")
    stretching_html = build_stretching_page()
    (ROOT_DIR / "stretching.html").write_text(stretching_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'stretching.html'}")

    print("Building sector landing page: /yoga...")
    yoga_html = build_yoga_page()
    (ROOT_DIR / "yoga.html").write_text(yoga_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'yoga.html'}")

    print("Building sector landing page: /trainers...")
    trainers_html = build_trainers_page()
    (ROOT_DIR / "trainers.html").write_text(trainers_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'trainers.html'}")

    print("Building sector landing page: /martial-arts...")
    martial_arts_html = build_martial_arts_page()
    (ROOT_DIR / "martial-arts.html").write_text(martial_arts_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'martial-arts.html'}")

    print("Building sector landing page: /psychologist...")
    psychologist_html = build_psychologist_page()
    (ROOT_DIR / "psychologist.html").write_text(psychologist_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'psychologist.html'}")

    print("Building sector landing page: /education...")
    education_html = build_education_page()
    (ROOT_DIR / "education.html").write_text(education_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'education.html'}")

    print("Building sector landing page: /pets...")
    pets_html = build_pets_page()
    (ROOT_DIR / "pets.html").write_text(pets_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'pets.html'}")

    print("Building sector landing page: /repair...")
    repair_html = build_repair_page()
    (ROOT_DIR / "repair.html").write_text(repair_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'repair.html'}")

    print("Building pricing landing page: /pricing.html...")
    pricing_html = build_pricing_page()
    (ROOT_DIR / "pricing.html").write_text(pricing_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'pricing.html'}")

    print("Building competitor migration landing page: /dikidi.html...")
    dikidi_html = build_dikidi_page()
    (ROOT_DIR / "dikidi.html").write_text(dikidi_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'dikidi.html'}")

    print("Building competitor migration landing page: /yclients.html...")
    yclients_html = build_yclients_page()
    (ROOT_DIR / "yclients.html").write_text(yclients_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'yclients.html'}")

    print("Building 404 error page: /404.html...")
    not_found_html = build_404_page()
    (ROOT_DIR / "404.html").write_text(not_found_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / '404.html'}")

    print("Building about page: /about.html...")
    about_html = build_about_page()
    (ROOT_DIR / "about.html").write_text(about_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'about.html'}")

    print("Building requisites page: /requisites.html...")
    req_html = build_requisites_page()
    (ROOT_DIR / "requisites.html").write_text(req_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'requisites.html'}")

    print("Building privacy policy page: /privacy.html...")
    privacy_html = build_privacy_page()
    (ROOT_DIR / "privacy.html").write_text(privacy_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'privacy.html'}")

    print("Building thank you page: /thanks.html...")
    thanks_html = build_thanks_page()
    (ROOT_DIR / "thanks.html").write_text(thanks_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'thanks.html'}")

    sync_navigation_to_index()
    sync_navigation_to_blog()
    sync_sitemap()
    print("DRY build complete!")


if __name__ == "__main__":
    main()
