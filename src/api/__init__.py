from fastapi import APIRouter

from src.api.v1.snippet import snippet_router
from src.api.v1.auth import auth_router

api_router = APIRouter()

api_router.include_router(snippet_router)
api_router.include_router(auth_router)
