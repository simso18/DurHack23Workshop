# Scrapy -Apache Kafka Workshop

Note: Feel free to skip over sections you are familiar with 

### Workshop Overview
We will be using:
- Powershell
- Conda
- Scrapy
- Apache Kafka 
- Python Confluent Kafka
- Beautiful Soup

#### Powershell 
This tutorial is based off a Windows OS but you can replace this with your native CLI 

#### Conda
We use conda to create our environment for scraping data, producing Kafka messages and consuming Kafka messages. Installation instructions can be found [here](https://hub.docker.com/r/bitnami/kafka). 

#### Scrapy
https://scrapy.org/


#### Kafka 
If you have a unix system and want to run a Kafka server from scratch, please follow the [quickstart guide](https://kafka.apache.org/quickstart).

We will be using the Kafka docker image which can be used on a Windows system in the interest of time.

Github Repo: https://github.com/bitnami/containers/blob/main/bitnami/kafka/docker-compose.yml

Docker Image: https://hub.docker.com/r/bitnami/kafka

#### python-kafka 

### Setting up Kafka 
#### Start a Kafka server
```
mkdir mw_workshop
 curl https://raw.githubusercontent.com/bitnami/containers/main/bitnami/kafka/docker-compose.yml | Select-Object -expand content > docker-compose.yml
docker-compose up -d
docker ps 
```

#### Create and Test a Kafka Topic
```
docker exec -it workshop_kafka_1 kafka-topics.sh --create --partitions 1 --topic testtopic --bootstrap-server 127.0.0.1:9092
```

In a new terminal, test the 'testtopic' you created by running the command below:
```
docker exec -it workshop_kafka_1 kafka-console-consumer.sh --topic testtopic --from-beginning --bootstrap-server 127.0.0.1:9092
```
Type messages into the first prompt and you should see them appear (consumed) in this second prompt. 

#### Creating and Managing Kafka messages in python
```
conda env create -f environment.yml
```

#### Scraping Data 
