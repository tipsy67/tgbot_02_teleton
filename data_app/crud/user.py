
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_app.models import UserModel


async def get_active_users(session: AsyncSession) -> list[UserModel]:
    stmt = select(UserModel).filter(UserModel.is_active == True)
    result = await session.scalars(stmt)

    return result.all()


async def get_user_by_phone(phone_number:str, session: AsyncSession) -> UserModel:
    stmt = select(UserModel).filter(UserModel.phone_number == phone_number)
    result = await session.scalar(stmt)

    return result

async def get_user_by_id(user_id:int, session: AsyncSession) -> UserModel:
    stmt = select(UserModel).filter(UserModel.id == user_id)
    result = await session.scalar(stmt)

    return result