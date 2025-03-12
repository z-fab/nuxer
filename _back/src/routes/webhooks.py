from fastapi import APIRouter, Depends, HTTPException, Request

from repositories import users_repository as ur
from repositories import echo_repository as er
from services.auth_service import admin_role
from services.fabbank_service import FabBankService as fbs

router = APIRouter(
    prefix="/wh",
    tags=["Webhooks"],
    responses={404: {"description": "Not found"}},
)

@router.post("/echo_not_indexed")
async def index_echo(request: Request, user: dict = Depends(admin_role)):
    print(er.get_echo_not_indexed())
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
