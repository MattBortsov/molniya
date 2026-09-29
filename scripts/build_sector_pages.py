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
        "active": False,
        "badge": "Скоро",
        "badge_class": "mt-dropdown-badge--soon",
    },
    {
        "id": "health",
        "slug": "health",
        "title": "Здоровье",
        "desc": "Клиники, массаж, частные кабинеты, спа",
        "icon": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="M12 9v4"/><path d="M10 11h4"/></svg>',
        "emoji": "🩺",
        "active": False,
        "badge": "Скоро",
        "badge_class": "mt-dropdown-badge--soon",
    },
    {
        "id": "education",
        "slug": "education",
        "title": "Образование",
        "desc": "Курсы, студии танцев, спортивные секции",
        "icon": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>',
        "emoji": "🎓",
        "active": False,
        "badge": "Скоро",
        "badge_class": "mt-dropdown-badge--soon",
    },
    {
        "id": "pets",
        "slug": "pets",
        "title": "Уход за животными",
        "desc": "Груминг-салоны, ветклиники, передержки",
        "icon": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="4" r="2"/><circle cx="18" cy="8" r="2"/><circle cx="4" cy="11" r="2"/><circle cx="7" cy="19" r="2"/><path d="M12 10a4 4 0 0 0-4 4c0 2.2 1.8 4 4 4s4-1.8 4-4a4 4 0 0 0-4-4z"/></svg>',
        "emoji": "🐾",
        "active": False,
        "badge": "Скоро",
        "badge_class": "mt-dropdown-badge--soon",
    },
    {
        "id": "repair",
        "slug": "repair",
        "title": "Ремонт и сервис",
        "desc": "Сервисные центры, ремонт техники, ателье",
        "icon": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
        "emoji": "🔧",
        "active": False,
        "badge": "Скоро",
        "badge_class": "mt-dropdown-badge--soon",
    },
]

