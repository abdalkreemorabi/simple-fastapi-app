from celery import Celery

app = Celery("worker", config_source="app.celery.config")
