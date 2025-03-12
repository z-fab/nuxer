import argparse

from loguru import logger

from config.logger import setup_logger
from externals.context import Context
from runners.api_runner import init_api
from runners.assistant_runner import init_assistant
from runners.schedule_runner import init_schedule

if __name__ == "__main__":
    setup_logger()
    context = Context()

    parser = argparse.ArgumentParser(description="Backend NUxer")
    parser.add_argument(
        "runner",
        choices=["schedule", "assistant", "api"],
        help="Runner a ser executado",
    )

    args = parser.parse_args()

    if args.runner == "listen":
        logger.debug("STARTING LISTENER")

        from repositories import fabbank_repository as fbr
        from repositories import itens_loja_repository as ilr

        context.slack.send_message("C04N17V06DS", "Estou online!")

        with context.db.session() as session:
            logger.debug(fbr.get_all_wallets())

        logger.debug(ilr.get_item_by_cod("F1"))

    elif args.runner == "api":
        init_api()

    elif args.runner == "assistant":
        init_assistant()

    elif args.runner == "schedule":
        logger.debug("STARTING SCHEDULE")
        init_schedule()

        # log.info(f"STARTING SCHEDULE - VERSION {SETTINGS.VERSION} | ENV {SETTINGS.ENV}")

    # if args.runner == "schedule":
    #     logger.info(
    #         f"STARTING SCHEDULE - VERSION {settings.VERSION} | ENV {settings.ENV}"
    #     )
    #     scheduler = Scheduler(context)
    #     scheduler.start()
    # elif args.runner == "listen":
    #     logger.info(
    #         f"STARTING LISTENER - VERSION {settings.VERSION} | ENV {settings.ENV}"
    #     )
    #     setup_listener()
    #     context.slack.start_socket()
    # elif args.runner == "ccu":
    #     CCUCommand({}).execute()
    # elif args.runner == "baygon":
    #     BaygonCommand({"action": "remember"}).execute()
    # else:
    #     print("Invalid action")
