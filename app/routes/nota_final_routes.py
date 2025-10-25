from flask import Blueprint, jsonify
from app.services import nota_final_service

nota_final_bp = Blueprint("nota_final", __name__, url_prefix="/notas_finais")

@nota_final_bp.route("", methods=["GET"])
def listar_notas():
    """
    Retorna todas as notas finais.
    """
    resultado = nota_final_service.listar_notas_finais()
    return jsonify(resultado), 200
