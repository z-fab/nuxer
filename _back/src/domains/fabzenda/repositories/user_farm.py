from datetime import datetime

from domains.fabzenda.entities.user_farm import UserFarmEntity
from domains.fabzenda.orm.user_farm import UserFarmORM
from shared.infrastructure.db_context import DatabaseExternal


class UserFarmRepository:
    def __init__(self, db_context: DatabaseExternal):
        self._db_session = db_context.session

    def get_user_farm_by_id(self, user_id: int) -> UserFarmEntity | None:
        with self._db_session() as session:
            orm = (
                session.query(UserFarmORM).filter(UserFarmORM.user_id == user_id).order_by(UserFarmORM.user_id).first()
            )
            if not orm:
                return None

            return UserFarmEntity.model_validate(orm)

    def create_user_farm(self, user_id: str, max_animals: int = 3) -> UserFarmEntity | None:
        with self._db_session() as session:
            orm = UserFarmORM(
                user_id=user_id,
                max_animals=max_animals,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            session.add(orm)
            session.commit()
            return UserFarmEntity.model_validate(orm) if orm else None

    def update_user_farm(self, user_farm: UserFarmEntity) -> UserFarmEntity | None:
        with self._db_session() as session:
            orm = session.query(UserFarmORM).filter(UserFarmORM.user_id == user_farm.user_id).first()
            if not orm:
                return None

            orm.max_animals = user_farm.max_animals
            orm.updated_at = datetime.now()

            session.commit()

            return UserFarmEntity.model_validate(orm)
