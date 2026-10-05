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
        "emoji": "📱",
        "active": False,
        "badge": "Скоро",
        "badge_class": "mt-dropdown-badge--soon",
    },
]

BRAND_MARK_SVG = '<svg width="56" height="56" viewBox="0 0 96 96" fill="none" aria-hidden="true"><circle cx="48" cy="48" r="11" fill="none" stroke="#131B2C" stroke-width="8"/><g transform="rotate(0 48 48)"><rect x="41.5" y="6" width="13" height="22" rx="6.5" fill="#131B2C"/></g><g transform="rotate(60 48 48)"><rect x="41.5" y="6" width="13" height="22" rx="6.5" fill="#DF5F3C"/></g><g transform="rotate(120 48 48)"><rect x="41.5" y="6" width="13" height="22" rx="6.5" fill="#131B2C"/></g><g transform="rotate(180 48 48)"><rect x="41.5" y="6" width="13" height="22" rx="6.5" fill="#131B2C"/></g><g transform="rotate(240 48 48)"><rect x="41.5" y="6" width="13" height="22" rx="6.5" fill="#131B2C"/></g><g transform="rotate(300 48 48)"><rect x="41.5" y="6" width="13" height="22" rx="6.5" fill="#131B2C"/></g></svg>'


def render_nav_html(active_item: str = "", asset_prefix: str = "") -> str:
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
                  <a class="mt-dropdown-footer-link" href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в Telegram →</a>
                </div>
              </div>
            </li>
            <li><a class="mt-nav-link" href="/#how-it-works">Как это работает</a></li>
            <li><a class="mt-nav-link" href="/#features">Функции</a></li>
            <li><a class="mt-nav-link" href="/blog"{blog_active}>Блог</a></li>
          </ul>

          <a class="mt-btn mt-btn-nav" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
            Подписаться
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
          <a class="mt-mobile-link" href="/blog">Блог</a>
          <a class="mt-btn mt-btn-hero mt-mobile-cta" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
            Подписаться в Telegram
          </a>
        </div>
      </nav>'''


def render_footer_html(asset_prefix: str = "") -> str:
    logo_path = f"{asset_prefix}assets/img/logo/molniya-logo-horizontal.svg" if asset_prefix else "/assets/img/logo/molniya-logo-horizontal.svg"
    return f'''      <!-- FOOTER -->
      <footer class="mt-footer">
        <div class="mt-footer-inner">
          <div class="mt-footer-brand-col">
            <div class="mt-footer-brand">
              <img class="mt-footer-brand-logo" src="{logo_path}" width="327" height="96" alt="Молния Тех">
              <span class="mt-footer-year">· 2026</span>
            </div>
            <p class="mt-footer-sub">Заряжает ваш бизнес на генерацию заработка</p>
            <p class="mt-footer-legal">ООО «МОЛНИЯ ТЕХ» · ИНН 7806637461 · ОГРН 1267800068458 · Санкт-Петербург</p>
          </div>
          <div class="mt-footer-links">
            <a class="mt-footer-link" href="https://t.me/molniya_tex" target="_blank" rel="noopener"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>Telegram-канал</a>
            <a class="mt-footer-link" href="/privacy">Конфиденциальность</a>
            <a class="mt-footer-link" href="/requisites">Реквизиты</a>
          </div>
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
            <label class="mt-lead-consent"><input name="consent" type="checkbox" required><span>Согласен на обработку персональных данных по <a href="/privacy" target="_blank" rel="noopener">политике конфиденциальности</a>.</span></label>
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
            "q": "Как клиенты записываются на автомойку и получают уведомления в Telegram?",
            "a": "Клиенты записываются онлайн через виджет на сайте, по ссылке в соцсетях или QR-коду. Сервисный Telegram-бот автоматически присылает подтверждение бронирования, напоминание за 2 часа до визита и оповещение «Ваш автомобиль готов к выдаче» со ссылкой на чек."
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
  <link rel="stylesheet" href="/styles.css?v=20261002-audiences">
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
            <a class="mt-tablet" href="https://rutube.ru/video/bf11679edec2bbe548a54f9adf6bc3ca/" target="_blank" rel="noopener" aria-label="Смотреть видео: работа расписания боксов в Молнии">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для автомойки и автосервиса: расписание боксов и электронный журнал записи" width="1710" height="983" fetchpriority="high">
                <span class="mt-tablet-play">
                  <svg width="26" height="26" viewBox="0 0 24 24" fill="#C6543B"><path d="M8 5v14l11-7z"></path></svg>
                </span>
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </a>
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
            <h3>Telegram-уведомления <span class="mt-overview-hook">и клиентская база</span></h3>
            <p>Клиент получает подтверждение бронирования, напоминание за 2 часа и уведомление «Автомобиль готов к выдаче» со ссылкой на электронный чек. Вся история визитов и ТО сохраняется в карточке авто.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Статус готовности</span><span>Telegram</span></div>
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
              <p>Клиент выбирает марку, тип кузова и комплекс услуг на сайте или через Telegram. Программа сразу резервирует окно нужной длительности (55 минут вместо 40) с учетом габаритов кроссовера.</p>
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
              <h3>Выдача авто, Telegram-чек и расчет зарплаты мастеров</h3>
              <p>Клиент получает оповещение о готовности и ссылку на чек в Telegram. Программа моментально начисляет мастеру 35% (1 365 ₽) на баланс смены — без ручных записей и споров.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--payout" aria-label="Финансовый расчёт">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Расчёт мастера</span>
                <span class="mt-journey-proof-badge">Начислено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Александр В. (35%)</span><strong>+1 365 ₽</strong></div>
              <div class="mt-journey-proof-row"><span>Выручка автомойки</span><strong>+2 535 ₽</strong></div>
              <div class="mt-journey-proof-row"><span>Статус Telegram</span><strong>«Автомобиль выдан»</strong></div>
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
              <span class="mt-case-label">Снижение неявок благодаря Telegram-напоминаниям</span>
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
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в Telegram-канал ↗</a>
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
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
      Подписаться
    </a>

  </div>

  <script src="/script.js?v=20261002-formsource"></script>
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
            "q": "Как клиенты записываются онлайн и получают напоминания в Telegram?",
            "a": "Клиенты переходят по ссылке в соцсетях, на сайте или по QR-коду и выбирают удобное время и любимого мастера. Сервисный Telegram-бот автоматически подтверждает запись, напоминает о визите за 24 и 2 часа, снижая неявки на 85%."
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
  <link rel="stylesheet" href="/styles.css?v=20261002-audiences">
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
                <span class="mt-facet-note">Telegram-напоминания и повторные визиты</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <a class="mt-tablet" href="https://rutube.ru/video/bf11679edec2bbe548a54f9adf6bc3ca/" target="_blank" rel="noopener" aria-label="Смотреть видео: работа расписания в Молнии">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для салона красоты: расписание мастеров и электронный журнал записи" width="1710" height="983" fetchpriority="high">
                <span class="mt-tablet-play">
                  <svg width="26" height="26" viewBox="0 0 24 24" fill="#C6543B"><path d="M8 5v14l11-7z"></path></svg>
                </span>
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </a>
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
            <p>Клиенты записываются онлайн через сайт, соцсети или Telegram 24/7. Администратор управляет загрузкой кресел и кабинетов в один клик. Программа предотвращает накладки и «окна» между визитами.</p>
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
            <h3>Telegram-уведомления <span class="mt-overview-hook">и возвращаемость</span></h3>
            <p>Сервисные напоминания в Telegram за 24 и 2 часа снижают процент неявок до 85%. Автоматические приглашения на повторный визит через 3–4 недели стабильно возвращают клиентов без спама.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Статус записи</span><span>Telegram</span></div>
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
              <p>Клиент выбирает услугу, мастера и время за 30 секунд в виджете онлайн-записи. Программа сразу бронирует окно в расписании, не допуская накладок, и присылает подтверждение в Telegram.</p>
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
              <p>Клиент получает электронный чек в Telegram. Программа начисляет мастеру 40% за услугу (3 400 ₽) и 10% за уход (240 ₽). Через 4 недели клиент получит автоприглашение на обновление цвета.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--payout" aria-label="Финансовый расчёт">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Расчёт мастера</span>
                <span class="mt-journey-proof-badge">Начислено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Елена К. (выработка)</span><strong>+3 640 ₽</strong></div>
              <div class="mt-journey-proof-row"><span>Списание со склада</span><strong>Краситель -45г</strong></div>
              <div class="mt-journey-proof-row"><span>Telegram-автоприглашение</span><strong>Запланировано через 28 дн</strong></div>
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
              <span class="mt-case-label">Рост повторных записей через Telegram-напоминания</span>
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
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в Telegram-канал ↗</a>
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
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
      Подписаться
    </a>

  </div>

  <script src="/script.js?v=20261002-formsource"></script>
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
  <link rel="stylesheet" href="/styles.css?v=20261002-audiences">
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
                <span class="mt-facet-note">Telegram-напоминания и повторные визиты</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <a class="mt-tablet" href="https://rutube.ru/video/bf11679edec2bbe548a54f9adf6bc3ca/" target="_blank" rel="noopener" aria-label="Смотреть видео: работа расписания в Молнии">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для клиники и медицинского центра: расписание врачей и электронный журнал записи" width="1710" height="983" fetchpriority="high">
                <span class="mt-tablet-play">
                  <svg width="26" height="26" viewBox="0 0 24 24" fill="#C6543B"><path d="M8 5v14l11-7z"></path></svg>
                </span>
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </a>
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
            <p>Пациенты записываются онлайн через сайт, соцсети или Telegram 24/7. Администратор управляет загрузкой кабинетов, аппаратов и врачей в один клик. Программа предотвращает пересечения специалистов и простой оборудования.</p>
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
            <h3>Telegram-напоминания <span class="mt-overview-hook">и повторные приемы</span></h3>
            <p>Автоматические напоминания в Telegram за 24 и 2 часа снижают долю пропущенных приемов до 88%. Система вовремя напоминает пациентам о плановых осмотрах, вакцинациях и повторных сеансах курса массажа.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Статус визита</span><span>Telegram</span></div>
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
              <p>Пациент выбирает специальность, врача и удобный интервал за 30 секунд через Telegram или на сайте. Программа бронирует кабинет и временной слот нужной длительности с учетом регламента приема.</p>
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
              <h3>Оплата, Telegram-памятка и начисление зарплаты врача</h3>
              <p>Пациент получает электронный чек и рекомендации врача в Telegram. Программа моментально начисляет терапевту 40% (1 400 ₽) за прием — выработка рассчитывается без ручных таблиц и споров.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--payout" aria-label="Финансовый расчёт">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Расчёт врача</span>
                <span class="mt-journey-proof-badge">Начислено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Анна М. (40%)</span><strong>+1 400 ₽</strong></div>
              <div class="mt-journey-proof-row"><span>Списание со склада</span><strong>Расходники списаны</strong></div>
              <div class="mt-journey-proof-row"><span>Telegram-памятка</span><strong>«Рекомендации отправлены»</strong></div>
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
              «Раньше администраторы путались в накладках врачей, а пациенты забывали о приемах. В Молнии мы настроили четкое расписание по кабинетам, электронные карты и Telegram-напоминания. Неявки снизились практически до нуля, а учет процедур и зарплат стал полностью автоматическим.»
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
              <span class="mt-case-label">Снижение пропусков приемов благодаря Telegram-напоминаниям</span>
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
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в Telegram-канал ↗</a>
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
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
      Подписаться
    </a>

  </div>

  <script src="/script.js?v=20261002-formsource"></script>
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
            "Все бронирования — с сайта, из Telegram, соцсетей или внесенные администратором вручную — мгновенно попадают в единый календарь в реальном времени. Если слот занят, клиент физически не может выбрать это время в виджете, что полностью исключает накладки и конфликты.",
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
  <link rel="stylesheet" href="/styles.css?v=20261002-audiences">
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
                <span class="mt-facet-note">Telegram-напоминания и повторные брони</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <a class="mt-tablet" href="https://rutube.ru/video/bf11679edec2bbe548a54f9adf6bc3ca/" target="_blank" rel="noopener" aria-label="Смотреть видео: работа расписания в Молнии">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для аренды пространств и залов: шахматка броней и электронное расписание" width="1710" height="983" fetchpriority="high">
                <span class="mt-tablet-play">
                  <svg width="26" height="26" viewBox="0 0 24 24" fill="#C6543B"><path d="M8 5v14l11-7z"></path></svg>
                </span>
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </a>
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
            <h3>Онлайн-виджет бронирования <span class="mt-overview-hook">и Telegram-бот</span></h3>
            <p>Клиенты сами видят свободные окна и бронируют слоты на сайте или в Telegram 24/7. Никаких бесконечных переписок в мессенджерах: система сама покажет фото зала, стоимость и правила аренды.</p>
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
            <h3>Telegram-напоминания арендаторам <span class="mt-overview-hook">и правила отмены</span></h3>
            <p>Бот отправляет гостям код от двери или схему проезда, напоминает о времени визита за 24 и 2 часа и запрашивает подтверждение. Неявки снижаются на 85%, а отмены происходят строго по регламенту.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Напоминание арендатору</span><span>Telegram</span></div>
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
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в Telegram-канал ↗</a>
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
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
      Подписаться
    </a>

  </div>

  <script src="/script.js?v=20261002-formsource"></script>
