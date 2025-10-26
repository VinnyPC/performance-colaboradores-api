from app.extensions import db

class AvaliacaoDesafio(db.Model):
    __tablename__ = 'tb_avaliacao_desafio'

    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('tb_colaborador.id'), nullable=False)
    data_avaliacao = db.Column(db.Date, nullable=False)
    media_desafio = db.Column(db.Numeric(3,2))

    itens = db.relationship(
        'AvaliacaoDesafioItem',
        backref='avaliacao',
        lazy=True,
        cascade="all, delete-orphan"
    )