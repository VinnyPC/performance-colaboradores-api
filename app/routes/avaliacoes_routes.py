from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.repositories import (
    avaliacao_comportamental_item_repository,
    avaliacao_comportamental_repository,
    avaliacao_desafio_item_repository,
    avaliacao_desafio_repository,
    colaborador_repository
)
from app.schemas import avaliacao_schema, AvaliacaoComportamentalSchema, AvaliacaoDesafioSchema
from app.services import avaliacao_service
from app.services.avaliacao_service import salvar_avaliacao
from app.logger import logger



avaliacoes_bp = Blueprint("avaliacoes", __name__, url_prefix="/avaliacoes")
avaliacao_schema = avaliacao_schema.AvaliacaoSchema()
media_comportamental_schema = AvaliacaoComportamentalSchema()
media_comportamental_schema_many = AvaliacaoComportamentalSchema(many=True)
media_desafio_schema = AvaliacaoDesafioSchema()
media_desafio_schema_many = AvaliacaoDesafioSchema(many=True)

@avaliacoes_bp.route("/comportamental", methods=["GET"])
def listar_comportamentais():
    try:
        matricula = request.args.get("matricula")
        data_inicio = request.args.get("data_inicio")
        data_fim = request.args.get("data_fim")

        if not matricula:
            return jsonify({"error": "O parâmetro 'matricula' é obrigatório"}), 400

        colaborador_id = colaborador_repository.get_id_por_matricula(matricula)

        itens = avaliacao_comportamental_item_repository.listar_por_colaborador(
            colaborador_id,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        return jsonify(itens), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404
    except Exception as e:
        logger.exception("Erro ao listar avaliações comportamentais")
        return jsonify({"error": f"Erro interno do servidor {e}"}), 500


@avaliacoes_bp.route("/desafio", methods=["GET"])
def listar_desafios():
    try:
        matricula = request.args.get("matricula")
        data_inicio = request.args.get("data_inicio")
        data_fim = request.args.get("data_fim")

        if not matricula:
            return jsonify({"error": "O parâmetro 'matricula' é obrigatório"}), 400

        colaborador_id = colaborador_repository.get_id_por_matricula(matricula)

        itens = avaliacao_desafio_item_repository.listar_por_colaborador(
            colaborador_id,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        return jsonify(itens), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404
    except Exception as e:
        logger.exception("Erro ao listar avaliações de desafios")
        return jsonify({"error": f"Erro interno do servidor {e}"}), 500
  
@avaliacoes_bp.route("/mediaFinalComportamental", methods=["GET"])
def listar_media_final_comportamental_por_matricula():
    """
    Retorna as médias finais comportamentais de um colaborador filtrando pela matrícula e período.
    """
    
    matricula = request.args.get("matricula")
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    if not matricula:
        return jsonify({"error": "O parâmetro 'matricula' é obrigatório"}), 400

    try:
        colaborador_id = colaborador_repository.get_id_por_matricula(matricula)
        avaliacoes = avaliacao_comportamental_repository.listar_por_colaborador(
            colaborador_id, data_inicio=data_inicio, data_fim=data_fim
        )
        return jsonify(media_comportamental_schema_many.dump(avaliacoes)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404


@avaliacoes_bp.route("/mediaFinalComportamental/<int:avaliacao_id>", methods=["GET"])
def get_media_final_comportamental_por_id(avaliacao_id):
    """
    Retorna a média final comportamental de uma avaliação pelo ID.
    """
    try:
        avaliacao = avaliacao_comportamental_repository.get_por_id(avaliacao_id)
        if not avaliacao:
            return jsonify({"error": "Avaliação comportamental não encontrada"}), 404
        return jsonify(media_comportamental_schema.dump(avaliacao)), 200
    except Exception as e:
        logger.exception("Erro ao obter avaliação comportamental por ID")
        return jsonify({"error": f"Erro interno do servidor {e}"}), 500


@avaliacoes_bp.route("/mediaFinalDesafio", methods=["GET"])
def listar_media_final_desafio_por_matricula():
    """
    Retorna as médias finais de desafios de um colaborador filtrando pela matrícula e período.
    """
    matricula = request.args.get("matricula")
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    if not matricula:
        return jsonify({"error": "O parâmetro 'matricula' é obrigatório"}), 400

    try:
        colaborador_id = colaborador_repository.get_id_por_matricula(matricula)
        avaliacoes = avaliacao_desafio_repository.listar_por_colaborador(
            colaborador_id, data_inicio=data_inicio, data_fim=data_fim
        )
        return jsonify(media_desafio_schema_many.dump(avaliacoes)), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404


@avaliacoes_bp.route("/mediaFinalDesafio/<int:avaliacao_id>", methods=["GET"])
def get_media_final_desafio_por_id(avaliacao_id):
    try:
        
        avaliacao = avaliacao_desafio_repository.get_por_id(avaliacao_id)
        if not avaliacao:
            return jsonify({"error": "Avaliação de desafio não encontrada"}), 404
        return jsonify(media_desafio_schema.dump(avaliacao)), 200
    except Exception as e:
        logger.exception("Erro ao obter avaliação de desafio por ID")
        return jsonify({"error": f"Erro interno do servidor {e}"}), 500


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

