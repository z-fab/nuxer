import re

from loguru import logger
from slack_bolt import Assistant, BoltContext, Say, SetSuggestedPrompts

from interfaces.slack.message_handler import handle_message_event
from shared.infrastructure.slack_context import SlackContext

# from slack_sdk import WebClient
# from externals.context import Context
# from services.action_slack_service import ActionSlackService
# from services.message_service import MessageService
# from services.view_slack_service import ViewSlackService
from shared.utils.slack_utils import get_random_saudacao

# context = Context()

slack = SlackContext()

app_slack = slack.get_app()
assistant = Assistant()
app_slack.use(assistant)


@app_slack.event("message")
def messages(body, say, context: BoltContext):
    pass


@app_slack.event("app_mention")
def messages(body, say, context: BoltContext):  # noqa: F811
    last_message = body.get("event", {}).get("text", "")
    last_message = re.sub(r"^\s*<@[^>]+>\s*", "", last_message)
    print(body)
    try:
        return handle_message_event(context, body.get("event", {}))

    except Exception as e:
        logger.exception(f"Failed to respond to an inquiry: {e}")
        say(":warning: Desculpe, algo deu errado nos meus bits e bytes :robot_face:")


# @app_slack.action({"action_id": re.compile(r".*")})
# def action_handler(body, ack, say, context: BoltContext, client: WebClient):
#     ack()
#     try:
#         return ActionSlackService(body, context, client).run()

#     except Exception as e:
#         logger.exception(f"Failed to execute action: {e}")
#         say(":warning: Desculpe, algo deu errado nos meus bits e bytes quando fui executar a ação :robot_face:")
#         return False


# @app_slack.view("")
# def view_handler(body, ack, context: BoltContext, client: WebClient):
#     ack()
#     try:
#         return ViewSlackService(body, context, client).run()

#     except Exception as e:
#         logger.exception(f"Failed to execute action: {e}")
#         return False

#     return True


@assistant.thread_started
def start_assistant_thread(say: Say, set_suggested_prompts: SetSuggestedPrompts):
    say(f":wave: {get_random_saudacao()}")


@assistant.user_message
def respond_in_assistant_thread(
    payload: dict,
    context: BoltContext,
    say: Say,
):
    try:
        return handle_message_event(context, payload)

    except Exception as e:
        logger.exception(f"Failed to respond to an inquiry: {e}")
        say(":warning: Desculpe, algo deu errado nos meus bits e bytes :robot_face:")


def init_assistant():
    slack.start_socket()


# # # Setting suggested prompts is optional
# # set_suggested_prompts(
# #     prompts=[
# #         # If the suggested prompt is long, you can use {"title": "short one to display", "message": "full prompt"}
# #         "What does SLACK stand for?",
# #         "When Slack was released?",
# #     ],
# # )


# # # Collect the conversation history with this user
# # replies_in_thread = client.conversations_replies(
# #     channel=context.channel_id,
# #     ts=context.thread_ts,
# #     oldest=context.thread_ts,
# #     limit=10,
# # )
# # messages_in_thread: List[Dict[str, str]] = []
# # for message in replies_in_thread["messages"]:
# #     print(message, "\n")
# #     # role = "user" if message.get("bot_id") is None else "assistant"
# #     # messages_in_thread.append({"role": role, "content": message["text"]})

# # print("\ncontext\n", context)
# # print("\nthread_context\n", get_thread_context())
# # print("\npayload\n", payload)
# # print("\nclient\n", client)

# # set_status("estou pensando...")

# # client.assistant_threads_setTitle(
# #     title="Oi, como vai?",
# #     channel_id=context.channel_id,
# #     thread_ts=context.thread_ts,
# # )
# # time.sleep(2)
# # set_status("estou pensando de novo...")

# # context.set_title("Oi, tudo bem?")

# # say("Respondido :D")
