## 1. Command to run Celery worker in background.

```
$ celery -A celery_worker.celery worker --loglevel=info
```

## 4. Command to run FastAPI project.

```
$ uvicorn main:app --reload
```

## 5. Command to run Unit Tests.

```
$ python -m pytest test_main.py
```