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
        grid_items.append(f'''              <a class="mt-dropdown-card{active_cls}" href="{href}" role="menuitem">
                <div class="mt-dropdown-icon">{s["icon"]}</div>
                <div class="mt-dropdown-info">
                  <div class="mt-dropdown-title">{html.escape(s["title"])}</div>
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
            <p class="mt-footer-legal">ООО «МОЛНИЯ ТЕХ» · ИНН 7806637461 · ОГРН 1267800068458 · Санкт-Петербург</p>
          </div>
          <div class="mt-footer-links">
            <a class="mt-footer-link" href="https://t.me/molniya_tex" target="_blank" rel="noopener"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>Telegram-канал</a>
            <a class="mt-footer-link" href="/privacy">Конфиденциальность</a>
            <a class="mt-footer-link" href="/cookies">Cookies</a>
            <a class="mt-footer-link" href="/requisites">Реквизиты</a>
          </div>
        </div>
      </footer>'''


def build_auto_page() -> str:
    """Builds the complete auto landing page matching the exact design system."""
    nav_html = render_nav_html(active_item="auto", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")

    title = "CRM для автомойки, детейлинга и автосервиса — программа учета и онлайн-записи Молния"
    description = "Программа и CRM для автомойки, детейлинга, СТО и шиномонтажа. Онлайн-запись 24/7, расписание боксов, электронные заказ-наряды с фотоосмотром кузова, учёт по классам авто и расчёт зарплаты мастеров."
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
            "name": "Молния — CRM для автомойки, детейлинга и автосервиса",
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
  <meta name="keywords" content="crm для автомойки, программа для автомойки, crm для автосервиса, программа для автосервиса, crm для детейлинга, программа для детейлинга, онлайн запись на автомойку, электронный заказ наряд, расписание боксов, учет на автомойке, программа для шиномонтажа, расчет зарплаты мойщиков">
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
  <link rel="stylesheet" href="/styles.css?v=20261001-cards">
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
              <a class="mt-btn mt-btn-hero" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
                Подключить автобизнес
              </a>
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
          <a class="mt-btn mt-btn-cta" href="https://t.me/molniya_tex" target="_blank" rel="noopener">Подключить автобизнес</a>
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

      <!-- FINAL CTA -->
      <section class="mt-section mt-section--final-cta mt-reveal" data-screen-label="Финальный CTA" data-mt-reveal>
        <div class="mt-final">
          <div class="mt-final-glow" aria-hidden="true"></div>
          <div class="mt-final-inner">
            <div class="mt-final-icon">
              <svg width="56" height="56" viewBox="0 0 34 34" fill="none"><circle cx="17" cy="17" r="15" stroke="url(#mtgrad)" stroke-width="1.2" opacity="0.45"></circle><ellipse cx="17" cy="17" rx="15" ry="5.5" stroke="url(#mtgrad)" stroke-width="1.2" opacity="0.65" transform="rotate(-28 17 17)"></ellipse><path d="M18.6 6.5 10.8 18.6H15.6L14 27.5 23.2 14.2H17.7Z" fill="url(#mtgrad)"></path></svg>
            </div>
            <h2 class="mt-final-title">Автоматизируйте свой автобизнес <span class="mt-hero-accent">на полную мощность</span></h2>
            <p class="mt-final-sub">Управляйте расписанием боксов, исключите простой постов и забудьте о ручных таблицах зарплат. Подключайтесь к CRM Молния уже сегодня.</p>
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
        подробнее в <a href="/cookies" class="mt-link-accent">политике cookie</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
      Подписаться
    </a>

  </div>

  <script src="/script.js?v=20260930-req2"></script>
</body>
</html>
'''
    return page_html


def build_beauty_page() -> str:
    """Builds the complete beauty salon landing page matching the exact design system."""
    nav_html = render_nav_html(active_item="beauty", asset_prefix="")
    footer_html = render_footer_html(asset_prefix="")

    title = "CRM для салона красоты, барбершопа и студии маникюра — программа учета и онлайн-записи Молния"
    description = "Программа и CRM для салона красоты, барбершопа и студии маникюра. Онлайн-запись 24/7, электронный журнал мастеров, расчёт зарплат, списание красителей по техкартам и Telegram-напоминания."
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
            "name": "Молния — CRM для салона красоты, барбершопа и студии маникюра",
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
  <meta name="keywords" content="crm для салона красоты, программа для салона красоты, crm для барбершопа, онлайн запись в салон красоты, электронный журнал записи, программа для студии маникюра, расчет зарплаты мастеров салона, учет материалов в салоне красоты, журнал мастеров, расписание мастеров">
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
  <link rel="stylesheet" href="/styles.css?v=20261001-cards">
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
              <a class="mt-btn mt-btn-hero" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
                Подключить салон красоты
              </a>
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
          <a class="mt-btn mt-btn-cta" href="https://t.me/molniya_tex" target="_blank" rel="noopener">Подключить салон красоты</a>
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

      <!-- FINAL CTA -->
      <section class="mt-section mt-section--final-cta mt-reveal" data-screen-label="Финальный CTA" data-mt-reveal>
        <div class="mt-final">
          <div class="mt-final-glow" aria-hidden="true"></div>
          <div class="mt-final-inner">
            <div class="mt-final-icon">
              <svg width="56" height="56" viewBox="0 0 34 34" fill="none"><circle cx="17" cy="17" r="15" stroke="url(#mtgrad)" stroke-width="1.2" opacity="0.45"></circle><ellipse cx="17" cy="17" rx="15" ry="5.5" stroke="url(#mtgrad)" stroke-width="1.2" opacity="0.65" transform="rotate(-28 17 17)"></ellipse><path d="M18.6 6.5 10.8 18.6H15.6L14 27.5 23.2 14.2H17.7Z" fill="url(#mtgrad)"></path></svg>
            </div>
            <h2 class="mt-final-title">Наведите идеальный порядок <span class="mt-hero-accent">в своём салоне красоты</span></h2>
            <p class="mt-final-sub">Заполняйте расписание без окон, удерживайте клиентов и забудьте о ручных расчетах зарплат. Подключайтесь к CRM Молния уже сегодня.</p>
            <div class="mt-final-actions">
              <a class="mt-btn mt-btn-cta" href="https://rutube.ru/video/bf11679edec2bbe548a54f9adf6bc3ca/" target="_blank" rel="noopener">Смотреть видео о Молнии ↗</a>
              <a class="mt-btn mt-btn-cta" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
                Подключить салон красоты
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
        подробнее в <a href="/cookies" class="mt-link-accent">политике cookie</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
      Подписаться
    </a>

  </div>

  <script src="/script.js?v=20260930-req2"></script>
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
  <link rel="stylesheet" href="/styles.css?v=20261001-cards">
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

  <script src="/script.js?v=20260930-req"></script>
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
  <link rel="stylesheet" href="/styles.css?v=20261001-cards">
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
        подробнее в <a href="/cookies" class="mt-link-accent">политике cookie</a>.
      </p>
      <button class="mt-btn mt-cookie-accept" type="button" id="mt-cookie-accept">Понятно</button>
    </div>

    <!-- sticky floating CTA -->
    <a class="mt-btn mt-btn-sticky" href="https://t.me/molniya_tex" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M21.94 4.3 2.9 11.64c-1.07.43-1.06 1.03-.2 1.3l4.88 1.52 1.88 5.78c.23.63.41.88.86.88.45 0 .64-.2.88-.5l2.35-2.28 4.9 3.62c.9.5 1.55.24 1.78-.83l3.2-15.1c.33-1.31-.5-1.9-1.37-1.5z"></path></svg>
      Подписаться
    </a>

  </div>

  <script src="/script.js?v=20260930-req2"></script>
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

    print("Building 404 error page: /404.html...")
    not_found_html = build_404_page()
    (ROOT_DIR / "404.html").write_text(not_found_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / '404.html'}")

    print("Building requisites page: /requisites.html...")
    req_html = build_requisites_page()
    (ROOT_DIR / "requisites.html").write_text(req_html, encoding="utf-8")
    print(f"Generated {ROOT_DIR / 'requisites.html'}")

    sync_navigation_to_index()
    sync_navigation_to_blog()
    sync_sitemap()
    print("DRY build complete!")


if __name__ == "__main__":
    main()


