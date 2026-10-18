from pydantic import BaseModel, Field


class RespostasQuestionario(BaseModel):
    """
    Recebe as respostas e o id do usuário obrigatório.
    Exemplo:
    {
        "usuario_id": 1,
        "respostas": {"1": "b", "2": "c", "3": "a", ...}
    }
    """
    usuario_id: int = Field(..., description="ID do usuário logado (obrigatório)")
    respostas: dict[str, str] = Field(..., description="Dicionário com {pergunta_id: opcao_id}")


class ResultadoQuestionarioResponse(BaseModel):
    jornada_recomendada: str
    pontuacao: dict[str, int]
    empate: bool = False
    mensagem: str

    model_config = {"from_attributes": True}
