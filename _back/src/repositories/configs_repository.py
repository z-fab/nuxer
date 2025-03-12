from models.orm.configs import Config as ConfigORM
from externals.context import Context
from loguru import logger

context = Context()


def get_config_by_name(name: str) -> ConfigORM:
    with context.db.session() as session:
        config = session.query(ConfigORM).filter(ConfigORM.name == name).first()
        session.expunge(config)
        return config


def save_config_value(config: ConfigORM, new_value: str):
    config.value = new_value
    with context.db.session() as session:
        session.merge(config)
        session.commit()
