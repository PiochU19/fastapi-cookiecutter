#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

{% if cookiecutter.server == "uvicorn" %}
exec "uvicorn --host 0.0.0.0 --port {{ cookiecutter.no_of_workers }} app.main:app"
{% elif cookiecutter.server == "gunicorn" %}
exec "gunicorn -w {{ cookiecutter.no_of_workers }} -k uvicorn.workers.UvicornWorker -b 0.0.0.0:{{ cookiecutter.app_port }} app.main:app"
{% endif %}
