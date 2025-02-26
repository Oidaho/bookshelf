from fastapi import APIRouter

from .authors import router as authors_router
from .books import router as books_router
from .health import router as health_router
from .publishers import router as publishers_router
from .readers import router as readers_router
from .issuances import router as issuances_router

api_router = APIRouter(prefix="/api")

api_router.include_router(health_router)
api_router.include_router(publishers_router)
api_router.include_router(authors_router)
api_router.include_router(readers_router)
api_router.include_router(books_router)
api_router.include_router(issuances_router)

__all__ = ("api_router",)
