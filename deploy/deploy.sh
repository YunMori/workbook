#!/usr/bin/env bash
# 서버에서 최신 코드로 갱신한다.  사용법: /srv/workbook/deploy/deploy.sh
#
# 마크다운 문제를 고쳤다면 따로 돌려야 한다 (admin에서 손으로 고친 내용이 덮어써진다):
#   docker compose exec web python manage.py import_exam --update

set -euo pipefail

cd "$(dirname "$0")/.."

echo "▶ 코드 가져오기"
git pull --ff-only

echo "▶ 이미지 빌드"
docker compose build

echo "▶ 재기동"
docker compose up -d

echo "▶ 사용하지 않는 이미지 정리"
docker image prune -f > /dev/null

echo
docker compose ps
echo "✓ 배포 완료"
