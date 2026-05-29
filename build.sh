#!/usr/bin/env bash
# Render build script (run from PCG_backend root — same folder as manage.py)
set -o errexit

pip install -r requirement.txt

# Admin CSS (optional: skip if output.css is already committed)
if command -v npm >/dev/null 2>&1; then
  npm ci --omit=dev 2>/dev/null || npm install
  npm run css:build
fi

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Create superuser on Render when env vars are set (see README / deploy notes).
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py createsuperuser --noinput || true
fi
