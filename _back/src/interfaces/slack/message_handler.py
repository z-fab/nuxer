# from externals.slack_external import send_message, set_status
# from interfaces.slack.command_handler import handle_command
import re

from slack_bolt import BoltContext

from interfaces.slack.command_handler import handle_command
from shared.dto.slack_command_input import SlackCommandInput
from shared.utils.slack_utils import extract_command


def handle_message_event(context: BoltContext, payload: dict) -> bool:
    command = ""
    args = []
    text = payload.get("text", "")

    if payload.get("type") == "app_mention":
        text = re.sub(r"^\s*<@[^>]+>\s*", "", text)

    if text.startswith("!"):
        command, args = extract_command(text)

        input_data = SlackCommandInput(
            user_id=payload.get("user"),
            channel_id=payload.get("channel"),
            type_message=payload.get("type"),
            ts=payload.get("ts"),
            command=command,
            args=args,
            func_set_status=context.get("set_status"),
            func_say=context.get("say"),
        )

        return handle_command(input_data)

    else:
        context.get("say")(text=":warning: Desculpe, não entendi o que você quis dizer. Tente novamente.")

    return False
