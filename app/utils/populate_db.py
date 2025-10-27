from os import getenv
import mysql.connector
from datetime import date
from decimal import Decimal
from loguru import logger

# Configurações da conexão (ajuste conforme seu ambiente)
config = {
    "user": getenv("DB_USER"),
    "password": getenv("DB_PASSWORD"),
    "host": getenv("DB_HOST"),
    "port": int(getenv("DB_PORT", 3306)),
}

def populate_database():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        colaboradores = [
            ("12345", "Ana Silva", "2023-01-10", "Desenvolvedora Back-End"),
            ("67890", "Bruno Souza", "2024-03-15", "Analista de Dados"),
            ("11122", "Carla Oliveira", "2022-11-05", "Gestora de Projetos"),
        ]

        cursor.executemany("""
            INSERT IGNORE INTO tb_colaborador (matricula, nome, data_admissao, cargo)
            VALUES (%s, %s, %s, %s);
        """, colaboradores)
        logger.success("Colaboradores inseridos.")

        cursor.execute("SELECT id FROM tb_colaborador WHERE matricula='12345'")
        colaborador_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO tb_avaliacao_comportamental (colaborador_id, data_avaliacao, media_comportamental)
            VALUES (%s, %s, %s)
        """, (colaborador_id, date(2025, 10, 25), Decimal("4.0")))
        avaliacao_comportamental_id = cursor.lastrowid

        comportamentais = [
            (avaliacao_comportamental_id, 1, "Você promove um ambiente colaborativo?", 4, date(2025, 10, 25)),
            (avaliacao_comportamental_id, 2, "Você se atualiza e aprende o tempo todo?", 5, date(2025, 10, 25)),
            (avaliacao_comportamental_id, 3, "Você utiliza dados para tomar suas decisões?", 3, date(2025, 10, 25)),
            (avaliacao_comportamental_id, 4, "Você trabalha com autonomia?", 4, date(2025, 10, 25)),
        ]
        cursor.executemany("""
            INSERT INTO tb_avaliacao_comportamental_item 
            (avaliacao_comportamental_id, numero_questao, descricao, nota, data_avaliacao)
            VALUES (%s, %s, %s, %s, %s)
        """, comportamentais)
        logger.success("Itens comportamentais inseridos.")

        cursor.execute("""
            INSERT INTO tb_avaliacao_desafio (colaborador_id, data_avaliacao, media_desafio)
            VALUES (%s, %s, %s)
        """, (colaborador_id, date(2025, 10, 25), Decimal("3.5")))
        avaliacao_desafio_id = cursor.lastrowid

        desafios = [
            (avaliacao_desafio_id, 1, "Desafio A", 4, date(2025, 10, 25)),
            (avaliacao_desafio_id, 2, "Desafio B", 3, date(2025, 10, 25)),
            (avaliacao_desafio_id, 3, "Desafio C", 3, date(2025, 10, 25)),
        ]
        cursor.executemany("""
            INSERT INTO tb_avaliacao_desafio_item 
            (avaliacao_desafio_id, numero_desafio, descricao, nota, data_avaliacao)
            VALUES (%s, %s, %s, %s, %s)
        """, desafios)
        logger.success("Itens de desafios inseridos.")

        nota_final = Decimal((4.0 + 3.5) / 2)
        cursor.execute("""
            INSERT INTO tb_nota_final (
                colaborador_id,
                avaliacao_comportamental_id,
                avaliacao_desafio_id,
                data_calculo,
                media_comportamental,
                media_desafio,
                nota_final
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            colaborador_id,
            avaliacao_comportamental_id,
            avaliacao_desafio_id,
            date.today(),
            Decimal("4.0"),
            Decimal("3.5"),
            nota_final
        ))
        logger.success("Nota final inserida.")

        cnx.commit()
        logger.success("Banco de dados populado com sucesso.")

    except mysql.connector.Error as err:
        logger.error(f"Erro ao popular o banco de dados: {err}")
    finally:
        cursor.close()
        cnx.close()

if __name__ == "__main__":
    populate_database()
