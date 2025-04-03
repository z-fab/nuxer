import random
from datetime import datetime, timedelta

from loguru import logger

from externals.context import Context
from models.entities.user_entity import UserEntity
from models.fabzenda.entities.animal_modifier_entity import AnimalModifierEntity
from models.fabzenda.entities.animal_type_entity import AnimalTypeEntity
from models.fabzenda.entities.user_animal_entity import UserAnimalEntity
from models.fabzenda.mappers.animal_modifier_mapper import AnimalModifierMapper
from models.fabzenda.mappers.animal_type_mapper import AnimalTypeMapper
from models.fabzenda.mappers.user_animal_mapper import UserAnimalMapper
from models.fabzenda.orm.animal_modifier import AnimalModifier
from models.fabzenda.orm.animal_type import AnimalType
from models.fabzenda.orm.user_animal import UserAnimal
from repositories.users_repository import get_users_by_id

context = Context()


def fetch_all_animal_types() -> AnimalTypeEntity:
    """
    Retrieve all animal types from the database.

    Returns:
        list[AnimalTypeEntity]: A list of animal type entities ordered by type_id.
        None: If no animal types are found in the database.

    Note:
        The ORM objects are detached from the session before returning.
    """
    with context.db.session() as session:
        animal_list = session.query(AnimalType).order_by(AnimalType.type_id).all()
        session.expunge_all()
        if not animal_list:
            return None

        return [AnimalTypeMapper.orm_to_entity(animal) for animal in animal_list]


def fetch_animal_type_by_id(animal_id: int) -> AnimalTypeEntity:
    """
    Retrieves an animal type by its ID from the database.

    Args:
        animal_id (int): The ID of the animal type to retrieve.

    Returns:
        AnimalTypeEntity: The mapped animal type entity if found, None otherwise.
    """
    with context.db.session() as session:
        animal = session.query(AnimalType).filter(AnimalType.type_id == animal_id).first()
        session.expunge_all()
        if not animal:
            return None

        return AnimalTypeMapper.orm_to_entity(animal)


def fetch_user_animal_by_id(animal_id: int) -> UserAnimalEntity:
    """
    Retrieves a user animal by its ID.

    This function queries the database for a UserAnimal with the specified ID,
    then maps it to a UserAnimalEntity object and enriches it with additional
    related data.

    Args:
        animal_id (int): The ID of the animal to retrieve.

    Returns:
        UserAnimalEntity: The retrieved user animal entity with enriched data.
        None: If no user animal with the specified ID is found.

    Note:
        This function enriches the returned entity with animal type and user entity information.
    """
    with context.db.session() as session:
        user_animal = session.query(UserAnimal).filter(UserAnimal.animal_id == animal_id).first()
        session.expunge_all()

        if not user_animal:
            return None

        user_animal = UserAnimalMapper.orm_to_entity(user_animal)
        user_animal.animal_type = fetch_animal_type_by_id(user_animal.type_id)
        user_animal.user_entity = get_users_by_id(user_animal.user_id)
        user_animal.modifier = fetch_modifier_by_id(user_animal.modifier_id) if user_animal.modifier_id else None

        return user_animal


def fetch_user_animals(user: UserEntity) -> list[UserAnimal]:
    """
    Retrieves all animals associated with a specific user.

    This function queries the database for all animal records linked to the provided user,
    converts them from ORM models to entity objects, and enriches them with related
    animal type and user information.

    Args:
        user (UserEntity): The user entity whose animals are to be retrieved.

    Returns:
        list[UserAnimal]: A list of UserAnimal entities with enriched data including
                          animal_type and user_entity. Returns an empty list if no
                          animals are found for the user.
    """
    with context.db.session() as session:
        user_animals = session.query(UserAnimal).filter(UserAnimal.user_id == user.id).all()
        session.expunge_all()
        if not user_animals:
            return []

        user_animals_entity = []
        for user_animal in user_animals:
            user_animal_entity = UserAnimalMapper.orm_to_entity(user_animal)
            user_animal_entity.animal_type = fetch_animal_type_by_id(user_animal.type_id)
            user_animal_entity.user_entity = get_users_by_id(user_animal.user_id)
            user_animal.modifier = fetch_modifier_by_id(user_animal.modifier_id) if user_animal.modifier_id else None
            user_animals_entity.append(user_animal_entity)

        return user_animals_entity


