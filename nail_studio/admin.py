from django.contrib import admin
from nail_studio.models import *
from nail_studio.views import courses


@admin.register(Courses)
class CoursesPanel(admin.ModelAdmin):
    fields = ('title', 'description', 'price', 'date_start_after_payment', 'date_end', 'course_type')
    list_display = ('title', 'description', 'price', 'date_start_after_payment', 'date_end', 'course_type')
    list_display_links = ('title', 'description', 'price', 'date_start_after_payment', 'date_end', 'course_type')
    list_filter = ('title', 'date_start_after_payment', 'course_type' , 'price')

    empty_value_display = '-пустой-'
    list_per_page = 64
    list_max_show_all = 4

    search_fields = ('title', 'course_type')


@admin.register(Person)
class PersonPanel(admin.ModelAdmin):
    fields = ('username', 'first_name', 'last_name', 'number', 'courses')
    list_display = ('username', 'first_name', 'last_name', 'number', 'get_courses', 'certificates')
    list_display_links = ('username', 'first_name', 'last_name', 'number', 'get_courses', 'certificates')
    list_filter = ('certificates',)

    empty_value_display = '-пустой-'
    list_per_page = 64
    list_max_show_all = 4

    search_fields = ('certificates', 'courses',)

    def get_courses(self, obj):
        return ", ".join(course.title for course in obj.courses.all())

    get_courses.short_description = 'Курсы'



@admin.register(Discounts)
class DiscountsPanel(admin.ModelAdmin):
    fields = ('title', 'date_start', 'date_end')
    list_display = ('title', 'date_start', 'date_end')
    list_display_links = ('title', 'date_start', 'date_end')
    list_filter = ('title', 'date_start', 'date_end')

    empty_value_display = '-пустой-'
    list_per_page = 64
    list_max_show_all = 4

    search_fields = ('title', 'date_start', 'date_end')


@admin.register(Questions)
class QuestionsPanel(admin.ModelAdmin):
    fields = ('title', 'created_at',)
    list_display = ('title', 'created_at')
    list_display_links = ('title', 'created_at')
    list_filter = ('title', 'created_at')

    empty_value_display = '-пустой-'
    list_per_page = 64
    list_max_show_all = 4

    search_fields = ('title', 'created_at')


@admin.register(Answers)
class AnswersPanel(admin.ModelAdmin):
    fields = ('title', 'created_at')
    list_display = ('title', 'created_at')
    list_display_links = ('title', 'created_at')
    list_filter = ('title', 'created_at')

    empty_value_display = '-пустой-'
    list_per_page = 64
    list_max_show_all = 4

    search_fields = ('title', 'created_at')


@admin.register(StudentsWorkBasicCourse)
class StudentsBasicPanel(admin.ModelAdmin):
    fields = ('image',)
    list_display = ('image',)
    list_display_links = ('image',)
    list_filter = ('image',)

    empty_value_display = '-пустой-'
    list_per_page = 64
    list_max_show_all = 4


@admin.register(StudentsWorkRetrainingCourse)
class StudentsRetrainingPanel(admin.ModelAdmin):
    fields = ('image',)
    list_display = ('image',)
    list_display_links = ('image',)
    list_filter = ('image',)

    empty_value_display = '-пустой-'
    list_per_page = 64
    list_max_show_all = 4
