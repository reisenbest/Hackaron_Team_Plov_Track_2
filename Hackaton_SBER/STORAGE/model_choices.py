from django.db import models
class FamilyStatus(models.TextChoices):
    DEFAULT = 'Информация отсутствует', 'Информация отсутствует'
    MARRIED_FEMALE = 'Замужем', 'Замужем'
    SINGLE_FEMALE   = 'Не замужем', 'Не замужем'
    MARRIED_MALE = 'Женат', 'Женат'
    SINGLE_MALE = 'Холос', 'Холост'

class HasChildren(models.TextChoices):
    NO = 'Нет', 'Нет'
    YES = 'Да','Да'

