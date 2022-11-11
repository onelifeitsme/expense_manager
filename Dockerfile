FROM python:3.8.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

COPY req.txt /app/

RUN pip install -U pip && pip install -r req.txt

EXPOSE 8000