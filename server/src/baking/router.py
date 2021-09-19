
from fastapi import Request
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse


api_router = APIRouter(
    default_response_class=JSONResponse
)
