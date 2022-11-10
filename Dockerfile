FROM python:3.8.10

ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN mkdir /expense_manager
COPY ./expense_manager /expense_manager
WORKDIR /expense_manager
COPY ./entrypoint.sh /