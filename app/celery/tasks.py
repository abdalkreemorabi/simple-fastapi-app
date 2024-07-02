from app.celery.app import app


@app.task(name="test_celery")
def test_celery():
    print("test_celery")