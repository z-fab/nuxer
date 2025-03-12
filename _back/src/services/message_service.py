import json
import re

from slack_bolt import BoltContext

from actions.fabbank_action import FabBankAction
from actions.fabzenda_action import FabzendaAction
from config.const import CONST_MESSAGE
from models.entities.user_entity import UserEntity
from repositories.users_repository import get_users_by_slack_id
from utils.slack_utils import text_to_blocks


class MessageService:
    CONTEXT_ASSISTANT: BoltContext = None
    LAST_MESSAGE: str = ""
    TYPE: str = ""
    USER: UserEntity = None

    def __init__(self, context: BoltContext, message: str, type_message: str):
        self.CONTEXT_ASSISTANT = context
        self.LAST_MESSAGE = message
        self.TYPE = type_message
        self.USER = get_users_by_slack_id(context.user_id)

    def _set_status(self, status: str, only_thread: bool = True):
        if self.TYPE != "mention":
            self.CONTEXT_ASSISTANT.set_status(status)
        else:
            if not only_thread:
                self.CONTEXT_ASSISTANT.say(status)

    def _say(self, message: str, alt_text: str = "Há uma nova mensagem"):
        blocks = text_to_blocks(message)

        blocks_send = 0
        ts = None
        while blocks_send < len(blocks):
            message = json.dumps(blocks[blocks_send : blocks_send + 49])
            response = self.CONTEXT_ASSISTANT.say(blocks=message, text=alt_text, thread_ts=ts)
            ts = response.get("ts")
            blocks_send += 49

    def _identify_message(self, message: str) -> str:
        self._set_status("Pensando...")
        if message == "Oi":
            return "saudacao"
        if message == "saldo":
            return "fabbank"
        if message.startswith("!"):
            return "comando"
        return "none"

    def _extract_command(self):
        pattern = r"!(\w+)(?:\s+(.+))?"
        search = re.search(pattern, self.LAST_MESSAGE)
        command = ""
        params = []
        if search:
            command = search.group(1)
            if search.group(2):
                # Expressão regular melhorada para capturar todos os tipos de parâmetros
                params = re.findall(r'([\'"“”][^\'"“”]*[\'"“”]|\S+)', search.group(2))
                params = [param.strip('"') for param in params]

        return command, params

    def _execute_command(self, command: str, params: list):
        match command:
            case "fb":
                if self.TYPE != "thread":
                    self._say(CONST_MESSAGE.MESSAGE_COMMAND_THREAD_ONLY)
                    return False
                return FabBankAction(self.USER, params, self._set_status, self._say, None).run()
            case "fabzenda":
                if self.TYPE != "thread":
                    self._say(CONST_MESSAGE.MESSAGE_COMMAND_THREAD_ONLY)
                    return False
                return FabzendaAction(self.USER, params, self._set_status, self._say, None).run()
            case _:
                self._say(CONST_MESSAGE.MESSAGE_COMMAND_NOT_FOUND)
                return False

    def run(self):
        message_type = self._identify_message(self.LAST_MESSAGE)
        if message_type == "saudacao":
            self._set_status("Digitando...")
            self.CONTEXT_ASSISTANT.say(":wave: Hey, tudo bem? Como posso te ajudar?")
        elif message_type == "fabbank":
            self._set_status("Pesquisando...", False)
            self.CONTEXT_ASSISTANT.say("Seu saldo é de R$ 100,00")
        elif message_type == "comando":
            self._set_status("Trabalhando...")
            command, param = self._extract_command()
            return self._execute_command(command, param)
        else:
            self.CONTEXT_ASSISTANT.say("Não entendi...")
            return False
