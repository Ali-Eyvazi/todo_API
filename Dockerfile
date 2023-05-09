FROM python:slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /home
COPY  ./todo_API .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
WORKDIR /home/todo_API/
