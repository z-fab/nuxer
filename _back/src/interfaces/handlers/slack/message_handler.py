import json
import re
from functools import partial

from loguru import logger
from slack_bolt import BoltContext

from interfaces.handlers.slack.command_handler import handle_command
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.slack_context import slack
from shared.utils.slack_utils import extract_command, text_to_blocks


def say(fn_say, message: str, alt_text: str = "Há uma nova mensagem", ts: str | None = None):
    blocks = text_to_blocks(message)

    blocks_send = 0
    current_ts = ts
    while blocks_send < len(blocks):
        sliced_blocks = json.dumps(blocks[blocks_send : blocks_send + 49])
        response = fn_say(blocks=sliced_blocks, text=alt_text, thread_ts=current_ts)
        current_ts = response.get("ts")
        blocks_send += 49


def set_status(fn_set_status, fn_say, type_message: str, ts: str | None, status: str):
    if type_message == "message":
        fn_set_status(status)
    else:
        say(fn_say, status, ts=ts)


def handle_message_event(context: BoltContext, payload: dict) -> bool:
    command = ""
    args = []
    text = payload.get("text", "")

    # Remove menções do texto se for app_mention
    if payload.get("type") == "app_mention":
        text = re.sub(r"^\\s*<@[^>]+>\\s*", "", text)

    if text.startswith("!"):
        command, args = extract_command(text)

        input_data = SlackCommandInput(
            user_id=payload.get("user"),
            channel_id=payload.get("channel"),
            command=command,
            args=args,
        )

        # Referência às funções do Slack
        say_fn = context.get("say")
        set_status_fn = context.get("set_status")
        type_message = payload.get("type")
        ts = payload.get("ts")
        composed_set_status = partial(set_status, set_status_fn, say_fn, type_message, ts)

        logger.info(f"Comando recebido de {input_data.user_id}: {command} | args: {args}")
        use_case_response: UseCaseResponse = handle_command(input_data, composed_set_status)

        # Comunicação com o usuário
        if use_case_response.success:
            say(say_fn, use_case_response.message, ts=ts)
            if use_case_response.data:
                notify = use_case_response.data.get("notify")
                if notify:
                    logger.info(
                        f"Notificando {notify['user'].nome} ({notify['user'].slack_id}) sobre: {notify['message']}"
                    )
                    slack.send_dm(user=notify["user"].slack_id, text=notify["message"], alt_text=notify["message"])
        else:
            fallback = use_case_response.message or "Desculpe, algo deu errado nos meus bits e bytes :robot_face:"
            say(say_fn, fallback, ts=ts)

    else:
        logger.debug(f"Mensagem recebida de {payload.get('user')}: {text}")
        context.get("say")(text="Desculpe, algo deu errado nos meus bits e bytes :robot_face:")

    return True
