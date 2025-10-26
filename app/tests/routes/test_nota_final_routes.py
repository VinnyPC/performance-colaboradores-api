import pytest
from unittest.mock import patch

def test_listar_notas_sucesso(client):
    fake_notas = [
        {"id": 1, "matricula": "161000", "nota_final": 4.5},
        {"id": 2, "matricula": "161001", "nota_final": 3.8}
    ]

    with patch("app.services.nota_final_service.listar_notas_finais", return_value=fake_notas):
        response = client.get("/notas_finais")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["nota_final"] == 4.5

def test_listar_notas_colaborador_sucesso(client):
    fake_notas = [
        {"id": 1, "matricula": "161000", "nota_final": 4.5}
    ]

    with patch("app.services.nota_final_service.listar_notas_por_matricula", return_value=fake_notas):
        response = client.get("/notas_finais/colaborador?matricula=161000")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["matricula"] == "161000"

def test_listar_notas_colaborador_sem_matricula(client):
    response = client.get("/notas_finais/colaborador")
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "O parâmetro 'matricula' é obrigatório"

def test_listar_notas_colaborador_erro_service(client):
    with patch("app.services.nota_final_service.listar_notas_por_matricula", side_effect=ValueError("Colaborador não encontrado")):
        response = client.get("/notas_finais/colaborador?matricula=999999")
        assert response.status_code == 404
        data = response.get_json()
        assert data["error"] == "Colaborador não encontrado"
