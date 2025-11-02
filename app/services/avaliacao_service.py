from datetime import datetime
from app.repositories import (
    avaliacao_comportamental_item_repository,
    avaliacao_desafio_item_repository,
    colaborador_repository,
    avaliacao_comportamental_repository,
    avaliacao_desafio_repository,
    nota_final_repository
)
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import AvaliacaoComportamental, AvaliacaoDesafio
from app.utils.math_utils import calcular_media
from app.logger import logger

def salvar_avaliacao(data: dict):
    """
    Salva uma nova avaliação comportamental e de desafios, juntamente com seus itens.
    Calcula as médias e a nota final, e persiste tudo no banco de dados.
    """
    try:
        matricula = data.get("matricula")
        if not matricula:
            logger.error("Erro ao tentar salvar a avaliação: matrícula não fornecida.")
            raise ValueError("O campo 'matricula' é obrigatório.")

        logger.info(f"Iniciando salvamento de avaliação para a matrícula {matricula}...")
        colaborador_id = colaborador_repository.get_id_por_matricula(matricula)
        
        data_avaliacao = data.get("data_avaliacao")
        if not data_avaliacao:
            logger.error("Erro ao salvar avaliação: data_avaliacao não fornecida.")
            raise ValueError("O campo 'data_avaliacao' é obrigatório.")

        comportamental_itens = data.get("comportamental", [])
        desafios_itens = data.get("desafios", [])

        logger.info(f"Calculando as médias para a matrícula {matricula}...")
        media_comportamental = calcular_media([item['nota'] for item in comportamental_itens])
        media_desafio = calcular_media([item['nota'] for item in desafios_itens])

        avaliacao_comportamental = AvaliacaoComportamental(
            colaborador_id=colaborador_id,
            data_avaliacao=data_avaliacao,
            media_comportamental=media_comportamental
        )
        avaliacao_desafio = AvaliacaoDesafio(
            colaborador_id=colaborador_id,
            data_avaliacao=data_avaliacao,
            media_desafio=media_desafio
        )

        logger.info(f"Salvando avaliações comportamentais e desafios no banco para a matrícula {matricula}...")

        avaliacao_comportamental_repository.salvar_avaliacao_comportamental(
            avaliacao_comportamental,
            [{**item, "data_avaliacao": data_avaliacao} for item in comportamental_itens]
        )
        avaliacao_desafio_repository.salvar_avaliacao_desafio(
            avaliacao_desafio,
            [{**item, "data_avaliacao": data_avaliacao} for item in desafios_itens]
        )
        
        logger.info(f"Calculando e salvando a nota final para a matrícula {matricula}...")
        nota_final = nota_final_repository.salvar(
            colaborador_id,
            avaliacao_comportamental,
            avaliacao_desafio,
            data_avaliacao
        )

        db.session.commit()

        logger.info(f"Avaliação salva com sucesso para a matrícula {matricula}.")
        return {
            "media_comportamental": media_comportamental,
            "media_desafio": media_desafio,
            "nota_final": nota_final.nota_final
        }

    except IntegrityError as e:
        db.session.rollback()
        logger.exception(f"Erro de integridade ao salvar avaliação para a matrícula {matricula}: {str(e.orig)}")
        raise ValueError(f"Erro ao salvar avaliação: {str(e.orig)}")
      
def deletar_avaliacao_por_nota_final(nota_final_id):
    """
    Deleta a avaliação comportamental e de desafios associadas a uma nota final.
    """
    try:
        nota_final = nota_final_repository.get_por_id(nota_final_id)
        if not nota_final:
            logger.error(f"Nota final com ID {nota_final_id} não encontrada para deleção.")
            raise ValueError("Nota final não encontrada")

        logger.info(f"Iniciando deleção da avaliação associada à nota final ID {nota_final_id}...")
        nota_final_repository.deletar(nota_final_id)

        logger.info("Deletando avaliações comportamental e de desafios associadas...")
        if nota_final.avaliacao_comportamental_id:
            avaliacao_comportamental_item_repository.deletar(nota_final.avaliacao_comportamental_id)
            avaliacao_comportamental_repository.deletar(nota_final.avaliacao_comportamental_id)

        if nota_final.avaliacao_desafio_id:
            avaliacao_desafio_item_repository.deletar(nota_final.avaliacao_desafio_id)
            avaliacao_desafio_repository.deletar(nota_final.avaliacao_desafio_id)

        db.session.commit()
        logger.success(f"Avaliação associada à nota final ID {nota_final_id} removida com sucesso.")
        return "Avaliação removida com sucesso"
    except ValueError as e:
        db.session.rollback()
        logger.exception(f"Erro ao deletar avaliação associada à nota final ID {nota_final_id}: {str(e)}")
        raise ValueError(f"Erro ao deletar avaliação: {str(e)}")
    
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Erro interno ao deletar avaliação associada à nota final ID {nota_final_id}: {str(e)}")
        raise Exception(f"Erro interno ao deletar avaliação: {str(e)}")


