from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .model_choices import BankDepositCategory, BankDepositExistance
def validate_passport_format(value):
    if not value or len(value) != 11:
        raise ValidationError('Паспортные данные должны состоять из цифр и быть в формате - "XXXX XXXXXX".')


def validate_deposit_fields(existence, category, size):
    if existence == BankDepositExistance.YES and not size:
        raise ValidationError({'size': 'Поле "Размер вклада" не может быть пустым, если есть сбережения в банке.'})

    if existence == BankDepositExistance.YES and category == BankDepositCategory.DEFAULT:
        raise ValidationError({'category': 'Категория накоплений не может отсутствовать.'})