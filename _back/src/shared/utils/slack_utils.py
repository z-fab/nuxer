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


def text_to_blocks(text: str) -> list:
    blocks = []
    for line in text.splitlines():
        line = line.strip()
        struct = {}

        if re.match(r"^--$", line):
            # Divider
            struct = {"type": "divider"}
        elif header_match := re.match(r"^#\s*(.*)$", line):
            # Header
            struct = {
                "type": "header",
                "text": {"type": "plain_text", "text": header_match.group(1)},
            }
        elif context_match := re.match(r"^:\s*(.*)$", line):
            # Context
            struct = {
                "type": "context",
                "elements": [{"type": "mrkdwn", "text": context_match.group(1)}],
            }
        # Nova condição para linhas com o formato "texto || <botão>"
        elif section_button_match := re.match(r"^(.*?)\s*\|\|\s*<([^(]+)\(([^)]+)\)(\[([^\]]+)\])?(P|D)?>$", line):
            # Section com botão como accessory
            section_text = section_button_match.group(1).strip()
            button_label = section_button_match.group(2)
            action_id = section_button_match.group(3)
            params_str = section_button_match.group(5) if section_button_match.group(5) else None
            is_primary = section_button_match.group(6) == "P" if section_button_match.group(6) else False
            is_danger = section_button_match.group(6) == "D" if section_button_match.group(6) else False

            button = {
                "type": "button",
                "text": {"type": "plain_text", "text": button_label},
                "action_id": action_id,
            }

            if params_str:
                params = dict(param.split("=") for param in params_str.split(","))
                button["value"] = json.dumps(params)

            if is_primary:
                button["style"] = "primary"
            elif is_danger:
                button["style"] = "danger"

            struct = {"type": "section", "text": {"type": "mrkdwn", "text": section_text}, "accessory": button}
        elif re.search(r"<([^(]+)\(([^)]+)\)(\[([^\]]+)\])?(P|D)?>", line):
            # Buttons <label(action_id)[params]P> - multiple allowed in one line, P for primary style
            button_matches = re.findall(r"<([^(]+)\(([^)]+)\)(\[([^\]]+)\])?(P|D)?>", line)
            buttons = []

            for i, match in enumerate(button_matches):
                label = match[0]
                action_id = match[1]
                params_str = match[3] if len(match) > 2 and match[3] else None
                is_primary = match[4] == "P" if len(match) > 4 else False
                is_danger = match[4] == "D" if len(match) > 4 else False

                button = {
                    "type": "button",
                    "text": {"type": "plain_text", "text": label},
                    "action_id": f"{action_id}_{i}",
                }

                if params_str:
                    params = dict(param.split("=") for param in params_str.split(","))
                    button["value"] = json.dumps(params)

                if is_primary:
                    button["style"] = "primary"
                elif is_danger:
                    button["style"] = "danger"

                buttons.append(button)

            struct = {"type": "actions", "elements": buttons}

        elif line == ".":
            struct = {"type": "section", "text": {"type": "mrkdwn", "text": " "}}

        elif line:
            # Section (for non-empty lines)
            struct = {"type": "section", "text": {"type": "mrkdwn", "text": line}}

        if struct:
            blocks.append(struct)

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
