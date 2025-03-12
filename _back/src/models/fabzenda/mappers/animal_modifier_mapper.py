from models.fabzenda.entities.animal_modifier_entity import AnimalModifierEntity
from models.fabzenda.orm.animal_modifier import AnimalModifier


class AnimalModifierMapper:
    DICT_RARITY = {0: "Comum", 1: "Incomum", 2: "Raro"}

    @staticmethod
    def orm_to_entity(orm_modifier: AnimalModifier) -> AnimalModifierEntity:
        feeding_cost_text = AnimalModifierMapper._get_multiplier_text(
            orm_modifier.feeding_cost_multiplier, "A comida custará", "menos fabcoins", "mais fabcoins"
        )

        burial_cost_text = AnimalModifierMapper._get_multiplier_text(
            orm_modifier.burial_cost_multiplier, "O enterro custará", "menos fabcoins", "mais fabcoins"
        )

        hunger_rate_text = AnimalModifierMapper._get_multiplier_text(
            orm_modifier.hunger_rate_multiplier, "O tempo de alimentação será", "menor", "maior"
        )

        expire_value_text = AnimalModifierMapper._get_multiplier_text(
            orm_modifier.expire_multiplier,
            "Quando o fabichinho for abduzido, você receberá",
            "menos fabcoins",
            "mais fabcoins",
        )

        reward_text = AnimalModifierMapper._get_multiplier_text(
            orm_modifier.reward_multiplier,
            "Quando o fabichinho for sorteado, você receberá",
            "menos fabcoins",
            "mais fabcoins",
        )

        lifespan_text = AnimalModifierMapper._get_multiplier_text(
            orm_modifier.lifespan_multiplier, "O fabichinho viverá", "menos tempo", "mais tempo"
        )

        # Texto especial para a chance de encontrar moeda
        found_coin_text = ""
        if orm_modifier.found_coin_percentage == 0:
            found_coin_text = "Não *encontra fabcoins* diariamente"
        elif orm_modifier.found_coin_percentage > 0.05:
            found_coin_text = "Tem *mais chance* de encontrar fabcoins diariamente"
        elif orm_modifier.found_coin_percentage > 0.05:
            found_coin_text = "Tem *menos chance* encontrar fabcoins diariamente"

        resume_text = "Por causa do modificador: "
        list_text = [
            feeding_cost_text,
            burial_cost_text,
            hunger_rate_text,
            expire_value_text,
            reward_text,
            lifespan_text,
            found_coin_text,
        ]

        non_empty_texts = [text for text in list_text if text]
        if non_empty_texts:
            resume_text += "; ".join(non_empty_texts[:-1]) if len(non_empty_texts) > 2 else non_empty_texts[0]
        resume_text += f" e {non_empty_texts[-1]}." if len(non_empty_texts) > 1 else "."

        return AnimalModifierEntity(
            modifier_id=orm_modifier.modifier_id,
            name=orm_modifier.name,
            emoji=orm_modifier.emoji,
            description=orm_modifier.description,
            rarity=orm_modifier.rarity,
            rarity_str=AnimalModifierMapper.DICT_RARITY[orm_modifier.rarity],
            feeding_cost_multiplier=orm_modifier.feeding_cost_multiplier,
            burial_cost_multiplier=orm_modifier.burial_cost_multiplier,
            hunger_rate_multiplier=orm_modifier.hunger_rate_multiplier,
            expire_multiplier=orm_modifier.expire_multiplier,
            reward_multiplier=orm_modifier.reward_multiplier,
            lifespan_multiplier=orm_modifier.lifespan_multiplier,
            found_coin_percentage=orm_modifier.found_coin_percentage,
            resume_modifier=resume_text,
            feeding_cost_text=feeding_cost_text,
            burial_cost_text=burial_cost_text,
            hunger_rate_text=hunger_rate_text,
            expire_value_text=expire_value_text,
            reward_text=reward_text,
            lifespan_text=lifespan_text,
            found_coin_text=found_coin_text,
        )

    @staticmethod
    def _get_multiplier_text(multiplier: float, phrase: str, complement_pos: str, complement_neg: str) -> str:
        if multiplier != 1.0:
            if multiplier < 1.0:
                multiplier_text = f"{phrase} *{abs((multiplier - 1.0) * 100):.0f}% {complement_pos}*"
            else:
                multiplier_text = f"{phrase} *{abs((multiplier - 1.0) * 100):.0f}% {complement_neg}*"
        else:
            multiplier_text = ""

        return multiplier_text

    @staticmethod
    def entity_to_dict(entity: AnimalModifierEntity) -> dict:
        """
        Converte a entidade em um dicionário para uso em APIs ou interfaces.

        Args:
            entity: A entidade do modificador

        Returns:
            Um dicionário com os dados formatados do modificador
        """
        return {
            "id": entity.modifier_id,
            "name": entity.name,
            "emoji": entity.emoji,
            "description": entity.description,
            "rarity": entity.rarity,
            "rarity_str": entity.rarity_str,
            "effects": [
                entity.feeding_cost_text,
                entity.burial_cost_text,
                entity.hunger_rate_text,
                entity.expire_value_text,
                entity.reward_text,
                entity.lifespan_text,
                entity.found_coin_text,
            ],
            "is_negative": entity.is_negative,
        }
