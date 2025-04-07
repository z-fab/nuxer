from collections.abc import Callable
from typing import Any

from actions.action import Action
from config.const import CONST_ERROR, CONST_MESSAGE, CONST_VIEW
from externals.context import Context
from loguru import logger
from repositories.fabzenda_repository import (
    fetch_animal_type_by_id,
)
from repositories.users_repository import get_users_by_slack_id
from services.fabzenda_service import FabzendaService
from utils.slack_utils import get_random_saudacao

from models.entities.user_entity import UserEntity
from models.fabzenda.entities.user_animal_entity import UserAnimalEntity

context = Context()


class FabzendaAction(Action):
    PARAMS: list = []
    SET_STATUS: Callable[..., Any] = None
    SAY: Callable[..., Any] = None
    OPEN_VIEW: Callable[..., Any] = None
    USER: UserEntity = None

    def __init__(
        self,
        user: UserEntity,
        params: list,
        set_status: Callable[..., Any],
        say: Callable[..., Any],
        open_view: Callable[..., Any],
    ):
        self.PARAMS = params
        self.SET_STATUS = set_status
        self.SAY = say
        self.USER = user
        self.OPEN_VIEW = open_view

    # def _opt_celeiro(self):
    #     view = CONST_VIEW.VIEW_HOME_FABZENDA
    #     view["title"]["text"] = "Celeiro Canto Bão 🌾"
    #     fbs = FabBankService(self.USER)
    #     all_animals: list[AnimalTypeEntity] = fetch_all_animal_types()

    #     animals = ""
    #     for animal in all_animals:
    #         animals += CONST_MESSAGE.TEMPLATE_FABZENDA_CELEIRO_ANIMAL.format(
    #             id=animal.type_id,
    #             name=animal.name,
    #             emoji=animal.emoji,
    #             price=animal.base_price,
    #             description=animal.description,
    #         )

    #     fbs = FabBankService(self.USER)
    #     balance, _ = fbs.get_saldo()
    #     text = CONST_MESSAGE.TEMPLATE_FABZENDA_CELEIRO.format(
    #         balance=balance,
    #         animals=animals,
    #     )

    #     self.OPEN_VIEW(view=view, content=text)

    # def _opt_detalhe_animal(self):
    #     animal = fetch_animal_type_by_id(self.PARAMS[1])
    #     view = CONST_VIEW.VIEW_HOME_FABZENDA
    #     view["title"]["text"] = "Detalhe do Fabichinho 🌾"

    #     if not animal:
    #         self.OPEN_VIEW(view=view, content=CONST_MESSAGE.MESSAGE_COMMAND_FB_HELP)
    #         return False

    #     text = CONST_MESSAGE.TEMPLATE_FABZENDA_CELEIRO_ANIMAL_DETALHE
    #     if not animal.available:
    #         text = CONST_MESSAGE.TEMPLATE_FABZENDA_CELEIRO_ANIMAL_DETALHE_UNAVAILABLE

    #     text = text.format(
    #         id=animal.type_id,
    #         name=animal.name,
    #         emoji=animal.emoji,
    #         price=animal.base_price,
    #         reward=animal.base_reward,
    #         hunger_rate=animal.hunger_rate,
    #         lifespan=animal.lifespan,
    #         description=animal.description,
    #     )

    #     self.OPEN_VIEW(view=view, content=text)

    # def _opt_comprar_animal(self):
    #     view = CONST_VIEW.VIEW_HOME_FABZENDA
    #     animal = fetch_animal_type_by_id(self.PARAMS[1])
    #     fzs = FabzendaService(self.USER)

    #     try:
    #         user_animal: UserAnimalEntity = fzs.comprar_animal(self.USER, animal)

    #         modifier_text = ""
    #         if user_animal.modifier:
    #             modifier_text = f"Seu fabichinho é `{user_animal.modifier.name} {user_animal.modifier.emoji}`\n"
    #             modifier_text += f": {user_animal.modifier.description}"
    #         else:
    #             modifier_text = "Seu fabichinho é `Normal 🌱`"
    #             modifier_text += ": Ele não tem nenhum modificador especial mas é muito especial para você"

    #         text = CONST_MESSAGE.TEMPLATE_FABZENDA_CELEIRO_ANIMAL_COMPRADO.format(
    #             apelido=self.USER.apelido, emoji=animal.emoji, nome=user_animal.name, modifier=modifier_text
    #         )

    #         view["title"]["text"] = "Fabichinho Adotado 🎉"
    #         self.OPEN_VIEW(view=view, content=text)

    #     except Exception as e:
    #         logger.warning(f"Erro ao comprar animal: {e}")

    #         match str(e):
    #             case CONST_ERROR.FABZENDA_COMPRAR_BALANCE_INSUFFICIENT:
    #                 text = CONST_MESSAGE.TEMPLATE_FABZENDA_CELEIRO_ANIMAL_ERROR_INSUFFICIENT_BALANCE.format(
    #                     apelido=self.USER.apelido
    #                 )
    #             case CONST_ERROR.FABZENDA_COMPRAR_MAX_ANIMALS:
    #                 text = CONST_MESSAGE.TEMPLATE_FABZENDA_CELEIRO_ANIMAL_ERROR_MAX_ANIMALS.format(
    #                     apelido=self.USER.apelido
    #                 )
    #             case _:
    #                 text = CONST_MESSAGE.TEMPLATE_FABZENDA_CELEIRO_ANIMAL_NAO_COMPRADO.format(apelido=self.USER.apelido)

    #         view["title"]["text"] = "Ops, deu errado! ⚠️"
    #         self.OPEN_VIEW(view=view, content=text)
    #         return False

    # def _opt_ver_fazenda(self):
    #     view = CONST_VIEW.VIEW_HOME_FABZENDA
    #     animals: list[UserAnimalEntity] = fetch_user_animals_alive(self.USER)

    #     if len(animals) <= 0:
    #         view["title"]["text"] = "Sua Fabzenda 🏕️"
    #         self.OPEN_VIEW(
    #             view=view, content=CONST_MESSAGE.TEMPLATE_FABZENDA_FAZENDA_VAZIA.format(apelido=self.USER.apelido)
    #         )
    #         return False

    #     slots = [f"{animal.animal_type.emoji}" for animal in animals]

    #     animals_text = ""
    #     for animal in animals:
    #         modifier_status = calculate_animal_stats_with_modifier(animal)
    #         if animal.health == 0:
    #             animals_text += CONST_MESSAGE.TEMPLATE_FABZENDA_FAZENDA_ANIMAL_MORTO.format(
    #                 emoji=animal.animal_type.emoji,
    #                 burial_cost=modifier_status["burial_cost"],
    #                 type=animal.animal_type.name,
    #                 name=animal.name,
    #                 health=animal.health_str,
    #                 id=animal.animal_id,
    #             )
    #             continue

    #         if animal.expiry_date < datetime.now():
    #             animals_text += CONST_MESSAGE.TEMPLATE_FABZENDA_FAZENDA_ANIMAL_EXPIRADO.format(
    #                 emoji=animal.animal_type.emoji,
    #                 expire_value=modifier_status["expire_value"],
    #                 type=animal.animal_type.name,
    #                 name=animal.name,
    #                 id=animal.animal_id,
    #             )
    #             continue

    #         food_slot_full = " `🍔` " * animal.food_slot
    #         food_slot_empty = " `‧` " * (4 - animal.food_slot)
    #         hunger = f"{food_slot_full}{food_slot_empty}"

    #         age = (datetime.now() - animal.purchase_date).days

    #         map_health_description = {
    #             4: CONST_MESSAGE.TEMPLATE_FABZENDA_FAZENDA_ANIMAL_HEALTH_4,
    #             3: CONST_MESSAGE.TEMPLATE_FABZENDA_FAZENDA_ANIMAL_HEALTH_3,
    #             2: CONST_MESSAGE.TEMPLATE_FABZENDA_FAZENDA_ANIMAL_HEALTH_2,
    #             1: CONST_MESSAGE.TEMPLATE_FABZENDA_FAZENDA_ANIMAL_HEALTH_1,
    #         }
    #         health_description = map_health_description.get(
    #             animal.health, CONST_MESSAGE.TEMPLATE_FABZENDA_FAZENDA_ANIMAL_HEALTH_4
    #         )

    #         animals_text += CONST_MESSAGE.TEMPLATE_FABZENDA_FAZENDA_ANIMAL.format(
    #             emoji=animal.animal_type.emoji,
    #             type=animal.animal_type.name,
    #             name=animal.name,
    #             reward=modifier_status["reward"],
    #             expire_value=modifier_status["expire_value"],
    #             modifier=f"{animal.modifier.name} {animal.modifier.emoji}" if animal.modifier else "Normal 🌱",
    #             modifier_description=animal.modifier.resume_modifier
    #             if animal.modifier
    #             else "Seu fabichinho é normal (mas continua especial)",
    #             health=animal.health_str,
    #             health_description=health_description,
    #             hunger=hunger,
    #             hunger_rate=modifier_status["hunger_rate"],
    #             age=f"{age} dias" if age > 1 else f"{age} dia" if age == 1 else "Recém-nascido",
    #             lifespan=modifier_status["lifespan"],
    #             feeding_cost=modifier_status["feeding_cost"],
    #             id=animal.animal_id,
    #             primary="P" if (animal.food_slot == 0 or animal.health < 4) else "",
    #         )

    #     text = CONST_MESSAGE.TEMPLATE_FABZENDA_FAZENDA.format(
    #         apelido=self.USER.apelido, slots=" ".join(slots), animals=animals_text
    #     )

    #     view["title"]["text"] = "Sua Fabzenda 🏕️"
    #     self.OPEN_VIEW(view=view, content=text)

    def _opt_alimentar_animal(self):
        view = CONST_VIEW.VIEW_HOME_FABZENDA
        animal_user_id = self.PARAMS[1]
        fzs = FabzendaService(self.USER)

        try:
            fzs.alimentar_animal(animal_user_id)

            text = CONST_MESSAGE.TEMPLATE_FABZENDA_ALIMENTAR_ANIMAL_SUCESSO.format(apelido=self.USER.apelido)

            view["title"]["text"] = "Fabichinho alimentado! 🥘"
            self.OPEN_VIEW(view=view, content=text)

        except Exception as e:
            logger.error(f"Erro ao alimentar animal: {e}")
            match str(e):
                case CONST_ERROR.FABZENDA_ALIMENTAR_ANIMAL_NOT_FOUND:
                    text = CONST_MESSAGE.TEMPLATE_FABZENDA_ALIMENTAR_ANIMAL_NOT_FOUND.format(apelido=self.USER.apelido)
                case CONST_ERROR.FABZENDA_ALIMENTAR_ANIMAL_DEAD:
                    text = CONST_MESSAGE.TEMPLATE_FABZENDA_ALIMENTAR_ANIMAL_DEAD.format(apelido=self.USER.apelido)
                case CONST_ERROR.FABZENDA_ALIMENTAR_INSUFFICIENT_BALANCE:
                    text = CONST_MESSAGE.TEMPLATE_FABZENDA_ALIMENTAR_INSUFFICIENT_BALANCE.format(
                        apelido=self.USER.apelido
                    )
                case _:
                    text = CONST_MESSAGE.TEMPLATE_FABZENDA_ALIMENTAR_ANIMAL_ERROR.format(apelido=self.USER.apelido)

            view["title"]["text"] = "Ops, deu errado! ⚠️"
            self.OPEN_VIEW(view=view, content=text)
            return False

    def _opt_enterrar_animal(self):
        view = CONST_VIEW.VIEW_HOME_FABZENDA
        animal_user_id = self.PARAMS[1]
        fzs = FabzendaService(self.USER)

        try:
            fzs.enterrar_animal(animal_user_id)
            text = CONST_MESSAGE.TEMPLATE_FABZENDA_ENTERRAR_ANIMAL_SUCESSO.format(apelido=self.USER.apelido)

            view["title"]["text"] = "Fabichinho Enterrado 🪦"
            self.OPEN_VIEW(view=view, content=text)

        except Exception as e:
            logger.error(f"Erro ao enterrar animal: {e}")
            match str(e):
                case CONST_ERROR.FABZENDA_ENTERRAR_INSUFFICIENT_BALANCE:
                    text = CONST_MESSAGE.TEMPLATE_FABZENDA_ENTERRAR_ANIMAL_INSUFFICIENT_BALANCE.format(
                        apelido=self.USER.apelido
                    )
                case CONST_ERROR.FABZENDA_ENTERRAR_ANIMAL_NOT_FOUND:
                    text = CONST_MESSAGE.TEMPLATE_FABZENDA_ENTERRAR_ANIMAL_NOT_FOUND.format(apelido=self.USER.apelido)
                case CONST_ERROR.FABZENDA_ENTERRAR_ANIMAL_LIVE:
                    text = CONST_MESSAGE.TEMPLATE_FABZENDA_ENTERRAR_ANIMAL_LIVE.format(apelido=self.USER.apelido)
                case _:
                    text = CONST_MESSAGE.TEMPLATE_FABZENDA_ENTERRAR_ANIMAL_ERROR.format(apelido=self.USER.apelido)

            view["title"]["text"] = "Ops, deu errado! ⚠️"
            self.OPEN_VIEW(view=view, content=text)
            return False

    def _opt_expirar_animal(self):
        view = CONST_VIEW.VIEW_HOME_FABZENDA
        animal_user_id = self.PARAMS[1]
        fzs = FabzendaService(self.USER)

        try:
            fzs.expirar_animal(animal_user_id)
            text = CONST_MESSAGE.TEMPLATE_FABZENDA_EXPIRAR_ANIMAL_SUCESSO.format(apelido=self.USER.apelido)

            view["title"]["text"] = "Fabichinho Abduzido 🛸"
            self.OPEN_VIEW(view=view, content=text)

        except Exception as e:
            logger.error(f"Erro ao abduzir animal: {e}")
            match str(e):
                case CONST_ERROR.FABZENDA_EXPIRAR_ANIMAL_LIVE:
                    text = CONST_MESSAGE.TEMPLATE_FABZENDA_EXPIRAR_ANIMAL_LIVE.format(apelido=self.USER.apelido)
                case _:
                    text = CONST_MESSAGE.TEMPLATE_FABZENDA_ENTERRAR_ANIMAL_ERROR.format(apelido=self.USER.apelido)

            view["title"]["text"] = "Ops, deu errado! ⚠️"
            self.OPEN_VIEW(view=view, content=text)
            return False

    def _opt_add_animal(self):
        if self.USER.role > 0:
            self.SAY(
                CONST_MESSAGE.MESSAGE_COMMAND_ADMIN_ONLY,
                "Ops! Você não tem autorização :eyes:",
            )
            return False

        to = self.PARAMS[1].replace("<@", "").replace(">", "")
        user_to = get_users_by_slack_id(to)
        animal = fetch_animal_type_by_id(self.PARAMS[2])
        fzs = FabzendaService(self.USER)

        user_animal: UserAnimalEntity = fzs.adicionar_animal(user_to, animal)

        modifier_text = ""
        if user_animal.modifier:
            modifier_text = f"Seu fabichinho é `{user_animal.modifier.name} {user_animal.modifier.emoji}`\n"
            modifier_text += f": {user_animal.modifier.description}"
        else:
            modifier_text = "Seu fabichinho é `Normal 🌱`"
            modifier_text += ": Ele não tem nenhum modificador especial mas é muito especial para você"

        context.slack.send_dm(
            user_to.slack_id,
            CONST_MESSAGE.TEMPLATE_FABZENDA_CELEIRO_ANIMAL_COMPRADO.format(
                apelido=user_to.apelido, emoji=animal.emoji, nome=user_animal.name, modifier=modifier_text
            ),
            "Novo Fabichinho 🌱",
        )

        self.SAY(
            f"Fabichinho enviado! 🚀\n[{user_animal.emoji}] {user_animal.animal_type.name} ({user_animal.modifier.name}) para {user_to.apelido}",
            "Fabzenda 🌱",
        )

    def run(self):
        self.SET_STATUS("indo para o Interior...", False)
        command = self.PARAMS[0] if len(self.PARAMS) > 0 else ""
        match command:
            case "btn_celeiro":
                return self._opt_celeiro()
            case "btn_detalhes":
                return self._opt_detalhe_animal()
            case "btn_comprar":
                return self._opt_comprar_animal()
            case "btn_ver_fabzenda":
                return self._opt_ver_fazenda()
            case "btn_alimentar":
                return self._opt_alimentar_animal()
            case "btn_enterrar":
                return self._opt_enterrar_animal()
            case "btn_expirar":
                return self._opt_expirar_animal()
            case "add":
                return self._opt_add_animal()
            case _:
                self.SAY(
                    CONST_MESSAGE.TEMPLATE_FABZENDA_OPTIONS.format(saudacao=get_random_saudacao(self.USER.apelido)),
                    "Fabzenda 🌱",
                )
                return False

        return True
