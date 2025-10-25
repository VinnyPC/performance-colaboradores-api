from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.repositories import avaliacao_comportamental_item_repository, avaliacao_comportamental_repository, avaliacao_desafio_item_repository, colaborador_repository
from app.schemas import avaliacao_schema
from app.services import avaliacao_service
from app.services.avaliacao_service import salvar_avaliacao
from app.logger import logger



avaliacoes_bp = Blueprint("avaliacoes", __name__, url_prefix="/avaliacoes")
avaliacao_schema = avaliacao_schema.AvaliacaoSchema()

@avaliacoes_bp.route("/comportamental", methods=["GET"])
def listar_comportamentais():
    matricula = request.args.get("matricula")
    if not matricula:
      
        logger.error("Matrícula não fornecida na requisição para listar avaliações comportamentais.")
        return jsonify({"error": "O parâmetro 'matricula' é obrigatório"}), 400
      
    try:
      
        logger.info(f"Obtendo ID do colaborador para a matrícula {matricula}...")
        colaborador_id = colaborador_repository.get_id_por_matricula(matricula)
        logger.info(f"ID encontrado. Listando avaliações comportamentais para a matrícula {matricula}...")
        itens = avaliacao_comportamental_item_repository.listar_por_colaborador(colaborador_id)
        return jsonify(itens), 200
      
    except ValueError as err:
        logger.error(f"Erro ao listar avaliações comportamentais: {err}")
        return jsonify({"error": str(err)}), 404
      
@avaliacoes_bp.route("/desafio", methods=["GET"])
def listar_desafios():
    matricula = request.args.get("matricula")
    if not matricula:
        return jsonify({"error": "O parâmetro 'matricula' é obrigatório"}), 400
    try:
        colaborador_id = colaborador_repository.get_id_por_matricula(matricula)
        itens = avaliacao_desafio_item_repository.listar_por_colaborador(colaborador_id)
        return jsonify(itens), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404


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

@avaliacoes_bp.route("/<int:avaliacao_id>", methods=["PUT"])
def atualizar_avaliacao(avaliacao_id):
    try:
        data = avaliacao_schema.load(request.json, partial=True)  
        resultado = avaliacao_service.atualizar_avaliacao(avaliacao_id, data)
        return jsonify(resultado), 200

    except ValidationError as err:
        return jsonify(err.messages), 400

    except ValueError as err:
        return jsonify({"error": str(err)}), 404

    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor {e}"}), 500
      
@avaliacoes_bp.route("/nota_final/<int:nota_final_id>", methods=["DELETE"])
def deletar_por_nota_final(nota_final_id):
    try:
        resultado = avaliacao_service.deletar_avaliacao_por_nota_final(nota_final_id)
        return jsonify({"message": resultado}), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404

