from loguru import logger

from shared.dto.use_case_code import FabbankUseCaseCode
from shared.dto.use_case_request import UseCaseRequest

MAP_COMMAND_USECASECODE = {
    ## Fabbank
    ("fb", "fabbank"): {
        "": FabbankUseCaseCode.OPTIONS,
        "saldo": FabbankUseCaseCode.SALDO,
        ("transferir", "pix"): FabbankUseCaseCode.TRANSFERENCIA,
        ("change", "alterar"): FabbankUseCaseCode.ALTERAR_SALDO,
        ("loja", "ver_loja"): FabbankUseCaseCode.LOJA,
        "comprar": FabbankUseCaseCode.LOJA_COMPRAR_ITEM,
    },
    # ## Fabzenda
    # ("fz", "fabzenda"): {
    #     "ver": UseCaseCode.FABZENDA_VER_FAZENDA,
    #     "celeiro": UseCaseCode.FABZENDA_VER_CELEIRO,
    #     "store": UseCaseCode.FABZENDA_VER_STORE,
    #     "detalhe_item_store": UseCaseCode.FABZENDA_STORE_DETALHE_ITEM,
    #     "comprar_item": UseCaseCode.FABZENDA_STORE_COMPRAR_ITEM,
    #     "detalhe_animal_celeiro": UseCaseCode.FABZENDA_CELEIRO_DETALHE_ANIMAL,
    #     "comprar_animal": UseCaseCode.FABZENDA_CELEIRO_COMPRAR_ANIMAL,
    #     "alimentar": UseCaseCode.FABZENDA_ALIMENTAR_ANIMAL,
    #     "enterrar": UseCaseCode.FABZENDA_ENTERRAR_ANIMAL,
    #     "abduzir": UseCaseCode.FABZENDA_ABDUZIR_ANIMAL,
    #     "detalhe_animal_fabzenda": UseCaseCode.FABZENDA_FAZENDA_DETALHE_ANIMAL,
    # },
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

    logger.warning(f"Comando não encontrado: {context_info.get('command')}")
    return None
