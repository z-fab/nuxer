from datetime import datetime

from domains.fabbank import messages as MSG
from domains.fabbank.entities.wallet import WalletEntity
from domains.fabbank.repositories.transaction import TransactionRepository
from domains.fabbank.repositories.wallet import WalletRepository
from shared.dto.use_case_response import UseCaseResponse


class TransactionService:
    def __init__(self, transaction_repo: TransactionRepository, wallet_repo: WalletRepository):
        self.transaction_repository: TransactionRepository = transaction_repo
        self.wallet_repository: WalletRepository = wallet_repo

    def transfer_coins(self, from_slack_id: str, to_slack_id: str, value: int, description: str) -> UseCaseResponse:
        # Obter as wallets
        wallet_from = self.wallet_repository.get_wallet_by_slack_id(from_slack_id)
        wallet_to = self.wallet_repository.get_wallet_by_slack_id(to_slack_id)

        # Validar as wallets
        if not wallet_from:
            return UseCaseResponse(message=MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_WALLET_NOT_FOUND, success=False)

        if not wallet_to:
            return UseCaseResponse(message=MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_USER_NOT_FOUND, success=False)

        # Validar o valor
        if value <= 0:
            return UseCaseResponse(message=MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_PARAMS, success=False)

        # Validar a descrição
        if not description:
            return UseCaseResponse(message=MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_PARAMS, success=False)

        # Validar o saldo
        if wallet_from.balance < value:
            return UseCaseResponse(message=MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_INSUFFICIENT_BALANCE, success=False)

        # Executar a transferência
        result = self._execute_transfer(wallet_from, wallet_to, value, description)
        if not result:
            return UseCaseResponse(message=MSG.TEMPLATE_FABBANK_TRANSFER_ERROR, success=False)

        # Mensagem para o usuário
        message = MSG.TEMPLATE_FABBANK_TRANSFER_SUCCESS.format(
            apelido=wallet_from.user.apelido,
            amount=value,
            to_name=wallet_to.user.nome,
            to_id_wallet=wallet_to.wallet_id,
            desc=description,
            id_wallet=wallet_from.wallet_id,
            data=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        )

        # Notificação para o usuário de destino
        message_to = MSG.TEMPLATE_FABBANK_TRANSFER_RECEIVE.format(
            to_apelido=wallet_to.user.apelido,
            amount=value,
            from_name=wallet_from.user.nome,
            from_id_wallet=wallet_from.wallet_id,
            desc=description,
        )

        return UseCaseResponse(
            message=message,
            success=True,
            data={
                "wallet_from": wallet_from,
                "wallet_to": wallet_to,
                "notify": {
                    "user": wallet_to.user,
                    "message": message_to,
                },
            },
        )

    def change_coins(self, from_slack_id: str, to_slack_id: str, value: int, description: str) -> UseCaseResponse:
        # Obter a wallet
        wallet_from = self.wallet_repository.get_wallet_by_slack_id(from_slack_id)
        wallet_to = self.wallet_repository.get_wallet_by_slack_id(to_slack_id)

        # Validando acesso
        if not wallet_from or wallet_from.user.role > 0:
            return UseCaseResponse(message=MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_PERMISSION, success=False)

        # Validar a wallet
        if not wallet_to:
            return UseCaseResponse(message=MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_USER_NOT_FOUND, success=False)

        # Validar a descrição
        if not description:
            return UseCaseResponse(message=MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_PARAMS, success=False)

        # Obter a wallet do sistema (ID 0)
        wallet_from = self.wallet_repository.get_wallet_by_user_id(0)
        if not wallet_from:
            return UseCaseResponse(message=MSG.TEMPLATE_FABBANK_TRANSFER_ERROR_WALLET_NOT_FOUND, success=False)

        # Executar a mudança
        result = self._execute_change(wallet_from, wallet_to, value, description)
        if not result:
            return UseCaseResponse(message=MSG.TEMPLATE_FABBANK_TRANSFER_ERROR, success=False)

        # Mensagem para o usuário
        message = MSG.TEMPLATE_FABBANK_TRANSFER_SUCCESS.format(
            apelido=wallet_from.user.apelido,
            amount=value,
            to_name=wallet_to.user.nome,
            to_id_wallet=wallet_to.wallet_id,
            desc=description,
            id_wallet=wallet_from.wallet_id,
            data=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        )

        # Notificação para o usuário de destino
        if value > 0:
            message_to = MSG.TEMPLATE_FABBANK_TRANSFER_RECEIVE
        else:
            message_to = MSG.TEMPLATE_FABBANK_DISCOUNT_RECEIVE

        message_to = message_to.format(
            to_apelido=wallet_to.user.apelido,
            amount=value,
            from_name=wallet_from.user.nome,
            from_id_wallet=wallet_from.wallet_id,
            desc=description,
        )

        return UseCaseResponse(
            message=message,
            success=True,
            data={
                "wallet_from": wallet_from,
                "wallet_to": wallet_to,
                "notify": {
                    "user": wallet_to.user,
                    "message": message_to,
                },
            },
        )

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