def fetch_user_animals_alive(user: UserEntity) -> list[UserAnimal]:
    """
    Retrieves all living animals owned by the specified user.

    This function queries the database for animals that belong to the given user
    and are currently alive, then converts them to domain entities with fully
    populated relationships.

    Args:
        user (UserEntity): The user whose living animals should be retrieved.

    Returns:
        list[UserAnimal]: A list of user animal entities belonging to the user.
                         Returns an empty list if no living animals are found.

    Note:
        The returned animal entities include their associated animal types and user information.
    """
    with context.db.session() as session:
        user_animals = session.query(UserAnimal).filter(UserAnimal.user_id == user.id, UserAnimal.is_alive).all()
        session.expunge_all()
        if not user_animals:
            return []

        user_animals_entity = []
        for user_animal in user_animals:
            user_animal_entity = UserAnimalMapper.orm_to_entity(user_animal)
            user_animal_entity.animal_type = fetch_animal_type_by_id(user_animal.type_id)
            user_animal_entity.user_entity = get_users_by_id(user_animal.user_id)
            user_animal_entity.modifier = (
                fetch_modifier_by_id(user_animal.modifier_id) if user_animal.modifier_id else None
            )
            user_animals_entity.append(user_animal_entity)

        return user_animals_entity


def fetch_all_user_animals_alive() -> list[UserAnimal]:
    """
    Retrieves all living user animals from the database.

    This function queries the database for all user animals that are marked as alive,
    converts the ORM objects to entity objects, and enriches each entity with its
    associated animal type and user entity.

    Returns:
        list[UserAnimal]: A list of user animal entities that are currently alive,
        each enriched with its animal type and user information.
        Returns an empty list if no living user animals are found.
    """
    with context.db.session() as session:
        user_animals = session.query(UserAnimal).filter(UserAnimal.is_alive).all()
        session.expunge_all()
        if not user_animals:
            return []

        user_animals_entity = []
        for user_animal in user_animals:
            user_animal_entity = UserAnimalMapper.orm_to_entity(user_animal)
            user_animal_entity.animal_type = fetch_animal_type_by_id(user_animal.type_id)
            user_animal_entity.user_entity = get_users_by_id(user_animal.user_id)
            user_animal_entity.modifier = (
                fetch_modifier_by_id(user_animal.modifier_id) if user_animal.modifier_id else None
            )
            user_animals_entity.append(user_animal_entity)

        return user_animals_entity


def fetch_all_user_animals_alive_by_type(type_id: int) -> list[UserAnimal]:
    """
    Retrieves all living user animals of a specific type from the database.

    This function queries the database for all user animals of a specific type that are
    marked as alive, converts the ORM objects to entity objects, and enriches each entity
    with its associated animal type and user entity.

    Args:
        type_id (int): The ID of the animal type to filter by.

    Returns:
        list[UserAnimal]: A list of user animal entities of the specified type that are
        currently alive, each enriched with its animal type and user information.
        Returns an empty list if no living user animals of the specified type are found.
    """
    with context.db.session() as session:
        user_animals = session.query(UserAnimal).filter(UserAnimal.is_alive, UserAnimal.type_id == type_id).all()
        session.expunge_all()
        if not user_animals:
            return []

        user_animals_entity = []
        for user_animal in user_animals:
            user_animal_entity = UserAnimalMapper.orm_to_entity(user_animal)
            user_animal_entity.animal_type = fetch_animal_type_by_id(user_animal.type_id)
            user_animal_entity.user_entity = get_users_by_id(user_animal.user_id)
            user_animal_entity.modifier = (
                fetch_modifier_by_id(user_animal.modifier_id) if user_animal.modifier_id else None
            )
            user_animals_entity.append(user_animal_entity)

        return user_animals_entity


