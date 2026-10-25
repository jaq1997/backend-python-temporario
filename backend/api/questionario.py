"""
Regras e scoring do questionário de triagem InformaSaúde.
Direciona para as 3 jornadas: "cardiaca", "sono" ou "respiratoria".
"""

PERGUNTAS = [
    # ── JORNADA CARDÍACA (Q1–Q3) ─────────────────────────────────────────────
    {
        "id": "1",
        "jornada": "cardiaca",
        "titulo": "Pergunta 1 — Cardíaca",
        "subtitulo": "Selecione a opção que melhor descreve sua rotina ou sintomas",
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
        "subtitulo": "Selecione a opção que melhor descreve sua rotina ou sintomas",
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
        "subtitulo": "Selecione a opção que melhor descreve sua rotina ou sintomas",
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
        "subtitulo": "Selecione a opção que melhor descreve sua rotina ou sintomas",
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
        "subtitulo": "Selecione a opção que melhor descreve sua rotina ou sintomas",
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
        "subtitulo": "Selecione a opção que melhor descreve sua rotina ou sintomas",
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
        "subtitulo": "Selecione a opção que melhor descreve sua rotina ou sintomas",
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
        "subtitulo": "Selecione a opção que melhor descreve sua rotina ou sintomas",
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
        "subtitulo": "Selecione a opção que melhor descreve sua rotina ou sintomas",
        "opcoes": [
            {"id": "a", "titulo": "Opção A", "descricao": "...", "pontos": {"respiratoria": 1}},
            {"id": "b", "titulo": "Opção B", "descricao": "...", "pontos": {"respiratoria": 2}},
            {"id": "c", "titulo": "Opção C", "descricao": "...", "pontos": {"respiratoria": 3}},
            {"id": "d", "titulo": "Opção D", "descricao": "...", "pontos": {"respiratoria": 4}},
        ],
    },
]

_INDICE = {
    p["id"]: {op["id"]: op["pontos"] for op in p["opcoes"]} for p in PERGUNTAS
}

JORNADAS = ["cardiaca", "sono", "respiratoria"]
_PRIORIDADE_EMPATE = {"cardiaca": 3, "respiratoria": 2, "sono": 1}


def calcular_jornada_recomendada(respostas: dict[str, str]) -> dict:
    pontuacao = {j: 0 for j in JORNADAS}
    empate = False

    for pergunta_id, opcao_id in respostas.items():
        if str(pergunta_id) not in _INDICE:
            raise ValueError(f"Pergunta '{pergunta_id}' não encontrada.")
        opcoes_da_pergunta = _INDICE[str(pergunta_id)]
        if opcao_id not in opcoes_da_pergunta:
            raise ValueError(f"Opção '{opcao_id}' inválida para a pergunta '{pergunta_id}'.")
        for jornada, pts in opcoes_da_pergunta[opcao_id].items():
            pontuacao[jornada] += pts

    score_maximo = max(pontuacao.values())
    vencedoras = [j for j, s in pontuacao.items() if s == score_maximo]

    if len(vencedoras) > 1:
        empate = True
        jornada_recomendada = max(vencedoras, key=lambda j: _PRIORIDADE_EMPATE[j])
    else:
        jornada_recomendada = vencedoras[0]

    mensagens = {
        "cardiaca": "Com base nas suas respostas, a Jornada Cardíaca é a mais indicada para você. Vamos juntos cuidar do seu coração! 💚",
        "sono": "Com base nas suas respostas, a Jornada do Sono é a mais indicada para você. Um bom descanso transforma tudo! 💚",
        "respiratoria": "Com base nas suas respostas, a Jornada Respiratória é a mais indicada para você. Respire bem e viva melhor! 💚",
    }

    return {
        "jornada_recomendada": jornada_recomendada,
        "pontuacao": pontuacao,
        "empate": empate,
        "mensagem": mensagens.get(jornada_recomendada, "Jornada recomendada com sucesso! 💚"),
    }
