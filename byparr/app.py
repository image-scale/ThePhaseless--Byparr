from __future__ import annotations

import asyncio
import logging
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from byparr.browser import create_browser_session
from byparr.config import HOST, LOG_LEVEL, PORT, VERSION
from byparr.helpers import logger
from byparr.logging_middleware import RequestLogger
from byparr.routes import api_router, check_health

logger.info("Using version %s", VERSION)
logger.info("Log level set to %s", logging.getLevelName(LOG_LEVEL))

app = FastAPI(debug=LOG_LEVEL == logging.DEBUG, log_level=LOG_LEVEL)
app.add_middleware(GZipMiddleware)
app.add_middleware(RequestLogger)
app.include_router(router=api_router)


async def initialize():
    async for session in create_browser_session():
        await check_health(session)


if __name__ == "__main__":
    if "--init" in sys.argv:
        logger.info("Running initialization script...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(initialize())
        logger.info("Initialization complete.")
    else:
        uvicorn.run(app, host=HOST, port=PORT)
