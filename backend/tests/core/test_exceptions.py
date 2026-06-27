"""Testes das exceções de domínio e do handler centralizado."""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.exceptions.base import (
    BadRequestException,
    CustomException,
    InsufficientPackagesException,
    NotFoundException,
    WeightLimitExceededException,
)
from core.exceptions.handlers import add_exception_handlers


def test_custom_exception_default_message():
    exc = CustomException()
    assert exc.message == "An unexpected error occurred."
    assert exc.status_code == 500
    assert exc.error_code == "INTERNAL_ERROR"


def test_custom_exception_custom_message():
    exc = CustomException("oops")
    assert exc.message == "oops"
    assert str(exc) == "oops"


def test_not_found_exception():
    exc = NotFoundException("item missing")
    assert exc.status_code == 404
    assert exc.error_code == "NOT_FOUND"
    assert exc.message == "item missing"


def test_bad_request_exception():
    exc = BadRequestException()
    assert exc.status_code == 400
    assert exc.error_code == "BAD_REQUEST"


def test_insufficient_packages_exception():
    exc = InsufficientPackagesException()
    assert exc.status_code == 400
    assert exc.error_code == "INSUFFICIENT_PACKAGES"


def test_weight_limit_exceeded_exception_message():
    exc = WeightLimitExceededException(total_weight=95.0, max_weight=80.0)
    assert exc.status_code == 422
    assert exc.error_code == "WEIGHT_LIMIT_EXCEEDED"
    assert "95.00kg" in exc.message
    assert "80.00kg" in exc.message
    assert exc.total_weight == 95.0
    assert exc.max_weight == 80.0


def test_all_custom_exceptions_inherit_base():
    for cls in (
        BadRequestException,
        NotFoundException,
        WeightLimitExceededException,
        InsufficientPackagesException,
    ):
        assert issubclass(cls, CustomException)


def _make_test_app() -> FastAPI:
    """App FastAPI mínimo com rotas que lançam exceções de domínio."""
    app = FastAPI()
    add_exception_handlers(app)

    @app.get("/not-found")
    def _raise_not_found():
        raise NotFoundException("thing not found")

    @app.get("/bad-request")
    def _raise_bad_request():
        raise BadRequestException("invalid input")

    @app.get("/weight-exceeded")
    def _raise_weight():
        raise WeightLimitExceededException(total_weight=100.0, max_weight=50.0)

    return app


@pytest.fixture(scope="module")
def test_client() -> TestClient:
    return TestClient(_make_test_app(), raise_server_exceptions=False)


def test_handler_returns_404_for_not_found(test_client):
    r = test_client.get("/not-found")
    assert r.status_code == 404
    body = r.json()
    assert body["error_code"] == "NOT_FOUND"
    assert body["message"] == "thing not found"


def test_handler_returns_400_for_bad_request(test_client):
    r = test_client.get("/bad-request")
    assert r.status_code == 400
    body = r.json()
    assert body["error_code"] == "BAD_REQUEST"


def test_handler_returns_422_with_details_for_weight_exceeded(test_client):
    r = test_client.get("/weight-exceeded")
    assert r.status_code == 422
    body = r.json()
    assert body["error_code"] == "WEIGHT_LIMIT_EXCEEDED"
    assert "details" in body
    assert body["details"]["total_weight"] == 100.0
    assert body["details"]["max_weight"] == 50.0
