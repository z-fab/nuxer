from loguru import logger

from interfaces.presenters.slack.message.presenter import MessagePresenter
from shared.dto.use_case_response import UseCaseResponse
from shared.infrastructure.slack_context import slack


def slack_notifier(use_case_response: UseCaseResponse):
    if use_case_response.notification:
        # Para cada notificação, renderiza a mensagem
        for notification in use_case_response.notification:
            if notification.get("user"):
                if notification.get("presenter_hint"):
                    presenter = MessagePresenter()
                    rendered_message = presenter.render(use_case_response.data, notification.get("presenter_hint"))
                    user_to_notify = notification.get("user")

                else:
                    # Se não houver presenter_hint, renderiza a mensagem padrão
                    rendered_message = (
                        use_case_response.message
                        or "Desculpe, algo deu errado nos meus bits e bytes e não sei o que responder :robot_face:"
                    )

                logger.info(
                    f"Notificando {notification.get('user').nome} ({notification.get('user').slack_id}) sobre: {rendered_message}"
                )
                slack.send_dm(user=user_to_notify.slack_id, text=rendered_message)
            else:
                logger.warning(f"Notificação sem usuário: {notification.get('presenter_hint')}")
    else:
        logger.warning("Nenhuma notificação encontrada: {use_case_response}")
