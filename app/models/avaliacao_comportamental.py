from app import db

class AvaliacaoComportamental(db.Model):
    __tablename__ = 'avaliacao_comportamental'

    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('tb_colaborador.id'), nullable=False)
    data_avaliacao = db.Column(db.Date, nullable=False)
    media_comportamental = db.Column(db.Numeric(3,2))

    itens = db.relationship('AvaliacaoComportamentalItem', backref='avaliacao', lazy=True, cascade="all, delete-orphan")
