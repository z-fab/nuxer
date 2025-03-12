class CONST_SLACK:
    SLACK_ID_CHANNEL = {
        "demandas": "C05KDV87GA2",
        "estimativa": "C06E23QD1PE",
        "ux_team": "C042SC9JG5C",
        "ux_review": "C02SCQ7U0EB",
        "playground_ux": "C04N17V06DS",
        "gazeta_uxer": "C07NAJ6C9UY",
    }

    COMMANDS = {
        "fb": "fabcoin-command",
        "msg": "msg-command",
        "survey": "survey-command",
    }

    ID_CHANNEL_DEV = "C04N17V06DS"
    ID_USER_DEV = "U02AL3FMQR4"
    ID_USER_ADMIN = "U02AL3FMQR4"


class CONST_NOTION:
    NOTION_ID_DATABASE = {
        "projetos": "11c349e005944817aabdcebd756bef2a",
        "echo": "136216fde88b80659662d496243a4157",
        "diario": "51ed23cc59294e5dae8a15b3cb776432",
        "ccu": "02ba3fd393a7438db09c13536e388868",
        "baygon": "63047a6b4f2f4b9ab7d93bc10604aa86",
        "tarefas": "9c673c17e42c4160a45f344da8aab48a",
    }

    ## STATUS PROJETO
    STATUS_PROJETO_PARA_ESTIMAR = "0.0. Para Estimar"
    STATUS_PROJETO_ESTIMADO = "0.1. Estimado"
    STATUS_PROJETO_INATIVO = "0.2. Inativo"
    STATUS_PROJETO_PRIORIZADO = "0.3. Priorizado"
    STATUS_PROJETO_CONTINUO = "1.0. Contínuo"
    STATUS_PROJETO_IMPEDIDO = "1.1. Impedido"
    STATUS_PROJETO_EM_EXECUCAO = "1.2. Em Execução"
    STATUS_PROJETO_EM_ACOMPANHAMENTO = "1.3. Em Acompanhamento"
    STATUS_PROJETO_FINALIZADO = "2.0. Finalizado"

    ## STATUS TAREFA
    STATUS_TAREFA_PARA_FAZER = "0. Para Fazer"
    STATUS_TAREFA_PAUSADO = "1. Pausado"
    STATUS_TAREFA_FAZENDO = "2. Fazendo"
    STATUS_TAREFA_FINALIZADO = "3. Finalizado"

    ## BAYGON
    BAYGON_SEVERIDADE_CRITICO = "1. Crítico"
    BAYGON_SEVERIDADE_IMPORTANTE = "2. Importante"
    BAYGON_SEVERIDADE_ATENCAO = "3. Atenção"
    BAYGON_SEVERIDADE_COSMETICO = "4. Cosmético"

    BAYGON_STATUS_BACKLOG = "Backlog"
    BAYGON_STATUS_NOTIFICAR = "Notificar"
    BAYGON_STATUS_AJUSTANDO = "Ajustando"
    BAYGON_STATUS_CORRIGIDO = "Corrigido"

    ## STATUS CCU
    CCU_STATUS_WAITING = "0. Waiting"
    CCU_STATUS_DOING = "1. Doing"
    CCU_STATUS_DONE = "2. Done"
    CCU_STATUS_ERROR = "3. Error"

    ## STATUS ECHO
    ECHO_STATUS_CADASTRO = "Cadastro"
    ECHO_STATUS_INDEXAR = "Indexar"
    ECHO_STATUS_INDEXADO = "Indexado"


