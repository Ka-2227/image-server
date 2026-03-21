# Image Server

Простой сервер загрузки и просмотра изображений (Flask + PostgreSQL + Nginx).

## Запуск

```bash
cp .env.example .env          # создай .env и обязательно смени SECRET_KEY и пароль
docker compose up --build -d