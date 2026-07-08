#!/usr/bin/env bash
# Следит за папкой blog/ на сервере и отправляет в IndexNow (подхватывают
# Bing, Yandex и другие участники протокола) URL каждой НОВОЙ статьи —
# независимо от того, как файл там появился (git-деплой или ручная правка
# на сервере). Уже отправленные статьи и legal-страницы (privacy/cookies —
# у них noindex) не трогает.
#
# Использование:
#   ./scripts/submit-indexnow.sh              — обычный запуск (для cron)
#   ./scripts/submit-indexnow.sh --all         — принудительно отправить все
#                                                 статьи заново (например,
#                                                 при первой настройке)
#
# Cron на сервере (проверка каждые 15 минут):
#   */15 * * * * cd /home/deploy/molniya && ./scripts/submit-indexnow.sh >> /var/log/molniya-indexnow.log 2>&1
#
# Требование: 224a02dac2334ddf85fd7a13f70849f0.txt должен быть доступен
# по https://molniya-tech.ru/224a02dac2334ddf85fd7a13f70849f0.txt.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BLOG_DIR="${SCRIPT_DIR}/blog"
STATE_FILE="${SCRIPT_DIR}/.indexnow-seen"

HOST="molniya-tech.ru"
KEY="224a02dac2334ddf85fd7a13f70849f0"
KEY_LOCATION="https://${HOST}/${KEY}.txt"

FORCE_ALL=false
if [[ "${1:-}" == "--all" ]]; then
  FORCE_ALL=true
fi

touch "${STATE_FILE}"

# index.html — это страница-заглушка со списком рубрик, не статья.
POSTS=()
while IFS= read -r post; do
  POSTS+=("${post}")
done < <(find "${BLOG_DIR}" -maxdepth 1 -name "*.html" ! -name "index.html" -exec basename {} \; | sort)

NEW_URLS=()
for post in "${POSTS[@]}"; do
  if [[ "${FORCE_ALL}" == true ]] || ! grep -qxF "${post}" "${STATE_FILE}"; then
    NEW_URLS+=("https://${HOST}/blog/${post%.html}")
  fi
done

if [[ ${#NEW_URLS[@]} -eq 0 ]]; then
  echo "$(date -Iseconds) — новых статей нет."
  exit 0
fi

echo "$(date -Iseconds) — найдено новых статей: ${#NEW_URLS[@]}"
printf '  %s\n' "${NEW_URLS[@]}"

URL_LIST_JSON=$(printf '"%s",' "${NEW_URLS[@]}")
URL_LIST_JSON="[${URL_LIST_JSON%,}]"

RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "{\"host\": \"${HOST}\", \"key\": \"${KEY}\", \"keyLocation\": \"${KEY_LOCATION}\", \"urlList\": ${URL_LIST_JSON}}")

echo "IndexNow ответил: HTTP ${RESPONSE}"

if [[ "${RESPONSE}" == "200" || "${RESPONSE}" == "202" ]]; then
  printf '%s\n' "${POSTS[@]}" > "${STATE_FILE}"
  echo "Готово, состояние обновлено."
else
  echo "Отправка не удалась (HTTP ${RESPONSE}), состояние не обновлено — повторим при следующем запуске."
  exit 1
fi
