# Start Celery Beat (Windows)
# Runs periodic tasks defined in celery_app.conf.beat_schedule

Write-Host "⏰ Starting Celery Beat scheduler..." -ForegroundColor Green

# Start beat scheduler
celery -A app.workers.celery_app beat `
    --loglevel=info `
    --pidfile=$env:TEMP\celerybeat.pid `
    --schedule=$env:TEMP\celerybeat-schedule
