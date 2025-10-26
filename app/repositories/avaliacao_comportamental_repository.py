from app.extensions import db
from app.models import AvaliacaoComportamental, AvaliacaoComportamentalItem

def salvar_avaliacao_comportamental(avaliacao, itens: list):
    db.session.add(avaliacao)
    db.session.flush() 

    itens_obj = []
    for item in itens:
        itens_obj.append(AvaliacaoComportamentalItem(
            avaliacao_comportamental_id=avaliacao.id,
            numero_questao=item["numero_questao"],
            descricao=item["descricao"],
            nota=item["nota"],
            data_avaliacao=item["data_avaliacao"]  
        ))

    db.session.add_all(itens_obj)

def listar_por_colaborador(colaborador_id):
    results = (
        AvaliacaoComportamental.query
        .filter_by(colaborador_id=colaborador_id)
        .order_by(AvaliacaoComportamental.data_avaliacao.desc())
        .all()
    )
    output = []
    for a in results:
        output.append({
            "id": a.id,
            "data_avaliacao": a.data_avaliacao.isoformat(),
            "media_comportamental": a.media_comportamental
        })
    return output

def get_por_id(avaliacao_id: int):
    """
    Retorna a avaliação comportamental pelo ID.
    """
    return AvaliacaoComportamental.query.filter_by(id=avaliacao_id).first()

def deletar(avaliacao_comportamental_id):
    from app.models import AvaliacaoComportamental
    AvaliacaoComportamental.query.filter_by(id=avaliacao_comportamental_id).delete()
    db.session.flush()



