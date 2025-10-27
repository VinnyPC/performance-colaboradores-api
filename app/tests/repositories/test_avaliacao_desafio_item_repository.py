import pytest
from unittest.mock import MagicMock, patch
from app.repositories import avaliacao_desafio_item_repository as repo


# ---------- LISTAR ----------
@patch("app.repositories.avaliacao_desafio_item_repository.AvaliacaoDesafioItem")
@patch("app.repositories.avaliacao_desafio_item_repository.AvaliacaoDesafio")
def test_listar_por_colaborador_sem_filtros(mock_model, mock_item_model):
    """Testa listagem sem filtros de data."""
    mock_query = MagicMock()
    mock_item_model.query.join.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = ["item_fake"]

    with patch("app.repositories.avaliacao_desafio_item_repository.AvaliacaoDesafioItemOutputSchema") as mock_schema:
        mock_schema.return_value.dump.return_value = [{"nota": 4}]
        result = repo.listar_por_colaborador(colaborador_id=1)

    assert result == [{"nota": 4}]
    mock_item_model.query.join.assert_called_once_with(mock_model)
    mock_query.filter.assert_called_once()
    mock_schema.assert_called_once_with(many=True)


# @patch("app.repositories.avaliacao_desafio_item_repository.AvaliacaoDesafioItem")
# @patch("app.repositories.avaliacao_desafio_item_repository.AvaliacaoDesafio")
# def test_listar_por_colaborador_com_filtros(mock_model, mock_item_model):
#     """Testa se filtros de data_inicio e data_fim são aplicados corretamente."""
#     mock_query = MagicMock()
#     mock_item_model.query.join.return_value = mock_query
#     mock_query.filter.return_value = mock_query
#     mock_query.all.return_value = []

#     repo.listar_por_colaborador(1, data_inicio="2025-10-20", data_fim="2025-10-25")

#     assert mock_query.filter.call_count == 3  # colaborador_id, data_inicio e data_fim


# ---------- GET ----------
@patch("app.repositories.avaliacao_desafio_item_repository.AvaliacaoDesafio")
def test_get_por_id(mock_model):
    """Testa se get_por_id retorna a avaliação correta."""
    mock_model.query.filter_by.return_value.first.return_value = "avaliacao_fake"
    result = repo.get_por_id(10)

    assert result == "avaliacao_fake"
    mock_model.query.filter_by.assert_called_once_with(id=10)


# ---------- ATUALIZAR ----------
def test_atualizar_itens_existentes():
    """Testa se itens existentes são atualizados corretamente."""
    mock_item = MagicMock(numero_desafio=1)
    avaliacao = MagicMock(itens=[mock_item])
    novos_itens = [{"numero_desafio": 1, "descricao": "Atualizado", "nota": 5}]

    repo.atualizar_itens(avaliacao, novos_itens)

    assert mock_item.descricao == "Atualizado"
    assert mock_item.nota == 5


@patch("app.repositories.avaliacao_desafio_item_repository.db")
@patch("app.repositories.avaliacao_desafio_item_repository.AvaliacaoDesafioItem")
def test_atualizar_itens_cria_novo(mock_model, mock_db):
    """Testa se um novo item é criado caso não exista."""
    avaliacao = MagicMock(id=99, itens=[])
    novos_itens = [{"numero_desafio": 2, "descricao": "Novo Desafio", "nota": 3}]

    repo.atualizar_itens(avaliacao, novos_itens)

    mock_model.assert_called_once_with(
        avaliacao_desafio_id=99,
        numero_desafio=2,
        descricao="Novo Desafio",
        nota=3
    )
    mock_db.session.add.assert_called_once()
