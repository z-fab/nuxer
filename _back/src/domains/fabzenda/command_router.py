from domains.fabzenda.use_cases.abduzir_animal import AbduzirAnimal
from domains.fabzenda.use_cases.alimentar_animal import AlimentarAnimal
from domains.fabzenda.use_cases.comprar_animal import ComprarAnimal
from domains.fabzenda.use_cases.detalhe_animal_celeiro import DetalheAnimalCeleiro
from domains.fabzenda.use_cases.detalhe_animal_fazenda import DetalheAnimalFazenda
from domains.fabzenda.use_cases.enterrar_animal import EnterrarAnimal
from domains.fabzenda.use_cases.ver_celeiro import VerCeleiro
from domains.fabzenda.use_cases.ver_fabzenda import VerFabzenda
from interfaces.presenters.hints import FabzendaHints
from shared.dto.slack_command_input import SlackCommandInput
from shared.dto.use_case_response import UseCaseResponse


def handle_fabzenda(input_data: SlackCommandInput, set_status: callable) -> UseCaseResponse:
    set_status("Indo para o interior...")

    option = ""
    if len(input_data.args) > 0:
        option = input_data.args[0]

    match option:
        case "ver":
            return VerFabzenda(input_data)()
        case "celeiro":
            return VerCeleiro(input_data)()
        case "detalhe_animal_celeiro":
            return DetalheAnimalCeleiro(input_data)()
        case "comprar_animal":
            return ComprarAnimal(input_data)()
        case "alimentar":
            return AlimentarAnimal(input_data)()
        case "enterrar":
            return EnterrarAnimal(input_data)()
        case "abduzir":
            return AbduzirAnimal(input_data)()
        case "detalhe_animal_fabzenda":
            return DetalheAnimalFazenda(input_data)()
        case _:
            return UseCaseResponse(
                success=True,
                notification=[
                    {"presenter_hint": FabzendaHints.FAZENDA_OPTIONS},
                ],
            )
