# Молния Тех

Лендинг: статические страницы обслуживает Nginx, а небольшой Python API проксирует форму проверки сферы в OpenRouter Jev. Ключ остаётся только на сервере.

## Локальный просмотр

Для полной проверки, включая форму Jev, создайте `.env` по `.env.example` и запустите:

```bash
python3 dev_server.py
```

Открыть http://127.0.0.1:8000

Если порт занят, можно выбрать другой:

```bash
python3 dev_server.py --port 8001
```

Для проверки контейнерной конфигурации используйте полный стек:

```bash
docker compose up -d
```

Открыть http://localhost:8090

## Деплой

Пушим в `main` → GitHub Actions деплоит по SSH на сервер, где уже крутится SEOSmith.
Сайт поднимается в **отдельном nginx-контейнере на порту 8090** (не трогает
80/443, занятые SEOSmith) — см. `docker-compose.yml` и `nginx/nginx.conf`.

Сайт также доступен напрямую по `http://<DEPLOY_HOST>:8090` (без домена/TLS) —
полезно для быстрой проверки, что контейнер жив.

### HTTPS через molniya-tech.ru

Домен проксируется через nginx SEOSmith (тот, что уже держит 80/443 на сервере).
Оба docker-compose проекта соединены общей внешней сетью `edge`:
Молния публикует себя туда как `molniya-nginx:80`, а в SEOSmith лежит
`nginx/molniya.conf` с `server_name molniya-tech.ru` и `proxy_pass` на этот
контейнер. См. подробности и bootstrap-инструкцию по первому выпуску
сертификата в шапке файла `SEOSmith/nginx/molniya.conf`.

Разовая настройка на сервере (после того как оба проекта склонированы):

```bash
docker network create edge
# в /home/deploy/molniya:
docker compose up -d
# в /home/deploy/seosmith — следуя bootstrap-инструкции в nginx/molniya.conf:
docker compose up -d nginx
docker compose run --rm certbot certonly --webroot -w /var/www/certbot \
  -d molniya-tech.ru -d www.molniya-tech.ru
docker compose up -d nginx
```

Дальше сертификат продлевается тем же фоновым `certbot renew`, что уже
обслуживает основной домен SEOSmith — ничего дополнительно настраивать не надо.

### Настройка (один раз)

В GitHub репозитория → Settings → Secrets and variables → Actions добавить:

| Secret | Значение |
|---|---|
| `DEPLOY_HOST` | IP или адрес сервера |
| `DEPLOY_USER` | SSH-пользователь (`deploy`, как у SEOSmith) |
| `SSH_PRIVATE_KEY` | приватный ключ для SSH (тот, чей публичный ключ добавлен на сервере) |
| `DEPLOY_PATH` | `/home/deploy/molniya` (рядом с `/home/deploy/seosmith`) |

На сервере должны быть установлены `git` и `docker compose` (v2, команда `docker compose`, не `docker-compose`).

На сервере в `${DEPLOY_PATH}/.env` должны быть заданы `OPENROUTER_API_KEY` и, при необходимости, `OPENROUTER_MODEL`. Файл игнорируется Git и не удаляется при обновлении репозитория.
