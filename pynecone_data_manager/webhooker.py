import logging
import sys
from functools import lru_cache

import pendulum
from fastapi import FastAPI
from pydantic import BaseModel
from state import ConnectionState
from webhook.task_producer import logger, msg_share
from webhook.webhookConfig import Settings

now = pendulum.now()
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
# Create a FastAPI instance
app = FastAPI()


# Cache the settings
@lru_cache()
def get_settings():
    return Settings()


# Load Flask configurations from config.py
class DestinatioSubmission(BaseModel):
    name: str
    desc: str
    catch_url: str


@app.get("/health", status_code=200)
async def health():
    return {"status": "OK - Webhook API is running"}


# @app.get("/history", status_code=200)
# async def index():
#     try:
#         all_connections = ConnnectionState.get_all_destinantions_history()
#         return {all_connections}
#     except Exception as e:
#         logger.error(str(e))
#         return {"ERROR": "An error occurred while querying the database"}, 500


@app.post("/init_webhook", status_code=201)
async def webhook_init(Destination: DestinatioSubmission):
    try:
        logger.debug(f"Webhook URL Registration Requested: {Destination.catch_url}")
        logger.debug(f"Webhook Name: {Destination.name}")
        logger.debug(f"Webhook Description: {Destination.desc}")
        try:
            logger.debug(f"Webhook URL Registration Requested: {Destination.catch_url}")
            msg_share(Destination.catch_url)
            logger.debug(
                f"Webhook URL Registered Successfully: {Destination.catch_url}"
            )
            try:
                ConnectionState.create_destination(
                    Destination.name,
                    Destination.desc,
                    True,
                    Destination.catch_url,
                    now.to_datetime_string(),
                )
            except Exception as e:
                logger.error(str(e))
                return {"Webhook Catch URL Registered": False}, 500
        except Exception as e:
            logger.error(str(e))
            return {"Webhook Catch URL Registered": False}, 500
        logger.info(f"Webhook URL Registered: {Destination.catch_url}")
        return {"Webhook Catch URL Registered": True}
    except Exception as e:
        logger.error(str(e))
        return {"Webhook Catch URL Registered": False}, 500


if __name__ == "__main__":
    app.run()