</body>
</html>
'''
    return page_html


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
            "При отметке визита ученика в журнале занятие автоматически списывается с его баланса в 1 клик. Программа отслеживает срок действия абонемента, остаток уроков и заблаговременно напоминает родителям или ученику о продлении через Telegram.",
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
            "Сервисный Telegram-бот отправляет автоматические уведомления за 24 и за 2 часа до урока: напоминает время, кабинет и тему занятия. Это снижает число пропусков без уважительной причины на 80% и избавляет администраторов от ручных обзвонов.",
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
  <link rel="stylesheet" href="/styles.css?v=20261002-audiences">
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
                <span class="mt-facet-note">Telegram-напоминания об уроках и продлениях</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <a class="mt-tablet" href="https://rutube.ru/video/bf11679edec2bbe548a54f9adf6bc3ca/" target="_blank" rel="noopener" aria-label="Смотреть видео: работа расписания в Молнии">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для учебных центров и курсов: расписание групп и электронный журнал посещаемости" width="1710" height="983" fetchpriority="high">
                <span class="mt-tablet-play">
                  <svg width="26" height="26" viewBox="0 0 24 24" fill="#C6543B"><path d="M8 5v14l11-7z"></path></svg>
                </span>
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </a>
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
            <h3>Telegram-напоминания ученикам <span class="mt-overview-hook">и родителям</span></h3>
            <p>Сервисный бот предупреждает о занятии за 24 и 2 часа, напоминает взять сменную обувь или форму, а родителям отправляет отчет об успеваемости и напоминание о скором окончании абонемента.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Уведомление в Telegram</span><span>Школа «Ритм»</span></div>
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
              <p>Родитель выбирает направление, удобный филиал и время пробного занятия через виджет на сайте или в Telegram. Слот в группе резервируется автоматически.</p>
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
              <p>Родитель оплачивает абонемент на 8 занятий. Программа автоматически начисляет ставку преподавателю, формирует график уроков и отправляет памятку в Telegram.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--payout" aria-label="Финансовый расчет">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Абонемент активирован</span>
                <span class="mt-journey-proof-badge">Оплачено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Абонемент</span><strong>8 уроков (6 400 ₽)</strong></div>
              <div class="mt-journey-proof-row"><span>Начислено педагогу</span><strong>+800 ₽ за урок</strong></div>
              <div class="mt-journey-proof-row"><span>Telegram-бот</span><strong>«График уроков отправлен»</strong></div>
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
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в Telegram-канал ↗</a>
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
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
      Подписаться
    </a>

  </div>

  <script src="/script.js?v=20261002-formsource"></script>
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
            "Сервисный Telegram-бот напоминает владельцу о визите за 24 и за 2 часа, а во время процедуры мастер или администратор в 1 клик отправляет уведомление: «Ваш питомец готов, можно забирать!». А через 4–6 недель система заботливо приглашает на регулярный уход, возвращая постоянных клиентов.",
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
  <link rel="stylesheet" href="/styles.css?v=20261002-audiences">
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
                <span class="mt-facet-note">Telegram-напоминания о повторной стрижке через 4 недели</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <a class="mt-tablet" href="https://rutube.ru/video/bf11679edec2bbe548a54f9adf6bc3ca/" target="_blank" rel="noopener" aria-label="Смотреть видео: работа расписания в Молнии">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Программа для груминг-салонов: электронное расписание столов и запись питомцев" width="1710" height="983" fetchpriority="high">
                <span class="mt-tablet-play">
                  <svg width="26" height="26" viewBox="0 0 24 24" fill="#C6543B"><path d="M8 5v14l11-7z"></path></svg>
                </span>
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </a>
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
            <p>Владельцы записывают собак и кошек прямо с сайта и Telegram-канала. Форма сама предлагает выбрать породу, вес и допуслуги (чистка зубов, стрижка когтей), показывая точную стоимость.</p>
            <div class="mt-overview-preview mt-overview-preview--process" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Онлайн-запись в салон</span><span>Груминг собак</span></div>
              <div class="mt-overview-stages"><span>Порода</span><i></i><span>Услуга</span><i></i><span>Запись</span></div>
              <div class="mt-overview-check">✓ <span>Питомец: Померанский шпиц (стрижка «Модерн»)</span></div>
              <div class="mt-overview-check">✓ <span>Запись подтверждена: Сегодня 15:30</span></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Telegram-напоминания <span class="mt-overview-hook">и «Питомец готов!»</span></h3>
            <p>Сервисный бот предупреждает о записи за 24 и 2 часа, отправляет уведомление в 1 клик, когда питомца можно забирать, и заботливо приглашает на повторный груминг через 4–6 недель.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Уведомление в Telegram</span><span>Салон «Лапки»</span></div>
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
              <p>Хозяйка мгновенно получает Telegram-сообщение: «Марси готова!». Администратор принимает оплату по карте или СБП, грумер видит начисленный %, а бот ставит напоминание на визит через месяц.</p>
            </div>
            <div class="mt-journey-proof mt-journey-proof--analytics" aria-label="Расчет визита">
              <div class="mt-journey-proof-head">
                <span class="mt-journey-proof-title">Расчет визита</span>
                <span class="mt-journey-proof-badge">Оплачено</span>
              </div>
              <div class="mt-journey-proof-row"><span>Сумма</span><strong>3 800 ₽ (карта / СБП)</strong></div>
              <div class="mt-journey-proof-row"><span>Зарплата грумера</span><strong>1 710 ₽ (45% начислено)</strong></div>
              <div class="mt-journey-proof-row"><span>Telegram</span><strong>«Марси готова!» отправлено</strong></div>
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
              <span>автонапоминания в Telegram через 4–6 недель</span>
            </div>
            <div class="mt-case-stat">
              <strong>2 минуты</strong>
              <span>вместо 4 часов на еженедельный расчет зарплат мастеров</span>
            </div>
          </div>

          <blockquote class="mt-case-quote">
            <p>«Раньше администраторы постоянно ошибались с длительностью записи: ставили хаски и шпица на одно и то же время, из-за чего мастера задерживались и нервничали. В Молнии система точно знает время под каждую породу, а кнопка "Питомец готов" с автосообщением в Telegram избавила наш холл от толпы ожидающих хозяев».</p>
            <cite>Анастасия Белова · Основательница сети «Лапки & Хвостики»</cite>
          </blockquote>
        </div>
      </section>

      <!-- FAQ SECTION -->
      <section class="mt-section mt-faq" data-screen-label="Частые вопросы" id="faq" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Часто задаваемые вопросы</h2>
          <p class="mt-section-sub">Ответы на главные вопросы владельцев и управляющих груминг-салонов.</p>
        </div>

        <div class="mt-faq-list">
{faq_html}
        </div>
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
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
      Подписаться
    </a>

  </div>

  <script src="/script.js?v=20261002-formsource"></script>
</body>
</html>
'''
    return page_html


