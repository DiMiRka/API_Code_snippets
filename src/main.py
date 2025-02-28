import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from asyncpg.pool import logger
from requests import Request
import logging.config
import logging.handlers
import atexit
from contextlib import asynccontextmanager
from typing import AsyncContextManager

from src.core.logger import LOGGING_CONFIG
from src.api import api_router
from src.core.config import uvicorn_options


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncContextManager[None]:
    logging.config.dictConfig(LOGGING_CONFIG)
    queue_handler = logging.getHandlerByName("queue_handler")
    try:
        if queue_handler is not None:
            queue_handler.listener.start()
            atexit.register(queue_handler.listener.stop)
        yield
    finally:
        if queue_handler is not None:
            queue_handler.listener.stop()

app = FastAPI(docs_url="/api/openapi", lifespan=lifespan)

app.include_router(api_router)


@app.exception_handler(Exception)
async def exception(request: Request, exc: Exception):
    logger.error(f"{request.url} | Error in application: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": exc}
    )


@app.exception_handler(HTTPException)
async def exception(request: Request, exc: HTTPException):
    logger.error(f"{request.url} | Error in application: {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


if __name__ == '__main__':
    print(uvicorn_options)
    uvicorn.run(
        'main:app',
        **uvicorn_options
    )
