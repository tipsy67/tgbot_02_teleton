from fastapi import APIRouter

from core.config import settings
from api_app.routers.router import router_v1

router = APIRouter(prefix=settings.api.prefix)

router.include_router(router_v1)
