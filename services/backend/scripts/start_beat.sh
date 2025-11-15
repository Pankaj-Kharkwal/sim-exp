#!/bin/bash

# Start Celery Beat (Scheduler)
# Runs periodic tasks defined in celery_app.conf.beat_schedule

set -e

echo "⏰ Starting Celery Beat scheduler..."

# Start beat scheduler
celery -A app.workers.celery_app beat \
    --loglevel=info \
    --pidfile=/tmp/celerybeat.pid \
    --schedule=/tmp/celerybeat-schedule
