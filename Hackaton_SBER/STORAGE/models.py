import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from .model_validators import validate_passport_format, validate_deposit_fields
from .model_choices import FamilyStatus, HasChildren, ObligationStatus, ObligationRole, BankDepositExistance, BankDepositCategory, OtherCondition, ProductCategory, ApplicationStatus
from django.utils import timezone
# Create your models here.


class ApplicationBase(models.Model):

    name = models.CharField(max_length=90, verbose_name="ФИО")
    passport_data = models.CharField(max_length=11,
                                     validators=[validate_passport_format],
                                     verbose_name='серия и номер пасспорта',blank=True)
    registration_address = models.CharField(max_length=255, verbose_name="адрес регистрации", blank=True)
    actual_address = models.CharField(max_length=255, verbose_name="адрес проживания", blank=True)
    family_status = models.CharField(max_length=70,
                                    choices=FamilyStatus.choices,
                                    default=FamilyStatus.DEFAULT,
                                    verbose_name="Семейное положение")
    has_child = models.CharField(max_length=3,
                                choices=HasChildren.choices,
                                default=HasChildren.NO,
                                verbose_name="Наличие детей")
    work = models.CharField(max_length=255, verbose_name="Место работы", blank=True)
    work_experience = models.CharField(max_length=255, verbose_name='Стаж работы', blank=True)
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
    application_status = models.CharField(max_length=70,
                                    choices=ApplicationStatus.choices,
                                    default=ApplicationStatus.NEW,
                                    verbose_name="Статус заявки для андеррайтера")

    class Meta:
        verbose_name = "Кредитная заявка (базовая)"
        verbose_name_plural = "Кредитная заявка (базовая)"

    def __str__(self):
        return f'id: {self.pk}'
    # verification_additional_earn доп таблица

class CreditHistoryReport(models.Model):
    application = models.ForeignKey(ApplicationBase, related_name='score_rating', on_delete=models.CASCADE)
    score_rating = models.IntegerField(default=0, verbose_name="Скорбалл (оценка кредитной истории в баллах)",)

    class Meta:
        verbose_name = "Бюро кредитных историй"
        verbose_name_plural = "Бюро кредитных историй"

    def __str__(self):
        return f'application_id: {self.application}'

from django.db import models

class ObligationInformation(models.Model):
    credit_history_report = models.ForeignKey(CreditHistoryReport, related_name='obligations_to_score_reating', on_delete=models.CASCADE)
    application = models.ForeignKey(ApplicationBase, related_name='obligations_to_application', on_delete=models.CASCADE)
    obligation_type = models.CharField(max_length=50, verbose_name="Вид обязательства", blank=True)
    start_date = models.DateField(verbose_name="Дата открытия", blank=True)
    planned_closure_date = models.DateField(verbose_name="Плановая дата закрытия", blank=True)
    actual_closure_date = models.DateField(verbose_name="Фактическая дата закрытия", blank=True)
    role = models.CharField(max_length=50,
                            choices=ObligationRole.choices,
                            default=ObligationRole.BORROWER,
                            verbose_name="Роль (заемщик, поручитель, созаемщик)")
    status = models.CharField(max_length=50,
                              choices=ObligationStatus.choices,
                              default=ObligationStatus.CURRENT,
                              verbose_name="Статус (текущий, завершенный)")
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Сумма", blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="% ставка", blank=True)
    remaining_payment = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Остаток к выплате", blank=True)
    overdue = models.IntegerField(verbose_name="Просрочка в днях",
                                    blank=True)
    amount_overdue = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Сумма просрочки", blank=True)

    class Meta:
        verbose_name = "Информация об обязательствах"
        verbose_name_plural = "Информация об обязательствах"

    def save(self, *args, **kwargs):
        if not self.actual_closure_date:
            self.actual_closure_date = timezone.now().date()

        if self.actual_closure_date > self.planned_closure_date:
            time_difference = self.actual_closure_date - self.planned_closure_date
            self.overdue = time_difference.days
        else:
            self.overdue = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f'application_id: {self.credit_history_report.application.id}, ' \
               f'credit_history_report_id: {self.credit_history_report.id}, ' \
               f'obligation_type: {self.obligation_type}'


