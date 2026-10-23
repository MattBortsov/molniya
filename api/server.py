"""Small same-origin proxy for the Molniya industry-fit decision form."""

from __future__ import annotations

import json
import hashlib
import hmac
import os
import re
import sqlite3
import threading
import time
from collections import defaultdict, deque
from html import escape
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import requests

if __package__:
    from . import blog as blog_store, leads as lead_store
else:
    import blog as blog_store
    import leads as lead_store


OPENROUTER_URL = "https://openrouter.ai/api/alpha/decisions"
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "typesafe/jev-1.13")
MAX_BODY_BYTES = 4_096
MAX_WEBHOOK_BYTES = 2_000_000
MAX_BUSINESS_LENGTH = 240
MAX_LEAD_BODY_BYTES = 2_048
TELEGRAM_LEADS_CHAT_ID = "-1003993624474"
RATE_WINDOW_SECONDS = 60
RATE_REQUESTS = 8

_calendar_cache: dict[int, str] = {
    2025: "11111111001100000110000011000001100000110000011000001100000110000211000001100000110000011000001100000110000011000001100211110001111000001100000110000011000001100211110000011000001100000110000011000001100000110000011000001100000110000011000001100000110000011000001100000110000011000001100000110000011000002111000110000011000001100000110000011000001100000110000011001",
    2026: "11111111111000001100000110000011000001100000110000011100001100000111000011000001100000110000011000001100000110000011000211100002111000011000001100000110000011000211100000110000011000001100000110000011000001100000110000011000001100000110000011000001100000110000011000001100000110000011000001100000110000011021001100000110000011000001100000110000011000001100000110001",
    2027: "11111111110000011000001100000110000011000001100000211100011000001110000110000011000001100000110000011000001100000110000211100001110000110000011000001100000110000211100001100000110000011000001100000110000011000001100000110000011000001100000110000011000001100000110000011000001100000110000011000001100000110021111000001100000110000011000001100000110000011000001100001",
}

_inn_cache: dict[str, dict[str, Any]] = {}
_inn_cache_lock = threading.Lock()


def fetch_counterparty_data(query: str) -> dict[str, Any]:
    """Queries official FNS Russia (EGRUL/EGRIP) and KontragentPro to retrieve company details."""
    cleaned = re.sub(r"\s+", "", query.strip())
    if not cleaned.isdigit() or len(cleaned) not in (10, 12, 13, 15):
        raise ValueError("Введите корректный ИНН (10 или 12 цифр) или ОГРН (13 или 15 цифр)")

    with _inn_cache_lock:
        if cleaned in _inn_cache:
            return _inn_cache[cleaned]

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
    })

    try:
        p = session.post("https://egrul.nalog.ru/", data={"query": cleaned}, timeout=7)
        if p.status_code != 200:
            raise RuntimeError("Сервис ФНС временно недоступен")
        t = p.json().get("t")
        if not t:
            raise RuntimeError("ФНС не вернула токен поиска")

        r_search = session.get(f"https://egrul.nalog.ru/search-result/{t}", timeout=7)
        if r_search.status_code != 200:
            raise RuntimeError("Ошибка получения ответа из ФНС")

        rows = r_search.json().get("rows", [])
        if not rows:
            raise LookupError("Контрагент с указанным ИНН или ОГРН не найден в реестре ФНС")
    except (requests.RequestException, ValueError, KeyError) as exc:
        if isinstance(exc, (LookupError, ValueError)):
            raise
        raise RuntimeError(f"Ошибка соединения с ФНС: {exc}")

    row = rows[0]
    entity_type = row.get("k", "ul")
    inn = row.get("i", cleaned)
    ogrn = row.get("o", "")
    kpp = row.get("p", "")
    reg_date = row.get("r", "")
    term_date = row.get("e", None)
    region = row.get("rn", "")
    director = row.get("g", "")
    pdf_token = row.get("t", "")

    if entity_type == "fl":
        name_short = f"ИП {row.get('n', '')}"
        name_full = f"Индивидуальный предприниматель {row.get('n', '')}"
        status_text = "Деятельность прекращена" if term_date else "Действующий предприниматель"
    else:
        name_short = row.get("c") or row.get("n", "")
        name_full = row.get("n", "")
        status_text = "Ликвидирована" if term_date else "Действующая организация"

    status = "liquidated" if term_date else "active"
    address = ""
    okved = ""
    okved_name = ""
    risk = {
        "is_bankrupt": False,
        "is_sanctioned": False,
        "is_foreign_agent": False,
        "inspections_count": 0,
    }

    if entity_type == "ul" and len(inn) == 10:
        try:
            kp_resp = session.get(f"https://kontragentpro.ru/api/v2/companies/{inn}", timeout=6)
            if kp_resp.status_code == 200:
                kp_data = kp_resp.json()
                address = kp_data.get("address") or address
                okved = kp_data.get("okved") or okved
                okved_name = kp_data.get("okved_name") or okved_name
                if kp_data.get("director") and isinstance(kp_data["director"], dict):
                    director = kp_data["director"].get("fio") or director
                if kp_data.get("risk") and isinstance(kp_data["risk"], dict):
                    risk = kp_data["risk"]
                if kp_data.get("status") == "liquidated":
                    status = "liquidated"
                    status_text = "Ликвидирована"
        except Exception:
            pass

    if pdf_token:
        try:
            session.get(f"https://egrul.nalog.ru/vyp-request/{pdf_token}", timeout=3)
        except Exception:
            pass

    result = {
        "type": entity_type,
        "inn": inn,
        "kpp": kpp,
        "ogrn": ogrn,
        "name_short": name_short,
        "name_full": name_full,
        "status": status,
        "status_text": status_text,
        "reg_date": reg_date,
        "term_date": term_date,
        "region": region,
        "address": address,
        "director": director,
        "okved": okved,
        "okved_name": okved_name,
        "risk": risk,
        "pdf_token": pdf_token,
    }

    with _inn_cache_lock:
        _inn_cache[cleaned] = result
        if inn:
            _inn_cache[inn] = result
        if ogrn:
            _inn_cache[ogrn] = result

    return result


