#!/usr/bin/env bash
# 서버에서 코드를 최신으로 갱신한다.  사용법: /srv/workbook/deploy/deploy.sh
#
# 문제 데이터는 건드리지 않는다. 마크다운을 고쳤다면 따로 돌려야 한다:
#   cd /srv/workbook/backend && ../.venv/bin/python manage.py import_exam --update
#   (주의: admin에서 손으로 고친 내용이 함께 덮어써진다)

set -euo pipefail

APP_DIR=/srv/workbook
cd "$APP_DIR"

echo "▶ 코드 가져오기"
git pull --ff-only

echo "▶ 파이썬 의존성"
.venv/bin/pip install -q -r backend/requirements.txt

echo "▶ 마이그레이션 · 정적 파일"
cd backend
../.venv/bin/python manage.py migrate --noinput
../.venv/bin/python manage.py collectstatic --noinput

echo "▶ 프론트엔드 빌드"
cd ../frontend
npm ci --silent
npm run build

echo "▶ 재시작"
sudo systemctl restart workbook
sudo systemctl reload nginx

echo "✓ 배포 완료"
systemctl --no-pager --lines=0 status workbook
