from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from domains.user.entities.user import UserEntity
from domains.user.repositories.user import UserRepository
from shared.config.settings import SETTINGS as S
from shared.infrastructure.db_context import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
user_repository = UserRepository(db)


async def current_user(token: str = Depends(oauth2_scheme)) -> UserEntity:
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

    user = user_repository.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user


def admin_role(user=Depends(current_user)) -> UserEntity:
    if user.role > 0:
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions: Admin role required",
        )
    return user
