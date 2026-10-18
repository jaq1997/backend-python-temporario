"""
Script para popular o banco de dados com UPAs e Hospitais de Porto Alegre (POA).
Executar uma única vez (ou para resetar/atualizar a carga).

Como rodar:
    cd backend
    python -m data.seed_estabelecimentos
"""

import sys
import os

# Adiciona o diretório do backend ao sys.path para importar app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, Base, engine
from app.models.estabelecimento import Estabelecimento

# Dados de UPAs e Hospitais de referência em Porto Alegre / SUS
ESTABELECIMENTOS_POA = [
    {
        "nome": "UPA Moacyr Scliar (Zona Norte)",
        "tipo": "UPA",
        "endereco": "Rua Jerônimo Zelmanovitz, 01",
        "bairro": "São Sebastião",
        "cep": "91060-340",
        "telefone": "(51) 3368-1619",
        "horario_funcionamento": "24 Horas",
        "latitude": -30.007629,
        "longitude": -51.144985,
        "codigo_cnes": "6984852",
    },
    {
        "nome": "UPA Bom Jesus",
        "tipo": "UPA",
        "endereco": "Rua Bom Jesus, 410",
        "bairro": "Bom Jesus",
        "cep": "91420-030",
        "telefone": "(51) 3289-5450",
        "horario_funcionamento": "24 Horas",
        "latitude": -30.046901,
        "longitude": -51.161118,
        "codigo_cnes": "7712392",
    },
    {
        "nome": "UPA Cruzeiro do Sul (Postão da Cruzeiro)",
        "tipo": "UPA",
        "endereco": "Rua Professor Manoel Lobato, 151",
        "bairro": "Santa Tereza",
        "cep": "90850-510",
        "telefone": "(51) 3289-4000",
        "horario_funcionamento": "24 Horas",
        "latitude": -30.076328,
        "longitude": -51.222384,
        "codigo_cnes": "2237602",
    },
    {
        "nome": "Hospital de Pronto Socorro (HPS)",
        "tipo": "Hospital",
        "endereco": "Largo Teodoro Herzl, s/n",
        "bairro": "Bom Fim",
        "cep": "90040-192",
        "telefone": "(51) 3289-7999",
        "horario_funcionamento": "24 Horas - Urgência e Emergência",
        "latitude": -30.038144,
        "longitude": -51.213192,
        "codigo_cnes": "2237572",
    },
    {
        "nome": "Hospital de Clínicas de Porto Alegre (HCPA)",
        "tipo": "Hospital",
        "endereco": "Rua Ramiro Barcelos, 2350",
        "bairro": "Santa Cecília",
        "cep": "90035-903",
        "telefone": "(51) 3359-8000",
        "horario_funcionamento": "24 Horas",
        "latitude": -30.039601,
        "longitude": -51.205934,
        "codigo_cnes": "2237610",
    },
    {
        "nome": "Hospital Nossa Senhora da Conceição (GHC)",
        "tipo": "Hospital",
        "endereco": "Avenida Francisco Trein, 596",
        "bairro": "Cristo Redentor",
        "cep": "91350-200",
        "telefone": "(51) 3357-2000",
        "horario_funcionamento": "24 Horas",
        "latitude": -30.015243,
        "longitude": -51.157832,
        "codigo_cnes": "2237254",
    },
    {
        "nome": "Hospital Materno Infantil Presidente Vargas (HMIPV)",
        "tipo": "Hospital",
        "endereco": "Avenida Independência, 661",
        "bairro": "Independência",
        "cep": "90035-074",
        "telefone": "(51) 3289-3000",
        "horario_funcionamento": "24 Horas",
        "latitude": -30.029801,
        "longitude": -51.217351,
        "codigo_cnes": "2237580",
    },
    {
        "nome": "Hospital Sanatório Partenon",
        "tipo": "Hospital",
        "endereco": "Avenida Bento Gonçalves, 3722",
        "bairro": "Partenon",
        "cep": "90650-001",
        "telefone": "(51) 3336-5200",
        "horario_funcionamento": "Atendimento ambulatorial e internação",
        "latitude": -30.063124,
        "longitude": -51.182415,
        "codigo_cnes": "2237629",
    },
    {
        "nome": "Hospital Fêmina (GHC)",
        "tipo": "Hospital",
        "endereco": "Rua Mostardeiro, 17",
        "bairro": "Rio Branco",
        "cep": "90430-001",
        "telefone": "(51) 3314-5200",
        "horario_funcionamento": "24 Horas - Saúde da Mulher",
        "latitude": -30.027814,
        "longitude": -51.205213,
        "codigo_cnes": "2237262",
    },
    {
        "nome": "Hospital São Lucas da PUCRS",
        "tipo": "Hospital",
        "endereco": "Avenida Ipiranga, 6690",
        "bairro": "Jardim Botânico",
        "cep": "90610-000",
        "telefone": "(51) 3320-3000",
        "horario_funcionamento": "24 Horas",
        "latitude": -30.057391,
        "longitude": -51.173822,
        "codigo_cnes": "2237637",
    },
]


def popular_banco():
    # Garante que as tabelas existem
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    print("Iniciando carga de estabelecimentos de Porto Alegre...")
    inseridos = 0
    atualizados = 0

    try:
        for item in ESTABELECIMENTOS_POA:
            # Procura por código CNES ou nome para evitar duplicação
            existente = None
            if item.get("codigo_cnes"):
                existente = db.query(Estabelecimento).filter(Estabelecimento.codigo_cnes == item["codigo_cnes"]).first()
            if not existente:
                existente = db.query(Estabelecimento).filter(Estabelecimento.nome == item["nome"]).first()

            if existente:
                for k, v in item.items():
                    setattr(existente, k, v)
                atualizados += 1
            else:
                novo = Estabelecimento(**item)
                db.add(novo)
                inseridos += 1

        db.commit()
        print(f"Sucesso! {inseridos} novos estabelecimentos inseridos, {atualizados} atualizados.")
    except Exception as e:
        db.rollback()
        print(f"Erro ao popular banco: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    popular_banco()
