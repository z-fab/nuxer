import time

from apscheduler.schedulers.background import BackgroundScheduler

from interfaces.handlers.schedule import job_handler as job

scheduler = BackgroundScheduler()


def configure_jobs():
    scheduler.add_job(
        job.job_update_animals_status,
        args=[],
        id="update_animals_status",
        trigger="interval",
        seconds=10,
    )

    # Job para sortear os animais
    scheduler.add_job(job.job_lottery_animals, args=[], id="lottery_animals", trigger="cron", hour=10, minute=0)

    # # Job para achar moedas
    # scheduler.add_job(
    #     FabzendaService().process_found_coin_for_animals, args=[], id="found_coin_1", trigger="interval", minutes=360
    # )


def init_schedule():
    configure_jobs()
    scheduler.start()
    print("Press Ctrl+C to exit")

    try:
        while True:
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
