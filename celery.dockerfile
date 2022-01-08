FROM python:3.6

RUN mkdir -p /code
WORKDIR /code
ADD . .

RUN pip install -r requirements.txt

CMD [ "celery", "-A", "celery_worker.celery", "worker", "--loglevel=info" ]
# celery -A celery_worker.celery worker --loglevel=info