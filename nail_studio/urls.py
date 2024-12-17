from django.urls import  path
from . import views, lk_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.make_login, name='make_login'),
    path('courses/', views.courses, name='courses'),
    path('contacts/', views.contacts, name='contacts'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),

    #LK
    path('logout/', lk_views.make_logout, name='make_logout'),
    path('lk_user/', lk_views.lk_user, name='lk_user'),
    path('lk_user/edit_profile/', lk_views.edit_profile, name='edit_profile'),
    path('lk_user/bonuses/', lk_views.get_bonuses, name='get_bonuses'),
    path('lk_user/submit_reviews/', lk_views.submit_review, name='submit_review'),
    path('lk_user/notifications/', lk_views.get_notifications, name='get_notifications'),
    path('lk_user/', lk_views.change_password, name='change_password'),
    path('lk_user/get_training/', lk_views.get_training, name="get_training"),
    path('lk_user/<int:course_id>/', lk_views.submit_course, name='submit_course'),
    path('lk_user/enroll/<int:course_id>/', lk_views.enroll_course, name='enroll_course'),
    path('lk_user/', lk_views.get_help, name="get_help"),
    path('lk_user/course/<int:course_id>/continue', lk_views.continue_learning, name="continue_learning"),
    path('lk_user/lesson/<int:lesson_id>/', lk_views.lesson_detail, name='lesson_detail'),
    path('lk_user/lesson/<int:lesson_id>/next', lk_views.next_lesson, name='next_lesson'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
