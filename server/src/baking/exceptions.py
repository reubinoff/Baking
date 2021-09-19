from fastapi import Request
from fastapi.responses import JSONResponse


async def base_error_handler(req: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "error-class": exc.__class__.__name__, "url": str(req.url)},
    )
