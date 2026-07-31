# 백엔드 (Django + gunicorn)
# 빌드 컨텍스트는 저장소 루트다:  docker build -f backend/Dockerfile .
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# settings.py의 EXAM_SOURCE_DIR이 BASE_DIR.parent/data/exams 라서
# 저장소와 같은 배치(/srv/app/backend, /srv/app/data)를 유지한다.
WORKDIR /srv/app/backend

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /srv/app/backend/
COPY data/ /srv/app/data/

RUN chmod +x /srv/app/backend/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/srv/app/backend/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
