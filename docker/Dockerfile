FROM python:3.8

WORKDIR /app

COPY ./api/requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./api /app

CMD ["python", "app.py"]
