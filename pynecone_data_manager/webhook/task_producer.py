import json
import logging
import sys

import requests
from confluent_kafka import Consumer

# URL = "https://6b7c3309-a6ac-46d8-b8e4-e45cffa50c20.mock.pstmn.io"


def read_ccloud_config(config_file):
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split("=", 1)
                conf[parameter] = value.strip()
        return conf


props = read_ccloud_config("client.properties")
props["group.id"] = "python-group-1"
props["auto.offset.reset"] = "earliest"
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

file_handler = logging.FileHandler("logs/runtime_logs.log")
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
#!SECTION = Logging Configurations


# SECTION - Webhook Transmission Logic
def send_webhook(msg: str, destination_url: str) -> int:
    """Send a webhook to a  a specified URL.

    Args:
    ----
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
def msg_share(URL: str) -> None:
    """The utility function that will be called to send the messages.

    Args:
    ----
    ::param URL: The ip address of the kafka server that will be used to forward the messages (Heroku/AWS/Google Cloud)
    ::return: None
    """
    try:
        consumer = Consumer(props)
        consumer.subscribe(["orders", "users"])
    except Exception as e:
        logger.error(f"First Level of Failure {str(e)}")
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is not None and msg.error() is None:
                resp = requests.post(URL, msg.value().decode("utf-8"))
                logger.info(
                    f"-- Status = {resp} | -- Message = {msg.value().decode('utf-8')}"
                )
    except Exception as e:
        logger.error(f"Second Level Failure {str(e)}")


#!SECTION - Kafka Message Consumption and Transmissions (Core Logic)
# # msg_share("https://6b7c3309-a6ac-46d8-b8e4-e45cffa50c20.mock.pstmn.io/alerts")
# if "__main__" == __name__:
#     msg_share()
