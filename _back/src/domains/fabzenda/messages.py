FABZENDA_OPTIONS = """
# Menu da Fabzendinha 🌱
: Selecione uma das opções abaixo
.
 <🏕️ Minha Fabzenda(fabzenda)[opt=ver]P>
 <🌾 Celeiro Canto Bão(fabzenda)[opt=celeiro,page=1]>
 <🏪 Oinc Store(fabzenda)[opt=store]>
.
"""

FABZENDA_PAGINADOR_ANTERIOR = """
<⬅️ Página Anterior(fabzenda)[opt={command},page={page}]P>
"""

FABZENDA_PAGINADOR_PROXIMO = """
<Próxima Página ➡️(fabzenda)[opt={command},page={page}]P>
"""

####
FAZENDA_OVERVIEW_VAZIA = """
{apelido}, sua Fabzenda está vazia! :seedling:
: Que tal adotar um fabichinho para cuidar?
.
<🌾 Celeiro Canto Bão(fabzenda)[opt=celeiro]P>
"""

FAZENDA_OVERVIEW = """
{apelido}, aqui está sua Fabzenda! Você tem `{num_animals}` fabichinhos (Max: {total_animals}).
> {slots}
{animals}
"""

FAZENDA_OVERVIEW_ANIMALS = """
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

FAZENDA_OVERVIEW_ANIMALS_DETAIL = """

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
###

FAZENDA_OVERVIEW_ANIMAL_HEALTH_4 = """
: _Seu fabichinho está muito bem! Continue cuidando dele._
"""

FAZENDA_OVERVIEW_ANIMAL_HEALTH_3 = """
: _Seu fabichinho está com fome! Alimente-o para que ele fique saudável. Nesse estado, em caso de sorteio, você ganha 75% do prêmio._
"""

FAZENDA_OVERVIEW_ANIMAL_HEALTH_2 = """
: _Seu fabichinho está desnutrito! Alimente-o para que ele fique saudável. Nesse estado, em caso de sorteio, você ganha 50% do prêmio._
"""

FAZENDA_OVERVIEW_ANIMAL_HEALTH_1 = """
: _Seu fabichinho está doente! Alimente-o ou ele pode morrer. Nesse estado, em caso de sorteio, você ganha 10% do prêmio._
"""

FAZENDA_OVERVIEW_ANIMAL_DEAD = """
.
--
.
{emoji} {type} *{name}* 
Seu fabichinho está `{health}`
: O céu ganhou mais uma estrela. Você precisa enterrá-lo para liberar o espaço na sua Fabzenda.
<🪦 Enterrar - F₵ {burial_cost}(fabzenda)[opt=enterrar,id={id}]D>
.
"""

FAZENDA_OVERVIEW_ANIMAL_ABDUZIDO = """
.
--
.
{emoji} {type} *{name}* `🛸 Abduzido`
Um ovni levou seu fabichinho! Virou estrela :star: 
: Parabéns pelo cuidado que teve durante esse tempo. Os seres de outro planeta deixaram uma recompensa para você.
<🛸 Receber F₵ {expire_value}(fabzenda)[opt=abduzir,id={id}]P>
"""

###
CELEIRO_OVERVIEW = """
A melhor, maior e único lugar que você pode comprar Fabichinhos para sua Fabzenda!
> Seu saldo: `F₵ {balance}`
--
.
{animals}
.
{paginador}
"""

CELEIRO_OVERVIEW_ANIMALS = """
{emoji} *{name}* `F₵ {price}` || <👀 Detalhes(fabzenda)[opt=detalhe_animal_celeiro,id={id}]>
: {description}
.
--
.
"""

CELEIRO_ANIMAL_DETAIL = """
{emoji} *{name}* `F₵ {price}`
: {description}

> *Fome*: Sente fome a cada `{hunger_rate} horas`
> *Longevidade*: Vive por `{lifespan} dias`
> *Prêmio*: Ao ser sorteada, seu tutor ganha `F₵ {reward}`
.
<🧺 Adotar(fabzenda)[opt=comprar_animal,id={id}]P> <🌾 Voltar para Celeiro(fabzenda)[opt=celeiro]>
"""

CELEIRO_ANIMAL_DETAIL_MAX_REACHED = """
{apelido}, não foi possível adotar o Fabichinho. Parece que sua Fabzenda está cheia.
: Não queremos que seus fabichinhos fiquem apertados, não é mesmo?
"""

CELEIRO_ANIMAL_DETAIL_INSUFFICIENT_BALANCE = """
{apelido}, não foi possível adotar o Fabichinho. Parece que você não tem saldo suficiente.
: Para verificar seu saldo, utilize o comando `!fb` `saldo`
"""

