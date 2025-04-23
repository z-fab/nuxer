from apscheduler.schedulers.background import BackgroundScheduler

from domains.fabzenda.services.lottery import LotteryService
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


def job_lottery_animals():
    lotery_service = LotteryService(db)
    response = lotery_service.run_lottery()

    presenter = MessagePresenter()

    rendered_message = presenter.render(response.data, FabzendaHints.NOTIFICATE_CHANNEL_LOTTERY)
    slack.send_message(channel="ux_team", text=rendered_message)

    for user_id, info_winners in response.data["winners"].items():
        rendered_message = presenter.render({"info_winners": info_winners}, FabzendaHints.NOTIFICATE_LOTTERY)
        slack.send_dm(user=user_id, text=rendered_message)
