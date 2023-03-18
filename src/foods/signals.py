from django.db.models import Sum
from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

from foods.models import UserFood


@receiver(pre_save, sender=UserFood)
def check_user_food_availability_pre_save(sender, instance, **kwargs):
    today_user_dose = UserFood.objects.filter(
        user=instance.user.uuid, dose_time__date=instance.dose_time.date()
    )

    # Check dose for one day
    today_user_calories = today_user_dose.aggregate(
        Sum('calorie_value'))['calorie_value__sum']
    if today_user_calories and \
       today_user_calories + instance.calorie_value > \
            instance.user.day_dose_limit:
        raise ValidationError({
            "message": f"Attention, your limit for one day is"
                       f" {instance.user.day_dose_limit}"})

    # Check dose for breakfast
    today_breakfast = today_user_dose.filter(
        meal=UserFood.MealType.BREAKFAST,
        dose_time__date=instance.dose_time.date()
    ).count()
    if instance.meal == UserFood.MealType.BREAKFAST and today_breakfast >= 3:
        raise ValidationError({
            "message": "Attention, your limit for breakfast is 3 foods."})

    # Check dose for lunch
    today_lunch = today_user_dose.filter(meal=UserFood.MealType.LUNCH).count()
    if instance.meal == UserFood.MealType.LUNCH and today_lunch >= 5:
        raise ValidationError({
            "message": "Attention, your limit for lunch is 5 foods."})

    # Check dose for dinner
    today_dinner = today_user_dose.filter(
        meal=UserFood.MealType.DINNER).count()
    if instance.meal == UserFood.MealType.DINNER and today_dinner >= 2:
        raise ValidationError({
            "message": "Attention, your limit for dinner is 2 foods."})
