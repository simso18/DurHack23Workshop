# syntax=docker/dockerfile:1

FROM python:3.10-slim
WORKDIR /src

# common layers shared between both images
COPY settings.py settings.py
COPY common common
RUN pip install -r ./common/requirements.txt

# docker builds in layers; requirements are less likely to change than the app itself
COPY ./dashboard/requirements.txt ./dashboard/requirements.txt
RUN pip install --default-timeout=100 -r ./dashboard/requirements.txt

COPY dashboard dashboard
EXPOSE 8080
CMD python -m dashboard.app