from sqlalchemy import Column, Integer, String, Float, Boolean
from ..database import Base


class Estabelecimento(Base):
    __tablename__ = "estabelecimentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    # Tipos: "UPA", "Hospital", "Policlinica"
    tipo = Column(String(50), nullable=False)
    endereco = Column(String(300), nullable=False)
    bairro = Column(String(100), nullable=True)
    cep = Column(String(10), nullable=True)
    telefone = Column(String(20), nullable=True)
    horario_funcionamento = Column(String(200), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    # Código CNES para referência futura do scraper
    codigo_cnes = Column(String(20), nullable=True, unique=True)
