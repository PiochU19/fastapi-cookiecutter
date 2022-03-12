#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# for local development, uvicorn is used
exec "uvicorn --reload --host 0.0.0.0 --port {{ cookiecutter.app_port }} app.main:app"
