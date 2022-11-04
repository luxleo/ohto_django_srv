FROM continuumio/miniconda3:latest

RUN apt-get update && apt-get install vim -y

WORKDIR /django_project/
RUN mkdir DEV 
ADD . /django_project/DEV

WORKDIR /django_project/DEV
RUN conda env update --file project_env.yaml --name base

ENV PYTHONUNBUFFERD=1
ENV PROD=--settings.ohto.settings.prod

