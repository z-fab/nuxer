# interfaces/presenters/presenter_dispatcher.py
from loguru import logger

from shared.dto.error_code import FabbankError
from shared.dto.use_case_code import FabbankUseCaseCode
from shared.dto.use_case_request import UseCaseRequest
from shared.dto.use_case_response import UseCaseResponse

# Presenters de Mensagem por Domínio
from .slack.message_presenters.fabbank_message_presenter import FabbankMessagePresenter


class PresentationStrategy:
    def __init__(self, presenter_class, target_method_name: str, **kwargs):
        self.presenter_class = presenter_class
        self.target_method_name = target_method_name
        self.kwargs = kwargs


MAP_SUCCESS = {
    ### Fabbank ###
    FabbankUseCaseCode.OPTIONS: {
        "*": PresentationStrategy(FabbankMessagePresenter, "options"),
    },
    FabbankUseCaseCode.SALDO: {
        "slack_message": PresentationStrategy(FabbankMessagePresenter, "consultar_saldo_sucesso"),
        "slack_app_mention": PresentationStrategy(FabbankMessagePresenter, "consultar_saldo_sucesso_dm"),
    },
    FabbankUseCaseCode.TRANSFERENCIA: {
        "*": PresentationStrategy(FabbankMessagePresenter, "transferir_sucesso"),
    },
    FabbankUseCaseCode.ALTERAR_SALDO: {
        "*": PresentationStrategy(FabbankMessagePresenter, "transferir_sucesso"),
    },
    FabbankUseCaseCode.LOJA: {
        "slack_message": PresentationStrategy(FabbankMessagePresenter, "ver_loja_sucesso"),
        "slack_app_mention": PresentationStrategy(FabbankMessagePresenter, "ver_loja_sucesso"),
        "slack_block_actions": PresentationStrategy(FabbankMessagePresenter, "view_ver_loja_sucesso"),
    },
    FabbankUseCaseCode.LOJA_COMPRAR_ITEM: {
        "slack_block_actions": PresentationStrategy(FabbankMessagePresenter, "view_comprar_item_sucesso"),
    },
}

MAP_ERROR = {
    ### Fabbank ###
    FabbankUseCaseCode.SALDO: {
        "*": {"*": PresentationStrategy(FabbankMessagePresenter, "error_generic")},
        FabbankError.WALLET_NOT_FOUND: {"*": PresentationStrategy(FabbankMessagePresenter, "error_wallet_not_found")},
    },
    FabbankUseCaseCode.TRANSFERENCIA: {
        "*": {"*": PresentationStrategy(FabbankMessagePresenter, "error_generic")},
        FabbankError.WALLET_NOT_FOUND: {
            "*": PresentationStrategy(FabbankMessagePresenter, "error_transfer_wallet_not_found")
        },
        FabbankError.INSUFFICIENT_BALANCE: {
            "*": PresentationStrategy(FabbankMessagePresenter, "error_insufficient_balance")
        },
        FabbankError.TRANSFER_WRONG_PARAMS: {"*": PresentationStrategy(FabbankMessagePresenter, "error_wrong_params")},
    },
    FabbankUseCaseCode.ALTERAR_SALDO: {
        "*": {"*": PresentationStrategy(FabbankMessagePresenter, "error_generic")},
        FabbankError.WALLET_NOT_FOUND: {
            "*": PresentationStrategy(FabbankMessagePresenter, "error_transfer_wallet_not_found")
        },
        FabbankError.TRANSFER_PERMISSION_DENIED: {
            "*": PresentationStrategy(FabbankMessagePresenter, "error_transfer_dont_have_permission")
        },
        FabbankError.TRANSFER_WRONG_PARAMS: {"*": PresentationStrategy(FabbankMessagePresenter, "error_wrong_params")},
    },
    FabbankUseCaseCode.LOJA: {"*": {"*": PresentationStrategy(FabbankMessagePresenter, "error_generic")}},
    FabbankUseCaseCode.LOJA_COMPRAR_ITEM: {
        "*": {"*": PresentationStrategy(FabbankMessagePresenter, "error_generic")},
        FabbankError.WALLET_NOT_FOUND: {
            "*": PresentationStrategy(FabbankMessagePresenter, "error_loja_wallet_not_found")
        },
        FabbankError.LOJA_ITEM_UNAVAILABLE: {
            "*": PresentationStrategy(FabbankMessagePresenter, "error_loja_item_unavailable")
        },
        FabbankError.INSUFFICIENT_BALANCE: {
            "*": PresentationStrategy(FabbankMessagePresenter, "error_loja_insufficient_balance")
        },
        FabbankError.LOJA_ITEM_PRICE_CHANGED: {
            "*": PresentationStrategy(FabbankMessagePresenter, "error_loja_item_price_changed")
        },
    },
}


def presenter_dispatcher(response: UseCaseResponse, request: UseCaseRequest) -> bool:
    logger.info(f"Presenter Dispatcher: UseCase {response.code}, Success: {response.success}, Source {request.source}")
    if not response.success:
        logger.warning(f"Error Code: {response.error_code}")
    else:
        logger.debug(f"Response data: {response.data}")

    presentation_strategy = None
    if response.success:
        presentation_strategy = MAP_SUCCESS.get(response.code, {}).get(request.source)
        if not presentation_strategy:
            presentation_strategy = MAP_SUCCESS.get(response.code, {}).get("*")
    else:
        presentation_erro_code = MAP_ERROR.get(response.code, {}).get(response.error_code)
        if not presentation_erro_code:
            presentation_erro_code = MAP_ERROR.get(response.code, {}).get("*", {})

        presentation_strategy = presentation_erro_code.get(request.source)
        if not presentation_strategy:
            presentation_strategy = presentation_erro_code.get("*")

    if not presentation_strategy:
        logger.warning(
            f"Nenhuma estratégia de apresentação (sucesso ou erro) encontrada para UseCase: '{response.code}', Source: '{request.source}', ErrorCode: '{response.error_code}'"
        )
        return False

    try:
        presenter_instance = presentation_strategy.presenter_class(request_payload=request.payload)
        render_method = getattr(presenter_instance, presentation_strategy.target_method_name)

        if response.success:
            render_method(response.data, **presentation_strategy.kwargs)
        else:
            # Passa o UseCaseResponse inteiro para os presenters de erro
            render_method(response, **presentation_strategy.kwargs)

        logger.info(
            f"Apresentação (success={response.success}) para UseCase {response.code.name}, Source {request.source} realizada com '{presentation_strategy.presenter_class.__name__}.{presentation_strategy.target_method_name}'."
        )
        return True
    except AttributeError as e:
        logger.error(
            f"Método '{presentation_strategy.target_method_name}' não encontrado no presenter '{presentation_strategy.presenter_class.__name__}': {e}"
        )
    except Exception as e:
        logger.exception(
            f"Erro durante a execução do presenter para UseCase {response.code.name}, Source {request.source}: {e}"
        )

    return False
