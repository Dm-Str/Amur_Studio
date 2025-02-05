from django.contrib import admin

from nail_studio.forms import LessonForm
from nail_studio.models import *
from django.utils.html import format_html

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


class HomeworkImageInline(admin.TabularInline):
    model = HomeworkImage
    extra = 0
    fields = ('images', 'image_preview')
    readonly_fields = ('image_preview', )
    verbose_name = ''
    verbose_name_plural = ''
    ordering = ('images',)

    def image_preview(self, obj):
        if obj.images:
            return format_html(
                f'<img src="{obj.images.url}" style="max-width: 200px; max-height: 200px; margin-right: 1px;" />'
            )
        return "Нет изображения"

    image_preview.short_description = 'Предпросмотр'  # Название колонки


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


@admin.register(HomeworkImage)
class HomeworkImagePanel(admin.ModelAdmin):
    fields = ('homework', 'images', 'image_preview')  # Добавьте image_preview здесь
    readonly_fields = ('image_preview',)
    list_display = ('homework', 'images', 'image_preview')  # Добавляем image_preview здесь
    list_display_links = ('homework', 'images')
    list_filter = ('homework',)

    empty_value_display = '-пустой-'
    list_per_page = 64
    list_max_show_all = 4

    def image_preview(self, obj):
        if obj.images:
            return format_html(
                f'<img src="{obj.images.url}" style="max-width: 100px; max-height: 100px; margin-right: 5px;" />'
            )
        return "Нет изображения"

    image_preview.short_description = 'Предпросмотр'  # Название колонки


@admin.register(StudentHomework)
class StudentHomeworkPanel(admin.ModelAdmin):
    # TODO: Фильтр по "Курс" недоступен. Почему?
    fields = ('person', 'course', 'lesson', 'description', 'status',)
    list_display = ('person', 'course', 'lesson', 'description', 'status', 'created_at')
    list_display_links = ('person', 'course', 'lesson', 'description', 'status')
    list_filter = ('person', 'status', 'course')

    inlines = [HomeworkImageInline]
    empty_value_display = '-пустой-'
    list_per_page = 64
    list_max_show_all = 4


@admin.register(Certificates)
class CertificatesPanel(admin.ModelAdmin):
    fields = ('user', 'course', 'certificate_file', 'issued_at')
    list_display = ('user', 'course', 'certificate_file', 'issued_at')
    list_display_links = ('user', 'course', 'certificate_file', 'issued_at')
    list_filter = ('user', 'course')

    empty_value_display = '-пустой-'
    list_per_page = 64
    list_max_show_all = 4


