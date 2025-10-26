import pytest
from app import create_app
from app.extensions import db as _db
from app.models import Colaborador, AvaliacaoComportamental, AvaliacaoDesafio, NotaFinal
from decimal import Decimal
import datetime

@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(scope="function")
def db_session(app):
    connection = _db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = _db.create_scoped_session(options=options)

    _db.session = session
    yield session

    transaction.rollback()
    connection.close()
    session.remove()

@pytest.fixture
def sample_colaboradores(db_session):
    c1 = Colaborador(matricula="001", nome="Ana Silva", data_admissao=datetime.date(2025,1,1), cargo="Analista")
    c2 = Colaborador(matricula="002", nome="Bruno Souza", data_admissao=datetime.date(2025,2,1), cargo="Desenvolvedor")
    db_session.add_all([c1, c2])
    db_session.commit()
    return [c1, c2]

@pytest.fixture
def sample_avaliacao_comportamental(db_session, sample_colaboradores):
    aval = AvaliacaoComportamental(
        colaborador_id=sample_colaboradores[0].id,
        data_avaliacao=datetime.date(2025,10,25),
        media_comportamental=Decimal("3.5")
    )
    db_session.add(aval)
    db_session.commit()
    return aval

@pytest.fixture
def sample_avaliacao_desafio(db_session, sample_colaboradores):
    aval = AvaliacaoDesafio(
        colaborador_id=sample_colaboradores[0].id,
        data_avaliacao=datetime.date(2025,10,25)
    )
    db_session.add(aval)
    db_session.commit()
    return aval

@pytest.fixture
def sample_notas_finais(db_session, sample_colaboradores):
    nf1 = NotaFinal(
        colaborador_id=sample_colaboradores[0].id,
        avaliacao_comportamental_id=1,
        avaliacao_desafio_id=1,
        data_calculo=datetime.date.today(),
        media_comportamental=Decimal("4.5"),
        media_desafio=Decimal("3.5"),
        nota_final=Decimal("4.0")
    )
    nf2 = NotaFinal(
        colaborador_id=sample_colaboradores[1].id,
        avaliacao_comportamental_id=2,
        avaliacao_desafio_id=2,
        data_calculo=datetime.date.today(),
        media_comportamental=Decimal("5.0"),
        media_desafio=Decimal("4.0"),
        nota_final=Decimal("4.5")
    )
    db_session.add_all([nf1, nf2])
    db_session.commit()
    return [nf1, nf2]
