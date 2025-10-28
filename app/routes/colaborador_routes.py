from flask import Blueprint, jsonify, request
from app.repositories import colaborador_repository
from app.services import colaborador_service
from marshmallow import ValidationError
from loguru import logger

colaboradores_bp = Blueprint("colaboradores", __name__, url_prefix="/colaboradores")

@colaboradores_bp.route("", methods=["GET"])
def listar_colaboradores():
    try:
        colaboradores = colaborador_service.listar_colaboradores()
        return jsonify(colaboradores), 200
    except Exception as e:
        logger.exception("Erro ao listar colaboradores")
        return jsonify({"error": str(e)}), 500


@colaboradores_bp.route("", methods=["POST"])
def criar_colaborador():
    try:
        dados = request.get_json()
        novo_colaborador = colaborador_service.criar_colaborador(dados)
        return jsonify(novo_colaborador), 201
    except ValidationError as err:
        logger.warning(f"Erro de validação: {err.messages}")
        return jsonify({"erros": err.messages}), 400
    except Exception as e:
        logger.exception("Erro ao criar colaborador")
        return jsonify({"error": str(e)}), 500


@colaboradores_bp.route("", methods=["PUT"])
def atualizar_colaborador():
    try:
        matricula = request.args.get("matricula")
        if not matricula:
            return jsonify({"error": "O parâmetro 'matricula' é obrigatório"}), 400

        dados = request.get_json()
        colaborador_id = colaborador_repository.get_id_por_matricula(matricula)

        atualizado = colaborador_service.atualizar_colaborador(colaborador_id, dados)
        return jsonify(atualizado), 200

    except ValidationError as err:
        logger.warning(f"Erro de validação: {err.messages}")
        return jsonify({"erros": err.messages}), 400
    except ValueError as err:
        logger.warning(f"Erro: {err}")
        return jsonify({"error": str(err)}), 404
    except Exception as e:
        logger.exception("Erro ao atualizar colaborador")
        return jsonify({"error": str(e)}), 500


@colaboradores_bp.route("", methods=["DELETE"])
def deletar_colaborador():
    try:
        matricula = request.args.get("matricula")
        if not matricula:
            return jsonify({"error": "O parâmetro 'matricula' é obrigatório"}), 400

        colaborador_id = colaborador_repository.get_id_por_matricula(matricula)
        colaborador_service.deletar_colaborador(colaborador_id)

        return jsonify({"mensagem": f"Colaborador com matrícula {matricula} deletado com sucesso"}), 200

    except ValueError as err:
        logger.warning(f"Erro: {err}")
        return jsonify({"error": str(err)}), 404
    except Exception as e:
        logger.exception("Erro ao deletar colaborador")
        return jsonify({"error": str(e)}), 500
