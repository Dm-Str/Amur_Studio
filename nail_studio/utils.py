from decimal import Decimal
import os
from django.conf import settings
from nail_studio.models import StudentCourseProgress, Lesson
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from datetime import datetime
from pdfrw import PdfReader, PdfWriter, PageMerge

pdfmetrics.registerFont(TTFont('Lato', 'Lato-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Lato-Bold', 'Lato-Bold.ttf'))


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


def check_completed_homework(request, course):
    sent_homeworks_lessons = Lesson.objects.filter(homework__isnull=False)
    all_homeworks = course.lessons.exclude(home_work__icontains='Нет')

    if set(sent_homeworks_lessons) == set(all_homeworks):
        student_homework = request.user.homework.all()
        all_checked = all(homework.status == 1 for homework in student_homework)

        if all_checked:
            return all_checked

        homework_on_check = student_homework.exclude(status=1).first()
        return homework_on_check.lesson_id

    no_solution_homework = all_homeworks.exclude(
        id__in=sent_homeworks_lessons.values_list('id', flat=True)).first()
    return no_solution_homework.pk


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


def create_text_pdf(student_name, student_surname, course_title):
    page_width = 3400
    page_height = 1900

    # Временный PDF с текстом
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))

    # Шрифт и размер
    can.setFillColorRGB(0.25, 0.25, 0.25)
    can.setFont("Lato-Bold", 170)

    # Вычисление ширину имени, пробела и фамилии
    name_width = can.stringWidth(student_name, "Lato-Bold", 170)
    surname_width = can.stringWidth(student_surname, "Lato-Bold", 170)
    space_width = can.stringWidth(" ", "Lato-Bold", 170)

    # Общая ширина текста имени и фамилии
    total_width = name_width + space_width + surname_width

    # Центрирование текста по координате x
    center_x_position = 1465
    start_x_position = center_x_position - (total_width / 2)

    can.drawString(start_x_position, 930, student_name)
    can.drawString(start_x_position + name_width + space_width, 930, student_surname)

    # Шрифт для названия курса
    can.setFont("Lato-Bold", 85)

    # Вычисление ширины названия курса, центрирование названия
    course_width = can.stringWidth(course_title, "Lato-Bold", 85)
    course_x_position = center_x_position - (course_width / 2)
    can.drawString(course_x_position, 700, f"«{course_title}»")

    # Шрифт для даты
    can.setFont("Lato", 50)
    can.drawString(515, 270, f"{datetime.now().strftime('%d.%m.%Y')}")

    can.save()
    packet.seek(0)
    return PdfReader(packet)


def generate_certificate(student_id, student_name, student_surname, course):
    template_path = os.path.join(
        settings.MEDIA_ROOT,'template_certificate/certificate_template.pdf')

    output_path = os.path.join(
        settings.MEDIA_ROOT,f'students_certificates/student_{student_id}_certificate_{course.id}.pdf')

    course_title = ''.join([i for i in course.title if i not in '<h2>«»</h2>'])

    text_pdf = create_text_pdf(student_name, student_surname, course_title)
    existing_pdf = PdfReader(template_path)
    output = PdfWriter()

    for page in existing_pdf.pages:

        if existing_pdf.pages.index(page) < len(text_pdf.pages):
            overlay_page = text_pdf.pages[0]
            PageMerge(page).add(overlay_page).render()

        output.addPage(page)

    output.write(output_path)

    student_certificate_url = os.path.join(
        settings.MEDIA_URL,f'students_certificates/student_{student_id}_certificate_{course.id}.pdf')

    return student_certificate_url
