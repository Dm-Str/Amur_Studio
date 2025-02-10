from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Courses, Discounts, StudentHomework, BonusTransaction
from telegram import Bot


TELEGRAM_BOT_TOKEN = ''
CHAT_ID = ''


# async def send_message():
#     bot = Bot(token=TELEGRAM_BOT_TOKEN)
#     await bot.send_message(chat_id=CHAT_ID, text='Вышел новый курс! СтрелаАмура.')


@receiver(post_save, sender=Courses)
def course_created(sender, instance, created, **kwargs):
    if created:
        try:
            print('Уведомление ползователю')
        except Exception as e:
            print(e)


@receiver(post_save, sender=Discounts)
def discount_created(sender, instance, created, **kwargs):
    if created:
        pass


@receiver(post_save, sender=StudentHomework)
def student_homework_created(sender, instance, created, **kwargs):
    if not created:
        if instance.status == 1:
            pass


@receiver(post_save, sender=BonusTransaction)
def bonus_transaction_created(sender, instance, created, **kwargs):
    if created:
        pass
