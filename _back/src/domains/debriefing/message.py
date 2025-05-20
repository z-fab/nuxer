DEBRIEFING_OPTIONS = """
# 📑 Menu Debriefings
: Selecione uma das opções abaixo
.
 < ☑️ Debriefings Validados(debriefing)[opt=ver_validados,page=1]>
 < 👟 Debriefings Priorizados(debriefing)[opt=ver_priorizados,page=1]>
 < 👀 Debriefings para Validar(debriefing)[opt=ver_para_validar,page=1]D>
.
"""


DEBRIEFING_NOTIFICATE_SOLICITANTE = """
Oi {solicitante}, <@{criado_por}> montou um debriefing para uma demanda que você solicitou e já está *pronto para ser validado*.
.
📑 *[ {cod} ] {titulo}* 
Você pode acessar pelo botão abaixo ou <{url}|clicando aqui>
.
<🔍 Ver Debriefing(debriefing)[opt=ver_debriefing,id={id}]P> <[✔︎] Validar Debriefing(debriefing)[opt=validar_debriefing,id={id}]D>
: ⚠️ Valide apenas após conferir todas as informações e se certificar que o mesmo está correto!

"""

DEBRIEFING_NOTIFICATE_CHANNEL = """
Um debriefing foi criado por <@{criado_por}> e enviado para: {solicitantes}
📑 *[ {cod} ] {titulo}* 
: Você pode acessar pelo botão abaixo ou <{url}|clicando aqui>
<🔍 Ver Debriefing(debriefing)[opt=ver_debriefing,id={id}]P>
"""

DEBRIEFING_NOT_COMPLETED = """
Hey ⚠️,
Parece que você não finalizou o debriefing e tentou notificar o solicitante. Só posso notificar o solicitante se o debriefing estiver preenchido.
: Conclua o debriefing e tente novamente.
.
"""

DEBRIEFING_SOLICITANTE_NOT_FOUND = """
⚠️ Não consegui encontrar o solicitante do debriefing.
Parece que você tentou notificar o solicitante, mas não consegui encontrar quem é.
: Verifique se o solicitante está correto. Na dúvida avise o Fabs
"""

DEBRIEFING_DETALHE_DEBRIEFING = """
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
