from app.extensions import db
from app.models import AvaliacaoDesafio, AvaliacaoDesafioItem

def salvar_avaliacao_desafio(avaliacao, itens: list):
    db.session.add(avaliacao)
    db.session.flush()

    itens_obj = []
    for item in itens:
        itens_obj.append(AvaliacaoDesafioItem(
            avaliacao_desafio_id=avaliacao.id,
            numero_desafio=item["numero_desafio"],
            descricao=item.get("descricao"),
            nota=item["nota"],
            data_avaliacao=item["data_avaliacao"]
        ))

    db.session.add_all(itens_obj)

def get_por_id(avaliacao_id: int):
    """
    Retorna a avaliação de desafio pelo ID.
    """
    return AvaliacaoDesafio.query.filter_by(id=avaliacao_id).first()
    
from app.extensions import db
from app.models import AvaliacaoDesafio, AvaliacaoDesafioItem

def deletar(avaliacao_desafio_id):
    from app.models import AvaliacaoDesafio
    AvaliacaoDesafio.query.filter_by(id=avaliacao_desafio_id).delete()
    db.session.flush()

def listar_por_colaborador(colaborador_id, data_inicio=None, data_fim=None):
    query = db.session.query(AvaliacaoDesafio).filter_by(colaborador_id=colaborador_id)
    
    if data_inicio:
        query = query.filter(AvaliacaoDesafio.data_avaliacao >= data_inicio)
    if data_fim:
        query = query.filter(AvaliacaoDesafio.data_avaliacao <= data_fim)
    
    return query.all()