from decimal import Decimal, ROUND_HALF_UP

def calcular_media(valores):
    if not valores:
        return Decimal("0.00")
    total = sum(Decimal(v) for v in valores)
    media = total / Decimal(len(valores))
    return media.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
