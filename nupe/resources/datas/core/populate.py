from datetime import date

academic_educations = [
    # EJA
    {
        "name": "Auxiliar Administrativo",
        "grade": "Educação de Jovens e Adultos",
        "campus_name": "São Francisco do Sul",
    },
    # Técnico
    {"name": "Agrimensura", "grade": "Técnico", "campus_name": "Araquari"},
    {"name": "Agropecuária", "grade": "Técnico", "campus_name": "Araquari"},
    {"name": "Informática", "grade": "Técnico", "campus_name": "Araquari"},
    {"name": "Química", "grade": "Técnico", "campus_name": "Araquari"},
    {"name": "Administração", "grade": "Técnico", "campus_name": "São Francisco do Sul"},
    {"name": "Automação Industrial", "grade": "Técnico", "campus_name": "São Francisco do Sul"},
    {"name": "Guia de Turismo", "grade": "Técnico", "campus_name": "São Francisco do Sul"},
    # Ensino Superior
    {"name": "Agronomia", "grade": "Bacharelado", "campus_name": "Araquari"},
    {"name": "Medicina Veterinária", "grade": "Bacharelado", "campus_name": "Araquari"},
    {"name": "Sistemas de Informação", "grade": "Bacharelado", "campus_name": "Araquari"},
    {"name": "Engenharia Elétrica", "grade": "Bacharelado", "campus_name": "São Francisco do Sul"},
    {"name": "Ciências Agrícolas", "grade": "Licenciatura", "campus_name": "Araquari"},
    {"name": "Química", "grade": "Licenciatura", "campus_name": "Araquari"},
    {"name": "Redes de Computadores", "grade": "Tecnologia", "campus_name": "Araquari"},
    {"name": "Logística", "grade": "Tecnologia", "campus_name": "São Francisco do Sul"},
    {"name": "Redes de Computadores", "grade": "Tecnologia", "campus_name": "São Francisco do Sul"},
    # Pós Graduação
    {"name": "Aquicultura", "grade": "Especialização", "campus_name": "Araquari"},
    {"name": "Educação Matemática", "grade": "Especialização", "campus_name": "Araquari"},
    {"name": "Produção e Sanidade Animal", "grade": "Mestrado", "campus_name": "Araquari"},
    {"name": "Tecnologia e Ambiente", "grade": "Mestrado", "campus_name": "Araquari"},
]

cities = [
    {"name": "Araquari", "state_initials": "SC"},
    {"name": "São Francisco do Sul", "state_initials": "SC"},
]

states = [
    {"name": "Santa Catarina", "initials": "SC"},
]

campi = [
    {
        "name": "Araquari",
        "cnpj": "10.635.424/0003-48",  # com ou sem pontuação
        "address": "Rodovia BR 280",
        "number": "km 27",
        "website": "https://araquari.ifc.edu.br/",
        "location": "Araquari - SC",  # cidade - sigla estado obrigatóriamente
        "institution": "Instituto Federal Catarinense",
    },
    {
        "name": "São Francisco do Sul",
        "cnpj": "10.635.424/0012-39",
        "address": "R. Rod. Duque de Caxias",
        "number": "6750",
        "website": "https://saofrancisco.ifc.edu.br/",
        "location": "São Francisco do Sul - SC",
        "institution": "Instituto Federal Catarinense",
    },
]

institutions = [
    {"name": "Instituto Federal Catarinense"},
]

