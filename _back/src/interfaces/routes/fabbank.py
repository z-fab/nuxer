from fastapi import APIRouter, Depends
from repositories import fabbank_repository as fbr
from services.auth_service import admin_role

from models.entities.wallet_entity import WalletEntity

# Criar o router com o prefixo /fabbank
router = APIRouter(
    prefix="/fabbank",
    tags=["fabbank"],
    responses={404: {"description": "Not found"}},
)


# Exemplo de rotas
@router.get("/")
async def read_fabbank_root():
    return {"message": "Bem-vindo ao FabBank API"}


@router.get("/wallets", response_model=list[WalletEntity])
async def read_accounts(user=Depends(admin_role)):
    return fbr.get_all_wallets()


# @router.get("/accounts/{account_id}")
# async def read_account(account_id: int):
#     # Aqui você implementaria a lógica para buscar uma conta específica
#     return {"account_id": account_id, "name": "Conta Exemplo", "balance": 1000.50}


# @router.post("/transfers")
# async def create_transfer(from_account: int, to_account: int, amount: float):
#     # Lógica para criar uma transferência
#     return {
#         "transfer_id": 123,
#         "from_account": from_account,
#         "to_account": to_account,
#         "amount": amount,
#         "status": "completed",
#     }
