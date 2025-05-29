# interfaces/presenters/slack/message_presenters/fabbank_message_presenter.py


from datetime import datetime

from domains.fabzenda.entities.animal_modifier import AnimalModifierEntity
from domains.fabzenda.entities.animal_type import AnimalTypeEntity
from domains.fabzenda.entities.item_definition import ItemDefinitionEntity
from domains.fabzenda.entities.user_animal import UserAnimalEntity
from domains.user.entities.user import UserEntity

from ..base_presenter import BaseSlackPresenter


class FabzendaMessagePresenter(BaseSlackPresenter):
    ## Messages
    _GENERIC_ERROR = """
    Algo deu errado na minha comunicação com a Fabzenda :warning:
    : Tente novamente mais tarde ou entre em contato com o Fabs
    """

    _OPTIONS = """
    # Menu da Fabzendinha 🌱
    : Selecione uma das opções abaixo
    .
    <🏕️ Minha Fabzenda(fabzenda)[opt=ver]P>
    <🌾 Celeiro Canto Bão(fabzenda)[opt=celeiro,page=1]>
    <🏪 Oinc Store(fabzenda)[opt=store]>
    .
    """

    _PAGINADOR_ANTERIOR = """
    <⬅️ Página Anterior(fabzenda)[opt={command},page={page}]P>
    """

    _PAGINADOR_PROXIMO = """
    <Próxima Página ➡️(fabzenda)[opt={command},page={page}]P>
    """

    _OVERVIEW_VAZIA = """
    {apelido}, sua Fabzenda está vazia! :seedling:
    : Que tal adotar um fabichinho para cuidar?
    .
    <🌾 Celeiro Canto Bão(fabzenda)[opt=celeiro]P>
    """

    _OVERVIEW = """
    {apelido}, aqui está sua Fabzenda! Você tem `{num_animals}` fabichinhos (Max: {total_animals}).
    > {slots}
    {animals}
    """

    _OVERVIEW_ANIMALS = """
    .
    --
    .
    {emoji} {type} *{name}* `🎰 F₵ {reward}` `🛸 F₵ {expire_value}`
    : Seu fabichinho está lorem ipsum dolor sit amet, consectetur adipiscing elit.
    .
    ↳ *Saúde*: `{health}`
    ↳ *Fome*: {hunger}
    ↳ *Idade*: `{age}`
    ↳ *Modificador*: `{modifier}`
    .
    <👁️ Detalhe do Fabichinho (fabzenda)[opt=detalhe_animal_fabzenda,id={id}]P> <🥘 Alimentar - F₵ {feeding_cost} (fabzenda)[opt=alimentar,id={id}]{primary}>
    .
    """

    _OVERVIEW_ANIMALS_DETAIL = """

    {emoji} {type} *{name}* `🎰 F₵ {reward}` `🛸 F₵ {expire_value}`
    _Seu fabichinho está lorem ipsum dolor sit amet, consectetur adipiscing elit_
    .
    > *Saúde*: `{health}`
    {health_description}
    .
    > *Fome*: {hunger}
    : _Seu fabichinho sente fome a cada_ *{hunger_rate} horas*
    .
    > *Idade*: `{age}`
    : _Seu fabichinho vive por_ *{lifespan} dias*
    .
    > *Modificador*: `{modifier}`
    : _{modifier_description}_
    .
    <🥘 Alimentar - F₵ {feeding_cost} (fabzenda)[opt=alimentar,id={id}]{primary}> <🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]>
    .
    """

    _OVERVIEW_ANIMAL_HEALTH_4 = """
    : _Seu fabichinho está muito bem! Continue cuidando dele._
    """

    _OVERVIEW_ANIMAL_HEALTH_3 = """
    : _Seu fabichinho está com fome! Alimente-o para que ele fique saudável. Nesse estado, em caso de sorteio, você ganha 75% do prêmio._
    """

    _OVERVIEW_ANIMAL_HEALTH_2 = """
    : _Seu fabichinho está desnutrito! Alimente-o para que ele fique saudável. Nesse estado, em caso de sorteio, você ganha 50% do prêmio._
    """

    _OVERVIEW_ANIMAL_HEALTH_1 = """
    : _Seu fabichinho está doente! Alimente-o ou ele pode morrer. Nesse estado, em caso de sorteio, você ganha 10% do prêmio._
    """

    _OVERVIEW_ANIMAL_DEAD = """
    .
    --
    .
    {emoji} {type} *{name}* 
    Seu fabichinho está `{health}`
    : O céu ganhou mais uma estrela. Você precisa enterrá-lo para liberar o espaço na sua Fabzenda.
    <🪦 Enterrar - F₵ {burial_cost}(fabzenda)[opt=enterrar,id={id}]D>
    .
    """

    _OVERVIEW_ANIMAL_ABDUZIDO = """
    .
    --
    .
    {emoji} {type} *{name}* `🛸 Abduzido`
    Um ovni levou seu fabichinho! Virou estrela :star: 
    : Parabéns pelo cuidado que teve durante esse tempo. Os seres de outro planeta deixaram uma recompensa para você.
    <🛸 Receber F₵ {expire_value}(fabzenda)[opt=abduzir,id={id}]P>
    """

    _FEED_INSUFFICIENT_BALANCE = """
    {apelido}, não foi possível alimentar o Fabichinho. Parece que você não tem saldo suficiente.
    : Para verificar seu saldo, utilize o comando `!fb` `saldo`
    .
    <🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
    """

    _FEED_ANIMAL_DEAD = """
    {apelido}, não foi possível alimentar o Fabichinho. Ele já está morto.
    : Para adotar um novo fabichinho, visite o Celeiro
    .
    <🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
    """

    _FEED_TRANSACTION_ERROR = """
    {apelido}, não foi possível alimentar o Fabichinho. Algo deu errado na hora do pagamento.
    : Para verificar seu saldo, utilize o comando `!fb` `saldo`
    """

    _FEED_ERROR = """
    {apelido}, não foi possível alimentar o Fabichinho. Algo deu errado.
    : Tente novamente e, caso não funcione, entre em contato com o Fabs
    .
    <🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
    """

    _FEED_SUCCESS = """
    {apelido}, você alimentou o seu Fabichinho com sucesso!
    : Ele está muito feliz e agradece a comida.
    .
    <🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
    """

    _ABDUCTION_ANIMAL_LIVES = """
    {apelido}, não foi possível receber a recompensa da abdução. Fabichinho ainda não foi abduzido.
    : Para ver seus fabichinhos, vá até sua Fabzenda
    .
    <🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
    """

    _ABDUCTION_TRANSACTION_ERROR = """
    {apelido}, não foi possível receber a recompensa da abdução. Algo deu errado na hora do pagamento.
    : Tente novamente e, caso não funcione, entre em contato com o Fabs
    """

    _ABDUCTION_ERROR = """
    {apelido}, não foi possível receber a recompensa da abdução. Algo deu errado.
    : Tente novamente e, caso não funcione, entre em contato com o Fabs
    .
    <🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
    """

    _ABDUCTION_SUCCESS = """
    {apelido}, você recebeu a recompensa por ter um fabichinho abduzido!
    : Agradeça aos seres de outro planeta 👽.
    .
    <🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
    """

    _BURIAL_INSUFFICIENT_BALANCE = """
    {apelido}, não foi possível enterrar o Fabichinho. Parece que você não tem saldo suficiente.
    : Para verificar seu saldo, utilize o comando `!fb` `saldo`
    .
    <🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
    """

    _BURIAL_ANIMAL_LIVES = """
    {apelido}, não foi possível enterrar o Fabichinho. Ele parece estar vivo
    : De alguma forma...
    .
    <🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
    """

    _BURIAL_TRANSACTION_ERROR = """
    {apelido}, não foi possível enterrar o Fabichinho. Algo deu errado na hora do pagamento.
    : Para verificar seu saldo, utilize o comando `!fb` `saldo`
    """

    _BURIAL_ERROR = """
    {apelido}, não foi possível enterrar o Fabichinho. Algo deu errado.
    : Tente novamente e, caso não funcione, entre em contato com o Fabs
    .
    <🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
    """

    _BURIAL_SUCCESS = """
    {apelido}, você enterrou o seu Fabichinho!
    : Rest In Peace, little buddy.
    .
    <🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
    """

    _CELEIRO_OVERVIEW = """
    A melhor, maior e único lugar que você pode comprar Fabichinhos para sua Fabzenda!
    > Seu saldo: `F₵ {balance}`
    --
    .
    {animals}
    .
    {paginador}
    """

    _CELEIRO_OVERVIEW_ANIMALS = """
    {emoji} *{name}* `F₵ {price}` || <👀 Detalhes(fabzenda)[opt=detalhe_animal_celeiro,id={id}]>
    : {description}
    .
    --
    .
    """

    _CELEIRO_ANIMAL_DETAIL = """
    {emoji} *{name}* `F₵ {price}`
    : {description}

    > *Fome*: Sente fome a cada `{hunger_rate} horas`
    > *Longevidade*: Vive por `{lifespan} dias`
    > *Prêmio*: Ao ser sorteada, seu tutor ganha `F₵ {reward}`
    .
    <🧺 Adotar(fabzenda)[opt=comprar_animal,id={id}]P> <🌾 Voltar para Celeiro(fabzenda)[opt=celeiro]>
    """

    _CELEIRO_ANIMAL_DETAIL_MAX_REACHED = """
    {apelido}, não foi possível adotar o Fabichinho. Parece que sua Fabzenda está cheia.
    : Não queremos que seus fabichinhos fiquem apertados, não é mesmo?
    """

    _CELEIRO_ANIMAL_DETAIL_INSUFFICIENT_BALANCE = """
    {apelido}, não foi possível adotar o Fabichinho. Parece que você não tem saldo suficiente.
    : Para verificar seu saldo, utilize o comando `!fb` `saldo`
    """

    _CELEIRO_ANIMAL_DETAIL_NOT_AVAILABLE = """
    {apelido}, não foi possível adotar o Fabichinho. Ele não está disponível para adoção.
    : Para verificar os fabichinhos disponíveis, visite o Celeiro
    """

    _CELEIRO_ANIMAL_DETAIL_TRANSACTION_ERROR = """
    {apelido}, não foi possível adotar o Fabichinho. Algo deu errado na hora do pagamento.
    : Para verificar seu saldo, utilize o comando `!fb` `saldo`
    """

    _CELEIRO_ANIMAL_DETAIL_CREATED_ERROR = """
    {apelido}, não foi possível adotar o Fabichinho. Algo deu errado na hora de adota-lo.
    : Tente novamente e, caso não funcione, entre em contato com o Fabs
    """

    _CELEIRO_ANIMAL_DETAIL_WALLET_NOT_FOUND = """
    Não consegui encontrar sua Wallet. Você precisa ter uma Wallet no FabBank para usar a Fabzenda.
    : Para criar uma Wallet, fale com o Fabs.
    """

    _CELEIRO_ANIMAL_DETAIL_BUY_SUCCESS = """
    {apelido}, você adotou um fabichinho!
    {emoji} `{nome}` ficará muito feliz em sua Fabzenda.
    .
    {modifier}
    """

    _STORE_OVERVIEW = """
    A melhor, maior e único lugar que você pode comprar itens para sua Fabzenda e Fabichinhos!
    > Seu saldo: `F₵ {balance}`
    {items}
    .
    {paginador}
    """

    _STORE_OVERVIEW_ITEM = """
    .
    --
    .
    {emoji} *{name}* `F₵ {price}` || <👀 Detalhes(fabzenda)[opt=detalhe_item_store,id={id}]>
    : {description}
    """

    _STORE_WALLET_NOT_FOUND = """
    Não consegui encontrar sua Wallet. Você precisa ter uma Wallet no FabBank para usar a Fabzenda.
    : Para criar uma Wallet, fale com o Fabs.
    """

    _STORE_ITEM_DETAIL = """
    {emoji} *{name}* `F₵ {price}`
    : {description}

    > O que esse item faz?
    {effect_str}
    SELECT<Fabichinho(user_animal_id)[{user_animal_list}]>
    .
    <💳 Comprar(fabzenda)[opt=comprar_item,id={id}]P> <🏪 Voltar para Store(fabzenda)[opt=store]>
    """

    # Selecione o fabichinho que receberá esse item
    # SELECT<Fabichinho(manage_action)[Editar=edit_value,Ler=read_value,Salvar=save_value]>
    # <💳 Comprar(fabzenda)[opt=comprar_item,id={id}]P>

    _STORE_BUY_SUCCESS = """
    {apelido}, você comprou um item para sua Fabzenda!
    `{emoji} {nome}` foi adicionado ao seu inventário e já está surtindo efeito.
    """

    _STORE_INSUFFICIENT_BALANCE = """
    {apelido}, não foi possível comprar o Item. Parece que você não tem saldo suficiente.
    : Para verificar seu saldo, utilize o comando `!fb` `saldo`
    """

    _STORE_ITEM_NOT_AVAILABLE = """
    {apelido}, não foi possível comprar o Item. Ele não está mais disponível para compra.
    : Para verificar os itens disponíveis, visite a Oinc Store
    """

    _STORE_TRANSACTION_ERROR = """
    {apelido}, não foi possível comprar o item. Algo deu errado na hora do pagamento.
    : Para verificar seu saldo, utilize o comando `!fb` `saldo`
    """

    _STORE_BUY_ERROR = """
    {apelido}, não foi possível comprar o Item. Algo deu errado.
    : Tente novamente e, caso não funcione, entre em contato com o Fabs
    """

    ## Success Messages
    def option_fabzenda(self, data: dict):
        return self._say(self._OPTIONS)

    ## Success View
    def overview(self, data: dict):
        user_animals: list[UserAnimalEntity] = data.get("user_animals", [])
        user: UserEntity = data.get("user", None)

        slots_fabzenda = [f"{animal.animal_type.emoji}" for animal in user_animals]

        while len(slots_fabzenda) < (3 + data.get("qtd_additional", 0)):
            slots_fabzenda.append("[⊹]")

        animals_text = ""
        for animal in user_animals:
            # Verificando se o animal está morto
            if animal.health == 0:
                animals_text += self._OVERVIEW_ANIMAL_DEAD.format(
                    emoji=animal.animal_type.emoji,
                    burial_cost=animal.burial_cost,
                    type=animal.animal_type.name,
                    name=animal.name,
                    health=animal.health_str,
                    id=animal.animal_id,
                )
                continue

            # Verificando se o animal foi Abduzido
            if (animal.expiry_date <= datetime.now()) or (animal.health == -1):
                animals_text += self._OVERVIEW_ANIMAL_ABDUZIDO.format(
                    emoji=animal.animal_type.emoji,
                    expire_value=animal.expire_value,
                    type=animal.animal_type.name,
                    name=animal.name,
                    id=animal.animal_id,
                )
                continue

            food_slot_full = " `🍔` " * animal.food_slot
            food_slot_empty = " `‧` " * (4 - animal.food_slot)
            hunger = f"{food_slot_full}{food_slot_empty}"

            age = (datetime.now() - animal.purchase_date).days

            animals_text += self._OVERVIEW_ANIMALS.format(
                emoji=animal.animal_type.emoji,
                type=animal.animal_type.name,
                name=animal.name,
                reward=animal.reward,
                expire_value=animal.expire_value,
                modifier=f"{animal.modifier.name} {animal.modifier.emoji}" if animal.modifier else "Normal 🌱",
                health=animal.health_str,
                hunger=hunger,
                age=f"{age} dias" if age > 1 else f"{age} dia" if age == 1 else "Recém-nascido",
                feeding_cost=animal.feeding_cost,
                id=animal.animal_id,
                primary="P" if (animal.food_slot == 0 or animal.health < 4) else "",
            )

        message_text = self._OVERVIEW.format(
            apelido=user.apelido,
            slots=" ‧ ".join(slots_fabzenda),
            animals=animals_text,
            num_animals=len(user_animals),
            total_animals=(3 + data.get("qtd_additional", 0)),
        )

        self._set_view(
            content=message_text,
            title="Fabzenda 🏕️",
        )

    def overview_detalhe_animal(self, data: dict):
        user_animal: UserAnimalEntity = data.get("user_animal", {})

        food_slot_full = " `🍔` " * user_animal.food_slot
        food_slot_empty = " `‧` " * (4 - user_animal.food_slot)
        hunger = f"{food_slot_full}{food_slot_empty}"

        age = (datetime.now() - user_animal.purchase_date).days

        map_health_description = {
            4: self._OVERVIEW_ANIMAL_HEALTH_4,
            3: self._OVERVIEW_ANIMAL_HEALTH_3,
            2: self._OVERVIEW_ANIMAL_HEALTH_2,
            1: self._OVERVIEW_ANIMAL_HEALTH_1,
        }
        health_description = map_health_description.get(user_animal.health, self._OVERVIEW_ANIMAL_HEALTH_4)

        message_text = self._OVERVIEW_ANIMALS_DETAIL.format(
            emoji=user_animal.animal_type.emoji,
            type=user_animal.animal_type.name,
            name=user_animal.name,
            reward=user_animal.reward,
            expire_value=user_animal.expire_value,
            modifier=f"{user_animal.modifier.name} {user_animal.modifier.emoji}"
            if user_animal.modifier
            else "Normal 🌱",
            modifier_description=user_animal.modifier.resume_modifier
            if user_animal.modifier
            else "Seu fabichinho é normal (mas continua especial)",
            health=user_animal.health_str,
            health_description=health_description,
            hunger=hunger,
            hunger_rate=user_animal.hunger_rate,
            age=f"{age} dias" if age > 1 else f"{age} dia" if age == 1 else "Recém-nascido",
            lifespan=user_animal.lifespan,
            feeding_cost=user_animal.feeding_cost,
            id=user_animal.animal_id,
            primary="P" if (user_animal.food_slot == 0 or user_animal.health < 4) else "",
        )

        self._set_view(
            content=message_text,
            title="Fabzenda 🏕️",
        )

    def alimentar_animal_sucesso(self, data: dict):
        self._set_view(
            content=self._FEED_SUCCESS.format(apelido=data.get("apelido")),
            title="Fabzenda 🏕️",
        )

    def abduzir_animal_sucesso(self, data: dict):
        self._set_view(
            content=self._ABDUCTION_SUCCESS.format(apelido=data.get("apelido")),
            title="Fabzenda 🏕️",
        )

    def enterrar_animal_sucesso(self, data: dict):
        self._set_view(
            content=self._BURIAL_SUCCESS.format(apelido=data.get("apelido")),
            title="Fabzenda 🏕️",
        )

    def celeiro_overview(self, data: dict):
        animal_types: list[AnimalTypeEntity] = data.get("animal_types", [])
        atual_page = data.get("atual_page", 1)

        # Paginação
        per_page = 10
        total_pages = len(animal_types) // per_page + (1 if len(animal_types) % per_page > 0 else 0)
        animal_types_page = animal_types[per_page * (atual_page - 1) : per_page * atual_page]

        animals_text = ""
        for animal in animal_types_page:
            animals_text += self._CELEIRO_OVERVIEW_ANIMALS.format(
                id=animal.type_id,
                name=animal.name,
                emoji=animal.emoji,
                price=animal.base_price,
                description=animal.description,
            )

        paginador = ""
        if atual_page > 1:
            paginador += self._PAGINADOR_ANTERIOR.format(
                command="celeiro",
                page=atual_page - 1,
            )

        if atual_page < total_pages:
            paginador += self._PAGINADOR_PROXIMO.format(
                command="celeiro",
                page=atual_page + 1,
            )

        message_text = self._CELEIRO_OVERVIEW.format(
            balance=data.get("balance", 0),
            animals=animals_text,
            paginador=paginador.replace("\n", ""),
        )

        self._set_view(
            content=message_text,
            title="Celeiro Canto Bão 🌾",
        )

    def celeiro_overview_detalhe_animal(self, data: dict):
        animal_type: AnimalTypeEntity = data.get("animal_type", {})

        message_text = self._CELEIRO_ANIMAL_DETAIL.format(
            id=animal_type.type_id,
            name=animal_type.name,
            emoji=animal_type.emoji,
            price=animal_type.base_price,
            reward=animal_type.base_reward,
            hunger_rate=animal_type.hunger_rate,
            lifespan=animal_type.lifespan,
            description=animal_type.description,
        )

        self._set_view(
            content=message_text,
            title="Celeiro Canto Bão 🌾",
        )

    def celeiro_comprar_animal(self, data: dict):
        user_animal: UserAnimalEntity = data.get("user_animal", None)
        animal_modifier: AnimalModifierEntity = data.get("animal_modifier", None)
        animal_type: AnimalTypeEntity = data.get("animal_type", None)
        user: UserEntity = data.get("user", None)

        modifier_text = ""
        if animal_modifier:
            modifier_text = f"Seu fabichinho é `{animal_modifier.name} {animal_modifier.emoji}`\n"
            modifier_text += f": {animal_modifier.description}"
        else:
            modifier_text = "Seu fabichinho é `Normal 🌱`"
            modifier_text += ": Ele não tem nenhum modificador especial mas é muito especial para você"

        message_text = self._CELEIRO_ANIMAL_DETAIL_BUY_SUCCESS.format(
            apelido=user.apelido, emoji=animal_type.emoji, nome=user_animal.name, modifier=modifier_text
        )

        self._set_view(
            content=message_text,
            title="Celeiro Canto Bão 🌾",
        )

    def store_overview(self, data: dict):
        items: list[ItemDefinitionEntity] = data.get("items", [])
        atual_page = data.get("atual_page", 1)

        # Paginação
        per_page = 10
        total_pages = len(items) // per_page + (1 if len(items) % per_page > 0 else 0)
        items_page = items[per_page * (atual_page - 1) : per_page * atual_page]

        items_text = ""
        for item in items_page:
            items_text += self._STORE_OVERVIEW_ITEM.format(
                id=item.item_id,
                name=item.name,
                emoji=item.emoji,
                price=item.price,
                description=item.description,
            )

        paginador = ""
        if atual_page > 1:
            paginador += self._PAGINADOR_ANTERIOR.format(
                command="store",
                page=atual_page - 1,
            )

        if atual_page < total_pages:
            paginador += self._PAGINADOR_PROXIMO.format(
                command="store",
                page=atual_page + 1,
            )

        message_text = self._STORE_OVERVIEW.format(
            balance=data.get("balance", 0),
            items=items_text,
            paginador=paginador.replace("\n", ""),
        )

        self._set_view(
            content=message_text,
            title="Oinc Store 🏪",
        )

    def store_detalhe_item(self, data: dict):
        item: ItemDefinitionEntity = data.get("item", {})
        user_animal_list = data.get("user_animal_list", [])

        options_user_animals = [
            f"{animal.animal_type.emoji} {animal.name}={animal.animal_id}" for animal in user_animal_list
        ]
        user_animal_list_str = ",".join(options_user_animals)

        self._set_view(
            content=self._STORE_ITEM_DETAIL.format(
                id=item.item_id,
                name=item.name,
                emoji=item.emoji,
                price=item.price,
                description=item.description,
                effect_str=item.effect_str,
                user_animal_list=user_animal_list_str,
            ),
            title="Oinc Store 🏪",
        )

    def store_comprar_item(self, data: dict):
        item: ItemDefinitionEntity = data.get("item_definition", None)
        apelido = data.get("apelido", None)

        message_text = self._STORE_BUY_SUCCESS.format(apelido=apelido, emoji=item.emoji, nome=item.name)

        self._set_view(
            content=message_text,
            title="Oinc Store 🏪",
        )

    ## Error Messages
    def error_generic(self, data: dict):
        return self._set_view(
            content=self._GENERIC_ERROR,
            title="Fabzenda 🏕️",
        )

    def error_overview_vazia(self, data: dict):
        return self._set_view(self._OVERVIEW_VAZIA.format(apelido=data.get("apelido")), "Fabzenda 🏕️")

    def error_feed_insufficient_balance(self, data: dict):
        return self._set_view(
            content=self._FEED_INSUFFICIENT_BALANCE.format(apelido=data.get("apelido")),
            title="Fabzenda 🏕️",
        )

    def error_feed_animal_dead(self, data: dict):
        return self._set_view(
            content=self._FEED_ANIMAL_DEAD.format(apelido=data.get("apelido")),
            title="Fabzenda 🏕️",
        )

    def error_feed_transaction_error(self, data: dict):
        return self._set_view(
            content=self._FEED_TRANSACTION_ERROR.format(apelido=data.get("apelido")),
            title="Fabzenda 🏕️",
        )

    def error_feed_error(self, data: dict):
        return self._set_view(
            content=self._FEED_ERROR.format(apelido=data.get("apelido")),
            title="Fabzenda 🏕️",
        )

    def error_abduction_animal_lives(self, data: dict):
        return self._set_view(
            content=self._ABDUCTION_ANIMAL_LIVES.format(apelido=data.get("apelido")),
            title="Fabzenda 🏕️",
        )

    def error_abduction_transaction_error(self, data: dict):
        return self._set_view(
            content=self._ABDUCTION_TRANSACTION_ERROR.format(apelido=data.get("apelido")),
            title="Fabzenda 🏕️",
        )

    def error_abduction_error(self, data: dict):
        return self._set_view(
            content=self._ABDUCTION_ERROR.format(apelido=data.get("apelido")),
            title="Fabzenda 🏕️",
        )

    def error_burial_insufficient_balance(self, data: dict):
        return self._set_view(
            content=self._BURIAL_INSUFFICIENT_BALANCE.format(apelido=data.get("apelido")),
            title="Fabzenda 🏕️",
        )

    def error_burial_animal_lives(self, data: dict):
        return self._set_view(
            content=self._BURIAL_ANIMAL_LIVES.format(apelido=data.get("apelido")),
            title="Fabzenda 🏕️",
        )

    def error_burial_transaction_error(self, data: dict):
        return self._set_view(
            content=self._BURIAL_TRANSACTION_ERROR.format(apelido=data.get("apelido")),
            title="Fabzenda 🏕️",
        )

    def error_burial_error(self, data: dict):
        return self._set_view(
            content=self._BURIAL_ERROR.format(apelido=data.get("apelido")),
            title="Fabzenda 🏕️",
        )

    def error_celeiro_max_reached(self, data: dict):
        return self._set_view(
            content=self._CELEIRO_ANIMAL_DETAIL_MAX_REACHED.format(apelido=data.get("apelido")),
            title="Celeiro Canto Bão 🌾",
        )

    def error_celeiro_insufficient_balance(self, data: dict):
        return self._set_view(
            content=self._CELEIRO_ANIMAL_DETAIL_INSUFFICIENT_BALANCE.format(apelido=data.get("apelido")),
            title="Celeiro Canto Bão 🌾",
        )

    def error_celeiro_not_available(self, data: dict):
        return self._set_view(
            content=self._CELEIRO_ANIMAL_DETAIL_NOT_AVAILABLE.format(apelido=data.get("apelido")),
            title="Celeiro Canto Bão 🌾",
        )

    def error_celeiro_transaction_error(self, data: dict):
        return self._set_view(
            content=self._CELEIRO_ANIMAL_DETAIL_TRANSACTION_ERROR.format(apelido=data.get("apelido")),
            title="Celeiro Canto Bão 🌾",
        )

    def error_celeiro_created_error(self, data: dict):
        return self._set_view(
            content=self._CELEIRO_ANIMAL_DETAIL_CREATED_ERROR.format(apelido=data.get("apelido")),
            title="Celeiro Canto Bão 🌾",
        )

    def error_celeiro_wallet_not_found(self, data: dict):
        return self._set_view(
            content=self._CELEIRO_ANIMAL_DETAIL_WALLET_NOT_FOUND,
            title="Celeiro Canto Bão 🌾",
        )

    def error_store_wallet_not_found(self, data: dict):
        return self._set_view(
            content=self._STORE_WALLET_NOT_FOUND,
            title="Oinc Store 🏪",
        )

    def error_store_insufficient_balance(self, data: dict):
        return self._set_view(
            content=self._STORE_INSUFFICIENT_BALANCE.format(apelido=data.get("apelido")),
            title="Oinc Store 🏪",
        )

    def error_store_item_not_available(self, data: dict):
        return self._set_view(
            content=self._STORE_ITEM_NOT_AVAILABLE.format(apelido=data.get("apelido")),
            title="Oinc Store 🏪",
        )

    def error_store_transaction_error(self, data: dict):
        return self._set_view(
            content=self._STORE_TRANSACTION_ERROR.format(apelido=data.get("apelido")),
            title="Oinc Store 🏪",
        )

    def error_store_buy_error(self, data: dict):
        return self._set_view(
            content=self._STORE_BUY_ERROR.format(apelido=data.get("apelido")),
            title="Oinc Store 🏪",
        )
