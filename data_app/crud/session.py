from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from data_app.crud.user import get_user_by_phone
from data_app.models import SessionModel
from data_app.schemas.session import SessionSchema


async def get_session(
    session_data: SessionSchema, session: AsyncSession
) -> SessionModel:
    stmt = select(SessionModel).filter(
        SessionModel.suffix == session_data.suffix,
        SessionModel.phone_number == session_data.phone_number,
    )
    result = await session.scalar(stmt)

    return result


async def save_session_string(session_data: SessionSchema, session: AsyncSession):
    result = await get_session(session_data=session_data, session=session)
    if result is None:
        result = SessionModel(**session_data.model_dump())
        user = await get_user_by_phone(session_data.phone_number)
        result.user = user
        result.created_at = datetime.now(timezone.utc).replace(tzinfo=None)
        session.add(result)

    else:
        result.session_string = session_data.session_string

    await session.commit()


async def get_session_string(session_data: SessionSchema, session: AsyncSession) -> str:
    result = await get_session(session_data=session_data, session=session)

    return getattr(result, "session_string", None)
