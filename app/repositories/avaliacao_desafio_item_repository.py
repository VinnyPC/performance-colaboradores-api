from app.models.avaliacao_desafio import AvaliacaoDesafio
from app.models.avaliacao_desafio_item import AvaliacaoDesafioItem
from app.extensions import db


def listar_por_colaborador(colaborador_id):
    """
    Retorna todas as avaliações de desafios de um colaborador específico
    """
    resultados = (
        AvaliacaoDesafioItem.query
        .join(AvaliacaoDesafio)
        .filter(AvaliacaoDesafio.colaborador_id == colaborador_id)
        .order_by(AvaliacaoDesafio.data_avaliacao.desc(), AvaliacaoDesafioItem.numero_desafio)
        .all()
    )
    output = []
    for item in resultados:
        output.append({
            "id": item.id,
            "avaliacao_id": item.avaliacao_desafio_id,
            "numero_desafio": item.numero_desafio,
            "descricao": item.descricao,
            "nota": item.nota,
            "data_avaliacao": item.avaliacao.data_avaliacao.isoformat()
        })
    return output


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

