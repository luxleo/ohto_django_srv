FROM python:3.10

RUN apt-get update && apt-get install vim -y

WORKDIR /django_project
ADD . /django_project

ENV DJANGO_SETTINGS_MODULE=ohto.settings.prod
RUN pip install -r ./requirements/prod.txt 


ENV PYTHONUNBUFFERD=1
ENV PROD=--settings.ohto.settings.prod

