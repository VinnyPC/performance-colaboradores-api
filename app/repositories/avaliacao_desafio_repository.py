from app import db
from app.models import AvaliacaoDesafio, AvaliacaoDesafioItem

def salvar_avaliacao_desafio(avaliacao: AvaliacaoDesafio, itens: list):
    """
    Persiste a avaliação de desafios e seus itens no banco.
    """
    db.session.add(avaliacao)
    db.session.flush() 

    for item in itens:
        db.session.add(AvaliacaoDesafioItem(
            avaliacao_desafio_id=avaliacao.id,
            numero_desafio=item['numero_desafio'],
            descricao=item.get('descricao'),
            nota=item['nota']
        ))

    return avaliacao

def get_por_id(avaliacao_id: int):
    """
    Retorna a avaliação de desafio pelo ID.
    """
    return AvaliacaoDesafio.query.filter_by(id=avaliacao_id).first()

def get_por_colaborador_e_data(colaborador_id, data_avaliacao):
    """
    Retorna a AvaliacaoDesafio de um colaborador em uma data específica.
    """
    return AvaliacaoDesafio.query.filter_by(
        colaborador_id=colaborador_id,
        data_avaliacao=data_avaliacao
    ).first()
    
from app import db
from app.models import AvaliacaoDesafio, AvaliacaoDesafioItem

def deletar(avaliacao_desafio_id):
    from app.models import AvaliacaoDesafio
    AvaliacaoDesafio.query.filter_by(id=avaliacao_desafio_id).delete()
    db.session.flush()

