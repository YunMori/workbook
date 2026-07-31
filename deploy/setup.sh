#!/usr/bin/env bash
# EC2(Ubuntu)에서 딱 한 번 실행하는 초기 설치 스크립트.
#
#   git clone <저장소> /srv/workbook   # 먼저 clone 해 두고
#   bash /srv/workbook/deploy/setup.sh
#
# 끝난 뒤에 해야 할 일은 스크립트가 마지막에 안내한다.

set -euo pipefail

APP_DIR=/srv/workbook

echo "▶ 스왑 2GB (t2.micro에서 npm install이 메모리 부족으로 죽는 것 방지)"
if ! swapon --show | grep -q /swapfile; then
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab > /dev/null
else
    echo "  이미 있음, 건너뜀"
fi

echo "▶ 패키지 설치"
sudo apt-get update -qq
sudo apt-get install -y -qq python3-venv python3-pip nginx git curl
if ! command -v node > /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y -qq nodejs
fi

echo "▶ 파이썬 가상환경"
cd "$APP_DIR"
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q --upgrade pip
.venv/bin/pip install -q -r backend/requirements.txt

echo "▶ nginx가 정적 파일을 읽을 수 있도록 경로 권한"
chmod o+x "$APP_DIR" "$APP_DIR/frontend" "$APP_DIR/backend"

echo "▶ systemd 서비스 등록"
sudo cp "$APP_DIR/deploy/workbook.service" /etc/systemd/system/workbook.service
sudo systemctl daemon-reload
sudo systemctl enable workbook

cat <<'GUIDE'

──────────────────────────────────────────────
설치는 끝났다. 남은 단계는 값이 필요해서 수동으로 한다.

1) 설정 파일
   cp /srv/workbook/backend/.env.example /srv/workbook/backend/.env
   chmod 600 /srv/workbook/backend/.env
   nano /srv/workbook/backend/.env
     SECRET_KEY  ← /srv/workbook/.venv/bin/python -c \
        "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ALLOWED_HOSTS         ← 탄력적 IP
     CSRF_TRUSTED_ORIGINS  ← http://탄력적IP

2) DB 준비
   cd /srv/workbook/backend
   ../.venv/bin/python manage.py migrate
   ../.venv/bin/python manage.py import_exam
   ../.venv/bin/python manage.py createsuperuser
   ../.venv/bin/python manage.py collectstatic --noinput

3) 프론트엔드 빌드
   cd /srv/workbook/frontend && npm ci && npm run build

4) nginx
   sudo cp /srv/workbook/deploy/nginx.conf /etc/nginx/sites-available/workbook
   sudo sed -i "s/__SERVER_NAME__/<탄력적 IP>/" /etc/nginx/sites-available/workbook
   sudo ln -sf /etc/nginx/sites-available/workbook /etc/nginx/sites-enabled/workbook
   sudo rm -f /etc/nginx/sites-enabled/default
   sudo nginx -t && sudo systemctl reload nginx

5) 기동
   sudo systemctl start workbook
   systemctl status workbook

6) 백업 (선택)
   mkdir -p ~/backup
   (crontab -l 2>/dev/null; echo '0 4 * * * cp /srv/workbook/backend/db.sqlite3 ~/backup/db-$(date +\%F).sqlite3') | crontab -
──────────────────────────────────────────────
GUIDE