class BankDeposit(models.Model):
    application = models.ForeignKey(ApplicationBase,
                                    related_name='bank_deposit',
                                    on_delete=models.CASCADE)
    existence = models.CharField(max_length=3,
                                 choices=BankDepositExistance.choices,
                                 default=BankDepositExistance.NO,
                                 verbose_name='Наличие сбережений на счетах в Банке')
    category = models.CharField(max_length=50,
                                 choices=BankDepositCategory.choices,
                                 default=BankDepositCategory.DEFAULT,
                                 verbose_name='Категория накоплений (вид вклада)')
    size = models.DecimalField(max_digits=50,
                                decimal_places=2,
                                verbose_name='Размер вклада',
                               blank=True,
                               null=True)



    def clean(self):
        validate_deposit_fields(self.existence, self.category, self.size)
    class Meta:
        verbose_name = "Наличие сбережений на счетах в Банке:"
        verbose_name_plural = "Наличие сбережений на счетах в Банке:"

    def __str__(self):
        return f'application_id: {self.application}'

class RequestedConditions(models.Model):
    application = models.ForeignKey(ApplicationBase,
                                    related_name='requested_condition',
                                    on_delete=models.CASCADE)
    product_category = models.CharField(max_length=30,
                                        choices=ProductCategory.choices,
                                        default=ProductCategory.CONSUMER,
                                        verbose_name='Вид кредита')
    sum_max = models.DecimalField(max_digits=20,
                                  decimal_places=2,
                                  verbose_name="Максимальная сумма, которую может дать банк",
                                  blank=True)
    sum_requested = models.DecimalField(max_digits=20,
                                  decimal_places=2,
                                  verbose_name="Сумма, которую запрашивает клиент",
                                  blank=True)
    period_max = models.CharField(max_length=255,
                                  verbose_name='Максимальный срок, на который банк может выдать кредит',
                                  blank=True)
    period_requested = models.CharField(max_length=255,
                                        verbose_name='Срок, на который клиент просит кредит',
                                        blank=True)

    credit_rate = models.FloatField(verbose_name='Ставка по кредиту, которую предлагает банк в процентах',
                                    blank=True)
    credit_rate_requested = models.FloatField(verbose_name='Ставка по кредиту, которую запрашивает клиент в процентах',
                                              blank=True)
    payment_per_month = models.DecimalField(max_digits=20,
                                  decimal_places=2,
                                  verbose_name="Сумма ежемесячного платежа, предлагаемая банком (руб)",
                                  blank=True)
    other_condition = models.CharField(max_length=30,
                                 choices=OtherCondition.choices,
                                 default=OtherCondition.DEFAULT,
                                 verbose_name='Иные условия запрашиваемые по кредиту')

    class Meta:
        verbose_name = "Запрашиваемые и предлагаемые условия"
        verbose_name_plural = "Запрашиваемые и предлагаемые условия"

    def __str__(self):
        return f'application_id: {self.application}'


def document_upload_to(instance, filename):
    # Формируем путь /applications/application_{application_id}/название_поля
    return f'applications/application_{instance.application_id}/{filename}'
class DocumentPackage(models.Model):
    application = models.ForeignKey(ApplicationBase,
                                related_name='document_package',
                                on_delete=models.CASCADE)
    passport = models.FileField(upload_to=document_upload_to,
                                verbose_name='Паспорт клиента (pdf, jpg, png)',
                                blank=True)
    work_document = models.FileField(upload_to=document_upload_to,
                                verbose_name='Документ, подтверждающий трудовую занятость клиента (pdf, jpg, png)',
                                blank=True)
    earn_document = models.FileField(upload_to=document_upload_to,
                                verbose_name='Документ, подтверждающий официальный доход клиента (pdf, jpg, png)',
                                blank=True)
    additional_earn_document = models.FileField(upload_to=document_upload_to,
                                verbose_name='Документ, подтверждающий дополнительный доход клиента (pdf, jpg, png)',
                                blank=True)
    additional_document_1 = models.FileField(upload_to=document_upload_to,
                                verbose_name='Иные документы, способные повлиять на принятие решения по клиенту (pdf, jpg, png)',
                                blank=True)
    additional_document_2 = models.FileField(upload_to=document_upload_to,
                                verbose_name='Иные документы, способные повлиять на принятие решения по клиенту (pdf, jpg, png)',
                                blank=True)
    additional_document_3 = models.FileField(upload_to=document_upload_to,
                                verbose_name='Иные документы, способные повлиять на принятие решения по клиенту (pdf, jpg, png)',
                                blank=True)
    additional_document_4 = models.FileField(upload_to=document_upload_to,
                                verbose_name='Иные документы, способные повлиять на принятие решения по клиенту (pdf, jpg, png)',
                                blank=True)
    additional_document_5 = models.FileField(upload_to=document_upload_to,
                                verbose_name='Иные документы, способные повлиять на принятие решения по клиенту (pdf, jpg, png)',
                                blank=True)

    class Meta:
        verbose_name = "Пакет документов клиента"
        verbose_name_plural = "Пакет документов клиента"

    def __str__(self):
        return f'application_id: {self.application}'