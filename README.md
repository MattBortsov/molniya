# Молния Тех

Статический лендинг: `index.html`, `blog/index.html`, `privacy.html`, общие `styles.css` / `script.js` / `fonts/` / `assets/`.

## Локальный просмотр

```bash
python3 -m http.server 8000
```

Открыть http://localhost:8000

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
