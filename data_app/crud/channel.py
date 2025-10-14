
from sqlalchemy import select

from core.db_helper import db_helper
from data_app.models import SessionModel, UserModel, ChannelModel


async def get_users_channels(user_id:int) -> list[ChannelModel]:
    async with db_helper.session_factory() as session:
        stmt = select(ChannelModel).filter(ChannelModel.user_id == user_id)
        result = await session.scalars(stmt)

    return result.all()

async def get_id_users_channels(user_id:int) -> list[ChannelModel]:
    async with db_helper.session_factory() as session:
        stmt = select(ChannelModel.chat_id).filter(ChannelModel.user_id == user_id)
        result = await session.scalars(stmt)

    return result.all()



