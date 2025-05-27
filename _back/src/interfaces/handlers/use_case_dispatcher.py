from loguru import logger

from domains.fabbank.use_cases.alterar_saldo import AlterarSaldo
from domains.fabbank.use_cases.comprar_item import ComprarItem as ComprarItemFabbank
from domains.fabbank.use_cases.consultar_saldo import ConsultarSaldo
from domains.fabbank.use_cases.option_loja import OptionLoja
from domains.fabbank.use_cases.transferir import Transferir
from domains.fabbank.use_cases.ver_loja import VerLoja
from domains.fabzenda.use_cases.abduzir_animal import AbduzirAnimal
from domains.fabzenda.use_cases.alimentar_animal import AlimentarAnimal
from domains.fabzenda.use_cases.comprar_animal import ComprarAnimal
from domains.fabzenda.use_cases.comprar_item import ComprarItem as ComprarItemFabzenda
from domains.fabzenda.use_cases.detalhe_animal_celeiro import DetalheAnimalCeleiro
from domains.fabzenda.use_cases.detalhe_animal_fazenda import DetalheAnimalFazenda
from domains.fabzenda.use_cases.detalhe_item_store import DetalheItemStore
from domains.fabzenda.use_cases.enterrar_animal import EnterrarAnimal
from domains.fabzenda.use_cases.option import OptionFabzenda
from domains.fabzenda.use_cases.ver_celeiro import VerCeleiro
from domains.fabzenda.use_cases.ver_fabzenda import VerFabzenda
from domains.fabzenda.use_cases.ver_store import VerStore
from interfaces.presenters.presenter_dispatcher import presenter_dispatcher
from shared.dto.use_case_code import FabbankUseCaseCode, FabzendaUseCaseCode
from shared.dto.use_case_request import UseCaseRequest
from shared.dto.use_case_response import UseCaseResponse

MAP_USECASE = {
    # Fabbank Use Cases
    FabbankUseCaseCode.OPTION_LOJA: OptionLoja,
    FabbankUseCaseCode.SALDO: ConsultarSaldo,
    FabbankUseCaseCode.TRANSFERENCIA: Transferir,
    FabbankUseCaseCode.ALTERAR_SALDO: AlterarSaldo,
    FabbankUseCaseCode.LOJA: VerLoja,
    FabbankUseCaseCode.LOJA_COMPRAR_ITEM: ComprarItemFabbank,
    # Fabzenda Use Cases
    FabzendaUseCaseCode.OPTION: OptionFabzenda,
    FabzendaUseCaseCode.VER_FAZENDA: VerFabzenda,
    FabzendaUseCaseCode.FAZENDA_DETALHE_ANIMAL: DetalheAnimalFazenda,
    FabzendaUseCaseCode.ALIMENTAR_ANIMAL: AlimentarAnimal,
    FabzendaUseCaseCode.ABDUZIR_ANIMAL: AbduzirAnimal,
    FabzendaUseCaseCode.ENTERRAR_ANIMAL: EnterrarAnimal,
    FabzendaUseCaseCode.VER_CELEIRO: VerCeleiro,
    FabzendaUseCaseCode.CELEIRO_DETALHE_ANIMAL: DetalheAnimalCeleiro,
    FabzendaUseCaseCode.CELEIRO_COMPRAR_ANIMAL: ComprarAnimal,
    FabzendaUseCaseCode.VER_STORE: VerStore,
    FabzendaUseCaseCode.STORE_DETALHE_ITEM: DetalheItemStore,
    FabzendaUseCaseCode.STORE_COMPRAR_ITEM: ComprarItemFabzenda,
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
