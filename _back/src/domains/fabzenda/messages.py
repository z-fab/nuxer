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
