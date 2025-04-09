from domains.fabbank.entities.wallet import WalletEntity
from domains.fabbank.repositories.transaction import TransactionRepository
from domains.fabbank.repositories.wallet import WalletRepository
from interfaces.presenters.hints import FabbankHints
from shared.dto.service_response import ServiceResponse
from shared.infrastructure.db_context import DatabaseExternal


class TransactionService:
    def __init__(self, db_context: DatabaseExternal):
        self.transaction_repository = TransactionRepository(db_context)
        self.wallet_repository = WalletRepository(db_context)

    def transfer_coins(self, from_id: str, to_id: str, value: int, description: str) -> ServiceResponse:
        wallet_from = self.wallet_repository.get_wallet_by_user_id(from_id)
        wallet_to = self.wallet_repository.get_wallet_by_user_id(to_id)

        return self._transfer_coins_entity(wallet_from, wallet_to, value, description)

    def _transfer_coins_entity(
        self, wallet_from: WalletEntity, wallet_to: WalletEntity, value: int, description: str
    ) -> ServiceResponse:
        # Executar a transferência
        result = self._execute_transfer(wallet_from, wallet_to, value, description)
        if not result:
            return ServiceResponse(success=False, error=FabbankHints.TRANSFER_ERROR)

        return ServiceResponse(
            success=True,
            data={"wallet_from": wallet_from, "wallet_to": wallet_to, "value": value, "description": description},
        )

    def validate_transfer_coins(self, from_id: str, to_id: str, value: int, description: str) -> ServiceResponse:
        wallet_from = self.wallet_repository.get_wallet_by_user_id(from_id)
        wallet_to = self.wallet_repository.get_wallet_by_user_id(to_id)

        return self._validate_transfer_coins_entity(wallet_from, wallet_to, value, description)

    def _validate_transfer_coins_entity(
        self, wallet_from: WalletEntity, wallet_to: WalletEntity, value: int, description: str
    ) -> ServiceResponse:
        # Validar as wallets
        if not wallet_from:
            return ServiceResponse(success=False, error=FabbankHints.TRANSFER_WALLET_NOT_FOUND)

        if not wallet_to:
            return ServiceResponse(success=False, error=FabbankHints.TRANSFER_WALLET_NOT_FOUND)

        # Validar o valor
        if value <= 0:
            return ServiceResponse(success=False, error=FabbankHints.TRANSFER_WRONG_PARAMS)

        # Validar a descrição
        if not description:
            return ServiceResponse(success=False, error=FabbankHints.TRANSFER_WRONG_PARAMS)

        # Validar o saldo
        if wallet_from.balance < value:
            return ServiceResponse(success=False, error=FabbankHints.TRANSFER_INSUFFICIENT_BALANCE)

        return ServiceResponse(success=True)

    def _execute_transfer(
        self, wallet_from: WalletEntity, wallet_to: WalletEntity, value: int, description: str
    ) -> bool:
        # Remover moedas da wallet de origem
        result = self.wallet_repository.remove_coins(wallet_from, value)
        if not result:
            return False

        # Adicionar moedas à wallet de destino
        result = self.wallet_repository.add_coins(wallet_to, value)
        if not result:
            # Reverter a remoção de moedas da wallet de origem
            self.wallet_repository.add_coins(wallet_from, value)
            return False

        # Criar a transação
        result = self.transaction_repository.create_transaction(wallet_from, wallet_to, value, description)
        return result

    #####
    def change_coins(self, to_id: str, value: int, description: str) -> ServiceResponse:
        # Obter a wallet
        wallet_to = self.wallet_repository.get_wallet_by_user_id(to_id)

        return self._change_coins_entity(wallet_to, value, description)

    def _change_coins_entity(self, wallet_to: WalletEntity, value: int, description: str) -> ServiceResponse:
        wallet_from = self.wallet_repository.get_wallet_by_user_id(0)

        # Executar a mudança
        result = self._execute_change(wallet_from, wallet_to, value, description)
        if not result:
            return ServiceResponse(success=False, error=FabbankHints.TRANSFER_ERROR)

        return ServiceResponse(
            success=True,
            data={"wallet_from": wallet_from, "wallet_to": wallet_to, "value": value, "description": description},
        )

    def validate_change_coins(self, from_id: str, to_id: str, value: int, description: str) -> ServiceResponse:
        wallet_from = self.wallet_repository.get_wallet_by_user_id(from_id)
        wallet_to = self.wallet_repository.get_wallet_by_user_id(to_id)

        return self._validate_change_coins_entity(wallet_from, wallet_to, value, description)

    def _validate_change_coins_entity(
        self, wallet_from: WalletEntity, wallet_to: WalletEntity, value: int, description: str
    ) -> ServiceResponse:
        # Validando acesso
        if not wallet_from or wallet_from.user.role > 0:
            return ServiceResponse(success=False, error=FabbankHints.TRANSFER_PERMISSION_DENIED)

        # Validar a wallet
        if not wallet_to:
            return ServiceResponse(success=False, error=FabbankHints.TRANSFER_WALLET_NOT_FOUND)

        # Validar se o valor é numérico
        if not isinstance(value, int):
            return ServiceResponse(success=False, error=FabbankHints.TRANSFER_WRONG_PARAMS)

        # Validar a descrição
        if not description:
            return ServiceResponse(success=False, error=FabbankHints.TRANSFER_WRONG_PARAMS)

        # Obter a wallet do sistema (ID 0)
        wallet_from = self.wallet_repository.get_wallet_by_user_id(0)
        if not wallet_from:
            return ServiceResponse(success=False, error=FabbankHints.TRANSFER_WALLET_NOT_FOUND)

        return ServiceResponse(success=True)

    def _execute_change(self, wallet_from: WalletEntity, wallet_to: WalletEntity, value: int, description: str) -> bool:
        if value >= 0:
            # Adicionar moedas à wallet de destino
            result = self.wallet_repository.add_coins(wallet_to, value)
        else:
            # Remover moedas da wallet de destino
            result = self.wallet_repository.remove_coins(wallet_to, abs(value))

        if not result:
            return False

        # Criar a transação
        result = self.transaction_repository.create_transaction(wallet_from, wallet_to, value, description)
        return result
