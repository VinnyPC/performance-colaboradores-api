from app.models.avaliacao_desafio import AvaliacaoDesafio
from app.models.avaliacao_desafio_item import AvaliacaoDesafioItem
from app.extensions import db
from app.schemas.avaliacao_schema import AvaliacaoDesafioItemOutputSchema


def listar_por_colaborador(colaborador_id, data_inicio=None, data_fim=None):
    query = AvaliacaoDesafioItem.query.join(AvaliacaoDesafio)\
        .filter(AvaliacaoDesafio.colaborador_id == colaborador_id)

    if data_inicio:
        query = query.filter(AvaliacaoDesafio.data_avaliacao >= data_inicio)
    if data_fim:
        query = query.filter(AvaliacaoDesafio.data_avaliacao <= data_fim)

    itens = query.all()
    schema = AvaliacaoDesafioItemOutputSchema(many=True)
    return schema.dump(itens)


def get_por_id(avaliacao_id: int):
    """
    Retorna a avaliação de desafio pelo ID
    """
    return AvaliacaoDesafio.query.filter_by(id=avaliacao_id).first()

def atualizar_itens(avaliacao: AvaliacaoDesafio, novos_itens: list):
    """
    Atualiza os itens de uma avaliação de desafios
    """
    for item_data in novos_itens:
        numero = item_data.get("numero_desafio")
        item = next((i for i in avaliacao.itens if i.numero_desafio == numero), None)
        if item:
            item.descricao = item_data.get("descricao")
            item.nota = item_data.get("nota")
        else:
            novo_item = AvaliacaoDesafioItem(
                avaliacao_desafio_id=avaliacao.id,
                numero_desafio=numero,
                descricao=item_data.get("descricao"),
                nota=item_data.get("nota")
            )
            db.session.add(novo_item)
    
def deletar(avaliacao_desafio_id):
    from app.models import AvaliacaoDesafioItem
    AvaliacaoDesafioItem.query.filter_by(avaliacao_desafio_id=avaliacao_desafio_id).delete()
    db.session.flush()

