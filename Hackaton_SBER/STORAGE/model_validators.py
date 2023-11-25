from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
def validate_passport_format(value):
    if not value or len(value) != 11:
        raise ValidationError('Паспортные данные должны состоять из цифр и быть в формате - "XXXX XXXXXX".')