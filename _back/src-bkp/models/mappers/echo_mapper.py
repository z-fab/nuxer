from models.entities.echo_entity import EchoEntity


class EchoMapper:
    @staticmethod
    def notion_to_entity(json_dict: dict) -> EchoEntity:

        # Properties
        properties = json_dict.get("properties", {})

        # Cod Echo
        cod_echo = properties.get("Cod", {}).get("unique_id", {}).get("number", "")


        # Titulo
        titulo_list = properties.get("Título", {}).get("title", [{}])
        titulo_str = ""
        for titulo in titulo_list:
            titulo_str += titulo.get("plain_text", "")

        # Descrição
        descricao_list = properties.get("Descrição", {}).get("rich_text", [{}])
        descricao_str = ""
        for descricao in descricao_list:
            descricao_str += descricao.get("plain_text", "")

        # # Criado em
        # criado_em = properties.get("Criado em", {}).get("created_time")
        # if criado_em:
        #     criado_em = notion_utils.notion_time_to_datetime(criado_em)

        # # Criado por
        # criado_por = (
        #     properties.get("Criado por", {}).get("created_by", {}).get("id", "")
        # )
        # criado_por = users_r.get_users_by_notion_id(criado_por.replace("-", ""))
        # criado_por = criado_por[0] if criado_por else None

        # Artefato
        file_url = properties.get("Arquivo", {}).get("files", [])
        if len(file_url) > 0:
            file_url = file_url[0].get("file", {}).get("url", "")
            #artefato_path = general_utils.download_image(artefato_url)
        else:
            artefato_path = None

        return EchoEntity(
            cod = cod_echo,
            situacao = "",
            titulo = titulo_str,
            descricao = descricao_str,
            file_url = file_url,
            tags = [""],
            criado_em = None,
            criado_por = None
        )