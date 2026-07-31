# SSAFY 모의고사 문제집

Vue.js & JavaScript 모의고사(2차 V1~V5)를 브라우저에서 풀고 채점하는 웹앱.
원본 마크다운을 파싱해 DB에 넣고, 문제 수정은 Django admin에서 한다.

- **문제 보기** — 문항을 훑어보며 정답·해설을 토글로 확인
- **응시하기** — 타이머와 OMR 답안지로 실제 시험처럼 풀고 제출
- **채점** — 객관식·주관식은 자동, 서술형은 채점 기준표를 보고 자기채점
- **응시 기록** — 로그인 없이 브라우저 토큰으로 이력 유지

## 구조

```
data/exams/        원본 마크다운 + overrides.json
backend/           Django 6 + DRF (SQLite)
frontend/          Vue 3 + Vite + Pinia
```

## 처음 실행할 때

```bash
# 백엔드
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements.txt
cd backend
../.venv/bin/python manage.py migrate
../.venv/bin/python manage.py createsuperuser   # 관리자 계정(본인) 하나만
../.venv/bin/python manage.py import_exam       # 마크다운 5세트 등록
../.venv/bin/python manage.py runserver

# 프론트엔드 (새 터미널)
cd frontend
npm install
npm run dev
```

- 앱: http://localhost:5173
- 관리자: http://localhost:8000/admin/

Vite가 `/api` 요청을 `127.0.0.1:8000`으로 프록시한다.

## 문제 관리

**수정·추가**는 admin에서 한다.

- `문항` — 지문·배점·난이도 수정, 선택지와 정답·해설이 인라인으로 함께 열린다
- `정답·해설` — 주관식 채점 규칙만 몰아서 손볼 때 사용. `검토 필요` 필터로 걸러 본다

**새 회차 추가**는 기존 마크다운과 같은 형식으로 `<이름>_문제.md` / `<이름>_정답해설.md`를
`data/exams/`에 넣고 다시 임포트한다.

```bash
../.venv/bin/python manage.py import_exam --dry-run   # 파싱 결과만 확인
../.venv/bin/python manage.py import_exam             # 새 회차만 등록
../.venv/bin/python manage.py import_exam --update    # 기존 회차까지 덮어쓰기
```

`--update`는 해당 시험의 문항을 지우고 다시 만든다. **admin에서 손으로 고친 내용도 함께 지워진다.**
다시 임포트해도 남아야 하는 수정은 `data/exams/overrides.json`에 적는다.

### overrides.json

파서가 지문과 구분할 수 없는 내용(원본에 손으로 적어 둔 답안 초안 등)을 문항 단위로 덮어쓴다.
키는 `"<차수>-<버전>"` / `"<문항번호>"`.

```json
{ "2-1": { "23": { "body": "다음 코드의 출력 결과를 순서대로 쓰시오.\n\n```js\n…\n```" } } }
```

## 채점 방식

| 유형 | 방식 |
|---|---|
| 객관식 | 선택 번호와 정답 번호 비교 |
| 주관식 | 표기 정규화 후 정답 후보와 완전 일치 → 실패하면 키워드 그룹이 모두 포함되는지 확인 |
| 서술형 | 자동 채점하지 않음. 채점 기준표를 체크해 부분점수를 직접 매긴다 |

주관식 자동 채점이 어긋나면 결과 화면의 `정답으로 인정` 버튼으로 바로잡을 수 있다.
임포트 시 규칙을 자신 있게 뽑아내지 못한 문항은 `검토 필요`로 표시되며, 30문항 중 10문항이
여기 해당한다 — admin에서 `정답 후보`와 `키워드 규칙`을 채워 넣으면 자동 채점 정확도가 올라간다.

## 테스트

```bash
cd backend && ../.venv/bin/python manage.py test exams
```

파서(실제 5개 버전이 30문항·배점 100점으로 파싱되는지, 정답표와 개별 해설이 일치하는지),
채점 로직, 응시 API, 관리자 화면을 확인한다.

## EC2 배포 (Docker)

컨테이너 두 개다.

