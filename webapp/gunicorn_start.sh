#!/usr/bin/env bash

exec /home/samk/acworkflow/env/bin/gunicorn run:app \
    --name "acworkflow" \
    --workers 2 \
    --timeout 120 \
    --bind 127.0.0.1:8001