import pytest
from unittest.mock import MagicMock, patch
from app.repositories import avaliacao_comportamental_item_repository as repo


@patch("app.repositories.avaliacao_comportamental_item_repository.AvaliacaoComportamentalItem")
@patch("app.repositories.avaliacao_comportamental_item_repository.AvaliacaoComportamental")
def test_listar_por_colaborador_sem_filtros(mock_model, mock_item_model):
    """Verifica se listar_por_colaborador faz o join e retorna itens serializados."""
    mock_query = MagicMock()
    mock_item_model.query.join.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = ["mocked_item"]

    with patch("app.repositories.avaliacao_comportamental_item_repository.AvaliacaoComportamentalItemOutputSchema") as mock_schema:
        mock_schema.return_value.dump.return_value = [{"nota": 5}]
        result = repo.listar_por_colaborador(colaborador_id=1)

    assert result == [{"nota": 5}]
    mock_item_model.query.join.assert_called_once_with(mock_model)
    mock_query.filter.assert_called_once()
    mock_schema.assert_called_once_with(many=True)


# @patch("app.repositories.avaliacao_comportamental_item_repository.AvaliacaoComportamentalItem")
# @patch("app.repositories.avaliacao_comportamental_item_repository.AvaliacaoComportamental")
# def test_listar_por_colaborador_com_filtros(mock_model, mock_item_model):
#     """Verifica se os filtros de data_inicio e data_fim são aplicados."""
#     mock_query = MagicMock()
#     mock_item_model.query.join.return_value = mock_query
#     mock_query.filter.return_value = mock_query
#     mock_query.all.return_value = []

#     repo.listar_por_colaborador(1, data_inicio="2025-10-20", data_fim="2025-10-25")

#     # Deve aplicar três filtros: colaborador_id, data_inicio e data_fim
#     assert mock_query.filter.call_count == 3


@patch("app.repositories.avaliacao_comportamental_item_repository.AvaliacaoComportamental")
def test_get_por_id(mock_model):
    """Garante que get_por_id retorna o objeto correto."""
    mock_model.query.filter_by.return_value.first.return_value = "avaliacao"
    result = repo.get_por_id(1)
    assert result == "avaliacao"
    mock_model.query.filter_by.assert_called_once_with(id=1)


def test_atualizar_itens_atualiza_existente():
    """Atualiza item existente da avaliação."""
    mock_item = MagicMock(numero_questao=1)
    avaliacao = MagicMock(itens=[mock_item])

    novos_itens = [
        {"numero_questao": 1, "descricao": "Nova desc", "nota": 4},
    ]

    repo.atualizar_itens(avaliacao, novos_itens)
    assert mock_item.descricao == "Nova desc"
    assert mock_item.nota == 4


@patch("app.repositories.avaliacao_comportamental_item_repository.db")
@patch("app.repositories.avaliacao_comportamental_item_repository.AvaliacaoComportamentalItem")
def test_atualizar_itens_adiciona_novo(mock_model, mock_db):
    """Adiciona novo item à avaliação caso não exista."""
    avaliacao = MagicMock(id=5, itens=[])
    novos_itens = [
        {"numero_questao": 1, "descricao": "Teste", "nota": 3},
    ]

    repo.atualizar_itens(avaliacao, novos_itens)

    mock_model.assert_called_once_with(
        avaliacao_comportamental_id=5,
        numero_questao=1,
        descricao="Teste",
        nota=3
    )
    mock_db.session.add.assert_called_once()


# @patch("app.repositories.avaliacao_comportamental_item_repository.db")
# @patch("app.repositories.avaliacao_comportamental_item_repository.AvaliacaoComportamentalItem")
# def test_deletar_remove_itens(mock_model, mock_db):
#     """Verifica se o delete é executado e o flush é chamado."""
#     mock_query = mock_model.query.filter_by.return_value
#     repo.deletar(10)
#     mock_model.query.filter_by.assert_called_once_with(avaliacao_comportamental_id=10)
#     mock_query.delete.assert_called_once()
#     mock_db.session.flush.assert_called_once()
