from django.conf import settings
from django.db import models
from .model_validators import validate_passport_format
from .model_choices import FamilyStatus, HasChildren
# Create your models here.


class ApplicationBase(models.Model):

    name = models.CharField(max_length=90, verbose_name="ФИО")
    passport_data = models.CharField(max_length=11,
                                     validators=[validate_passport_format],
                                     verbose_name='серия и номер пасспорта',blank=True)
    registration_address = models.CharField(max_length=255, verbose_name="адрес регистрации", blank=True)
    actual_address = models.CharField(max_length=255, verbose_name="адрес проживания", blank=True)
    family_status = models.CharField(max_length=40,
                                    choices=FamilyStatus.choices,
                                    default=FamilyStatus.DEFAULT,
                                    verbose_name="Семейное положение")
    has_child = models.CharField(max_length=3,
                                choices=HasChildren.choices,
                                default=HasChildren.NO,
                                verbose_name="Наличие детей")
    work = models.CharField(max_length=255, verbose_name="Место работы", blank=True)
    work_experience = models.DurationField(verbose_name='Стаж работы', blank=True)
    work_position = models.CharField(max_length=255, verbose_name="Должность", blank=True)
    aprove_salary_per_month = models.DecimalField(max_digits=20,
                                                  decimal_places=2,
                                                  verbose_name='Ежемесячный подтвержденный доход по месту работы',
                                                  blank=True)
    additional_earn_per_month = models.DecimalField(max_digits=20,
                                                    decimal_places=2,
                                                    verbose_name='Ежемесячный дополнительный доход',
                                                    blank=True)
    source_additional_earn = models.CharField(max_length=255, verbose_name='Источник дополнительного дохода', blank=True)

    class Meta:
        verbose_name = "Кредитная заявка (базовая)"
        verbose_name_plural = "Кредитная заявка (базовая)"

    def __str__(self):
        return f'id: {self.pk}'
    # verification_additional_earn доп таблица

