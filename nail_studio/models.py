from django.contrib.auth.models import AbstractUser
from django.db import models
from nail_studio.validators import *


class Courses(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField(default=0)
    number_of_hours = models.IntegerField(default=0)
    date_start_after_payment = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    course_type = models.CharField(max_length=100, default='Базовый')
    image = models.ImageField(upload_to='images/')


class Person(AbstractUser):
    number = models.CharField(max_length=25, unique=True, validators=[validate_phone])
    location = models.CharField(max_length=50)
    experience = models.CharField(max_length=50, default='Нет') # стаж
    bonuses = models.IntegerField(default=0)
    certificates = models.ImageField(upload_to='certificates/')
    courses = models.ManyToManyField(Courses, related_name='persons')


class Discounts(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    courses = models.ManyToManyField(Courses, related_name='discounts') # ???


class Questions(models.Model):
    title = models.CharField(max_length=300)
    created_at = models.DateField(auto_now_add=True)


class Answers(models.Model):
    title = models.CharField(max_length=300)
    created_at = models.DateField(auto_now_add=True)
    question = models.ForeignKey(Questions, related_name='answers', on_delete=models.CASCADE)


class StudentsWorkBasicCourse(models.Model):
    image = models.ImageField(upload_to='images/')


class StudentsWorkRetrainingCourse(models.Model):
    image = models.ImageField(upload_to='images/')
