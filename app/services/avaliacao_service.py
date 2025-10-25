from datetime import datetime
from app.repositories import (
    colaborador_repository,
    avaliacao_comportamental_repository,
    avaliacao_desafio_repository,
    nota_final_repository
)
from app import db
from app.models import AvaliacaoComportamental, AvaliacaoDesafio
from app.utils.math_utils import calcular_media

def salvar_avaliacao(data: dict):
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
