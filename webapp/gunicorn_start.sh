#!/usr/bin/env bash

exec /home/samk/acworkflow/acenv/bin/gunicorn run:app \
    --name "acworkflow" \
    --workers 2 \
    --timeout 120 \
    --bind 0.0.0.0:8085 \
    --reload