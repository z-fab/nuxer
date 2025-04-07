from loguru import logger

from interfaces.presenters.slack.view.fabzenda import FabzendaSlackPresenter
from shared.dto.use_case_response import UseCaseResponse


class ViewPresenter:
    def __init__(self):
        self.fabzenda = FabzendaSlackPresenter()
        self._registry = {
            "fabzenda.fazenda_vazia": self.fabzenda.fazenda_vazia,
            "fabzenda.ver_fazenda": self.fabzenda.fazenda_overview,
            "fabzenda.ver_celeiro": self.fabzenda.celeiro_overview,
            "fabzenda.wallet_not_found": self.fabzenda.wallet_not_found,
            "fabzenda.detalhe_animal_celeiro": self.fabzenda.detalhe_animal_celeiro,
            "fabzenda.max_animals_reached": self.fabzenda.max_animals_reached,
            "fabzenda.insufficient_balance": self.fabzenda.insufficient_balance,
            "fabzenda.transaction_error": self.fabzenda.transaction_error,
            "fabzenda.comprar_animal": self.fabzenda.comprar_animal,
            "fabzenda.alimentar_animal": self.fabzenda.alimentar_animal,
            "fabzenda.animal_not_created": self.fabzenda.generic_error,
            "fabzenda.animal_type_not_available": self.fabzenda.generic_error,
        }

    def render(self, response: UseCaseResponse, presenter_hint: str) -> str:
        if presenter_hint in self._registry:
            return self._registry[presenter_hint](**response.data)

        logger.warning(f"Presenter hint '{presenter_hint}' não encontrado no registro.")
        return None, "Não consegui entender o que você quis dizer."
