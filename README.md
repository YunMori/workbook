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

## EC2 배포

nginx가 80번을 받아 `/api/`·`/admin/`은 유닉스 소켓으로 gunicorn에 넘기고, 나머지는
`frontend/dist`를 정적으로 서빙한다. 프론트와 API가 같은 오리진이 되므로 CORS 설정이 필요 없다.

설정은 `backend/.env`로 주입한다. 이 파일이 없으면 개발용 기본값으로 동작하므로
로컬 실행 방법은 그대로다. 항목은 `backend/.env.example` 참고.

### 준비

- EC2에 **탄력적 IP를 연결**한다. 안 하면 재시작할 때마다 IP가 바뀌어 `ALLOWED_HOSTS`를 매번 고쳐야 한다.
- 보안 그룹: 22번은 내 IP만, 80번은 전체 개방.

### 처음 한 번

```bash
sudo mkdir -p /srv/workbook && sudo chown "$USER":"$USER" /srv/workbook
git clone <저장소> /srv/workbook
bash /srv/workbook/deploy/setup.sh
```

`setup.sh`가 스왑·패키지·가상환경·systemd 등록까지 하고, 값이 필요한 남은 단계
(`.env` 작성 → migrate/import_exam/createsuperuser/collectstatic → 프론트 빌드 → nginx → 기동)를
화면에 안내한다.

### 업데이트

```bash
/srv/workbook/deploy/deploy.sh
```

git pull → 의존성 → migrate → collectstatic → 프론트 빌드 → 재시작을 한 번에 한다.
**마크다운 문제를 고쳤다면** 별도로 돌려야 한다 (admin 수정분이 덮어써진다):

```bash
cd /srv/workbook/backend && ../.venv/bin/python manage.py import_exam --update
```

### HTTPS

도메인이 없는 동안은 HTTP라 **admin 비밀번호가 평문으로 오간다.** 두 가지 대응:

1. `deploy/nginx.conf`의 `allow __MY_IP__; deny all;` 주석을 풀어 관리자 화면을 내 IP로 제한
2. 도메인(무료 서브도메인도 가능)을 얻어 `sudo certbot --nginx` 실행 후 `.env`에 `SECURE_SSL=1`

`SECURE_SSL=1`은 HTTPS 리다이렉트와 secure 쿠키를 켠다. **HTTP 상태에서 켜면 무한 리다이렉트가 된다.**

### 파일

| 경로 | 용도 |
|---|---|
| `deploy/setup.sh` | 최초 설치 |
| `deploy/deploy.sh` | 업데이트 |
| `deploy/workbook.service` | gunicorn systemd 유닛 |
| `deploy/nginx.conf` | nginx 사이트 설정 (`__SERVER_NAME__` 치환 필요) |
| `backend/.env.example` | 환경변수 목록 |

### 백업

`backend/db.sqlite3` 하나가 전부다.

```
0 4 * * * cp /srv/workbook/backend/db.sqlite3 ~/backup/db-$(date +\%F).sqlite3
```
