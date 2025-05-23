from datetime import datetime

from domains.fabbank.services.wallet import WalletService
from domains.fabzenda.entities.user_animal import UserAnimalEntity
from domains.fabzenda.repositories.animal_type import AnimalTypeRepository
from domains.fabzenda.repositories.inventory_item import InventoryItemRepository
from domains.fabzenda.repositories.user_animal import UserAnimalRepository
from domains.fabzenda.services.animal_modifier import AnimalModifierService
from domains.fabzenda.services.item import ItemService
from domains.user.repositories.user import UserRepository
from interfaces.presenters.hints import FabzendaHints
from shared.dto.service_response import ServiceResponse
from shared.infrastructure.db_context import DatabaseExternal
from shared.utils import fabzenda_utils


class UserAnimalService:
    def __init__(self, db_context: DatabaseExternal):
        self.user_repository = UserRepository(db_context)
        self.user_animal_repository = UserAnimalRepository(db_context)
        self.animal_type_repository = AnimalTypeRepository(db_context)
        self.inventory_item_repository = InventoryItemRepository(db_context)

        self.wallet_service = WalletService(db_context)
        self.animal_modifier_service = AnimalModifierService(db_context)
        self.item_service = ItemService(db_context)

    def get_user_animals(self, user_id: int) -> ServiceResponse:
        user = self.user_repository.get_user_by_id(user_id)
        user_animals = self.user_animal_repository.get_user_animals_alive_by_user_id(user_id)

        # Verificando se há animais na fabzenda
        if len(user_animals) <= 0:
            return ServiceResponse(
                success=False, data={"apelido": user.apelido}, error=FabzendaHints.FAZENDA_OVERVIEW_VAZIA
            )

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
                error=FabzendaHints.CELEIRO_CREATED_ERROR,
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
        user_animals = self.user_animal_repository.get_user_animals_alive_by_user_id(user_id)
        wallet = self.wallet_service.get_balance_info(user_id).data["user_wallet"]

        # Verificando se o usuário tem itens que aumentam o número de slots de animais
        qtd_aditional_animals = self.item_service.get_additional_animals_slot_by_user(user_id=user_id)
        max_animals = 3 + qtd_aditional_animals.data["n_animals"]

        if len(user_animals) >= max_animals:
            return ServiceResponse(
                success=False,
                error=FabzendaHints.CELEIRO_MAX_ANIMALS_REACHED,
            )

        # Verificando se o usuário tem saldo suficiente
        if int(wallet.balance) < animal_type.base_price:
            return ServiceResponse(
                success=False,
                error=FabzendaHints.CELEIRO_INSUFFICIENT_BALANCE,
            )

        # Verificando se o item está disponível
        if not animal_type.available:
            return ServiceResponse(
                success=False,
                error=FabzendaHints.CELEIRO_ANIMAL_TYPE_NOT_AVAILABLE,
            )

        return ServiceResponse(success=True, data={"user_animals": user_animals, "animal_type": animal_type})

    def feed_animal(self, user_animal_id: int) -> ServiceResponse:
        user_animal = self.user_animal_repository.get_user_animal_by_id(user_animal_id)

        return self._feed_animal_entity(user_animal=user_animal)

    def _feed_animal_entity(self, user_animal: UserAnimalEntity) -> ServiceResponse:
        user_animal.food_slot = 4
        user_animal.health = 4
        user_animal.last_fed = datetime.now()

        response = self.user_animal_repository.update_user_animal(user_animal)

        if not response:
            return ServiceResponse(
                success=False,
                error=FabzendaHints.FEED_ERROR,
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
                error=FabzendaHints.FEED_ANIMAL_DEAD,
            )

        # Verificando se o usuário tem saldo suficiente
        if int(wallet.balance) < user_animal.feeding_cost:
            return ServiceResponse(
                success=False,
                error=FabzendaHints.FEED_INSUFFICIENT_BALANCE,
            )

        return ServiceResponse(success=True, data={"user_animal": user_animal})

    def burial_animal(self, user_animal_id: int) -> ServiceResponse:
        user_animal = self.user_animal_repository.get_user_animal_by_id(user_animal_id)

        return self._burial_animal_entity(user_animal=user_animal)

    def _burial_animal_entity(self, user_animal: UserAnimalEntity) -> ServiceResponse:
        user_animal.is_alive = False
        user_animal.health = 0

        response = self.user_animal_repository.update_user_animal(user_animal)

        if not response:
            return ServiceResponse(
                success=False,
                error=FabzendaHints.BURIAL_ERROR,
            )

        return ServiceResponse(
            success=True,
            data={
                "user_animal": response,
            },
        )

    def can_burial_animal(self, user_id: int, user_animal_id: int) -> ServiceResponse:
        user_animal = self.user_animal_repository.get_user_animal_by_id(user_animal_id)
        return self._can_burial_animal_entity(user_id=user_id, user_animal=user_animal)

    def _can_burial_animal_entity(self, user_id: int, user_animal: UserAnimalEntity) -> ServiceResponse:
        wallet = self.wallet_service.get_balance_info(user_id).data["user_wallet"]

        # Verificando se o animal existe e está morto
        if not user_animal or not user_animal.is_alive or user_animal.health != 0:
            return ServiceResponse(
                success=False,
                error=FabzendaHints.BURIAL_ANIMAL_LIVES,
            )

        # Verificando se o usuário tem saldo suficiente
        if int(wallet.balance) < user_animal.burial_cost:
            return ServiceResponse(
                success=False,
                error=FabzendaHints.BURIAL_INSUFFICIENT_BALANCE,
            )

        return ServiceResponse(success=True, data={"user_animal": user_animal})

    def abduction_animal(self, user_animal_id: int) -> ServiceResponse:
        user_animal = self.user_animal_repository.get_user_animal_by_id(user_animal_id)

        return self._abduction_animal_entity(user_animal=user_animal)

    def _abduction_animal_entity(self, user_animal: UserAnimalEntity) -> ServiceResponse:
        user_animal.is_alive = False
        user_animal.health = -1

        response = self.user_animal_repository.update_user_animal(user_animal)
        if not response:
            return ServiceResponse(
                success=False,
                error=FabzendaHints.ABDUCTION_ERROR,
            )

        return ServiceResponse(
            success=True,
            data={
                "user_animal": response,
            },
        )

    def can_abduction_animal(self, user_animal_id: int) -> ServiceResponse:
        user_animal = self.user_animal_repository.get_user_animal_by_id(user_animal_id)
        return self._can_abduction_animal_entity(user_animal=user_animal)

    def _can_abduction_animal_entity(self, user_animal: UserAnimalEntity) -> ServiceResponse:
        print("not user_animal", not user_animal)
        print("user_animal.is_alive", not user_animal.is_alive)
        print("user_animal.health", user_animal.health not in (0, -1))
        print(user_animal.expiry_date > datetime.now())
        print("user_animal.expiry_date", user_animal.expiry_date)
        print("datetime.now()", datetime.now())
        # Verificando se o animal existe e está morto
        if (
            not user_animal
            or not user_animal.is_alive
            or user_animal.health in (0, -1)
            or user_animal.expiry_date > datetime.now()
        ):
            return ServiceResponse(
                success=False,
                error=FabzendaHints.ABDUCTION_ANIMAL_LIVES,
            )

        return ServiceResponse(success=True, data={"user_animal": user_animal})
