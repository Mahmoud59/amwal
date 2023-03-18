from django.urls import path
from rest_framework.routers import DefaultRouter

from foods.api import (
    FoodViewSet, UserFoodLimitAPIView, UserFoodReportAPIView, UserFoodViewSet,
)

urlpatterns = [
    path('users/<str:uuid>/foods/', UserFoodViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='user-food-list'),
    path('users/<str:uuid>/foods/<int:pk>/', UserFoodViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='user-food-detail'),
    path('users-foods/report/', UserFoodReportAPIView.as_view(),
         name='user-food-report-list'),
    path('users/<str:uuid>/foods/limits/', UserFoodLimitAPIView.as_view(),
         name='user-food-limits'),
]

router = DefaultRouter()
router.register(r'foods', FoodViewSet, basename='food')
urlpatterns += router.urls
