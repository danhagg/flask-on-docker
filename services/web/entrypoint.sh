#!/bin/sh

# Verify postgres up and healthy 
# BEFORE creating db and running Flask dev server
# Also, add $DATABASE, $SQL_HOST, $SQL_PORT to .env.dev
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py create_db

exec "$@"