from rest_framework import serializers

from users.models import UserAccount


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        exclude = ('uuid',)


class ListUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'
