#!/bin/sh

exec /home/samk/webapp/env/bin/gunicorn run:app \
    --name "webapp" \
    --workers 2 \
    --timeout 120 \
    --bind 127.0.0.1:8000