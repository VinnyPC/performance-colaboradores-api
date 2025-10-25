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
from app import db
from app.models import AvaliacaoComportamental, AvaliacaoDesafio
from app.utils.math_utils import calcular_media

def salvar_avaliacao(data: dict):
    try:
        matricula = data.get("matricula")
        if not matricula:
            raise ValueError("O campo 'matricula' é obrigatório.")

        colaborador_id = colaborador_repository.get_id_por_matricula(matricula)
        
        data_avaliacao = data.get("data_avaliacao")

        comportamental_itens = data.get("comportamental", [])
        desafios_itens = data.get("desafios", [])

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

        avaliacao_comportamental_repository.salvar_avaliacao_comportamental(avaliacao_comportamental, comportamental_itens)
        avaliacao_desafio_repository.salvar_avaliacao_desafio(avaliacao_desafio, desafios_itens)
        nota_final = nota_final_repository.salvar(colaborador_id, avaliacao_comportamental, avaliacao_desafio, data_avaliacao)

        db.session.commit()

        return {
            "media_comportamental": media_comportamental,
            "media_desafio": media_desafio,
            "nota_final": nota_final.nota_final
        }
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Erro ao salvar avaliação: {str(e.orig)}")
    
def atualizar_avaliacao(avaliacao_id, data):
    avaliacao = avaliacao_comportamental_repository.get_por_id(avaliacao_id)
    if not avaliacao:
        raise ValueError("Avaliação comportamental não encontrada")
    avaliacao_comportamental_item_repository.atualizar_itens(avaliacao, data.get("comportamental"))

    avaliacao_desafio = avaliacao_desafio_repository.get_por_colaborador_e_data(
        colaborador_id=avaliacao.colaborador_id,
        data_avaliacao=data.get("data_avaliacao")
    )
    if not avaliacao_desafio:
        raise ValueError("Avaliação de desafios não encontrada")

    avaliacao_desafio_item_repository.atualizar_itens(avaliacao_desafio, data.get("desafios"))

    media_comportamental = calcular_media([item.nota for item in avaliacao.itens])
    media_desafio = calcular_media([item.nota for item in avaliacao_desafio.itens])

    avaliacao.media_comportamental = media_comportamental
    avaliacao_desafio.media_desafio = media_desafio
    nota_final_repository.atualizar_nota_final(
        colaborador_id=avaliacao.colaborador_id,
        media_comportamental=media_comportamental,
        media_desafio=media_desafio
    )

    db.session.commit()

    return {
        "media_comportamental": media_comportamental,
        "media_desafio": media_desafio
    }
    
def deletar_avaliacao_por_nota_final(nota_final_id):
    nota_final = nota_final_repository.get_por_id(nota_final_id)
    if not nota_final:
        raise ValueError("Nota final não encontrada")

    nota_final_repository.deletar(nota_final_id)

    if nota_final.avaliacao_comportamental_id:
        avaliacao_comportamental_item_repository.deletar(nota_final.avaliacao_comportamental_id)
        avaliacao_comportamental_repository.deletar(nota_final.avaliacao_comportamental_id)

    if nota_final.avaliacao_desafio_id:
        avaliacao_desafio_item_repository.deletar(nota_final.avaliacao_desafio_id)
        avaliacao_desafio_repository.deletar(nota_final.avaliacao_desafio_id)

    db.session.commit()
    return "Avaliação removida com sucesso"


