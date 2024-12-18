from django.core.exceptions import ValidationError
import re


def validate_name(value):
    if not re.match(r"^[A-Za-zА-Яа-яЁё0-9_-]+$", value):
        raise ValidationError("Логин может содержать только буквы, цифры, дефисы и нижние подчеркивания.")

    if not (1 < len(value) < 45):
        raise ValidationError("Длина логина должна быть от 1 до 25 символов.")


def validate_email(value):
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, value):
        raise ValidationError(f"{value if value else 'Пустое значение'} "
                              f"не является корректным адресом электронной почты.")


def validate_first_name(value):
    if not re.match(r"^[A-Za-zА-Яа-яЁё\s'-]+$", value):
        raise ValidationError("Имя может содержать только буквы, пробелы, дефисы и апострофы.")
    if not (1 < len(value) < 25):
        raise ValidationError("Длина имени должна быть от 1 до 25 символов.")


def validate_last_name(value):
    if not re.match(r"^[A-Za-zА-Яа-яЁё\s'-]+$", value):
        raise ValidationError("Фамилия может содержать только буквы, пробелы, дефисы и апострофы.")
    if not (1 < len(value) < 35):
        raise ValidationError("Длина фамилии должна быть от 1 до 25 символов.")


def validate_phone(value):
    cleaned_value = re.sub(r'[^0-9+]', '', value)

    if not re.match(r'^\+7\d{10}$', cleaned_value):
        raise ValidationError("Номер телефона должен начинаться с +7 и содержать 10 цифр после кода страны.")


def validate_password(value):
    if re.search(r'[А-Яа-я]', value):
        raise ValidationError("Пароль может содержать только буквы латиницы.")

    if not re.search(r'\d', value):
        raise ValidationError("Пароль должен содержать хотя бы одну цифру.")

    if not re.search(r'[A-Z]', value):
        raise ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")

    if len(value) > 50:
        raise ValidationError("Пароль не должен превышать 50 символов.")

    if len(value) < 6:
        raise ValidationError("Пароль должен содержать не менее 6 символов.")
