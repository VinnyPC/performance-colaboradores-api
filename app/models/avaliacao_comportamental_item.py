from app.extensions import db

class AvaliacaoComportamentalItem(db.Model):
    __tablename__ = 'avaliacao_comportamental_item'

    id = db.Column(db.Integer, primary_key=True)
    avaliacao_comportamental_id = db.Column(db.Integer, db.ForeignKey('avaliacao_comportamental.id'), nullable=False)
    numero_questao = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    nota = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('avaliacao_comportamental_id', 'numero_questao', name='uq_comportamental_item'),
    )
