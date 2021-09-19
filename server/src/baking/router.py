from fastapi import Request
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from baking.routers.recipe.views import router as recipe_router
from baking.auth.services import get_current_user

api_router = APIRouter(default_response_class=JSONResponse)

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
