from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from nail_studio.forms import PersonProfileForm
from nail_studio.models import Person, Courses, StudentCourseProgress, Lesson
from django.contrib import messages


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

        user.courses.add(course)
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


def get_bonuses(request):
    return render(request, 'lk_get_bonuses.html')


def my_reviews(request):
    return render(request, 'lk.html')


def get_notifications(request):
    return render(request, 'lk.html')


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