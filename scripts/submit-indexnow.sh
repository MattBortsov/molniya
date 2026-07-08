#!/usr/bin/env bash
# Отправляет все URL сайта в IndexNow (подхватывают Bing, Yandex и другие
# участники протокола). Запускать вручную после деплоя, когда нужно
# ускорить переиндексацию — например, после публикации новых страниц блога.
#
# Требование: 224a02dac2334ddf85fd7a13f70849f0.txt должен уже быть доступен
# по https://molniya-tech.ru/224a02dac2334ddf85fd7a13f70849f0.txt (т.е. сайт
# уже задеплоен с этим файлом в корне).

set -euo pipefail

HOST="molniya-tech.ru"
KEY="224a02dac2334ddf85fd7a13f70849f0"
KEY_LOCATION="https://${HOST}/${KEY}.txt"

curl -s -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d @- <<EOF
{
  "host": "${HOST}",
  "key": "${KEY}",
  "keyLocation": "${KEY_LOCATION}",
  "urlList": [
    "https://${HOST}/",
    "https://${HOST}/blog",
    "https://${HOST}/privacy.html",
    "https://${HOST}/cookies.html"
  ]
}
EOF

echo ""
echo "Готово. Ожидаемые коды: 200 (принято) или 202 (принято, ключ проверяется асинхронно)."
