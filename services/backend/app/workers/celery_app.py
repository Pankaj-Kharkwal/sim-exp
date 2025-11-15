"""
Celery Application Configuration

Configures Celery with Redis broker and result backend.
Includes task routing, rate limits, and error handling.
"""

import os
from celery import Celery
from celery.schedules import crontab
from kombu import Exchange, Queue

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Initialize Celery
celery_app = Celery(
    "pankh_workers",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.workers.tasks",
        "app.workers.scheduled_tasks",
    ],
)

# Celery Configuration
celery_app.conf.update(
    # Task settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,

    # Task routing
    task_routes={
        "app.workers.tasks.execute_workflow_task": {"queue": "workflows"},
        "app.workers.tasks.send_notification_task": {"queue": "notifications"},
        "app.workers.scheduled_tasks.*": {"queue": "scheduled"},
    },

    # Result backend settings
    result_expires=3600,  # 1 hour
    result_backend_transport_options={
        "master_name": "mymaster",
    },

    # Worker settings
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,

    # Task execution settings
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_time_limit=300,  # 5 minutes hard limit
    task_soft_time_limit=240,  # 4 minutes soft limit

    # Rate limiting
    task_default_rate_limit="100/m",  # 100 tasks per minute

    # Error handling
    task_annotations={
        "*": {
            "rate_limit": "100/m",
            "time_limit": 300,
            "soft_time_limit": 240,
        },
        "app.workers.tasks.execute_workflow_task": {
            "rate_limit": "50/m",
            "time_limit": 600,  # 10 minutes for workflows
            "soft_time_limit": 540,
        },
    },

    # Retry settings
    task_autoretry_for=(Exception,),
    task_retry_kwargs={"max_retries": 3, "countdown": 5},

    # Beat schedule (periodic tasks)
    beat_schedule={
        "cleanup-old-logs": {
            "task": "app.workers.scheduled_tasks.cleanup_old_logs_task",
            "schedule": crontab(hour=2, minute=0),  # Daily at 2 AM
        },
        "cleanup-old-executions": {
            "task": "app.workers.scheduled_tasks.cleanup_old_executions_task",
            "schedule": crontab(hour=3, minute=0),  # Daily at 3 AM
        },
        "send-daily-summary": {
            "task": "app.workers.scheduled_tasks.send_daily_summary_task",
            "schedule": crontab(hour=9, minute=0),  # Daily at 9 AM
        },
    },
)

# Define queues
celery_app.conf.task_queues = (
    Queue("workflows", Exchange("workflows"), routing_key="workflows"),
    Queue("notifications", Exchange("notifications"), routing_key="notifications"),
    Queue("scheduled", Exchange("scheduled"), routing_key="scheduled"),
    Queue("default", Exchange("default"), routing_key="default"),
)

# Task events
celery_app.conf.task_send_sent_event = True
celery_app.conf.worker_send_task_events = True

logger.info(
    "celery_configured",
    broker=settings.REDIS_URL,
    queues=["workflows", "notifications", "scheduled", "default"],
)


# Celery signals for monitoring
@celery_app.task(bind=True)
def debug_task(self):
    """Debug task to test Celery setup"""
    logger.info("celery_debug_task", request=self.request)
    return {"status": "ok", "task_id": self.request.id}
