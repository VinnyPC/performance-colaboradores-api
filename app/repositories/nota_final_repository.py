from app.extensions import db
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


def atualizar_nota_final(colaborador_id, media_comportamental, media_desafio):
    """
    Atualiza a nota final de um colaborador com base nas novas médias.
    """
    nota_final = NotaFinal.query.filter_by(colaborador_id=colaborador_id).first()
    if not nota_final:
        raise ValueError(f"Nota final para o colaborador {colaborador_id} não encontrada")

    nota_final.media_comportamental = media_comportamental
    nota_final.media_desafio = media_desafio
    nota_final.nota_final = round((media_comportamental + media_desafio) / 2, 1)

    db.session.add(nota_final)
    return nota_final

def get_por_id(nota_final_id):
    return NotaFinal.query.filter_by(id=nota_final_id).first()

def listar_todos():
    """
    Retorna todos os registros da tabela NotaFinal.
    """
    return NotaFinal.query.all()

def listar_por_colaborador(colaborador_id: int):
    """
    Retorna todas as notas finais de um colaborador.
    """
    return NotaFinal.query.filter_by(colaborador_id=colaborador_id).all()

def deletar(nota_final_id):
    NotaFinal.query.filter_by(id=nota_final_id).delete()
    db.session.flush()
    
    
