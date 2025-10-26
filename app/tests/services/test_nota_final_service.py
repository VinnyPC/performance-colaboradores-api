import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from app.services import nota_final_service


def test_listar_notas_finais(monkeypatch):

    class FakeNota:
        def __init__(self, id, colaborador_id, aval_comp_id, aval_desafio_id, media_c, media_d, nota_final, data_calculo):
            self.id = id
            self.colaborador_id = colaborador_id
            self.avaliacao_comportamental_id = aval_comp_id
            self.avaliacao_desafio_id = aval_desafio_id
            self.media_comportamental = media_c
            self.media_desafio = media_d
            self.nota_final = nota_final
            self.data_calculo = data_calculo

    fake_notas = [
        FakeNota(1, 101, 11, 21, 3.5, 4.0, 3.75, datetime(2025, 10, 25)),
        FakeNota(2, 102, 12, 22, 4.0, 4.5, 4.25, datetime(2025, 10, 26))
    ]

    monkeypatch.setattr(
        nota_final_service.nota_final_repository,
        "listar_todos",
        lambda: fake_notas
    )

    resultado = nota_final_service.listar_notas_finais()
    assert len(resultado) == 2
    assert resultado[0]["media_comportamental"] == 3.5
    assert resultado[1]["nota_final"] == 4.25
    assert resultado[0]["data_calculo"] == "2025-10-25T00:00:00"


def test_listar_notas_por_matricula(monkeypatch):
    class FakeNota:
        def __init__(self, id, colaborador_id, aval_comp_id, aval_desafio_id, media_c, media_d, nota_final, data_calculo):
            self.id = id
            self.colaborador_id = colaborador_id
            self.avaliacao_comportamental_id = aval_comp_id
            self.avaliacao_desafio_id = aval_desafio_id
            self.media_comportamental = media_c
            self.media_desafio = media_d
            self.nota_final = nota_final
            self.data_calculo = data_calculo

    fake_notas = [
        FakeNota(1, 101, 11, 21, 3.5, 4.0, 3.75, datetime(2025, 10, 25))
    ]


    monkeypatch.setattr(
        nota_final_service.colaborador_repository,
        "get_id_por_matricula",
        lambda matricula: 101
    )


    monkeypatch.setattr(
        nota_final_service.nota_final_repository,
        "listar_por_colaborador",
        lambda colaborador_id: fake_notas
    )

    resultado = nota_final_service.listar_notas_por_matricula("161000")
    assert len(resultado) == 1
    assert resultado[0]["colaborador_id"] == 101
    assert resultado[0]["nota_final"] == 3.75
