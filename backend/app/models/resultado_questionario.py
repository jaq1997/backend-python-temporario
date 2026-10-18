from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database import Base


class ResultadoQuestionario(Base):
    """
    Armazena o resultado do questionário de triagem.
    O usuario_id é OBRIGATÓRIO (o usuário precisa estar cadastrado e logado).
    """
    __tablename__ = "resultados_questionario"

    id = Column(Integer, primary_key=True, index=True)
    # Obrigatório: aponta para a tabela users (do login do colega)
    usuario_id = Column(Integer, nullable=False, index=True)
    # Ex: {"1": "b", "2": "a", "3": "d", ...}
    respostas = Column(JSON, nullable=False)
    # Ex: {"cardiaca": 8, "sono": 5, "respiratoria": 3}
    pontuacao = Column(JSON, nullable=False)
    # "cardiaca" | "sono" | "respiratoria"
    jornada_recomendada = Column(String(50), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
