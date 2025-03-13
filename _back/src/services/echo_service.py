from externals.context import Context
from models.entities.echo_entity import EchoEntity
from utils import slack_utils as slack_utils

context = Context()


class EchoService:
    ECHO: EchoEntity = None

    def __init__(self, echo: EchoEntity = None):
        self.ECHO = echo

    def index_echo(self):
        print("Echo indexed")
