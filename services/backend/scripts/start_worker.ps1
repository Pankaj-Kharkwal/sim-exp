# Start Celery Worker (Windows)
# Usage: .\scripts\start_worker.ps1 [queue_name]

param(
    [string]$Queue = "workflows,notifications,default"
)

Write-Host "🚀 Starting Celery worker..." -ForegroundColor Green
Write-Host "📦 Queue: $Queue" -ForegroundColor Cyan

# Start worker
celery -A app.workers.celery_app worker `
    --loglevel=info `
    --queues=$Queue `
    --concurrency=4 `
    --max-tasks-per-child=1000 `
    --pool=solo `
    --hostname=worker@localhost

# Note: Windows uses 'solo' pool instead of 'prefork'
