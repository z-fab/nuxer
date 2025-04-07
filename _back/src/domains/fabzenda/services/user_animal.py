from datetime import datetime

from domains.fabbank.services.wallet import WalletService
from domains.fabzenda.entities.user_animal import UserAnimalEntity
from domains.fabzenda.repositories.animal_type import AnimalTypeRepository
from domains.fabzenda.repositories.user_animal import UserAnimalRepository
from domains.fabzenda.services.animal_modifier import AnimalModifierService
from domains.user.repositories.user import UserRepository
from shared.dto.service_response import ServiceResponse
from shared.infrastructure.db_context import DatabaseExternal
from shared.utils import fabzenda_utils


class UserAnimalService:
    def __init__(self, db_context: DatabaseExternal):
        self.user_repository = UserRepository(db_context)
        self.user_animal_repository = UserAnimalRepository(db_context)
        self.animal_type_repository = AnimalTypeRepository(db_context)

        self.wallet_service = WalletService(db_context)
        self.animal_modifier_service = AnimalModifierService(db_context)

    def get_user_animals(self, user_id: int) -> ServiceResponse:
        user = self.user_repository.get_user_by_id(user_id)
        user_animals = self.user_animal_repository.get_user_animals_alive_by_user_id(user_id)

        # Verificando se há animais na fabzenda
        if len(user_animals) <= 0:
            return ServiceResponse(success=False, data={"apelido": user.apelido}, error="fazenda_vazia")

        return ServiceResponse(
            success=True,
            data={
                "user_animals": user_animals,
                "user": user,
            },
        )

    def buy_animal(self, user_id: int, animal_type_id: int) -> ServiceResponse:
        animal_type = self.animal_type_repository.get_animal_type_by_id(animal_type_id)

        return self._buy_animal_entity(user_id=user_id, animal_type=animal_type)

    def _buy_animal_entity(self, user_id: int, animal_type: UserAnimalEntity) -> ServiceResponse:
        # Sorteando o modificador
        animal_modifier = self.animal_modifier_service.get_random_modifier()
        animal_modifier_id = animal_modifier.modifier_id if animal_modifier else None

        # Adicionando o animal ao usuário
        animal_name = fabzenda_utils.get_random_animal_names()
        user_animal = self.user_animal_repository.create_user_animal(
            user_id=user_id,
            animal_type_id=animal_type.type_id,
            lifespan=animal_type.lifespan,
            nickname=animal_name,
            id_modifier=animal_modifier_id,
        )

        if not user_animal:
            return ServiceResponse(
                success=False,
                error="animal_not_created",
            )

        return ServiceResponse(
            success=True,
            data={
                "user_animal": user_animal,
                "animal_type": animal_type,
                "animal_modifier": animal_modifier,
            },
        )

    def can_buy_animal(self, user_id: int, animal_type_id: int) -> ServiceResponse:
        animal_type = self.animal_type_repository.get_animal_type_by_id(animal_type_id)

        return self._can_buy_animal_entity(user_id=user_id, animal_type=animal_type)

    def _can_buy_animal_entity(self, user_id: int, animal_type: UserAnimalEntity) -> ServiceResponse:
        max_animals = 3
        user_animals = self.user_animal_repository.get_user_animals_alive_by_user_id(user_id)
        wallet = self.wallet_service.get_balance_info(user_id).data["user_wallet"]

        if len(user_animals) >= max_animals:
            return ServiceResponse(
                success=False,
                error="max_animals_reached",
            )

        # Verificando se o usuário tem saldo suficiente
        if int(wallet.balance) < animal_type.base_price:
            return ServiceResponse(
                success=False,
                error="insufficient_balance",
            )

        # Verificando se o item está disponível
        if not animal_type.available:
            return ServiceResponse(
                success=False,
                error="animal_type_not_available",
            )

        return ServiceResponse(success=True, data={"user_animals": user_animals, "animal_type": animal_type})

    def feed_animal(self, user_id: int, user_animal_id: int) -> ServiceResponse:
        user_animal = self.user_animal_repository.get_user_animal_by_id(user_animal_id)

        return self._feed_animal_entity(user_id=user_id, user_animal=user_animal)

    def _feed_animal_entity(self, user_id: int, user_animal: UserAnimalEntity) -> ServiceResponse:
        user_animal.food_slot = 4
        user_animal.health = 4
        user_animal.last_fed = datetime.now()

        response = self.user_animal_repository.update_user_animal(user_animal)

        if not response:
            return ServiceResponse(
                success=False,
                error="animal_not_updated",
            )

        return ServiceResponse(
            success=True,
            data={
                "user_animal": response,
            },
        )

    def can_feed_animal(self, user_id: int, user_animal_id: int) -> ServiceResponse:
        user_animal = self.user_animal_repository.get_user_animal_by_id(user_animal_id)
        return self._can_feed_animal_entity(user_id=user_id, user_animal=user_animal)

    def _can_feed_animal_entity(self, user_id: int, user_animal: UserAnimalEntity) -> ServiceResponse:
        wallet = self.wallet_service.get_balance_info(user_id).data["user_wallet"]

        # Verificando se o animal existe e está vivo
        if not user_animal or not user_animal.is_alive or user_animal.health == 0:
            return ServiceResponse(
                success=False,
                error="not_possible_to_feed_animal_dead",
            )

        # Verificando se o usuário tem saldo suficiente
        if int(wallet.balance) < user_animal.feeding_cost:
            return ServiceResponse(
                success=False,
                error="not_possible_to_feed_insufficient_balance",
            )

        return ServiceResponse(success=True, data={"user_animal": user_animal})
