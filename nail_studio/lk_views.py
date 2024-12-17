from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from nail_studio.forms import PersonProfileForm
from nail_studio.models import Person, Courses, StudentCourseProgress, Lesson, Review
from django.contrib import messages
from nail_studio.utils import calculation_bonuses_for_buy


def make_logout(request):
    logout(request)
    return render(request, 'index.html')


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Courses, pk=course_id)
    return render(request, 'lk_submit_course.html', {'course': course})


@login_required
def submit_course(request, course_id):
    course = get_object_or_404(Courses, pk=course_id)
    user = request.user

    if request.method == 'POST':
        if course in user.courses.all():
            return render(request, 'lk_submit_course.html', {
                'course': course,
                'error': 'Вы уже записаны на этот курс!'
            })
        else:
            user.courses.add(course)

            price_course = course.price
            user.bonuses = calculation_bonuses_for_buy(price_course)
            user.save()

            return render(request, 'lk_get_courses.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = PersonProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен успешно!')
            return render(request, 'lk_edit_profile.html', {'form': form})
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')

    else:
        form = PersonProfileForm(instance=request.user)
    return render(request, 'lk_edit_profile.html', {'form': form})


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
        person.add_bonuses(100)
        messages.success(request, 'Ваш отзыв был успешно добавлен!\n'
                                           'И вам начисленно 100 бонусов!')
        return redirect('submit_review')

    context = {
            'courses': courses,
            'reviews': reviews
    }
    return render(request, 'lk_reviews.html', context)


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

    return render(request, 'lk_get_bonuses.html', context=context)


@login_required
def get_notifications(request):
    return render(request, 'lk.html')


@login_required
def change_password(request):
    return render(request, 'lk.html')


@login_required
def get_training(request):
    user_courses = request.user.courses.all()
    if not user_courses:
        return redirect('courses')
    return render(request, 'lk_get_courses.html')


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

    lessons = course.lessons.all()

    user = Person.objects.get(pk=request.user.id)

    context = {
        'course': course,
        'progress': progress,
        'current_lesson': current_lesson,
        'lessons': lessons,
        'user': user
    }

    return render(request, 'lk_continue_learning.html', context)


@login_required
def lesson_detail(request, lesson_id):
    current_lesson = get_object_or_404(Lesson, id=lesson_id)
    course = current_lesson.course

    context = {
        'current_lesson': current_lesson,
        'course': course,
        'lessons': course.lessons.all(),

    }
    return render(request, 'lk_continue_learning.html', context)


@login_required
def next_lesson(request, lesson_id):
    current_lesson = get_object_or_404(Lesson, id=lesson_id)
    course = current_lesson.course

    lessons = list(course.lessons.all())

    current_index = lessons.index(current_lesson)

    if current_index + 1 < len(lessons):
        next_lesson = lessons[current_index + 1]
    else:
        next_lesson = current_lesson

    progress = StudentCourseProgress.objects.filter(person=request.user, course=course).first()
    if progress:
        progress.current_lesson = next_lesson
        progress.save()

    context = {
        'current_lesson': next_lesson,
        'course': course,
        'lessons': course.lessons.all(),
        'user': request.user
    }

    return render(request, 'lk_continue_learning.html', context)


@login_required
def lk_user(request):
    return render(request, 'lk.html')

def get_help(request):
    return render(request, 'lk.html')