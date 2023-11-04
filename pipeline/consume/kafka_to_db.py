from confluent_kafka import Consumer, KafkaError
import json

from settings import KAFKA_CONFIGS, KAFKA_TOPIC
from common import HockeyTeamResults

def push_to_sqlite():
    consumer = Consumer({
        "bootstrap.servers": KAFKA_CONFIGS["bootstrap.servers"],
        "group.id": "sqlite",
        "auto.offset.reset": "earliest"
    })

    consumer.subscribe([KAFKA_TOPIC])

    data = []
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            # No more messages
            break
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        data.append(json.loads(msg.value().decode("utf-8")))

    print(data[0])
    consumer.close()