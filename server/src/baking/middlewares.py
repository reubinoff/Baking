from asyncio.log import logger
import logging
import functools
from typing import Optional, Sequence
from fastapi import Request, Response
from fastapi import status

from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from baking.database.manage import get_client
from pydantic.error_wrappers import ValidationError
from starlette.middleware.cors import CORSMiddleware


LOGGER = logging.getLogger(__name__)

@functools.lru_cache()
def get_middlewares() -> Optional[Sequence[Middleware]]:
    origins = [
        "*",
    ]

    middlewares = [
        Middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(BaseHTTPMiddleware, dispatch=db_session_middleware),
        Middleware(BaseHTTPMiddleware, dispatch=add_security_headers),
        Middleware(BaseHTTPMiddleware, dispatch=exceptions),
        # Middleware(SentryMiddleware)

    ]

    return middlewares


async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers[
        "Strict-Transport-Security"
    ] = "max-age=31536000 ; includeSubDomains"
    return response


async def db_session_middleware(request: Request, call_next):
    response = Response("Internal Server Error", status_code=500)
    try:
        client = get_client()

        if not client:
            return response

        request.state.db = client
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


async def exceptions(request: Request, call_next) -> Response:
    try:
        response = await call_next(request)
    except ValidationError as e:
        LOGGER.exception(e)
        print(e.errors())
        response = JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": e.errors()},
        )
    except ValueError as e:
        LOGGER.exception(e)
        response = JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": [{"msg": "Unknown", "loc": ["Unknown"], "type": "Unknown"}]
            },
        )

    return response