sectors = [
    # Direção de Desenvolvimento Educacional - DDE
    {"name": "Assessor de Ensino"},
    {"name": "Secretaria Escolar e Acadêmica"},
    {"name": "Pesquisa Institucional"},
    {"name": "Coordenação PROEJA"},
    {"name": "Coordenação EAD"},
    {"name": "Coordenação Cursos de Qualificação"},
    {"name": "Núcleo Pedagógico"},
    {"name": "Biblioteca"},
    # Coordenação Geral de Ensino Técnico - CGT
    {"name": "Coordenação Técnico em Agropecuária"},
    {"name": "Coordenação Técnico em Informática"},
    {"name": "Coordenação Técnico em Química"},
    {"name": "Laboratório Química Geral"},
    {"name": "Laboratório de Química Orgânica"},
    {"name": "Laboratório de Química Analítica e Ambiental"},
    {"name": "Almoxarifado de Produtos Químicos"},
    {"name": "Laboratório de Artes"},
    {"name": "Laboratório de Agrimensura"},
    {"name": "Laboratório de Física"},
    {"name": "Laboratório de Biologia"},
    {"name": "Laboratório de Informática - B1"},
    {"name": "Laboratório de Informática - B2"},
    {"name": "Laboratório de Informática - B3"},
    {"name": "Laboratório de Informática - B4"},
    {"name": "Laboratório de Informática - B5"},
    {"name": "Laboratório de Informática - A11"},
    {"name": "Laboratório de Hardware"},
    {"name": "Laboratório de Aquicultura"},
    # Coordenação Geral de Graduação - CGG
    {"name": "Coordenação de Medicina Veterinária"},
    {"name": "Coordenação de Sistemas de Informação"},
    {"name": "Coordenação de Ciências Agrícolas"},
    {"name": "Coordenação de Química"},
    {"name": "Coordenação de Redes"},
    {"name": "Coordenação de Agronomia"},
    {"name": "Laboratório de Ensino e Diagnóstico Veterinário - Microscopia"},
    {"name": "Laboratório de Ensino e Diagnóstico Veterinário - Parasitologia"},
    {"name": "Laboratório de Ensino e Diagnóstico Veterinário - Microbiologia"},
    {"name": "Laboratório de Ensino e Diagnóstico Veterinário - Biologia Molecular"},
    {"name": "Laboratório de Anatomia"},
    {"name": "Laboratório de Patologia"},
    {"name": "Centro de Práticas Clínicas e Cirúrgicas Veterinárias"},
    {"name": "Laboratório Clínico"},
    {"name": "Diagnóstico por Imagem"},
    {"name": "Clínica Cirúrgica"},
    {"name": "Clínica Médica"},
    {"name": "Laboratório de Ensino e Aprendizagem"},
    {"name": "Laboratório de Ecotoxicologia e Fisiologia Veterinária"},
    {"name": "Laboratório de Engenharia Agrícola"},
    {"name": "Laboratório de Biologia e Genética de Organismos Aquáticos"},
    # Coordenação Geral de Assistência Estudantil
    {"name": "Moradia Estudantil"},
    {"name": "Coordenadoria-Geral de Assistência Estudantil"},
    # Coordenação de Pesquisa e Inovação
    {"name": "Coordenação de Pesquisa e Inovação"},
    # Coordenação de Extensão
    {"name": "Coordenação de Estágios e Egressos"},
]

functions = [
    {"name": "Coordenador(a)"},
    {"name": "Pedagoga(o)"},
    {"name": "Psicóloga(o)"},
    {"name": "Apoio Pedagógico"},
    {"name": "Enfermeira(o)"},
    {"name": "Chefia de Controles e Estrutura de Alimentação"},
    {"name": "Coordenadora e Assistente Social"},
]

attendance_reasons = [
    {"name": "Uso de Drogas", "sons": [{"name": "Maconha"}, {"name": "Cigarro"}, {"name": "Bebida Alcoólica"}]},
    {
        "name": "Necessidades Especiais",
        "sons": [{"name": "TDA"}, {"name": "TDAH"}, {"name": "Autismo"}, {"name": "Surdes"}],
    },
    {"name": "Crises", "sons": [{"name": "Ansiedade"}, {"name": "Pânico"}]},
    {
        "name": "Outros",
        "sons": [
            {"name": "Gazeando Aula"},
            {"name": "Desrespeitando o Professor"},
            {"name": "Briga"},
            {"name": "Excesso de Faltas"},
        ],
    },
]

persons = [
    {
        "first_name": "Luis Fernando",
        "last_name": "Carvalho",
        "cpf": "385.301.570-01",
        "birthday_date": date(year=1999, month=2, day=14),
        "gender": "M",
    },
    {
        "first_name": "Antonio",
        "last_name": "Fernandes",
        "cpf": "203.299.980-30",
        "birthday_date": date(year=1999, month=1, day=21),
        "gender": "M",
    },
    {
        "first_name": "Vitor Leonardo",
        "last_name": "Esser",
        "cpf": "921.549.040-09",
        "birthday_date": date(year=1999, month=9, day=28),
        "gender": "M",
    },
    {
        "first_name": "Fernanda",
        "last_name": "Strebe",
        "cpf": "271.603.800-70",
        "birthday_date": date(year=2000, month=4, day=8),
        "gender": "F",
    },
]

students = [
    {
        "registration": "2018014476",
        "cpf": "385.301.570-01",
        "academic_education_campus": "Sistemas de Informação - Araquari",
        "ingress_date": date(year=2018, month=2, day=27),
    },
    {
        "registration": "2018003436",
        "cpf": "203.299.980-30",
        "academic_education_campus": "Sistemas de Informação - Araquari",
        "ingress_date": date(year=2018, month=2, day=27),
    },
    {
        "registration": "2018014583",
        "cpf": "921.549.040-09",
        "academic_education_campus": "Sistemas de Informação - Araquari",
        "ingress_date": date(year=2018, month=2, day=27),
    },
    {
        "registration": "2018014387",
        "cpf": "271.603.800-70",
        "academic_education_campus": "Sistemas de Informação - Araquari",
        "ingress_date": date(year=2018, month=2, day=27),
    },
]

attendances = [
    {"attendance_reason": "TDAH", "attendance_severity": "M", "registration": "2018014476"},
    {"attendance_reason": "Excesso de Faltas", "attendance_severity": "H", "registration": "2018003436"},
    {"attendance_reason": "Maconha", "attendance_severity": "M", "registration": "2018014583"},
    {"attendance_reason": "Ansiedade", "attendance_severity": "L", "registration": "2018014387"},
]
