from django.core.exceptions import ValidationError
import re


def validate_name(value):
    if not re.match(r"^[A-Za-zА-Яа-яЁё\s'-]+$", value):
        raise ValidationError("Имя может содержать только буквы, пробелы, дефисы и апострофы.")
    if not (1 < len(value) < 25):
        raise ValidationError("Длина имени должна быть от 1 до 25 символов.")


def validate_email(value):
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, value):
        raise ValidationError(f"{value} не является корректным адресом электронной почты.")


def validate_phone(value):
    phone_regex = r'^\d{10}$'
    if not re.match(phone_regex, value):
        raise ValidationError("Номер телефона должен содержать ровно 10 цифр.")


def validate_password(value):
    if not re.search(r'\d', value):
        raise ValidationError("Пароль должен содержать хотя бы одну цифру.")

    if not re.search(r'[A-Z]', value):
        raise ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError("Пароль должен содержать хотя бы один специальный символ.")

    if len(value) > 50:
        raise ValidationError("Пароль не должен превышать 50 символов.")

    if len(value) < 6:
        raise ValidationError("Пароль должен содержать не менее 6 символов.")