class CONST_MESSAGE:
    MESSAGE = {
        # WEEKLY
        "weekly": """
        # Weekly do Time :point_right::point_left:
        <!channel> Passando para lembrar que hoje temos nossa Semanal do time as 16h30.
        Não se esqueçam de preencher o arquivo da Weekly dessa semana: https://www.notion.so/fabzd/86452b5a02fb4c6f84ea92b76806832c?v=4c2a8fdcc2e6489cbc80263fe7693f26
        Confirmem presença no invite e bebam água. Lembrando que é muito importante a participação de todas as pessoas do time.
        """,
        # SHARECODE
        "sharecode": """
        # ShareCode :tv: :musical_note: :microphone:
        <!channel> Galerinha, Fabs pediu para lembrar do nosso *ShareCode: Research* a cada 15 dias
        Chamem todos pra participar. Cronograma de apresentações:
        *→ ??/??* - A Definir - A Definir
        *→ 13/05* - Felipe - Titano! Como estamos?
        *→ 27/05* - Amanda - Novidades PROX 2
        *→ 10/06* - Writers - Novo DoC!
        """,
        # LANÇAMENTO DE HORAS
        "lancamento_horas": """
        # Weekly do Time :point_right::point_left:
        <!channel> Passando para lembrar que hoje temos nossa Semanal do time as 16h30.
        Não se esqueçam de preencher o arquivo da Weekly dessa semana: https://www.notion.so/fabzd/86452b5a02fb4c6f84ea92b76806832c?v=4c2a8fdcc2e6489cbc80263fe7693f26
        Confirmem presença no invite e bebam água. Lembrando que é muito importante a participação de todas as pessoas do time.
        """,
    }

    # ======================================================
    # ============== TEMPLATES LOGIN =====================
    # ======================================================

    TEMPLATE_LOGIN_MAGIC_LINK = """
    {saudacao}! :wave:
    Fiquei sabendo que você gostaria de acessar minha casa! :house:
    Para isso, basta clicar no link abaixo! Esse convite é exclusivo para você e expira em 5 minutos.

    : ⚠️ Não compartilhe esse link com ninguém! Ele é exclusivo para você e libera acesso às suas informações .
    :link: {magic_link}
    """

    TEMPLATE_VERIFY_MAGIC_LINK = """
    {saudacao},
    Passando para avisar que alguém acessou minha casa usando seu convite! :house:
    Se não foi você, por favor, avise o Fabs imediatamente.
    Se foi você, sintam-se em casa! :smile:
    """

    # ======================================================
    # ============== TEMPLATES BAYGON =====================
    # ======================================================

    # Notificar criação de Baygon para responsáveis
    TEMPLATE_BAYGON_NOTIFY_DM = """
    Uma pessoa do time de UX encontrou um problema em um produto no ar e pediu para te notificar!
    Quando o problema for resolvido, ou caso tenha alguma dúvida, é só procurar alguém do time ou o autor do registro :smile:
    """

    # Notificar criação de Baygon para o canal
    TEMPLATE_BAYGON_NOTIFY_CHANNEL = """
    # 🪲 Baygon :: Problema encontrado
    Um problema foi encontrado em um produto no ar e notifiquei {users_notify}.
    """

    # Lembrete de Baygon para responsáveis
    TEMPLATE_BAYGON_NOTIFY_DM_REMEMBER = """
    Passando para lembrar que temos alguns problemas em produtos no ar que precisam ser resolvidos.
    Se foi resolvido (ou está sendo), por favor, fale com o time de UX para que eles me avisem! :smile:
    """

    # Lembrete de Baygon para o canal
    TEMPLATE_BAYGON_NOTIFY_CHANNEL_REMEMBER = """
    <!channel> Olá! Passando para lembrar que temos alguns problemas em produtos no ar que precisam ser resolvidos. Já notifiquei as pessoas responsáveis, mas é sempre bom lembrar!
    Se foi resolvido (ou está sendo), por favor, fale com o time de UX para que eles me avisem! :smile:
    """

    # Registro de Baygon - Completo
    TEMPLATE_BAYGON_REGISTER_FULL = """
    # {emoji_severidade} [BY-{id_baygon}] {problema}
    : Erro classificado como {severidade}. {url}
    > *Descrição*:
    {descricao}
    > *Resolução Sugerida*:
    {resolucao}
    > *Informações*:
    Esse erro está marcado como *{status}*.
    Em caso de dúvida, procure por <@{criado_por}>
    Aberto há {dias_criacao}.
    > *Ações*:
    : Se esse problema já foi endereçado, marque como Ajustado
    <🚜 Marcar como Ajustando(baygon)[action=ajustando,id={id_page}]>
    : Se esse problema já foi resolvido, sinalize para o time
    <✅ Sinalizar como Resolvido(baygon)[action=avisar_resolvido,id={id_page}]>
    """

    # Registro de Baygon - Pequeno
    TEMPLATE_BAYGON_REGISTER_SMALL = """
    *{emoji_severidade} [BY-{id_baygon}] {problema}* - {descricao}
    : Classificado como {severidade}.
    : Marcado como *{status}*.
    : Notifiquei {users_notify}
    : Aberto há {dias_criacao}.
    """

    # Aviso que Baygon foi marcado como ajustando
    TEMPLATE_BAYGON_AJUSTANDO_DM = """
    O problema *[BY-{id_baygon}] {problema}* foi marcado como `Ajustando` 😊.
    : Quando for resolvido, por favor, avise o time de UX ou use o botão "✅ Sinalizar como Resolvido".
    """

    # Aviso para o time que Baygon foi marcado como ajustando
    TEMPLATE_BAYGON_AJUSTANDO_CHANNEL = """
    *🪲 Baygon :: Ajustando*
    O problema *[BY-{id_baygon}] {problema}* foi marcado como `Ajustando` por <@{ajustado_por}>.
    """

    # Aviso que Baygon foi sinalizado como resolvido
    TEMPLATE_BAYGON_SINALIZAR_RESOLVIDO_DM = """
    O problema *[BY-{id_baygon}] {problema}* foi sinalizado como `Resolvido` ✅.
    O time de UX irá validar e, se estiver tudo certo, o problema será fechado.
    : Se precisar de mais informações, fale com o time de UX.
    """

    # Aviso para o time que Baygon foi sinalizado como resolvido
    TEMPLATE_BAYGON_SINALIZAR_RESOLVIDO_CHANNEL = """
    *🪲 Baygon :: Resolvido*
    O problema *[BY-{id_baygon}] {problema}* foi sinalizado como `Resolvido` por <@{resolvido_por}>.
    : Notifiquei a pessoa responsável pelo registro (<@{criado_por}>).
    """

    # Aviso para o responsável que Baygon foi sinalizado como resolvido
    TEMPLATE_BAYGON_SINALIZAR_RESOLVIDO_NOTIFY = """
    O problema *[BY-{id_baygon}] {problema}* foi sinalizado como `Resolvido` por <@{resolvido_por}>. Você pode acessar o registro <{url_page}|clicando aqui>.
    Valide se está tudo certo e, se sim, feche o problema.
    <✅ Marcar como Resolvido(baygon)[action=marcar_corrigido,id={id_page}]>
    """

    # Aviso que Baygon foi corrigido
    TEMPLATE_BAYGON_CORRIGIDO_DM = """
    O problema *[BY-{id_baygon}] {problema}* foi confirmado como corrigido 🥳.
    : Obrigado por ajudar a melhorar nossos produtos! <3
    """

    # Aviso para o time que Baygon foi corrigido
    TEMPLATE_BAYGON_CORRIGIDO_CHANNEL = """
    *🪲 Baygon :: Resolvido*
    O problema *[BY-{id_baygon}] {problema}* foi confirmado como corrigido 🥳.
    : Uma fada não morrerá hoje, graças a nós! <3
    """

    # Aviso para o responsável que Baygon foi corrigido
    TEMPLATE_BAYGON_CORRIGIDO_NOTIFY = """
    Atualizei o problema *[BY-{id_baygon}] {problema}* como corrigido <3.
    """

    # ======================================================
    # ============= TEMPLATES DEBRIEFING ===================
    # ======================================================

    TEMPLATE_DEBRIEFING_NOTIFICAR_RESPONSAVEL = """
    {saudacao}
    Uma pessoa do time de UX finalizou um debriefing e pediu para te notificar! Verifique o debriefing e, caso encontre algo errado, entre em contato com o time de UX.
    
    # [DB-{id_debriefing}] Debriefing: {titulo}
    : {url}
    > *Descrição e Objetivos*:
    {descricao}
    > *Entregáveis*:
    {entregaveis}
    > *Prazos e Marcos*:
    {prazos}
    > *Destaques*:
    {destaques}
    > *Limitações*:
    {limitacoes}
    > *Premissas e Requisitos*:
    {premissas}
    --
    : Com base nas informações do debriefing, a estimativa para a realização da demanda é:
    *Estimativa de BI*: {estimativa_bi}
    *Estimativa de UX*: {estimativa_ux}
    *Estimativa de Writing*: {estimativa_writing}
    --
    """

    TEMPLATE_DEBRIEFING_NOTIFICAR_CHANNEL = """
    Um debriefing foi finalizado e já notifiquei: {solicitantes}.
    📑 *[DB-{id_debriefing}] {titulo}*
    : {url}
    """

    # ======================================================
    # ============== TEMPLATES FABZENDA ====================
    # ======================================================

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

    # ======================================================
    # ============== TEMPLATES FABBANK =====================
    # ======================================================

    TEMPLATE_FABBANK_WALLET = """
    # Extrato do FabBank :moneybag:
    {apelido}, aqui está o saldo da sua Wallet:
    > *Saldo atual*: `F₵ {balance}`
    : Wallet ID: {id_wallet} - Valores atualizados em {data}
    """

    TEMPLATE_FABBANK_TRANSFER_SUCCESS = """
    # Transferência Realizada com Sucesso :money_with_wings:
    {apelido}, você realizou uma transferência com o sucesso.
    > *Você transferiu* `F₵ {amount}` para `{to_name} (Wallet ID: {to_id_wallet})`
    *Motivo informado:* _{desc}_
    : Wallet ID: {id_wallet} - transação realizada em {data}
    """

    TEMPLATE_FABBANK_TRANSFER_RECEIVE = """
    # Recebimento de Transferência :moneybag:
    {to_apelido}, você recebeu uma transferência em sua Wallet.
    > *Você recebeu* `F₵ {amount}` de `{from_name} (Wallet ID: {from_id_wallet})`
    *Motivo informado:* _{desc}_
    """

    TEMPLATE_FABBANK_DISCOUNT_RECEIVE = """
    # Desconto Recebido :money_with_wings:
    {to_apelido}, você recebeu um desconto em sua Wallet.
    > *Você foi descontado* `F₵ {amount}` de `{from_name} (Wallet ID: {from_id_wallet})`
    *Motivo informado:* _{desc}_
    """

    TEMPLATE_FABBANK_TRANSFER_ERROR = """
    Ops, ocorreu um erro ao realizar a transferência :warning:
    : Tente novamente e avise o Fabs
    """

    TEMPLATE_FABBANK_TRANSFER_ERROR_USER_NOT_FOUND = """
    Ops, parece que o usuário que você escolheu para receber a transferência não tem uma wallet no FabBank :warning:
    : Verifique o usuário que você escolheu para receber a transferência e tente novamente
    """

    TEMPLATE_FABBANK_TRANSFER_ERROR_WALLET_NOT_FOUND = """
    Ops, parece que você (ou a pessoa para quem você quer transferir) não tem uma wallet no FabBank :warning:
    : Para criar fale com o Fabs
    """

    TEMPLATE_FABBANK_TRANSFER_ERROR_PARAMS = """
    Ops, parece que você não preencheu corretamente os parâmetros para realizar a transferência :warning:
    : Para realizar a transferência, utilize o comando `!fb` `pix` `[@usuario]` `[valor]` `"[descrição]"`
    """

    TEMPLATE_FABBANK_TRANSFER_ERROR_INSUFFICIENT_BALANCE = """
    Ops, parece que você não tem saldo suficiente para realizar a transferência ou o valor informado é inválido :warning:
    : Verifique o saldo da sua Wallet com o comando `!fb` `saldo`
    """

    TEMPLATE_FABBANK_EXTRACT = """
    # Extrato FabBank :moneybag:
    {apelido}, aqui está o extrato da sua Wallet (ID {id_wallet}) em {data}:
    > *Saldo atual*: `F₵ {balance}`
    --
    {extract}
    """

    TEMPLATE_FABBANK_EXTRACT_TRANSACTION = """
    *{user_from}* (Wallet ID: {id_wallet_from}) transferiu `F₵ {amount}`
    *Motivo:* {description}
    : Transação realizada em {timestamp}
    --
    """

    TEMPLATE_FABBANK_WALLET_ADMIN = """
    # Saldos no Fabbank
    Aqui estão os saldos no Fabbank
    > *Saldo Total*: `F₵ {balance_total}`
    --
    {balances}
    """

    TEMPLATE_FABBANK_LOJA = """
    # Vendinha do Uxer 🛍️
    A melhor, maior e única loja do mundo que aceita Fabcoins! Preços atualizados a todo momento.
    > Seu saldo: `F₵ {balance}`
    --
    {items}
    """

    TEMPLATE_FABBANK_LOJA_ITEM = """
    [ cod: *{id}* ] {item} `F₵ {price}`
    : {description}
    {amount}
    <🛒 Comprar(fb)[opt=btn_comprar,id={id},preco={price}]>
    --
    """

    TEMPLATE_FABBANK_LOJA_ITEM_COMPRADO = """
    # Item Comprado 🛒
    {apelido}, você comprou um item da loja com sucesso!
    > {item} por `F₵ {price}`
    : Já notifiquei o fabs e em breve o item será enviado.
    """

    TEMPLATE_FABBANK_LOJA_ITEM_NAO_COMPRADO = """
    # Ops, item não comprado 🛒
    {apelido}, não foi possível realizar a compra do seu item. Verifique seu saldo ou se o preço do item não foi alterado
    > {item} por `F₵ {price}`
    : Para verificar seu saldo, utilize o comando `!fb` `saldo` e para verificar os itens com preço atualizado, utilize o comando `!fb` `loja`
    """

    TEMPLATE_FABBANK_LOJA_ITEM_COMPRADO_ADMIN = """
    --
    # Item Comprado 🛍️
    {user_from} comprou um item da loja.
    > {item} por `F₵ {price}` em {data}
    --
    """

    # ======================================================
    # ============== MESSAGE COMMAND =====================
    # ======================================================

    MESSAGE_COMMAND_ADMIN_ONLY = """
    Desculpe, mas esse comando é só para o Fabs usar :warning:
    : Ei, como você conseguiu adivinhar esse comando? Vou ter que contar pra o Fabs. 
    """

    MESSAGE_COMMAND_THREAD_ONLY = """
    Desculpe, mas por motivos de segurança, esse comando só pode ser utilizado em nossa conversa privada :eyes:
    : Só me chamar na DM que eu te ajudo :) 
    """

    MESSAGE_COMMAND_NOT_FOUND = """
    Desculpe, mas eu não entendi qual comando você quis utilizar. Por enquanto o Fabs só me ensinou:
    --
    > `!fb` - Comando do FabBank para gerenciar sua wallet
    --
    Você pode utilizar a palavra `help` após o comando para ver detalhes de como utilizar. Exemplo: `!fb help`
    """

    MESSAGE_COMMAND_FB_HELP = """
    # Comando FabBank [ !fb ]
    Comando do FabBank para gerenciar sua wallet
    --
    > `!fb` `saldo` - Para consultar o saldo da sua wallet
    > `!fb` `extrato` - Para consultar o extrato da sua wallet. Visualiza os 10 últimos pix recebidos
    > `!fb` `pix` `[@usuario]` `[valor]` `"[descrição]"` - Para transferir valor para outro usuário
    > `!fb` `loja` - Para consultar os itens disponíveis na loja e comprar
    --
    : `[@usuario]` - Usuário que receberá o pix.
    : `[valor]` - Valor da transferência. Deve ser um número inteiro.
    : `"[descrição]"` - Descrição da transferência. Deve ser um texto *envolto por aspas duplas*.
    """

    MESSAGE_COMMAND_SURVEY_HELP = """
    # Comando Survey [ !survey ]
    Comando para responder pesquisas do DataUxer
    --
    > `!survey` `list` - Para listar as pesquisas disponíveis
    > `!survey` - Para responder uma pesquisa aleatória
    """

    MESSAGE_RESPOND_COMMAND = """
    Certo! Vou fazer agora mesmo. Só um instante... 🕐
    """

    MESSAGE_RESPOND_COMMAND_ERROR = """
    😥 Desculpe, meus bits estão confusos. Não consegui executar o comando.\nDeve ser culpa do aquecimento global. Tente novamente ou avise o time de UX
    """

    MESSAGE_RESPOND_ACTION = """
    Certo! Vou fazer agora mesmo. Só um instante... 🕐
    """

    MESSAGE_RESPOND_ACTION_ERROR = """
    😥 Desculpe, meus bits estão confusos. Não consegui executar o comando.\nDeve ser culpa do aquecimento global. Tente novamente ou avise o time de UX
    """

    # ======================================================
    # ============== MESSAGE ADMIN =====================
    # ======================================================

    MESSAGE_RECEIVE_BY_UXER = """
    *✉️ Mensagem recebida pelo UXER*
    `Quem`: {user_name} ({user_slack_id})
    `Onde`: {channel_name} ({channel_id})
    `Mensagem`
    {message}
    {commands}
    : {timestamp}
    --
    """

    MESSAGE_ANSWER_BY_UXER = """
    *💬 Mensagem respondida pelo UXER*
    `Para quem`: {user_name} ({user_slack_id})
    `Onde`: {channel_name} ({channel_id})
    `Mensagem`
    {message}
    : {timestamp}
    --
    """


