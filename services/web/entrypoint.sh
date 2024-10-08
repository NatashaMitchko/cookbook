#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

if [ "$DATABASE" = "redis" ]
then
    echo "Waiting for Redis..."

    while ! nc -z $REDIS_HOST $REDIS_PORT; do
      sleep 0.1
    done

    echo "Redis started"
fi

if [ "$FLASK_DEBUG" = "1" ]
then

    echo "Entrypoint"
    python manage.py list_routes
    echo "Done"

fi

exec "$@"
