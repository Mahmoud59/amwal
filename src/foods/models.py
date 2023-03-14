from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from safedelete.models import SafeDeleteModel

from users.models import UserAccount


class Food(TimeStampedModel, SafeDeleteModel):
    name = models.CharField('Name', max_length=100)


class UserFood(TimeStampedModel, SafeDeleteModel):
    class MealType(models.TextChoices):
        BREAKFAST = 'breakfast', _('breakfast')
        LUNCH = 'lunch', _('lunch')
        DINNER = 'dinner', _('dinner')

    meal = models.TextField(choices=MealType.choices,
                            default=MealType.BREAKFAST)
    calorie_value = models.FloatField('Calorie Value', default=0)
    dose_time = models.DateTimeField('Dose Time')
    food = models.ForeignKey(Food, related_name="user_dose_food",
                             on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UserAccount, related_name="user_dose_user",
                             on_delete=models.SET_NULL, null=True)
