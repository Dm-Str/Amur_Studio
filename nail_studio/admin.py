from django.contrib import admin

from nail_studio.forms import LessonForm
from nail_studio.models import *


class ModulesInline(admin.TabularInline):
    model = Modules
    extra = 1
    fields = ('title', 'order')
    verbose_name = 'Модуль'
    verbose_name_plural = 'Модули'


class TopicsInline(admin.TabularInline):
    model = Topics
    extra = 1
    fields = ('module', 'title', 'order')
    verbose_name = 'Тема'
    verbose_name_plural = 'Темы'


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('module', 'topic', 'title', 'content', 'home_work', 'order', 'image', 'video')
    verbose_name = 'Урок'
    verbose_name_plural = 'Уроки'
    ordering = ('module',)
    form = LessonForm


@admin.register(Courses)
class CoursesPanel(admin.ModelAdmin):
    fields = ('title', 'description', 'price', 'date_start_after_payment',
              'date_end', 'course_type', 'image')
    list_display = ('title', 'get_description_short', 'price', 'course_type',
                    'date_start_after_payment', 'date_end')
    list_display_links = ('title', 'get_description_short', 'price', 'course_type',
                          'date_start_after_payment', 'date_end')
    list_filter = ('title', 'date_start_after_payment', 'course_type' , 'price')

    inlines = [ModulesInline, TopicsInline, LessonInline]
    empty_value_display = '-пустой-'
    list_per_page = 64
    list_max_show_all = 4

    search_fields = ('title', 'course_type')


@admin.register(Person)
class PersonPanel(admin.ModelAdmin):
    fields = ('username', 'first_name', 'last_name', 'number', 'courses')
    list_display = ('username', 'first_name', 'last_name', 'number', 'get_courses')
    list_display_links = ('username', 'first_name', 'last_name', 'number', 'get_courses')
    list_filter = ('courses',)

    empty_value_display = '-пустой-'
    list_per_page = 64
    list_max_show_all = 4

    search_fields = ('courses',)

    def get_courses(self, obj):
        return ", ".join(course.title for course in obj.courses.all())

    get_courses.short_description = 'Курсы'


@admin.register(Lesson)
class LessonPanel(admin.ModelAdmin):
    fields = ('course', 'title', 'content', 'home_work', 'image', 'video', 'order')
    list_display = ('course', 'title', 'get_description_lesson', 'order')
    list_display_links = ('course','title', 'get_description_lesson', 'order')
    list_filter = ('course', 'course__course_type', 'title', 'order')

    empty_value_display = '-пустой-'
    list_per_page = 64
    list_max_show_all = 4

    search_fields = ('course__course_type', 'title',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = ('course', 'person', 'rating', 'text')
    list_display = ('course', 'person', 'rating', 'created_at')
    list_display_links = ('course', 'person', 'rating', 'created_at')
    list_filter = ('course', 'course__course_type', 'person', 'rating', 'created_at')

    empty_value_display = '-пустой-'
    list_per_page = 64
    list_max_show_all = 4


@admin.register(StudentCourseProgress)
class StudentCourseProgressAdmin(admin.ModelAdmin):
    fields = ('person', 'course', 'progress')
    list_display = ('person', 'course', 'progress')
    list_display_links = ('person', 'course', 'progress')
    list_filter = ('person', 'course')

    empty_value_display = '-пустой-'
    list_per_page = 64
    list_max_show_all = 4

    search_fields = ('course__title',)


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


@admin.register(StudentHomework)
class StudentHomeworkPanel(admin.ModelAdmin):
    # TODO: Фильтр по "Курс" недоступен. Почему?
    fields = ('person', 'course', 'lesson', 'description', 'image', 'status',)
    list_display = ('person', 'course', 'lesson', 'description', 'image', 'status', 'created_at')
    list_display_links = ('person', 'course', 'lesson', 'description', 'image', 'status')
    list_filter = ('person', 'status', 'course')

    empty_value_display = '-пустой-'
    list_per_page = 64
    list_max_show_all = 4

