from fastapi import Request
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

from baking.routers.recipe.views import router as recipe_router

from baking.auth.services import get_current_user


class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)

authenticated_api_router = APIRouter()


authenticated_api_router.include_router(
    recipe_router, prefix="/recipe", tags=["recipes"]
)


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}


api_router.include_router(
    authenticated_api_router, dependencies=[Depends(get_current_user)]
)
