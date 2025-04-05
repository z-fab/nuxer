from pydantic import BaseModel


class SlackCommandInput(BaseModel):
    user_id: str
    channel_id: str | None
    command: str
    args: list[str]
