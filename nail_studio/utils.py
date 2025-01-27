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


def is_completed_course(course, student_progress, current_lesson):
    last_lesson_course = (course.modules.order_by('-order').first().
                          lessons.order_by('-order').first())
    all_lessons_course = course.lessons.all().count()
    all_completed_lessons_course = student_progress.filter(progress=1.0).count()

    if (current_lesson == last_lesson_course) and (all_lessons_course == all_completed_lessons_course):
        return True
