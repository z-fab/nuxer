from contextlib import contextmanager
from typing import Generator
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from config.settings import SETTINGS as S


class Database_SQL:
    # ===================== #
    #  BASES                #
    # ===================== #

    def __init__(self):
        self.__engine = sqlalchemy.create_engine(
            f"postgresql+psycopg2://{S.DATABASE_USER}:{S.DATABASE_PASSWORD}@{S.DATABASE_HOST}:{S.DATABASE_PORT}/{S.DATABASE_NAME}"
        )
        self.__sessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.__engine
        )

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        session: Session = self.__sessionLocal()

        try:
            yield session
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            # self.logger.error(f"Erro na sessão do banco de dados: {str(e)}")
            raise
        finally:
            session.close()
