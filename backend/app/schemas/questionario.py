from pydantic import BaseModel, Field


class RespostasQuestionario(BaseModel):
    """
    Recebe as respostas e, quando disponível, o ID do usuário autenticado.
    Exemplo:
    {
        "usuario_id": 1,
        "respostas": {"1": "b", "2": "c", "3": "a", ...}
    }
    """
    usuario_id: int | None = Field(default=None, gt=0, description="ID do usuário logado, quando disponível")
    respostas: dict[str, str] = Field(..., description="Dicionário com {pergunta_id: opcao_id}")
    jornada_escolhida: str | None = Field(
        default=None,
        description="Jornada escolhida pela pessoa quando houver empate",
    )


class ResultadoQuestionarioResponse(BaseModel):
    jornada_recomendada: str | None
    pontuacao: dict[str, int]
    empate: bool = False
    jornadas_empatadas: list[str] = Field(default_factory=list)
    mensagem: str
    persistido: bool = False

    model_config = {"from_attributes": True}