RUSSIAN_CITIES: list[dict[str, Any]] = [
    {"slug": "msk", "name": "Москва", "lat": 55.7558, "lon": 37.6176, "region": "Центральный ФО"},
    {"slug": "spb", "name": "Санкт-Петербург", "lat": 59.9343, "lon": 30.3351, "region": "Северо-Западный ФО"},
    {"slug": "kazan", "name": "Казань", "lat": 55.7961, "lon": 49.1064, "region": "Татарстан"},
    {"slug": "ekb", "name": "Екатеринбург", "lat": 56.8389, "lon": 60.6057, "region": "Урал"},
    {"slug": "nsk", "name": "Новосибирск", "lat": 55.0084, "lon": 82.9357, "region": "Сибирь"},
    {"slug": "nn", "name": "Нижний Новгород", "lat": 56.3269, "lon": 44.0059, "region": "Приволжский ФО"},
    {"slug": "krr", "name": "Краснодар", "lat": 45.0355, "lon": 38.9754, "region": "Южный ФО"},
    {"slug": "samara", "name": "Самара", "lat": 53.1959, "lon": 50.1002, "region": "Поволжье"},
    {"slug": "ufa", "name": "Уфа", "lat": 54.7388, "lon": 55.9721, "region": "Башкортостан"},
    {"slug": "rostov", "name": "Ростов-на-Дону", "lat": 47.2225, "lon": 39.7187, "region": "Южный ФО"},
    {"slug": "chelyabinsk", "name": "Челябинск", "lat": 55.1644, "lon": 61.4368, "region": "Южный Урал"},
    {"slug": "krasnoyarsk", "name": "Красноярск", "lat": 56.0153, "lon": 92.8932, "region": "Восточная Сибирь"},
    {"slug": "voronezh", "name": "Воронеж", "lat": 51.6720, "lon": 39.1843, "region": "Черноземье"},
    {"slug": "perm", "name": "Пермь", "lat": 58.0105, "lon": 56.2502, "region": "Предуралье"},
    {"slug": "volgograd", "name": "Волгоград", "lat": 48.7080, "lon": 44.5133, "region": "Нижнее Поволжье"},
    {"slug": "saratov", "name": "Саратов", "lat": 51.5336, "lon": 46.0343, "region": "Поволжье"},
    {"slug": "tyumen", "name": "Тюмень", "lat": 57.1530, "lon": 65.5343, "region": "Западная Сибирь"},
    {"slug": "tula", "name": "Тула", "lat": 54.1931, "lon": 37.6173, "region": "Центральный ФО"},
    {"slug": "sochi", "name": "Сочи", "lat": 43.5855, "lon": 39.7231, "region": "Черноморское побережье"},
    {"slug": "vladivostok", "name": "Владивосток", "lat": 43.1198, "lon": 131.8869, "region": "Дальний Восток"},
]

CITIES_BY_SLUG: dict[str, dict[str, Any]] = {c["slug"]: c for c in RUSSIAN_CITIES}

