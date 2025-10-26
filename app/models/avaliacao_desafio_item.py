from app.extensions import db

class AvaliacaoDesafioItem(db.Model):
    __tablename__ = 'tb_avaliacao_desafio_item'

    id = db.Column(db.Integer, primary_key=True)
    avaliacao_desafio_id = db.Column(
        db.Integer, db.ForeignKey('tb_avaliacao_desafio.id'), nullable=False
    )
    numero_desafio = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(255))
    nota = db.Column(db.Integer, nullable=False)
    data_avaliacao = db.Column(db.Date, nullable=False)  

    __table_args__ = (
        db.UniqueConstraint('avaliacao_desafio_id', 'numero_desafio', name='uq_desafio_item'),
    )
