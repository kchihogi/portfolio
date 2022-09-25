#!/bin/bash
python /workspace/app/portfolio_site/manage.py collectstatic --noinput --clear
while ! python /workspace/app/portfolio_site/manage.py migrate --noinput; do
    sleep 1
done
pass=$(openssl rand -base64 8)
export DJANGO_SUPERUSER_PASSWORD=$pass
echo ==============================
echo ${DJANGO_SUPERUSER_PASSWORD}
echo ==============================
python /workspace/app/portfolio_site/manage.py createsuperuser --noinput --username Administrator --email admin@example.com
gunicorn portfolio_site.wsgi --bind=unix:/var/run/gunicorn/gunicorn.sock --chdir=/workspace/app/portfolio_site
# sleep infinity