WMO_DESCRIPTIONS: dict[int, tuple[str, str]] = {
    0: ("Ясно", "sun"),
    1: ("Преимущественно ясно", "sun-cloud"),
    2: ("Переменная облачность", "cloud-sun"),
    3: ("Пасмурно", "cloud"),
    45: ("Туман", "fog"),
    48: ("Изморозь", "fog"),
    51: ("Небольшая морось", "drizzle"),
    53: ("Морось", "drizzle"),
    55: ("Плотная морось", "drizzle"),
    56: ("Ледяная морось", "drizzle"),
    57: ("Сильная ледяная морось", "drizzle"),
    61: ("Небольшой дождь", "rain"),
    63: ("Умеренный дождь", "rain"),
    65: ("Сильный дождь", "heavy-rain"),
    66: ("Ледяной дождь", "heavy-rain"),
    67: ("Сильный ледяной дождь", "heavy-rain"),
    71: ("Небольшой снегопад", "snow"),
    73: ("Снегопад", "snow"),
    75: ("Сильный снегопад", "heavy-snow"),
    77: ("Снежные зерна", "snow"),
    80: ("Кратковременный дождь", "rain"),
    81: ("Ливень", "heavy-rain"),
    82: ("Шквальный ливень", "heavy-rain"),
    85: ("Снегопад", "snow"),
    86: ("Сильный снегопад", "heavy-snow"),
    95: ("Гроза", "thunder"),
    96: ("Гроза с градом", "thunder"),
    99: ("Сильная гроза с градом", "thunder"),
}

_weather_cache: dict[str, tuple[float, dict[str, Any]]] = {}
_weather_cache_lock = threading.Lock()
WEATHER_CACHE_TTL = 900  # 15 minutes


def compute_wash_index(forecast: dict[str, Any], city_name: str, city_slug: str) -> dict[str, Any]:
    daily = forecast.get("daily", {})
    times = daily.get("time", [])
    if not times:
        raise ValueError("Нет данных прогноза")

    probs = daily.get("precipitation_probability_max", [0] * len(times))
    sums = daily.get("precipitation_sum", [0.0] * len(times))
    codes = daily.get("weathercode", [0] * len(times))
    t_max = daily.get("temperature_2m_max", [15.0] * len(times))
    t_min = daily.get("temperature_2m_min", [5.0] * len(times))
    current_weather = forecast.get("current_weather", {})
    curr_temp = round(current_weather.get("temperature", t_max[0] if t_max else 15.0))

    p0 = probs[0] if len(probs) > 0 else 0
    s0 = sums[0] if len(sums) > 0 else 0.0
    p1 = probs[1] if len(probs) > 1 else p0
    s1 = sums[1] if len(sums) > 1 else s0
    p2 = probs[2] if len(probs) > 2 else p1
    s2 = sums[2] if len(sums) > 2 else s1

    precip_penalty = (p0 * 0.45) + (p1 * 0.35) + (p2 * 0.15)
    precip_penalty += min(s0 * 6.0, 25.0) + min(s1 * 4.0, 15.0) + min(s2 * 2.0, 10.0)

    temp_penalty = 0.0
    is_slush = False
    if (t_min[0] < 0 and t_max[0] > 0) or (len(t_min) > 1 and t_min[1] < 0 and t_max[1] > 0):
        temp_penalty += 14.0
        is_slush = True

    if t_max[0] < -15:
        temp_penalty += 6.0

    raw_score = 100.0 - precip_penalty - temp_penalty
    score = int(round(max(5.0, min(100.0, raw_score))))

    if score >= 80:
        status = "perfect"
        verdict = "Идеально! Мой на все деньги"
        tagline = "Впереди сухие чистые дни. Машина будет сиять и радовать глаз."
        image = "/assets/img/carwash/wash-perfect.webp"
        badge_text = "Зеленый свет"
        badge_color = "#2E7D32"
        badge_bg = "rgba(46, 125, 50, 0.12)"
        days_clean_estimate = "4–6 дней чистоты"
        advice = "Отличное время для комплексной мойки, воска или детейлинга — результат продержится долго!"
    elif score >= 60:
        status = "good"
        verdict = "Смело на мойку"
        tagline = "Погода стабильная, легкая пыль не помеха. Отличный момент сбить дорожный налет."
        image = "/assets/img/carwash/wash-good.webp"
        badge_text = "Благоприятно"
        badge_color = "#1565C0"
        badge_bg = "rgba(21, 101, 192, 0.12)"
        days_clean_estimate = "2–3 дня чистоты"
        advice = "Кузов быстро сохнет, риск осадков низкий. Экспресс или кузов + коврики окупятся с лихвой."
    elif score >= 35:
        status = "risky"
        verdict = "Рискованно: спонсор чистых луж"
        tagline = "Высокая влажность или скорый дождь/снег. Чистым авто пробудет считанные часы."
        image = "/assets/img/carwash/wash-risky.webp"
        badge_text = "50 / 50"
        badge_color = "#E65100"
        badge_bg = "rgba(230, 81, 0, 0.12)"
        days_clean_estimate = "Меньше 24 часов"
        advice = "Если авто сильно загрязнено — сделайте быструю техническую сбивку грязи за 150 ₽. Дорогие полировки отложите."
    else:
        status = "disaster"
        verdict = "Остановись! Танки грязи не боятся"
        tagline = "Ливни, снегопад или слякоть с реагентами. Деньги на ветер — лучше переждать непогоду."
        image = "/assets/img/carwash/wash-disaster.webp"
        badge_text = "Не рекомендуем"
        badge_color = "#C62828"
        badge_bg = "rgba(198, 40, 40, 0.12)"
        days_clean_estimate = "До первой лужи (20 минут)"
        advice = "Протрите только стекла, зеркала, оптику и номерные знаки для безопасности. Полноценную мойку отложите до ясных дней."

    if is_slush:
        road_condition = "Слякоть и дорожные реагенты"
    elif s0 > 3.0 or p0 > 70:
        road_condition = "Мокрый асфальт, лужи и взвесь"
    elif s0 > 0.5 or p0 > 40:
        road_condition = "Влажное дорожное полотно"
    else:
        road_condition = "Сухой чистый асфальт"

    if p0 < 20 and s0 < 0.2:
        precip_risk = "Минимальный"
    elif p0 < 50 and s0 < 2.0:
        precip_risk = "Умеренный"
    elif p0 < 75:
        precip_risk = "Высокий"
    else:
        precip_risk = "Штормовой / Непрерывный"

    weekdays_ru = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    days_forecast = []
    from datetime import date
    for i in range(min(5, len(times))):
        d_str = times[i]
        d_parts = d_str.split("-")
        try:
            d_obj = date(int(d_parts[0]), int(d_parts[1]), int(d_parts[2]))
            w_idx = d_obj.weekday()
            day_name = "Сегодня" if i == 0 else ("Завтра" if i == 1 else weekdays_ru[w_idx])
            date_label = f"{d_obj.day:02d}.{d_obj.month:02d}"
        except Exception:
            day_name = f"День {i+1}"
            date_label = d_str

        code = codes[i] if i < len(codes) else 0
        desc, icon = WMO_DESCRIPTIONS.get(code, ("Облачно", "cloud"))
        prob = probs[i] if i < len(probs) else 0
        p_sum = sums[i] if i < len(sums) else 0.0
        t_hi = round(t_max[i]) if i < len(t_max) else 0
        t_lo = round(t_min[i]) if i < len(t_min) else 0

        day_raw = 100.0 - (prob * 0.7) - min(p_sum * 10.0, 30.0)
        if t_lo < 0 and t_hi > 0:
            day_raw -= 15.0
        day_score = int(round(max(5.0, min(100.0, day_raw))))

        days_forecast.append({
            "date": d_str,
            "date_label": date_label,
            "day_name": day_name,
            "temp_max": t_hi,
            "temp_min": t_lo,
            "precip_prob": prob,
            "precip_sum": round(p_sum, 1),
            "weather_code": code,
            "weather_desc": desc,
            "weather_icon": icon,
            "day_score": day_score,
        })

    return {
        "city_slug": city_slug,
        "city_name": city_name,
        "score": score,
        "status": status,
        "verdict": verdict,
        "tagline": tagline,
        "image": image,
        "badge_text": badge_text,
        "badge_color": badge_color,
        "badge_bg": badge_bg,
        "days_clean_estimate": days_clean_estimate,
        "advice": advice,
        "road_condition": road_condition,
        "precip_risk": precip_risk,
        "current_temp": curr_temp,
        "temp_min": round(t_min[0]) if t_min else curr_temp,
        "temp_max": round(t_max[0]) if t_max else curr_temp,
        "precip_prob_today": p0,
        "precip_sum_today": round(s0, 1),
        "days": days_forecast,
        "updated_at": int(time.time()),
    }


