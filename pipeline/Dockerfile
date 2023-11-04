# syntax=docker/dockerfile:1

FROM python:3.10-slim
WORKDIR /src

# common layers shared between both images
COPY settings.py settings.py
COPY common common
RUN pip install -r ./common/requirements.txt

# docker builds in layers; requirements are less likely to change than the app itself
COPY ./pipeline/requirements.txt ./pipeline/requirements.txt
RUN pip install -r ./pipeline/requirements.txt

COPY pipeline pipeline
CMD python -m pipeline.run