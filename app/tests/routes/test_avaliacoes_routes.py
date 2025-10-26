import pytest
from unittest.mock import patch, MagicMock
from flask import url_for

@pytest.mark.parametrize("endpoint,repository,items_key", [
    ("/avaliacoes/comportamental", "avaliacao_comportamental_item_repository", "itens"),
    ("/avaliacoes/desafio", "avaliacao_desafio_item_repository", "itens"),
])
def test_listar_itens_por_matricula(client, endpoint, repository, items_key):
    matricula = "12345"

    with patch("app.repositories.colaborador_repository.get_id_por_matricula") as mock_get_id, \
         patch(f"app.repositories.{repository}.listar_por_colaborador") as mock_listar:

        mock_get_id.return_value = 1
        mock_listar.return_value = [{"id": 1, "nota": 5, "descricao": "Teste"}]

        response = client.get(f"{endpoint}?matricula={matricula}")
        data = response.get_json()

        assert response.status_code == 200
        assert isinstance(data, list)
        assert data[0]["nota"] == 5
        mock_get_id.assert_called_once_with(matricula)
        mock_listar.assert_called_once_with(1, data_inicio=None, data_fim=None)

def test_listar_itens_sem_matricula(client):
    response = client.get("/avaliacoes/comportamental")
    data = response.get_json()
    assert response.status_code == 400
    assert "error" in data

def test_listar_media_final_comportamental(client):
    matricula = "12345"
    mock_avaliacao = MagicMock()
    mock_avaliacao_dump = {"id": 1, "media_comportamental": 4.0, "data_avaliacao": "2025-10-25"}

    with patch("app.repositories.colaborador_repository.get_id_por_matricula") as mock_get_id, \
         patch("app.repositories.avaliacao_comportamental_repository.listar_por_colaborador") as mock_listar, \
         patch("app.routes.avaliacoes_routes.media_comportamental_schema_many.dump") as mock_dump:

        mock_get_id.return_value = 1
        mock_listar.return_value = [mock_avaliacao]
        mock_dump.return_value = [mock_avaliacao_dump]

        response = client.get(f"/avaliacoes/mediaFinalComportamental?matricula={matricula}")
        data = response.get_json()

        assert response.status_code == 200
        assert isinstance(data, list)
        assert data[0]["media_comportamental"] == 4.0

def test_listar_media_final_desafio(client):
    matricula = "12345"
    mock_avaliacao = MagicMock()
    mock_avaliacao_dump = {"id": 1, "media_desafio": 3.5, "data_avaliacao": "2025-10-25"}

    with patch("app.repositories.colaborador_repository.get_id_por_matricula") as mock_get_id, \
         patch("app.repositories.avaliacao_desafio_repository.listar_por_colaborador") as mock_listar, \
         patch("app.routes.avaliacoes_routes.media_desafio_schema_many.dump") as mock_dump:

        mock_get_id.return_value = 1
        mock_listar.return_value = [mock_avaliacao]
        mock_dump.return_value = [mock_avaliacao_dump]

        response = client.get(f"/avaliacoes/mediaFinalDesafio?matricula={matricula}")
        data = response.get_json()

        assert response.status_code == 200
        assert isinstance(data, list)
        assert data[0]["media_desafio"] == 3.5
