from domains.user.entities.user import UserEntity
from domains.user.orm.user import UserORM
from shared.infrastructure.db_context import DatabaseExternal


class UserRepository:
    def __init__(self, db_context: DatabaseExternal):
        self._db_session = db_context.session

    def get_user_by_slack_id(self, slack_id: str) -> UserEntity | None:
        with self._db_session() as session:
            orm = session.query(UserORM).filter(UserORM.slack_id == slack_id).order_by(UserORM.id.desc()).first()
            if not orm:
                return None

            return UserEntity.model_validate(orm)

    def get_user_by_id(self, user_id: str) -> UserEntity | None:
        with self._db_session() as session:
            orm = session.query(UserORM).filter(UserORM.id == user_id).order_by(UserORM.id.desc()).first()
            if not orm:
                return None

            return UserEntity.model_validate(orm)

    def get_user_by_email(self, email: str) -> UserEntity | None:
        with self._db_session() as session:
            orm = session.query(UserORM).filter(UserORM.email == email).order_by(UserORM.id.desc()).first()
            if not orm:
                return None

            return UserEntity.model_validate(orm)

    def get_user_by_notion_user_id(self, notion_user_id: str) -> UserEntity | None:
        with self._db_session() as session:
            orm = (
                session.query(UserORM)
                .filter(UserORM.notion_user_id == notion_user_id)
                .order_by(UserORM.id.desc())
                .first()
            )
            if not orm:
                return None

            return UserEntity.model_validate(orm)

    def get_user_by_notion_id(self, notion_id: str) -> UserEntity | None:
        with self._db_session() as session:
            orm = session.query(UserORM).filter(UserORM.notion_id == notion_id).order_by(UserORM.id.desc()).first()
            if not orm:
                return None

            return UserEntity.model_validate(orm)
