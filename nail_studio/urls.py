from django.urls import  path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.make_login, name='make_login'),
    path('courses/', views.courses, name='courses'),
    path('contacts/', views.contacts, name='contacts'),
]
