import pytest
from unittest.mock import MagicMock, patch
from datetime import date
from app.repositories import avaliacao_comportamental_repository as repo

@patch("app.repositories.avaliacao_comportamental_repository.db")
def test_listar_por_colaborador_sem_filtros(mock_db):
    """Verifica se listar_por_colaborador retorna a query básica."""
    mock_query = MagicMock()
    mock_db.session.query.return_value.filter_by.return_value = mock_query
    mock_query.all.return_value = ["objeto1", "objeto2"]

    result = repo.listar_por_colaborador(colaborador_id=10)

    mock_db.session.query.assert_called_once()
    mock_db.session.query.return_value.filter_by.assert_called_once_with(colaborador_id=10)
    assert result == ["objeto1", "objeto2"]

@patch("app.repositories.avaliacao_comportamental_repository.AvaliacaoComportamental")
def test_get_por_id(mock_model):
    """Garante que get_por_id chama corretamente o filter_by."""
    mock_model.query.filter_by.return_value.first.return_value = "objeto"
    result = repo.get_por_id(99)
    assert result == "objeto"
    mock_model.query.filter_by.assert_called_once_with(id=99)

