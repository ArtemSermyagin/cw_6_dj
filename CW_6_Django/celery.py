import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CW_6_Django.settings")
app = Celery("CW_6_Django")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "mailing_monthly": {
        "task": "clients.tasks.mailing_monthly",
        "schedule": crontab(
            minute=0,
            hour=0,
            day_of_month=1,
        ),
    },
    "mailing_weekly": {
        "task": "clients.tasks.mailing_weekly",
        "schedule": crontab(
            minute=0,
            hour=0,
            day_of_week='mon',
        ),
    },
    "mailing_daily": {
        "task": "clients.tasks.mailing_daily",
        "schedule": crontab(
            minute=0,
            hour=0,
        ),
    },
}
