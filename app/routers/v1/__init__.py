from fastapi import APIRouter
from .health import health_router

router = APIRouter(prefix="/v1")

router.include_router(health_router)

__all__ = ("router",)