def sync_navigation_to_index():
    """Syncs the DRY nav, footer, and cookie banner into index.html."""
    content = INDEX_HTML.read_text(encoding="utf-8")
    nav_html = render_nav_html(active_item="", asset_prefix="")

    start_marker = "<!-- NAV -->"
    end_marker = "</nav>"
    if start_marker in content and end_marker in content:
        before = content.split(start_marker, 1)[0].rstrip(" \t")
        after = content.split(end_marker, 1)[1]
        content = before + nav_html + after

    footer_html = render_footer_html(asset_prefix="")
    f_start = "<!-- FOOTER -->"
    f_end = "</footer>"
    if f_start in content and f_end in content:
        before = content.split(f_start, 1)[0].rstrip(" \t")
        after = content.split(f_end, 1)[1]
        content = before + footer_html + after

    old_cookie_link = '<a href="/cookies" class="mt-link-accent">политике cookie</a>'
    new_cookie_link = '<a href="/privacy#cookies" class="mt-link-accent">политике конфиденциальности</a>'
    content = content.replace(old_cookie_link, new_cookie_link)

    INDEX_HTML.write_text(content, encoding="utf-8")
    print("Updated navigation, footer, and banner in index.html")


def sync_navigation_to_blog():
    """Syncs the DRY nav, footer, and cookie banner into blog/index.html."""
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
  <link rel="stylesheet" href="/styles.css?v=20261002-audiences">
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
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener" class="mt-link-accent">Напишите нам в Telegram →</a>
          </div>
        </div>
      </main>

