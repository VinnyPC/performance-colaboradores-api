from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.schemas import avaliacao_schema
from app.services.avaliacao_service import salvar_avaliacao

avaliacoes_bp = Blueprint("avaliacoes", __name__, url_prefix="/avaliacoes")
avaliacao_schema = avaliacao_schema.AvaliacaoSchema()

@avaliacoes_bp.route("", methods=["POST"])
def criar_avaliacao():
    try:
        data = avaliacao_schema.load(request.json)
        resultado = salvar_avaliacao(data)
        return jsonify(resultado), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
