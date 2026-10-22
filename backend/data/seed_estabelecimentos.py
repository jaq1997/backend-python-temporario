"""Load the approved Porto Alegre health facilities into PostgreSQL.

Run from the backend directory:
    python -m data.seed_estabelecimentos

The source data is in rede_saude_carga.json. Coordinates are provisional and
should be verified against CNES before being treated as official.
"""

import json
from pathlib import Path

from app.database import Base, SessionLocal, engine
from app.models.estabelecimento import Estabelecimento

DATA_PATH = Path(__file__).with_name("rede_saude_carga.json")
TIPOS_VALIDOS = {"UPA", "Pronto Atendimento", "Hospital"}


def popular_banco() -> None:
    with DATA_PATH.open(encoding="utf-8") as arquivo:
        estabelecimentos = json.load(arquivo)

    if not isinstance(estabelecimentos, list) or not estabelecimentos:
        raise ValueError("O arquivo de estabelecimentos está vazio ou inválido.")

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    inseridos = 0
    atualizados = 0
    desativados = 0

    try:
        nomes_publicados = {item.get("nome") for item in estabelecimentos}
        for existente in db.query(Estabelecimento).filter(Estabelecimento.ativo.is_(True)):
            if existente.nome not in nomes_publicados:
                existente.ativo = False
                desativados += 1

        for item in estabelecimentos:
            if item.get("tipo") not in TIPOS_VALIDOS:
                raise ValueError(
                    f"Tipo inválido para '{item.get('nome')}': {item.get('tipo')}."
                )
            if item.get("latitude") is None or item.get("longitude") is None:
                raise ValueError(
                    f"Coordenadas ausentes para o estabelecimento '{item.get('nome')}'."
                )

            dados = {
                campo: item[campo]
                for campo in (
                    "nome",
                    "tipo",
                    "endereco",
                    "telefone",
                    "latitude",
                    "longitude",
                    "codigo_cnes",
                )
            }
            existente = (
                db.query(Estabelecimento)
                .filter(Estabelecimento.nome == dados["nome"])
                .first()
            )

            if existente:
                for campo, valor in dados.items():
                    setattr(existente, campo, valor)
                existente.ativo = True
                atualizados += 1
            else:
                db.add(Estabelecimento(**dados, ativo=True))
                inseridos += 1

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    print(
        f"Carga concluída: {inseridos} inseridos, {atualizados} atualizados, "
        f"{desativados} desativados. "
        "Coordenadas provisórias; fonte cadastral informada: Google Maps via Apify."
    )


if __name__ == "__main__":
    popular_banco()
