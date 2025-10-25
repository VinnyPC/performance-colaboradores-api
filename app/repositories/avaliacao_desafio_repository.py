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
