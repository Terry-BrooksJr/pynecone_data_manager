#!/usr/bin/python3
import requests

import json
import logging
import sys
import argparse

from kafka import KafkaConsumer


# SECTION -  Logging Configurations
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename="error.log",
    filemode="w",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)

file_handler = logging.FileHandler("error.log")
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
#!SECTION = Logging Configurations


# SECTION - Webhook Transmission Logic
def send_webhook(msg: str, destination_url: str) -> int:
    """Send a webhook to a  a specified URL

    Args:
    :param msg: task details
    :return status_code: Result of HTTP POST Request
    """
    try:
        resp = requests.post(
            destination_url,
            data=json.dumps(msg, sort_keys=True, default=str),
            headers={"Content-Type": "application/json"},
            timeout=1.0,
        )
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.error("An HTTP Error occurred", repr(err))
        pass
    except requests.exceptions.ConnectionError as err:
        logger.error("An Error Connecting to the API occurred", repr(err))
        pass
    except requests.exceptions.Timeout as err:
        logger.error("A Timeout Error occurred", repr(err))
        pass
    except requests.exceptions.RequestException as err:
        logger.error("An Unknown Error occurred", repr(err))
        pass
    except Exception as e:
        logger.error(str(e))
        pass
    else:
        return resp.status_code


#!SECTION - Webhook Transmission Logic


# SECTION - Kafka Message Consumption and Transmissions (Core Logic)
def msg_share(destination_url: str) -> None:
    """
    ::param stream_ids: The list stream id that is assigned by the Chooch Dashboard you want to forward predictions from
    ::param kafka_server_ip: The ip address of the kafka server that will be used to forward the messages (Heroku/AWS/Google Cloud)
    ::param kafka_topic: The topic to which the messages will be forwarded to at the kafka server ip
    ::return: None
    """
    consumer = KafkaConsumer(
        bootstrap_servers="ec2-44-210-36-238.compute-1.amazonaws.com:9092",
        auto_offset_reset="earliest",
    )
    topic_list = [topic for topic in consumer.topics()]
    for topic in topic_list:
        if "alert" in topic:
            logger.info(f"Successfully subscribed to {topic}")

    consumer.subscribe("demo_messages")

    for message in consumer:
        msg = message.value.decode("utf-8")
        msg = json.loads(msg)
        resp = send_webhook(msg, destination_url)
        logger.info(" -- Status", resp, " -- Message \= ", msg)
        yield resp


#!SECTION - Kafka Message Consumption and Transmissions (Core Logic)
msg_share("https://6b7c3309-a6ac-46d8-b8e4-e45cffa50c20.mock.pstmn.io/alerts")
# if "__main__" == __name__:
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--destination_url", type=str, required=True, default="")
#     args = parser.parse_args()
#     msg_share(args.destination_url)
