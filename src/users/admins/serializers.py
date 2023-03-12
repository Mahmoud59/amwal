from rest_framework import serializers

from users.models import AdminAccount


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAccount
        exclude = ('uuid',)
