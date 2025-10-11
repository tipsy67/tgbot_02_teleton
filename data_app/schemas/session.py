from pydantic import BaseModel


class SessionSchema(BaseModel):
    api_id: int
    session_string: str
    suffix: str