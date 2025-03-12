import uuid
from datetime import UTC, datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import EmailStr

from config.const import CONST_MESSAGE
from config.settings import SETTINGS as S
from externals.context import Context
from models.entities.user_entity import UserEntity
from repositories import users_repository as ur
from utils.slack_utils import get_random_saudacao

pending_magic_links = {}
context = Context()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=S.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, S.AUTH_SECRET_KEY, algorithm=S.AUTH_ALGORITHM)
    return encoded_jwt


def create_magic_link(email: EmailStr):
    user: UserEntity = ur.get_users_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email não encontrado")

    # Gerar um token único para o magic link
    token = str(uuid.uuid4())
    expires = datetime.now(UTC) + timedelta(minutes=S.AUTH_MAGIC_LINK_EXPIRE_MINUTES)
    pending_magic_links[token] = {"email": email, "expires": expires}

    # Em produção, você enviaria um email real
    magic_link = f"{S.URL_FRONT}/auth/verify?token={token}"

    context.slack.send_dm(
        user.slack_id,
        CONST_MESSAGE.TEMPLATE_LOGIN_MAGIC_LINK.format(
            **{"saudacao": get_random_saudacao(user.apelido), "magic_link": magic_link}
        ),
    )

    print(f"Magic link para {email}: {magic_link}")

    return magic_link


def verify_magic_link(token: str):
    # Verificar se o token existe e não expirou
    if token not in pending_magic_links:
        return None

    link_data = pending_magic_links[token]
    if datetime.now(UTC) > link_data["expires"]:
        del pending_magic_links[token]
        return None

    # Limpar o token usado
    email = link_data["email"]
    del pending_magic_links[token]

    user = ur.get_users_by_email(email)
    if not user:
        return None

    context.slack.send_dm(
        user.slack_id,
        CONST_MESSAGE.TEMPLATE_VERIFY_MAGIC_LINK.format(**{"saudacao": get_random_saudacao(user.apelido)}),
    )

    return email


# def create_api_key(name: str, user_id: int):
#     # Gerar uma chave de API aleatória
#     key = f"fbapi_{secrets.token_urlsafe(32)}"

#     # Armazenar a chave (em produção, use um banco de dados)
#     api_key = {
#         "id": len(api_keys_db) + 1,
#         "key": key,
#         "name": name,
#         "created_at": datetime.now(timezone.utc),
#         "user_id": user_id,
#     }
#     api_keys_db[key] = api_key

#     return api_key


async def current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, S.AUTH_SECRET_KEY, algorithms=[S.AUTH_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e

    user = ur.get_users_by_email(email)
    if user is None:
        raise credentials_exception
    return user


def admin_role(user=Depends(current_user)):
    if user.role > 0:
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions: Admin role required",
        )
    return user


# Função para verificar API keys
# async def verify_api_key(api_key: str):
#     if api_key not in api_keys_db:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid API key",
#         )
#     return api_keys_db[api_key]
