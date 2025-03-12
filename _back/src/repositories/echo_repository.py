from typing import List
from externals.context import Context
from config.const import CONST_NOTION
from loguru import logger

from models.entities.echo_entity import EchoEntity
from models.mappers.echo_mapper import EchoMapper


context = Context()


# def get_baygon_by_id(baygon_id: str | List[str]) -> EchoEntity | List[EchoEntity]:
#     list_baygon_entity = []
#     list_baygon_id = baygon_id
#     if isinstance(baygon_id, str):
#         list_baygon_id = [baygon_id]

#     for baygon_id in list_baygon_id:
#         baygon_result = context.notion.get_page(baygon_id)

#         if baygon_result is not None:
#             result_mapper = EchoMapper
#             .notion_to_entity(baygon_result)
#             list_baygon_entity.append(result_mapper)

#     return list_baygon_entity if len(list_baygon_entity) > 1 else list_baygon_entity[0]


def get_echo_not_indexed() -> List[EchoEntity]:
    list_result = context.notion.query_database(
        "echo",
        body={
            "filter": {
                "and": [
                    {
                        "property": "Situação",
                        "status": {
                            "does_not_equal": CONST_NOTION.ECHO_STATUS_INDEXAR
                        },
                    }
                ]
            }
        },
    )

    list_echo_entity = []
    for page in list_result:
        echo_entity = EchoMapper.notion_to_entity(page)
        logger.debug(f"Page returned: {echo_entity}")
        list_echo_entity.append(echo_entity)

    return list_echo_entity


# def get_baygon_by_baygon_id(baygon_id: str) -> EchoEntity:
#     list_result = context.notion.query_database(
#         "baygon",
#         body={
#             "filter": {
#                 "property": "ID",
#                 "unique_id": {"equals": int(baygon_id.split("-")[1])},
#             },
#         },
#     )

#     if list_result is not None:
#         baygon_entity = EchoMapper.notion_to_entity(list_result[0])
#         logger.debug(f"Page returned: {baygon_entity}")

#     return baygon_entity


# def set_baygon_status(page_id: str, status: str) -> bool:
#     json_body = {}
#     json_body["properties"] = {}
#     json_body["properties"]["Status"] = {}
#     json_body["properties"]["Status"]["status"] = {"name": status}

#     baygon_updated = context.notion.update_page(page_id=page_id, json_body=json_body)
#     if baygon_updated is not None:
#         return EchoMapper.notion_to_entity(baygon_updated)

#     return False
