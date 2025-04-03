from models.entities.user_entity import UserEntity
from models.orm.users import User


class UserMapper:
    @staticmethod
    def orm_to_entity(orm_user: User) -> UserEntity:
        return UserEntity(
            id=orm_user.id,
            nome=orm_user.nome,
            apelido=orm_user.apelido,
            email=orm_user.email,
            slack_id=orm_user.slack_id,
            notion_id=orm_user.notion_id,
            notion_user_id=orm_user.notion_user_id,
            ativo=orm_user.ativo,
            role=orm_user.role,
        )
