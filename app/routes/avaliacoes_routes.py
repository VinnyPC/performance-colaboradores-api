from flask import Blueprint, request, jsonify
from app.services.avaliacao_service import salvar_avaliacao

avaliacoes_bp = Blueprint("avaliacoes", __name__, url_prefix="/avaliacoes")

@avaliacoes_bp.route("", methods=["POST"])
def criar_avaliacao():
    """
    Recebe um body JSON com o formato esperado e salva tudo no banco
    """
    data = request.get_json()
    
    try:
        resultado = salvar_avaliacao(data)
        return jsonify({
            "message": "Avaliação salva com sucesso!",
            "nota_final": resultado
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
