from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import UserAccount
from users.serializers import UserSerializer
from users.users.serializers import (
    ListUserModelSerializer, UserModelSerializer,
)


class UserViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserModelSerializer
    queryset = UserAccount.objects.all().order_by('-created')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            self.serializer_class = ListUserModelSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        request.data['user'] = user_serializer.data['id']
        user_profile_serializer = self.serializer_class(data=request.data)
        user_profile_serializer.is_valid(raise_exception=True)
        user_profile_serializer.save()
        return Response(user_profile_serializer.data,
                        status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(UserAccount, uuid=kwargs['uuid'])
        user_serializer = self.serializer_class(user)
        return Response(data=user_serializer.data,
                        status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = get_object_or_404(UserAccount, uuid=kwargs['uuid'])
        user_serializer = self.serializer_class(user, data=request.data,
                                                partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response(data=user_serializer.data,
                        status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        user = get_object_or_404(UserAccount, uuid=kwargs['uuid'])
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
