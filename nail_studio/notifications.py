from datetime import datetime, timezone
from .models import Courses, Notifications, Discounts, Person
from telegram import Bot


# TELEGRAM_BOT_TOKEN = ''
# CHAT_ID = ''
#
#
# async def send_message():
#     bot = Bot(token=TELEGRAM_BOT_TOKEN)
#     await bot.send_message(chat_id=CHAT_ID, text='Вышел новый курс! СтрелаАмура.')


def notify_welcome_student(instance):
    Notifications.objects.create(
        user=instance,
        topic=f'{datetime.now(timezone.utc).strftime("%d.%m.%Y")}<br>'
              f'Благодарим за регистрацию!',
        message="Здравствуйте! 🎉<br>"
                "Вам начислено 50 бонусов за регистрацию на нашей площадке!<br>"
                "Подробнее о системе бонусов можно узнать во вкладке 'Бонусы'."
                "Мы надеемся, что они принесут вам много приятных моментов!",
    )


def notify_new_course(instance):
    # TODO: Сделать цвет даты серым или черным
    all_persons = Person.objects.all()
    for person in all_persons:
        Notifications.objects.create(
            user=person,
            topic=f'{datetime.now(timezone.utc).strftime("%d.%m.%Y")}<br>'
                  f'Новый курс «{instance.title}»!',
            message='Ура! На нашей площадке вышел новый курс! 🎉<br>'
                    'Скорее приступайте к обучению!'
        )


def notify_homework_accepted(instance):
    Notifications.objects.create(
        user=instance.person,
        topic=f'Домашнее задание принято. {datetime.now(timezone.utc).strftime("%d.%m.%Y")}<br>'
              f'Курс: «{instance.course.title}»',
        message=f'Ваше домашнее задание было успешно принято преподавателем!<br>'
                f'Урок: «{instance.lesson.title}»',
    )


def notify_put_bonuses_student(instance):
    # TODO: Использовать одно уведомление для всех начислений?
    #  Либо создать под каждое начисление отдельное.
    Notifications.objects.create(
        user=instance.person,
        topic=f'Начисление бонусов. {datetime.now(timezone.utc).strftime("%d.%m.%Y")}',
        message=f'Вам начислены бонусы за!'
    )
