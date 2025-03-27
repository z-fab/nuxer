import random
from collections import defaultdict
from datetime import datetime, timedelta
from math import floor

from loguru import logger

from config.const import CONST_ERROR, CONST_MESSAGE, CONST_SLACK
from externals.context import Context
from models.entities.user_entity import UserEntity
from models.fabzenda.entities.animal_type_entity import AnimalTypeEntity
from models.fabzenda.entities.user_animal_entity import UserAnimalEntity
from repositories import fabbank_repository as fbr
from repositories import fabzenda_repository as fzr
from repositories.configs_repository import get_config_by_name
from services.fabbank_service import FabBankService
from utils import fabzenda_utils as fabzenda_utils
from utils import slack_utils as slack_utils

context = Context()


class FabzendaService:
    USER: UserEntity = None

    def __init__(self, user: UserEntity = None):
        self.USER = user

    def comprar_animal(self, user: UserEntity, animal: AnimalTypeEntity):
        max_animals = int(get_config_by_name("MAX_ANIMALS").value)
        user_animals = fzr.fetch_user_animals_alive(user)
        wallet = fbr.get_wallet_by_user_id(user.id)

        if len(user_animals) >= max_animals:
            raise ValueError(CONST_ERROR.FABZENDA_COMPRAR_MAX_ANIMALS)

        # Verificando se o usuário tem saldo suficiente
        if int(wallet.balance) < animal.base_price:
            raise ValueError(CONST_ERROR.FABZENDA_COMPRAR_BALANCE_INSUFFICIENT)

        # Verificando se o item está disponível
        if not animal.available:
            raise ValueError(CONST_ERROR.FABZENDA_COMPRAR_ANIMAL_UNAVAILABLE)

        # realizando a compra
        if not fbr.remove_coins(wallet, animal.base_price):
            raise RuntimeError(CONST_ERROR.FABZENDA_COMPRA_ANIMAL_FAILED)

        # Adicionando o animal ao usuário
        animal_name = fabzenda_utils.get_random_animal_names()
        user_animal = fzr.create_user_animal(user, animal, animal_name)
        if not user_animal:
            raise RuntimeError(CONST_ERROR.FABZENDA_COMPRA_ANIMAL_FAILED)

        user_animal = fzr.assign_random_modifier_to_animal(user_animal)

        fbr.create_transaction(
            fbr.get_wallet_by_user_id(0),
            wallet,
            animal.base_price * (-1),
            f"Compra de Fabichinho: {animal.name}",
        )

        return user_animal

    def adicionar_animal(self, user: UserEntity, animal: AnimalTypeEntity):
        # Adicionando o animal ao usuário
        animal_name = fabzenda_utils.get_random_animal_names()
        user_animal = fzr.create_user_animal(user, animal, animal_name)
        if not user_animal:
            raise RuntimeError(CONST_ERROR.FABZENDA_COMPRA_ANIMAL_FAILED)

        user_animal = fzr.assign_random_modifier_to_animal(user_animal)

        return user_animal

    def alimentar_animal(self, animal_user_id: int):
        user_animal = fzr.fetch_user_animal_by_id(animal_user_id)
        wallet = fbr.get_wallet_by_user_id(user_animal.user_id)
        modifier_status = fzr.calculate_animal_stats_with_modifier(user_animal)
        cost = modifier_status["feeding_cost"]

        # Verificando se o animal existe
        if not user_animal or not user_animal.is_alive:
            raise ValueError(CONST_ERROR.FABZENDA_ALIMENTAR_ANIMAL_NOT_FOUND)

        # Verificando se o animal está vivo
        if user_animal.health == 0:
            raise ValueError(CONST_ERROR.FABZENDA_ALIMENTAR_ANIMAL_DEAD)

        # Verificando se o usuário tem saldo suficiente
        if int(wallet.balance) < cost:
            raise ValueError(CONST_ERROR.FABZENDA_ALIMENTAR_INSUFFICIENT_BALANCE)

        # Realizando a compra
        result = fbr.remove_coins(wallet, cost)

        if not result:
            raise RuntimeError(CONST_ERROR.FABZENDA_ALIMENTAR_ANIMAL_FAILED)

        # Atualizando a fome do animal
        user_animal.food_slot = 4
        user_animal.last_fed = datetime.now()
        user_animal.health = 4

        result = fzr.update_user_animal(user_animal)

        if not result:
            raise RuntimeError(CONST_ERROR.FABZENDA_ALIMENTAR_ANIMAL_FAILED)

        return fbr.create_transaction(
            fbr.get_wallet_by_user_id(0),
            wallet,
            cost * (-1),
            f"Fabzenda: Alimentação do Fabichino {user_animal.name}",
        )

    def enterrar_animal(self, animal_user_id: int):
        user_animal = fzr.fetch_user_animal_by_id(animal_user_id)
        wallet = fbr.get_wallet_by_user_id(user_animal.user_id)
        modifier_status = fzr.calculate_animal_stats_with_modifier(user_animal)
        cost = modifier_status["burial_cost"]

        # Verificando se o animal existe
        if not user_animal or not user_animal.is_alive:
            raise ValueError(CONST_ERROR.FABZENDA_ENTERRAR_ANIMAL_NOT_FOUND)

        # Verificando se o animal está vivo
        if user_animal.health > 0:
            raise ValueError(CONST_ERROR.FABZENDA_ENTERRAR_ANIMAL_LIVE)

        # Realizando a compra
        result = fbr.remove_coins(wallet, cost)

        if not result:
            raise RuntimeError(CONST_ERROR.FABZENDA_ENTERRAR_INSUFFICIENT_BALANCE)

        # Enterrando o animal
        user_animal.is_alive = False
        result = fzr.update_user_animal(user_animal)

        if not result:
            raise RuntimeError(CONST_ERROR.FABZENDA_ENTERRAR_ANIMAL_FAILED)

        return fbr.create_transaction(
            fbr.get_wallet_by_user_id(0),
            wallet,
            0,
            f"Fabzenda: Sepultamento do Fabichinho {user_animal.name}",
        )

    def expirar_animal(self, animal_user_id: int):
        user_animal = fzr.fetch_user_animal_by_id(animal_user_id)
        wallet = fbr.get_wallet_by_user_id(user_animal.user_id)
        modifier_status = fzr.calculate_animal_stats_with_modifier(user_animal)
        reward = modifier_status["expire_value"]

        # Verificando se o animal existe
        if not user_animal or not user_animal.is_alive:
            raise ValueError(CONST_ERROR.FABZENDA_EXPIRAR_ANIMAL_FAILED)

        # Verificando se o animal está vivo
        if user_animal.expiry_date > datetime.now():
            raise ValueError(CONST_ERROR.FABZENDA_EXPIRAR_ANIMAL_LIVE)

        result = fbr.add_coins(wallet, reward)

        if not result:
            raise RuntimeError(CONST_ERROR.FABZENDA_EXPIRAR_ANIMAL_FAILED)

        # Enterrando o animal
        user_animal.is_alive = False
        result = fzr.update_user_animal(user_animal)

        if not result:
            raise RuntimeError(CONST_ERROR.FABZENDA_EXPIRAR_ANIMAL_FAILED)

        return fbr.create_transaction(
            fbr.get_wallet_by_user_id(0),
            wallet,
            0,
            f"Fabzenda: Presente pela abdução do Fabichinho {user_animal.name}",
        )

    def notificate_animal_status(self, user_animal: UserAnimalEntity, message: str = None):
        pass

    def process_update_animals_status(self):
        all_users_animals = fzr.fetch_all_user_animals_alive()
        try:
            for user_animal in all_users_animals:
                last_fed = user_animal.last_fed
                hunger_rate = user_animal.animal_type.hunger_rate

                # Calculando o tempo decorrido excluindo finais de semana
                current_time = datetime.now()
                hours_elapsed = 0

                # Iterando por cada hora desde o último alimentado
                temp_time = last_fed
                while temp_time < current_time:
                    # Verificando se é final de semana (5=sábado, 6=domingo)
                    if temp_time.weekday() < 5:  # Se não for final de semana
                        hours_elapsed += 1

                    temp_time += timedelta(hours=1)

                delta_fed = hours_elapsed
                slots_used = floor(delta_fed / hunger_rate)

                # Atualizando os slots de fome
                user_animal.food_slot = 0
                if slots_used <= 4:
                    user_animal.food_slot = 4 - slots_used

                # Atualizando a saúde do animal
                user_animal.health = 4
                if slots_used == 4:
                    user_animal.health = 3
                elif slots_used == 5:
                    user_animal.health = 2
                elif slots_used == 6:
                    user_animal.health = 1
                elif slots_used >= 7:
                    user_animal.health = 0

                fzr.update_user_animal(user_animal)

            logger.info("Atualização de status dos animais realizada com sucesso")
            return True
        except Exception as e:
            logger.warning(f"Erro ao atualizar os status dos animais: {e}")
            return False

    def process_animal_lottery(self):
        fbs = FabBankService()

        # Função para calcular o prêmio do animal
        def calculate_prize(user_animal: UserAnimalEntity):
            prize = user_animal.animal_type.base_reward

            modifier_status = fzr.calculate_animal_stats_with_modifier(user_animal)
            prize = modifier_status["reward"]

            if user_animal.health == 3:
                prize = prize * 0.75
            elif user_animal.health == 2:
                prize = prize * 0.5
            elif user_animal.health == 1:
                prize = prize * 0.1
            elif user_animal.health == 0:
                prize = 0

            return round(prize)

        # Função para notificar o vencedor
        def notificate_winner(wins: tuple[UserAnimalEntity, int]):
            total_prize = sum([win[1] for win in wins])
            total_prize = total_prize * 1.2 if len(wins) == 3 else total_prize
            total_prize = round(total_prize)
            user = wins[0][0].user_entity

            fbs.change_coins(user, total_prize, "Premiação - Jogo dos Fabichinhos")

            bonus_text = "Você ganhou 20% de bônus por ter 3 animais sorteados!" if len(wins) == 3 else ""

            text = CONST_MESSAGE.TEMPLATE_FABZENDA_LOTTERY_WIN.format(
                apelido=user.apelido, reward=total_prize, bonus=bonus_text
            )

            context.slack.send_dm(user.slack_id, text, "Resultado - Jogo dos Fabichinhos")

            logger.info(
                f"Usuário {user.apelido} ganhou F₵ {total_prize} com {' '.join([win[0].animal_type.name for win in wins])}"
            )

            return True

        # Função para notificar os resultados
        def notificate_results(result: list[AnimalTypeEntity], winners: dict[int, list[tuple[UserAnimalEntity, int]]]):
            result_text = " ".join([animal.emoji for animal in result])

            if len(winners) == 0:
                text = CONST_MESSAGE.TEMPLATE_FABZENDA_LOTTERY_RESULT_NONE.format(result=result_text)

                context.slack.send_message(
                    CONST_SLACK.SLACK_ID_CHANNEL.get("ux_team"), text, "Resultado - Jogo do Fabichinhos"
                )
                return True

            total_reward = sum([sum([win[1] for win in wins]) for wins in winners.values()])
            n_ganhadores = len(winners)

            ganhadores = ""
            for _, wins in winners.items():
                ganhadores += f"> {wins[0][0].user_entity.nome} ganhou `F₵ {sum([win[1] for win in wins])}` com {' '.join([win[0].animal_type.emoji for win in wins])}\n"

            text = CONST_MESSAGE.TEMPLATE_FABZENDA_LOTTERY_RESULT.format(
                result=result_text,
                n_ganhadores="1 ganhador" if n_ganhadores == 1 else f"{n_ganhadores} ganhadores",
                total_reward=total_reward,
                ganhadores=ganhadores,
            )

            context.slack.send_message(
                CONST_SLACK.SLACK_ID_CHANNEL.get("ux_team"), text, "Resultado - Jogo do Fabichinhos"
            )

            return True

        all_animals: AnimalTypeEntity = fzr.fetch_all_animal_types()
        winning_types: list[AnimalTypeEntity] = random.sample(all_animals, 3)

        dict_winners = defaultdict(list)
        for winning_type in winning_types:
            user_animals: list[UserAnimalEntity] = fzr.fetch_all_user_animals_alive_by_type(winning_type.type_id)

            for animal in user_animals:
                prize = calculate_prize(animal)
                dict_winners[animal.user_id].append((animal, prize))

        if len(dict_winners) > 0:
            for _, wins in dict_winners.items():
                notificate_winner(wins)

        notificate_results(winning_types, dict_winners)

    def process_found_coin_for_animals(self):
        all_users_animals = fzr.fetch_all_user_animals_alive()
        for user_animal in all_users_animals:
            if user_animal.health == 4:
                status = fzr.calculate_animal_stats_with_modifier(user_animal)
                if random.random() < status["found_coin_percentage"]:
                    wallet = fbr.get_wallet_by_user_id(user_animal.user_id)
                    coin_value = 1
                    fbr.add_coins(wallet, coin_value)

                    text = CONST_MESSAGE.TEMPLATE_FABZENDA_FOUND_COIN.format(
                        emoji=user_animal.animal_type.emoji,
                        name=user_animal.name,
                        coin_value=coin_value,
                        apelido=user_animal.user_entity.apelido,
                    )
                    user_slack_id = user_animal.user_entity.slack_id

                    context.slack.send_dm(user_slack_id, text, "Fabichinho encontrou algo")

                    fbr.create_transaction(
                        fbr.get_wallet_by_user_id(0),
                        wallet,
                        coin_value,
                        f"Fabzenda: {user_animal.animal_type.name} encontrou fabcoin",
                    )

                    logger.info(
                        f"Fabichinho {user_animal.name} ({user_animal.user_entity.apelido}) encontrou FC {coin_value}"
                    )
