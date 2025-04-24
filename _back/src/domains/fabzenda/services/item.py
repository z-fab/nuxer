from domains.fabbank.services.wallet import WalletService
from domains.fabzenda.entities.item_definition import ItemDefinitionEntity
from domains.fabzenda.repositories.inventory_item import InventoryItemRepository
from domains.fabzenda.repositories.item_definition import ItemDefinitionRepository
from domains.fabzenda.services.animal_modifier import AnimalModifierService
from domains.fabzenda.services.user_farm import UserFarmService
from domains.user.repositories.user import UserRepository
from interfaces.presenters.hints import FabzendaHints
from shared.dto.service_response import ServiceResponse
from shared.infrastructure.db_context import DatabaseExternal


class ItemService:
    def __init__(self, db_context: DatabaseExternal):
        self.user_repository = UserRepository(db_context)
        self.item_definition_repository = ItemDefinitionRepository(db_context)
        self.inventory_item_repository = InventoryItemRepository(db_context)

        self.wallet_service = WalletService(db_context)
        self.animal_modifier_service = AnimalModifierService(db_context)
        self.user_farm_service = UserFarmService(db_context)

    def buy_item(self, user_id: int, item_id: int) -> ServiceResponse:
        item = self.item_definition_repository.get_item_definition_by_id(item_id)

        return self._buy_item_entity(user_id=user_id, item=item)

    def _buy_item_entity(self, user_id: int, item: ItemDefinitionEntity) -> ServiceResponse:
        # Adicionando o animal ao usuário
        inventory_item = self.inventory_item_repository.create_inventory_item(
            user_id=user_id, item_id=item.item_id, user_animal_id=None, quantity=1, duration=item.duration
        )

        if not inventory_item:
            return ServiceResponse(
                success=False,
                error=FabzendaHints.STORE_BUY_ERROR,
            )

        return ServiceResponse(
            success=True,
            data={"item_definition": item, "inventory_item": inventory_item},
        )

    def can_buy_item(self, user_id: int, item_id: int) -> ServiceResponse:
        item_definition = self.item_definition_repository.get_item_definition_by_id(item_id)

        return self._can_buy_item_entity(user_id=user_id, item=item_definition)

    def _can_buy_item_entity(self, user_id: int, item: ItemDefinitionEntity) -> ServiceResponse:
        wallet = self.wallet_service.get_balance_info(user_id).data["user_wallet"]

        # Verificando se o usuário tem saldo suficiente
        if int(wallet.balance) < item.price:
            return ServiceResponse(
                success=False,
                error=FabzendaHints.STORE_INSUFFICIENT_BALANCE,
            )

        # Verificando se o item está disponível
        if not item.available:
            return ServiceResponse(
                success=False,
                error=FabzendaHints.STORE_ITEM_UNAVAILABLE,
            )

        return ServiceResponse(success=True, data={"item_definition": item})

    def get_additional_animals_slot_by_user(self, user_id: int) -> ServiceResponse:
        inventory_item = self.inventory_item_repository.get_inventory_items_with_effect_by_user(
            user_id, "ADD_SLOT_FARM"
        )
        n_animals = 0
        if inventory_item is not None:
            for item in inventory_item:
                n_animals += item.item_definition.effect["ADD_SLOT_FARM"]

        return ServiceResponse(
            success=True,
            data={"n_animals": n_animals},
        )
