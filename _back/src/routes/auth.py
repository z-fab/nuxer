# auth_routes.py
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from config.settings import SETTINGS as S
from models.entities.token_entity import MagicLinkRequest
from models.entities.user_entity import UserEntity
from services.auth_service import create_access_token, create_magic_link, current_user, verify_magic_link

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/request-magic-link")
async def request_login(request: MagicLinkRequest):
    create_magic_link(request.email)

    return {"message": "Link enviado"}


@router.get("/verify-magic-link")
async def verify_login(token: str):
    email = verify_magic_link(token)
    if not email:
        raise HTTPException(status_code=400, detail="Link inválido ou expirado")

    # Criar o token JWT para o usuário
    access_token_expires = timedelta(minutes=S.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.api_route("/me", response_model=UserEntity, methods=["GET", "POST"])
async def read_users_me(current_user: UserEntity = Depends(current_user)):
    return current_user


# async def get_authenticated_user(
#     current_user: Optional[UserEntity] = Depends(get_current_user),
#     # api_key: Optional[dict] = Depends(get_api_key),
# ):
#     if current_user:
#         return current_user
#     # if api_key:
#     #     # Buscar o usuário associado à API key
#     #     user_id = api_key["user_id"]
#     #     # Em produção, você buscaria o usuário no banco de dados
#     #     return {"id": user_id, "is_authenticated": True}

#     raise HTTPException(status_code=401, detail="Autenticação necessária")


# @router.post("/api-keys", response_model=APIKey)
# async def create_new_api_key(name: str, current_user: User = Depends(get_current_user)):
#     api_key = create_api_key(name, current_user.id)
#     return api_key


# # Função auxiliar para extrair a API key do cabeçalho
# async def get_api_key(x_api_key: Optional[str] = Header(None)):
#     if x_api_key:
#         return await verify_api_key(x_api_key)
#     return None
