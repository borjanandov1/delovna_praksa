FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings.prod \
    SQLITE_PATH=/data/db.sqlite3 \
    MEDIA_ROOT=/data/media

WORKDIR /app

COPY requirements.txt requirements-prod.txt ./
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY . .

# Static files and translations don't depend on runtime secrets, so bake them into the image.
RUN SECRET_KEY=build-only python manage.py collectstatic --noinput \
 && python scripts/i18n_tools.py compile

CMD ["sh", "docker-entrypoint.sh"]
