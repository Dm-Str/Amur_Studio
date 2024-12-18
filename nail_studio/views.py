from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from nail_studio.models import Person, Courses
from nail_studio.validators import *
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password_repiet = request.POST.get('password_repiet')
        user_name = Person.generate_username(email)

        if password != password_repiet:
            return render(request, 'register.html', {
                'errors': ['Пароли не совпадают!'],
                'email': email,
                'phone': phone
            })

        try:
            validate_email(email)
            validate_phone(phone)
            validate_password(password)
            validate_name(user_name)

            user = Person.objects.create_user(username=user_name,
                                              email=email,
                                              number=phone,
                                              password=password)

            login(request, user)
            messages.success(request, 'Ваш аккаунт успешно создан!')
            return redirect('lk_user')

        except ValidationError as e:
            return render(request, 'register.html', {
                'errors': e.messages,
                'email': email,
                'phone': phone
            })

    if request.method == 'GET':
        return render(request, 'register.html')


def make_login(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        password = request.POST.get('password')
        user = Person.objects.filter(number=number).first()
        print(f"Trying to log in with number: {number}")

        if user and user.check_password(password):
            login(request, user)
            return redirect('lk_user')
        else:
            messages.error(request, 'Неверный номер телефона или пароль!')

    return render(request, 'login.html')


def courses(request):
    all_courses = Courses.objects.all()
    return render(request, 'courses.html', {
        'all_courses': all_courses,
    })


def course_detail(request, course_id):
    course = get_object_or_404(Courses, pk=course_id)
    return render(request, 'course_detail.html', {'course': course})


def contacts(request):
    return render(request, 'contacts.html')