def build_fallback_forecast(lat: float, lon: float) -> dict[str, Any]:
    from datetime import date, timedelta
    today = date.today()
    times = [(today + timedelta(days=i)).isoformat() for i in range(5)]
    # Lat-based heuristic for realistic temperatures
    base_t = round(12.0 - (lat - 45.0) * 0.8)
    return {
        "daily": {
            "time": times,
            "weathercode": [1, 2, 0, 61, 2],
            "temperature_2m_max": [base_t + 2, base_t + 3, base_t + 1, base_t, base_t + 2],
            "temperature_2m_min": [max(0, base_t - 4), max(0, base_t - 3), max(0, base_t - 5), max(0, base_t - 4), max(0, base_t - 3)],
            "precipitation_sum": [0.0, 0.1, 0.0, 2.5, 0.2],
            "precipitation_probability_max": [10, 20, 5, 70, 15],
            "windspeed_10m_max": [10.0, 11.0, 8.0, 15.0, 9.0],
        },
        "current_weather": {
            "temperature": float(base_t),
            "weathercode": 1,
        },
    }


def fetch_weather_data(lat: float, lon: float, city_name: str, city_slug: str) -> dict[str, Any]:
    cache_key = f"{round(lat, 2)}:{round(lon, 2)}"
    now = time.time()
    with _weather_cache_lock:
        if cache_key in _weather_cache:
            ts, cached_result = _weather_cache[cache_key]
            if now - ts < WEATHER_CACHE_TTL:
                res = dict(cached_result)
                res["city_name"] = city_name
                res["city_slug"] = city_slug
                return res

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat:.4f}&longitude={lon:.4f}&"
        f"daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,windspeed_10m_max&"
        f"current_weather=true&timezone=auto"
    )

    proxy_url = (
        os.getenv("WEATHER_PROXY_URL", "").strip()
        or os.getenv("OPENROUTER_PROXY_URL", "").strip()
        or os.getenv("TELEGRAM_PROXY_URL", "").strip()
    )
    if proxy_url.startswith("socks5://"):
        proxy_url = "socks5h://" + proxy_url.removeprefix("socks5://")
    proxies = {"https": proxy_url, "http": proxy_url} if proxy_url else None

    try:
        resp = requests.get(url, timeout=7, proxies=proxies, headers={"User-Agent": "MolniyaCarwashWeather/1.0"})
        if resp.status_code != 200:
            raise RuntimeError(f"Open-Meteo returned status {resp.status_code}")
        raw_json = resp.json()
    except Exception:
        with _weather_cache_lock:
            if cache_key in _weather_cache:
                _, cached_result = _weather_cache[cache_key]
                res = dict(cached_result)
                res["city_name"] = city_name
                res["city_slug"] = city_slug
                return res
        raw_json = build_fallback_forecast(lat, lon)

    result = compute_wash_index(raw_json, city_name, city_slug)
    with _weather_cache_lock:
        _weather_cache[cache_key] = (now, result)
    return result


