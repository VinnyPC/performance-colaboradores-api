import pytest
from unittest.mock import patch, MagicMock
from app.services import colaborador_service

def test_listar_colaboradores_sucesso(monkeypatch):
    fake_colaboradores = [
        {"id": 1, "nome": "João"},
        {"id": 2, "nome": "Maria"}
    ]

    monkeypatch.setattr(
        colaborador_service.colaborador_repository,
        "listar_todos",
        lambda: fake_colaboradores
    )

    resultado = colaborador_service.listar_colaboradores()
    assert isinstance(resultado, list)
    assert len(resultado) == 2
    assert resultado[0]["nome"] == "João"

def test_listar_colaboradores_vazio(monkeypatch):
    monkeypatch.setattr(
        colaborador_service.colaborador_repository,
        "listar_todos",
        lambda: []
    )

    resultado = colaborador_service.listar_colaboradores()
    assert resultado == []
