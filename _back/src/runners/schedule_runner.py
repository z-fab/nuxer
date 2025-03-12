import time

from apscheduler.schedulers.background import BackgroundScheduler

from services.fabzenda_service import FabzendaService

scheduler = BackgroundScheduler()


def configure_jobs():
    # Job para atualizar o status dos animais
    scheduler.add_job(
        FabzendaService().process_update_animals_status,
        args=[],
        id="update_animals_status",
        trigger="interval",
        minutes=10,
    )

    # Job para sortear os animais
    scheduler.add_job(
        FabzendaService().process_animal_lottery,
        args=[],
        id="lottery_animals",  # trigger="cron", hour=11, minute=0
        trigger="interval",
        minutes=2,
    )

    # Job para sortear os animais
    scheduler.add_job(
        FabzendaService().process_found_coin_for_animals,
        args=[],
        id="found_coin",
        trigger="interval",
        seconds=30,
    )


def init_schedule():
    configure_jobs()
    scheduler.start()
    print("Press Ctrl+C to exit")

    try:
        while True:
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
