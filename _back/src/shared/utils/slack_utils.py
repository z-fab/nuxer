import json
import random
import re


def extract_command(text):
    pattern = r"!(\w+)(?:\s+(.+))?"
    search = re.search(pattern, text)
    command = ""
    params = []
    if search:
        command = search.group(1)
        if search.group(2):
            # Expressão regular melhorada para capturar todos os tipos de parâmetros
            params = re.findall(r'([\'"“”][^\'"“”]*[\'"“”]|\S+)', search.group(2))
            params = [param.strip('"') for param in params]

    return command.lower(), params


def _parse_select_options(options_str: str) -> list:
    """Converte a string de opções de um select para o formato de lista de dicionários."""
    options = []
    if options_str:
        for option_pair in options_str.split(","):
            text_val = option_pair.split("=")
            if len(text_val) == 2:
                options.append(
                    {
                        "text": {"type": "plain_text", "text": text_val[0].strip(), "emoji": True},
                        "value": text_val[1].strip(),
                    }
                )
            else:
                # Log ou tratamento para opção malformada, se necessário
                print(f"Aviso: Par de opção de select malformado ignorado: '{option_pair}'")
    return options


def _parse_button_params(params_str: str | None) -> str | None:
    """Converte a string de parâmetros de um botão para JSON string."""
    if params_str:
        params = dict(param.split("=") for param in params_str.split(","))
        return json.dumps(params)
    return None


def _create_button_element(label: str, action_id: str, params_str: str | None, style_char: str | None) -> dict:
    """Cria a estrutura de um elemento de botão."""
    button = {
        "type": "button",
        "text": {"type": "plain_text", "text": label, "emoji": True},
        "action_id": action_id,
    }
    button_value = _parse_button_params(params_str)
    if button_value:
        button["value"] = button_value

    if style_char == "P":
        button["style"] = "primary"
    elif style_char == "D":
        button["style"] = "danger"
    return button


def _create_static_select_element(placeholder: str, action_id: str, options_str: str) -> dict:
    """Cria a estrutura de um elemento static_select."""
    return {
        "type": "static_select",
        "placeholder": {"type": "plain_text", "text": placeholder, "emoji": True},
        "action_id": action_id,
        "options": _parse_select_options(options_str),
    }


