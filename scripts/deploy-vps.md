# Деплой на VPS (вариант A)

## Требования

- Ubuntu/Debian VPS с Docker и Docker Compose v2
- Домен указывает на IP VPS (для TLS)
- Порты 80/443 открыты; 5432 наружу не публиковать

## Шаги

```bash
sudo apt update && sudo apt install -y git docker.io docker-compose-plugin
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

git clone https://github.com/YOUR_USER/stepik-course.git
cd stepik-course
cp .env.prod.example .env.prod
# Задайте надёжный POSTGRES_PASSWORD в .env.prod

docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
curl -sS http://YOUR_SERVER/health
```

## TLS (Let's Encrypt)

Установите certbot на хосте и расширьте `nginx.conf` для `listen 443 ssl` или используйте Caddy как внешний reverse proxy.

## Обновление

```bash
git pull
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
```

Данные PostgreSQL в volume `pgdata_prod` сохраняются, пока не выполнять `docker volume rm`.
