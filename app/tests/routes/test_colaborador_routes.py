import pytest
from unittest.mock import patch
from flask import url_for
from app.routes.colaborador_routes import colaboradores_bp

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
        
@patch("app.routes.colaborador_routes.colaborador_service")
def test_listar_colaboradores_sucesso(mock_service, client):
    """Deve retornar lista de colaboradores com status 200."""
    mock_service.listar_colaboradores.return_value = [{"id": 1, "nome": "Ana"}]
    response = client.get("/colaboradores")

    assert response.status_code == 200
    assert response.get_json() == [{"id": 1, "nome": "Ana"}]
    mock_service.listar_colaboradores.assert_called_once()


@patch("app.routes.colaborador_routes.colaborador_service")
def test_listar_colaboradores_erro(mock_service, client):
    """Deve retornar erro 500 se houver exceção."""
    mock_service.listar_colaboradores.side_effect = Exception("Erro inesperado")
    response = client.get("/colaboradores")

    assert response.status_code == 500
    assert "error" in response.get_json()

@patch("app.routes.colaborador_routes.colaborador_service")
def test_criar_colaborador_sucesso(mock_service, client):
    """Deve criar colaborador e retornar 201."""
    mock_service.criar_colaborador.return_value = {"id": 1, "nome": "Ana"}
    response = client.post(
        "/colaboradores",
        json={"matricula": "123", "nome": "Ana", "data_admissao": "2024-01-01", "cargo": "Dev"},
    )

    assert response.status_code == 201
    assert response.get_json()["id"] == 1
    mock_service.criar_colaborador.assert_called_once()


@patch("app.routes.colaborador_routes.colaborador_service")
def test_criar_colaborador_erro_validacao(mock_service, client):
    """Deve retornar 400 se houver erro de validação."""
    from marshmallow import ValidationError
    mock_service.criar_colaborador.side_effect = ValidationError({"nome": ["Campo obrigatório."]})

    response = client.post(
        "/colaboradores",
        json={"matricula": "123"},
    )

    assert response.status_code == 400
    assert "erros" in response.get_json()


@patch("app.routes.colaborador_routes.colaborador_service")
def test_criar_colaborador_erro_geral(mock_service, client):
    """Deve retornar 500 em erro inesperado."""
    mock_service.criar_colaborador.side_effect = Exception("Falha geral")

    response = client.post(
        "/colaboradores",
        json={"matricula": "123", "nome": "Ana"},
    )

    assert response.status_code == 500
    assert "error" in response.get_json()

@patch("app.routes.colaborador_routes.colaborador_repository")
@patch("app.routes.colaborador_routes.colaborador_service")
def test_atualizar_colaborador_sucesso(mock_service, mock_repo, client):
    """Deve atualizar colaborador com sucesso."""
    mock_repo.get_id_por_matricula.return_value = 5
    mock_service.atualizar_colaborador.return_value = {"id": 5, "nome": "Atualizado"}

    response = client.put(
        "/colaboradores?matricula=123",
        json={"nome": "Atualizado"},
    )

    assert response.status_code == 200
    assert response.get_json()["id"] == 5
    mock_repo.get_id_por_matricula.assert_called_once_with("123")


@patch("app.routes.colaborador_routes.colaborador_repository")
@patch("app.routes.colaborador_routes.colaborador_service")
def test_atualizar_colaborador_sem_matricula(mock_service, mock_repo, client):
    """Deve retornar 400 se 'matricula' não for informada."""
    response = client.put("/colaboradores", json={"nome": "Teste"})
    assert response.status_code == 400
    assert "matricula" in response.get_json()["error"]


@patch("app.routes.colaborador_routes.colaborador_repository")
@patch("app.routes.colaborador_routes.colaborador_service")
def test_atualizar_colaborador_nao_encontrado(mock_service, mock_repo, client):
    """Deve retornar 404 se colaborador não existir."""
    mock_repo.get_id_por_matricula.return_value = 10
    mock_service.atualizar_colaborador.side_effect = ValueError("Colaborador não encontrado")

    response = client.put("/colaboradores?matricula=999", json={"nome": "Teste"})
    assert response.status_code == 404
    assert "error" in response.get_json()

@patch("app.routes.colaborador_routes.colaborador_repository")
@patch("app.routes.colaborador_routes.colaborador_service")
def test_deletar_colaborador_sucesso(mock_service, mock_repo, client):
    """Deve deletar colaborador e retornar 200."""
    mock_repo.get_id_por_matricula.return_value = 3
    response = client.delete("/colaboradores?matricula=123")

    assert response.status_code == 200
    assert "mensagem" in response.get_json()
    mock_service.deletar_colaborador.assert_called_once_with(3)


@patch("app.routes.colaborador_routes.colaborador_repository")
@patch("app.routes.colaborador_routes.colaborador_service")
def test_deletar_colaborador_sem_matricula(mock_service, mock_repo, client):
    """Deve retornar 400 se 'matricula' não for informada."""
    response = client.delete("/colaboradores")
    assert response.status_code == 400
    assert "matricula" in response.get_json()["error"]


@patch("app.routes.colaborador_routes.colaborador_repository")
@patch("app.routes.colaborador_routes.colaborador_service")
def test_deletar_colaborador_nao_encontrado(mock_service, mock_repo, client):
    """Deve retornar 404 se colaborador não existir."""
    mock_repo.get_id_por_matricula.side_effect = ValueError("Colaborador não encontrado.")
    response = client.delete("/colaboradores?matricula=999")

    assert response.status_code == 404
    assert "error" in response.get_json()
