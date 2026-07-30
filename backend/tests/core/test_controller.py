"""
Testes de BaseController.

Usa o mesmo modelo Item de test_repository.py para exercitar os métodos
genéricos do controller (get_by_id, get_all, create, update, delete),
verificando que as exceções corretas são lançadas para casos de borda.
"""

from __future__ import annotations

from uuid import uuid4

import pytest
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from core.controller.base import BaseController
from core.database.setup import BaseDBModel
from core.exceptions.base import NotFoundException
from core.repository.base import BaseRepository


class ControllerItem(BaseDBModel):
    __tablename__ = "controller_test_items"
    name: Mapped[str] = mapped_column(String(100), nullable=False)


class ControllerItemRepository(BaseRepository[ControllerItem]):
    def __init__(self, session):
        super().__init__(ControllerItem, session)


class ControllerItemController(BaseController[ControllerItemRepository]):
    pass


@pytest.mark.asyncio
async def test_controller_create_and_get_by_id(session):
    ctrl = ControllerItemController(ControllerItemRepository(session))

    created = await ctrl.create({"name": "Bolt"})
    found = await ctrl.get_by_id(created.id)

    assert found.id == created.id
    assert found.name == "Bolt"


@pytest.mark.asyncio
async def test_controller_get_by_id_raises_not_found(session):
    ctrl = ControllerItemController(ControllerItemRepository(session))

    with pytest.raises(NotFoundException):
        await ctrl.get_by_id(uuid4())


@pytest.mark.asyncio
async def test_controller_get_all(session):
    ctrl = ControllerItemController(ControllerItemRepository(session))
    await ctrl.create({"name": "A"})
    await ctrl.create({"name": "B"})

    items = await ctrl.get_all()

    assert len(items) == 2


@pytest.mark.asyncio
async def test_controller_update(session):
    ctrl = ControllerItemController(ControllerItemRepository(session))
    item = await ctrl.create({"name": "Before"})

    updated = await ctrl.update(item.id, {"name": "After"})

    assert updated.name == "After"


@pytest.mark.asyncio
async def test_controller_update_raises_not_found(session):
    ctrl = ControllerItemController(ControllerItemRepository(session))

    with pytest.raises(NotFoundException):
        await ctrl.update(uuid4(), {"name": "Ghost"})


@pytest.mark.asyncio
async def test_controller_delete(session):
    ctrl = ControllerItemController(ControllerItemRepository(session))
    item = await ctrl.create({"name": "Bye"})

    result = await ctrl.delete(item.id)

    assert result is True


@pytest.mark.asyncio
async def test_controller_delete_raises_not_found(session):
    ctrl = ControllerItemController(ControllerItemRepository(session))

    with pytest.raises(NotFoundException):
        await ctrl.delete(uuid4())
