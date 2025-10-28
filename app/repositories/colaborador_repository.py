from app.models import Colaborador
from app.extensions import db
from datetime import datetime


def get_id_por_matricula(matricula: str) -> int:
    colaborador = Colaborador.query.filter_by(matricula=str(matricula)).first()
    if not colaborador:
        raise ValueError(f"Colaborador com matrícula {matricula} não encontrado.")
    return colaborador.id

def listar_todos():
    colaboradores = Colaborador.query.all()
    return [
        {
            "id": c.id,
            "nome": c.nome,
            "matricula": c.matricula,
            "cargo": c.cargo,
            "cargo": c.cargo
        }
        for c in colaboradores
    ]
    
def criar(dados):
    novo = Colaborador(
        matricula=dados.get("matricula"),
        nome=dados.get("nome"),
        data_admissao=datetime.strptime(dados.get("data_admissao"), "%Y-%m-%d").date(),
        cargo=dados.get("cargo")
    )
    db.session.add(novo)
    db.session.commit()
    return {
        "id": novo.id,
        "matricula": novo.matricula,
        "nome": novo.nome,
        "cargo": novo.cargo,
        "data_admissao": novo.data_admissao.strftime("%Y-%m-%d"),
    }
    
def atualizar(colaborador_id, dados):
    colaborador = Colaborador.query.get(colaborador_id)
    if not colaborador:
        raise ValueError("Colaborador não encontrado.")

    colaborador.nome = dados.get("nome", colaborador.nome)
    colaborador.cargo = dados.get("cargo", colaborador.cargo)
    if "data_admissao" in dados:
        from datetime import datetime
        colaborador.data_admissao = datetime.strptime(dados["data_admissao"], "%Y-%m-%d").date()

    db.session.commit()

    return {
        "id": colaborador.id,
        "matricula": colaborador.matricula,
        "nome": colaborador.nome,
        "cargo": colaborador.cargo,
        "data_admissao": colaborador.data_admissao.strftime("%Y-%m-%d"),
    }

def deletar(colaborador_id):
    colaborador = Colaborador.query.get(colaborador_id)
    if not colaborador:
        raise ValueError("Colaborador não encontrado.")

    db.session.delete(colaborador)
    db.session.commit()

