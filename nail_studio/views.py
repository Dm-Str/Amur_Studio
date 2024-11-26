from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from nail_studio.models import Person
from nail_studio.validators import *
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        try:
            validate_name(name)
            validate_email(email)
            validate_phone(phone)
            validate_password(password)

            user = Person.objects.create_user(username=name,
                                              email=email,
                                              number=phone,
                                              password=password
                                              )

            login(request, user)
            messages.success(request, 'Ваш аккаунт успешно создан!')
            return render(request, 'lk.html')

        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, 'register.html', {
                'errors': e.messages,
                'name': name,
                'email': email,
                'phone': phone
            })

    if request.method == 'GET':
        return render(request, 'register.html')


def make_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = Person.objects.filter(email=email).first()

        if user and user.check_password(password):
            login(request, user)
            return render(request, 'lk.html')

    return render(request, 'login.html')


def make_logout(request):
    logout(request)
    return render(request, 'index.html')


def courses(request):
    return render(request, 'courses.html')


def contacts(request):
    return render(request, 'contacts.html')


@login_required
def lk_user(request):
    return render(request, 'lk.html')