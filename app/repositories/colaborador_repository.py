from app.models import Colaborador


def get_id_por_matricula(matricula: str) -> int:
    colaborador = Colaborador.query.filter_by(matricula=str(matricula)).first()
    if not colaborador:
        raise ValueError(f"Colaborador com matrícula {matricula} não encontrado.")
    return colaborador.id
