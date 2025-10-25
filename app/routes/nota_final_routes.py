from flask import Blueprint, jsonify, request
from app.services import nota_final_service

nota_final_bp = Blueprint("nota_final", __name__, url_prefix="/notas_finais")

@nota_final_bp.route("", methods=["GET"])
def listar_notas():
    """
    Retorna todas as notas finais.
    """
    resultado = nota_final_service.listar_notas_finais()
    return jsonify(resultado), 200

@nota_final_bp.route("/colaborador", methods=["GET"])
def listar_notas_colaborador():
    """
    Retorna as notas finais de um colaborador filtrando pela matrícula.
    """
    matricula = request.args.get("matricula")
    if not matricula:
        return jsonify({"error": "O parâmetro 'matricula' é obrigatório"}), 400
    try:
        resultado = nota_final_service.listar_notas_por_matricula(matricula)
        return jsonify(resultado), 200
    except ValueError as err:
        return jsonify({"error": str(err)}), 404
