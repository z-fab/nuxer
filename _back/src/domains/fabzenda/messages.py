TEMPLATE_FABZENDA_OPTIONS = """
# Fabzendinha 🌱
{saudacao}! O que gostaria de fazer hoje?
.
--
.
Veja seus fabichinhos na sua Fabzenda || <🏕️ Ver Fabzenda(fabzenda)[opt=btn_ver_fabzenda]P>
.
--
.
Adote um novo fabichinho || <🌾 Celeiro Canto Bão(fabzenda)[opt=btn_celeiro]>
.
--
"""

TEMPLATE_FABZENDA_FAZENDA_VAZIA = """
{apelido}, sua Fabzenda está vazio! :seedling:
: Que tal adotar um fabichinho para cuidar?
.
<🌾 Celeiro Canto Bão(fabzenda)[opt=btn_celeiro]P>
"""

TEMPLATE_FABZENDA_FAZENDA = """
{apelido}, aqui está sua Fabzenda!
> {slots}
{animals}
"""

TEMPLATE_FABZENDA_FAZENDA_ANIMAL = """
.
--
.
{emoji} {type} *{name}* `🎰 F₵ {reward}` `🛸 F₵ {expire_value}`
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

<🥘 Alimentar - F₵ {feeding_cost} (fabzenda)[opt=btn_alimentar,id={id}]{primary}>
.
"""

TEMPLATE_FABZENDA_FAZENDA_ANIMAL_HEALTH_4 = """
: _Seu fabichinho está muito bem! Continue cuidando dele._
"""

TEMPLATE_FABZENDA_FAZENDA_ANIMAL_HEALTH_3 = """
: _Seu fabichinho está com fome! Alimente-o para que ele fique saudável. Nesse estado, em caso de sorteio, você ganha 75% do prêmio._
"""

TEMPLATE_FABZENDA_FAZENDA_ANIMAL_HEALTH_2 = """
: _Seu fabichinho está desnutrito! Alimente-o para que ele fique saudável. Nesse estado, em caso de sorteio, você ganha 50% do prêmio._
"""

TEMPLATE_FABZENDA_FAZENDA_ANIMAL_HEALTH_1 = """
: _Seu fabichinho está doente! Alimente-o ou ele pode morrer. Nesse estado, em caso de sorteio, você ganha 10% do prêmio._
"""

TEMPLATE_FABZENDA_FAZENDA_ANIMAL_MORTO = """
.
--
.
{emoji} {type} *{name}* 
Seu fabichinho está `{health}`
: O céu ganhou mais uma estrela. Você precisa enterrá-lo para liberar o espaço na sua Fabzenda.
<🪦 Enterrar - F₵ {burial_cost}(fabzenda)[opt=btn_enterrar,id={id}]D>
.
"""

TEMPLATE_FABZENDA_FAZENDA_ANIMAL_EXPIRADO = """
.
--
.
{emoji} {type} *{name}* `🛸 Abduzido`
Um ovni levou seu fabichinho! Virou estrela :star: 
: Parabéns pelo cuidado que teve durante esse tempo. Os seres de outro planeta deixaram uma recompensa para você.
<🛸 Receber F₵ {expire_value}(fabzenda)[opt=btn_expirar,id={id}]P>
"""

TEMPLATE_FABZENDA_CELEIRO = """
A melhor, maior e único lugar que você pode comprar Fabichinhos para sua Fabzenda!
> Seu saldo: `F₵ {balance}`
--
.
{animals}
"""

TEMPLATE_FABZENDA_CELEIRO_ANIMAL = """
{emoji} *{name}* `F₵ {price}` || <👀 Detalhes(fabzenda)[opt=btn_detalhes,id={id}]>
: {description}
.
--
.
"""

TEMPLATE_FABZENDA_CELEIRO_ANIMAL_DETALHE = """
{emoji} *{name}* `F₵ {price}`
: {description}

> *Fome*: Sente fome a cada `{hunger_rate} horas`
> *Longevidade*: Vive por `{lifespan} dias`
> *Prêmio*: Ao ser sorteada, seu tutor ganha `F₵ {reward}`
.
<🧺 Adotar(fabzenda)[opt=btn_comprar,id={id}]P> <🌾 Voltar para Celeiro(fabzenda)[opt=btn_celeiro]>
"""

TEMPLATE_FABZENDA_CELEIRO_ANIMAL_COMPRADO = """
{apelido}, você adotou um fabichinho!
{emoji} `{nome}` ficará muito feliz em sua Fabzenda.
.
{modifier}
"""

TEMPLATE_FABZENDA_ANIMAL_COMPRADO_MODIFICADOR = """
--
O seu fabichinho é `{modifier_name}`
: {modifier_description}

{feeding_cost_text}
{burial_cost_text}
{hunger_rate_text}
{expire_value_text}
{reward_text}
{lifespan_text}
{found_coin_text}
"""

TEMPLATE_FABZENDA_CELEIRO_ANIMAL_NAO_COMPRADO = """
{apelido}, não foi possível adotar o Fabichinho. Algo deu errado ou você não tem saldo suficiente.
: Para verificar seu saldo, utilize o comando `!fb` `saldo`
"""

TEMPLATE_FABZENDA_CELEIRO_ANIMAL_ERROR_MAX_ANIMALS = """
{apelido}, não foi possível adotar o Fabichinho. Parece que sua Fabzenda está cheia.
: Não queremos que seus fabichinhos fiquem apertados, não é mesmo?
"""

