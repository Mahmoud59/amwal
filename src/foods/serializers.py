from rest_framework import serializers

from foods.models import Food, UserFood


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class UserFoodSerializer(serializers.ModelSerializer):
    calorie_value = serializers.FloatField(
        required=True, min_value=0.1, max_value=2.1)

    class Meta:
        model = UserFood
        fields = '__all__'
        extra_kwargs = {'food': {'required': True}}
