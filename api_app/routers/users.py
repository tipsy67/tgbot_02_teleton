import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette import status

from core.config import settings
from core.db_helper import db_helper
from data_app.crud.user import get_active_users

log = logging.getLogger(__name__)
router = APIRouter()


@router.get("")
async def get_users(session: AsyncSession = Depends(db_helper.session_getter)):
    user = await get_active_users(session)
    return user


# @router.post("", status_code=status.HTTP_200_OK, response_model=UserResponse)
# async def set_user_rt(
#     tg_user: UserCreateUpdate,
#     session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
# ):
#     user = await set_user(tg_user, session)
#     return user



