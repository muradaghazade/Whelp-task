FROM python:3.6

COPY . /code

COPY requirements.txt /code/requirements.txt

WORKDIR /code

EXPOSE 8000:8000

RUN pip install -r requirements.txt

RUN python -m pip install -U celery

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--reload" ]