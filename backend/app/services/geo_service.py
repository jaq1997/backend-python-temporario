"""Geocodificação de CEP e busca dos estabelecimentos mais próximos por ruas."""

import math

import httpx

VIACEP_URL = "https://viacep.com.br/ws/{cep}/json/"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_HEADERS = {"User-Agent": "InformaSaude/1.0 (projeto-maisprati)"}
OSRM_TABLE_URL = "https://router.project-osrm.org/table/v1/driving/{coordinates}"
TOP_K_ESTABELECIMENTOS = 5


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


async def buscar_top_k_por_rota(
    estabelecimentos,
    lat_ref: float,
    lng_ref: float,
    raio_km: float,
    limite: int = TOP_K_ESTABELECIMENTOS,
):
    """
    Calcula uma matriz de distâncias viárias por OSRM e retorna os K mais próximos
    dentro do raio. Distâncias são as rotas de carro do perfil driving do OSRM.
    """
    if not estabelecimentos:
        return []

    coordenadas = [f"{lng_ref},{lat_ref}"] + [
        f"{est.longitude},{est.latitude}" for est in estabelecimentos
    ]
    indices_destino = ";".join(str(indice) for indice in range(1, len(coordenadas)))

    async with httpx.AsyncClient(timeout=15) as client:
        resposta = await client.get(
            OSRM_TABLE_URL.format(coordinates=";".join(coordenadas)),
            params={
                "sources": "0",
                "destinations": indices_destino,
                "annotations": "distance",
            },
        )
        resposta.raise_for_status()
        matriz = resposta.json()

    if not isinstance(matriz, dict) or matriz.get("code") != "Ok":
        raise ValueError("O OSRM não conseguiu calcular a matriz de rotas.")

    distancias = matriz.get("distances")
    if (
        not isinstance(distancias, list)
        or not distancias
        or not isinstance(distancias[0], list)
        or len(distancias[0]) != len(estabelecimentos)
    ):
        raise ValueError("O OSRM retornou uma matriz de distâncias inválida.")

    resultado = []
    for estabelecimento, distancia_metros in zip(estabelecimentos, distancias[0]):
        if distancia_metros is None:
            continue
        if (
            not isinstance(distancia_metros, (int, float))
            or not math.isfinite(distancia_metros)
            or distancia_metros < 0
        ):
            raise ValueError("O OSRM retornou uma distância inválida.")
        distancia_km = distancia_metros / 1000
        if distancia_km <= raio_km:
            resultado.append((estabelecimento, distancia_km))

    resultado.sort(key=lambda x: x[1])
    return [
        (estabelecimento, round(distancia_km, 2))
        for estabelecimento, distancia_km in resultado[:limite]
    ]
