from pydantic import BaseModel


class SessionSchema(BaseModel):
    phone_number: str
    session_string: str
    suffix: str
    user_id: int|None = None
