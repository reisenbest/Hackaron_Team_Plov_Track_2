from django.db import models
class FamilyStatus(models.TextChoices):
    DEFAULT = 'Информация отсутствует', 'Информация отсутствует'
    MARRIED_FEMALE = 'Замужем', 'Замужем'
    SINGLE_FEMALE = 'Не замужем', 'Не замужем'
    MARRIED_MALE = 'Женат', 'Женат'
    SINGLE_MALE = 'Холос', 'Холост'

class HasChildren(models.TextChoices):
    NO = 'Нет', 'Нет'
    YES = 'Да', 'Да'


class ObligationRole(models.TextChoices):
    BORROWER = 'Заемщик', 'Заемщик'
    GUARANTOR = 'Поручитель', 'Поручитель'
    CO_BORROWER = 'Созаемщик', 'Созаемщик'

class ObligationStatus(models.TextChoices):
    CURRENT = 'Текущий', 'Текущий'
    COMPLETED = 'Завершенный', 'Завершенный'

class BankDepositExistance(models.TextChoices):
    YES = 'Да', 'Да'
    NO = 'Нет', 'Нет'

class BankDepositCategory(models.TextChoices):
    SAVING = 'Сберегательный', 'Сберегательный'
    ACCUMULATIVE = 'Накопительный', 'Накопительный'
    SETTLEMENT = 'Расчетный', 'Расчетный'
    DEFAULT = 'Отсутствует', 'Отсутствует'

class ProductCategory(models.TextChoices):
    CONSUMER = 'Потребительский кредит','Потребительский кредит'
    EDUCATION = 'Кредит на образование', 'Кредит на образование',
    AUTO = 'Кредит на машину', 'Кредит на машину'
    IPOTECA = 'Ипотечный кредит', 'Ипотечный кредит'


class OtherCondition(models.TextChoices):
    DEFERRED_REPAYMENT = 'Отсроченное погашение', 'Отсроченное погашение'
    CREDIT_HOLIDAYS = 'Кредитные каникулы', 'Кредитные каникулы'
    DEFAULT = 'Специальные уловия отсуствуют', 'Специальные уловия отсуствуют'
