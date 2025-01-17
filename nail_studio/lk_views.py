from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from nail_studio.forms import PersonProfileForm
from nail_studio.models import Person, Courses, StudentCourseProgress, Lesson, Review, Topics
from django.contrib import messages
from nail_studio.utils import calculation_bonuses_for_buy
from decimal import Decimal


def make_logout(request):
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
    course = get_object_or_404(Courses, pk=course_id)

    progress = StudentCourseProgress.objects.filter(course=course, person=request.user).first()

    if not progress:
        first_lesson = course.lessons.first()
        progress = StudentCourseProgress.objects.create(person=request.user, course=course,
                                                        current_lesson=first_lesson, progress=1.0)

    current_lesson = progress.current_lesson
    if current_lesson is None:
        current_lesson = course.lessons.first()

    modules = course.modules.all()
    topics = Topics.objects.filter(module__in=modules)
    lessons = course.lessons.all()
    lessons_without_topics = lessons.filter(topic__isnull=True)

    user = Person.objects.get(pk=request.user.id)

    context = {
        'course': course,
        'progress': progress,
        'current_lesson': current_lesson,
        'modules': modules,
        'topics': topics,
        'lessons': lessons,
        'lessons_without_topics': lessons_without_topics,
        'user': user
    }

    return render(request, 'lk/lk_continue_learning.html', context)


@login_required
def lesson_detail(request, lesson_id):
    #TODO: Возможно необходимо получать не id урока, а его номер из модуля.
    current_lesson = get_object_or_404(Lesson, id=lesson_id)
    course = current_lesson.course
    lessons = course.lessons.all()
    lessons_without_topics = lessons.filter(topic__isnull=True)

    context = {
        'current_lesson': current_lesson,
        'course': course,
        'lessons': course.lessons.all(),
        'lessons_without_topics': lessons_without_topics,

    }
    return render(request, 'lk/lk_continue_learning.html', context)


@login_required
def next_lesson(request, lesson_id):
    # TODO: исправить код для корректного переключения на следующий урок.
    #  Исправить current_index. Заменить id на номер урока.
    current_lesson = get_object_or_404(Lesson, id=lesson_id)
    course = current_lesson.course
    lessons = course.lessons.all()
    lessons_without_topics = lessons.filter(topic__isnull=True)

    lessons = list(course.lessons.all())
    current_index = lessons.index(current_lesson)


    if current_index + 1 < len(lessons):
        #next_lesson = lessons[current_index + 1]
        next_lesson = current_index + 1
        return redirect('lesson_detail', lesson_id=next_lesson)
    else:
        next_lesson = current_lesson

    # progress = StudentCourseProgress.objects.filter(person=request.user, course=course).first()
    # if progress:
    #     progress.current_lesson = next_lesson
    #     progress.save()
    #
    # context = {
    #     'current_lesson': next_lesson,
    #     'course': course,
    #     'lessons': course.lessons.all(),
    #     'lessons_without_topics': lessons_without_topics,
    #     'user': request.user
    # }
    #
    # return render(request, 'lk/lk_continue_learning.html', context)


@login_required
def lk_user(request):
    return render(request, 'lk/lk.html')

def get_help(request):
    return render(request, 'lk/lk.html')