def text_to_blocks(text: str) -> list:
    """
    Converte uma string de texto formatada em uma lista de blocos Slack.
    Suporta: dividers, headers, context, sections com texto, botões, selects e imagens.
    """
    blocks = []
    for line_number, raw_line in enumerate(text.splitlines(), 1):
        line = raw_line.strip()
        struct = {}

        # 1. Divider (--)
        if re.fullmatch(r"--", line):
            struct = {"type": "divider"}

        # 2. Header (# Texto do Header)
        elif header_match := re.fullmatch(r"#\s*(.*)", line):
            struct = {
                "type": "header",
                "text": {"type": "plain_text", "text": header_match.group(1).strip(), "emoji": True},
            }

        # 3. Context (: Texto do Contexto <img url>)
        elif context_match := re.fullmatch(r":\s*(.*)", line):
            context_content = context_match.group(1).strip()
            elements = []
            # Divide o conteúdo mantendo os delimitadores de imagem
            parts = re.split(r"(<img\s+[^>]+>)", context_content)
            for part in parts:
                img_tag_match = re.fullmatch(r"<img\s+([^>]+)>", part.strip())
                if img_tag_match:
                    img_url = img_tag_match.group(1).strip()
                    elements.append({"type": "image", "image_url": img_url, "alt_text": "imagem"})
                elif part.strip():  # Adiciona texto apenas se não for vazio
                    elements.append({"type": "mrkdwn", "text": part.strip()})
            if elements:  # Adiciona o bloco de contexto apenas se houver elementos
                struct = {"type": "context", "elements": elements}

        # 4. Section com Accessory (Texto || <Botão> ou Texto || SELECT<...> ou Texto || <img ...>)
        elif accessory_line_match := re.fullmatch(r"(.*?)\s*\|\|\s*(.+)", line):
            section_text_content = accessory_line_match.group(1).strip()
            accessory_content_str = accessory_line_match.group(2).strip()
            accessory_obj = None

            # 4a. Botão como Accessory: <label(action_id)[params]P/D>
            if btn_accessory_match := re.fullmatch(
                r"<([^(]+)\(([^)]+)\)(\[([^\]]+)\])?([PD]?)>", accessory_content_str
            ):
                label, action_id, _, params_str, style_char = btn_accessory_match.groups()
                accessory_obj = _create_button_element(label, action_id, params_str, style_char)

            # 4b. Imagem como Accessory: <img url>
            elif img_accessory_match := re.fullmatch(r"<img\s+([^>]+)>", accessory_content_str):
                img_url = img_accessory_match.group(1).strip()
                accessory_obj = {"type": "image", "image_url": img_url, "alt_text": "imagem"}

            # 4c. Select como Accessory: SELECT<Placeholder(action_id)[options]>
            elif select_accessory_match := re.fullmatch(
                r"SELECT<([^)]+)\(([^)]+)\)\[([^\]]+)\]>", accessory_content_str
            ):
                placeholder, action_id, options_str = select_accessory_match.groups()
                accessory_obj = _create_static_select_element(placeholder, action_id, options_str)

            if accessory_obj:
                struct = {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": section_text_content if section_text_content else " "},
                    "accessory": accessory_obj,
                }
            else:  # Fallback: se o acessório não for reconhecido, trata a linha inteira como texto
                struct = {"type": "section", "text": {"type": "mrkdwn", "text": line}}

        # 5. Standalone Select (SELECT<Placeholder(action_id)[options]>)
        elif standalone_select_match := re.fullmatch(r"SELECT<([^)]+)\(([^)]+)\)\[([^\]]+)\]>", line):
            placeholder, action_id, options_str = standalone_select_match.groups()
            struct = {
                "type": "actions",
                "elements": [_create_static_select_element(placeholder, action_id, options_str)],
            }

        # 6. Standalone Buttons (<label(action_id)[params]P/D> ...)
        # Esta regex garante que a linha inteira seja composta por um ou mais botões.
        elif re.fullmatch(r"(\s*<([^(]+)\(([^)]+)\)(\[([^\]]+)\])?([PD]?)>\s*)+", line):
            # Encontra todos os botões individuais na linha
            button_captures = re.findall(r"<([^(]+)\(([^)]+)\)(\[([^\]]+)\])?([PD]?)>", line)
            buttons_elements = []
            for i, capture in enumerate(button_captures):
                label, action_id, _, params_str, style_char = capture
                # Garante um action_id único se houver múltiplos botões, embora o action_id original já deva ser único.
                # Se a intenção é que o action_id seja o mesmo para todos os botões na linha de actions, remova o _i.
                buttons_elements.append(_create_button_element(label, f"{action_id}_{i}", params_str, style_char))

            if buttons_elements:
                struct = {"type": "actions", "elements": buttons_elements}

        # 7. Linha de placeholder para espaço (.)
        elif line == ".":
            struct = {"type": "section", "text": {"type": "mrkdwn", "text": " "}}

        # 8. Linha de texto comum (Section)
        elif line:  # Se a linha não estiver vazia e não corresponder a nenhum padrão anterior
            struct = {"type": "section", "text": {"type": "mrkdwn", "text": line}}

        if struct:
            blocks.append(struct)
        elif line:  # Se a linha não foi processada mas não está vazia, logar um aviso
            print(f"Aviso: Linha {line_number} não reconhecida e ignorada: '{raw_line}'")

    return blocks


