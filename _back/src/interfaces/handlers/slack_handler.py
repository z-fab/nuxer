import json
import re

from loguru import logger
from slack_bolt import BoltContext
from slack_sdk import WebClient

from interfaces.handlers.command_mapper import command_mapper
from interfaces.handlers.use_case_dispatcher import use_case_dispatcher
from shared.utils.slack_utils import extract_command


def _extract_message_info(payload: dict) -> dict:
    ts = payload.get("ts")
    text = payload.get("text", "")

    # Remove menções do texto se for app_mention
    if payload.get("type") == "app_mention":
        text = re.sub(r"^\s*<@[^>]+>\s*", "", text)

    command, args = None, None
    if text.startswith("!"):
        command, args = extract_command(text)

    user_id = payload.get("user", None)
    channel_id = payload.get("channel", None)

    return {
        "ts": ts,
        "user_id": user_id,
        "channel_id": channel_id,
        "text": text,
        "command": command,
        "args": args,
    }


def _extract_action_info(payload: dict) -> dict:
    type_container = payload.get("container", {}).get("type", "")
    type_view_id = payload.get("container", {}).get("view_id", None)
    trigger_id = payload.get("trigger_id", None)

    actions = payload.get("actions", [])
    actions = actions[0] if len(actions) > 0 else {}
    actions_type = actions.get("type", "")

    command = None
    args = {}
    if actions_type == "button":
        command = actions.get("action_id", "").split("_")[0]
        args_action = json.loads(actions.get("value", "{}")).values()
        args_action = list(args_action)
        args = dict(enumerate(args_action))

        # Extraindo informações de selects na view
        states = payload.get("view", {}).get("state", {}).get("values", {})
        for element in states.values():
            for key, field in element.items():
                # Verifica se o campo é um select estático
                if field.get("type") == "static_select":
                    args[key] = None
                    if field.get("selected_option") is not None:
                        args[key] = field.get("selected_option", {}).get("value", "")

    user_id = payload.get("user", {}).get("id", None)
    channel_id = payload.get("channel", {}).get("id", None)

    return {
        "type_container": type_container,
        "type_view_id": type_view_id,
        "trigger_id": trigger_id,
        "command": command,
        "args": args,
        "user_id": user_id,
        "channel_id": channel_id,
        "actions_type": actions_type,
    }


def handle_slack_event(context: BoltContext, web_client: WebClient, payload: dict) -> bool:
    type_event = payload.get("type")
    ucr = None

    if type_event == "message" or type_event == "app_mention":
        context_info = _extract_message_info(payload)
    else:
        context_info = _extract_action_info(payload)
        if context_info.get("actions_type") != "button":
            logger.debug(f"Tipo de ação não suportada: {context_info.get('actions_type')}")
            return True

    context_info["source"] = "slack_" + type_event

    if type_event == "message":
        context.set_status("Pensando...")

    # Comando Recebido
    if context_info.get("command"):
        logger.info(
            f"Comando recebido de {context_info.get('user_id')}: {context_info.get('command')} | args: {context_info.get('args')}"
        )

        # Adquire o UseCaseRequest para executar o comando
        ucr = command_mapper(context_info)

    # Sem Comando identificado
    else:
        logger.info(f"Mensagem recebida de {context_info.get('user_id')}: {context_info.get('text')}")
        if type_event == "message" or type_event == "app_mention":
            context.say("Oi, me envie um comando começando com '!' para que eu possa te ajudar :robot_face:")
        return True

    if ucr is None:
        logger.warning("Nenhum Use Case encontrado para ser executado")
        if type_event == "message" or type_event == "app_mention":
            context.say("Desculpe, não consegui entender o que você quis dizer :robot_face:")
        return False

    if not use_case_dispatcher(ucr):
        logger.error("Erro ao executar o Use Case")
        if type_event == "message" or type_event == "app_mention":
            context.say("Desculpe, algo deu errado nos meus bits e bytes e não sei o que responder :robot_face:")
        return False
