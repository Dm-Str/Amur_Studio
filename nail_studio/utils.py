from decimal import Decimal

def calculation_bonuses_for_buy(price_course):
    sum_bonuses = Decimal(price_course) * Decimal('0.03')

    return int(sum_bonuses)