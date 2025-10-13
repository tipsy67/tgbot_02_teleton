from pydantic import BaseModel


class ChannelSchema(BaseModel):
    chat_id: int
    prompt: str
    system_prompt: str
