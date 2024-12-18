from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from nail_studio.validators import *


class Courses(models.Model):
    COURSE_TYPES = [
        ('basic', 'Базовый'),
        ('advanced', 'Повышение квалификации'),
    ]

    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Стоимость')
    number_of_hours = models.IntegerField(default=0, verbose_name='Количество часов')
    date_start_after_payment = models.DateField(verbose_name='Начало курса') # имя поля?
    date_end = models.DateField(blank=True, null=True, verbose_name='Конец курса')
    course_type = models.CharField(max_length=30, choices=COURSE_TYPES, default='basic', verbose_name='Тип курса')
    image = models.ImageField(upload_to='images/', verbose_name='Изображение курса')
    image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(300, 200)],
                                     format='JPEG', options={'quality': 85})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def get_description_short(self):
        return self.description[:100]

    get_description_short.short_description = 'Описание'


class Lesson(models.Model):
    course = models.ForeignKey(Courses, related_name='lessons', on_delete=models.CASCADE, verbose_name='Курс')
    title = models.CharField(max_length=200, verbose_name='Название урока')
    content = models.TextField(verbose_name='Содержание урока')
    home_work = models.TextField(blank=True, null=True, verbose_name='Домашнее задание')
    order = models.PositiveIntegerField(verbose_name='Порядок урока')
    image = models.ImageField(upload_to='lesson_images/', blank=True, null=True, verbose_name='Изображение')
    video = models.FileField(upload_to='lesson_videos/', blank=True, null=True, verbose_name='Видео')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['order']

    def get_description_lesson(self):
        return self.content[:100]

    get_description_lesson.short_description = 'Содержание урока'


class Person(AbstractUser):
    username = models.CharField(max_length=45, unique=True, validators=[validate_name], verbose_name='Логин')
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='День рождения')
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name='Страна')
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='Город')
    messenger= models.CharField(max_length=50, blank=True, null=True, verbose_name='Мессенджер')
    number = models.CharField(max_length=25, unique=True, validators=[validate_phone], verbose_name='Телефон')
    photo = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Фото профиля')
    experience = models.CharField(max_length=50, default='Нет', verbose_name='Опыт работы')
    bonuses = models.IntegerField(default=50, verbose_name='Бонусы')
    certificate_image = models.ImageField(upload_to='certificates/', verbose_name='Сертификаты')
    courses = models.ManyToManyField(Courses, related_name='persons', blank=True, verbose_name='Курсы')

    def add_bonuses(self, amount):
        self.bonuses += amount
        self.save()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('number',)


class Review(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='review')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.person} - {self.rating}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['created_at']


class StudentCourseProgress(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='course_progress',
                               verbose_name='Студент')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='student_progress',
                               verbose_name='Курс')
    current_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, verbose_name='Текущий урок')
    progress = models.FloatField(default=0.0, verbose_name='Прогресс (%)')

    def __str__(self):
        return f"{self.person.username} - {self.course.title} - {self.current_lesson}"

    class Meta:
        verbose_name = 'Прогресс пользователя по курсу'


class Discounts(models.Model):
    courses = models.ManyToManyField(Courses, related_name='discounts')  # ???
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    date_start = models.DateField(verbose_name='Начало скидки')
    date_end = models.DateField(blank=True, null=True, verbose_name='Конец скидки')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Процент скидки',
                                              default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Certificates(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='certificates')
    certificate_file = models.FileField(upload_to='certificates/', verbose_name='Файл сертификата')
    issued_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата выдачи')

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'


class Notifications(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='notifications',
                             verbose_name='Пользователь')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='notifications',
                               verbose_name='Курс')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')

    class Meta:
        verbose_name = 'Оповещение'
        verbose_name_plural = 'Оповещения'


class BonusTransaction(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='bonus_transactions',
                             verbose_name='Пользователь')
    amount = models.IntegerField(verbose_name='Сумма бонусов')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    transaction_type = models.CharField(max_length=20, choices=[('earn', 'Начисление'), ('spend', 'Списание')],
                                        verbose_name='Тип транзакции')

    class Meta:
        verbose_name = 'Транзакция бонусов'
        verbose_name_plural = 'Транзакции бонусов'


class Questions(models.Model):
    title = models.CharField(max_length=300, verbose_name='Название')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answers(models.Model):
    title = models.CharField(max_length=300, verbose_name='Название')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    question = models.ForeignKey(Questions, related_name='answers', on_delete=models.CASCADE, verbose_name='Вопрос')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class StudentsWorkBasicCourse(models.Model):
    student = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='basic_course_works',
                                verbose_name='Студент')
    image = models.ImageField(upload_to='images/', verbose_name='Фото работы')

    class Meta:
        verbose_name = 'Работа студента базового курса'
        verbose_name_plural = 'Работы студентов базового курс'


class StudentsWorkRetrainingCourse(models.Model):
    student = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='retraining_course_works',
                                verbose_name='Студент')
    image = models.ImageField(upload_to='images/', verbose_name='Фото работы')

    class Meta:
        verbose_name = 'Работа студента повышение квалификации'
        verbose_name_plural = 'Работы студентов повышение квалификации'
