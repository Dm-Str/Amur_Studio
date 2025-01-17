from decimal import Decimal

def calculation_bonuses_for_buy(price_course):
    """
        Вычисляет количество бонусов за покупку на основе цены курса.
        Параметры:
        price_course (float или str): Цена курса, на основе которой будут рассчитаны бонусы.
        Возвращает:
        int: Количество бонусов, равное 3% от цены курса.
    """
    sum_bonuses = Decimal(price_course) * Decimal('0.03')

    return int(sum_bonuses)