# interfaces/presenters/slack/base_presenter.py


from loguru import logger

from shared.infrastructure.slack_context import slack
from shared.utils.slack_utils import text_to_blocks


class BaseSlackPresenter:
    def __init__(self, request_payload: dict):
        self.slack = slack
        self.request_payload = request_payload

    def _get_user_id(self) -> str | None:
        return self.request_payload.get("user_id")

    def _get_channel_id(self) -> str | None:
        return self.request_payload.get("channel_id")

    def _get_thread_ts(self) -> str | None:
        return self.request_payload.get("ts")

    def _get_trigger_id(self) -> str | None:
        return self.request_payload.get("trigger_id")

    def _get_view_id(self) -> str | None:
        return self.request_payload.get("type_view_id")

    def _get_container_type(self) -> str | None:
        return self.request_payload.get("type_container")

    def _get_source(self) -> str | None:
        return self.request_payload.get("source", "")

    def _say(self, message: str, alt_text: str = "Nova mensagem"):
        """Envia uma mensagem para o canal/thread da requisição original ou DM."""
        target_channel_id = self._get_channel_id()
        target_user_id = self._get_user_id()
        thread_ts = self._get_thread_ts()

        # Verifica se a origem é uma mensagem em canal ou menção em canal
        # e não uma interação de view que não tem um channel_id óbvio para resposta direta de mensagem.
        source_type = self._get_source()

        if target_channel_id and source_type.startswith("slack_app_mention"):
            self.slack.send_message(target_channel_id, text=message, alt_text=alt_text, thread_ts=thread_ts)
        elif target_user_id:
            self.slack.send_dm(target_user_id, text=message, alt_text=alt_text, thread_ts=thread_ts)
        else:
            logger.error(f"Não foi possível enviar mensagem, sem channel_id ou user_id no payload: {message}")

    def _send_dm_to_user(self, user_id: str, message: str, alt_text: str = "Nova mensagem"):
        if user_id:
            self.slack.send_dm(user_id, text=message, alt_text=alt_text)
        else:
            logger.error(f"Não foi possível enviar DM, user_id não fornecido: {message}")

    def _send_message_to_channel(self, channel_id: str, message: str, alt_text: str = "Nova mensagem"):
        if channel_id:
            self.slack.send_message(channel_id, text=message, alt_text=alt_text)
        else:
            logger.error(f"Não foi possível enviar mensagem ao canal, channel_id não fornecido: {message}")

    def _set_view(self, content: str, title: str):
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
        type_container = self._get_container_type()

        if type_container != "view":
            self._open_slack_view(view_payload=view, title=title)
        else:
            self._update_slack_view(view_payload=view, title=title)

    def _open_slack_view(self, view_payload: dict, title: str = "Nuxer"):
        trigger_id = self._get_trigger_id()
        if trigger_id:
            view_payload.setdefault("title", {"type": "plain_text", "text": title, "emoji": True})
            view_payload.setdefault("close", {"type": "plain_text", "text": "Fechar", "emoji": True})
            self.slack.open_view(trigger_id=trigger_id, view=view_payload)
        else:
            logger.error("Não foi possível abrir a view: trigger_id ausente no payload.")

    def _update_slack_view(self, view_payload: dict, title: str = "Nuxer"):
        view_id = self._get_view_id()
        if view_id:
            view_payload.setdefault("title", {"type": "plain_text", "text": title, "emoji": True})
            view_payload.setdefault("close", {"type": "plain_text", "text": "Fechar", "emoji": True})

            try:
                self.slack.update_view(view_id=view_id, view=view_payload)
            except Exception as e:
                logger.error(f"Erro ao atualizar view {view_id}: {e}")
                # Fallback: tentar abrir uma nova se a atualização falhar (ou notificar o usuário)
                trigger_id = self._get_trigger_id()
                if trigger_id:
                    self.slack.open_view(trigger_id=trigger_id, view=view_payload)
                else:
                    self._send_dm_to_user(self._get_user_id(), "Houve um problema ao atualizar a tela.")

        else:
            logger.error("Não foi possível atualizar a view: view_id ausente no payload.")
