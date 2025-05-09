DEBRIEFING_NOTIFICATE_SOLICITANTE = """
Oi {solicitante}!,
A {criado_por} montou um debriefing para uma demanda que você solicitou.
> {titulo}
: Clique no botão abaixo para visualizar o debriefing em detalhes.
<🔍 Ver Debriefing(debriefing)[opt=ver_debriefing,id={id}]P>
"""

DEBRIEFING_NOT_COMPLETED = """
Hey ⚠️,
Parece que você não finalizou o debriefing e tentou notificar o solicitante. Só posso notificar o solicitante se o debriefing estiver preenchido.
: Conclua o debriefing e tente novamente.
.
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

TEMPLATE_DEBRIEFING_NOTIFICAR_CHANNEL = """
Um debriefing foi finalizado e validado por: {solicitantes}.
📑 *[DB-{id_debriefing}] {titulo}*
: {url}
<🔍 Ver Debriefing(debriefing)[opt=ver_debriefing,id={id}]P>
"""
