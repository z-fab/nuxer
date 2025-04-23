import argparse

from interfaces.runners.api_runner import init_api
from interfaces.runners.assistant_runner import init_assistant
from interfaces.runners.schedule_runner import init_schedule
from shared.config.logger import setup_logger

if __name__ == "__main__":
    setup_logger()
    parser = argparse.ArgumentParser(description="Backend Uxer")
    parser.add_argument(
        "runner",
        choices=["schedule", "assistant", "api"],
        help="Runner a ser executado",
    )

    args = parser.parse_args()

    if args.runner == "api":
        init_api()

    elif args.runner == "assistant":
        init_assistant()

    elif args.runner == "schedule":
        init_schedule()
