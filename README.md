## Run

```bash
$ uvicorn app.main:app --reload
# Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## Alembic

1. Generate migrate script:

   Auto generate after changing table in model.py.

   ```bash
   $ alembic revision --autogenerate -m "Change user table"
   ```

   Alembic will detect model change and generate a migration script.

   ~~OR manually generate migration script: run `alembic revision -m "create user table"`~~

2. Migrate(apply change) to DB:
   ```bash
   $ alembic upgrade head
   ```

ref: [使用 Alembic 來進行資料庫版本管理](https://medium.com/@acer1832a/%E4%BD%BF%E7%94%A8-alembic-%E4%BE%86%E9%80%B2%E8%A1%8C%E8%B3%87%E6%96%99%E5%BA%AB%E7%89%88%E6%9C%AC%E7%AE%A1%E7%90%86-32d949f7f2c6)

## Deploy

```bash
$ docker build -t rosethorn999/property_backend_fastapi:latest .
$ docker run --env-file .env --name fastapi8000 -p 8000:8000 rosethorn999/property_backend_fastapi
```

## Example for .env file

```
FRONTEND_HOST=https://property-stg-next.nodm.app
DB_CONNECTION=postgresql://postgres:password@localhost:5432/property
DB_CONNECTION_ASYNC=postgresql+asyncpg://postgres:password@localhost:5432/property
SECRET=@@SECRET!!

SMTP_USE_TLS=True
SMTP_HOST=smtp.domain.com
SMTP_HOST_USER=admin@example.com
SMTP_HOST_PASSWORD=password
SMTP_PORT=587

OAUTH2_GOOGLE_CLIENT_ID=328xxxxxxxxxxxcom
OAUTH2_GOOGLE_CLIENT_SECRET=GOCxxxxxxxxxnug
OAUTH2_GOOGLE_REDIRECT_URL=http://localhost:3000/en/oauth2/google

OAUTH2_FACEBOOK_CLIENT_ID=103xxxxxxxxxxx549
OAUTH2_FACEBOOK_CLIENT_SECRET=456
OAUTH2_FACEBOOK_REDIRECT_URL=http://localhost:3000/en/oauth2/facebook
```

## Ref

- https://github.com/mjhea0/awesome-fastapi
- https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D
