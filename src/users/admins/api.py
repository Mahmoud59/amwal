from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.admins.serializers import AdminSerializer
from users.models import AdminAccount
from users.serializers import UserSerializer
from utils.permissions import AdminPermission


class AdminViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, AdminPermission)
    serializer_class = AdminSerializer
    queryset = AdminAccount.objects.all().order_by('-created')

    def create(self, request, *args, **kwargs):
        request.data['is_superuser'] = True
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        request.data['user'] = user_serializer.data['id']
        user_profile_serializer = self.serializer_class(data=request.data)
        user_profile_serializer.is_valid(raise_exception=True)
        user_profile_serializer.save()
        return Response(user_profile_serializer.data,
                        status=status.HTTP_201_CREATED)
