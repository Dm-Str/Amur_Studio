from django.contrib.auth.models import AbstractUser
from django.db import models
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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Person(AbstractUser):
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    username = models.CharField(max_length=45, validators=[validate_name], verbose_name='Логие')
    number = models.CharField(max_length=25, unique=True, validators=[validate_phone], verbose_name='Телефон')
    experience = models.CharField(max_length=50, default='Нет') # оставить?
    bonuses = models.IntegerField(default=0, verbose_name='Бонусы')
    certificates = models.ImageField(upload_to='certificates/', verbose_name='Сертификаты')
    courses = models.ManyToManyField(Courses, related_name='persons', verbose_name='Курсы')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('number',)


class Discounts(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    date_start = models.DateField(verbose_name='Начало скидки')
    date_end = models.DateField(blank=True, null=True, verbose_name='Конец скидки')
    courses = models.ManyToManyField(Courses, related_name='discounts') # ???

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Certificates(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='certificates')
    certificate_file = models.FileField(upload_to='certificates/', verbose_name='Файл сертификата')
    # issued_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата выдачи')

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


class StudentsWorkAdvancedCourse(models.Model):
    student = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='advanced_course_works',
                                verbose_name='Студент')
    image = models.ImageField(upload_to='images/', verbose_name='Фото работы')

    class Meta:
        verbose_name = 'Работа студента повышение квалификации'
        verbose_name_plural = 'Работы студентов повышение квалификации'
