# FastTrack — Motor de Roteirização Multi-Objetivo

> Sistema fullstack que calcula e compara **três estratégias de roteirização de entregas** em tempo real,
> permitindo visualizar side-by-side distância, custo operacional e rota no plano cartesiano.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.118-green)
![React](https://img.shields.io/badge/React-19-61dafb)
![TypeScript](https://img.shields.io/badge/TypeScript-5.7-blue)
![Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen)
![Tests](https://img.shields.io/badge/tests-157%20backend%20%7C%2030%20frontend-brightgreen)

---

## Sumário

1. [Visão Geral](#1-visão-geral)
2. [As Três Estratégias de Rota](#2-as-três-estratégias-de-rota)
3. [Stack Tecnológica](#3-stack-tecnológica)
4. [Arquitetura](#4-arquitetura)
5. [Estrutura de Pastas](#5-estrutura-de-pastas)
6. [Pré-requisitos](#6-pré-requisitos)
7. [Instalação e Execução](#7-instalação-e-execução)
8. [Variáveis de Ambiente](#8-variáveis-de-ambiente)
9. [Como usar a API](#9-como-usar-a-api)
10. [Como usar a interface](#10-como-usar-a-interface)
11. [Testes](#11-testes)
12. [Qualidade de Código](#12-qualidade-de-código)
13. [Migrações de Banco](#13-migrações-de-banco)
14. [Uso de Inteligência Artificial](#14-uso-de-inteligência-artificial)
15. [Roadmap / Melhorias Futuras](#15-roadmap--melhorias-futuras)
16. [Documentação Técnica](#16-documentação-técnica)

---

## 1. Visão Geral

FastTrack resolve o problema clássico de **roteirização de última milha** com uma abordagem multi-objetivo:
em vez de forçar um único critério de otimização, o sistema calcula três rotas com heurísticas diferentes
e devolve todas simultaneamente, deixando o operador escolher a estratégia mais adequada ao contexto.

**Entidades principais:**

| Entidade | Papel |
|---|---|
| **Pacote** | Item a ser entregue, com coordenadas cartesianas (x, y), peso e custo de acesso ao endereço |
| **Veículo** | Transportador com capacidade máxima de carga (kg) |
| **Hub Central** | Ponto de partida e retorno de todas as rotas |
| **Hub Secundário** | Ponto de cross-docking: o veículo desvia para coletar pacotes extras |

---

## 2. As Três Estratégias de Rota

| Estratégia | Critério de seleção da próxima parada | Quando usar |
|---|---|---|
| **Expressa** | `argmin{ distância_euclidiana(atual, p) }` — Nearest Neighbor puro | Urgência, janela de tempo curta |
| **Econômica** | `argmin{ distância × w₁ + access_cost × w₂ }` — penaliza endereços de difícil acesso | Redução de custo operacional |
| **Estratégica** | Desvio pelo hub secundário mais próximo do centroide dos pacotes + coleta greedy de extras | Consolidação de carga / cross-docking |

> As três rotas sempre retornam a mesma estrutura de dados (`stops`, `total_distance`, `total_cost`, `total_weight`),
> permitindo comparação direta no frontend.

---

## 3. Stack Tecnológica

### Backend

| Tecnologia | Versão | Papel |
|---|---|---|
| Python | 3.12 | Runtime |
| FastAPI | ^0.118.0 | Framework HTTP async |
| SQLAlchemy | ^2.0.0 [asyncio] | ORM async |
| asyncpg | ^0.31.0 | Driver PostgreSQL async |
| Alembic | ^1.16.0 | Migrations |
| Pydantic | ^2.11.0 | Validação e serialização |
| pydantic-settings | ^2.7.0 | Configuração via `.env` |
| uvicorn | ^0.37.0 | Servidor ASGI |
| gunicorn | ^23.0.0 | Process manager (produção) |
| pytest | ^8.0.0 | Testes |
| pytest-asyncio | ^0.25.0 | Suporte a corrotinas nos testes |
| httpx | ^0.28.0 | Cliente HTTP nos testes de integração |
| aiosqlite | ^0.20.0 | SQLite in-memory para testes |
| ruff | ^0.8.0 | Linter + formatter |
| mypy | ^1.14.0 | Type checking estático |

### Frontend

| Tecnologia | Versão | Papel |
|---|---|---|
| React | ^19.0.0 | UI |
| TypeScript | ^5.7.0 | Tipagem estática |
| Vite | ^6.0.0 | Build tool |
| Redux Toolkit | ^2.5.0 | Gerenciamento de estado |
| React Redux | ^9.2.0 | Bindings React ↔ Redux |
| React Router | ^7.1.0 | Roteamento SPA |
| Recharts | ^2.15.0 | Visualização cartesiana das rotas |
| Axios | ^1.7.0 | Cliente HTTP |
| Vitest | ^2.1.0 | Test runner |
| Testing Library | ^16.1.0 | Testes de componentes |

### Infraestrutura

| Tecnologia | Versão | Papel |
|---|---|---|
| PostgreSQL | 16 (Alpine) | Banco de dados relacional |
| Docker / Compose | v2+ | Orquestração local |
| nginx | Alpine | Serve o build estático do frontend |

---

## 4. Arquitetura

```mermaid
flowchart LR
    Browser -->|HTTP| nginx
    nginx -->|/api/*| FastAPI
    Browser -->|SPA| nginx

    subgraph Backend
        FastAPI --> Controller
        Controller --> Repository
        Repository -->|SQLAlchemy async| PostgreSQL
        Controller --> RoutingModule["routing/\n(Strategy Pattern)"]
    end

    subgraph Frontend
        Redux --> APIClient["axios\napi/"]
        APIClient --> FastAPI
    end
```

**Fluxo de uma requisição POST /routes/:**

```
Browser → nginx → FastAPI Router
    → calculate_routes()
        → VehicleController.get_by_id()      → VehicleRepository → PostgreSQL
        → PackageController.get_by_id() × N  → PackageRepository → PostgreSQL
        → HubRepository.get_hubs_for_routing()                    → PostgreSQL
        → validate_weight()                   → WeightLimitExceededException (422)
        → ExpressRouteStrategy.calculate()    → RouteOption
        → EconomicRouteStrategy.calculate()   → RouteOption
        → StrategicCrossDockingStrategy.calculate() → RouteOption
    ← RouteResponse { express, economic, strategic }
← Browser renderiza RouteMap (Recharts) + tabela comparativa
```

> Documentação técnica completa em [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

---

## 5. Estrutura de Pastas

```
fasttrack/
├── docker-compose.yml          # Orquestra: postgres + backend + frontend
├── README.md
├── docs/                       # Documentação técnica detalhada
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── ALGORITHMS.md
│   ├── DATA_MODEL.md
│   ├── FRONTEND.md
│   └── RELATORIO_TECNICO.md
│
├── backend/
│   ├── Dockerfile
│   ├── .env.example            # Template de variáveis de ambiente
│   ├── pyproject.toml          # Dependências, ruff, pytest, mypy
│   ├── alembic.ini
│   ├── Makefile                # Atalhos: install, run, test, lint, typecheck
│   │
│   ├── api/                    # Routers FastAPI (1 arquivo por recurso)
│   │   ├── packages.py         # GET/POST /packages/, GET/PATCH/DELETE /packages/{id}
│   │   ├── vehicles.py         # CRUD + GET /vehicles/by-plate/{plate}
│   │   ├── hubs.py             # CRUD + filtro ?is_central=
│   │   └── routes.py           # POST /routes/
│   │
│   ├── app/
│   │   ├── controllers/        # Lógica de negócio; herdam BaseController
│   │   ├── models/             # Modelos SQLAlchemy (Package, Vehicle, Hub, HubPackage)
│   │   ├── repositories/       # Acesso a dados; herdam BaseRepository
│   │   └── schemas/            # Schemas Pydantic (Create, Update, Response)
│   │
│   ├── core/
│   │   ├── config.py           # Settings via pydantic-settings / .env
│   │   ├── server.py           # create_app() — CORS, middlewares, routers
│   │   ├── database/setup.py   # engine async, BaseDBModel, get_session
│   │   ├── exceptions/         # Hierarquia CustomException + handlers
│   │   ├── factory/factory.py  # DI com functools.partial
│   │   └── repository/base.py  # BaseRepository genérico (CRUD + soft-delete)
│   │
│   ├── routing/                # Algoritmos — sem dependências de framework
│   │   ├── base.py             # BaseRoutingStrategy (ABC)
│   │   ├── geometry.py         # Point, Stop, centroid, validate_weight, resolve_central_hub
│   │   ├── models.py           # VehicleData, PackageData, HubData, RouteOption
│   │   ├── express.py          # Nearest Neighbor por distância
│   │   ├── economic.py         # Nearest Neighbor por custo ponderado
│   │   └── strategic.py        # Cross-docking com coleta greedy
│   │
│   ├── alembic/
│   │   ├── env.py              # Configuração async do Alembic
│   │   └── versions/           # Scripts de migração
│   │
│   └── tests/
│       ├── conftest.py         # Fixtures: engine SQLite, session, client HTTP
│       ├── core/               # 30 testes (repository, controller, exceptions)
│       ├── routing/            # 40 testes (cada estratégia + comparações)
│       ├── app/                # 39 testes (models, repositories, controllers)
│       ├── factory/            # 7 testes
│       └── api/                # 43 testes (endpoints HTTP)
│
└── frontend/
    ├── Dockerfile              # Build estático + nginx
    ├── nginx.conf              # SPA fallback para React Router
    ├── package.json
    ├── vite.config.ts
    ├── vitest.config.ts
    └── src/
        ├── api/                # Funções axios por recurso (client.ts + 4 módulos)
        ├── store/
        │   ├── index.ts        # configureStore com 4 reducers
        │   └── slices/         # packagesSlice, vehiclesSlice, hubsSlice, routesSlice
        ├── features/
        │   ├── routes/         # RouteCalculator.tsx + RouteMap.tsx
        │   ├── packages/       # PackageList.tsx
        │   ├── vehicles/       # VehicleList.tsx
        │   └── hubs/           # HubList.tsx
        ├── components/         # Layout.tsx (navbar)
        ├── router/             # BrowserRouter com 4 rotas
        └── types/index.ts      # Interfaces TypeScript (espelham schemas do backend)
```

---

## 6. Pré-requisitos

| Ferramenta | Versão mínima | Uso |
|---|---|---|
| Docker | 24+ | Execução em container |
| Docker Compose | v2 | Orquestração dos serviços |
| Python | 3.12+ | Apenas para desenvolvimento local sem Docker |
| Poetry | 1.8+ | Apenas para desenvolvimento local sem Docker |
| Node.js | 20+ | Apenas para desenvolvimento local sem Docker |
| npm | 10+ | Apenas para desenvolvimento local sem Docker |

---

## 7. Instalação e Execução

### 7.1 Execução completa com Docker (recomendado)

```bash
# 1. Clone o repositório
git clone <url-do-repositório>
cd fasttrack

# 2. Copie o arquivo de variáveis de ambiente
cp backend/.env.example backend/.env

# 3. Suba toda a stack (postgres + backend + frontend)
docker compose up --build
```

Os containers sobem na seguinte ordem:
1. **`db`** (PostgreSQL 16) — healthcheck `pg_isready`
2. **`backend`** — aguarda `db` estar healthy, executa `alembic upgrade head` e inicia uvicorn
3. **`frontend`** — nginx servindo o build estático

| Serviço | URL |
|---|---|
| Frontend (React) | http://localhost:5173 |
| API REST | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| PostgreSQL | `localhost:5432` — usuário/senha/db: `fasttrack` |

> **Nota:** As migrações Alembic são executadas automaticamente na inicialização do container `backend`.
> Não é necessário rodar `alembic upgrade head` manualmente.

Para parar os serviços:

```bash
docker compose down          # para e remove os containers
docker compose down -v       # remove também o volume do banco
```

### 7.2 Desenvolvimento local (sem Docker para backend)

```bash
cd fasttrack/backend

# 1. Instalar dependências
poetry install

# 2. Configurar variáveis
cp .env.example .env
# Edite DATABASE_URL para apontar ao banco local se necessário

# 3. Subir apenas o banco de dados
docker compose -f ../docker-compose.yml up db -d

# 4. Aplicar migrações
poetry run alembic upgrade head

# 5. Iniciar servidor com hot-reload
poetry run uvicorn core.server:app --reload --port 8000
# Ou via Makefile:
make run
```

### 7.3 Desenvolvimento local (sem Docker para frontend)

```bash
cd fasttrack/frontend

# 1. Instalar dependências (flag necessária pelo Recharts)
npm install --legacy-peer-deps

# 2. Iniciar servidor de desenvolvimento
npm run dev
```

---

## 8. Variáveis de Ambiente

Arquivo: `backend/.env` (copiar de `backend/.env.example`)

| Variável | Descrição | Valor padrão |
|---|---|---|
| `DATABASE_URL` | URL de conexão async (asyncpg) para o PostgreSQL | `postgresql+asyncpg://fasttrack:fasttrack@localhost:5432/fasttrack` |
| `DEBUG` | Ativa logs SQL do SQLAlchemy e modo debug do FastAPI | `false` |
| `CORS_ORIGINS` | Lista JSON de origens permitidas pelo CORS | `["http://localhost:5173"]` |

> Em produção, sobrescreva via variáveis de ambiente do sistema operacional ou do orquestrador.
> **Nunca commite o arquivo `.env`** — apenas o `.env.example`.

---

## 9. Como usar a API

A documentação interativa completa está disponível em **http://localhost:8000/docs** (Swagger UI).

### Endpoints disponíveis

#### Pacotes

| Método | Rota | Descrição | Status |
|---|---|---|---|
| `GET` | `/packages/` | Lista todos os pacotes ativos | 200 |
| `POST` | `/packages/` | Cadastra um pacote | 201 |
| `GET` | `/packages/{id}` | Busca pacote por ID | 200 / 404 |
| `PATCH` | `/packages/{id}` | Atualiza campos do pacote | 200 / 404 |
| `DELETE` | `/packages/{id}` | Soft-delete do pacote | 204 / 404 |

#### Veículos

| Método | Rota | Descrição | Status |
|---|---|---|---|
| `GET` | `/vehicles/` | Lista todos os veículos ativos | 200 |
| `POST` | `/vehicles/` | Cadastra um veículo | 201 |
| `GET` | `/vehicles/by-plate/{plate}` | Busca veículo por placa | 200 / 404 |
| `GET` | `/vehicles/{id}` | Busca veículo por ID | 200 / 404 |
| `PATCH` | `/vehicles/{id}` | Atualiza campos do veículo | 200 / 404 |
| `DELETE` | `/vehicles/{id}` | Soft-delete do veículo | 204 / 404 |

#### Hubs

| Método | Rota | Descrição | Status |
|---|---|---|---|
| `GET` | `/hubs/` | Lista hubs (aceita `?is_central=true/false`) | 200 |
| `POST` | `/hubs/` | Cadastra um hub | 201 |
| `GET` | `/hubs/{id}` | Busca hub por ID | 200 / 404 |
| `PATCH` | `/hubs/{id}` | Atualiza campos do hub | 200 / 404 |
| `DELETE` | `/hubs/{id}` | Soft-delete do hub | 204 / 404 |

#### Roteirização

| Método | Rota | Descrição | Status |
|---|---|---|---|
| `POST` | `/routes/` | Calcula as três rotas simultaneamente | 200 / 404 / 422 |

### Exemplos com curl

#### Criar um veículo

```bash
curl -sL -X POST http://localhost:8000/vehicles/ \
  -H "Content-Type: application/json" \
  -d '{"plate": "ABC-1234", "max_weight": 100.0}'
```

```json
{
  "id": "d4d3a4dd-d155-4d0e-932d-cf6d9993e707",
  "plate": "ABC-1234",
  "max_weight": 100.0,
  "deleted": false,
  "created_at": "2026-06-27T02:20:09.173160Z"
}
```

#### Criar um pacote

```bash
curl -sL -X POST http://localhost:8000/packages/ \
  -H "Content-Type: application/json" \
  -d '{"recipient_name": "João Silva", "x": 3.0, "y": 2.0, "weight": 10.0, "access_cost": 2.0}'
```

#### Calcular rotas

```bash
curl -sL -X POST http://localhost:8000/routes/ \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_id": "<uuid-do-veiculo>",
    "package_ids": ["<uuid-p1>", "<uuid-p2>", "<uuid-p3>"]
  }'
```

**Resposta (sucesso 200):**

```json
{
  "express": {
    "type": "express",
    "stops": [
      {"id": "<hub-id>", "label": "Hub Central", "x": 0.0, "y": 0.0},
      {"id": "<p1-id>",  "label": "João Silva",   "x": 3.0, "y": 2.0},
      {"id": "<p2-id>",  "label": "Ana Costa",    "x": 9.0, "y": 1.0},
      {"id": "<hub-id>", "label": "Hub Central", "x": 0.0, "y": 0.0}
    ],
    "total_distance": 33.47,
    "total_cost": 104.41,
    "total_weight": 65.0
  },
  "economic": {
    "type": "economic",
    "stops": [...],
    "total_distance": 33.91,
    "total_cost": 106.10,
    "total_weight": 65.0
  },
  "strategic": {
    "type": "strategic",
    "stops": [...],
    "total_distance": 36.32,
    "total_cost": 100.01,
    "total_weight": 65.0
  }
}
```

**Erro 422 — Excesso de peso (`WEIGHT_LIMIT_EXCEEDED`):**

```bash
# Pacotes com peso total = 110 kg em veículo com max_weight = 100 kg
curl -sL -X POST http://localhost:8000/routes/ \
  -H "Content-Type: application/json" \
  -d '{"vehicle_id": "<uuid>", "package_ids": ["<p-pesado-1>", "<p-pesado-2>"]}'
```

```json
{
  "error_code": "WEIGHT_LIMIT_EXCEEDED",
  "message": "Total weight 110.00kg exceeds vehicle capacity of 100.00kg.",
  "details": {
    "total_weight": 110.0,
    "max_weight": 100.0
  }
}
```

---

## 10. Como usar a interface

Acesse **http://localhost:5173** após subir os serviços.

### Fluxo completo

1. **Cadastre dados** via API (curl ou Swagger UI):
   - Pelo menos **1 veículo** (`POST /vehicles/`)
   - Pelo menos **2 pacotes** (`POST /packages/`)
   - Pelo menos **1 hub central** (`POST /hubs/` com `"is_central": true`)

2. **Acesse a página "Roteirização"** (rota `/`):
   - Selecione o veículo no dropdown
   - Marque os pacotes desejados nos checkboxes
   - Clique em **Calcular Rotas**

3. **Analise o resultado**:
   - O **mapa cartesiano** (Recharts) exibe as 3 rotas sobrepostas em cores distintas
   - A **tabela comparativa** mostra distância total, custo total e peso para cada estratégia
   - Use os botões de tab (Expressa / Econômica / Estratégica / Comparar todas) para focar em uma rota
   - Ao selecionar uma aba, a **sequência de paradas** é exibida em uma lista ordenada

| Cor | Estratégia |
|---|---|
| 🔵 Azul | Expressa |
| 🟢 Verde | Econômica |
| 🟠 Laranja | Estratégica |

### Navegação

| Rota | Página | Descrição |
|---|---|---|
| `/` | Roteirização | Calculadora de rotas (principal) |
| `/packages` | Pacotes | Lista de pacotes cadastrados |
| `/vehicles` | Veículos | Lista de veículos cadastrados |
| `/hubs` | Hubs | Lista de hubs com badge de tipo |

---

## 11. Testes

### Backend (pytest)

```bash
cd fasttrack/backend

# Executar todos os testes
poetry run pytest
# Ou via Makefile:
make test

# Executar com relatório de cobertura HTML
make test-cov
# Relatório gerado em htmlcov/index.html

# Executar suite específica
poetry run pytest tests/routing/ -v
poetry run pytest tests/api/ -v
```

**Resultado atual:**

```
157 passed in ~7s
Coverage: 96.08% (threshold: 80%)
```

**Suites de teste:**

| Suite | Arquivo(s) | Testes | O que cobre |
|---|---|---|---|
| `core/` | `test_repository`, `test_controller`, `test_exceptions` | 30 | BaseRepository, BaseController, hierarquia de exceções |
| `routing/` | `test_express`, `test_economic`, `test_strategic`, `test_route_comparison`, `test_weight_validation` | 40 | Cada estratégia, trade-offs entre rotas, validação de peso |
| `app/` | `test_models`, `test_repositories`, `test_controllers` | 39 | Modelos SQLAlchemy, repositórios concretos, controllers |
| `factory/` | `test_factory` | 7 | Injeção de dependência via Factory |
| `api/` | `test_packages`, `test_vehicles`, `test_hubs`, `test_routes` | 43 | Endpoints HTTP completos |

> **Teste crítico:** `tests/routing/test_route_comparison.py::test_express_distance_lt_economic_distance`
> prova matematicamente que a Rota Expressa tem distância menor que a Econômica para um fixture específico,
> enquanto a Econômica tem custo total menor — demonstrando o trade-off entre as estratégias.

### Frontend (Vitest)

```bash
cd fasttrack/frontend

# Executar todos os testes
npm test -- --run

# Executar com cobertura
npm run test:coverage
```

**Resultado atual:** 30 testes passando (5 suites)

| Suite | Testes |
|---|---|
| `packagesSlice.test.ts` | 8 |
| `vehiclesSlice.test.ts` | 6 |
| `hubsSlice.test.ts` | 5 |
| `routesSlice.test.ts` | 6 |
| `RouteMap.test.tsx` | 5 |

---

## 12. Qualidade de Código

### Backend

```bash
cd fasttrack/backend

# Verificar lint e formatação (sem alterar)
make lint

# Aplicar formatação e correções automáticas
make format

# Verificar tipos estáticos
make typecheck

# Ou individualmente:
poetry run ruff check .
poetry run ruff format --check .
poetry run mypy .
```

**Ferramentas configuradas em `pyproject.toml`:**

| Ferramenta | Papel |
|---|---|
| **ruff** | Linter (substitui pylint, flake8, isort) + formatter (substitui black) |
| **mypy** | Type checking estático (modo `strict` parcial) |

### Frontend

```bash
cd fasttrack/frontend

# TypeScript type checking
npx tsc --noEmit

# Lint (ESLint)
npm run lint
```

---

## 13. Migrações de Banco

```bash
cd fasttrack/backend

# Aplicar todas as migrações pendentes
poetry run alembic upgrade head

# Gerar nova migração após alterar modelos SQLAlchemy
poetry run alembic revision --autogenerate -m "descricao_da_mudanca"

# Verificar histórico de migrações
poetry run alembic history

# Reverter a última migração
poetry run alembic downgrade -1

# Reverter todas as migrações
poetry run alembic downgrade base
```

**Migração atual:** `7061ef8dc7e2_create_initial_tables` — cria as tabelas
`packages`, `vehicles`, `hubs` e `hub_packages`.

---

## 14. Uso de Inteligência Artificial

Durante o desenvolvimento utilizei o GitHub Copilot como ferramenta de apoio para agilizar
a escrita de código repetitivo e a estruturação inicial de alguns módulos. Todas as decisões
de arquitetura, os algoritmos de roteirização, os trade-offs técnicos e a validação dos
resultados foram concebidos e conduzidos por mim. O código foi integralmente revisado,
testado e validado — os 157 testes de backend e 30 de frontend são o registro dessa verificação.

---

## 15. Roadmap / Melhorias Futuras

| Item | Descrição |
|---|---|
| **Autenticação** | JWT (Auth0 ou self-hosted) — ponto de extensão já previsto em `core/config.py` |
| **Cache** | Redis para resultados de roteirização repetidos — ponto de extensão em `core/` |
| **Algoritmos avançados** | Or-Tools (otimização exata) ou metaheurísticas (SA, GA) para frotas grandes |
| **Formulários na UI** | Criar pacotes/veículos/hubs diretamente pelo frontend |
| **Deploy em nuvem** | Docker em ECS, Cloud Run ou Kubernetes |
| **CI/CD** | Pipeline de lint + testes + build + deploy |
| **Observabilidade** | Logging estruturado (JSON), métricas (Prometheus), tracing (OpenTelemetry) |
| **Frota múltipla** | Roteirização para múltiplos veículos simultâneos (VRP) |

---

## 16. Documentação Técnica

| Documento | Conteúdo |
|---|---|
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Arquitetura em profundidade: camadas, padrões, DI, async |
| [`docs/API.md`](docs/API.md) | Referência completa de todos os endpoints com exemplos JSON |
| [`docs/ALGORITHMS.md`](docs/ALGORITHMS.md) | Explicação detalhada dos 3 algoritmos com pseudocódigo |
| [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md) | Modelo ER, DDL das tabelas e schemas Pydantic |
| [`docs/FRONTEND.md`](docs/FRONTEND.md) | Arquitetura do frontend: Redux, feature-based, Recharts |
| [`docs/RELATORIO_TECNICO.md`](docs/RELATORIO_TECNICO.md) | Relatório completo do processo de desenvolvimento |

---

*FastTrack — desenvolvido como projeto de portfólio demonstrando arquitetura fullstack,
algoritmos de roteirização e boas práticas de engenharia de software.*
