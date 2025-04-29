from notion_client import Client

from shared.config.settings import SETTINGS as s


class NotionContext:
    def __init__(self):
        self.__client = Client(auth=s.NOTION_TOKEN)

    def get_client(self):
        return self.__client


notion = NotionContext().get_client()