_requests_by_ip: dict[str, deque[float]] = defaultdict(deque)
_rate_lock = threading.Lock()


def build_decision_request(business: str) -> dict[str, Any]:
    """Build a typed Jev choice request. User text remains state, never instructions."""
    return {
        "model": OPENROUTER_MODEL,
        "state": business,
        "questions": {
            "fit": {
                "type": "choice",
                "instructions": (
                    "Определи, насколько Молния подходит организации из описания. "
                    "Молния управляет онлайн-записью, расписанием сотрудников или рабочих мест, "
                    "услугами и ценами, этапами выполнения, клиентской базой, филиалами, "
                    "аналитикой и расчётом зарплаты."
                ),
                "criteria": {
                    "fit": (
                        "Организация оказывает услуги клиентам, работает по записи или расписанию "
                        "и управляет сотрудниками, рабочими местами либо этапами выполнения услуг."
                    ),
                    "clarify": (
                        "Организация может оказывать услуги, но в описании недостаточно информации "
                        "о записи, расписании, ресурсах или процессе обслуживания."
                    ),
                    "not_fit": (
                        "Основная деятельность не связана с оказанием услуг клиентам по записи, "
                        "расписанию или управляемому процессу выполнения."
                    ),
                },
            }
        },
    }


def format_public_result(choice: str, confidence: float) -> dict[str, Any]:
    """Turn Jev's typed answer into deterministic user-facing copy."""
    if confidence < 0.58 or choice == "clarify":
        return {
            "status": "clarify",
            "title": "Похоже, Молния может подойти",
            "message": (
                "Нужно чуть больше деталей о записи клиентов, расписании команды "
                "или рабочих местах. Мы быстро разберём ваш сценарий на консультации."
            ),
            "confidence": round(confidence, 3),
        }
    if choice == "fit":
        return {
            "status": "fit",
            "title": "Да, Молния подходит вашей сфере",
            "message": (
                "Можно связать запись, расписание, услуги, сотрудников, клиентов "
                "и финансовые показатели в одном рабочем процессе."
            ),
            "confidence": round(confidence, 3),
        }
    return {
        "status": "not_fit",
        "title": "Нужна короткая консультация",
        "message": (
            "Описанный сценарий не похож на основной формат Молнии, но мы проверим, "
            "можно ли адаптировать систему под вашу работу."
        ),
        "confidence": round(confidence, 3),
    }


def call_jev(business: str) -> dict[str, Any]:
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not configured")

    proxy_url = os.getenv("OPENROUTER_PROXY_URL", "").strip()
    if proxy_url.startswith("socks5://"):
        proxy_url = "socks5h://" + proxy_url.removeprefix("socks5://")
    proxies = {"https": proxy_url} if proxy_url else None

    with requests.Session() as session:
        session.trust_env = False
        response = session.post(
            OPENROUTER_URL,
            json=build_decision_request(business),
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://molniya-tech.ru",
                "X-OpenRouter-Title": "Molniya Tech",
            },
            proxies=proxies,
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()

    answer = payload.get("answers", {}).get("fit", {})
    choice = answer.get("choice")
    confidence = answer.get("confidence")
    if choice not in {"fit", "clarify", "not_fit"} or not isinstance(confidence, (int, float)):
        raise ValueError("Unexpected Jev response")
    return format_public_result(choice, float(confidence))


