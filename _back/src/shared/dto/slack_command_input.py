import json
from collections.abc import Callable

from pydantic import BaseModel

from shared.utils.slack_utils import text_to_blocks


class SlackCommandInput(BaseModel):
    user_id: str
    channel_id: str
    type_message: str
    ts: str | None
    command: str
    args: list[str]
    func_set_status: Callable[[str], None] | None
    func_say: Callable[[str], None]

    def set_status(self, status: str):
        if self.type_message == "message":
            self.func_set_status(status)
        else:
            self.say(status)

    def say(self, message: str, alt_text: str = "Há uma nova mensagem"):
        blocks = text_to_blocks(message)

        blocks_send = 0
        ts = self.ts
        while blocks_send < len(blocks):
            message = json.dumps(blocks[blocks_send : blocks_send + 49])
            response = self.func_say(blocks=message, text=alt_text, thread_ts=ts)
            ts = response.get("ts")
            blocks_send += 49
