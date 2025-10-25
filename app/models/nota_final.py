from app.extensions import db

class NotaFinal(db.Model):
    __tablename__ = 'tb_nota_final'

    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('tb_colaborador.id'), nullable=False)
    avaliacao_comportamental_id = db.Column(db.Integer, db.ForeignKey('avaliacao_comportamental.id'))
    avaliacao_desafio_id = db.Column(db.Integer, db.ForeignKey('avaliacao_desafio.id'))
    data_calculo = db.Column(db.Date, nullable=False)
    media_comportamental = db.Column(db.Numeric(3,2), nullable=False)
    media_desafio = db.Column(db.Numeric(3,2), nullable=False)
    nota_final = db.Column(db.Numeric(3,2), nullable=False)
