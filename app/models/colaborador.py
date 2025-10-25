from app import db

class Colaborador(db.Model):
    __tablename__ = 'tb_colaborador'

    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    data_admissao = db.Column(db.Date, nullable=False)
    cargo = db.Column(db.String(50))

    avaliacoes_comportamentais = db.relationship('AvaliacaoComportamental', backref='colaborador', lazy=True)
    avaliacoes_desafios = db.relationship('AvaliacaoDesafio', backref='colaborador', lazy=True)
    notas_finais = db.relationship('NotaFinal', backref='colaborador', lazy=True)
