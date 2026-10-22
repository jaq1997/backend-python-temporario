"""Scoring de interesse nas jornadas de educação em saúde."""

import json
from pathlib import Path

JORNADAS = ["cardiaca", "respiratoria", "sono"]

_ROTULOS_JORNADA = {
    "cardiaca": "Jornada Cardíaca",
    "respiratoria": "Jornada Respiratória",
    "sono": "Jornada do Sono",
}

_CONFIG_PATH = Path(__file__).resolve().parent.parent / "data" / "questionario.json"
with _CONFIG_PATH.open(encoding="utf-8") as arquivo_config:
    PERGUNTAS = json.load(arquivo_config)["perguntas"]

_INDICE: dict[str, dict[str, str]] = {
    pergunta["id"]: {
        opcao["id"]: opcao["jornada"]
        for opcao in pergunta["opcoes"]
    }
    for pergunta in PERGUNTAS
}


def calcular_resultado(
    respostas: dict[str, str],
    jornada_escolhida: str | None = None,
) -> dict:
    """Conta escolhas por jornada e valida o desempate quando necessário."""
    perguntas_esperadas = {pergunta["id"] for pergunta in PERGUNTAS}
    perguntas_ausentes = perguntas_esperadas - respostas.keys()
    if perguntas_ausentes:
        ausentes = ", ".join(sorted(perguntas_ausentes))
        raise ValueError(f"Respostas incompletas. Perguntas não respondidas: {ausentes}.")

    perguntas_desconhecidas = respostas.keys() - perguntas_esperadas
    if perguntas_desconhecidas:
        desconhecidas = ", ".join(sorted(perguntas_desconhecidas))
        raise ValueError(f"Perguntas não encontradas: {desconhecidas}.")

    pontuacao = {jornada: 0 for jornada in JORNADAS}
    for pergunta_id, opcao_id in respostas.items():
        jornada = _INDICE[pergunta_id].get(opcao_id)
        if jornada is None:
            raise ValueError(
                f"Opção '{opcao_id}' inválida para pergunta '{pergunta_id}'."
            )
        pontuacao[jornada] += 1

    maior_pontuacao = max(pontuacao.values())
    jornadas_empatadas = [
        jornada for jornada, pontos in pontuacao.items()
        if pontos == maior_pontuacao
    ]
    empate = len(jornadas_empatadas) > 1

    if empate:
        if jornada_escolhida is None:
            jornada_recomendada = None
            mensagem = "Suas respostas apontam mais de uma jornada de interesse. Escolha por qual prefere começar."
        elif jornada_escolhida not in jornadas_empatadas:
            raise ValueError(
                "Escolha uma das jornadas empatadas para concluir o questionário."
            )
        else:
            jornada_recomendada = jornada_escolhida
            mensagem = (
                "Suas respostas apontam mais de uma jornada de interesse. "
                f"Você escolheu começar pela {_ROTULOS_JORNADA[jornada_recomendada]}."
            )
    else:
        jornada_recomendada = jornadas_empatadas[0]
        if jornada_escolhida and jornada_escolhida != jornada_recomendada:
            raise ValueError("A jornada escolhida não corresponde à maior pontuação.")
        mensagem = (
            f"Com base nas suas respostas, sugerimos começar pela "
            f"{_ROTULOS_JORNADA[jornada_recomendada]}."
        )

    return {
        "jornada_recomendada": jornada_recomendada,
        "pontuacao": pontuacao,
        "empate": empate,
        "jornadas_empatadas": jornadas_empatadas if empate else [],
        "mensagem": mensagem,
    }
