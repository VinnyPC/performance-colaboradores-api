from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime

def validar_data(valor):
    try:
        datetime.strptime(valor, "%Y-%m-%d")
    except ValueError:
        raise ValidationError("Data deve estar no formato YYYY-MM-DD")

class ColaboradorInputSchema(Schema):
    matricula = fields.Str(required=True, validate=validate.Length(min=3, max=20))
    nome = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    data_admissao = fields.Str(required=True, validate=validar_data)
    cargo = fields.Str(required=False, validate=validate.Length(max=50))

class ColaboradorOutputSchema(Schema):
    id = fields.Int()
    matricula = fields.Str()
    nome = fields.Str()
    data_admissao = fields.Str()
    cargo = fields.Str()
