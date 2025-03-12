import random


def get_random_animal_names():
    nome = [
        "Abóbora",
        "Aipo",
        "Amora",
        "Anjo",
        "Aveia",
        "Biscoito",
        "Bolota",
        "Brisa",
        "Broto",
        "Cacau",
        "Café",
        "Caramelo",
        "Cereja",
        "Chiclete",
        "Choco",
        "Chuvisco",
        "Coco",
        "Confete",
        "Cookie",
        "Creme",
        "Cristal",
        "Cupcake",
        "Doce",
        "Especiaria",
        "Estrela",
        "Floco",
        "Flor",
        "Frappé",
        "Fruta",
        "Fuji",
        "Ginger",
        "Gota",
        "Kiwi",
        "Jujuba",
        "Lámen",
        "Leite",
        "Lilás",
        "Limão",
        "Lua",
        "Macarrão",
        "Macaron",
        "Magia",
        "Manga",
        "Manhã",
        "Marzipan",
        "Mel",
        "Menta",
        "Mimosa",
        "Mocha",
        "Mochi",
        "Muffin",
        "Néctar",
        "Nozes",
        "Nugget",
        "Oliva",
        "Onda",
        "Orvalho",
        "Panqueca",
        "Pastel",
        "Pêssego",
        "Pirulito",
        "Pipoca",
        "Pistache",
        "Pitaya",
        "Pizza",
        "PomPom",
        "Pingo",
        "Pudim",
        "Queijo",
        "Quindim",
        "Rainbow",
        "Raio",
        "Rosquinha",
        "Rubi",
        "Sal",
        "Semente",
        "Sol",
        "Soneca",
        "Sorvete",
        "Sprite",
        "Sushi",
        "Suspiro",
        "Tangerina",
        "Tapioca",
        "Telha",
        "Tempo",
        "Terra",
        "Torta",
        "Trança",
        "Trigo",
        "Trix",
        "Trufa",
        "Tuíte",
        "Uva",
        "Ursinho",
        "Vanilla",
        "Verão",
        "Vida",
        "Waffle",
        "Zafira",
    ]

    sobrenome = [
        "Amarelo",
        "Azul",
        "Branco",
        "Caramelo",
        "Cereja",
        "Chocolate",
        "Coco",
        "Dourado",
        "Flocos",
        "Gelado",
        "Laranja",
        "Lilás",
        "Menta",
        "Morango",
        "Neve",
        "Pêssego",
        "Rosa",
        "Roxo",
        "Verde",
        "Vermelho",
        "Lambeijos",
        "Fofurildes",
        "Ronronildo",
        "Biscoitinho",
        "Amorzístico",
        "Cosquinhento",
        "Denguinho Feliz",
        "Mimozildo",
        "Chameguinho",
        "Beijoca Doce",
        "Gostosuras",
        "Sonequinha Paz",
        "Travessildo",
        "Risadinha Sol",
        "Cacarejildo",
        "Bolotinha Amor",
        "Cotonete Fofo",
        "Flocosinho Alegre",
        "Jujubinha Doce",
        "Suspirinho Paz",
        "Tutu Delícia",
        "Xuxuzinho Bom",
        "Zezinho Esperto",
        "Lelé Travesso",
        "Bubu Feliz",
        "Lala Dengosa",
        "Dudu Amigo",
        "Tete Carinhoso",
        "Nenenzinho Lindo",
        "Anjinho Bom",
        "Queridinho Doce",
        "Fofucho Paz",
        "Espertildo Feliz",
        "Felpudo Amor",
        "Mimoso Doce",
        "Risonho Bom",
        "Amigão Paz",
        "Lealzinho Feliz",
        "Bravinho Amor",
        "Bocejo Barulhento",
        "Tropeção Elegante",
        "Esquecido Distraído",
        "Comilão Faminto",
        "Dançarino Desengonçado",
        "Cantor Desafinado",
        "Dorminhoco Profissional",
        "Fugitivo Desastrado",
        "Perdido Confuso",
        "Gritador Exagerado",
        "Chorão Dramático",
        "Assustado Covarde",
        "Atrapalhado Desajeitado",
        "Teimoso Irredutível",
        "Curioso Intrometido",
        "Bagunceiro Destruidor",
        "Mimado Insaciável",
        "Preocupado Neurótico",
        "Indeciso Enrolado",
        "Arrogante Presunçoso",
        "Invejoso Rancoroso",
        "Mentiroso Compulsivo",
        "Grosseiro Mal-Educado",
        "Egoísta Mesquinho",
        "Critico Implacável",
        "Resmungão Insatisfeito",
        "Desconfiado Paranoico",
        "Ansioso Inquieto",
        "Reclamão Crônico",
        "Entediado Apático",
        "Iludido Ingenuo",
        "Desmotivado Desanimado",
        "Frustrado Revoltado",
        "Carente Pegajoso",
        "Meloso Enjoativo",
        "Pegajoso Grudento",
        "Exibido Vanglorioso",
        "Competitivo Desleal",
        "Inseguro Vulnerável",
        "Inconstante Volúvel",
        "Distraído Aéreo",
        "Lento Tartaruga",
        "Rápido Furacão",
        "Alto Gigante",
        "Baixo Anão",
        "Grande Elefante",
        "Pequeno Formiga",
        "Forte Leão",
        "Fraco Rato",
        "Lindo Pavão",
        "Feio Urubu",
        "Bom Cordeiro",
        "Mau Lobo",
        "Feliz Esquilo",
        "Triste Coruja",
        "Bravo Touro",
        "Calmo Bicho-Preguiça",
        "Tímido Coelho",
        "Ousado Tigre",
        "Gentil Borboleta",
        "Grosso Rinoceronte",
        "Inteligente Golfinho",
        "Burro Jumento",
        "Preguiçoso Verme",
        "Trabalhador Abelha",
        "Alegre Macaco",
        "Sério Pinguim",
        "Engraçado Hiena",
        "Chato Caracol",
        "Novo Pintinho",
        "Velho Jabuti",
        "Jovem Cabrito",
        "Idoso Búfalo",
        "Rico Ganso",
        "Pobre Pombo",
        "Bonito Beija-Flor",
        "Esquisito Ornitorrinco",
        "Normal Vaca",
        "Diferente Camaleão",
        "Comum Galinha",
        "Estranho Kiwi",
        "Peludinho Quentinho",
        "Bochechudo Rosado",
        "Cílios Longos",
        "Umbigo Redondo",
        "Sobrancelha Curva",
        "Cabelo Macio",
        "Dedo Pequeno",
        "Braço Forte",
        "Perna Curta",
        "Pescoço Longo",
        "Testa Lisa",
        "Queixo Fino",
        "Costas Largas",
        "Barriga Cheia",
        "Quadril Estreito",
        "Coxa Grossa",
        "Canela Fina",
        "Calcanhar Duro",
        "Pé Chato",
        "Joelho Velho",
        "Cérebro Lento",
        "Coração Grande",
        "Pulmão Forte",
        "Fígado Cansado",
        "Rim Doente",
        "Estômago Vazio",
        "Intestino Irritado",
        "Osso Frágil",
        "Músculo Tenso",
        "Pele Sensível",
        "Unha Quebrada",
        "Sangue Quente",
        "Lágrima Salgada",
        "Suor Frio",
        "Arroto Alto",
        "Tosse Seca",
        "Espirro Forte",
        "Soluço Chato",
        "Coceira Irritante",
        "Dor Insistente",
        "Medo Bobo",
        "Raiva Cega",
        "Ódio Injusto",
        "Inveja Ruim",
        "Cobiça Insaciável",
        "Avareza Mesquinha",
        "Gula Voraz",
        "Luxúria Desenfreada",
        "Ira Explosiva",
        "Preguiça Crônica",
        "Vaidade Vã",
        "Inocência Perdida",
        "Pureza Maculada",
        "Fé Inabalável",
        "Esperança Renascida",
        "Caridade Verdadeira",
        "Justiça Imparcial",
        "Paz Interior",
        "Amor Eterno",
        "Sabedoria Divina",
        "Humildade Genuína",
        "Coragem Audaz",
        "Lealdade Incondicional",
    ]

    return f"{random.choice(nome)} {random.choice(sobrenome)}"
