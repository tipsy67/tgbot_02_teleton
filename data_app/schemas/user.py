from pydantic import BaseModel


class UserSchema(BaseModel):
    phone: str
    is_active: bool
