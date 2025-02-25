from fastapi import APIRouter
from .health import router as health_router
from .publishers import router as publishers_router
from .authors import router as authors_router

api_router = APIRouter(prefix="/api")

api_router.include_router(health_router)
api_router.include_router(publishers_router)
api_router.include_router(authors_router)

__all__ = ("api_router",)
