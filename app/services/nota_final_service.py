from app.repositories import nota_final_repository

def listar_notas_finais():
    """
    Busca todas as notas finais e formata em dicionário.
    """
    notas = nota_final_repository.listar_todos()
    resultado = []
    for nota in notas:
        resultado.append({
            "id": nota.id,
            "colaborador_id": nota.colaborador_id,
            "avaliacao_comportamental_id": nota.avaliacao_comportamental_id,
            "avaliacao_desafio_id": nota.avaliacao_desafio_id,
            "media_comportamental": float(nota.media_comportamental),
            "media_desafio": float(nota.media_desafio),
            "nota_final": float(nota.nota_final),
            "data_calculo": nota.data_calculo.isoformat()
        })
    return resultado