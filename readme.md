## Steps to run a project:
## 1. Install all packages from requirements.txt file.

```
$ pip install -r requirements.txt
```

## 2. Run docker-compose file.

```
$ docker-compose up -d
```

## 3. Run Celery worker in background.

```
$ celery -A celery_worker.celery worker --loglevel=info
```

## 4. Run FastAPI project.

```
$ uvicorn main:app --reload
```

## 5. Command to run Unit Tests.

```
$ python -m pytest test_main.py
```