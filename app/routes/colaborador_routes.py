from flask import Blueprint, jsonify
from app.services import colaborador_service
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
