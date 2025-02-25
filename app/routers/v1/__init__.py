from fastapi import APIRouter
from .health import router as health_router
from .publishers import router as publishers_router
from .authors import router as authors_router

router = APIRouter(prefix="/v1")

router.include_router(health_router)
router.include_router(publishers_router)
router.include_router(authors_router)

__all__ = ("router",)
