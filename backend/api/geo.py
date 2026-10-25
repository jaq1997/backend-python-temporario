import math
import httpx

VIACEP_URL = "https://viacep.com.br/ws/{cep}/json/"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_HEADERS = {"User-Agent": "InformaSaude/1.0 (projeto-maisprati)"}


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcula a distância em km entre dois pontos geográficos."""
    raio_terra = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return raio_terra * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


async def geocodificar_cep(cep: str) -> tuple[float, float]:
    """Converte CEP em coordenadas (lat, lng) usando ViaCEP + Nominatim."""
    cep_limpo = cep.replace("-", "").replace(" ", "").strip()
    if len(cep_limpo) != 8 or not cep_limpo.isdigit():
        raise ValueError("CEP inválido. Use o formato 90000-000.")

    async with httpx.AsyncClient(timeout=10) as client:
        resp_cep = await client.get(VIACEP_URL.format(cep=cep_limpo))
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
        resultados = resp_geo.json()
        if not resultados:
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
            resultados = resp_geo2.json()

        if not resultados:
            raise ValueError("Não foi possível determinar a localização a partir do CEP.")

        return float(resultados[0]["lat"]), float(resultados[0]["lon"])


def filtrar_por_raio(estabelecimentos, lat_ref: float, lng_ref: float, raio_km: float):
    """Filtra estabelecimentos dentro do raio e ordena pelo mais próximo."""
    resultado = []
    for est in estabelecimentos:
        dist = haversine_km(lat_ref, lng_ref, float(est.latitude), float(est.longitude))
        if dist <= raio_km:
            resultado.append((est, round(dist, 2)))
    resultado.sort(key=lambda x: x[1])
    return resultado
