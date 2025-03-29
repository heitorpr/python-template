from fastapi import APIRouter

from .routes import app_router, hero_router

api_router = APIRouter()
api_router.include_router(app_router, tags=["app"])
api_router.include_router(hero_router, prefix="/heroes", tags=["heroes"])
