import pytest
from unittest.mock import patch, MagicMock
from app.services import avaliacao_service
from sqlalchemy.exc import IntegrityError

def test_salvar_avaliacao_sucesso(monkeypatch):
    data = {
        "matricula": "161000",
        "data_avaliacao": "2025-10-30",
        "comportamental": [{"numero_questao": i+1, "descricao": f"Q{i+1}", "nota": 3} for i in range(4)],
        "desafios": [{"numero_desafio": i+1, "descricao": f"D{i+1}", "nota": 4} for i in range(2)]
    }

    fake_nota_final = MagicMock()
    fake_nota_final.nota_final = 4.0

    monkeypatch.setattr(avaliacao_service.colaborador_repository, "get_id_por_matricula", lambda x: 1)
    monkeypatch.setattr(avaliacao_service.avaliacao_comportamental_repository, "salvar_avaliacao_comportamental", lambda a, b: None)
    monkeypatch.setattr(avaliacao_service.avaliacao_desafio_repository, "salvar_avaliacao_desafio", lambda a, b: None)
    monkeypatch.setattr(avaliacao_service.nota_final_repository, "salvar", lambda cid, a, d, dt: fake_nota_final)
    monkeypatch.setattr(avaliacao_service.db.session, "commit", lambda: None)

    resultado = avaliacao_service.salvar_avaliacao(data)
    assert resultado["media_comportamental"] == 3
    assert resultado["media_desafio"] == 4
    assert resultado["nota_final"] == 4.0

def test_salvar_avaliacao_sem_matricula():
    data = {"data_avaliacao": "2025-10-30", "comportamental": [], "desafios": []}
    with pytest.raises(ValueError, match="O campo 'matricula' é obrigatório."):
        avaliacao_service.salvar_avaliacao(data)
        
def test_deletar_avaliacao_por_nota_final_sucesso(monkeypatch):
    nota_final_mock = MagicMock()
    nota_final_mock.avaliacao_comportamental_id = 1
    nota_final_mock.avaliacao_desafio_id = 2

    monkeypatch.setattr(avaliacao_service.nota_final_repository, "get_por_id", lambda x: nota_final_mock)
    monkeypatch.setattr(avaliacao_service.nota_final_repository, "deletar", lambda x: None)
    monkeypatch.setattr(avaliacao_service.avaliacao_comportamental_item_repository, "deletar", lambda x: None)
    monkeypatch.setattr(avaliacao_service.avaliacao_comportamental_repository, "deletar", lambda x: None)
    monkeypatch.setattr(avaliacao_service.avaliacao_desafio_item_repository, "deletar", lambda x: None)
    monkeypatch.setattr(avaliacao_service.avaliacao_desafio_repository, "deletar", lambda x: None)
    monkeypatch.setattr(avaliacao_service.db.session, "commit", lambda: None)

    resultado = avaliacao_service.deletar_avaliacao_por_nota_final(1)
    assert resultado == "Avaliação removida com sucesso"

def test_deletar_avaliacao_por_nota_final_nao_encontrada(monkeypatch, app):
    monkeypatch.setattr(avaliacao_service.nota_final_repository, "get_por_id", lambda x: None)

    with app.app_context(): 
        with pytest.raises(ValueError, match="Nota final não encontrada"):
            avaliacao_service.deletar_avaliacao_por_nota_final(999)

