from config.const import CONST_NOTION
from externals.context import Context
from models.entities.echo_entity import EchoEntity
from models.mappers.echo_mapper import EchoMapper

context = Context()


def fetch_echo_entity_by_id(echo_id: str | list[str]) -> EchoEntity | list[EchoEntity]:
    """
    Fetches echo entities from Notion by their ID(s).

    This function retrieves one or more echo entities from the Notion database
    using the provided ID(s). If a single ID is provided, a single entity is returned.
    If multiple IDs are provided, a list of entities is returned.

    Args:
        echo_id (str | list[str]): Either a single echo ID as a string or a list of echo IDs.

    Returns:
        EchoEntity | list[EchoEntity]: A single EchoEntity object if a single ID was provided,
        or a list of EchoEntity objects if multiple IDs were provided. If an echo with a
        provided ID doesn't exist, it will be omitted from the results.
    """
    list_echo_entity = []
    list_echo_id = echo_id
    if isinstance(echo_id, str):
        list_echo_id = [echo_id]

    for echo_id in list_echo_id:
        echo_result = context.notion.get_page(echo_id)

        if echo_result is not None:
            echo_entity = EchoMapper.notion_to_entity(echo_result)
            list_echo_entity.append(echo_entity)

    return list_echo_entity if len(list_echo_entity) > 1 else list_echo_entity[0]


def fetch_echo_entities_not_indexed() -> list[EchoEntity]:
    list_result = context.notion.query_database(
        "echo",
        body={
            "filter": {
                "and": [
                    {
                        "property": "Situação",
                        "status": {"does_not_equal": CONST_NOTION.ECHO_STATUS_INDEXAR},
                    }
                ]
            }
        },
    )

    if list_result is None:
        return []

    return [EchoMapper.notion_to_entity(page) for page in list_result]


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
