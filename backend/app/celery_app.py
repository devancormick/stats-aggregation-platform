from celery import Celery
from app.config import settings

celery_app = Celery(
    "stats_scraper",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks.scraper_tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "daily-scrape": {
            "task": "app.tasks.scraper_tasks.scrape_all_leagues",
            "schedule": 86400.0,  # Run daily
        },
    },
)
