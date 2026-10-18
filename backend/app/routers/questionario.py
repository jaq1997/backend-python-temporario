from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.resultado_questionario import ResultadoQuestionario
from ..schemas.questionario import RespostasQuestionario, ResultadoQuestionarioResponse
from ..services.questionario_service import calcular_resultado, PERGUNTAS

router = APIRouter(prefix="/api/questionario", tags=["Questionário"])


@router.get("/perguntas")
def listar_perguntas():
    """
    Retorna as perguntas do questionário (sem o campo 'pontos', que é interno).
    O frontend pode consumir esse endpoint para centralizar as perguntas no backend,
    evitando duplicação entre Questionario.jsx e este serviço.
    """
    perguntas_publicas = []
    for p in PERGUNTAS:
        opcoes_publicas = [
            {"id": op["id"], "titulo": op["titulo"], "descricao": op["descricao"]}
            for op in p["opcoes"]
        ]
        perguntas_publicas.append(
            {
                "id": p["id"],
                "titulo": p["titulo"],
                "subtitulo": p["subtitulo"],
                "opcoes": opcoes_publicas,
            }
        )
    return perguntas_publicas


@router.post("/resultado", response_model=ResultadoQuestionarioResponse)
def calcular_e_salvar_resultado(
    payload: RespostasQuestionario,
    db: Session = Depends(get_db),
):
    """
    Recebe as respostas do usuário, calcula o scoring por jornada e retorna
    a jornada recomendada. Salva o resultado no banco para análise futura.
    """
    try:
        resultado = calcular_resultado(payload.respostas)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Persiste o resultado associado ao usuário informado no payload.
    registro = ResultadoQuestionario(
        usuario_id=payload.usuario_id,
        respostas=payload.respostas,
        pontuacao=resultado["pontuacao"],
        jornada_recomendada=resultado["jornada_recomendada"],
    )
    db.add(registro)
    db.commit()
    db.refresh(registro)

    return resultado
