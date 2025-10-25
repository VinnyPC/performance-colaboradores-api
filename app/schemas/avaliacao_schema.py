from marshmallow import Schema, fields, validates, ValidationError, post_load, validate

# Importante: é preciso usar **kwargs para marshmallow>=3.13
class AvaliacaoComportamentalItemSchema(Schema):
    numero_questao = fields.Integer(required=True)
    descricao = fields.String(required=True)
    nota = fields.Integer(required=True)

    @validates("nota")
    def validar_nota(self, value, **kwargs):
        if not (1 <= value <= 5):
            raise ValidationError("Nota deve estar entre 1 e 5")

class AvaliacaoDesafioItemSchema(Schema):
    numero_desafio = fields.Integer(required=True)
    descricao = fields.String(required=False, allow_none=True)
    nota = fields.Integer(required=True)

    @validates("nota")
    def validar_nota(self, value, **kwargs):
        if not (1 <= value <= 5):
            raise ValidationError("Nota deve estar entre 1 e 5")

class AvaliacaoSchema(Schema):
    matricula = fields.String(required=True)
    data_avaliacao = fields.Date(required=True)
    comportamental = fields.List(fields.Nested(AvaliacaoComportamentalItemSchema), required=True)
    desafios = fields.List(fields.Nested(AvaliacaoDesafioItemSchema), required=True)

    @validates("comportamental")
    def validar_comportamental(self, value, **kwargs):
        if len(value) != 4:
            raise ValidationError("A avaliação comportamental deve conter exatamente 4 itens")
        numeros = [item["numero_questao"] for item in value]
        if len(numeros) != len(set(numeros)):
            raise ValidationError("Não pode haver questões repetidas na avaliação comportamental")

    @validates("desafios")
    def validar_desafios(self, value, **kwargs):
        if not (2 <= len(value) <= 4):
            raise ValidationError("A avaliação de desafios deve conter entre 2 e 4 itens")
        numeros = [item["numero_desafio"] for item in value]
        if len(numeros) != len(set(numeros)):
            raise ValidationError("Não pode haver desafios repetidos na avaliação de desafios")

    @post_load
    def padronizar_nota(self, data, **kwargs):
        return data
    
class AvaliacaoItemSchema(Schema):
    numero_questao = fields.Integer(required=False)
    numero_desafio = fields.Integer(required=False)
    descricao = fields.String(required=True)
    nota = fields.Integer(required=True, validate=validate.Range(min=1, max=5))

class AvaliacaoUpdateSchema(Schema):
    matricula = fields.String(required=True)
    data_avaliacao = fields.Date(required=True)
    comportamental = fields.List(fields.Nested(AvaliacaoItemSchema), required=False)
    desafios = fields.List(fields.Nested(AvaliacaoItemSchema), required=False)
