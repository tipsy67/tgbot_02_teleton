
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_app.models import ChannelModel


async def get_users_channels(user_id:int, session: AsyncSession) -> list[ChannelModel]:
    stmt = select(ChannelModel).filter(ChannelModel.user_id == user_id)
    result = await session.scalars(stmt)

    return result.all()

async def get_id_users_channels(user_id:int, session: AsyncSession) -> list[ChannelModel]:
    stmt = select(ChannelModel.chat_id).filter(ChannelModel.user_id == user_id)
    result = await session.scalars(stmt)

    return result.all()



