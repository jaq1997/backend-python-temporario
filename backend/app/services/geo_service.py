"""
Serviço de geolocalização para busca de estabelecimentos de saúde.

Fluxo 1 (geolocalização do navegador):
    Frontend → lat/lng → GET /api/estabelecimentos/proximos

Fluxo 2 (fallback ViaCEP):
    Frontend → CEP → GET /api/estabelecimentos/por-cep
    Backend → ViaCEP (endereço) → Nominatim/OSM (lat/lng) → busca por raio

A fórmula de Haversine é aplicada no Python após trazer os candidatos do banco.
Para conjuntos grandes de dados, considere mover o cálculo para SQL com PostGIS.
"""

import math
import httpx

VIACEP_URL = "https://viacep.com.br/ws/{cep}/json/"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_HEADERS = {"User-Agent": "InformaSaude/1.0 (projeto-maisprati)"}


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcula a distância em km entre dois pontos geográficos (fórmula de Haversine)."""
    R = 6371  # raio da Terra em km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


async def geocodificar_cep(cep: str) -> tuple[float, float]:
    """
    Converte CEP em coordenadas (lat, lng) usando ViaCEP + Nominatim.

    Returns:
        Tupla (latitude, longitude)

    Raises:
        ValueError: se o CEP for inválido ou não encontrado.
    """
    cep_limpo = cep.replace("-", "").replace(" ", "").strip()
    if len(cep_limpo) != 8 or not cep_limpo.isdigit():
        raise ValueError("CEP inválido. Use o formato 90000-000.")

    async with httpx.AsyncClient(timeout=10) as client:
        # 1. ViaCEP → endereço textual
        resp_cep = await client.get(VIACEP_URL.format(cep=cep_limpo))
        resp_cep.raise_for_status()
        if resp_cep.status_code != 200:
            raise ValueError("CEP não encontrado.")

        dados_cep = resp_cep.json()
        if dados_cep.get("erro"):
            raise ValueError("CEP não encontrado.")

        logradouro = dados_cep.get("logradouro", "")
        bairro = dados_cep.get("bairro", "")
        localidade = dados_cep.get("localidade", "")
        uf = dados_cep.get("uf", "")
        endereco_completo = f"{logradouro}, {bairro}, {localidade}, {uf}, Brasil"

        # 2. Nominatim → coordenadas
        resp_geo = await client.get(
            NOMINATIM_URL,
            params={
                "q": endereco_completo,
                "format": "json",
                "limit": 1,
                "countrycodes": "br",
            },
            headers=NOMINATIM_HEADERS,
        )
        resp_geo.raise_for_status()
        resultados = resp_geo.json()
        if not resultados:
            # Fallback: tenta só cidade + UF
            resp_geo2 = await client.get(
                NOMINATIM_URL,
                params={
                    "q": f"{localidade}, {uf}, Brasil",
                    "format": "json",
                    "limit": 1,
                    "countrycodes": "br",
                },
                headers=NOMINATIM_HEADERS,
            )
            resp_geo2.raise_for_status()
            resultados = resp_geo2.json()

        if not resultados:
            raise ValueError(
                "Não foi possível determinar a localização a partir do CEP informado."
            )

        lat = float(resultados[0]["lat"])
        lng = float(resultados[0]["lon"])
        return lat, lng


def filtrar_por_raio(estabelecimentos, lat_ref: float, lng_ref: float, raio_km: float):
    """
    Recebe uma lista de objetos Estabelecimento e retorna apenas os que estão
    dentro do raio, com o campo distancia_km calculado, ordenados por proximidade.
    """
    resultado = []
    for est in estabelecimentos:
        dist = haversine_km(lat_ref, lng_ref, est.latitude, est.longitude)
        if dist <= raio_km:
            resultado.append((est, round(dist, 2)))
    resultado.sort(key=lambda x: x[1])
    return resultado
