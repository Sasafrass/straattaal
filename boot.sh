#!/bin/bash
source venv/bin/activate
flask db upgrade
export TMPDIR='/var/tmp'
exec gunicorn -b :5000 --access-logfile - --error-logfile - straattaal:app
