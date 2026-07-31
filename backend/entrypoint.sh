#!/bin/sh
# 컨테이너가 뜰 때마다 실행된다. 전부 여러 번 돌려도 안전한 작업이다.
set -e

echo "▶ 마이그레이션"
python manage.py migrate --noinput

echo "▶ 정적 파일 수집 (admin CSS/JS)"
python manage.py collectstatic --noinput --clear > /dev/null

# --update 없이 실행하면 이미 등록된 회차는 건너뛴다.
# 첫 기동에서는 문제를 채우고, 이후에는 아무것도 바꾸지 않는다.
echo "▶ 문제 데이터 확인"
python manage.py import_exam || echo "  (임포트 건너뜀)"

exec "$@"
