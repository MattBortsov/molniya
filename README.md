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

После деплоя сайт доступен по `http://<DEPLOY_HOST>:8090`, пока нет домена.
Когда домен появится — либо добавить его как ещё один `server_name` в этот
nginx и повесить certbot, либо проксировать с основного nginx SEOSmith.

### Настройка (один раз)

В GitHub репозитория → Settings → Secrets and variables → Actions добавить:

| Secret | Значение |
|---|---|
| `DEPLOY_HOST` | IP или адрес сервера |
| `DEPLOY_USER` | SSH-пользователь (`deploy`, как у SEOSmith) |
| `SSH_PRIVATE_KEY` | приватный ключ для SSH (тот, чей публичный ключ добавлен на сервере) |
| `DEPLOY_PATH` | `/home/deploy/molniya` (рядом с `/home/deploy/seosmith`) |

На сервере должны быть установлены `git` и `docker compose` (v2, команда `docker compose`, не `docker-compose`).
