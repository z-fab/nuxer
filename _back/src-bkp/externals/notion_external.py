import requests
from _back.src.shared.config.settings import SETTINGS as S
from loguru import logger

from config.const import CONST_NOTION


class NotionExternal:
    # ===================== #
    #  BASES                #
    # ===================== #
    def __init__(self):
        """
        Inicializa o serviço do Notion com as configurações necessárias.
        """
        self.__BASE_URL = "https://api.notion.com/v1"
        self.__TOKEN = S.NOTION_TOKEN
        self.__headers = {
            "Authorization": f"Bearer {self.__TOKEN}",
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "content-type": "application/json",
        }

    def __request(self, method: str, endpoint: str, body: dict[str, None] = None) -> dict[str, None]:
        """
        Realiza uma requisição HTTP para a API do Notion.

        Args:
            method (str): Método HTTP (GET, POST, PATCH, DELETE).
            endpoint (str): Endpoint da API.
            body (dict, opcional): Corpo da requisição, se aplicável.

        Returns:
            dict: Resposta da API em formato JSON, ou None se houver erro.

        Raises:
            requests.RequestException: Se ocorrer um erro durante a requisição.
        """
        url = f"{self.__BASE_URL}{endpoint}"
        logger.debug(f"Requesting {url} with method {method} and body {body}")

        try:
            response = requests.request(method=method, url=url, headers=self.__headers, json=body)

            response.raise_for_status()

            response_data = response.json()
            logger.debug(f"Request return: {response_data}")
            return response_data

        except requests.RequestException as error:
            logger.error(f"ERROR REQUESTING NOTION API: {error}")
            return None

    def query_database(self, database_id: str, body=None):
        """
        Recupera todas as páginas de um database do Notion.

        Args:
            database_id (str): ID do database no Notion.
            body (dict, optional): Corpo da requisição para filtrar ou ordenar resultados.

        Returns:
            list: Lista de objetos NotionPage representando as páginas do database.
        """
        result = []

        notion_database_id = CONST_NOTION.NOTION_ID_DATABASE.get(database_id, database_id)
        response = self.__request(endpoint=f"/databases/{notion_database_id}/query", method="POST", body=body)

        if response is None:
            return result

        logger.debug(f"Number of pages returned: {len(response['results'])}")
        result += response["results"]

        if response["has_more"]:
            logger.debug(f"Next cursor at get_database: {response['next_cursor']}")
            body = {"start_cursor": response["next_cursor"]}
            result = result + self.query_database(database_id, body)

        return result

    def get_page(self, page_id: str):
        response = self.__request(endpoint=f"/pages/{page_id}", method="GET")

        if response is None:
            return None

        logger.debug(f"Page returned: {response}")
        return response

    def update_page(self, page_id: str, json_body: dict[str, None]):
        logger.debug(f"Updating page {page_id} with {json_body}")

        response = self.__request(endpoint=f"/pages/{page_id}", method="PATCH", body=json_body)

        return response

    # ===================== #
    #  PAGES                #
    # ===================== #

    # def get_page(self, page_id: str):
    #     """
    #     Recupera uma página específica do Notion.

    #     Args:
    #         page_id (str): ID da página no Notion.

    #     Returns:
    #         NotionPage: Objeto representando a página, ou None se não encontrada.
    #     """
    #     response = self.__request(
    #         endpoint=f"{self.__BASE_URL}/pages/{page_id}", method="GET"
    #     )

    #     if response is None:
    #         return None

    #     logger.debug(f"Page returned: {response}")
    #     return NotionPage(api_response=response)

    # def create_page(self, notionPage: NotionPage):
    #     """
    #     Cria uma nova página no Notion.

    #     Args:
    #         notionPage (NotionPage): Objeto representando a página a ser criada.

    #     Returns:
    #         dict: Resposta da API do Notion após a criação da página.
    #     """

    #     body = notionPage.get_api_dict()

    #     logger.debug(f"Creating page {body}")
    #     response = self.__request(f"{self.__BASE_URL}/pages", "POST", body)

    #     return response

    # def update_page(self, notionPage: NotionPage = None):
    #     """
    #     Atualiza uma página existente no Notion.

    #     Args:
    #         notionPage (NotionPage): Objeto representando a página a ser atualizada.

    #     Returns:
    #         dict: Resposta da API do Notion após a atualização da página.
    #     """
    #     url_request = f"{self.__BASE_URL}/pages/{notionPage.id}"

    #     logger.debug(f"Updating page {notionPage.id} with {notionPage.properties}")

    #     body = {}
    #     if len(notionPage.properties) > 0:
    #         body["properties"] = notionPage.properties

    #     response = self.__request(endpoint=url_request, method="PATCH", body=body)

    #     return response

    # # ===================== #
    # #  DIÁRIO & TAREFAS     #
    # # ===================== #

    # def create_page_diario(self, projeto_id: str, registro: str, desc: str, tipo: str):
    #     """
    #     Cria um novo diário associado a um projeto no Notion.

    #     Args:
    #         projeto_id (str): ID do projeto associado.
    #         registro (str): Título do registro do diário.
    #         desc (str): Descrição do diário.
    #         tipo (str): Tipo do diário.

    #     Returns:
    #         NotionPage: Objeto representando o diário criado, ou None se falhar.
    #     """
    #     projects = self.get_project_by_code(projeto_id)
    #     if projects is None or len(projects) <= 0:
    #         return None

    #     notionPage = NotionPage(
    #         parent=CONST_NOTION.NOTION_ID_DATABASE["diario"], properties={}
    #     )

    #     notionPage.properties["Registro"] = {}
    #     notionPage.properties["Registro"]["title"] = [{"text": {"content": registro}}]

    #     notionPage.properties["Descrição"] = {}
    #     notionPage.properties["Descrição"]["rich_text"] = [{"text": {"content": desc}}]

    #     notionPage.properties["Projeto"] = {}
    #     notionPage.properties["Projeto"]["relation"] = [{"id": projects[0].id_notion}]

    #     notionPage.properties["Tipo"] = {}
    #     notionPage.properties["Tipo"]["multi_select"] = [{"name": tipo}]

    #     notionPage.properties["Data"] = {}
    #     notionPage.properties["Data"]["date"] = {
    #         "start": datetime.now().strftime("%Y-%m-%d")
    #     }

    #     response_notion = self.create_page(notionPage=notionPage)

    #     responsePage = NotionPage(api_response=response_notion)

    #     return responsePage

    # def get_diarios_from_project_id(self, notionPage: NotionPage):
    #     """
    #     Recupera diários associados a um projeto específico.

    #     Args:
    #         notionPage (NotionPage): Objeto representando o projeto.

    #     Returns:
    #         list: Lista de objetos NotionDiarioDTO representando os diários do projeto.
    #     """
    #     logger.debug("Start get diarios by Project id")
    #     result = self.get_database(
    #         CONST_NOTION.NOTION_ID_DATABASE["diario"],
    #         body={
    #             "filter": {
    #                 "or": [
    #                     {
    #                         "property": "Projeto",
    #                         "relation": {"contains": notionPage.id},
    #                     },
    #                     {
    #                         "property": "Projeto [Tarefa]",
    #                         "rollup": {
    #                             "any": {
    #                                 "rich_text": {
    #                                     "contains": notionPage.properties.get(
    #                                         "Nome", {}
    #                                     )
    #                                     .get("title", [{}])[0]
    #                                     .get("plain_text", "")
    #                                 }
    #                             }
    #                         },
    #                     },
    #                 ]
    #             },
    #             "sorts": [{"property": "Data", "direction": "descending"}],
    #         },
    #     )

    #     list_diarios = []
    #     logger.debug(f"Number of diarios: {len(result)}")
    #     if len(result) > 0:
    #         for diario in result:
    #             logger.debug(f"Diario: {diario}")
    #             # diario_dto = NotionDiarioDTO(notionPage=diario)
    #             # list_diarios.append(diario_dto)

    #     return list_diarios

    # # ===================== #
    # #  PROJETO              #
    # # ===================== #

    # def get_projects(self, filter: dict = None):
    #     """
    #     Recupera projetos do Notion com base em um filtro opcional.

    #     Args:
    #         filter (dict, optional): Filtro para a consulta de projetos.

    #     Returns:
    #         list: Lista de objetos NotionProject representando os projetos.
    #     """
    #     logger.debug(f"Getting projects from Notion with filter {filter}")

    #     result = self.get_database(
    #         CONST_NOTION.NOTION_ID_DATABASE["projetos"],
    #         body={"filter": filter} if filter else None,
    #     )

    #     list_projetos = []
    #     logger.debug(f"Number of projects: {len(result)}")
    #     if len(result) > 0:
    #         for projeto in result:
    #             diarios_list = self.get_diarios_from_project_id(projeto)
    #             tarefas_list = self.get_tarefas_from_project_id(projeto)
    #             logger.debug(f"Number of tarefas: {tarefas_list}")
    #             projeto_dto = NotionProject(
    #                 notionPage=projeto, diarios=diarios_list, tarefas=tarefas_list
    #             )
    #             list_projetos.append(projeto_dto)

    #     return list_projetos

    # def get_active_projects(self):
    #     """
    #     Recupera todos os projetos ativos do Notion.

    #     Returns:
    #         list: Lista de objetos NotionProject representando os projetos ativos.
    #     """
    #     return self.get_projects(
    #         {
    #             "and": [
    #                 {
    #                     "property": "Situação",
    #                     "status": {
    #                         "does_not_equal": CONST_NOTION.STATUS_PROJETO_FINALIZADO
    #                     },
    #                 },
    #                 {
    #                     "property": "Situação",
    #                     "status": {
    #                         "does_not_equal": CONST_NOTION.STATUS_PROJETO_CONTINUO
    #                     },
    #                 },
    #                 {
    #                     "property": "Situação",
    #                     "status": {
    #                         "does_not_equal": CONST_NOTION.STATUS_PROJETO_INATIVO
    #                     },
    #                 },
    #             ]
    #         }
    #     )

    # def get_active_projects_by_responsavel(self, id_notion: str = None):
    #     """
    #     Recupera projetos ativos associados a um responsável específico.

    #     Args:
    #         id_notion (str, optional): ID do responsável no Notion.

    #     Returns:
    #         list: Lista de objetos NotionProject representando os projetos ativos do responsável.
    #     """
    #     logger.debug("Start get projects from Notion by Responsável")
    #     filter = {
    #         "and": [
    #             {
    #                 "property": "Situação",
    #                 "status": {"does_not_equal": "2.0. Finalizado"},
    #             },
    #             {"property": "Situação", "status": {"does_not_equal": "1.0. Contínuo"}},
    #             {
    #                 "property": "Situação",
    #                 "status": {"does_not_equal": CONST_NOTION.STATUS_PROJETO_INATIVO},
    #             },
    #         ]
    #     }

    #     if id_notion is not None:
    #         filter["and"].append(
    #             {"property": "Responsável", "relation": {"contains": id_notion}}
    #         )
    #     else:
    #         filter["and"].append({"property": "Responsável", "is_not_empty": True})

    #     return self.get_projects(filter)

    # def get_project_by_code(self, code_project: str = None) -> NotionProject:
    #     """
    #     Recupera um projeto específico pelo seu código.

    #     Args:
    #         code_project (str): Código do projeto.

    #     Returns:
    #         list: Lista contendo o objeto NotionProject do projeto, ou None se não encontrado.
    #     """
    #     logger.debug("Getting projects from Notion by code")

    #     filter = {
    #         "property": "ID",
    #         "unique_id": {"equals": int(code_project.split("-")[1])},
    #     }

    #     return self.get_projects(filter)

    # def get_project_by_id(self, id_project: str = None):
    #     """
    #     Recupera um projeto específico pelo seu ID do Notion.

    #     Args:
    #         id_project (str): ID do projeto no Notion.

    #     Returns:
    #         NotionProject: Objeto representando o projeto, ou None se não encontrado.
    #     """
    #     logger.debug("Start get projects from Notion by Id")

    #     if id_project is None:
    #         return None
    #     page = self.get_page(id_project)

    #     diarios_list = self.get_diarios_from_project_id(page)
    #     tarefas_list = self.get_tarefas_from_project_id(page)
    #     projeto_dto = NotionProject(
    #         notionPage=page, diarios=diarios_list, tarefas=tarefas_list
    #     )

    #     return projeto_dto

    # # ===================== #
    # #  BLOCKS & PROPERTIES  #
    # # ===================== #

    # def get_properties(self, page_id: str, prop_id: str, body: dict = None):
    #     """
    #     Recupera propriedades específicas de uma página do Notion.

    #     Args:
    #         page_id (str): ID da página no Notion.
    #         prop_id (str): ID da propriedade a ser recuperada.
    #         body (dict, optional): Corpo adicional para a requisição.

    #     Returns:
    #         dict: Dicionário contendo as propriedades recuperadas, ou None se houver erro.
    #     """
    #     url_request = f"{self.__BASE_URL}/pages/{page_id}/properties/{prop_id}"
    #     response = self.__request(url_request, "GET", body)

    #     if response is None:
    #         logger.error("Erro no retorno da API")
    #         return None

    #     if response["object"] != "list":
    #         return response

    #     results = {
    #         "list": response.get("results", []),
    #         "properties": response.get("property_item", {}),
    #     }

    #     if response["has_more"]:
    #         logger.debug(f"Next cursor at get_properties: {response['next_cursor']}")
    #         body = {"start_cursor": response["next_cursor"]}
    #         result_hasMore = self.get_properties(page_id, prop_id, body)
    #         results["list"] = results["list"] + result_hasMore["list"]

    #     return results

    # def get_blocks_from_parent(self, block_id: str):
    #     """
    #     Recupera os blocos filhos de um bloco pai no Notion.

    #     Args:
    #         block_id (str): ID do bloco pai.

    #     Returns:
    #         list: Lista de dicionários representando os blocos filhos.
    #     """
    #     logger.debug(f"Getting blocks from parent {block_id}")

    #     url_request = f"{self.__BASE_URL}/blocks/{block_id}/children"
    #     response = self.__request(url_request, "GET")

    #     if response is None:
    #         return []

    #     block_list = []
    #     for block in response["results"]:
    #         block_dict = {"id": block["id"], "type": block["type"], "content": None}

    #         if block.get("has_children", False):
    #             logger.debug(f"Block {block['id']} has children")
    #             block_list = block_list + self.get_blocks_from_parent(block["id"])

    #         if block["type"] == "paragraph":
    #             block_content = block.get("paragraph", {}).get("rich_text", [{}])
    #             block_dict["content"] = (
    #                 block_content[0].get("plain_text", "")
    #                 if len(block_content) > 0
    #                 else ""
    #             )

    #         elif block["type"] == "heading_1":
    #             block_content = block.get("heading_1", {}).get("rich_text", [{}])
    #             block_dict["content"] = (
    #                 block_content[0].get("plain_text", "")
    #                 if len(block_content) > 0
    #                 else ""
    #             )

    #         elif block["type"] == "heading_2":
    #             block_content = block.get("heading_2", {}).get("rich_text", [{}])
    #             block_dict["content"] = (
    #                 block_content[0].get("plain_text", "")
    #                 if len(block_content) > 0
    #                 else ""
    #             )

    #         elif block["type"] == "heading_3":
    #             block_content = block.get("heading_3", {}).get("rich_text", [{}])
    #             block_dict["content"] = (
    #                 block_content[0].get("plain_text", "")
    #                 if len(block_content) > 0
    #                 else ""
    #             )

    #         elif block["type"] == "callout":
    #             block_content = block.get("callout", {}).get("rich_text", [{}])
    #             block_dict["content"] = (
    #                 block_content[0].get("plain_text", "")
    #                 if len(block_content) > 0
    #                 else ""
    #             )

    #         else:
    #             block_dict["content"] = block

    #         block_list.append(block_dict)

    #     logger.debug(f"Blocks returned: {block_list}")

    #     return block_list

    # def delete_block(self, block_id: str):
    #     """
    #     Deleta um bloco específico do Notion.

    #     Args:
    #         block_id (str): ID do bloco a ser deletado.

    #     Returns:
    #         dict: Resposta da API do Notion após a deleção do bloco.
    #     """
    #     url_request = f"{self.__BASE_URL}/blocks/{block_id}"

    #     response = self.__request(url_request, "DELETE")

    #     return response

    # # def get_tarefas_from_project_id(self, notionPage: NotionPage):
    # #     """
    # #     Recupera tarefas associadas a um projeto específico.

    # #     Args:
    # #         notionPage (NotionPage): Objeto representando o projeto.

    # #     Returns:
    # #         list: Lista de objetos NotionTarefaDTO representando as tarefas do projeto.
    # #     """
    # #     logger.debug("Start get tarefas by Project id")

    # #     result = self.get_database(
    # #         CONST_NOTION.NOTION_ID_DATABASE["tarefas"],
    # #         body={
    # #             "filter": {
    # #                 "property": "Projetos",
    # #                 "relation": {"contains": notionPage.id},
    # #             },
    # #             "sorts": [{"property": "Início", "direction": "ascending"}],
    # #         },
    # #     )

    # #     list_tarefas = []
    # #     logger.debug(f"Number of tarefas: {len(result)}")
    # #     if len(result) > 0:
    # #         for tarefa in result:
    # #             #tarefa_dto = NotionTarefaDTO(tarefa)
    # #             #list_tarefas.append(tarefa_dto)

    # #     return list_tarefas