def rate_limit_allows(ip_address: str, now: float | None = None) -> bool:
    current = now if now is not None else time.monotonic()
    with _rate_lock:
        bucket = _requests_by_ip[ip_address]
        cutoff = current - RATE_WINDOW_SECONDS
        while bucket and bucket[0] <= cutoff:
            bucket.popleft()
        if len(bucket) >= RATE_REQUESTS:
            return False
        bucket.append(current)
        return True


def validate_lead(payload: Any) -> dict[str, str]:
    """Accept only the three contact fields needed to reply to an applicant."""
    if not isinstance(payload, dict) or payload.get("consent") is not True:
        raise ValueError("Подтвердите согласие на обработку данных")

    fields: dict[str, str] = {}
    for key in ("name", "email", "phone"):
        value = payload.get(key)
        if not isinstance(value, str):
            raise ValueError("Заполните имя, почту и телефон")
        fields[key] = " ".join(value.split())

    name, email, phone = fields["name"], fields["email"], fields["phone"]
    if not 2 <= len(name) <= 80 or any(ord(char) < 32 for char in name):
        raise ValueError("Укажите имя от 2 до 80 символов")
    if len(email) > 254 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        raise ValueError("Укажите корректную почту")
    if len(phone) > 32 or not re.fullmatch(r"\+?[\d\s().-]+", phone) or not 10 <= sum(char.isdigit() for char in phone) <= 15:
        raise ValueError("Укажите корректный телефон")
    source = payload.get("source", "home")
    if not isinstance(source, str) or source not in lead_store.FORM_NAMES:
        raise ValueError("Неизвестная форма заявки")
    fields["source_slug"] = source
    fields["form_name"] = lead_store.FORM_NAMES[source]
    return fields


def send_lead_to_telegram(lead: dict[str, str]) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Telegram bot is not configured")

    proxy_url = os.getenv("TELEGRAM_PROXY_URL", "").strip() or os.getenv("OPENROUTER_PROXY_URL", "").strip()
    if proxy_url.startswith("socks5://"):
        proxy_url = "socks5h://" + proxy_url.removeprefix("socks5://")
    proxies = {"https": proxy_url} if proxy_url else None

    page_url = f"https://molniya-tech.ru{lead_store.SOURCE_PATHS[lead['source_slug']]}"
    text = (
        f"<b>Заявка №{escape(lead['id'][:8].upper())}</b>\n\n"
        "<b>Информация о клиенте:</b>\n"
        f"Имя: {escape(lead['name'], quote=False)}\n"
        f"Телефон: {escape(lead['phone'], quote=False)}\n"
        f"Почта: {escape(lead['email'], quote=False)}\n\n"
        "<b>Дополнительная информация:</b>\n"
        f"Код заявки: <code>{escape(lead['id'])}</code>\n"
        f"Форма: {escape(lead['form_name'], quote=False)}\n"
        f'<a href="{escape(page_url, quote=True)}">{escape(page_url, quote=False)}</a>'
    )
    with requests.Session() as session:
        session.trust_env = False
        response = session.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": int(os.getenv("TELEGRAM_LEADS_CHAT_ID", TELEGRAM_LEADS_CHAT_ID)), "text": text, "parse_mode": "HTML"},
            proxies=proxies,
            timeout=8,
        )
        response.raise_for_status()
        result = response.json()
        if not isinstance(result, dict) or result.get("ok") is not True:
            raise ValueError("Telegram rejected the message")


def deliver_lead_notification(record: dict[str, str]) -> None:
    try:
        send_lead_to_telegram(record)
    except (RuntimeError, requests.RequestException, ValueError):
        sent = False
    else:
        sent = True
    try:
        lead_store.mark_telegram_attempt(record["id"], sent)
    except (OSError, sqlite3.Error):
        # The saved application remains pending for the retry worker.
        pass