TEMPLATE_FABZENDA_CELEIRO_ANIMAL_ERROR_INSUFFICIENT_BALANCE = """
{apelido}, não foi possível adotar o Fabichinho. Parece que você não tem saldo suficiente.
: Para verificar seu saldo, utilize o comando `!fb` `saldo`
"""

TEMPLATE_FABZENDA_ALIMENTAR_ANIMAL_SUCESSO = """
{apelido}, você alimentou o seu Fabichinho com sucesso!
: Ele está muito feliz e agradece a comida.
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=btn_ver_fabzenda]P>
"""

TEMPLATE_FABZENDA_ALIMENTAR_ANIMAL_ERROR = """
{apelido}, não foi possível alimentar o Fabichinho. Algo deu errado.
: Tente novamente e avise o Fabs
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=btn_ver_fabzenda]P>
"""

TEMPLATE_FABZENDA_ALIMENTAR_ANIMAL_DEAD = """
{apelido}, não foi possível alimentar o Fabichinho. Ele já está morto.
: Para adotar um novo fabichinho, visite o Celeiro
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=btn_ver_fabzenda]P>
"""

TEMPLATE_FABZENDA_ALIMENTAR_ANIMAL_NOT_FOUND = """
{apelido}, não foi possível alimentar o Fabichinho. Ele não foi encontrado na sua Fabzenda.
: Para ver seus fabichinhos, vá até sua Fabzenda
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=btn_ver_fabzenda]P>
"""

TEMPLATE_FABZENDA_ALIMENTAR_INSUFFICIENT_BALANCE = """
{apelido}, não foi possível alimentar o Fabichinho. Parece que você não tem saldo suficiente.
: Para verificar seu saldo, utilize o comando `!fb` `saldo`
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=btn_ver_fabzenda]P>
"""

TEMPLATE_FABZENDA_ENTERRAR_ANIMAL_SUCESSO = """
{apelido}, você enterrou o seu Fabichinho!
: Que ele descanse em paz.
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=btn_ver_fabzenda]P>
"""

TEMPLATE_FABZENDA_ENTERRAR_ANIMAL_ERROR = """
{apelido}, não foi possível enterrar o Fabichinho. Algo deu errado.
: Tente novamente e avise o Fabs
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=btn_ver_fabzenda]P>
"""

TEMPLATE_FABZENDA_ENTERRAR_ANIMAL_LIVE = """
{apelido}, não foi possível enterrar o Fabichinho. Ele ainda está vivo.
: Para ver seus fabichinhos, vá até sua Fabzenda
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=btn_ver_fabzenda]P>
"""

TEMPLATE_FABZENDA_ENTERRAR_ANIMAL_NOT_FOUND = """
{apelido}, não foi possível enterrar o Fabichinho. Ele não foi encontrado na sua Fabzenda.
: Para ver seus fabichinhos, vá até sua Fabzenda
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=btn_ver_fabzenda]P>
"""

TEMPLATE_FABZENDA_ENTERRAR_ANIMAL_INSUFFICIENT_BALANCE = """
{apelido}, não foi possível enterrar o Fabichinho. Parece que você não tem saldo suficiente.
: Para verificar seu saldo, utilize o comando `!fb` `saldo`
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=btn_ver_fabzenda]P>
"""

TEMPLATE_FABZENDA_EXPIRAR_ANIMAL_SUCESSO = """
{apelido}, você recebeu a recompensa por ter um fabichinho abduzido!
: Agradeça aos seres de outro planeta.
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=btn_ver_fabzenda]P>
"""

TEMPLATE_FABZENDA_EXPIRAR_ANIMAL_ERROR = """
{apelido}, não foi possível receber a recompensa. Algo deu errado.
: Tente novamente e avise o Fabs
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=btn_ver_fabzenda]P>
"""

TEMPLATE_FABZENDA_EXPIRAR_ANIMAL_LIVE = """
{apelido}, não foi possível receber a recompensa. Ele não foi abduzido.
: Para ver seus fabichinhos, vá até sua Fabzenda
.
<🏕️ Voltar para Fabzenda(fabzenda)[opt=btn_ver_fabzenda]P>
"""

TEMPLATE_FABZENDA_LOTTERY_WIN = """
# Resultado - Jogo do Fabichinhos 🎰
{apelido}, parabéns! Você ganhou `F₵ {reward}` no sorteio do Fabichinhos!
{bonus}
"""

TEMPLATE_FABZENDA_LOTTERY_RESULT = """
# Resultado - Jogo do Fabichinhos 🎰
<!channel> Atenção, atenção! O resultado do sorteio do Fabichinhos foi:
.
> {result}
.
Tivemos {n_ganhadores}, recebendo um total de `F₵ {total_reward}` em prêmios.
{ganhadores}
: Os ganhadores já foram notificados e o premio foi depositado em suas Wallets.
"""

TEMPLATE_FABZENDA_LOTTERY_RESULT_NONE = """
# Resultado - Jogo do Fabichinhos 🎰
Atenção, atenção! O resultado do sorteio do Fabichinhos foi:
.
> {result}
.
Não tivemos ganhadores nesse sorteio. 😿
: Mas não desanime, o próximo pode ser o seu!
"""

TEMPLATE_FABZENDA_FOUND_COIN = """
# Hey, encontrei algo [{emoji}]
{apelido}, seu fabichinho *{name}* estava tão feliz que encontrou fabcoins no chão! :moneybag:
> Acabei de adicionar `F₵ {coin_value}` na sua Wallet.
"""
