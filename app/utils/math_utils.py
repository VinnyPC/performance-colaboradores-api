from decimal import Decimal, ROUND_HALF_UP

def calcular_media(notas):
    if not notas:
        return 0
    return float(Decimal(sum(notas)/len(notas)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
