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
