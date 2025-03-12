import json

from slack_bolt import BoltContext
from slack_sdk import WebClient

from actions.fabbank_action import FabBankAction
from actions.fabzenda_action import FabzendaAction
from models.entities.user_entity import UserEntity
from repositories.users_repository import get_users_by_slack_id
from utils.slack_utils import text_to_blocks


class ActionSlackService:
    BODY: dict = None
    CONTEXT: BoltContext = None
    CLIENT: WebClient = None

    TYPE_CONTAINER: str = ""
    TYPE_VIEW_ID: str = ""

    TRIGGERID: str = ""
    CHANNEL_ID: str = ""
    TS_MESSAGE: str = ""

    USER: UserEntity = None
    COMMAND: str = ""
    DICT_PARAMS: dict = {}

    def __init__(self, body: dict, context: BoltContext, client: WebClient):
        self.BODY = body
        self.CONTEXT = context
        self.CLIENT = client

        actions = body.get("actions", [])
        actions = actions[0] if len(actions) > 0 else {}

        slack_id = self.BODY.get("user", {}).get("id", None)
        self.USER = get_users_by_slack_id(slack_id) if slack_id else None

        self.TYPE_CONTAINER = body.get("container", {}).get("type", "")
        self.TYPE_VIEW_ID = body.get("container", {}).get("view_id", "")

        self.TRIGGERID = self.BODY.get("trigger_id", "")
        self.CHANNEL_ID = context.get("channel_id", "")
        self.TS_MESSAGE = self.BODY.get("container", {}).get("message_ts", "")

        self.COMMAND = actions.get("action_id", "").split("_")[0]
        self.DICT_PARAMS = json.loads(actions.get("value", "{}"))

    def _set_status(self, status: str, only_thread: bool = True):
        return None

    def _say(self, message: str, alt_text: str = "Há uma nova mensagem"):
        blocks = text_to_blocks(message)

        blocks_send = 0
        ts = self.TS_MESSAGE
        while blocks_send < len(blocks):
            message = json.dumps(blocks[blocks_send : blocks_send + 49])
            response = self.CONTEXT.say(
                blocks=message,
                text=alt_text,
                channel=self.CHANNEL_ID,
                thread_ts=ts,
            )
            ts = response.get("ts")
            blocks_send += 49

    def _open_view(self, view: dict, content: str):
        if isinstance(content, str):
            content = text_to_blocks(content)

        view["blocks"] = content

        if self.TYPE_CONTAINER != "view":
            self.CLIENT.views_open(trigger_id=self.TRIGGERID, view=view)
        else:
            self.CLIENT.views_update(view_id=self.TYPE_VIEW_ID, view=view)

    def run(self):
        match self.COMMAND:
            case "fb":
                return FabBankAction(
                    self.USER, list(self.DICT_PARAMS.values()), self._set_status, self._say, self._open_view
                ).run()
            case "fabzenda":
                return FabzendaAction(
                    self.USER, list(self.DICT_PARAMS.values()), self._set_status, self._say, self._open_view
                ).run()
