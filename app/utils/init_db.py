import mysql.connector
from mysql.connector import errorcode
from loguru import logger
try:
    import mysql.connector
except ModuleNotFoundError:
    from unittest import mock
    mysql = mock.MagicMock()
# Configurações da conexão
config = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "port": 3306,
}

# Nome do banco de dados
DB_NAME = "db_performance_colaboradores"

# Script SQL com a criação das tabelas
TABLES = {}
TABLES["tb_colaborador"] = """
CREATE TABLE IF NOT EXISTS tb_colaborador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    matricula VARCHAR(20) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    data_admissao DATE NOT NULL,
    cargo VARCHAR(50)
);
"""

TABLES["tb_avaliacao_comportamental"] = """
CREATE TABLE IF NOT EXISTS tb_avaliacao_comportamental (
    id INT AUTO_INCREMENT PRIMARY KEY,
    colaborador_id INT NOT NULL,
    data_avaliacao DATE NOT NULL,
    media_comportamental DECIMAL(3,2),
    FOREIGN KEY (colaborador_id) REFERENCES tb_colaborador(id)
);
"""

TABLES["tb_avaliacao_comportamental_item"] = """
CREATE TABLE IF NOT EXISTS tb_avaliacao_comportamental_item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    avaliacao_comportamental_id INT NOT NULL,
    numero_questao INT NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    nota TINYINT NOT NULL CHECK (nota BETWEEN 1 AND 5),
    data_avaliacao DATE NOT NULL,
    FOREIGN KEY (avaliacao_comportamental_id) REFERENCES tb_avaliacao_comportamental(id),
    UNIQUE(avaliacao_comportamental_id, numero_questao)
);
"""

TABLES["tb_avaliacao_desafio"] = """
CREATE TABLE IF NOT EXISTS tb_avaliacao_desafio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    colaborador_id INT NOT NULL,
    data_avaliacao DATE NOT NULL,
    media_desafio DECIMAL(3,2),
    FOREIGN KEY (colaborador_id) REFERENCES tb_colaborador(id)
);
"""

TABLES["tb_avaliacao_desafio_item"] = """
CREATE TABLE IF NOT EXISTS tb_avaliacao_desafio_item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    avaliacao_desafio_id INT NOT NULL,
    numero_desafio INT NOT NULL,
    descricao VARCHAR(100),
    nota TINYINT NOT NULL CHECK (nota BETWEEN 1 AND 5),
    data_avaliacao DATE NOT NULL,
    FOREIGN KEY (avaliacao_desafio_id) REFERENCES tb_avaliacao_desafio(id),
    UNIQUE(avaliacao_desafio_id, numero_desafio)
);
"""

TABLES["tb_nota_final"] = """
CREATE TABLE IF NOT EXISTS tb_nota_final (
    id INT AUTO_INCREMENT PRIMARY KEY,
    colaborador_id INT NOT NULL,
    avaliacao_comportamental_id INT,
    avaliacao_desafio_id INT,
    data_calculo DATE NOT NULL,
    media_comportamental DECIMAL(3,2) NOT NULL,
    media_desafio DECIMAL(3,2) NOT NULL,
    nota_final DECIMAL(3,2) NOT NULL,
    FOREIGN KEY (colaborador_id) REFERENCES tb_colaborador(id),
    FOREIGN KEY (avaliacao_comportamental_id) REFERENCES tb_avaliacao_comportamental(id),
    FOREIGN KEY (avaliacao_desafio_id) REFERENCES tb_avaliacao_desafio(id)
);
"""

def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8mb4'")
        logger.success(f"Banco de dados {DB_NAME} criado ou já existente.")
    except mysql.connector.Error as err:
        logger.error(f"Falha ao criar o banco de dados: {err}")

def create_tables(cursor):
    cursor.execute(f"USE {DB_NAME}")
    for name, ddl in TABLES.items():
        try:
            print(f"🧱 Criando tabela {name}...", end=" ")
            cursor.execute(ddl)
            logger.success("Ok")
        except mysql.connector.Error as err:
            logger.error(f"Falha ao criar a tabela {name}: {err}")

if __name__ == "__main__":
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        create_database(cursor)
        create_tables(cursor)
        cursor.close()
        cnx.close()
        logger.success("Inicialização do banco de dados concluída com sucesso.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger.error("Erro de autenticação: verifique seu usuário e senha.")
        else:
            print(err)