def render_nav_html(active_item: str = "", asset_prefix: str = "") -> str:
    """Builds the single source of truth for navigation across all pages."""
    logo_path = f"{asset_prefix}assets/img/logo/molniya-logo-horizontal.svg" if asset_prefix else "/assets/img/logo/molniya-logo-horizontal.svg"

    # Build dropdown grid
    grid_items = []
    mobile_items = []
    for s in SECTORS:
        href = f"/{s['slug']}" if s['active'] else f"/{s['slug']}"
        active_cls = " mt-dropdown-card--active" if s["slug"] == active_item else ""
        badge_html = f'<span class="mt-dropdown-badge {s["badge_class"]}">{s["badge"]}</span>'

        grid_items.append(f'''              <a class="mt-dropdown-card{active_cls}" href="{href}" role="menuitem">
                <div class="mt-dropdown-icon">{s["icon"]}</div>
                <div class="mt-dropdown-info">
                  <div class="mt-dropdown-title">{html.escape(s["title"])} {badge_html}</div>
                  <div class="mt-dropdown-desc">{html.escape(s["desc"])}</div>
                </div>
              </a>''')

        m_highlight = " mt-mobile-sublink--highlight" if s["slug"] == active_item else ""
        mobile_items.append(f'''            <a class="mt-mobile-sublink{m_highlight}" href="{href}">
              <span class="mt-mobile-sublink-icon">{s["emoji"]}</span>
              <span class="mt-mobile-sublink-info">
                <strong>{html.escape(s["title"])}</strong>
                <small>{html.escape(s["desc"])}</small>
              </span>
            </a>''')

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
            <p class="mt-footer-legal">ИП Нестеренко Илья Александрович · ИНН 272198132745 · Санкт-Петербург</p>
          </div>
          <div class="mt-footer-links">
            <a class="mt-footer-link" href="https://t.me/molniya_tex" target="_blank" rel="noopener"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>Telegram-канал</a>
            <a class="mt-footer-link" href="/privacy.html">Конфиденциальность</a>
            <a class="mt-footer-link" href="/cookies.html">Cookies</a>
          </div>
        </div>
      </footer>'''


def build_auto_page() -> str:
    """Builds the complete auto landing page matching the exact design system."""
    nav_html = render_nav_html(active_item="auto", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")

    title = "Молния для автобизнеса — CRM и онлайн-запись для автомоек, детейлинга и СТО"
    description = "Специализированная CRM для автобизнеса: расписание боксов и постов, нормативы по классам авто, сдельная зарплата мастеров, фотоосмотр кузова и Telegram-запись."
    canonical = "https://molniya-tech.ru/auto"

    faq_items = [
        {
            "q": "Подходит ли Молния для небольшой мойки на 2–3 бокса?",
            "a": "Да. Молния отлично подходит как для компактных автомоек на 2 поста, так и для крупных детейлинг-центров и СТО с десятками постов и мастеров. Вы настраиваете количество рабочих мест и нормативы за 15 минут."
        },
        {
            "q": "Как система учитывает разницу во времени между седаном и крупным внедорожником?",
            "a": "В Молнии встроен классификатор автомобилей. Вы один раз привязываете время и цену к категории (седан, кроссовер, рамный джип, микроавтобус). При записи система автоматически резервирует нужное окно в расписании бокса."
        },
        {
            "q": "Можно ли начислять разный процент автомойщикам и детейлерам?",
            "a": "Да, в карточке сотрудника и услуги настраивается гибкая модель: процент от чека (например, мойка 30%, полировка 45%), фиксированная ставка за выход или за конкретную операцию. Баланс рассчитывается мгновенно."
        },
        {
            "q": "Как клиенты узнают о записи и готовности автомобиля?",
            "a": "Через автоматические сервисные сообщения в Telegram. Клиент получает подтверждение записи со ссылкой на заказ, напоминание за 2 часа до визита и оповещение «Ваш автомобиль готов к выдаче» в один клик мастера."
        },
        {
            "q": "Как работает фотоосмотр повреждений кузова?",
            "a": "Мастер открывает заказ-наряд на смартфоне или планшете перед заездом машины, делает несколько фото сколов или царапин и сохраняет в карточке заказа. Это надёжная защита от необоснованных претензий клиентов при выдаче."
        },
        {
            "q": "Как перенести базу клиентов из тетради или другой CRM?",
            "a": "Наша служба заботы бесплатно помогает импортировать базу клиентов, перечень услуг и историю визитов при подключении. Вы начинаете работу без пауз и потери постоянных клиентов."
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
            "name": "Молния — CRM для автобизнеса",
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
  <meta name="keywords" content="crm для автомойки, программа для детейлинга, crm для автобизнеса, расписание боксов, автосервис онлайн запись, учет мойщиков">
  <link rel="canonical" href="{canonical}">
  <meta name="theme-color" content="#FFFEFD">

  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="alternate icon" href="/favicon.ico">
  <link rel="apple-touch-icon" href="/assets/img/logo/icon-192.png">

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

  <link rel="preload" href="/fonts/unbounded-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20260928-2">
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
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/></svg>
            Для автобизнеса
          </div>

          <h1 class="mt-hero-title">
            Управляй боксами<br>и планируй прибыль
          </h1>

          <div class="mt-hero-bottom">
            <div class="mt-hero-intro">
              <p class="mt-hero-sub">Специализированная система для автомоек, детейлинг-студий, СТО и шиномонтажей. Учитывает габариты авто, посты, допуслуги и прозрачную сдельную оплату.</p>
              <a class="mt-btn mt-btn-hero" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
                Подключить автобизнес
              </a>
            </div>

            <ul class="mt-facets mt-facets--full" aria-label="Преимущества для автобизнеса">
              <li class="mt-facet">
                <span class="mt-facet-name">Боксы и посты</span>
                <span class="mt-facet-note">распределение по длине и типу авто</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Сдельная оплата</span>
                <span class="mt-facet-note">нормочасы и % от чека за смену</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name">Осмотр и дефекты</span>
                <span class="mt-facet-note">чек-лист и фотофиксация до заезда</span>
              </li>
              <li class="mt-facet">
                <span class="mt-facet-name mt-facet-name--soon">AI & Сезон</span>
                <span class="mt-facet-note">умный прогноз очередей и погоды</span>
              </li>
            </ul>
          </div>
        </div>

        <div id="product-preview" class="mt-hero-col mt-hero-col--media">
          <div class="mt-hero-media-motion">
            <a class="mt-tablet" href="https://rutube.ru/video/bf11679edec2bbe548a54f9adf6bc3ca/" target="_blank" rel="noopener" aria-label="Смотреть видео: работа расписания боксов в Молнии">
              <span class="mt-tablet-screen">
                <img class="mt-tablet-img" src="/assets/img/schedule.jpg" alt="Журнал записи автомойки и детейлинга с расписанием боксов" width="1710" height="983" fetchpriority="high">
                <span class="mt-tablet-play">
                  <svg width="26" height="26" viewBox="0 0 24 24" fill="#C6543B"><path d="M8 5v14l11-7z"></path></svg>
                </span>
              </span>
              <img class="mt-tablet-frame" src="/assets/img/ipad-mockup.svg?v=20260925-8" alt="" aria-hidden="true" width="1280" height="950" fetchpriority="high">
            </a>
            <p class="mt-hero-media-caption">Расписание боксов и контроль загрузки постов в реальном времени</p>
          </div>
        </div>

      </section>

      <!-- LIVE BAYS STATUS -->
      <section class="mt-section mt-reveal" data-screen-label="Загрузка боксов" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <div class="mt-eyebrow">Мониторинг комплекса</div>
          <h2 class="mt-section-title">Все посты и автомобили <span class="mt-overview-hook">как на ладони</span></h2>
          <p class="mt-section-sub">Администратор и мастера видят статус каждого бокса, закреплённого мастера, марку авто и сумму заказ-наряда в одну секунду.</p>
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
              <span>Комплекс «Премиум» + Воск</span>
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
              <span>Полировка фар + Керамика</span>
              <span class="mt-auto-price">14 500 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Пост 3 · СТО / Подъемник</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--done">Готово</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Geely Monjaro</div>
                <div class="mt-auto-car-tier">II класс · Кроссовер</div>
              </div>
              <span class="mt-dropdown-footer-icon">🔧</span>
            </div>
            <div class="mt-auto-service">
              <span>Замена масла + Колодки</span>
              <span class="mt-auto-price">7 800 ₽</span>
            </div>
          </div>

          <div class="mt-auto-bay">
            <div class="mt-auto-bay-head">
              <span class="mt-auto-bay-title">Пост 4 · Шиномонтаж</span>
              <span class="mt-auto-bay-status mt-auto-bay-status--wait">Ожидает заезда</span>
            </div>
            <div class="mt-auto-car">
              <div>
                <div class="mt-auto-car-name">Zeekr 001 (14:30)</div>
                <div class="mt-auto-car-tier">I класс · Седан/Лифтбек</div>
              </div>
              <span class="mt-dropdown-footer-icon">🛞</span>
            </div>
            <div class="mt-auto-service">
              <span>Сезонный шиномонтаж R21</span>
              <span class="mt-auto-price">5 200 ₽</span>
            </div>
          </div>
        </div>
      </section>

      <!-- AUTO OVERVIEW VALUE GRID -->
      <section class="mt-section mt-section--overview mt-reveal" data-screen-label="Функции для автобизнеса" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <h2 class="mt-section-title">Ведите автобизнес <span class="mt-overview-hook">от заезда до чистой прибыли</span></h2>
          <p class="mt-section-sub">Расписание постов, фотоосмотр, нормативы по классам авто и зарплаты сотрудников объединены в одной интуитивной системе.</p>
        </div>

        <div class="mt-overview-grid">
          <article class="mt-overview-card">
            <h3><span class="mt-overview-hook">Запись по боксам</span> и постам</h3>
            <p>Клиент выбирает удобное время и бокс: пост экспресс-мойки, сухой пост детейлинга или подъемник. Система учитывает габариты авто и исключает простой оборудования.</p>
            <div class="mt-overview-preview mt-overview-preview--schedule" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Расписание боксов</span><span>Сегодня</span></div>
              <div class="mt-overview-calendar"><span>09:00</span><div></div><span>10:00</span><div class="mt-overview-slot">Бокс 1 <small>BMW X5 · Комплекс</small></div><span>11:30</span><div class="mt-overview-slot mt-overview-slot--light">Бокс 2 <small>Porsche · Полировка</small></div></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3><span class="mt-overview-hook">Фотоосмотр кузова</span> до начала работ</h3>
            <p>Мастер за 60 секунд фиксирует состояние кузова и дисков со смартфона: сколы, вмятины, трещины. Акт сохраняется в заказе — защита от претензий при выдаче.</p>
            <div class="mt-overview-preview mt-overview-preview--process" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Чек-лист приёмки</span><span>Бокс 1</span></div>
              <div class="mt-overview-stages"><span>Осмотр</span><i></i><span>Мойка</span><i></i><span>Выдача</span></div>
              <div class="mt-overview-check">✓ <span>Фото кузова по кругу (4 фото)</span></div>
              <div class="mt-overview-check">✓ <span>Скол на капоте зафиксирован</span></div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Нормативы и цены <span class="mt-overview-hook">по классам авто</span></h3>
            <p>Молния автоматически пересчитывает стоимость и длительность услуги: седан (40 мин), SUV (55 мин), джип (70 мин). В часы пик и непогоду действуют гибкие сезонные тарифы.</p>
            <div class="mt-overview-preview mt-overview-preview--prices" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Прайс по классам</span><span>Мойка «Люкс»</span></div>
              <div class="mt-overview-price-row"><span>I класс (Седан)</span><strong>2 200 ₽ · 40 мин</strong></div>
              <div class="mt-overview-price-row"><span>II класс (Кроссовер)</span><strong>2 700 ₽ · 55 мин</strong></div>
              <div class="mt-overview-price-tag">Выходные · Часы пик · Праздники</div>
            </div>
          </article>

          <article class="mt-overview-card">
            <h3>Telegram-оповещение <span class="mt-overview-hook">«Автомобиль готов»</span></h3>
            <p>Клиент получает подтверждение записи, схему проезда к боксу и автоматическое уведомление в Telegram сразу, когда авто готово к выдаче. Меньше очередей в клиентской зоне.</p>
            <div class="mt-overview-preview mt-overview-preview--clients" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Статус готовности</span><span>Telegram</span></div>
              <div class="mt-overview-message">
                Ваш Porsche Macan готов к выдаче в Боксе №2. Сумма к оплате: 4 500 ₽.
                <span class="mt-overview-reaction">🚗</span>
              </div>
              <div class="mt-overview-client-row"><span>Клиентская база</span><strong>История визитов и ТО →</strong></div>
            </div>
          </article>

          <article class="mt-overview-card mt-overview-card--featured">
            <h3>Прозрачная сдельная <span class="mt-overview-hook">зарплата мастеров</span></h3>
            <p>Автоматическое начисление процента от чека или фиксированной ставки за каждую услугу сразу после выдачи авто. Мойщики видят свою выработку прямо на телефоне.</p>
            <div class="mt-overview-preview mt-overview-preview--metrics" aria-hidden="true">
              <div class="mt-overview-ui-head"><span>Выработка за смену</span><span>Смена №1</span></div>
              <div class="mt-overview-metrics"><span>Мойка<b>30%</b></span><span>Детейлинг<b>40%</b></span><span>К выплате<b>₽</b></span></div>
              <div class="mt-overview-chart"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            </div>
          </article>
        </div>

        <div class="mt-overview-action">
          <a class="mt-btn mt-btn-cta" href="https://t.me/molniya_tex" target="_blank" rel="noopener">Подключить автобизнес</a>
        </div>
      </section>

      <!-- AUTO JOURNEY -->
      <section class="mt-section mt-journey mt-reveal" data-screen-label="Путь визита авто" data-mt-reveal>
        <div class="mt-section-head mt-section-head--center">
          <div class="mt-eyebrow">Рабочий процесс</div>
          <h2 class="mt-section-title">Один заезд авто. <span class="mt-hero-accent">Полный контроль в Молнии.</span></h2>
          <p class="mt-section-sub">Посмотрите, как система автоматизирует обслуживание автомобиля от онлайн-записи до выдачи ключей и выплаты мастеру.</p>
        </div>

        <div class="mt-journey-example" aria-label="Пример прохождения записи">
          <span>Пример</span><strong>Комплексная мойка + Твёрдый воск</strong><span>Geely Monjaro · Бокс №1</span>
        </div>

        <div class="mt-journey-list">
          <article class="mt-journey-step">
            <div class="mt-journey-index">01</div>
            <div class="mt-journey-copy">
              <span class="mt-journey-actor">Клиент</span>
              <h3>Записывается онлайн и указывает класс авто</h3>
              <p>Выбирает марку, кузов и комплекс услуг на сайте или в Telegram. Молния сразу резервирует окно нужной длины (55 минут вместо 40) с учётом кроссовера.</p>
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
              <h3>Заезд в бокс и экспресс-осмотр кузова</h3>
              <p>При заезде мастер за 60 секунд фотографирует сколы на капоте и притёртость на диске. Чек-лист прикрепляется к электронному заказ-наряду.</p>
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
              <h3>Выполнение работ и допродажа в 1 тап</h3>
              <p>Мастер заметил битумные пятна на порогах и согласовал с клиентом удаление за 900 ₽ прямо в системе. Сумма заказа автоматически пересчиталась.</p>
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
              <h3>Оплата, выдача и прозрачный расчёт зарплаты</h3>
              <p>Клиент оплачивает заказ картой или переводом. Система сразу начисляет мастеру Александру 35% (1 365 ₽) на баланс смены. Никаких вечерних споров и ручных таблиц.</p>
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
            <div class="mt-case-tag">⚡ Кейс внедрения Молнии</div>
            <h2 class="mt-case-title">Детейлинг-студия «Вектор», 4 поста</h2>
            <blockquote class="mt-case-quote">
              «Раньше каждый вечер уходил час на сведение тетради с мойщиками, а по выходным была давка из-за джипов, которые не влезали по времени. В Молнии мы настроили нормативы по классам авто — расписание стало идеальным, а выручка выросла на треть.»
            </blockquote>
            <div class="mt-case-author">
              Алексей Смирнов <span>· Руководитель студии, Санкт-Петербург</span>
            </div>
          </div>
          <div class="mt-case-stats">
            <div class="mt-case-stat">
              <span class="mt-case-num">+35%</span>
              <span class="mt-case-label">Рост выручки за счёт ликвидации пустых окон</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">-86%</span>
              <span class="mt-case-label">Снижение неявок благодаря Telegram-напоминаниям</span>
            </div>
            <div class="mt-case-stat">
              <span class="mt-case-num">0 мин</span>
              <span class="mt-case-label">На вечерний подсчёт зарплат и выработки мастеров</span>
            </div>
          </div>
        </div>
      </section>

      <!-- AUTO FAQ -->
      <section id="faq" class="mt-section mt-reveal" data-screen-label="Вопросы и ответы" data-mt-reveal>
        <div class="mt-section-head">
          <div class="mt-eyebrow">Вопросы и ответы</div>
          <h2 class="mt-section-title">Часто задаваемые вопросы по автобизнесу</h2>
        </div>
        <div class="mt-before-start-grid">
          <article class="mt-before-start-highlight">
            <span>Подключение</span>
            <h3>Попробуйте Молнию для своего автобизнеса</h3>
            <p>Мы поможем бесплатно перенести вашу базу клиентов, настроить посты, классы авто и проценты мастеров. Оставьте заявку в нашем Telegram-канале.</p>
            <a href="https://t.me/molniya_tex" target="_blank" rel="noopener">Написать в Telegram-канал ↗</a>
          </article>
          <div class="mt-before-start-questions">
{faq_html}
          </div>
        </div>
        <p class="mt-before-start-privacy">Как мы обрабатываем данные — в <a href="/privacy.html">политике конфиденциальности</a>.</p>
      </section>

      <!-- FINAL CTA -->
      <section class="mt-section mt-section--final-cta mt-reveal" data-screen-label="Финальный CTA" data-mt-reveal>
        <div class="mt-final">
          <div class="mt-final-glow" aria-hidden="true"></div>
          <div class="mt-final-inner">
            <div class="mt-final-icon">
              <svg width="56" height="56" viewBox="0 0 34 34" fill="none"><circle cx="17" cy="17" r="15" stroke="url(#mtgrad)" stroke-width="1.2" opacity="0.45"></circle><ellipse cx="17" cy="17" rx="15" ry="5.5" stroke="url(#mtgrad)" stroke-width="1.2" opacity="0.65" transform="rotate(-28 17 17)"></ellipse><path d="M18.6 6.5 10.8 18.6H15.6L14 27.5 23.2 14.2H17.7Z" fill="url(#mtgrad)"></path></svg>
            </div>
            <h2 class="mt-final-title">Зарядите свой автобизнес <span class="mt-hero-accent">на полную мощность</span></h2>
            <p class="mt-final-sub">Порядок в расписании боксов, лояльные клиенты и прозрачные расчёты с мастерами. Подключайтесь к Молнии.</p>
            <div class="mt-final-actions">
              <a class="mt-btn mt-btn-cta" href="https://rutube.ru/video/bf11679edec2bbe548a54f9adf6bc3ca/" target="_blank" rel="noopener">Смотреть видео о Молнии ↗</a>
              <a class="mt-btn mt-btn-cta" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
                Подключить автобизнес
              </a>
            </div>
            <div class="mt-final-note">Новости об обновлениях и тарифах публикуем в Telegram-канале.</div>
          </div>
        </div>
      </section>

{footer_html}

    </div>

    <!-- cookie notice -->
    <div class="mt-cookie-banner" id="mt-cookie-banner" role="dialog" aria-live="polite">
      <p class="mt-cookie-text">
        Мы используем файлы cookie и Яндекс.Метрику для аналитики сайта.
        Продолжая пользоваться сайтом, вы соглашаетесь с этим —
        подробнее в <a href="/cookies.html" class="mt-link-accent">политике cookie</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
      Подписаться
    </a>

  </div>

  <script src="/script.js?v=20260928-2"></script>
</body>
</html>
'''
    return page_html


