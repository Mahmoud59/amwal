from django.db import models
from django_extensions.db.models import TimeStampedModel
from safedelete.models import SafeDeleteModel

from users.models import UserAccount


class Food(TimeStampedModel, SafeDeleteModel):
    name = models.CharField('Name', max_length=100)


class UserFood(TimeStampedModel, SafeDeleteModel):
    calorie_value = models.FloatField('Calorie Value', default=0)
    dose_time = models.DateTimeField('Dose Time')
    food = models.ForeignKey(Food, related_name="user_dose_food",
                             on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UserAccount, related_name="user_dose_user",
                             on_delete=models.SET_NULL, null=True)
