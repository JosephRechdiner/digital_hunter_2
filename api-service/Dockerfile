FROM python:3.11-slim

WORKDIR /app

COPY ./api-service/requirements.txt /app

RUN pip install -r requirements.txt

COPY ./api-service /app

EXPOSE 8000

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]