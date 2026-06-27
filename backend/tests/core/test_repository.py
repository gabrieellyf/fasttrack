"""
Testes unitários de BaseRepository.

Usa um modelo de teste (Item) para exercitar todos os métodos do repositório
genérico sem depender de modelos de produção (que serão criados na Etapa 3).

Banco: SQLite in-memory via fixture `session` do conftest.py.
"""

from __future__ import annotations

from uuid import uuid4

import pytest
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from core.database.setup import BaseDBModel
from core.repository.base import BaseRepository


class Item(BaseDBModel):
    """Modelo auxiliar de teste — herda BaseDBModel para satisfazer TypeVar bound."""

    __tablename__ = "test_items"

    name: Mapped[str] = mapped_column(String(100), nullable=False)


class ItemRepository(BaseRepository[Item]):
    def __init__(self, session):
        super().__init__(Item, session)


@pytest.mark.asyncio
async def test_create_returns_instance_with_id(session):
    repo = ItemRepository(session)
    item = await repo.create({"name": "Widget"})

    assert item.id is not None
    assert item.name == "Widget"
    assert item.deleted is False
    assert item.created_at is not None


@pytest.mark.asyncio
async def test_get_by_id_returns_created_item(session):
    repo = ItemRepository(session)
    created = await repo.create({"name": "Gadget"})

    found = await repo.get_by_id(created.id)

    assert found is not None
    assert found.id == created.id
    assert found.name == "Gadget"


@pytest.mark.asyncio
async def test_get_by_id_returns_none_for_unknown_id(session):
    repo = ItemRepository(session)

    result = await repo.get_by_id(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_get_all_returns_all_active_items(session):
    repo = ItemRepository(session)
    await repo.create({"name": "Alpha"})
    await repo.create({"name": "Beta"})

    items = await repo.get_all()

    assert len(items) == 2


@pytest.mark.asyncio
async def test_get_all_respects_pagination(session):
    repo = ItemRepository(session)
    for i in range(5):
        await repo.create({"name": f"Item {i}"})

    page = await repo.get_all(skip=2, limit=2)

    assert len(page) == 2


@pytest.mark.asyncio
async def test_update_changes_field(session):
    repo = ItemRepository(session)
    item = await repo.create({"name": "Old Name"})

    updated = await repo.update(item.id, {"name": "New Name"})

    assert updated is not None
    assert updated.name == "New Name"


@pytest.mark.asyncio
async def test_update_nonexistent_id_returns_none(session):
    repo = ItemRepository(session)

    result = await repo.update(uuid4(), {"name": "Ghost"})

    assert result is None


@pytest.mark.asyncio
async def test_update_with_all_none_values_returns_unchanged(session):
    """Campos None são ignorados — o registro não é alterado."""
    repo = ItemRepository(session)
    item = await repo.create({"name": "Stable"})

    result = await repo.update(item.id, {"name": None})

    assert result is not None
    assert result.name == "Stable"


@pytest.mark.asyncio
async def test_delete_returns_true_for_existing_item(session):
    repo = ItemRepository(session)
    item = await repo.create({"name": "ToDelete"})

    result = await repo.delete(item.id)

    assert result is True


@pytest.mark.asyncio
async def test_delete_hides_item_from_get_by_id(session):
    """Soft-delete: item deletado não é retornado por get_by_id."""
    repo = ItemRepository(session)
    item = await repo.create({"name": "Hidden"})

    await repo.delete(item.id)
    found = await repo.get_by_id(item.id)

    assert found is None


@pytest.mark.asyncio
async def test_delete_hides_item_from_get_all(session):
    """Soft-delete: item deletado não aparece em get_all."""
    repo = ItemRepository(session)
    kept = await repo.create({"name": "Keep"})
    removed = await repo.create({"name": "Remove"})

    await repo.delete(removed.id)
    items = await repo.get_all()
    ids = [i.id for i in items]

    assert kept.id in ids
    assert removed.id not in ids


@pytest.mark.asyncio
async def test_delete_nonexistent_id_returns_false(session):
    repo = ItemRepository(session)

    result = await repo.delete(uuid4())

    assert result is False


@pytest.mark.asyncio
async def test_double_delete_returns_false_on_second_call(session):
    """Segundo delete num item já deletado retorna False (item não está mais visível)."""
    repo = ItemRepository(session)
    item = await repo.create({"name": "Once"})

    first = await repo.delete(item.id)
    second = await repo.delete(item.id)

    assert first is True
    assert second is False
