import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session  import AsyncSession

from core.db_helper import db_helper
from data_app.crud.channel import get_channels

log = logging.getLogger(__name__)
router = APIRouter()


@router.get("")
async def get_users(session: AsyncSession = Depends(db_helper.session_getter)):
    channels = await get_channels(session)
    return channels