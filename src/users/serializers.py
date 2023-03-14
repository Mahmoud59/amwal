from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import AdminAccount, UserAccount


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, password):
        """Hash the password correctly."""
        return make_password(password)


class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        user_account = AdminAccount.objects.filter(
            user__username=user).first()
        user_type = "admin"
        if not user_account:
            user_account = UserAccount.objects.filter(
                user__username=user).first()
            user_type = "user"

        if not user_account:
            raise NotAuthenticated

        token = super().get_token(user)
        # Add custom claims
        token['user_type'] = user_type
        token['uuid'] = str(user_account.uuid)
        return token
