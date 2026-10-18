# InformaSaúde — Backend (FastAPI + PostgreSQL)

Módulos desenvolvidos:
1. **Rede de Busca de Estabelecimentos (UPAs e Hospitais de Porto Alegre):**
   - Busca conjunta de UPAs e hospitais em um raio padrão de 20 km via fórmula de Haversine.
   - Fallback por CEP via ViaCEP + Nominatim (geocodificador do OpenStreetMap).
   - Rota de atualização cadastral de endereço e dados (`PATCH /api/estabelecimentos/{id}`).
   - Carga estática/batch inicial de estabelecimentos reais com coordenadas e código CNES.

2. **Questionário de Triagem de Saúde:**
   - 9 perguntas obrigatórias com pontuação direcionada para 3 jornadas:
     - `cardiaca` (Jornada Cardíaca)
     - `respiratoria` (Jornada Respiratória)
     - `sono` (Jornada do Sono)
   - Armazenamento de resultados associado ao `usuario_id` inteiro.
   - Textos e pesos atuais são placeholders sujeitos à revisão.

---

## Como rodar o projeto

### 1. Ativar o ambiente virtual (Git Bash):
```bash
source venv/Scripts/activate
```

### 2. Configurar o banco de dados:
Crie o arquivo `.env` com a sua senha do PostgreSQL:
```env
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/informasaude
RAIO_PADRAO_KM=20
```

### 3. Popular o banco com UPAs e Hospitais de Porto Alegre:
```bash
python -m data.seed_estabelecimentos
```

### 4. Iniciar o servidor FastAPI:
```bash
uvicorn app.main:app --reload --port 8000
```

Documentação interativa Swagger: **http://localhost:8000/docs**
