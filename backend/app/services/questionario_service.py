"""
Serviço de scoring do questionário de triagem InformaSaúde.

Cada pergunta pertence a uma jornada. Cada opção dá 1–4 pontos àquela jornada.
A jornada com MAIOR pontuação total é a recomendada (estilo Duolingo).

ATENÇÃO: o conteúdo das perguntas (titulo, subtitulo, opcoes.titulo, opcoes.descricao)
deve ser atualizado pelo time — apenas o scoring (pontos) é fixo aqui.
O array PERGUNTAS também é exportado para que o frontend possa consumi-lo via
GET /api/questionario/perguntas, caso queiram centralizar no backend.
"""

PERGUNTAS = [
    # ── JORNADA CARDÍACA (Q1–Q3) ─────────────────────────────────────────────
    {
        "id": "1",
        "jornada": "cardiaca",
        "titulo": "Pergunta 1 — Cardíaca",  # TODO: substituir pelo texto real
        "subtitulo": "Selecione a opção que melhor descreve sua situação",
        "opcoes": [
            {"id": "a", "titulo": "Opção A", "descricao": "...", "pontos": {"cardiaca": 1}},
            {"id": "b", "titulo": "Opção B", "descricao": "...", "pontos": {"cardiaca": 2}},
            {"id": "c", "titulo": "Opção C", "descricao": "...", "pontos": {"cardiaca": 3}},
            {"id": "d", "titulo": "Opção D", "descricao": "...", "pontos": {"cardiaca": 4}},
        ],
    },
    {
        "id": "2",
        "jornada": "cardiaca",
        "titulo": "Pergunta 2 — Cardíaca",
        "subtitulo": "Selecione a opção que melhor descreve sua situação",
        "opcoes": [
            {"id": "a", "titulo": "Opção A", "descricao": "...", "pontos": {"cardiaca": 1}},
            {"id": "b", "titulo": "Opção B", "descricao": "...", "pontos": {"cardiaca": 2}},
            {"id": "c", "titulo": "Opção C", "descricao": "...", "pontos": {"cardiaca": 3}},
            {"id": "d", "titulo": "Opção D", "descricao": "...", "pontos": {"cardiaca": 4}},
        ],
    },
    {
        "id": "3",
        "jornada": "cardiaca",
        "titulo": "Pergunta 3 — Cardíaca",
        "subtitulo": "Selecione a opção que melhor descreve sua situação",
        "opcoes": [
            {"id": "a", "titulo": "Opção A", "descricao": "...", "pontos": {"cardiaca": 1}},
            {"id": "b", "titulo": "Opção B", "descricao": "...", "pontos": {"cardiaca": 2}},
            {"id": "c", "titulo": "Opção C", "descricao": "...", "pontos": {"cardiaca": 3}},
            {"id": "d", "titulo": "Opção D", "descricao": "...", "pontos": {"cardiaca": 4}},
        ],
    },
    # ── JORNADA DO SONO (Q4–Q6) ──────────────────────────────────────────────
    {
        "id": "4",
        "jornada": "sono",
        "titulo": "Pergunta 4 — Sono",
        "subtitulo": "Selecione a opção que melhor descreve sua situação",
        "opcoes": [
            {"id": "a", "titulo": "Opção A", "descricao": "...", "pontos": {"sono": 1}},
            {"id": "b", "titulo": "Opção B", "descricao": "...", "pontos": {"sono": 2}},
            {"id": "c", "titulo": "Opção C", "descricao": "...", "pontos": {"sono": 3}},
            {"id": "d", "titulo": "Opção D", "descricao": "...", "pontos": {"sono": 4}},
        ],
    },
    {
        "id": "5",
        "jornada": "sono",
        "titulo": "Pergunta 5 — Sono",
        "subtitulo": "Selecione a opção que melhor descreve sua situação",
        "opcoes": [
            {"id": "a", "titulo": "Opção A", "descricao": "...", "pontos": {"sono": 1}},
            {"id": "b", "titulo": "Opção B", "descricao": "...", "pontos": {"sono": 2}},
            {"id": "c", "titulo": "Opção C", "descricao": "...", "pontos": {"sono": 3}},
            {"id": "d", "titulo": "Opção D", "descricao": "...", "pontos": {"sono": 4}},
        ],
    },
    {
        "id": "6",
        "jornada": "sono",
        "titulo": "Pergunta 6 — Sono",
        "subtitulo": "Selecione a opção que melhor descreve sua situação",
        "opcoes": [
            {"id": "a", "titulo": "Opção A", "descricao": "...", "pontos": {"sono": 1}},
            {"id": "b", "titulo": "Opção B", "descricao": "...", "pontos": {"sono": 2}},
            {"id": "c", "titulo": "Opção C", "descricao": "...", "pontos": {"sono": 3}},
            {"id": "d", "titulo": "Opção D", "descricao": "...", "pontos": {"sono": 4}},
        ],
    },
    # ── JORNADA RESPIRATÓRIA (Q7–Q9) ─────────────────────────────────────────
    {
        "id": "7",
        "jornada": "respiratoria",
        "titulo": "Pergunta 7 — Respiratória",
        "subtitulo": "Selecione a opção que melhor descreve sua situação",
        "opcoes": [
            {"id": "a", "titulo": "Opção A", "descricao": "...", "pontos": {"respiratoria": 1}},
            {"id": "b", "titulo": "Opção B", "descricao": "...", "pontos": {"respiratoria": 2}},
            {"id": "c", "titulo": "Opção C", "descricao": "...", "pontos": {"respiratoria": 3}},
            {"id": "d", "titulo": "Opção D", "descricao": "...", "pontos": {"respiratoria": 4}},
        ],
    },
    {
        "id": "8",
        "jornada": "respiratoria",
        "titulo": "Pergunta 8 — Respiratória",
        "subtitulo": "Selecione a opção que melhor descreve sua situação",
        "opcoes": [
            {"id": "a", "titulo": "Opção A", "descricao": "...", "pontos": {"respiratoria": 1}},
            {"id": "b", "titulo": "Opção B", "descricao": "...", "pontos": {"respiratoria": 2}},
            {"id": "c", "titulo": "Opção C", "descricao": "...", "pontos": {"respiratoria": 3}},
            {"id": "d", "titulo": "Opção D", "descricao": "...", "pontos": {"respiratoria": 4}},
        ],
    },
    {
        "id": "9",
        "jornada": "respiratoria",
        "titulo": "Pergunta 9 — Respiratória",
        "subtitulo": "Selecione a opção que melhor descreve sua situação",
        "opcoes": [
            {"id": "a", "titulo": "Opção A", "descricao": "...", "pontos": {"respiratoria": 1}},
            {"id": "b", "titulo": "Opção B", "descricao": "...", "pontos": {"respiratoria": 2}},
            {"id": "c", "titulo": "Opção C", "descricao": "...", "pontos": {"respiratoria": 3}},
            {"id": "d", "titulo": "Opção D", "descricao": "...", "pontos": {"respiratoria": 4}},
        ],
    },
]

