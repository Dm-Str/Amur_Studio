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
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('lk_user/<int:course_id>/', views.submit_course, name='submit_course'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),


    #LK
    path('lk_user/edit_profile/', views.edit_profile, name='edit_profile'),
    path('lk_user/', views.get_bonuses, name='get_bonuses'),
    path('lk_user/', views.my_reviews, name='my_reviews'),
    path('lk_user/', views.get_notifications, name='get_notifications'),
    path('lk_user/', views.change_password, name='change_password'),
    path('lk_user/get_training/', views.get_training, name="get_training"),
    path('lk_user/', views.get_help, name="get_help"),
    path('lk_user/learning/course/<int:course_id>', views.continue_learning, name="continue_learning"),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
