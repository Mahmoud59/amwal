from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, password):
        """Hash the password correctly."""
        return make_password(password)