| 서비스 | 하는 일 |
|---|---|
| `web` | Django + gunicorn. `/api/`, `/admin/`, `/static/`(WhiteNoise) 처리 |
| `nginx` | 80번을 받아 위 경로는 `web`으로 넘기고, 나머지는 Vue 빌드 결과를 서빙 |

Vue는 `frontend/Dockerfile`의 빌드 스테이지에서 컴파일돼 nginx 이미지에 구워진다.
서버에 파이썬·Node·nginx를 따로 설치할 일이 없다.

**데이터**는 `db` 볼륨의 `db.sqlite3` 하나뿐이다. 이미지를 다시 빌드해도 응시 기록과
admin에서 고친 내용은 남는다.

설정은 `backend/.env`로 주입한다. 이 파일이 없으면 개발용 기본값으로 동작하므로
로컬 실행 방법(`runserver` + `npm run dev`)은 그대로다. 항목은 `backend/.env.example` 참고.

### 준비

- EC2에 **탄력적 IP를 연결**한다. 안 하면 재시작할 때마다 IP가 바뀌어 `ALLOWED_HOSTS`를 매번 고쳐야 한다.
- 보안 그룹: 22번은 내 IP만, 80번은 전체 개방.
- Docker 설치:
  ```bash
  curl -fsSL https://get.docker.com | sudo sh
  sudo usermod -aG docker $USER && exec newgrp docker
  ```
- **스왑 2GB** — 1GB 인스턴스(t2.micro 등)에서 프론트엔드 빌드가 메모리 부족으로 죽는 것을 막는다.
  ```bash
  sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile
  sudo mkswap /swapfile && sudo swapon /swapfile
  echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
  ```

### 처음 한 번

```bash
sudo mkdir -p /srv/workbook && sudo chown "$USER":"$USER" /srv/workbook
git clone <저장소> /srv/workbook && cd /srv/workbook

export IP=<탄력적 IP>
cat > backend/.env <<EOF
SECRET_KEY=$(head -c 50 /dev/urandom | base64 | tr -d '\n=+/')
DEBUG=0
ALLOWED_HOSTS=$IP
CSRF_TRUSTED_ORIGINS=http://$IP
SECURE_SSL=0
EOF
chmod 600 backend/.env

docker compose up -d --build
docker compose exec web python manage.py createsuperuser
```

첫 기동에서 `web` 컨테이너가 migrate → collectstatic → `import_exam`을 자동으로 돌려
문제 150개를 채운다. 이후 기동에서는 이미 등록된 회차를 건너뛴다.

`http://<탄력적 IP>` 로 접속.

### 업데이트

```bash
/srv/workbook/deploy/deploy.sh
```

git pull → 이미지 빌드 → 재기동 → 오래된 이미지 정리.

**마크다운 문제를 고쳤다면** 따로 돌린다 (admin에서 손으로 고친 내용이 덮어써진다):

```bash
docker compose exec web python manage.py import_exam --update
```

### 자주 쓰는 명령

```bash
docker compose ps                  # 상태
docker compose logs -f web         # 로그
docker compose restart web         # 재시작
docker compose exec web sh         # 컨테이너 안으로

HTTP_PORT=8080 docker compose up -d   # 80번이 이미 쓰이고 있을 때
```

### HTTPS

도메인이 없는 동안은 HTTP라 **admin 비밀번호가 평문으로 오간다.** 두 가지 대응:

1. `deploy/nginx.conf`의 `allow __MY_IP__; deny all;` 주석을 풀어 관리자 화면을 내 IP로 제한 (이미지 재빌드 필요)
2. 도메인(무료 서브도메인도 가능)을 얻어 인증서를 받은 뒤 `.env`에 `SECURE_SSL=1`

`SECURE_SSL=1`은 HTTPS 리다이렉트와 secure 쿠키를 켠다. **HTTP 상태에서 켜면 무한 리다이렉트가 된다.**

### 백업

볼륨 안의 SQLite 파일 하나가 전부다.

```bash
docker compose cp web:/srv/app/db/db.sqlite3 ~/backup/db-$(date +%F).sqlite3
```

crontab에 넣으려면 `%`를 이스케이프해야 한다 (`\%F`).
