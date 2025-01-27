from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import first

from nail_studio.forms import PersonProfileForm
from nail_studio.models import Person, Courses, StudentCourseProgress, Lesson, Review, Topics
from django.contrib import messages
from nail_studio.utils import calculation_bonuses_for_buy, is_completed_course
from decimal import Decimal
from nail_studio.views import courses


def make_logout(request):
    # TODO: заменить render на redirect
    logout(request)
    return render(request, 'index.html')


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Courses, pk=course_id)
    person = request.user

    bonuses_person = person.bonuses
    course_price = course.price

    bonuses_person = Decimal(bonuses_person)
    course_price = Decimal(course_price)

    if bonuses_person:
        max_bonus_spend = course_price * Decimal("0.5")
        used_bonuses = min(bonuses_person, max_bonus_spend)
        final_price = course_price - used_bonuses

        context = {
            'course': course,
            'final_price': final_price,
            'bonuses_person': bonuses_person,
        }

        return render(request, 'lk/lk_submit_course.html', context=context)

    return render(request, 'lk/lk_submit_course.html',
                  {'course': course, 'final_price': course_price})


@login_required
def submit_course(request, course_id):
    course = get_object_or_404(Courses, pk=course_id)
    user = request.user

    if request.method == 'POST':
        if course in user.courses.all():
            return render(request, 'lk/lk_submit_course.html', {
                'course': course,
                'error': 'Вы уже записаны на этот курс!'
            })
        else:
            user.courses.add(course)

            price_course = course.price
            user.bonuses = calculation_bonuses_for_buy(price_course)
            user.save()

            return render(request, 'lk/lk_get_courses.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = PersonProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен успешно!')
            return render(request, 'lk/lk_edit_profile.html', {'form': form})
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')

    else:
        form = PersonProfileForm(instance=request.user)
    return render(request, 'lk/lk_edit_profile.html', {'form': form})


@login_required
def submit_review(request):
    person = get_object_or_404(Person, pk=request.user.id)
    courses = person.courses.all()
    reviews = Review.objects.filter(person=person)

    if request.method == 'POST':
        course_id = request.POST.get('course')
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')

        course = get_object_or_404(Courses, pk=course_id)

        review = Review(person=person,
                        course=course,
                        rating=rating,
                        text=review_text)

        review.save()

        #Бонусы за отзыв
        person.calculate_review_bonuses(100)
        messages.success(request, 'Ваш отзыв был успешно добавлен!\n'
                                           'И вам начисленно 100 бонусов!')
        return redirect('submit_review')

    context = {
            'courses': courses,
            'reviews': reviews
    }
    return render(request, 'lk/lk_reviews.html', context)


@login_required
def delete_review(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Courses, pk=course_id)
        review = get_object_or_404(Review, pk=request.user.id)
        review.delete()
        return redirect('submit_review')


@login_required
def get_bonuses(request):
    person = get_object_or_404(Person, pk=request.user.id)

    bonuses = person.bonuses

    context = {
        'person': person,
        'bonuses': bonuses
    }

    return render(request, 'lk/lk_get_bonuses.html', context=context)


@login_required
def get_notifications(request):
    return render(request, 'lk/lk.html')


@login_required
def change_password(request):
    return render(request, 'lk/lk.html')


@login_required
def get_training(request):
    user_courses = request.user.courses.all()
    if not user_courses:
        return redirect('courses')
    return render(request, 'lk/lk_get_courses.html')


@login_required
def continue_learning(request, course_id):
    # TODO: Сейчас view возвращает последний пройденный урок,
    #  возможно, нужно исправить так, чтобы получать следующий урок за последним пройденным.
    course = get_object_or_404(Courses, pk=course_id)
    progress = StudentCourseProgress.objects.filter(course=course,
                                                    person=request.user).all()

    if not progress:
        first_module = course.modules.first()

        if first_module:
            first_topic = first_module.topics.first()

            if first_topic:
                first_lesson = first_topic.lessons.first()
                return redirect('lesson_detail', lesson_id=first_lesson.pk)

            first_lesson = first_module.lessons.first()
            return redirect('lesson_detail', lesson_id=first_lesson.pk)

    last_completed_lesson = progress.order_by('-id').first().current_lesson_id
    return redirect('lesson_detail', lesson_id=last_completed_lesson)


@login_required
def lesson_detail(request, lesson_id):
    #TODO: Возможно необходимо получать не id урока, а его номер из модуля?
    current_lesson = get_object_or_404(Lesson, id=lesson_id)
    course = current_lesson.course
    lessons = course.lessons.all()
    lessons_without_topics = lessons.filter(topic__isnull=True)
    student_progress = StudentCourseProgress.objects.filter(course=course, person=request.user).all()
    completed_lessons_ids = student_progress.values_list('current_lesson_id', flat=True)

    context = {
        'current_lesson': current_lesson,
        'course': course,
        'lessons': course.lessons.all(),
        'lessons_without_topics': lessons_without_topics,
        'completed_lessons_ids': completed_lessons_ids,

    }
    return render(request, 'lk/lk_lesson_detail.html', context)


@login_required
def next_lesson(request, lesson_id):
    # TODO: Добавить логику: если пользователь пропустил урок,
    #  и начал проходить следующие кроки, то наяходясь на последнем уроке,
    #  после нажатия кнокпи следующего урока, он должен получать первый из непройденных уроков.
    current_lesson = get_object_or_404(Lesson, id=lesson_id)
    course = current_lesson.course
    student_progress = StudentCourseProgress.objects.filter(course=course,
                                                    person=request.user).all()
    completed_lessons_ids = student_progress.values_list('current_lesson_id', flat=True)

    if current_lesson.pk not in completed_lessons_ids:
        StudentCourseProgress.objects.create(
            person=request.user,
            course=course,
            current_lesson=current_lesson,
            progress=1.0
        )

    if is_completed_course(
            course=course,
            student_progress=student_progress,
            current_lesson=current_lesson
    ):
        return redirect('complete_current_course', course_id=course.id)

    # Здесь нужно получить все не пройденные уроки,
    # если они есть, вернуть к первому не пройденному.

    current_module = course.modules.get(id=current_lesson.module_id)
    last_lesson_module = current_module.lessons.order_by('-order').first()

    # Код падает здесь, т.к. пытается получить следующий модуль.
    # Либо добавить здесь проверку на последний модуль.
    if current_lesson == last_lesson_module:
        next_module_id = current_module.pk + 1
        first_lesson_next_module = course.modules.get(id=next_module_id).lessons.first()
        return redirect('lesson_detail', lesson_id=first_lesson_next_module.pk)

    next_lesson_order = current_lesson.order + 1
    next_lesson_module = current_module.lessons.get(order=next_lesson_order)
    return redirect('lesson_detail', lesson_id=next_lesson_module.pk)


@login_required
def complete_current_course(request, course_id):
    # TODO: добавить логику проверки прохождения всех уроков.
    #  Определить ответственное view
    course = get_object_or_404(Courses, pk=course_id)
    lessons = course.lessons.all()
    lessons_without_topics = lessons.filter(topic__isnull=True)

    context = {

        'course': course,
        'lessons': course.lessons.all(),
        'lessons_without_topics': lessons_without_topics,

    }
    return render(request, 'lk/lk_complete_current_course.html', context)


@login_required
def lk_user(request):
    return render(request, 'lk/lk.html')


def get_help(request):
    return render(request, 'lk/lk.html')
