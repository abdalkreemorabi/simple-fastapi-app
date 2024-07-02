from core.settings import AppSettings, get_settings

broker_url = get_settings(AppSettings).CELERY_BROKER_URL

worker_concurrency = 4

include = ("app.celery.tasks",)

timezone = "UTC"
enable_utc = True
