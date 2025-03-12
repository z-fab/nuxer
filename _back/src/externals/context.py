from .database_external import Database_SQL
from .notion_external import NotionService
from .slack_external import SlackService


class Context:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.notion = NotionService()
            cls.__instance.db = Database_SQL()
            cls.__instance.slack = SlackService()
        return cls.__instance
