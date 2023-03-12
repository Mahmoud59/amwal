from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from foods.models import Food, UserFood
from foods.serializers import FoodSerializer, UserFoodSerializer
from users.models import UserAccount


class FoodViewSet(ModelViewSet):
    permission_classes = ()
    serializer_class = FoodSerializer
    queryset = Food.objects.order_by('-id')


class UserFoodViewSet(ModelViewSet):
    permission_classes = ()
    serializer_class = UserFoodSerializer

    def get_queryset(self):
        return UserFood.objects.filter(
            user__uuid=self.kwargs['uuid'])

    def create(self, request, *args, **kwargs):
        request.data['user'] = get_object_or_404(
            UserAccount, uuid=kwargs['uuid']).pk
        user_food = self.serializer_class(data=request.data)
        user_food.is_valid(raise_exception=True)
        user_food.save()
        return Response(data=user_food.data,
                        status=status.HTTP_201_CREATED)
