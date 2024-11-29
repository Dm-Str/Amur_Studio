from django.urls import  path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.make_login, name='make_login'),
    path('courses/', views.courses, name='courses'),
    path('contacts/', views.contacts, name='contacts'),
    path('lk_user/', views.lk_user, name='lk_user'),
    path('logout/', views.make_logout, name='make_logout'),

    #LK
    path('lk_user/edit_profile/', views.edit_profile, name='edit_profile'),
    path('lk_user/', views.get_bonuses, name='get_bonuses'),
    path('lk_user/', views.my_reviews, name='my_reviews'),
    path('lk_user/', views.get_notifications, name='get_notifications'),
    path('lk_user/', views.change_password, name='change_password'),
    path('lk_user/get_training/', views.get_training, name="get_training"),
    path('lk_user/', views.get_help, name="get_help"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
