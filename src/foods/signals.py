from datetime import datetime

from django.db.models import Sum
from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

from foods.models import UserFood


@receiver(pre_save, sender=UserFood)
def check_user_food_availability_pre_save(sender, instance, **kwargs):
    today_user_dose = UserFood.objects.filter(
        user=instance.user.uuid, dose_time__date=datetime.today().date()
    ).aggregate(Sum('calorie_value'))['calorie_value__sum']
    if today_user_dose and \
       today_user_dose + instance.calorie_value > instance.user.day_dose_limit:
        raise ValidationError({
            "message": f"Attention, your limit for one day is"
                       f" {instance.user.day_dose_limit}"})
