from _back.src.fabbank.services.fabbank_service import FabBankService as fbs
from fastapi import APIRouter, Depends, HTTPException, Request
from repositories import echo_repository as er
from repositories import users_repository as ur
from services.auth_service import admin_role
from services.echo_service import EchoService

router = APIRouter(
    prefix="/wh",
    tags=["Webhooks"],
    responses={404: {"description": "Not found"}},
)


@router.post("/index_echo")
async def index_echo(request: Request, user: dict = Depends(admin_role)):
    body_json = await request.json()
    echo_id = body_json.get("data", {}).get("id")

    if not echo_id:
        raise HTTPException(status_code=404, detail="Echo ID not found in request body")

    echo_entity = er.fetch_echo_entity_by_id(echo_id)
    ecs = EchoService(echo_entity)
    ecs.index_echo()


@router.post("/echo_not_indexed")
async def get_not_indexed_echos(request: Request, user: dict = Depends(admin_role)):
    print(er.fetch_echo_entities_not_indexed())
    return {"message": "Webhooks"}


@router.post("/add_coins")
async def add_coins(request: Request, user: dict = Depends(admin_role)):
    user_to = None
    amount_str = request.headers.get("amount")
    description = request.headers.get("description")
    print(f"amount: {amount_str}, description: {description}")
    try:
        body = await request.json()
        user_notion_id = body.get("source", {}).get("user_id").replace("-", "")
        user_to = ur.get_users_by_notion_id(user_notion_id)
    except Exception as err:
        raise HTTPException(status_code=404, detail="User not found") from err

    if fbs().change_coins(user_to, int(amount_str), description):
        return {"message": "Fabcoins adicionados com sucesso"}
    else:
        raise HTTPException(status_code=500, detail="Failed to add coins")