def create_user_animal(user: UserEntity, animal: AnimalTypeEntity, nome: str = "Fabichinho") -> UserAnimalEntity:
    """
    Adds a new animal to the user's collection.

    This function creates a new user-animal association in the database, setting up
    initial values for the animal including purchase date, last fed time, and expiration
    date based on the animal's lifespan.

    Args:
        user (UserEntity): The user who will own the animal.
        animal (AnimalTypeEntity): The type of animal to add.
        nome (str, optional): Name for the animal. Defaults to "Fabichinho".

    Returns:
        UserAnimalEntity: The newly created user-animal association entity.
    """
    with context.db.session() as session:
        user_animal = UserAnimal(
            user_id=user.id,
            type_id=animal.type_id,
            name=nome,
            purchase_date=datetime.now(),
            last_fed=datetime.now(),
            expiry_date=datetime.now() + timedelta(days=animal.lifespan),
        )

        session.add(user_animal)
        session.commit()
        return UserAnimalMapper.orm_to_entity(user_animal)


def update_user_animal(user_animal: UserAnimalEntity) -> UserAnimalEntity:
    """
    Updates an animal record in the database with new information.

    Args:
        user_animal (UserAnimalEntity): The animal entity containing updated information

    Returns:
        bool: True if the update was successful, False if an error occurred

    Note:
        While the return type annotation indicates UserAnimalEntity, the function
        actually returns a boolean value indicating success or failure.
    """
    try:
        with context.db.session() as session:
            session.query(UserAnimal).filter(UserAnimal.animal_id == user_animal.animal_id).update(
                {
                    "user_id": user_animal.user_id,
                    "type_id": user_animal.type_id,
                    "name": user_animal.name,
                    "last_fed": user_animal.last_fed,
                    "food_slot": user_animal.food_slot,
                    "health": user_animal.health,
                    "expiry_date": user_animal.expiry_date,
                    "is_alive": user_animal.is_alive,
                    "modifier_id": user_animal.modifier_id,
                }
            )
            session.commit()
            return True
    except Exception as e:
        logger.warning(f"Erro ao atualizar o animal: {e}")
        return False


def fetch_all_modifiers() -> list[AnimalModifierEntity]:
    """
    Retrieve all animal modifiers from the database.

    Returns:
        list[AnimalModifierEntity]: A list of animal modifier entities ordered by modifier_id.
        None: If no modifiers are found in the database.

    Note:
        The ORM objects are detached from the session before returning.
    """
    with context.db.session() as session:
        modifiers = session.query(AnimalModifier).order_by(AnimalModifier.modifier_id).all()
        session.expunge_all()
        if not modifiers:
            return None

        return [AnimalModifierMapper.orm_to_entity(modifier) for modifier in modifiers]


def fetch_modifiers_by_rarity(rarity: int) -> list[AnimalModifierEntity]:
    """
    Retrieve all animal modifiers of a specific rarity from the database.

    Args:
        rarity (int): The rarity level to filter by (0=common, 1=uncommon, 2=rare)

    Returns:
        list[AnimalModifierEntity]: A list of animal modifier entities of the specified rarity.
        None: If no modifiers of the specified rarity are found.
    """
    with context.db.session() as session:
        modifiers = session.query(AnimalModifier).filter(AnimalModifier.rarity == rarity).all()
        session.expunge_all()
        if not modifiers:
            return None

        return [AnimalModifierMapper.orm_to_entity(modifier) for modifier in modifiers]


def fetch_modifier_by_id(modifier_id: int) -> AnimalModifierEntity:
    """
    Retrieves a modifier by its ID from the database.

    Args:
        modifier_id (int): The ID of the modifier to retrieve.

    Returns:
        AnimalModifierEntity: The mapped modifier entity if found, None otherwise.
    """
    with context.db.session() as session:
        modifier = session.query(AnimalModifier).filter(AnimalModifier.modifier_id == modifier_id).first()
        session.expunge_all()
        if not modifier:
            return None

        return AnimalModifierMapper.orm_to_entity(modifier)