class CONST_VIEW:
    # ======================================================
    # ================= VIEW SURVEY ========================
    # ======================================================

    VIEW_HOME_FABZENDA = {
        "type": "modal",
        "title": {"type": "plain_text", "text": "", "emoji": True},
        "close": {"type": "plain_text", "text": "Fechar", "emoji": True},
        "private_metadata": "",
        "blocks": [],
    }

    VIEW_HOME_FABZENDA_DETALHE_ANIMAL = {
        "type": "modal",
        "title": {"type": "plain_text", "text": "Detalhes do Fabicho 🌾", "emoji": True},
        "close": {"type": "plain_text", "text": "Fechar", "emoji": True},
        "private_metadata": "",
        "blocks": [],
    }


class CONST_ERROR:
    FABBANK_TRANSFER_USER_NOT_FOUND = "User not found"
    FABBANK_TRANSFER_INSUFFICIENT_BALANCE = "Insufficient balance"
    FABBANK_TRANSFER_WALLET_NOT_FOUND = "Wallet not found"
    FABBANK_TRANSFER_PARAMS = "Invalid params"
    FABBANK_TRANSFER_FAILED = "Transfer failed"

    FABBANK_CHANGE_COINS_FAILED = "Change coins failed"

    FABBANK_LOJA_ITEM_NOT_FOUND = "Item not found"
    FABBANK_LOJA_INSUFFICIENT_BALANCE = "Insufficient balance"
    FABBANK_LOJA_ITEM_UNAVAILABLE = "Item unavailable"
    FABBANK_LOJA_FAILED = "Purchase failed"

    FABZENDA_COMPRAR_MAX_ANIMALS = "Max animals"
    FABZENDA_COMPRAR_BALANCE_INSUFFICIENT = "Insufficient balance"
    FABZENDA_COMPRAR_ANIMAL_UNAVAILABLE = "Animal unavailable"
    FABZENDA_COMPRA_ANIMAL_FAILED = "Purchase failed"

    FABZENDA_ALIMENTAR_ANIMAL_NOT_FOUND = "Animal not found"
    FABZENDA_ALIMENTAR_ANIMAL_DEAD = "Animal dead"
    FABZENDA_ALIMENTAR_ANIMAL_FAILED = "Feed failed"
    FABZENDA_ALIMENTAR_INSUFFICIENT_BALANCE = "Insufficient balance"

    FABZENDA_ENTERRAR_ANIMAL_NOT_FOUND = "Animal not found"
    FABZENDA_ENTERRAR_INSUFFICIENT_BALANCE = "Insufficient balance"
    FABZENDA_ENTERRAR_ANIMAL_FAILED = "Burial failed"
    FABZENDA_ENTERRAR_ANIMAL_LIVE = "Animal live"

    FABZENDA_EXPIRAR_ANIMAL_FAILED = "Burial failed"
    FABZENDA_EXPIRAR_ANIMAL_LIVE = "Animal live"
