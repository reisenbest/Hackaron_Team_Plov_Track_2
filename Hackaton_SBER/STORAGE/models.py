from django.conf import settings
from django.db import models
from .model_validators import validate_passport_format
from .model_choices import FamilyStatus, HasChildren, ObligationStatus, ObligationRole
from django.utils import timezone
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
