import random

from domains.fabzenda.entities.animal_modifier import AnimalModifierEntity
from domains.fabzenda.repositories.animal_modifier import AnimalModifierRepository
from shared.infrastructure.db_context import DatabaseExternal


class AnimalModifierService:
    def __init__(self, db_context: DatabaseExternal):
        self.animal_modifier_repository = AnimalModifierRepository(db_context)

    def get_random_modifier(self) -> AnimalModifierEntity:
        chance_no_modifier = 0.60
        chance_common = 0.25
        chance_uncommon = 0.10
        chance_rare = 0.05

        # Random roll
        roll = random.random()

        # Determine modifier rarity or no modifier
        selected_modifier = None
        if roll >= chance_no_modifier:
            if roll < chance_no_modifier + chance_common:
                rarity = 0  # Common
            elif roll < chance_no_modifier + chance_common + chance_uncommon:
                rarity = 1  # Uncommon
            else:
                rarity = 2  # Rare

            # Get all modifiers of the selected rarity
            modifiers = self.animal_modifier_repository.get_modifier_by_rarity(rarity)
            if modifiers:
                # Select a random modifier from the list
                selected_modifier = random.choice(modifiers)

        return selected_modifier
