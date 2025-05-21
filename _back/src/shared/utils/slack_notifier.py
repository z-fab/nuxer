from loguru import logger

from interfaces.presenters.slack.message.presenter import MessagePresenter
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.slack_context import slack


def slack_notifier(use_case_response: UseCaseResponse):
    if use_case_response.notification:
        # Para cada notificação, renderiza a mensagem
        for notification in use_case_response.notification:
            if notification.get("presenter_hint"):
                presenter = MessagePresenter()
                use_case_response.data["user"] = notification.get("user")
                use_case_response.data["channel"] = notification.get("channel")
                rendered_message = presenter.render(use_case_response.data, notification.get("presenter_hint"))
            else:
                rendered_message = (
                    use_case_response.message
                    or "Desculpe, algo deu errado nos meus bits e bytes e não sei o que responder :robot_face:"
                )

            if notification.get("user"):
                user_to_notify = notification.get("user")
                logger.info(
                    f"Notificando {notification.get('user').nome} ({notification.get('user').slack_id}) sobre: {rendered_message}"
                )
                slack.send_dm(user=user_to_notify.slack_id, text=rendered_message)

            elif notification.get("channel"):
                channel_to_notify = notification.get("channel")
                logger.info(f"Notificando canal {channel_to_notify} sobre: {rendered_message}")
                slack.send_message(channel=channel_to_notify, text=rendered_message)

            else:
                logger.warning(f"Notificação sem usuário ou channel: {notification.get('presenter_hint')}")

    else:
        logger.warning("Nenhuma notificação encontrada: {use_case_response}")
