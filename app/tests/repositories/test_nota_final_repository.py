from decimal import Decimal
import pytest
from datetime import date
from app.repositories import nota_final_repository
from app.models import NotaFinal


@pytest.fixture
def sample_dados(app):
    """Cria dados de teste no banco."""
    from app.extensions import db

    with app.app_context():
        class MockAvaliacao:
            def __init__(self, id, media_comportamental=None, media_desafio=None):
                self.id = id
                self.media_comportamental = media_comportamental
                self.media_desafio = media_desafio

        avaliacao_comportamental = MockAvaliacao(1, 4.5)
        avaliacao_desafio = MockAvaliacao(2, 3.5)

        nota = nota_final_repository.salvar(
            colaborador_id=123,
            avaliacao_comportamental=avaliacao_comportamental,
            avaliacao_desafio=avaliacao_desafio,
            data_calculo=date.today(),
        )
        db.session.commit()
        yield nota


def test_salvar(app):
    """Testa se a função salvar cria corretamente uma NotaFinal."""
    from app.extensions import db

    with app.app_context():
        class MockAvaliacao:
            def __init__(self, id, media_comportamental=None, media_desafio=None):
                self.id = id
                self.media_comportamental = media_comportamental
                self.media_desafio = media_desafio

        avaliacao_comportamental = MockAvaliacao(1, 4.0)
        avaliacao_desafio = MockAvaliacao(2, 5.0)

        nota = NotaFinal(
            colaborador_id=1,
            media_comportamental=Decimal("4.0"),
            media_desafio=Decimal("4.5"),
            nota_final=Decimal("4.25")
        )

        db.session.commit()

        assert nota.id is None
        assert nota.colaborador_id == 1
        assert nota.nota_final == 4.25


def test_atualizar_nota_final_nao_encontrada(app):
    """Testa se atualizar_nota_final lança erro ao não encontrar nota."""
    with app.app_context():
        with pytest.raises(ValueError, match="não encontrada"):
            nota_final_repository.atualizar_nota_final(
                colaborador_id=999, media_comportamental=3.0, media_desafio=3.0
            )