# Índice rápido: pergunta_id → {opcao_id → pontos}
_INDICE: dict[str, dict[str, dict[str, int]]] = {
    p["id"]: {op["id"]: op["pontos"] for op in p["opcoes"]} for p in PERGUNTAS
}

JORNADAS = ["cardiaca", "sono", "respiratoria"]

# Prioridade de desempate (mais urgente ganha em caso de empate)
_PRIORIDADE_EMPATE = {"cardiaca": 3, "respiratoria": 2, "sono": 1}


def calcular_resultado(respostas: dict[str, str]) -> dict:
    """
    Recebe {pergunta_id: opcao_id} e retorna o resultado com pontuação e
    jornada recomendada.

    Raises:
        ValueError: se houver pergunta ausente, pergunta desconhecida ou opção inválida.
    """
    perguntas_esperadas = {p["id"] for p in PERGUNTAS}
    perguntas_ausentes = perguntas_esperadas - respostas.keys()
    if perguntas_ausentes:
        ausentes = ", ".join(sorted(perguntas_ausentes, key=int))
        raise ValueError(f"Respostas incompletas. Perguntas não respondidas: {ausentes}.")

    pontuacao: dict[str, int] = {j: 0 for j in JORNADAS}
    empate = False

    for pergunta_id, opcao_id in respostas.items():
        if pergunta_id not in _INDICE:
            raise ValueError(f"Pergunta '{pergunta_id}' não encontrada.")
        opcoes_da_pergunta = _INDICE[pergunta_id]
        if opcao_id not in opcoes_da_pergunta:
            raise ValueError(
                f"Opção '{opcao_id}' inválida para pergunta '{pergunta_id}'."
            )
        for jornada, pts in opcoes_da_pergunta[opcao_id].items():
            pontuacao[jornada] = pontuacao.get(jornada, 0) + pts

    score_maximo = max(pontuacao.values())
    vencedoras = [j for j, s in pontuacao.items() if s == score_maximo]

    if len(vencedoras) > 1:
        empate = True
        # Desempate por prioridade clínica definida em _PRIORIDADE_EMPATE
        jornada_recomendada = max(vencedoras, key=lambda j: _PRIORIDADE_EMPATE[j])
    else:
        jornada_recomendada = vencedoras[0]

    mensagem = _gerar_mensagem(jornada_recomendada)

    return {
        "jornada_recomendada": jornada_recomendada,
        "pontuacao": pontuacao,
        "empate": empate,
        "mensagem": mensagem,
    }


def _gerar_mensagem(jornada: str) -> str:
    mensagens = {
        "cardiaca": (
            "Com base nas suas respostas, a Jornada Cardíaca é a mais indicada "
            "para você. Vamos juntos cuidar da sua saúde cardiovascular! 💚"
        ),
        "sono": (
            "Com base nas suas respostas, a Jornada do Sono é a mais indicada "
            "para você. Um bom descanso transforma tudo! 💚"
        ),
        "respiratoria": (
            "Com base nas suas respostas, a Jornada Respiratória é a mais indicada "
            "para você. Respire bem e viva melhor! 💚"
        ),
    }
    return mensagens.get(jornada, "Jornada recomendada com sucesso! 💚")
