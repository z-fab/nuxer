from fastapi import APIRouter, Depends, Request

from domains.debriefing.use_cases.notificar_debriefing import NotificarDebriefing
from interfaces.routes.auth.dependencies import admin_role
from shared.utils.slack_notifier import slack_notifier

router = APIRouter(
    prefix="/wh/db",
    tags=["Webhooks - Debriefing"],
    responses={404: {"description": "Not found"}},
)


@router.post("/notificar")
async def notificar(request: Request, user: dict = Depends(admin_role)):
    body_json = await request.json()

    debriefing_id = body_json.get("data", {}).get("id")

    use_case_response = NotificarDebriefing(debriefing_id)()
    slack_notifier(use_case_response)

    return {"message": "Debriefing notificado com sucesso!"}
