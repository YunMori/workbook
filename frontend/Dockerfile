# 프론트엔드 — Vue를 빌드해서 nginx 이미지에 정적 파일로 굽는다.
# 빌드 컨텍스트는 저장소 루트다:  docker build -f frontend/Dockerfile .
FROM node:20-alpine AS build

WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build


FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
