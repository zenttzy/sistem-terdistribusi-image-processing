#!/usr/bin/env bash
set -euo pipefail

WORKER_NAME="${1:-worker1}"
CONCURRENCY="${2:-1}"

exec celery -A app.celery_app:celery_app worker \
  --hostname="${WORKER_NAME}@%h" \
  --concurrency="${CONCURRENCY}" \
  --loglevel=INFO

