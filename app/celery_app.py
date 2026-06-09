from celery import Celery
from celery.schedules import crontab

from app.config import settings

celery_app = Celery(
    "flight_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.services"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "fetch-flight-data-every-morning": {
        "task": "app.services.celery_track_flights",
        "schedule": crontab(hour=6, minute=0),
        "args": ("HYD", 1, 30),
    },
}