def assign_random_modifier_to_animal(user_animal: UserAnimalEntity) -> UserAnimalEntity:
    """
    Assigns a random modifier to an animal based on probability.

    There's a 40% chance the animal will have no modifier, 35% chance for a common modifier,
    20% chance for an uncommon modifier, and 5% chance for a rare modifier.

    Args:
        user_animal (UserAnimalEntity): The animal entity to assign a modifier to.

    Returns:
        UserAnimalEntity: The updated animal entity with modifier information.
    """
    # Probability distribution
    chance_no_modifier = 0.60
    chance_common = 0.25
    chance_uncommon = 0.10
    chance_rare = 0.05  # noqa: F841

    # Random roll
    roll = random.random()

    # Determine modifier rarity or no modifier
    modifier_id = None
    if roll >= chance_no_modifier:
        if roll < chance_no_modifier + chance_common:
            rarity = 0  # Common
        elif roll < chance_no_modifier + chance_common + chance_uncommon:
            rarity = 1  # Uncommon
        else:
            rarity = 2  # Rare

        # Get all modifiers of the selected rarity
        modifiers = fetch_modifiers_by_rarity(rarity)
        if modifiers:
            # Select a random modifier from the list
            selected_modifier = random.choice(modifiers)
            modifier_id = selected_modifier.modifier_id

    # Update the animal with the selected modifier
    if modifier_id:
        user_animal.modifier_id = modifier_id
        user_animal.modifier = fetch_modifier_by_id(modifier_id)
        update_user_animal(user_animal)

    return user_animal


def update_animal_modifier(animal_id: int, modifier_id: int) -> bool:
    """
    Updates an animal's modifier in the database.

    Args:
        animal_id (int): The ID of the animal to update.
        modifier_id (int): The ID of the modifier to assign, or None to remove modifier.

    Returns:
        bool: True if the update was successful, False if an error occurred.
    """
    try:
        with context.db.session() as session:
            session.query(UserAnimal).filter(UserAnimal.animal_id == animal_id).update({"modifier_id": modifier_id})
            session.commit()
            return True
    except Exception as e:
        logger.warning(f"Erro ao atualizar o modificador do animal: {e}")
        return False


def remove_animal_modifier(animal_id: int) -> bool:
    """
    Removes a modifier from an animal.

    Args:
        animal_id (int): The ID of the animal to remove the modifier from.

    Returns:
        bool: True if the removal was successful, False if an error occurred.
    """
    try:
        with context.db.session() as session:
            session.query(UserAnimal).filter(UserAnimal.animal_id == animal_id).update({"modifier_id": None})
            session.commit()
            return True
    except Exception as e:
        logger.warning(f"Erro ao remover o modificador do animal: {e}")
        return False


def calculate_animal_stats_with_modifier(user_animal: UserAnimalEntity) -> dict:
    """
    Calculates the actual stats of an animal considering its modifier effects.

    Args:
        user_animal (UserAnimalEntity): The user animal entity with modifier information.

    Returns:
        dict: A dictionary containing the calculated stats.
    """

    # Get base values from the animal type
    base_feeding_cost = 2  # Default feeding cost is 2 coins
    base_burial_cost = 1  # Default burial cost is 1 coin
    base_hunger_rate = 24 if not user_animal.animal_type else user_animal.animal_type.hunger_rate
    base_lifespan = 14 if not user_animal.animal_type else user_animal.animal_type.lifespan
    base_reward = 0 if not user_animal.animal_type else user_animal.animal_type.base_reward
    base_expire_value = (
        0 if not user_animal.animal_type else round(user_animal.animal_type.base_price * 0.25)
    )  # 25% of purchase price
    base_found_coin_percentage = 0.05  # Default 5% chance to find coins

    # Apply modifier effects if the animal has a modifier
    if hasattr(user_animal, "modifier") and user_animal.modifier:
        modifier = user_animal.modifier
        feeding_cost = max(1, round(base_feeding_cost * modifier.feeding_cost_multiplier))
        burial_cost = max(0, round(base_burial_cost * modifier.burial_cost_multiplier))
        hunger_rate = round(base_hunger_rate * modifier.hunger_rate_multiplier)
        lifespan = max(1, round(base_lifespan * modifier.lifespan_multiplier))
        reward = max(0, round(base_reward * modifier.reward_multiplier))
        expire_value = max(0, round(base_expire_value * modifier.expire_multiplier))
        found_coin_percentage = modifier.found_coin_percentage
    else:
        feeding_cost = int(base_feeding_cost)
        burial_cost = int(base_burial_cost)
        hunger_rate = int(base_hunger_rate)
        lifespan = int(base_lifespan)
        reward = int(base_reward)
        expire_value = int(base_expire_value)
        found_coin_percentage = base_found_coin_percentage

    return {
        "feeding_cost": feeding_cost,
        "burial_cost": burial_cost,
        "hunger_rate": hunger_rate,
        "lifespan": lifespan,
        "reward": reward,
        "expire_value": expire_value,
        "found_coin_percentage": found_coin_percentage,
    }
