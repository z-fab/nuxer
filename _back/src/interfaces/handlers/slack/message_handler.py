import json
import re
from functools import partial

from loguru import logger
from slack_bolt import BoltContext

from interfaces.handlers.slack.command_handler import handle_command
from interfaces.presenters.slack.message.presenter import MessagePresenter
from shared.dto.slack_command_input import SlackCommandInput
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

    say_fn = context.get("say")
    set_status_fn = context.get("set_status")
    type_message = payload.get("type")
    ts = payload.get("ts")

    # Remove menções do texto se for app_mention
    if payload.get("type") == "app_mention":
        text = re.sub(r"^\s*<@[^>]+>\s*", "", text)

    if text.startswith("!"):
        command, args = extract_command(text)

        input_data = SlackCommandInput(
            user_id=payload.get("user"),
            channel_id=payload.get("channel"),
            command=command,
            args=args,
        )

        composed_set_status = partial(set_status, set_status_fn, say_fn, type_message, ts)

        logger.info(f"Comando recebido de {input_data.user_id}: {command} | args: {args}")
        use_case_response = handle_command(input_data, composed_set_status)

        # Verifica se há notificações definidas
        if use_case_response.notification:
            # Para cada notificação, renderiza a mensagem
            for notification in use_case_response.notification:
                if notification.get("presenter_hint"):
                    presenter = MessagePresenter()
                    rendered_message = presenter.render(use_case_response, notification.get("presenter_hint"))

                    # Notifica o usuário
                    if not notification.get("user"):
                        say(say_fn, rendered_message, ts=ts)
                    # Notifica o usuário específico
                    else:
                        user_to_notify = notification.get("user")
                        logger.info(
                            f"Notificando {user_to_notify.nome} ({user_to_notify.slack_id}) sobre: {rendered_message}"
                        )
                        slack.send_dm(user=notification.get("user").slack_id, text=rendered_message)
                else:
                    # Se não houver presenter_hint, renderiza a mensagem padrão
                    message = (
                        use_case_response.message
                        or "Desculpe, algo deu errado nos meus bits e bytes e não sei o que responder :robot_face:"
                    )
                    say(say_fn, message, ts=ts)
        else:
            # Se não houver notificações, renderiza a mensagem padrão
            message = (
                use_case_response.message
                or "Desculpe, algo deu errado nos meus bits e bytes e não sei o que responder :robot_face:"
            )
            say(say_fn, message, ts=ts)

    # Não é um comando, então apenas responde com uma mensagem padrão
    else:
        logger.debug(f"Mensagem recebida de {payload.get('user')}: {text}")
        say(say_fn, "Não entendi o que você disse :robot_face:", ts=ts)

    return True
