#!/usr/bin/env bash

exec /home/samk/dispimdb/env/bin/gunicorn run:app \
    --name "webapp" \
    --workers 2 \
    --timeout 120 \
    --bind 0.0.0.0:8085 \
    --reload