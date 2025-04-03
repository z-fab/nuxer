from .database_external import DatabaseExternal
from .notion_external import NotionExternal
from .qdrant_external import QdrantExternal
from .slack_external import SlackExternal


class Context:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.notion = NotionExternal()
            cls.__instance.db = DatabaseExternal()
            cls.__instance.slack = SlackExternal()
            cls.__instance.qdrant = QdrantExternal()
        return cls.__instance
