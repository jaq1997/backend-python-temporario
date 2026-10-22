from typing import Optional
import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.estabelecimento import Estabelecimento
from ..schemas.estabelecimento import (
    EstabelecimentoResponse,
    EstabelecimentoCreate,
    EstabelecimentoUpdate,
)
from ..services.geo_service import buscar_top_k_por_rota, geocodificar_cep
from ..config import settings

router = APIRouter(prefix="/api/estabelecimentos", tags=["Estabelecimentos"])

TIPOS_VALIDOS = {"UPA", "Pronto Atendimento", "Hospital"}


async def _formatar_estabelecimentos_proximos(
    estabelecimentos: list[Estabelecimento],
    lat: float,
    lng: float,
    raio_km: float,
) -> list[EstabelecimentoResponse]:
    try:
        filtrados = await buscar_top_k_por_rota(estabelecimentos, lat, lng, raio_km)
    except (httpx.HTTPError, ValueError) as e:
        raise HTTPException(
            status_code=502,
            detail="Serviço de cálculo de rotas indisponível. Tente novamente mais tarde.",
        ) from e

    resultado = []
    for estabelecimento, distancia in filtrados:
        item = EstabelecimentoResponse.model_validate(estabelecimento)
        item.distancia_km = distancia
        resultado.append(item)
    return resultado


@router.get("/proximos", response_model=list[EstabelecimentoResponse])
async def buscar_por_coordenadas(
    lat: float = Query(..., description="Latitude do usuário"),
    lng: float = Query(..., description="Longitude do usuário"),
    raio: Optional[float] = Query(None, description="Raio viário em km (ex: 20)"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo: UPA ou Hospital"),
    db: Session = Depends(get_db),
):
    """
    Retorna estabelecimentos de saúde dentro do raio informado a partir de
    coordenadas geográficas (obtidas do navegador do usuário).
    """
    raio_km = raio or settings.RAIO_PADRAO_KM

    query = db.query(Estabelecimento).filter(
        Estabelecimento.ativo.is_(True),
        Estabelecimento.tipo.in_(TIPOS_VALIDOS),
    )
    if tipo:
        tipo_normalizado = next(
            (tipo_valido for tipo_valido in TIPOS_VALIDOS if tipo_valido.casefold() == tipo.strip().casefold()),
            None,
        )
        if tipo_normalizado is None:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo inválido. Valores aceitos: {', '.join(TIPOS_VALIDOS)}",
            )
        query = query.filter(Estabelecimento.tipo == tipo_normalizado)

    return await _formatar_estabelecimentos_proximos(query.all(), lat, lng, raio_km)


@router.get("/por-cep", response_model=list[EstabelecimentoResponse])
async def buscar_por_cep(
    cep: str = Query(..., description="CEP do usuário no formato 90000-000"),
    raio: Optional[float] = Query(None, description="Raio viário em km (ex: 20)"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo: UPA ou Hospital"),
    db: Session = Depends(get_db),
):
    """Geocodifica o CEP e retorna os cinco estabelecimentos mais próximos por ruas."""
    raio_km = raio or settings.RAIO_PADRAO_KM

    try:
        lat, lng = await geocodificar_cep(cep)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail="Serviço de busca de CEP/localização indisponível.") from e

    query = db.query(Estabelecimento).filter(
        Estabelecimento.ativo.is_(True),
        Estabelecimento.tipo.in_(TIPOS_VALIDOS),
    )
    if tipo:
        tipo_normalizado = next(
            (tipo_valido for tipo_valido in TIPOS_VALIDOS if tipo_valido.casefold() == tipo.strip().casefold()),
            None,
        )
        if tipo_normalizado is None:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo inválido. Valores aceitos: {', '.join(TIPOS_VALIDOS)}",
            )
        query = query.filter(Estabelecimento.tipo == tipo_normalizado)

    return await _formatar_estabelecimentos_proximos(query.all(), lat, lng, raio_km)


@router.get("/tipos")
def listar_tipos():
    """Retorna os tipos de estabelecimentos disponíveis para filtro."""
    return sorted(TIPOS_VALIDOS)


@router.get("/{estabelecimento_id}", response_model=EstabelecimentoResponse)
def obter_estabelecimento(
    estabelecimento_id: int,
    db: Session = Depends(get_db),
):
    """Retorna os detalhes de um estabelecimento pelo ID."""
    estabelecimento = db.query(Estabelecimento).filter(Estabelecimento.id == estabelecimento_id).first()
    if not estabelecimento:
        raise HTTPException(status_code=404, detail="Estabelecimento não encontrado.")
    return estabelecimento


@router.post("", response_model=EstabelecimentoResponse, status_code=status.HTTP_201_CREATED)
def criar_estabelecimento(
    dados: EstabelecimentoCreate,
    db: Session = Depends(get_db),
):
    """Cadastra um novo estabelecimento no banco."""
    estabelecimento = Estabelecimento(**dados.model_dump())
    db.add(estabelecimento)
    db.commit()
    db.refresh(estabelecimento)
    return estabelecimento


@router.patch("/{estabelecimento_id}", response_model=EstabelecimentoResponse)
def atualizar_estabelecimento(
    estabelecimento_id: int,
    dados: EstabelecimentoUpdate,
    db: Session = Depends(get_db),
):
    """
    Atualiza dados do estabelecimento (endereço, telefone, horário, coordenadas, etc.).
    Permite atualização parcial.
    """
    estabelecimento = db.query(Estabelecimento).filter(Estabelecimento.id == estabelecimento_id).first()
    if not estabelecimento:
        raise HTTPException(status_code=404, detail="Estabelecimento não encontrado.")

    campos_atualizados = dados.model_dump(exclude_unset=True)
    for campo, valor in campos_atualizados.items():
        setattr(estabelecimento, campo, valor)

    db.commit()
    db.refresh(estabelecimento)
    return estabelecimento
