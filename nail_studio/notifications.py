from datetime import datetime, timezone
from .models import Courses, Notifications, Discounts
from telegram import Bot


# TELEGRAM_BOT_TOKEN = ''
# CHAT_ID = ''
#
#
# async def send_message():
#     bot = Bot(token=TELEGRAM_BOT_TOKEN)
#     await bot.send_message(chat_id=CHAT_ID, text='Вышел новый курс! СтрелаАмура.')


def notify_homework_accepted(person, homework_instance):
    Notifications.objects.create(
        user=person,
        topic=f'Домашнее задание. Курс: {homework_instance.course.title}.'
              f'{datetime.now(timezone.utc).strftime("%H:%M  %d.%m.%Y")}',
        message=f'Ваше домашнее задание для урока принято!',
    )