CELEIRO_ANIMAL_DETAIL_NOT_AVAILABLE = """
{apelido}, não foi possível adotar o Fabichinho. Ele não está disponível para adoção.
: Para verificar os fabichinhos disponíveis, visite o Celeiro
"""

CELEIRO_ANIMAL_DETAIL_TRANSACTION_ERROR = """
{apelido}, não foi possível adotar o Fabichinho. Algo deu errado na hora do pagamento.
: Para verificar seu saldo, utilize o comando `!fb` `saldo`
"""

CELEIRO_ANIMAL_DETAIL_CREATED_ERROR = """
{apelido}, não foi possível adotar o Fabichinho. Algo deu errado na hora de adota-lo.
: Tente novamente e, caso não funcione, entre em contato com o Fabs
"""

CELEIRO_ANIMAL_DETAIL_WALLET_NOT_FOUND = """
Não consegui encontrar sua Wallet. Você precisa ter uma Wallet no FabBank para usar a Fabzenda.
: Para criar uma Wallet, fale com o Fabs.
"""

CELEIRO_ANIMAL_DETAIL_BUY_SUCCESS = """
{apelido}, você adotou um fabichinho!
{emoji} `{nome}` ficará muito feliz em sua Fabzenda.
.
{modifier}
"""
###

STORE_OVERVIEW = """
A melhor, maior e único lugar que você pode comprar itens para sua Fabzenda e Fabichinhos!
> Seu saldo: `F₵ {balance}`
{items}
.
{paginador}
"""

STORE_OVERVIEW_ITEM = """
.
--
.
{emoji} *{name}* `F₵ {price}` || <👀 Detalhes(fabzenda)[opt=detalhe_item_store,id={id}]>
: {description}
"""

STORE_WALLET_NOT_FOUND = """
Não consegui encontrar sua Wallet. Você precisa ter uma Wallet no FabBank para usar a Fabzenda.
: Para criar uma Wallet, fale com o Fabs.
"""

STORE_ITEM_DETAIL = """
{emoji} *{name}* `F₵ {price}`
: {description}

> O que esse item faz?
{effect_str}
.
<💳 Comprar(fabzenda)[opt=comprar_item,id={id}]P> <🏪 Voltar para Store(fabzenda)[opt=store]>
"""

STORE_BUY_SUCCESS = """
{apelido}, você comprou um item para sua Fabzenda!
`{emoji} {nome}` foi adicionado ao seu inventário e já está surtindo efeito.
"""

STORE_INSUFFICIENT_BALANCE = """
{apelido}, não foi possível comprar o Item. Parece que você não tem saldo suficiente.
: Para verificar seu saldo, utilize o comando `!fb` `saldo`
"""

STORE_ITEM_NOT_AVAILABLE = """
{apelido}, não foi possível comprar o Item. Ele não está mais disponível para compra.
: Para verificar os itens disponíveis, visite a Oinc Store
"""

STORE_TRANSACTION_ERROR = """
{apelido}, não foi possível comprar o item. Algo deu errado na hora do pagamento.
: Para verificar seu saldo, utilize o comando `!fb` `saldo`
"""

STORE_BUY_ERROR = """
{apelido}, não foi possível comprar o Item. Algo deu errado.
: Tente novamente e, caso não funcione, entre em contato com o Fabs
"""


###
FEED_INSUFFICIENT_BALANCE = """
{apelido}, não foi possível alimentar o Fabichinho. Parece que você não tem saldo suficiente.
: Para verificar seu saldo, utilize o comando `!fb` `saldo`
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
"""

FEED_ANIMAL_DEAD = """
{apelido}, não foi possível alimentar o Fabichinho. Ele já está morto.
: Para adotar um novo fabichinho, visite o Celeiro
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
"""

FEED_TRANSACTION_ERROR = """
{apelido}, não foi possível alimentar o Fabichinho. Algo deu errado na hora do pagamento.
: Para verificar seu saldo, utilize o comando `!fb` `saldo`
"""

FEED_ERROR = """
{apelido}, não foi possível alimentar o Fabichinho. Algo deu errado.
: Tente novamente e, caso não funcione, entre em contato com o Fabs
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
"""

FEED_SUCCESS = """
{apelido}, você alimentou o seu Fabichinho com sucesso!
: Ele está muito feliz e agradece a comida.
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
"""


###

BURIAL_INSUFFICIENT_BALANCE = """
{apelido}, não foi possível enterrar o Fabichinho. Parece que você não tem saldo suficiente.
: Para verificar seu saldo, utilize o comando `!fb` `saldo`
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
"""

