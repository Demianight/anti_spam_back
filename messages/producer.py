import json
from logging import getLogger

from quixstreams import Application

logger = getLogger(__name__)
logger.setLevel("DEBUG")

kafka = Application(
    broker_address="10.10.127.2:9092",
)


def send_message_to_kafka(message_dict: dict, topic: str = "spam_messages"):
    with kafka.get_producer() as producer:
        producer.produce(
            topic=topic,
            value=json.dumps(message_dict),
        )
    logger.debug(f"Produced message to Kafka: {message_dict}")
