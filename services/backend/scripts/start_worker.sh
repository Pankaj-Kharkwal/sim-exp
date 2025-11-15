#!/bin/bash

# Start Celery Worker
# Usage: ./scripts/start_worker.sh [queue_name]

set -e

# Get queue name from argument or use default
QUEUE=${1:-"workflows,notifications,default"}

echo "🚀 Starting Celery worker..."
echo "📦 Queue: $QUEUE"

# Start worker with concurrency based on CPU cores
celery -A app.workers.celery_app worker \
    --loglevel=info \
    --queues=$QUEUE \
    --concurrency=4 \
    --max-tasks-per-child=1000 \
    --pool=prefork \
    --hostname=worker@%h
