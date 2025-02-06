from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Max
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import datetime
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


class Modules(models.Model):
    course = models.ForeignKey(Courses, related_name='modules', on_delete=models.CASCADE, verbose_name='Курс')
    title = models.CharField(max_length=200, verbose_name='Название модуля')
    order = models.PositiveIntegerField(verbose_name='Порядок модуля')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
        ordering = ['order']


class Topics(models.Model):
    course = models.ForeignKey(Courses, related_name='topics', on_delete=models.CASCADE, verbose_name='Курс')
    module = models.ForeignKey(Modules, related_name='topics', on_delete=models.CASCADE, verbose_name='Модуль')
    title = models.CharField(max_length=200, default='Новая тема', verbose_name='Название темы')
    order = models.PositiveIntegerField(verbose_name='Порядок темы')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        ordering = ['order']


class Lesson(models.Model):
    course = models.ForeignKey(Courses, related_name='lessons', on_delete=models.CASCADE,
                               verbose_name='Курс')
    module = models.ForeignKey(Modules, related_name='lessons', blank=True, null=True,
                                on_delete=models.CASCADE, verbose_name='Модуль')
    topic = models.ForeignKey(Topics, related_name='lessons', blank=True, null=True,
                              on_delete=models.CASCADE, verbose_name='Тема')
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
    courses = models.ManyToManyField(Courses, related_name='persons', blank=True, verbose_name='Курсы')
    username = models.CharField(max_length=45, unique=True, validators=[validate_name], verbose_name='Логин')
    number = models.CharField(max_length=25, unique=True, validators=[validate_phone], verbose_name='Телефон')
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='День рождения')
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='Город')
    messenger= models.CharField(max_length=50, verbose_name='Мессенджер')
    photo = models.ImageField(upload_to='images/', default='images/default_prof_img.jpg', verbose_name='Фото профиля')
    experience = models.CharField(max_length=50, blank=True, null=True, verbose_name='Опыт работы')
    bonuses = models.IntegerField(default=50, verbose_name='Бонусы')

    @classmethod
    def generate_username(cls, email):
        username = email.split('@')[0]
        last_pk = cls.objects.aggregate(max_id=Max('id'))
        last_pk = last_pk['max_id']

        if last_pk is None:
            last_pk = 0

        new_username = username + str(last_pk)
        return new_username

    def calculate_review_bonuses(self, amount):
        """
            Увеличивает количество бонусов на указанную сумму.
        """
        self.bonuses += amount
        self.save()

    def calculate_birthday_bonuses(self):
        """
           Увеличивает количество бонусов на 500, если сегодня день рождения пользователя.
           Проверяет, совпадает ли текущая дата с датой рождения пользователя.
           Если совпадает, добавляет 500 бонусов и сохраняет изменения.
        """
        today = datetime.date.today()
        if self.date_of_birth:
            if (self.date_of_birth.month == today.month
                    and self.date_of_birth.day == today.day):
                self.bonuses += 500
                self.save()

    def calculate_professional_holiday_bonuses(self):
        """
            Увеличивает количество бонусов на 300, если сегодня профессиональный праздник.
            Проверяет, совпадает ли текущая дата с 24 марта.
            Если совпадает, добавляет 300 бонусов и сохраняет изменения.
        """
        today = datetime.date.today()
        if today == datetime.date(today.year, 3, 24):
            self.bonuses += 300
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

    @classmethod
    def get_student_progress(cls, course, request):
        return cls.objects.filter(person=request.user, course=course).all()

    def __str__(self):
        return f"{self.person.username} - {self.course.title} - {self.current_lesson}"

    class Meta:
        verbose_name = 'Прогресс пользователя по курсу'


class StudentHomework(models.Model):
    STATUS_CHOICES = [
        (0, 'Не принято'),
        (1, 'Принято'),
        (2, 'На проверке'),
    ]

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='homework',
                               verbose_name='Студент')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='homework',
                               verbose_name='Курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='homework',
                               verbose_name='Урок')
    description = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Комментарий')
    status = models.IntegerField(choices=STATUS_CHOICES, default=2, verbose_name='Статус' )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.person} - {self.lesson}"

    class Meta:
        verbose_name = 'Домашняя работа студента'
        verbose_name_plural = 'Домашние работы студентов'
        ordering = ['-id']

class HomeworkImage(models.Model):
    homework = models.ForeignKey(StudentHomework, on_delete=models.CASCADE, related_name='images')
    images = models.ImageField(upload_to='student_homework/', blank=True, null=True, verbose_name='Фото')

    class Meta:
        verbose_name = 'Фото домашней работы'
        verbose_name_plural = 'Фото домашних работ'


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