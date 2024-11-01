from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def courses(request):
    return render(request, 'courses.html')

def contacts(request):
    return render(request, 'contacts.html')