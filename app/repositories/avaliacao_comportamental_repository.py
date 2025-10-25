from app import db
from app.models import AvaliacaoComportamental, AvaliacaoComportamentalItem

def salvar_avaliacao_comportamental(avaliacao: AvaliacaoComportamental, itens: list):
    """
    Persiste a avaliação comportamental e seus itens no banco.
    """
    db.session.add(avaliacao)
    db.session.flush()

    for item in itens:
        db.session.add(AvaliacaoComportamentalItem(
            avaliacao_comportamental_id=avaliacao.id,
            numero_questao=item['numero_questao'],
            descricao=item['descricao'],
            nota=item['nota']
        ))

    return avaliacao
