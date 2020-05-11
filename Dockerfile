# Authors: Mike Menendez, Frank Piva, Felix Romero-Flores, Edgaras Slezas
# Date: May 11, 2020
# Course: CST 205
# Description: Dockerfile for running the application locally or in an ECS-like enviorment

FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD uvicorn main:app --reload