def get_random_saudacao(name: str = "Humano"):
    saudacoes = [
        "Hey, {nome}! Como você está hoje?",
        "Ei, {nome}! Que alegria te ver. Como vão as coisas?",
        "Oi, {nome}! Espero que seu dia esteja indo bem. Tudo certo por aí?",
        "Olá, {nome}! Como você está se sentindo hoje?",
        "Fala, {nome}! Como está sendo o seu dia até agora?",
        "Saudações, {nome}! Como tem passado?",
        "Opa, {nome}! Tudo tranquilo por aí?",
        "E aí, {nome}, tudo em cima?",
        "Olá, {nome}! Como está o seu ânimo hoje?",
        "Oi, {nome}! Alguma novidade por aí?",
        "Ei, {nome}, tudo bem? Como foi o seu dia?",
        "Olá, {nome}! Pronto para uma nova aventura hoje?",
        "Bom te ver, {nome}! Como você está se sentindo?",
        "Fala, {nome}! Tudo bem por aí? Alguma novidade?",
        "Oi, {nome}! Como está seu coração hoje?",
        "Olá, {nome}, tudo certo? Como está indo a semana?",
        "E aí, {nome}! Tudo bem? Pronto para os desafios de hoje?",
        "Oi, {nome}! Como você está se saindo hoje?",
        "Saudações, {nome}! Pronto para um dia incrível?",
        "Olá, {nome}! Espero que esteja com o ânimo lá em cima. Como vai?",
        "Hey, {nome}! Espero que esteja tendo um ótimo começo de dia.",
        "Oi, {nome}! Como tem sido seu dia até agora?",
        "Salve, {nome}! O que você tem feito de bom hoje?",
        "E aí, {nome}! Que tal compartilhar algo novo que aconteceu recentemente?",
        "Olá, {nome}! Está preparado para as surpresas que o dia pode trazer?",
        "Oi, {nome}! Como tem lidado com os desafios do dia?",
        "Fala, {nome}! Alguma história interessante para contar hoje?",
        "Saudações, {nome}! O que tem feito seu coração feliz ultimamente?",
        "Oi, {nome}! Como você está se sentindo em relação ao dia?",
        "Bom te ver, {nome}! Que alegria saber de você hoje.",
        "Olá, {nome}! Como anda sua energia hoje?",
        "Oi, {nome}! Alguma boa nova para compartilhar?",
        "Fala, {nome}! Estou curioso, como foi o seu final de semana?",
        "Olá, {nome}! O dia está favorável para boas conversas, não acha?",
        "E aí, {nome}! Pronto para encarar o que o dia trouxer?",
        "Oi, {nome}! Espero que seu dia esteja cheio de boas vibrações.",
        "Saudações, {nome}! Como você tem se divertido ultimamente?",
        "Hey, {nome}! Vamos fazer deste dia algo especial?",
        "Olá, {nome}! Que tal um café virtual para começar bem o dia?",
        "Oi, {nome}! Espero que esteja cercado de boas energias hoje.",
        "Hey, {nome}! Como você está se sentindo: mais para um super-herói ou para um despertador quebrado?",
        "E aí, {nome}! Se seu dia fosse um filme, seria uma comédia romântica ou uma tragédia hilária?",
        "Oi, {nome}! Você sabia que hoje é o dia perfeito para fazer algo inesperado? Como, por exemplo, fazer um cafezinho de cenoura?",  # noqa: E501
        "Saudações, {nome}! Se você pudesse ser qualquer coisa hoje, seria um lobo solitário ou um gato preguiçoso?",
        "Fala, {nome}! Espero que seu dia esteja mais doce que um brigadeiro derretido!",
        "Oi, {nome}! Como vai a vitória contra a preguiça hoje?",
        "E aí, {nome}! Se a vida te der limões, faça uma limonada... ou um mojito, porque não?",
        "Hey, {nome}! Lembre-se: hoje é um ótimo dia para realizar suas metas... ou apenas existir!",
        "Olá, {nome}! Preparado para mais um dia de desafios? Melhor estar de 'armadura'!",
        "Oi, {nome}! Espero que sua energia esteja mais alta que a conta do mês passado!",
        "Fala, {nome}! Você já se sentiu como um mistério sem solução? Hoje é o dia de desvendar isso!",
        "Oi, {nome}! Como está a batalha contra a monotonia? Usando poderes especiais hoje?",
        "Saudações, {nome}! Acordou mais para um 'detetive da soneca' ou para um 'explorador do sofá'?",
        "Hey, {nome}! Se você tivesse uma superpotência, seria a de encontrar remotamente as meias que sumiram?",
        "E aí, {nome}! Se hoje fosse um sorvete, que sabor você seria? 'Sabor energizante com cobertura de risadas'?",
        "Olá, {nome}! Espero que sua disposição esteja mais alta que a fila de filmes na Netflix!",
        "Oi, {nome}! Vamos fazer deste dia uma sequência de cenas hilárias!",
        "Fala, {nome}! Se você pudesse ser um personagem de desenho animado hoje, quem seria? O Pepe Le Pew talvez?",
        "Saudações, {nome}! Lembre-se: a vida é curta, mas seus sapatos podem ser confortáveis!",
        "Hey, {nome}! Vamos encarar hoje como um jogo de tabuleiro: se perder, ao menos divirta-se!",
        "E aí, {nome}! Espero que seu dia seja tão bom quanto descobrir que não precisa trabalhar no feriado!",
    ]

    return random.choice(saudacoes).format(nome=name)
