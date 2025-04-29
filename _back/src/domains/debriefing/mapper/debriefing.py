from domains.debriefing.entities.debriefing import DebriefingEntity
from domains.debriefing.types.status import DebriefingStatus
from domains.user.repositories.user import UserRepository
from shared.infrastructure.db_context import db
from shared.utils.notion_utils import notion_rich_text_to_markdown, notion_time_to_datetime


def notion_to_entity(notion_response: dict) -> DebriefingEntity | None:
    print(notion_response)

    if not notion_response.get("id"):
        return None

    user_repository = UserRepository(db)

    props = notion_response.get("properties", {})

    criado_por = notion_response.get("created_by", {}).get("id", "")
    criado_por = user_repository.get_user_by_notion_user_id(criado_por.replace("-", ""))

    editado_por = notion_response.get("last_edited_by", {}).get("id", "")
    editado_por = user_repository.get_user_by_notion_user_id(editado_por.replace("-", ""))

    validado_por = props.get("Validado por", {}).get("relation", [{}])
    validado_por = validado_por[0].get("id", "") if len(validado_por) > 0 else ""
    validado_por = user_repository.get_user_by_notion_id(validado_por.replace("-", ""))

    cod = props.get("ID", {}).get("unique_id", {}).get("number", 0)
    cod = f"DB-{cod}"

    titulo = props.get("Demanda", {}).get("title", [{}])
    titulo = notion_rich_text_to_markdown(titulo)

    enviado_em = props.get("ultimo_envio", {}).get("date", {})
    enviado_em = enviado_em.get("start", None) if enviado_em else None
    enviado_em = notion_time_to_datetime(enviado_em)

    validado_em = props.get("Validado em", {}).get("date", {})
    validado_em = validado_em.get("start", None) if validado_em else None
    validado_em = notion_time_to_datetime(validado_em)

    solicitante = props.get("Solicitante", {}).get("relation", [{}])
    solicitante = solicitante[0].get("id", "") if len(solicitante) > 0 else ""
    solicitante = user_repository.get_user_by_notion_id(solicitante.replace("-", ""))

    descricao = props.get("Descrição e Objetivos", {}).get("rich_text", [{}])
    descricao = notion_rich_text_to_markdown(descricao)

    entregaveis = props.get("Entregáveis", {}).get("rich_text", [{}])
    entregaveis = notion_rich_text_to_markdown(entregaveis)

    prazo = props.get("Prazos e Marcos", {}).get("rich_text", [{}])
    prazo = notion_rich_text_to_markdown(prazo)

    destaques = props.get("Destaques", {}).get("rich_text", [{}])
    destaques = notion_rich_text_to_markdown(destaques)

    limitacoes = props.get("Limitações", {}).get("rich_text", [{}])
    limitacoes = notion_rich_text_to_markdown(limitacoes)

    premissas = props.get("Premissas e Requisitos", {}).get("rich_text", [{}])
    premissas = notion_rich_text_to_markdown(premissas)

    outras_info = props.get("Outras Informações", {}).get("rich_text", [{}])
    outras_info = notion_rich_text_to_markdown(outras_info)

    return DebriefingEntity(
        id=notion_response.get("id", "").replace("-", ""),
        cod=cod,
        titulo=titulo,
        status=DebriefingStatus.NAO_PREENCHIDO,
        url=notion_response.get("url", None),
        criado_por=criado_por,
        editado_por=editado_por,
        criado_em=notion_time_to_datetime(notion_response.get("created_time", None)),
        editado_em=notion_time_to_datetime(notion_response.get("last_edited_time", None)),
        enviado_em=enviado_em,
        validado_por=validado_por,
        validado_em=validado_em,
        produto=[""],
        solicitante=solicitante,
        projeto=[""],
        estimativa_bi=props.get("Estimativa BI", {}).get("number", 0),
        estimativa_ux=props.get("Estimativa UX", {}).get("number", 0),
        estimativa_writing=props.get("Estimativa Writing", {}).get("number", 0),
        descricao=descricao,
        entregaveis=entregaveis,
        prazo=prazo,
        destaques=destaques,
        limitacoes=limitacoes,
        premissas=premissas,
        link_workfront=props.get("Link Workfront", {}).get("url", ""),
        outras_informacoes=outras_info,
    )
