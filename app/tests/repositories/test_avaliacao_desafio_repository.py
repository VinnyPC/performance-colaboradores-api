import pytest
from datetime import date
from app.models import AvaliacaoDesafio, AvaliacaoDesafioItem
from app.repositories import avaliacao_desafio_repository


@pytest.fixture
def mock_avaliacao():
    """Cria uma avaliação de desafio falsa para os testes."""
    return AvaliacaoDesafio(
        id=1,
        colaborador_id=10,
        data_avaliacao=date(2024, 5, 20),
        media_desafio=4.5
    )


@pytest.fixture
def mock_itens():
    """Cria uma lista de itens de avaliação de desafio falsos."""
    return [
        {
            "numero_desafio": 1,
            "descricao": "Entrega de projeto A",
            "nota": 4.0,
            "data_avaliacao": date(2024, 5, 20)
        },
        {
            "numero_desafio": 2,
            "descricao": "Apresentação técnica",
            "nota": 5.0,
            "data_avaliacao": date(2024, 5, 20)
        }
    ]


def test_salvar_avaliacao_desafio(app, mock_avaliacao, mock_itens, mocker):
    """Testa se salvar_avaliacao_desafio adiciona a avaliação e os itens corretamente."""
    mock_add = mocker.patch.object(avaliacao_desafio_repository.db.session, "add")
    mock_flush = mocker.patch.object(avaliacao_desafio_repository.db.session, "flush")
    mock_add_all = mocker.patch.object(avaliacao_desafio_repository.db.session, "add_all")

    avaliacao_desafio_repository.salvar_avaliacao_desafio(mock_avaliacao, mock_itens)

    mock_add.assert_called_once_with(mock_avaliacao)
    mock_flush.assert_called_once()
    mock_add_all.assert_called_once()
    assert all(isinstance(i, AvaliacaoDesafioItem) for i in mock_add_all.call_args[0][0])


def test_get_por_id(app, mocker, mock_avaliacao):
    """Testa se get_por_id retorna a avaliação correta."""
    mock_query = mocker.MagicMock()
    mock_query.filter_by.return_value.first.return_value = mock_avaliacao
    mocker.patch.object(avaliacao_desafio_repository.AvaliacaoDesafio, "query", mock_query)

    result = avaliacao_desafio_repository.get_por_id(1)
    assert result == mock_avaliacao
    mock_query.filter_by.assert_called_once_with(id=1)


def test_listar_por_colaborador_sem_datas(app, mocker):
    """Testa listar_por_colaborador sem filtros de data."""
    mock_query = mocker.MagicMock()
    mock_query.filter_by.return_value = mock_query
    mock_query.all.return_value = ["avaliacao1", "avaliacao2"]
    mocker.patch.object(avaliacao_desafio_repository.db, "session", mocker.Mock(query=mocker.Mock(return_value=mock_query)))
    mocker.patch.object(avaliacao_desafio_repository, "db", mocker.Mock(session=mocker.Mock(query=lambda _: mock_query)))

    result = avaliacao_desafio_repository.listar_por_colaborador(10)
    assert result == ["avaliacao1", "avaliacao2"]


def test_listar_por_colaborador_com_datas(app, mocker):
    """Testa listar_por_colaborador com filtros de data."""
    mock_query = mocker.MagicMock()
    mock_query.filter_by.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = ["avaliacao_filtrada"]
    mocker.patch.object(avaliacao_desafio_repository, "db", mocker.Mock(session=mocker.Mock(query=lambda _: mock_query)))

    result = avaliacao_desafio_repository.listar_por_colaborador(10, "2024-01-01", "2024-12-31")
    assert result == ["avaliacao_filtrada"]
    assert mock_query.filter.call_count == 2  


def test_deletar(app, mocker):
    """Testa se deletar remove corretamente uma avaliação."""
    mock_query = mocker.MagicMock()
    mock_query.filter_by.return_value.delete.return_value = 1
    mock_flush = mocker.patch.object(avaliacao_desafio_repository.db.session, "flush")
    mocker.patch.object(avaliacao_desafio_repository.AvaliacaoDesafio, "query", mock_query)

    avaliacao_desafio_repository.deletar(1)

    mock_query.filter_by.assert_called_once_with(id=1)
    mock_flush.assert_called_once()
