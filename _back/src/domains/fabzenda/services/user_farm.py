from domains.fabzenda.repositories.user_farm import UserFarmRepository
from domains.user.repositories.user import UserRepository
from shared.dto.service_response import ServiceResponse
from shared.infrastructure.db_context import DatabaseExternal


class UserFarmService:
    def __init__(self, db_context: DatabaseExternal):
        self.user_repository = UserRepository(db_context)
        self.user_farm_repository = UserFarmRepository(db_context)

    def get_user_farm(self, user_id: int) -> ServiceResponse:
        user_farm = self.user_farm_repository.get_user_farm_by_id(user_id)

        if not user_farm:
            user_farm = self.user_farm_repository.create_user_farm(user_id=user_id)

        return ServiceResponse(success=True, data={"user_farm": user_farm})
