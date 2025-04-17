import json

from loguru import logger
from slack_sdk import WebClient

from interfaces.handlers.slack.command_handler import handle_command
from interfaces.presenters.slack.view.presenter import ViewPresenter
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.slack_context import slack
from shared.utils.slack_utils import text_to_blocks


def set_view(content: str, title: str, type_container: str, client, type_view_id, trigger_id):
    title = title or "Nuxer"
    view = {
        "type": "modal",
        "title": {"type": "plain_text", "text": title, "emoji": True},
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

    # Verifica se há notificações definidas
    if use_case_response.notification:
        for notification in use_case_response.notification:
            if notification.get("presenter_hint"):
                presenter = ViewPresenter()
                title_view, rendered_message = presenter.render(
                    use_case_response.data, notification.get("presenter_hint")
                )

                # Notifica o usuário
                if not notification.get("user"):
                    set_view(rendered_message, title_view, type_container, client, type_view_id, trigger_id)

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
                slack.send_dm(user=input_data.user_id, text=message)
    else:
        # Se não houver notificações, renderiza a mensagem padrão
        message = (
            use_case_response.message
            or "Desculpe, algo deu errado nos meus bits e bytes e não sei o que responder :robot_face:"
        )
        slack.send_dm(user=input_data.user_id, text=message)
