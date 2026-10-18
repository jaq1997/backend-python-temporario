from pydantic import BaseModel
from typing import Optional


class EstabelecimentoBase(BaseModel):
    nome: str
    tipo: str  # "UPA", "Hospital", "Policlinica"
    endereco: str
    bairro: Optional[str] = None
    cep: Optional[str] = None
    telefone: Optional[str] = None
    horario_funcionamento: Optional[str] = None
    latitude: float
    longitude: float
    codigo_cnes: Optional[str] = None


class EstabelecimentoCreate(EstabelecimentoBase):
    pass


class EstabelecimentoUpdate(BaseModel):
    """Schema para atualização parcial ou total de dados/endereço do estabelecimento."""
    nome: Optional[str] = None
    tipo: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cep: Optional[str] = None
    telefone: Optional[str] = None
    horario_funcionamento: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    ativo: Optional[bool] = None
    codigo_cnes: Optional[str] = None


class EstabelecimentoResponse(EstabelecimentoBase):
    id: int
    ativo: bool
    # Distância em km — calculada dinamicamente na busca por proximidade
    distancia_km: Optional[float] = None

    model_config = {"from_attributes": True}
