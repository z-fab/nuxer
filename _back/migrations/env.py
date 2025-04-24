import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# --- garantir que o src esteja no path ---
BASE_DIR = Path(__file__).resolve().parent.parent  # aponta para _back
SRC_DIR = BASE_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

# agora podemos importar o SETTINGS
from shared.config.settings import SETTINGS  # type: ignore  # noqa: E402, I001

# montar URL
db = SETTINGS
db_url = (
    f"postgresql+psycopg2://{db.DATABASE_USER}:"
    f"{db.DATABASE_PASSWORD}@"
    f"{db.DATABASE_HOST}:"
    f"{db.DATABASE_PORT}/"
    f"{db.DATABASE_NAME}"
)

config = context.config
db_url = db_url.replace("%", "%%")
config.set_main_option("sqlalchemy.url", db_url)
fileConfig(config.config_file_name)

# importa seu metadata
from shared.infrastructure.db_base import Base  # type: ignore # noqa: E402

target_metadata = Base.metadata

import domains.user.orm.user  # type: ignore  # noqa: E402, F401, F811, I001
import domains.config.orm.config  # type: ignore  # noqa: E402, F401, F811, I001
import domains.fabbank.orm.item_loja  # type: ignore  # noqa: E402, F401, F811, I001
import domains.fabbank.orm.transaction  # type: ignore  # noqa: E402, F401, F811, I001
import domains.fabbank.orm.wallet  # type: ignore  # noqa: E402, F401, F811, I001
import domains.fabzenda.orm.animal_modifier  # type: ignore  # noqa: E402, F401, F811, I001
import domains.fabzenda.orm.animal_type  # type: ignore  # noqa: E402, F401, F811, I001
import domains.fabzenda.orm.user_animal  # type: ignore  # noqa: E402, F401, F811, I001
import domains.fabzenda.orm.user_farm  # type: ignore  # noqa: E402, F401, F811, I001
import domains.fabzenda.orm.item_definition  # type: ignore  # noqa: E402, F401, F811, I001


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,  # ← agora também no modo online
            version_table_schema="public",
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
