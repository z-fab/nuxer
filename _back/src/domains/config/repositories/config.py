from domains.config.entities.config import ConfigEntity
from domains.config.orm.config import ConfigORM
from shared.infrastructure.db_context import DatabaseExternal


class ConfigRepository:
    def __init__(self, db_context: DatabaseExternal):
        self._db_session = db_context.session

    def get_config_by_name(self, name: str) -> ConfigEntity | None:
        with self._db_session() as session:
            orm = session.query(ConfigORM).filter(ConfigORM.name == name).first()

            if not orm:
                return None

            return ConfigEntity.model_validate(orm)

    def save_config(self, config: ConfigEntity) -> bool:
        with self._db_session() as session:
            orm = session.query(ConfigORM).filter(ConfigORM.id == config.id).first()
            if not orm:
                return False

            orm.name = config.name
            orm.value = config.value
            session.commit()
            return True
