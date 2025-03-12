import json

from loguru import logger
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from config.const import CONST_SLACK
from config.settings import SETTINGS as settings
from utils.slack_utils import text_to_blocks


class SlackService:
    """
    A class to handle Slack messaging operations.

    This class provides methods to initialize a Slack app, send messages to channels,
    and send direct messages to users.

    Attributes:
        __app (App): The Slack Bolt app instance.
        __socket (SocketModeHandler): The Socket Mode handler for the app.
    """

    def __init__(self):
        """
        Initialize the SlackService with Slack app and socket handler.
        """
        self.__app = App(token=settings.SLACK_BOT_TOKEN)
        self.__socket = SocketModeHandler(self.__app, settings.SLACK_APP_TOKEN)

    def get_app(self):
        """
        Get the Slack Bolt app instance.

        Returns:
            App: The Slack Bolt app instance.
        """
        return self.__app

    def start_socket(self):
        """
        Start the Socket Mode handler and return the app.

        Returns:
            App: The Slack Bolt app instance.
        """
        self.__socket.start()
        return self.__app

    def __chat_postMessage(
        self,
        channel_id: str,
        blocks: str = "{}",
        alt_text: str = "",
        thread_ts: str = None,
    ):
        """
        Send a message to a Slack channel.

        Args:
            channel_id (str): The ID of the channel to send the message to.
            blocks (str): The message content in Slack blocks format (JSON string).
            alt_text (str): Alternative text for the message.
            thread_ts (str, optional): The timestamp of the thread to reply to.

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """
        try:
            self.__app.client.chat_postMessage(channel=channel_id, thread_ts=thread_ts, blocks=blocks, text=alt_text)
            logger.debug(f"Message sent to {channel_id}:\n{blocks}")
            return True
        except Exception as e:
            logger.error(f"ERROR SENDING MESSAGE TO {channel_id}:\n{e}")
            return False

    def __send_file(
        self,
        channel_id: str,
        files_info: list[dict] = None,
        blocks: str = "{}",
        thread_ts: str = None,
    ):
        if files_info is None:
            files_info = [{}]
        try:
            if isinstance(files_info, dict):
                files_info = [files_info]

            for file in files_info:
                response = self.__app.client.files_upload_v2(
                    channel=channel_id,
                    file=file.get("path", ""),
                    title=file.get("title", ""),
                    initial_comment=blocks,
                    thread_ts=thread_ts,
                    alt_txt=file.get("alt", ""),
                )
                if not response["ok"]:
                    logger.error(f"ERROR SENDING FILE TO {channel_id}:\n{response}")
                logger.debug(f"File sent to {channel_id}:\n{file}")
            return True
        except Exception as e:
            logger.error(f"ERROR SENDING FILE TO {channel_id}:\n{e}")
            return False

    def send_message(
        self,
        channel: str,
        text: str,
        alt_text: str = "Há uma nova mensagem",
        thread_ts: str = None,
        files_info: list[dict] = None,
    ):
        id_channel = CONST_SLACK.SLACK_ID_CHANNEL.get(channel, channel)
        if settings.ENV == "dev":
            id_channel = CONST_SLACK.ID_CHANNEL_DEV

        blocks = text_to_blocks(text)
        blocks_str = json.dumps(blocks)

        if files_info:
            self.__chat_postMessage(id_channel, blocks_str, alt_text, thread_ts)
            return self.__send_file(
                channel_id=id_channel,
                files_info=files_info,
                blocks="",
                thread_ts=thread_ts,
            )
        else:
            return self.__chat_postMessage(id_channel, blocks_str, alt_text, thread_ts)

    def send_dm(
        self,
        user: str,
        text: str,
        alt_text: str = "Há uma nova mensagem",
        files_info: list[dict] = None,
    ):
        if settings.ENV == "dev":
            id_user = CONST_SLACK.ID_USER_DEV
        else:
            id_user = user

        result = self.__app.client.conversations_open(users=id_user)

        if result["ok"]:
            blocks = text_to_blocks(text)
            blocks_str = json.dumps(blocks)
            id_channel = result["channel"]["id"]

            if files_info:
                self.__chat_postMessage(id_channel, blocks_str, alt_text)
                return self.__send_file(
                    channel_id=id_channel,
                    files_info=files_info,
                    blocks="",
                    thread_ts=None,
                )
            else:
                return self.__chat_postMessage(id_channel, blocks_str, alt_text)

    def open_view(self, trigger_id: str, view: dict):
        try:
            self.__app.client.views_open(trigger_id=trigger_id, view=view)
            return True
        except Exception as e:
            logger.error(f"ERROR OPENING VIEW:\n{e}")
            return False
