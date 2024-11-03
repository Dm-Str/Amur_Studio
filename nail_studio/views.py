from django.contrib.auth import login
from django.shortcuts import render
from nail_studio.models import Person


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        if not (1 < len(name) < 25):
            return render(request, 'register.html')
        if not ('@' in email):
            return render(request, 'register.html')
        if not (1 < len(password) < 50):
            return render(request, 'register.html')
        if len(phone) != 10 or not phone.isdigit():
            return render(request, 'register.html')

        user = Person.objects.create_user(username=name,
                                          email=email,
                                          password=password,
                                          number=phone)

        login(request, user)
        return render(request, 'index.html')

    if request.method == 'GET':
        return render(request, 'register.html')


def make_login(request):
    return render(request, 'login.html')


def courses(request):
    return render(request, 'courses.html')


def contacts(request):
    return render(request, 'contacts.html')