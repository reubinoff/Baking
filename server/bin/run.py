import logging
import uvicorn
import os

if __name__ == "__main__":
    uvicorn.run(
        "src.baking.main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8888")),
        log_level=logging.DEBUG,
    )