{footer_html}

    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
      Подписаться
    </a>

  </div>

  <script src="/script.js?v=20261002-formsource"></script>
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
        "taxID": "7806637461",
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
  <link rel="stylesheet" href="/styles.css?v=20261002-audiences">
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
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
      Подписаться
    </a>

  </div>

  <script src="/script.js?v=20261002-formsource"></script>
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
  <link rel="stylesheet" href="/styles.css?v=20261002-audiences">
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

          <p>Заявка, отметка о согласии, время её получения и действовавшая редакция Политики сохраняются в базе данных Оператора. Уведомление о заявке также направляется через Telegram в указанный Оператором канал для обработки заявки и ответа заявителю.</p>
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
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
      Подписаться
    </a>

  </div>

  <script src="/script.js?v=20261002-formsource"></script>
</body>
</html>
"""


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

    print("Building sector landing page: /education...")
    education_html = build_education_page()
    (ROOT_DIR / "education.html").write_text(education_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'education.html'}")

    print("Building sector landing page: /pets...")
    pets_html = build_pets_page()
    (ROOT_DIR / "pets.html").write_text(pets_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'pets.html'}")

    print("Building 404 error page: /404.html...")
    not_found_html = build_404_page()
    (ROOT_DIR / "404.html").write_text(not_found_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / '404.html'}")

    print("Building requisites page: /requisites.html...")
    req_html = build_requisites_page()
    (ROOT_DIR / "requisites.html").write_text(req_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'requisites.html'}")

    print("Building privacy policy page: /privacy.html...")
    privacy_html = build_privacy_page()
    (ROOT_DIR / "privacy.html").write_text(privacy_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'privacy.html'}")

    sync_navigation_to_index()
    sync_navigation_to_blog()
    sync_sitemap()
    print("DRY build complete!")


if __name__ == "__main__":
    main()
