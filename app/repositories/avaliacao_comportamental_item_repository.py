from app.models.avaliacao_comportamental import AvaliacaoComportamental
from app.models.avaliacao_comportamental_item import AvaliacaoComportamentalItem
from app.extensions import db
from app.schemas.avaliacao_schema import AvaliacaoComportamentalItemOutputSchema


def listar_por_colaborador(colaborador_id, data_inicio=None, data_fim=None):
    query = AvaliacaoComportamentalItem.query.join(AvaliacaoComportamental)\
        .filter(AvaliacaoComportamental.colaborador_id == colaborador_id)

    if data_inicio:
        query = query.filter(AvaliacaoComportamental.data_avaliacao >= data_inicio)
    if data_fim:
        query = query.filter(AvaliacaoComportamental.data_avaliacao <= data_fim)

    itens = query.all()
    schema = AvaliacaoComportamentalItemOutputSchema(many=True)
    return schema.dump(itens)

def get_por_id(avaliacao_id: int):
    """
    Retorna a avaliação comportamental pelo ID.
    """
    return AvaliacaoComportamental.query.filter_by(id=avaliacao_id).first()

def atualizar_itens(avaliacao: AvaliacaoComportamental, novos_itens: list):
    """
    Atualiza os itens de uma avaliação comportamental.
    """
    for item_data in novos_itens:
        numero = item_data.get("numero_questao")
        item = next((i for i in avaliacao.itens if i.numero_questao == numero), None)
        if item:
            item.descricao = item_data.get("descricao")
            item.nota = item_data.get("nota")
        else:
            novo_item = AvaliacaoComportamentalItem(
                avaliacao_comportamental_id=avaliacao.id,
                numero_questao=numero,
                descricao=item_data.get("descricao"),
                nota=item_data.get("nota")
            )
            db.session.add(novo_item)

def deletar(avaliacao_comportamental_id):
    from app.models import AvaliacaoComportamentalItem
    AvaliacaoComportamentalItem.query.filter_by(avaliacao_comportamental_id=avaliacao_comportamental_id).delete()
    db.session.flush()