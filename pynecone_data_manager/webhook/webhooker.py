from functools import lru_cache
from fastapi import Depends, FastAPI
from typing_extensions import Annotated
from pydantic import BaseModel

from task_producer import msg_share, logger
from webhookConfig import Settings
from . import state

# Create a FastAPI instance
app = FastAPI()


# Cache the settings
@lru_cache()
def get_settings():
    return Settings()


# Load Flask configurations from config.py
class CatchURL(BaseModel):
    catch_url: str


@app.get("/history", status_code=200)
async def index():
    try:
        all_connections = state.ConnnectionState.get_all_destinantions_history()
        return {all_connections}
    except Exception as e:
        logger.error(str(e))
        return {"ERROR": "An error occurred while querying the database"}, 500


@app.post("/init_webhook", status_code=201)
async def webhook_init(catch_url: CatchURL):
    try:
        logger.debug(f"Webhook URL Registration Requested: {catch_url}")
        try:
            msg_share(catch_url)
        except Exception as e:
            logger.error(str(e))
            return {"Webhook Catch URL Registered": False}, 500
        logger.info(f"Webhook URL Registered: {catch_url}")
        return {"Webhook Catch URL Registered": True}
    except Exception as e:
        logger.error(str(e))
        return {"Webhook Catch URL Registered": False}, 500


if __name__ == "__main__":
    app.run()
