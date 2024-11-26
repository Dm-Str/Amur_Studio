from django.urls import  path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.make_login, name='make_login'),
    path('courses/', views.courses, name='courses'),
    path('contacts/', views.contacts, name='contacts'),
    path('lk_user/', views.lk_user, name='lk_user'),
    path('logout/', views.make_logout, name='make_logout'),
]
