# from externals.slack_external import send_message, set_status
# from interfaces.slack.command_handler import handle_command

import json

from loguru import logger
from slack_sdk import WebClient

from interfaces.handlers.slack.command_handler import handle_command
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.slack_context import slack
from shared.utils.slack_utils import text_to_blocks


def set_view(content: str, type_container: str, client, type_view_id, trigger_id):
    view = {
        "type": "modal",
        "title": {"type": "plain_text", "text": "Teste", "emoji": True},
        "close": {"type": "plain_text", "text": "Fechar", "emoji": True},
        "private_metadata": "",
        "blocks": [],
    }
    if isinstance(content, str):
        content = text_to_blocks(content)
    view["blocks"] = content

    if type_container != "view":
        client.views_open(trigger_id=trigger_id, view=view)
    else:
        client.views_update(view_id=type_view_id, view=view)


def handle_action_event(payload: dict, client: WebClient) -> bool:
    type_container = payload.get("container", {}).get("type", "")
    type_view_id = payload.get("container", {}).get("view_id", None)
    trigger_id = payload.get("trigger_id", None)

    actions = payload.get("actions", [])
    actions = actions[0] if len(actions) > 0 else {}

    command = actions.get("action_id", "").split("_")[0]
    args = json.loads(actions.get("value", "{}"))

    input_data = SlackCommandInput(
        user_id=payload.get("user", {}).get("id"),
        channel_id=payload.get("channel", {}).get("id"),
        command=command,
        args=args.values(),
    )

    logger.info(f"Ação feita por {input_data.user_id}: {input_data.command} | args: {input_data.args}")
    use_case_response: UseCaseResponse = handle_command(input_data, lambda set_status: None)

    message = "Desculpe, algo deu errado nos meus bits e bytes :robot_face:"
    if use_case_response.message:
        message = use_case_response.message

    set_view(message, type_container, client, type_view_id, trigger_id)
    if use_case_response.data:
        notify = use_case_response.data.get("notify")
        if notify:
            logger.info(f"Notificando {notify['user'].nome} ({notify['user'].slack_id}) sobre: {notify['message']}")
            slack.send_dm(user=notify["user"].slack_id, text=notify["message"], alt_text=notify["message"])
