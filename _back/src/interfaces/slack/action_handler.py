# from externals.slack_external import send_message, set_status
# from interfaces.slack.command_handler import handle_command

from slack_bolt import BoltContext


def handle_action_event(context: BoltContext, payload: dict) -> bool:
    command = ""
    args = []
    text = payload.get("text", "")

    print("payload", payload)
    print("context", context)

    # # Verifica se a mensagem é um comando
    # if text.startswith("!"):
    #     command, args = extract_command(text)

    #     input_data = SlackCommandInput(
    #         user_id=payload.get("user"),
    #         channel_id=payload.get("channel"),
    #         type_message=payload.get("type"),
    #         ts=payload.get("ts"),
    #         command=command,
    #         args=args,
    #         func_set_status=context.get("set_status"),
    #         func_say=context.get("say"),
    #     )
    #     logger.info(f"Comando recebido de {input_data.user_id}: {command} | args: {args}")
    #     use_case_response: UseCaseResponse = handle_command(input_data)

    #     # Comunicação com o usuário
    #     if use_case_response.success:
    #         input_data.say(use_case_response.message)
    #         if use_case_response.data:
    #             notify = use_case_response.data.get("notify")
    #             if notify:
    #                 logger.info(
    #                     f"Notificando {notify['user'].nome} ({notify['user'].slack_id}) sobre: {notify['message']}"
    #                 )
    #                 slack.send_dm(user=notify["user"].slack_id, text=notify["message"], alt_text=notify["message"])

    #     else:
    #         if use_case_response.message:
    #             input_data.say(use_case_response.message)
    #         else:
    #             input_data.say("Desculpe, algo deu errado nos meus bits e bytes :robot_face:")

    # # Não foi possível identificar o comando
    # else:
    #     logger.debug(f"Mensagem recebida de {payload.get('user')}: {text}")
    #     context.get("say")(text="Desculpe, algo deu errado nos meus bits e bytes :robot_face:")

    # return True