def sync_navigation_to_index():
    """Syncs the DRY nav into index.html."""
    content = INDEX_HTML.read_text(encoding="utf-8")
    nav_html = render_nav_html(active_item="", asset_prefix="")

    start_marker = "<!-- NAV -->"
    end_marker = "</nav>"
    if start_marker in content and end_marker in content:
        before = content.split(start_marker, 1)[0]
        after = content.split(end_marker, 1)[1]
        new_content = before + nav_html + after
        INDEX_HTML.write_text(new_content, encoding="utf-8")
        print("Updated navigation in index.html")


def sync_navigation_to_blog():
    """Syncs the DRY nav into blog/index.html."""
    content = BLOG_INDEX_HTML.read_text(encoding="utf-8")
    nav_html = render_nav_html(active_item="blog", asset_prefix="../")

    start_marker = "<!-- NAV -->"
    end_marker = "</nav>"
    if start_marker in content and end_marker in content:
        before = content.split(start_marker, 1)[0]
        after = content.split(end_marker, 1)[1]
        new_content = before + nav_html + after
        BLOG_INDEX_HTML.write_text(new_content, encoding="utf-8")
        print("Updated navigation in blog/index.html")


def sync_sitemap():
    """Ensures /auto is in sitemap.xml."""
    content = SITEMAP_XML.read_text(encoding="utf-8")
    if "https://molniya-tech.ru/auto" not in content:
        url_entry = """  <url>
    <loc>https://molniya-tech.ru/auto</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
"""
        content = content.replace("</urlset>", url_entry + "</urlset>")
        SITEMAP_XML.write_text(content, encoding="utf-8")
        print("Added /auto to sitemap.xml")


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

  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="alternate icon" href="/favicon.ico">
  <link rel="apple-touch-icon" href="/assets/img/logo/icon-192.png">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Молния Тех">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="404 — Страница не найдена — Молния Тех">
  <meta property="og:description" content="Запрошенная страница не найдена. Перейдите на главную страницу Молнии.">
  <meta property="og:image" content="https://molniya-tech.ru/assets/img/schedule.jpg">

  <link rel="preload" href="/fonts/unbounded-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20260929-2">
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

  <script src="/script.js?v=20260928-2"></script>
</body>
</html>
"""


def main():
    print("Building sector landing page: /auto...")
    auto_html = build_auto_page()
    (ROOT_DIR / "auto.html").write_text(auto_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'auto.html'}")

    print("Building 404 error page: /404.html...")
    not_found_html = build_404_page()
    (ROOT_DIR / "404.html").write_text(not_found_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / '404.html'}")

    sync_navigation_to_index()
    sync_navigation_to_blog()
    sync_sitemap()
    print("DRY build complete!")


if __name__ == "__main__":
    main()

