# Modelo de Dados — FastTrack

## Sumário

1. [Diagrama ER](#1-diagrama-er)
2. [DDL das Tabelas](#2-ddl-das-tabelas)
3. [Descrição das Tabelas](#3-descrição-das-tabelas)
4. [Soft-Delete](#4-soft-delete)
5. [Schemas Pydantic](#5-schemas-pydantic)
6. [Mapeamento ORM → Domínio](#6-mapeamento-orm--domínio)

---

## 1. Diagrama ER

```mermaid
erDiagram
    packages {
        UUID id PK
        VARCHAR recipient_name
        FLOAT x
        FLOAT y
        FLOAT weight
        FLOAT access_cost
        BOOLEAN deleted
        TIMESTAMPTZ created_at
    }

    vehicles {
        UUID id PK
        VARCHAR plate UK
        FLOAT max_weight
        BOOLEAN deleted
        TIMESTAMPTZ created_at
    }

    hubs {
        UUID id PK
        VARCHAR name
        FLOAT x
        FLOAT y
        BOOLEAN is_central
        BOOLEAN deleted
        TIMESTAMPTZ created_at
    }

    hub_packages {
        UUID hub_id PK FK
        UUID package_id PK FK
    }

    hubs ||--o{ hub_packages : "contém"
    packages ||--o{ hub_packages : "disponível em"
```

---

## 2. DDL das Tabelas

### `packages`

```sql
CREATE TABLE packages (
    id          UUID         NOT NULL PRIMARY KEY,
    deleted     BOOLEAN      NOT NULL DEFAULT false,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT now(),
    recipient_name VARCHAR(255) NOT NULL,
    x           FLOAT        NOT NULL,
    y           FLOAT        NOT NULL,
    weight      FLOAT        NOT NULL,
    access_cost FLOAT        NOT NULL DEFAULT 0
);
```

### `vehicles`

```sql
CREATE TABLE vehicles (
    id          UUID        NOT NULL PRIMARY KEY,
    deleted     BOOLEAN     NOT NULL DEFAULT false,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    plate       VARCHAR(20) NOT NULL,
    max_weight  FLOAT       NOT NULL,
    UNIQUE (plate)
);
```

### `hubs`

```sql
CREATE TABLE hubs (
    id          UUID         NOT NULL PRIMARY KEY,
    deleted     BOOLEAN      NOT NULL DEFAULT false,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT now(),
    name        VARCHAR(255) NOT NULL,
    x           FLOAT        NOT NULL,
    y           FLOAT        NOT NULL,
    is_central  BOOLEAN      NOT NULL DEFAULT false
);
```

### `hub_packages` (tabela de associação)

```sql
CREATE TABLE hub_packages (
    hub_id      UUID NOT NULL REFERENCES hubs(id),
    package_id  UUID NOT NULL REFERENCES packages(id),
    PRIMARY KEY (hub_id, package_id)
);
```

---

## 3. Descrição das Tabelas

### `packages`

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | UUID | Chave primária, gerada no lado Python (`uuid4()`) |
| `recipient_name` | VARCHAR(255) | Nome do destinatário |
| `x` | FLOAT | Coordenada cartesiana X do endereço de entrega |
| `y` | FLOAT | Coordenada cartesiana Y do endereço de entrega |
| `weight` | FLOAT | Peso do pacote em kg (> 0) |
| `access_cost` | FLOAT | Custo adicional de acesso ao endereço (≥ 0, default 0) |
| `deleted` | BOOLEAN | Soft-delete flag |
| `created_at` | TIMESTAMPTZ | Timestamp UTC de criação |

### `vehicles`

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | UUID | Chave primária |
| `plate` | VARCHAR(20) | Placa — chave natural de negócio, **única** |
| `max_weight` | FLOAT | Capacidade máxima de carga em kg (> 0) |
| `deleted` | BOOLEAN | Soft-delete flag |
| `created_at` | TIMESTAMPTZ | Timestamp UTC de criação |

### `hubs`

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | UUID | Chave primária |
| `name` | VARCHAR(255) | Nome do hub |
| `x` | FLOAT | Coordenada cartesiana X |
| `y` | FLOAT | Coordenada cartesiana Y |
| `is_central` | BOOLEAN | `true` = Hub Central (origem/destino); `false` = Hub Secundário |
| `deleted` | BOOLEAN | Soft-delete flag |
| `created_at` | TIMESTAMPTZ | Timestamp UTC de criação |

### `hub_packages`

Tabela de associação many-to-many entre `hubs` e `packages`.
Representa os pacotes **disponíveis para coleta** em um hub secundário
(cross-docking). Não herda `deleted`/`created_at` — é apenas uma ligação referencial.

| Coluna | Tipo | Descrição |
|---|---|---|
| `hub_id` | UUID FK | Referência para `hubs.id` |
| `package_id` | UUID FK | Referência para `packages.id` |
| PK composta | (hub_id, package_id) | Garante unicidade da associação |

---

## 4. Soft-Delete

Nenhum registro é deletado fisicamente do banco. O campo `deleted` é setado como `true`.

**Comportamento:**
- `BaseRepository.get_by_id()` filtra `WHERE deleted = false`
- `BaseRepository.get_all()` filtra `WHERE deleted = false`
- `BaseRepository.delete()` executa `UPDATE SET deleted = true`

**Vantagens:**
- Auditoria: histórico completo de registros
- Reversibilidade: soft-deletes podem ser desfeitos
- Referências íntegras: FKs em `hub_packages` não quebram com soft-delete

---

## 5. Schemas Pydantic

Os schemas Pydantic definem os contratos de request/response da API.
São independentes dos modelos ORM — a conversão é feita via `model_dump()` (request → ORM)
e `from_attributes=True` (ORM → response).

### Pacotes

```python
class PackageCreate(BaseModel):
    recipient_name: str
    x: float
    y: float
    weight: float = Field(gt=0)
    access_cost: float = Field(ge=0, default=0.0)

class PackageUpdate(BaseModel):
    recipient_name: str | None = None
    x: float | None = None
    y: float | None = None
    weight: float | None = Field(default=None, gt=0)
    access_cost: float | None = Field(default=None, ge=0)

class PackageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    recipient_name: str
    x: float
    y: float
    weight: float
    access_cost: float
    deleted: bool
    created_at: datetime
```

### Veículos

```python
class VehicleCreate(BaseModel):
    plate: str = Field(max_length=20)
    max_weight: float = Field(gt=0)

class VehicleUpdate(BaseModel):
    plate: str | None = Field(default=None, max_length=20)
    max_weight: float | None = Field(default=None, gt=0)

class VehicleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    plate: str
    max_weight: float
    deleted: bool
    created_at: datetime
```

### Hubs

```python
class HubCreate(BaseModel):
    name: str = Field(max_length=255)
    x: float
    y: float
    is_central: bool = False

class HubUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    x: float | None = None
    y: float | None = None
    is_central: bool | None = None

class HubResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    x: float
    y: float
    is_central: bool
    deleted: bool
    created_at: datetime
```

### Roteirização

```python
class RouteRequest(BaseModel):
    vehicle_id: UUID
    package_ids: list[UUID] = Field(min_length=1)
    hub_ids: list[UUID] | None = None

class RouteStopResponse(BaseModel):
    id: str
    label: str
    x: float
    y: float

class RouteOptionResponse(BaseModel):
    type: Literal["express", "economic", "strategic"]
    stops: list[RouteStopResponse]
    total_distance: float
    total_cost: float
    total_weight: float

class RouteResponse(BaseModel):
    express: RouteOptionResponse
    economic: RouteOptionResponse
    strategic: RouteOptionResponse
```

---

## 6. Mapeamento ORM → Domínio

O endpoint `POST /routes/` converte modelos ORM para dataclasses de domínio
antes de passar ao módulo `routing/`:

```
Package (ORM)        →  PackageData (dataclass)
Vehicle (ORM)        →  VehicleData (dataclass)
Hub (ORM)            →  HubData (dataclass)
  Hub.packages       →  HubData.packages: list[PackageData]
```

Funções de conversão em `api/routes.py`:

```python
def _to_package_data(package: Package) -> PackageData:
    return PackageData(
        id=package.id,
        recipient_name=package.recipient_name,
        x=package.x,
        y=package.y,
        weight=package.weight,
        access_cost=package.access_cost,
    )
```

O relacionamento `Hub.packages` é carregado via **SELECT-IN** (`selectinload`)
no método `HubRepository.get_hubs_for_routing()`, evitando o erro `MissingGreenlet`
que ocorre com lazy loading em contexto async.
