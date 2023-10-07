#!/bin/sh

# if [ "$DATABASE" = "postgres" ]
# then
#     echo "Waiting for postgres..."

#     while ! nc -z $SQL_HOST $SQL_PORT; do
#       sleep 0.1
#     done

#     echo "PostgreSQL started"
# fi

python manage.py migrate
python manage.py makemigrations
python manage.py migrate
# python manage.py migrate django_celery_results

python manage.py createsuperuser --username kingship --email kingship.lc@gmail.com --noinput

python manage.py collectstatic --noinput

exec "$@"