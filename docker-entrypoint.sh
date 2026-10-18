#!/bin/sh
set -e

mkdir -p "$(dirname "${SQLITE_PATH:-/app/db.sqlite3}")" "${MEDIA_ROOT:-/app/media}"

echo "ALLOWED_HOSTS=${ALLOWED_HOSTS:-<not set>}"

python manage.py migrate --noinput

# Seed demo content only on an empty database, so admin edits survive redeploys.
# -v 0 stops Django 5.2's shell from printing its "N objects imported" banner.
if [ "$(python manage.py shell -v 0 -c 'from training.models import MembershipPlan; print(MembershipPlan.objects.exists())' | tail -n 1)" = "False" ]; then
  python manage.py seed_demo
fi

# No shell access on RepoRun, so create the admin from DJANGO_SUPERUSER_* env vars if set.
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser --noinput 2>/dev/null || true
fi

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --access-logfile -
