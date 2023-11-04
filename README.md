# Durhack 2023 Webscraping and Apache Kafka Workshop

## Introduction

In this repository, we will be spinning up a few different components for a very simple data application. There will be:
1. A webscraping service (code is found under ./pipeline/)
2. A Kafka service (we will use the public docker image for this service and connect to it using `confluent_kafka`)
3. A simple dashboard made using Plotly Dash (code under ./dashboard/)

## Docker

Docker is a way of ensuring that the code we run is independent of the OS we use (Linux/MacOS/Windows etc.) by using the concept of 'containerization'. Hence, a docker image which runs on a Linux machine should also be able to run on a Windows machine et cetera. This allows for code to be more easily shared and tested.

The services in this repo have also been packaged into various Docker images, including the `durhack/pipeline` and `durhack/dashboard` images (the Kafka image is a public one). These images are built from source from the respective directories, where the Dockerfiles can also be found.

Docker compose is used to manage the orchestration of multiple containers and services. In this repo, using Docker compose allows us to link the various components together by sharing the same volumes, and to allow the services to connect with a local instance of Kafka.

To start all the services up is as simple as running:
```
docker compose up
```
after which you should see some logs about the various services being buiilt and run.