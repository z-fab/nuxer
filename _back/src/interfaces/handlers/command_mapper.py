from loguru import logger

from shared.dto.use_case_code import FabbankUseCaseCode, FabzendaUseCaseCode
from shared.dto.use_case_request import UseCaseRequest

MAP_COMMAND_USECASECODE = {
    ## Fabbank
    ("fb", "fabbank"): {
        "saldo": FabbankUseCaseCode.SALDO,
        ("transferir", "pix"): FabbankUseCaseCode.TRANSFERENCIA,
        ("change", "alterar"): FabbankUseCaseCode.ALTERAR_SALDO,
        "loja": FabbankUseCaseCode.OPTION_LOJA,
        "ver_loja": FabbankUseCaseCode.LOJA,
        "comprar": FabbankUseCaseCode.LOJA_COMPRAR_ITEM,
    },
    # ## Fabzenda
    ("fz", "fabzenda"): {
        "": FabzendaUseCaseCode.OPTION,
        "ver": FabzendaUseCaseCode.VER_FAZENDA,
        "detalhe_animal_fabzenda": FabzendaUseCaseCode.FAZENDA_DETALHE_ANIMAL,
        "alimentar": FabzendaUseCaseCode.ALIMENTAR_ANIMAL,
        "abduzir": FabzendaUseCaseCode.ABDUZIR_ANIMAL,
        "enterrar": FabzendaUseCaseCode.ENTERRAR_ANIMAL,
        "celeiro": FabzendaUseCaseCode.VER_CELEIRO,
        "detalhe_animal_celeiro": FabzendaUseCaseCode.CELEIRO_DETALHE_ANIMAL,
        "comprar_animal": FabzendaUseCaseCode.CELEIRO_COMPRAR_ANIMAL,
        "store": FabzendaUseCaseCode.VER_STORE,
        "detalhe_item_store": FabzendaUseCaseCode.STORE_DETALHE_ITEM,
        "comprar_item": FabzendaUseCaseCode.STORE_COMPRAR_ITEM,
    },
    # # Debriefing
    # ("db", "debriefing"): {
    #     "ver_debriefing": UseCaseCode.DEBRIEFING_NOTIFICAR,
    #     "validar_debriefing": UseCaseCode.DEBRIEFING_VALIDAR,
    # },
}


def command_mapper(context_info: dict) -> UseCaseRequest | None:
    """
    Map a command and its arguments to a UseCaseCode.
    """
    for cmd, usecase_map in MAP_COMMAND_USECASECODE.items():
        if context_info.get("command") in cmd:
            # Verificando se há uma opção
            if len(context_info.get("args")) > 0:
                opt_search = context_info.get("args")[0]

                for opt, usecase in usecase_map.items():
                    # Verifica se a opção é uma tupla
                    if type(opt) is tuple:
                        if opt_search in opt:
                            return UseCaseRequest(source=context_info["source"], code=usecase, payload=context_info)
                    # Se a opção não for uma tupla, verifica se é igual
                    else:
                        if opt_search == opt:
                            return UseCaseRequest(source=context_info["source"], code=usecase, payload=context_info)

            # Sem argumento
            else:
                return UseCaseRequest(
                    source=context_info["source"], code=usecase_map.get("", None), payload=context_info
                )

    logger.warning(f"Comando não encontrado: {context_info.get('command')} com args: {context_info.get('args', [])}")
    return None
