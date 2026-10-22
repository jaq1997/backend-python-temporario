import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from app.services.geo_service import buscar_top_k_por_rota


class GeoServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_returns_five_nearest_road_routes_within_radius(self):
        estabelecimentos = [
            SimpleNamespace(id=1, latitude=-30.01, longitude=-51.01),
            SimpleNamespace(id=2, latitude=-30.02, longitude=-51.02),
            SimpleNamespace(id=3, latitude=-30.03, longitude=-51.03),
            SimpleNamespace(id=4, latitude=-30.04, longitude=-51.04),
            SimpleNamespace(id=5, latitude=-30.05, longitude=-51.05),
            SimpleNamespace(id=6, latitude=-30.06, longitude=-51.06),
            SimpleNamespace(id=7, latitude=-30.07, longitude=-51.07),
        ]
        resposta = SimpleNamespace(
            raise_for_status=lambda: None,
            json=lambda: {
                "code": "Ok",
                "distances": [[3000, 1000, 6000, 800, 2000, 4000, None]],
            },
        )

        with patch("app.services.geo_service.httpx.AsyncClient") as cliente_http:
            cliente = cliente_http.return_value.__aenter__.return_value
            cliente.get = AsyncMock(return_value=resposta)

            resultado = await buscar_top_k_por_rota(
                estabelecimentos,
                lat_ref=-30.0,
                lng_ref=-51.0,
                raio_km=10,
            )

        self.assertEqual(
            [(estabelecimento.id, distancia) for estabelecimento, distancia in resultado],
            [(4, 0.8), (2, 1.0), (5, 2.0), (1, 3.0), (6, 4.0)],
        )
        cliente.get.assert_awaited_once()
        self.assertEqual(cliente.get.await_args.kwargs["params"]["sources"], "0")
        self.assertEqual(
            cliente.get.await_args.kwargs["params"]["destinations"],
            "1;2;3;4;5;6;7",
        )

    async def test_returns_empty_without_calling_osrm_when_no_candidates(self):
        with patch("app.services.geo_service.httpx.AsyncClient") as cliente_http:
            resultado = await buscar_top_k_por_rota([], -30.0, -51.0, 10)

        self.assertEqual(resultado, [])
        cliente_http.assert_not_called()


if __name__ == "__main__":
    unittest.main()
