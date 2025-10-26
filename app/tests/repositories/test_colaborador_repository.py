from datetime import date
import pytest
from app.repositories import colaborador_repository
from app.models import Colaborador
from app.extensions import db

@pytest.fixture
def sample_colaboradores(app):
    """Cria colaboradores de teste no banco."""
    from app.models import Colaborador
    from app.extensions import db
    from datetime import date

    with app.app_context():
        db.session.query(Colaborador).delete()
        db.session.flush()

        c1 = Colaborador(
            nome="Ana Silva",
            matricula="001",  
            cargo="Analista",
            data_admissao=date(2022, 1, 10)
        )
        c2 = Colaborador(
            nome="Bruno Souza",
            matricula="002",  
            cargo="Desenvolvedor",
            data_admissao=date(2021, 6, 5)
        )

        db.session.add_all([c1, c2])
        db.session.commit()

        yield [c1, c2]


def test_get_id_por_matricula_sucesso(app, sample_colaboradores):
    """Testa se retorna o ID correto ao buscar por matrícula."""
    with app.app_context():
        colaborador_id = colaborador_repository.get_id_por_matricula("001")
        assert isinstance(colaborador_id, int)
        assert colaborador_id == sample_colaboradores[0].id


def test_get_id_por_matricula_nao_encontrado(app):
    """Testa se lança erro ao buscar uma matrícula inexistente."""
    with app.app_context():
        with pytest.raises(ValueError, match="não encontrado"):
            colaborador_repository.get_id_por_matricula("999")


def test_listar_todos(app, sample_colaboradores):
    """Testa se listar_todos retorna todos os colaboradores corretamente."""
    with app.app_context():
        resultado = colaborador_repository.listar_todos()

        assert isinstance(resultado, list)
        assert len(resultado) >= 2
        assert all("id" in c and "nome" in c and "matricula" in c and "cargo" in c for c in resultado)
        assert resultado[0]["nome"] == "Ana Silva"
        assert resultado[1]["nome"] == "Bruno Souza"
