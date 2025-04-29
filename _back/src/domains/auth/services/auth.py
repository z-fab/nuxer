import uuid
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt
from pydantic import EmailStr

from domains.auth import messages as MSG
from domains.user.repositories.user import UserRepository
from shared.config.settings import SETTINGS as S
from shared.infrastructure.db_context import DatabaseExternal
from shared.infrastructure.slack_context import slack
from shared.utils.slack_utils import get_random_saudacao


class AuthService:
    def __init__(self, db_context: DatabaseExternal):
        self.pending_magic_links = {}
        self.user_repository = UserRepository(db_context)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=S.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, S.AUTH_SECRET_KEY, algorithm=S.AUTH_ALGORITHM)
        return encoded_jwt

    def create_magic_link(self, email: EmailStr):
        user = self.user_repository.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email não encontrado")

        # Gerar um token único para o magic link
        token = str(uuid.uuid4())
        expires = datetime.now(UTC) + timedelta(minutes=S.AUTH_MAGIC_LINK_EXPIRE_MINUTES)
        self.pending_magic_links[token] = {"email": email, "expires": expires}

        # Em produção, você enviaria um email real
        magic_link = f"{S.URL_FRONT}/auth/verify?token={token}"

        slack.send_dm(
            user.slack_id,
            MSG.LOGIN_MAGIC_LINK.format(**{"saudacao": get_random_saudacao(user.apelido), "magic_link": magic_link}),
        )

        print(f"Magic link para {email}: {magic_link}")

        return magic_link

    def verify_magic_link(self, token: str):
        # Verificar se o token existe e não expirou
        if token not in self.pending_magic_links:
            return None

        link_data = self.pending_magic_links[token]
        if datetime.now(UTC) > link_data["expires"]:
            del self.pending_magic_links[token]
            return None

        # Limpar o token usado
        email = link_data["email"]
        del self.pending_magic_links[token]

        user = self.user_repository.get_user_by_email(email)
        if not user:
            return None

        slack.send_dm(
            user.slack_id,
            MSG.VERIFY_MAGIC_LINK.format(**{"saudacao": get_random_saudacao(user.apelido)}),
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


# Função para verificar API keys
# async def verify_api_key(api_key: str):
#     if api_key not in api_keys_db:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid API key",
#         )
#     return api_keys_db[api_key]
