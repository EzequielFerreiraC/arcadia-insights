"""
API v1 Routes Module
"""
from fastapi import APIRouter
from c_api.src.presentation.api.v1.routes import players, saves, analytics, platform, ml

router = APIRouter(prefix="/v1")

# Include route modules
router.include_router(players.router)
router.include_router(saves.router)
router.include_router(analytics.router)
router.include_router(platform.router)
router.include_router(ml.router)

__all__ = ["router"]
