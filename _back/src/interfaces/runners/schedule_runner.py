import time

from apscheduler.schedulers.background import BackgroundScheduler

from domains.fabzenda.services.update_animal import UpdateAnimalService
from interfaces.presenters.hints import FabzendaHints
from interfaces.presenters.slack.message.presenter import MessagePresenter
from shared.infrastructure.db_context import db
from shared.infrastructure.slack_context import slack

scheduler = BackgroundScheduler()


def job_update_animals_status():
    presenter = MessagePresenter()
    service_response = UpdateAnimalService(db).update_animals_status()

    if len(service_response.data["sick_animals"]) > 0:
        for animal in service_response.data["sick_animals"]:
            rendered_message = presenter.render({"animal": animal}, FabzendaHints.NOTIFICATE_ANIMAL_SICK)
            slack.send_dm(user=animal.user.slack_id, text=rendered_message)

    if len(service_response.data["dead_animals"]) > 0:
        for animal in service_response.data["dead_animals"]:
            rendered_message = presenter.render({"animal": animal}, FabzendaHints.NOTIFICATE_ANIMAL_DEAD)
            slack.send_dm(user=animal.user.slack_id, text=rendered_message)
            rendered_message = presenter.render({"animal": animal}, FabzendaHints.NOTIFICATE_CHANNEL_ANIMAL_DEAD)
            slack.send_message(channel="ux_team", text=rendered_message)


def configure_jobs():
    scheduler.add_job(
        job_update_animals_status,
        args=[],
        id="update_animals_status",
        trigger="interval",
        seconds=5,
    )

    # # Job para sortear os animais
    # scheduler.add_job(
    #     FabzendaService().process_animal_lottery, args=[], id="lottery_animals", trigger="cron", hour=11, minute=0
    # )

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
