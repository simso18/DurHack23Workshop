# syntax=docker/dockerfile:1

FROM python:3.10-slim
WORKDIR /src

# docker builds in layers; requirements are less likely to change than the app itself
COPY ./requirements.txt ./requirements.txt
RUN pip install --default-timeout=100 -r requirements.txt

COPY ../settings.py ../settings.py
COPY ../common ../common
RUN pip install -r ../common/requirements.txt

COPY . .
CMD python app.py