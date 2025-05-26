from pydantic import BaseModel


class SlackCommandInput(BaseModel):
    user_id: str
    channel_id: str | None
    text: str | None
    command: str | None
    args: list[str] | None
