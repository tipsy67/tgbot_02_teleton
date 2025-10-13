
from sqlalchemy import select

from core.db_helper import db_helper
from data_app.models import UserModel


async def get_active_users() -> list[UserModel]:
    async with db_helper.session_factory() as session:
        stmt = select(UserModel).filter(UserModel.is_active == True)
        result = await session.scalars(stmt)

    return result.all()


async def get_user_by_phone(phone_number:str) -> UserModel:
    async with db_helper.session_factory() as session:
        stmt = select(UserModel).filter(UserModel.phone_number == phone_number)
        result = await session.scalar(stmt)

    return result

async def get_user_by_id(user_id:int) -> UserModel:
    async with db_helper.session_factory() as session:
        stmt = select(UserModel).filter(UserModel.id == user_id)
        result = await session.scalar(stmt)

    return result