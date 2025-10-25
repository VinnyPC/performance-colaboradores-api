from app.models.avaliacao_comportamental import AvaliacaoComportamental
from app.models.avaliacao_comportamental_item import AvaliacaoComportamentalItem
from app import db


def listar_por_colaborador(colaborador_id):
    resultados = (
        AvaliacaoComportamentalItem.query
        .join(AvaliacaoComportamental)
        .filter(AvaliacaoComportamental.colaborador_id == colaborador_id)
        .order_by(AvaliacaoComportamental.data_avaliacao.desc(), AvaliacaoComportamentalItem.numero_questao)
        .all()
    )
    output = []
    for item in resultados:
        output.append({
            "id": item.id,
            "avaliacao_id": item.avaliacao_comportamental_id,
            "numero_questao": item.numero_questao,
            "descricao": item.descricao,
            "nota": item.nota,
            "data_avaliacao": item.avaliacao.data_avaliacao.isoformat()
        })
    return output

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