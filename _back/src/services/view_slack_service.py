import json

from slack_bolt import BoltContext
from slack_sdk import WebClient

from models.entities.user_entity import UserEntity
from repositories.users_repository import get_users_by_slack_id
from utils.slack_utils import text_to_blocks


class ViewSlackService:
    BODY: dict = None
    CONTEXT: BoltContext = None
    CLIENT: WebClient = None

    TYPE: str = ""
    TYPE_VIEW_ID: str = ""

    TRIGGERID: str = ""

    USER: UserEntity = None
    DICT_PARAMS: dict = {}

    def __init__(self, body: dict, context: BoltContext, client: WebClient):
        self.BODY = body
        self.CONTEXT = context
        self.CLIENT = client

        slack_id = self.BODY.get("user", {}).get("id", None)
        self.USER = get_users_by_slack_id(slack_id) if slack_id else None

        self.TYPE = body.get("type", "")
        self.TYPE_VIEW_ID = body.get("view", {}).get("id", "")

        self.TRIGGERID = body.get("trigger_id", "")
        self.DICT_PARAMS = json.loads(body.get("view", {}).get("private_metadata", "{}"))

    def _set_status(self, status: str, only_thread: bool = True):
        return None

    def _say(self, message: str, alt_text: str = "Há uma nova mensagem"):
        return None

    def _open_view(self, view: dict, content: str):
        if isinstance(content, str):
            content = text_to_blocks(content)

        view["blocks"] = content

        if self.TYPE_CONTAINER != "view":
            self.CLIENT.views_open(trigger_id=self.TRIGGERID, view=view)
        else:
            self.CLIENT.views_update(view_id=self.TYPE_VIEW_ID, view=view)

    def run(self):
        print(self.BODY, "\n", "\n")
        print(self.TYPE, "\n", "\n")
        print(self.DICT_PARAMS, "\n", "\n")

        # match self.DICT_PARAMS.get("command"):
        #     case "fabzenda":
        #         return FabzendaAction(
        #             self.USER, list(self.DICT_PARAMS.values()), self._set_status, self._say, self._open_view
        #         ).run()
