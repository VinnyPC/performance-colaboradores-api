from marshmallow import Schema, fields, validates, ValidationError, post_load
# anotação: kwargs é necessário para compatibilidade com marshmallow >= 3.13
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

    @post_load
    def padronizar_nota(self, data, **kwargs):
        return data
