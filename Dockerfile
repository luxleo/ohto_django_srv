FROM python:3.10

RUN apt-get update && apt-get install vim -y

WORKDIR /django_project/
ADD . /django_project/

WORKDIR /django_project/
RUN pip install -r ./requirements.txt 


ENV PYTHONUNBUFFERD=1
ENV PROD=--settings.ohto.settings.prod

