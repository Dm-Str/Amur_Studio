from django.contrib.auth.models import AbstractUser
from django.db import models
from nail_studio.validators import *


class Courses(models.Model):
    # Разбить на две модели. Исправить/дописать поля.
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.IntegerField(default=0, verbose_name='Цена')
    number_of_hours = models.IntegerField(default=0)
    date_start_after_payment = models.DateField(verbose_name='Начало')
    date_end = models.DateField(blank=True, null=True, verbose_name='Конец')
    course_type = models.CharField(max_length=100, default='Базовый', verbose_name='Тип')
    #location = models.CharField(default='Оффлайн')
    image = models.ImageField(upload_to='images/')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Person(AbstractUser):
    # Исправить окно регистрации. Добавить имя фамилию.
    # Нужно ли разбить сайт студии и сайт школы на разные приложения?
    # Добавить фильтр для пользователей которые не успели пройти курс за отведенное время.
    number = models.CharField(max_length=25, unique=True, validators=[validate_phone], verbose_name='Телефон')
    location = models.CharField(max_length=50)
    experience = models.CharField(max_length=50, default='Нет') # стаж
    bonuses = models.IntegerField(default=0)
    #пройденные курсы =
    certificates = models.ImageField(upload_to='certificates/', verbose_name='Сертификаты')
    courses = models.ManyToManyField(Courses, related_name='persons')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Discounts(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField()
    date_start = models.DateField(verbose_name='Начало')
    date_end = models.DateField(blank=True, null=True, verbose_name='Конец')
    courses = models.ManyToManyField(Courses, related_name='discounts') # ???

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Questions(models.Model):
    title = models.CharField(max_length=300, verbose_name='Название')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answers(models.Model):
    title = models.CharField(max_length=300, verbose_name='Название')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    question = models.ForeignKey(Questions, related_name='answers', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class StudentsWorkBasicCourse(models.Model):
    image = models.ImageField(upload_to='images/', verbose_name='Фото')

    class Meta:
        verbose_name = 'Работа студента базовый курс'
        verbose_name_plural = 'Работы студентов базовый курс'


class StudentsWorkRetrainingCourse(models.Model):
    image = models.ImageField(upload_to='images/', verbose_name='Фото')

    class Meta:
        verbose_name = 'Работа студента повышение квалификации'
        verbose_name_plural = 'Работы студентов повышение квалификации'
