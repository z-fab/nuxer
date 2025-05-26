from loguru import logger

from domains.fabbank.use_cases.alterar_saldo import AlterarSaldo
from domains.fabbank.use_cases.comprar_item import ComprarItem
from domains.fabbank.use_cases.consultar_saldo import ConsultarSaldo
from domains.fabbank.use_cases.options import Options
from domains.fabbank.use_cases.transferir import Transferir
from domains.fabbank.use_cases.ver_loja import VerLoja
from interfaces.presenters.presenter_dispatcher import presenter_dispatcher
from shared.dto.use_case_code import FabbankUseCaseCode
from shared.dto.use_case_request import UseCaseRequest
from shared.dto.use_case_response import UseCaseResponse

MAP_USECASE = {
    FabbankUseCaseCode.OPTIONS: Options,
    FabbankUseCaseCode.SALDO: ConsultarSaldo,
    FabbankUseCaseCode.TRANSFERENCIA: Transferir,
    FabbankUseCaseCode.ALTERAR_SALDO: AlterarSaldo,
    FabbankUseCaseCode.LOJA: VerLoja,
    FabbankUseCaseCode.LOJA_COMPRAR_ITEM: ComprarItem,
}


def use_case_dispatcher(use_case_request: UseCaseRequest) -> bool:
    # Obtendo o use case correspondente ao código
    user_case = MAP_USECASE.get(use_case_request.code, None)
    if user_case is None:
        logger.error(f"Use case não encontrado para o código: {use_case_request.code}")
        return False

    logger.info(f"Executando o use case: {user_case.__name__}")
    use_case_response: UseCaseResponse = user_case(use_case_request)()

    if not presenter_dispatcher(use_case_response, use_case_request):
        logger.error(f"Erro ao renderizar resultado do Use Case: {use_case_response.code}")
        return False

    return True
