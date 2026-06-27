# Referência da API — FastTrack

## Sumário

1. [Visão Geral](#1-visão-geral)
2. [Convenções](#2-convenções)
3. [Hierarquia de Erros](#3-hierarquia-de-erros)
4. [Pacotes (`/packages/`)](#4-pacotes-packages)
5. [Veículos (`/vehicles/`)](#5-veículos-vehicles)
6. [Hubs (`/hubs/`)](#6-hubs-hubs)
7. [Roteirização (`/routes/`)](#7-roteirização-routes)

---

## 1. Visão Geral

| Item | Valor |
|---|---|
| Base URL (local) | `http://localhost:8000` |
| Formato | JSON (`Content-Type: application/json`) |
| Documentação interativa | `http://localhost:8000/docs` (Swagger UI) |
| Documentação alternativa | `http://localhost:8000/redoc` (ReDoc) |
| Autenticação | Nenhuma nesta versão |

---

## 2. Convenções

### IDs
Todos os IDs são **UUID v4** gerados no lado do servidor. Formato: `xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx`.

### Soft-delete
`DELETE` não remove fisicamente o registro. O campo `deleted: true` é setado e o registro
deixa de aparecer em qualquer query de leitura.

### PATCH semântico
`PATCH` aceita qualquer subconjunto dos campos editáveis. Campos omitidos ou `null` são ignorados.

### Paginação
Endpoints de listagem aceitam query params `skip` (default: `0`) e `limit` (default: `20`).

### Redirect de barra
FastAPI redireciona `/packages` → `/packages/` com HTTP 307. Use sempre a barra final
ou o header `follow redirects` no cliente.

---

## 3. Hierarquia de Erros

Todos os erros retornam um JSON consistente:

```json
{
  "error_code": "string",
  "message": "string",
  "details": {}
}
```

| `error_code` | HTTP | Quando ocorre |
|---|---|---|
| `NOT_FOUND` | 404 | Recurso não existe ou foi soft-deletado |
| `BAD_REQUEST` | 400 | Payload inválido |
| `WEIGHT_LIMIT_EXCEEDED` | 422 | Peso total dos pacotes excede `max_weight` do veículo |
| `INSUFFICIENT_PACKAGES` | 400 | Nenhum `package_id` fornecido |
| `INTERNAL_ERROR` | 500 | Erro inesperado do servidor |
| `VALIDATION_ERROR` | 422 | Violação de schema Pydantic (gerado automaticamente pelo FastAPI) |

`WeightLimitExceededException` inclui campo `details` adicional:
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

## 4. Pacotes (`/packages/`)

### GET /packages/

Lista todos os pacotes ativos (não soft-deletados).

**Query params:**

| Param | Tipo | Default | Descrição |
|---|---|---|---|
| `skip` | integer | `0` | Offset de paginação |
| `limit` | integer | `20` | Máximo de registros retornados |

**Resposta 200:**
```json
[
  {
    "id": "bff80352-af8c-4079-b430-da7e6c12a071",
    "recipient_name": "João Silva",
    "x": 3.0,
    "y": 2.0,
    "weight": 10.0,
    "access_cost": 2.0,
    "deleted": false,
    "created_at": "2026-06-27T02:20:09.245744Z"
  }
]
```

---

### POST /packages/

Cadastra um novo pacote.

**Request body:**
```json
{
  "recipient_name": "João Silva",
  "x": 3.0,
  "y": 2.0,
  "weight": 10.0,
  "access_cost": 2.0
}
```

| Campo | Tipo | Obrigatório | Restrições |
|---|---|---|---|
| `recipient_name` | string | ✅ | — |
| `x` | float | ✅ | Coordenada cartesiana |
| `y` | float | ✅ | Coordenada cartesiana |
| `weight` | float | ✅ | `> 0` |
| `access_cost` | float | ❌ | `>= 0`, default `0.0` |

**Resposta 201:** objeto `PackageResponse` completo (ver GET /packages/).

---

### GET /packages/{package_id}

Busca um pacote pelo UUID.

**Resposta 200:** `PackageResponse`
**Resposta 404:** `NOT_FOUND`

---

### PATCH /packages/{package_id}

Atualiza parcialmente um pacote.

**Request body** (todos opcionais):
```json
{
  "recipient_name": "João S. Atualizado",
  "weight": 12.5
}
```

**Resposta 200:** `PackageResponse` atualizado
**Resposta 404:** `NOT_FOUND`

---

### DELETE /packages/{package_id}

Soft-delete do pacote.

**Resposta 204:** sem corpo
**Resposta 404:** `NOT_FOUND`

---

## 5. Veículos (`/vehicles/`)

### GET /vehicles/

Lista todos os veículos ativos.

**Query params:** `skip`, `limit` (idem pacotes)

**Resposta 200:**
```json
[
  {
    "id": "d4d3a4dd-d155-4d0e-932d-cf6d9993e707",
    "plate": "ABC-1234",
    "max_weight": 100.0,
    "deleted": false,
    "created_at": "2026-06-27T02:20:09.173160Z"
  }
]
```

---

### POST /vehicles/

Cadastra um novo veículo.

**Request body:**
```json
{
  "plate": "ABC-1234",
  "max_weight": 100.0
}
```

| Campo | Tipo | Obrigatório | Restrições |
|---|---|---|---|
| `plate` | string | ✅ | `max_length=20`, **único** |
| `max_weight` | float | ✅ | `> 0` |

**Resposta 201:** `VehicleResponse`

---

### GET /vehicles/by-plate/{plate}

Busca um veículo pela placa (chave natural de negócio).

```bash
curl -sL http://localhost:8000/vehicles/by-plate/ABC-1234
```

**Resposta 200:** `VehicleResponse`
**Resposta 404:** `NOT_FOUND`

---

### GET /vehicles/{vehicle_id}

Busca um veículo pelo UUID.

**Resposta 200:** `VehicleResponse`
**Resposta 404:** `NOT_FOUND`

---

### PATCH /vehicles/{vehicle_id}

Atualiza parcialmente um veículo.

**Request body** (todos opcionais):
```json
{
  "max_weight": 150.0
}
```

**Resposta 200:** `VehicleResponse` atualizado
**Resposta 404:** `NOT_FOUND`

---

### DELETE /vehicles/{vehicle_id}

Soft-delete do veículo.

**Resposta 204:** sem corpo
**Resposta 404:** `NOT_FOUND`

---

## 6. Hubs (`/hubs/`)

### GET /hubs/

Lista hubs com filtro opcional por papel.

**Query params:**

| Param | Tipo | Default | Descrição |
|---|---|---|---|
| `skip` | integer | `0` | Offset |
| `limit` | integer | `20` | Máximo |
| `is_central` | boolean | *(omitido)* | `true` = apenas hub central; `false` = apenas secundários; omitido = todos |

```bash
# Apenas hub central
curl -sL "http://localhost:8000/hubs/?is_central=true"

# Apenas hubs secundários
curl -sL "http://localhost:8000/hubs/?is_central=false"
```

**Resposta 200:**
```json
[
  {
    "id": "17ee7033-c30d-4664-833b-af184e376eed",
    "name": "Hub Central",
    "x": 0.0,
    "y": 0.0,
    "is_central": true,
    "deleted": false,
    "created_at": "2026-06-27T02:20:09.390709Z"
  }
]
```

---

### POST /hubs/

Cadastra um novo hub.

**Request body:**
```json
{
  "name": "Hub Central",
  "x": 0.0,
  "y": 0.0,
  "is_central": true
}
```

| Campo | Tipo | Obrigatório | Restrições |
|---|---|---|---|
| `name` | string | ✅ | `max_length=255` |
| `x` | float | ✅ | Coordenada cartesiana |
| `y` | float | ✅ | Coordenada cartesiana |
| `is_central` | boolean | ❌ | default `false` |

**Resposta 201:** `HubResponse`

---

### GET /hubs/{hub_id}

Busca um hub pelo UUID.

**Resposta 200:** `HubResponse`
**Resposta 404:** `NOT_FOUND`

---

### PATCH /hubs/{hub_id}

Atualiza parcialmente um hub.

**Request body** (todos opcionais):
```json
{
  "name": "Hub Central Atualizado",
  "is_central": false
}
```

**Resposta 200:** `HubResponse` atualizado
**Resposta 404:** `NOT_FOUND`

---

### DELETE /hubs/{hub_id}

Soft-delete do hub.

**Resposta 204:** sem corpo
**Resposta 404:** `NOT_FOUND`

---

## 7. Roteirização (`/routes/`)

### POST /routes/

Calcula as três estratégias de rota simultaneamente.

**Request body:**

```json
{
  "vehicle_id": "d4d3a4dd-d155-4d0e-932d-cf6d9993e707",
  "package_ids": [
    "bff80352-af8c-4079-b430-da7e6c12a071",
    "4f77db14-c692-4b75-8d52-4f26b0be36c0",
    "b120a33f-14bc-44dd-9683-496f0119f836"
  ],
  "hub_ids": ["17ee7033-c30d-4664-833b-af184e376eed"]
}
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `vehicle_id` | UUID | ✅ | ID do veículo — define capacidade máxima |
| `package_ids` | UUID[] | ✅ | Lista de IDs dos pacotes (`min_length=1`) |
| `hub_ids` | UUID[] | ❌ | IDs dos hubs a considerar. Omitido = todos os hubs cadastrados |

**Resposta 200:**

```json
{
  "express": {
    "type": "express",
    "stops": [
      {"id": "17ee7033-...", "label": "Hub Central",   "x": 0.0, "y": 0.0},
      {"id": "bff80352-...", "label": "João Silva",     "x": 3.0, "y": 2.0},
      {"id": "b120a33f-...", "label": "Pedro Oliveira", "x": 2.0, "y": 8.0},
      {"id": "4f77db14-...", "label": "Maria Santos",   "x": 7.0, "y": 4.0},
      {"id": "17ee7033-...", "label": "Hub Central",   "x": 0.0, "y": 0.0}
    ],
    "total_distance": 27.14,
    "total_cost":     57.14,
    "total_weight":   33.0
  },
  "economic": {
    "type": "economic",
    "stops": [...],
    "total_distance": 27.89,
    "total_cost":     54.89,
    "total_weight":   33.0
  },
  "strategic": {
    "type": "strategic",
    "stops": [...],
    "total_distance": 31.42,
    "total_cost":     56.42,
    "total_weight":   41.0
  }
}
```

**Campos da resposta:**

| Campo | Tipo | Descrição |
|---|---|---|
| `type` | `"express" \| "economic" \| "strategic"` | Identificador da estratégia |
| `stops` | `RouteStop[]` | Lista ordenada de paradas (inclui hub inicial e retorno) |
| `stops[].id` | string | UUID do pacote/hub, ou `"hub-central"` se não houver hub cadastrado |
| `stops[].label` | string | Nome do destinatário ou hub |
| `stops[].x`, `.y` | float | Coordenadas cartesianas |
| `total_distance` | float | Distância euclidiana total (inclui retorno ao hub), em unidades do plano |
| `total_cost` | float | Σ(distância_segmento + access_cost) para cada parada de pacote |
| `total_weight` | float | Peso total (pode incluir extras na rota estratégica) |

**Resposta 404 — Veículo ou pacote não encontrado:**
```json
{
  "error_code": "NOT_FOUND",
  "message": "Resource with id=xxxxxxxx-... not found."
}
```

**Resposta 422 — Excesso de peso:**
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
