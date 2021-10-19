from fastapi import Request
from fastapi.responses import JSONResponse

from pydantic.errors import PydanticValueError


async def base_error_handler(req: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "error-class": exc.__class__.__name__,
            "url": str(req.url),
        },
    )


class FieldNotFound(Exception):
    pass


class FieldNotFoundError(PydanticValueError):
    code = "not_found.field"
    msg_template = "{msg}"


class BadFilterFormat(Exception):
    pass


class InvalidFilterError(PydanticValueError):
    code = "invalid.filter"
    msg_template = "{msg}"
