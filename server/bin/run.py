import logging
from re import I
import random
import uvicorn
import os


import requests


if __name__ == "__main__":
    uvicorn.run(
        "src.baking.main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8888")),
        log_level=logging.DEBUG,
    )


