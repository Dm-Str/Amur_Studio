from decimal import Decimal
from nail_studio.models import StudentCourseProgress


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


def get_completed_lessons_ids(student_progress):
    completed_lessons_ids = student_progress.values_list('current_lesson_id', flat=True)
    return completed_lessons_ids


def get_last_lesson_course(course):
    last_lesson_course = (course.modules.order_by('-order').first().
                          lessons.order_by('-order').first())
    return last_lesson_course


def get_last_module_course(course):
    last_module_course = course.modules.order_by('-order').first()
    return last_module_course


def get_lessons_course(course):
    lessons_course = course.lessons.all()
    return lessons_course


def get_not_completed_lessons(course, student_progress):
    not_completed_lessons = get_lessons_course(course).exclude(
        pk__in=get_completed_lessons_ids(student_progress))
    return not_completed_lessons


def check_completed_course(course, student_progress, current_lesson):
    lessons_course = get_lessons_course(course).count()
    completed_lessons_course = student_progress.filter(progress=1.0).count()

    if (current_lesson == get_last_lesson_course(course) and
            lessons_course == completed_lessons_course):
        return True


def update_student_progress(current_lesson, course, student_progress, user):
    if current_lesson.pk not in get_completed_lessons_ids(student_progress=student_progress):
        StudentCourseProgress.objects.create(
            person=user,
            course=course,
            current_lesson=current_lesson,
            progress=1.0
        )


# def handle_last_lesson(course, student_progress):
#     if get_completed_lessons_ids(student_progress).count() != get_lessons_course(course).count():
#         not_completed_lessons = get_not_completed_lessons(course, student_progress)
#         return not_completed_lessons[0]
#     return None
#
#
# def get_next_lesson(current_lesson, current_module, course):
#     last_lesson_module = current_module.lessons.order_by('-order').first()
#     if current_lesson == last_lesson_module:
#         if get_last_module_course(course) == current_module:
#             return True
