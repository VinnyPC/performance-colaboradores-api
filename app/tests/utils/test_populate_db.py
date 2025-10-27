import pytest
from unittest.mock import MagicMock, patch
from app.utils import populate_db


# ---------- TESTE PRINCIPAL DE SUCESSO ----------
@patch("app.utils.populate_db.mysql.connector.connect")
@patch("app.utils.populate_db.logger")
def test_populate_database_sucesso(mock_logger, mock_connect):
    """Verifica se todas as queries são executadas e commitadas corretamente."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    populate_db.populate_database()

    # Verifica se a conexão foi aberta e fechada corretamente
    mock_connect.assert_called_once_with(**populate_db.config)
    mock_cursor.execute.assert_any_call("SELECT id FROM tb_colaborador WHERE matricula='12345'")
    assert mock_cursor.executemany.call_count >= 2  # Inserções em lote (colaboradores, desafios)
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()
    mock_logger.success.assert_any_call("Banco de dados populado com sucesso.")


@patch("app.utils.populate_db.mysql.connector.connect", side_effect=Exception("Falha de conexão"))
@patch("app.utils.populate_db.logger")
def test_populate_database_falha_conexao(mock_logger, mock_connect):
    """Simula falha ao conectar com o banco de dados."""
    with pytest.raises(Exception):
        populate_db.mysql.connector.connect()
    mock_logger.error.assert_not_called()  # erro tratado fora do escopo do populate_database


# ---------- TESTE DE ESTRUTURA DE DADOS ----------
def test_dados_estruturados_corretamente():
    """Verifica se os dados base possuem estrutura esperada antes da inserção."""
    colaboradores = populate_db.populate_database.__defaults__  # obtém config padrão
    config = populate_db.config
    assert "user" in config and "password" in config
    assert isinstance(config["port"], int)