BURIAL_ANIMAL_LIVES = """
{apelido}, não foi possível enterrar o Fabichinho. Ele parece estar vivo
: De alguma forma...
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
"""

BURIAL_TRANSACTION_ERROR = """
{apelido}, não foi possível enterrar o Fabichinho. Algo deu errado na hora do pagamento.
: Para verificar seu saldo, utilize o comando `!fb` `saldo`
"""

BURIAL_ERROR = """
{apelido}, não foi possível enterrar o Fabichinho. Algo deu errado.
: Tente novamente e, caso não funcione, entre em contato com o Fabs
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
"""

BURIAL_SUCCESS = """
{apelido}, você enterrou o seu Fabichinho!
: Rest In Peace, little buddy.
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
"""

###

ABDUCTION_ANIMAL_LIVES = """
{apelido}, não foi possível receber a recompensa da abdução. Fabichinho ainda não foi abduzido.
: Para ver seus fabichinhos, vá até sua Fabzenda
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
"""

ABDUCTION_TRANSACTION_ERROR = """
{apelido}, não foi possível receber a recompensa da abdução. Algo deu errado na hora do pagamento.
: Tente novamente e, caso não funcione, entre em contato com o Fabs
"""

ABDUCTION_ERROR = """
{apelido}, não foi possível receber a recompensa da abdução. Algo deu errado.
: Tente novamente e, caso não funcione, entre em contato com o Fabs
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
"""

ABDUCTION_SUCCESS = """
{apelido}, você recebeu a recompensa por ter um fabichinho abduzido!
: Agradeça aos seres de outro planeta 👽.
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=ver]P>
"""

#
###

TEMPLATE_FABZENDA_FOUND_COIN = """
# Hey, encontrei algo [{emoji}]
{apelido}, seu fabichinho *{name}* estava tão feliz que encontrou fabcoins no chão! :moneybag:
> Acabei de adicionar `F₵ {coin_value}` na sua Wallet.
"""

TEMPLATE_FABZENDA_GENERIC_ERROR = """
Algo deu errado e não consegui atuar na Fabzenda 🫠
: Tente novamente e, se não der certo, entre em contato com o Fabs.
"""

###

NOTIFICATION_ANIMAL_SICK = """
{apelido}, seu fabichinho {emoji} *{name}* está doente! 😵‍💫
: Ele precisa de comida para não morrer. Alimente-o antes que seja tarde demais.
.
<🥘 Alimentar - F₵ {feeding_cost} (fabzenda)[opt=alimentar,id={id}]P> <🏕️ Ver Fabzenda(fabzenda)[opt=ver]>
"""

NOTIFICATION_ANIMAL_DEAD = """
{apelido}, seu fabichinho {emoji} *{name}* morreu! :skull:
: A fome venceu e ele não conseguiu sobreviver. Agora você precisa enterrá-lo
.
<🏕️ Ver Fabzenda(fabzenda)[opt=ver]>
"""

NOTIFICATION_CHANNEL_ANIMAL_DEAD = """
# Jornal Agronews 📰
Atenção, temos uma notícia triste para compartilhar com vocês.
> O fabichinho {emoji} *{name}* do usuário <@{slack_id}> faleceu. :skull:
: Resistiu bravamente, mas não conseguiu sobreviver à fome
"""

NOTIFICATION_CHANNEL_LOTERY = """
# Jornal Agronews 📰
<!channel> Foi divulgado o resultado do Jogo dos Fabichinhos 🎰
.
> O resultado foi: {result}
.
Tivemos {n_ganhadores}, recebendo um total de `F₵ {total_reward}` em prêmios.
{ganhadores}
: O Jogo dos Fabichinhos é um jogo de sorte, totalmente aleatório, auditado pela Caixa Econômica Faberal.
"""

NOTIFICATION_CHANNEL_LOTERY_NONE = """
# Jornal Agronews 📰
<!channel> Foi divulgado o resultado do Jogo dos Fabichinhos 🎰
.
> O resultado foi: {result}
.
Não tivemos ganhadores nesse sorteio 🥲
: Mas não desanime, o próximo pode ser o seu! O Jogo dos Fabichinhos é um jogo de sorte, totalmente aleatório, auditado pela Caixa Econômica Faberal.
"""

NOTIFICATION_LOTERY = """
# Resultado - Jogo dos Fabichinhos 🎰
{apelido}, parabéns! Você ganhou `F₵ {reward}` no sorteio com {result}!
{bonus}
"""
