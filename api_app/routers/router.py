from fastapi import APIRouter

from core.config import settings
from api_app.routers.users import router as users_router
from api_app.routers.channels import router as channels_router

router_v1 = APIRouter(prefix=settings.api.v1.prefix)

router_v1.include_router(users_router, prefix=settings.api.v1.users, tags=["users"])
router_v1.include_router(channels_router, prefix=settings.api.v1.channels, tags=["channels"])