#!/bin/ash

echo "Apply database migrations"

Python manage.py migrate

exec "$@"