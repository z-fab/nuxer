from typing import List
from externals.context import Context
from models.orm.users import User
from models.mappers.user_mapper import UserMapper
from loguru import logger

context = Context()


def get_users_by_notion_id(notion_id: str | List[str]) -> List[User]:
    if isinstance(notion_id, str):
        notion_id = [notion_id]

    with context.db.session() as session:
        users = (
            session.query(User)
            .filter(User.ativo)
            .filter(User.notion_id.in_(notion_id) | User.notion_user_id.in_(notion_id))
            .all()
        )
        session.expunge_all()
        if not users:
            return None
        users_entity = [UserMapper.orm_to_entity(user) for user in users]
        return users_entity if len(users_entity) > 1 else users_entity[0]

def get_users_by_slack_id(slack_id: str | List[str]) -> List[User]:
    if isinstance(slack_id, str):
        slack_id = [slack_id]

    with context.db.session() as session:
        users = (
            session.query(User)
            .filter(User.ativo)
            .filter(User.slack_id.in_(slack_id))
            .filter(User.id != 0)  # ignorando o FabBank
            .all()
        )
        session.expunge_all()
        if not users:
            return None
        users_entity = [UserMapper.orm_to_entity(user) for user in users]
        return users_entity if len(users_entity) > 1 else users_entity[0]


def get_users_by_id(list_id: int | List[int]) -> List[User]:
    if isinstance(list_id, int):
        list_id = [list_id]

    with context.db.session() as session:
        users = (
            session.query(User).filter(User.ativo).filter(User.id.in_(list_id)).all()
        )
        session.expunge_all()
        if not users:
            return None
        users_entity = [UserMapper.orm_to_entity(user) for user in users]
        return users_entity if len(users_entity) > 1 else users_entity[0]


def get_users_by_email(list_email: str | List[int]) -> List[User]:
    if isinstance(list_email, str):
        list_email = [list_email]

    with context.db.session() as session:
        users = (
            session.query(User)
            .filter(User.ativo)
            .filter(User.email.in_(list_email))
            .all()
        )
        session.expunge_all()
        if not users:
            return None
        users_entity = [UserMapper.orm_to_entity(user) for user in users]
        return users_entity[0] if len(users_entity) == 1 else users_entity
