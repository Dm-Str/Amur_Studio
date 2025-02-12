from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Courses, Discounts, StudentHomework, BonusTransaction
from .notifications import *


@receiver(post_save, sender=Courses)
def course_created(sender, instance, created, **kwargs):
    if created:
        notify_new_course(instance)


@receiver(post_save, sender=Discounts)
def discount_created(sender, instance, created, **kwargs):
    if created:
        pass


@receiver(post_save, sender=StudentHomework)
def student_homework_created(sender, instance, created, **kwargs):
    if not created:
        if instance.status == 1:
            notify_homework_accepted(instance)


@receiver(post_save, sender=BonusTransaction)
def bonus_transaction_created(sender, instance, created, **kwargs):
    if created:
        pass
