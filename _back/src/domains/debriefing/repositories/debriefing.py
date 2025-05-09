from datetime import datetime
from zoneinfo import ZoneInfo

from loguru import logger

from domains.debriefing.mapper.debriefing import notion_to_entity
from shared.infrastructure.notion_context import notion


class DebriefingRepository:
    def __init__(self):
        self._notion = notion

    def get_debriefing_by_page_id(self, page_id: str):
        try:
            response = self._notion.pages.retrieve(page_id=page_id)
            return notion_to_entity(response)

        except Exception as e:
            logger.error(f"Erro ao buscar debriefing: {e}")

    def update_ultimo_envio(self, page_id: str, data: datetime | None = None) -> bool:
        if data is None:
            data = datetime.now(tz=ZoneInfo("America/Sao_Paulo"))

        properties = {
            "ultimo_envio": {
                "date": {
                    "start": data.isoformat(),
                },
            },
        }
        return self._update_debriefing(page_id, properties)

    def _update_debriefing(self, page_id: str, properties: dict) -> bool:
        try:
            self._notion.pages.update(page_id=page_id, properties=properties)
            return True
        except Exception as e:
            logger.error(f"Erro ao atualizar debriefing: {e}")
