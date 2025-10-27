from decimal import Decimal
from app.utils.math_utils import calcular_media


def test_calcular_media_lista_valida():
    valores = [3, 4, 5]
    resultado = calcular_media(valores)
    assert resultado == Decimal("4.00")


def test_calcular_media_lista_vazia():
    valores = []
    resultado = calcular_media(valores)
    assert resultado == Decimal("0.00")


def test_calcular_media_com_decimais():
    valores = [2.5, 3.5, 4.5]
    resultado = calcular_media(valores)
    assert resultado == Decimal("3.50")


def test_calcular_media_com_numeros_negativos():
    valores = [-2, 4, 6]
    resultado = calcular_media(valores)
    assert resultado == Decimal("2.67")  # (8 / 3 = 2.666... → arredonda para 2.67)


def test_calcular_media_arredondamento_half_up():
    valores = [1, 2]
    resultado = calcular_media(valores)
    assert resultado == Decimal("1.50")

    valores = [1, 2, 2]
    resultado = calcular_media(valores)
    assert resultado == Decimal("1.67")  # 1.6666... arredonda para 1.67