class MolniyaApiHandler(BaseHTTPRequestHandler):
    server_version = "MolniyaApi/1.0"
    sys_version = ""

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        self._send(status, json.dumps(payload, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def _client_ip(self) -> str:
        forwarded = self.headers.get("X-Real-IP", "").strip()
        return forwarded or self.client_address[0]

    def do_GET(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path
        if path == "/health":
            self._send_json(HTTPStatus.OK, {"status": "ok"})
            return
        if path == "/api/calendar":
            self._handle_calendar()
            return
        if path == "/api/inn":
            self._handle_inn()
            return
        if path == "/api/inn/pdf":
            self._handle_inn_pdf()
            return
        if path == "/api/weather":
            self._handle_weather()
            return
        if path == "/api/weather/cities":
            self._handle_weather_cities()
            return
        if path in {"/blog", "/blog/", "/blog/index.html"}:
            self._send(HTTPStatus.OK, (blog_store.DATA_DIR / "index.html").read_bytes(), "text/html; charset=utf-8")
            return
        if path == "/sitemap.xml":
            self._send(HTTPStatus.OK, (blog_store.DATA_DIR / "sitemap.xml").read_bytes(), "application/xml; charset=utf-8")
            return
        if path == "/rss.xml":
            rss_candidates = [
                Path("/usr/share/nginx/html/rss.xml"),
                blog_store.DATA_DIR / "rss.xml",
                Path(__file__).resolve().parent.parent / "rss.xml",
                blog_store.TEMPLATE_DIR / "rss.xml",
            ]
            for candidate in rss_candidates:
                if candidate.is_file():
                    self._send(HTTPStatus.OK, candidate.read_bytes(), "application/rss+xml; charset=utf-8")
                    return
            self.send_error(HTTPStatus.NOT_FOUND, "RSS feed not found")
            return
        if path.startswith("/blog/"):
            slug = path.removeprefix("/blog/")
            if blog_store.SLUG_RE.fullmatch(slug):
                page = blog_store.DATA_DIR / f"{slug}.html"
                if page.is_file():
                    self._send(HTTPStatus.OK, page.read_bytes(), "text/html; charset=utf-8")
                    return
                target = blog_store.redirect_target(slug)
                if target:
                    self.send_response(HTTPStatus.MOVED_PERMANENTLY)
                    self.send_header("Location", f"/blog/{target}")
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
        self._send_json(HTTPStatus.NOT_FOUND, {"error": "Не найдено"})

    def do_POST(self) -> None:  # noqa: N802
        if urlsplit(self.path).path == "/api/seosmith":
            self._handle_seosmith()
            return
        if urlsplit(self.path).path == "/api/lead":
            self._handle_lead()
            return
        if self.path != "/api/industry-fit":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Не найдено"})
            return

        if not rate_limit_allows(self._client_ip()):
            self._send_json(HTTPStatus.TOO_MANY_REQUESTS, {"error": "Слишком много запросов"})
            return

        content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type != "application/json":
            self._send_json(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"error": "Ожидается JSON"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0
        if content_length <= 0 or content_length > MAX_BODY_BYTES:
            self._send_json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "Некорректный размер запроса"})
            return

        try:
            raw_payload = self.rfile.read(content_length)
            payload = json.loads(raw_payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Некорректный JSON"})
            return

        if not isinstance(payload, dict) or payload.get("website"):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Некорректный запрос"})
            return

        business = payload.get("business")
        if not isinstance(business, str):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Опишите сферу бизнеса"})
            return
        business = " ".join(business.split())
        if not 3 <= len(business) <= MAX_BUSINESS_LENGTH:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Описание должно содержать от 3 до 240 символов"})
            return

        try:
            result = call_jev(business)
        except (requests.RequestException, ValueError, RuntimeError):
            self._send_json(HTTPStatus.BAD_GATEWAY, {"error": "Сервис проверки временно недоступен"})
            return

        self._send_json(HTTPStatus.OK, result)

    def _handle_lead(self) -> None:
        if not rate_limit_allows("lead:" + self._client_ip()):
            self._send_json(HTTPStatus.TOO_MANY_REQUESTS, {"error": "Слишком много заявок. Попробуйте позже."})
            return
        if self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower() != "application/json":
            self._send_json(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"error": "Ожидается JSON"})
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0
        if content_length <= 0 or content_length > MAX_LEAD_BODY_BYTES:
            self._send_json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "Некорректный размер запроса"})
            return
        try:
            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Некорректный JSON"})
            return
        if isinstance(payload, dict) and payload.get("website"):
            self._send_json(HTTPStatus.OK, {"ok": True})
            return
        try:
            lead = validate_lead(payload)
        except ValueError as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        try:
            record = lead_store.save_lead(lead)
        except (OSError, sqlite3.Error, UnicodeError):
            self._send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "Не удалось сохранить заявку. Попробуйте позже."})
            return
        deliver_lead_notification(record)
        self._send_json(HTTPStatus.OK, {"ok": True})

    def _handle_calendar(self) -> None:
        from urllib.parse import parse_qs
        query = parse_qs(urlsplit(self.path).query)
        year_param = query.get("year", ["2026"])[0]
        try:
            year = int(year_param)
            if not (2020 <= year <= 2035):
                raise ValueError("Год вне допустимого диапазона")
        except ValueError:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Некорректный год"})
            return

        if year in _calendar_cache:
            self._send_json(HTTPStatus.OK, {"year": year, "data": _calendar_cache[year]})
            return

        try:
            resp = requests.get(
                f"https://isdayoff.ru/api/getdata?year={year}&pre=1&cc=ru",
                timeout=4,
                headers={"User-Agent": "MolniyaCalendar/1.0"},
            )
            if resp.status_code == 200 and len(resp.text.strip()) in (365, 366):
                data = resp.text.strip()
                _calendar_cache[year] = data
                self._send_json(HTTPStatus.OK, {"year": year, "data": data})
                return
        except Exception:
            pass

        self._send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "Данные календаря временно недоступны"})

    def _handle_inn(self) -> None:
        from urllib.parse import parse_qs
        query_params = parse_qs(urlsplit(self.path).query)
        query = query_params.get("query", [""])[0].strip()
        if not query:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Параметр query обязателен"})
            return

        try:
            data = fetch_counterparty_data(query)
            self._send_json(HTTPStatus.OK, data)
        except ValueError as err:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(err)})
        except LookupError as err:
            self._send_json(HTTPStatus.NOT_FOUND, {"error": str(err)})
        except RuntimeError as err:
            self._send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": str(err)})
        except Exception:
            self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "Не удалось проверить контрагента"})

    def _handle_inn_pdf(self) -> None:
        from urllib.parse import parse_qs
        query_params = parse_qs(urlsplit(self.path).query)
        token = query_params.get("token", [""])[0].strip()
        inn = query_params.get("inn", ["fns"])[0].strip()
        if not token:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Токен выписки не указан"})
            return

        session = requests.Session()
        session.headers.update({"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})

        for _ in range(4):
            try:
                st = session.get(f"https://egrul.nalog.ru/vyp-status/{token}", timeout=3).json()
                if st.get("status") == "ready":
                    break
            except Exception:
                pass
            time.sleep(1)

        try:
            dl = session.get(f"https://egrul.nalog.ru/vyp-download/{token}", timeout=8)
            if dl.status_code == 200 and len(dl.content) > 1000:
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Disposition", f'attachment; filename="vypiska_{inn}.pdf"')
                self.send_header("Content-Length", str(len(dl.content)))
                self.end_headers()
                self.wfile.write(dl.content)
                return
        except Exception:
            pass

        self._send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "Не удалось скачать выписку из ФНС"})

    def _handle_weather_cities(self) -> None:
        self._send_json(HTTPStatus.OK, {"cities": RUSSIAN_CITIES})

    def _handle_weather(self) -> None:
        from urllib.parse import parse_qs
        query = parse_qs(urlsplit(self.path).query)
        city_param = query.get("city", ["msk"])[0].strip().lower()
        lat_param = query.get("lat", [None])[0]
        lon_param = query.get("lon", [None])[0]

        if lat_param and lon_param:
            try:
                lat = float(lat_param)
                lon = float(lon_param)
                if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
                    raise ValueError
                city_name = query.get("name", ["Моя геопозиция"])[0].strip() or "Моя геопозиция"
                city_slug = "custom"
            except (ValueError, TypeError):
                self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Некорректные координаты"})
                return
        else:
            city_entry = CITIES_BY_SLUG.get(city_param, CITIES_BY_SLUG["msk"])
            lat = float(city_entry["lat"])
            lon = float(city_entry["lon"])
            city_name = city_entry["name"]
            city_slug = city_entry["slug"]

        try:
            data = fetch_weather_data(lat, lon, city_name, city_slug)
            self._send_json(HTTPStatus.OK, data)
        except Exception as exc:
            self._send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": str(exc)})

    def _handle_seosmith(self) -> None:
        secret = os.getenv("SEOSMITH_WEBHOOK_SECRET", "")
        if not secret:
            self._send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "Webhook не настроен"})
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0
        if content_length <= 0 or content_length > MAX_WEBHOOK_BYTES:
            self._send_json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "Некорректный размер запроса"})
            return
        raw_body = self.rfile.read(content_length)
        signature = self.headers.get("X-SeoSmith-Signature", "")
        expected = "sha256=" + hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            self._send_json(HTTPStatus.UNAUTHORIZED, {"error": "Неверная подпись"})
            return
        try:
            payload = json.loads(raw_body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Некорректный JSON"})
            return
        if not isinstance(payload, dict):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Некорректный запрос"})
            return
        if payload.get("event") != "article.published":
            self._send_json(HTTPStatus.OK, {"ok": True, "skipped": True})
            return
        try:
            article = blog_store.validate_article(payload.get("article"))
            blog_store.upsert_article(article)
        except ValueError as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        except OSError:
            self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "Не удалось сохранить статью"})
            return
        self._send_json(HTTPStatus.OK, {"ok": True})

    def log_message(self, _format: str, *_args: Any) -> None:
        # Intentionally avoid request logs: descriptions may contain business details.
        return


def run() -> None:
    blog_store.rebuild_public()
    lead_store.init_db()
    threading.Thread(target=_retry_pending_leads, daemon=True, name="telegram-lead-retry").start()
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8080"))
    server = ThreadingHTTPServer((host, port), MolniyaApiHandler)
    server.serve_forever()


def _retry_pending_leads() -> None:
    while True:
        time.sleep(60)
        try:
            retry_pending_leads_once()
        except (OSError, sqlite3.Error):
            continue


def retry_pending_leads_once() -> None:
    for record in lead_store.pending_telegram_leads():
        deliver_lead_notification(record)


if __name__ == "__main__":
    run()
