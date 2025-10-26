import pytest
from unittest.mock import patch
from flask import url_for

def test_listar_colaboradores_sucesso(client):
    fake_colaboradores = [
        {"id": 1, "matricula": "161000", "nome": "Vinicius Silva"},
        {"id": 2, "matricula": "161001", "nome": "Maria Souza"}
    ]

    with patch("app.services.colaborador_service.listar_colaboradores", return_value=fake_colaboradores):
        response = client.get("/colaboradores")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["nome"] == "Vinicius Silva"

def test_listar_colaboradores_erro(client):
    with patch("app.services.colaborador_service.listar_colaboradores", side_effect=Exception("Falha no serviço")):
        response = client.get("/colaboradores")
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Falha no serviço"
