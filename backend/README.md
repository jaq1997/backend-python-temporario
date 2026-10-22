# InformaSaúde — Backend (FastAPI + PostgreSQL)

Módulos desenvolvidos:
1. **Rede de Busca de Estabelecimentos (UPAs e Hospitais de Porto Alegre):**
   - Matriz de distâncias por ruas via OSRM/OpenStreetMap e retorno dos cinco estabelecimentos mais próximos dentro do raio configurado.
   - Fallback por CEP via ViaCEP + Nominatim, com cálculo de rotas pelo OSRM.
   - A API pública de demonstração do OSRM é usada para o MVP; ela não oferece garantia de disponibilidade para produção ou alto volume.
   - Rota de atualização cadastral de endereço e dados (`PATCH /api/estabelecimentos/{id}`).
   - Carga inicial de hospitais e UPAs identificados no Google Maps via Apify.
   - Coordenadas provisórias; os códigos CNES e dados cadastrais ainda precisam ser verificados.

2. **Questionário de preferência de jornada:**
   - Perguntas configuradas em `app/data/questionario.json`.
   - O serviço `app/services/questionario_service.py` valida as respostas e centraliza a pontuação e o desempate; o frontend apenas envia as respostas e apresenta as opções devolvidas pela API.
   - Cada resposta soma um ponto para a jornada associada à opção; em caso de empate, a pessoa escolhe entre as jornadas empatadas.

---

## Como rodar o projeto

### 1. Ativar o ambiente virtual (Git Bash)

```bash
source venv/Scripts/activate
```

### 2. Configurar o banco de dados

Crie ou atualize o arquivo `.env` com as mesmas configurações PostgreSQL usadas pelo backend de autenticação:

```env
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=informasaude
RAIO_PADRAO_KM=20
```

O backend de autenticação também usa variáveis adicionais no `.env`. Este serviço ignora as variáveis que não utiliza. Não compartilhe nem faça commit do `.env`.

### 3. Popular o banco com UPAs e Hospitais de Porto Alegre

```bash
python -m data.seed_estabelecimentos
```

O script carrega os 6 registros aprovados em `data/rede_saude_carga.json` e desativa registros ativos que não estejam nessa lista, sem apagá-los do banco. Os 11 registros pendentes de conferência ficam em `data/rede_saude_revisar.json`. Os dados vieram do Google Maps via Apify; as coordenadas são provisórias e não devem ser consideradas confirmação oficial do CNES.

### 4. Iniciar o servidor FastAPI

```bash
uvicorn app.main:app --reload --port 8000
```

Documentação interativa Swagger: **http://localhost:8000/docs**
