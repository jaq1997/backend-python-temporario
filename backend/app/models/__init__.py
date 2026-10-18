# Importa todos os models para que o SQLAlchemy os registre
from .estabelecimento import Estabelecimento
from .resultado_questionario import ResultadoQuestionario

__all__ = ["Estabelecimento", "ResultadoQuestionario"]
