from app import db
from app.models import NotaFinal
from app.utils.math_utils import calcular_media

def salvar(colaborador_id, avaliacao_comportamental, avaliacao_desafio, data_calculo):
    """
    Persiste a nota final no banco.
    """
    nota_final_valor = calcular_media([
        avaliacao_comportamental.media_comportamental,
        avaliacao_desafio.media_desafio
    ])
    nota_final = NotaFinal(
        colaborador_id=colaborador_id,
        avaliacao_comportamental_id=avaliacao_comportamental.id,
        avaliacao_desafio_id=avaliacao_desafio.id,
        data_calculo=data_calculo,
        media_comportamental=avaliacao_comportamental.media_comportamental,
        media_desafio=avaliacao_desafio.media_desafio,
        nota_final=nota_final_valor
    )
    db.session.add(nota_final)
    return nota_final
