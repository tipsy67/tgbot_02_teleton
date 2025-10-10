from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from data_app.models import SessionModel
from data_app.schemas.session import SessionSchema


async def get_session(api_id: int , session: AsyncSession) -> SessionModel:
    stmt = select(SessionModel).filter(SessionModel.api_id == api_id)
    result = await session.scalar(stmt)

    return result

async def save_session_string(session_data:SessionSchema):
    async with db_helper.session_factory() as session:
        result = await get_session(api_id=session_data.api_id, session=session)
        if result is None:
            result = SessionModel(**session_data.model_dump())
            result.created_at = datetime.now(timezone.utc).replace(tzinfo=None)
            session.add(result)

        else:
            result.session_string = session_data.session_string

        await session.commit()



async def get_session_string(api_id:int) -> str:
    async with db_helper.session_factory() as session:
        result = await get_session(api_id=api_id, session=session)

    return getattr(result, "session_string", None)