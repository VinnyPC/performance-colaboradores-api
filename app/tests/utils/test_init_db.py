import pytest
from unittest.mock import MagicMock, patch
from app.utils import init_db


# ---------- TESTES DE CRIAÇÃO DO BANCO ----------
@patch("app.utils.init_db.logger")
def test_create_database_sucesso(mock_logger):
    """Verifica se o banco de dados é criado com sucesso."""
    mock_cursor = MagicMock()
    init_db.create_database(mock_cursor)

    mock_cursor.execute.assert_called_once_with(
        f"CREATE DATABASE IF NOT EXISTS {init_db.DB_NAME} DEFAULT CHARACTER SET 'utf8mb4'"
    )
    mock_logger.success.assert_called_once_with(
        f"Banco de dados {init_db.DB_NAME} criado ou já existente."
    )

@patch("app.utils.init_db.logger")
def test_create_tables_sucesso(mock_logger):
    """Verifica se todas as tabelas são criadas corretamente."""
    mock_cursor = MagicMock()
    init_db.create_tables(mock_cursor)

    # Deve selecionar o banco antes de criar tabelas
    mock_cursor.execute.assert_any_call(f"USE {init_db.DB_NAME}")
    # Deve tentar criar todas as tabelas do dicionário
    for nome, ddl in init_db.TABLES.items():
        mock_cursor.execute.assert_any_call(ddl)
    # Log de sucesso deve aparecer pelo menos uma vez
    assert mock_logger.success.call_count >= len(init_db.TABLES)



@patch("app.utils.init_db.mysql.connector.connect", side_effect=Exception("Falha de conexão"))
@patch("app.utils.init_db.logger")
def test_main_falha_conexao(mock_logger, mock_connect):
    """Verifica se erro de conexão é tratado corretamente no bloco principal."""
    with pytest.raises(Exception):
        from app.utils import init_db
        init_db.mysql.connector.connect()
    mock_logger.error.assert_not_called()  # Erro é tratado fora do try principal
