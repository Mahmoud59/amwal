from datetime import datetime, timedelta

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from foods.models import Food, UserFood
from foods.serializers import FoodSerializer, UserFoodSerializer, ListUserFoodSerializer
from users.models import UserAccount
from utils.permissions import AdminPermission, UserPermission, decode_token


class FoodViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, AdminPermission |
                          UserPermission)
    serializer_class = FoodSerializer
    queryset = Food.objects.order_by('-id')


class UserFoodViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, AdminPermission |
                          UserPermission)
    serializer_class = UserFoodSerializer

    def get_queryset(self):
        user_token = decode_token(self.request)
        if user_token['user_type'] == 'user' and \
           user_token['uuid'] != self.kwargs['uuid']:
            raise PermissionDenied
        return UserFood.objects.filter(
            user__uuid=self.kwargs['uuid']).order_by('-id')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            self.serializer_class = ListUserFoodSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        request.data['user'] = get_object_or_404(
            UserAccount, uuid=kwargs['uuid']).pk
        user_food = self.serializer_class(data=request.data)
        user_food.is_valid(raise_exception=True)
        user_food.save()
        return Response(data=user_food.data,
                        status=status.HTTP_201_CREATED)


class UserFoodReportAPIView(APIView):
    permission_classes = (IsAuthenticated, AdminPermission)

    def get(self, request, *args, **kwargs):
        today = datetime.today().date()
        from_date = request.query_params.get(
            'from_date', today - timedelta(days=7))
        to_date = request.query_params.get('to_date', today)

        users_foods = UserFood.objects.filter(
            dose_time__date__gte=from_date,
            dose_time__date__lte=to_date
        ).order_by('-id')
        users_foods_serializer = UserFoodSerializer(
            users_foods, many=True)

        return Response(data=users_foods_serializer.data,
                        status=status.HTTP_200_OK)
