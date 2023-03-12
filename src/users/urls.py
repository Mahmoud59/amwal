from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from users.admins.api import AdminViewSet
from users.users.api import UserViewSet

urlpatterns = [
    # Admin
    path('admins/login/', TokenObtainPairView.as_view(),
         name='admin-login'),

    path('admins/', AdminViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='admin-list'),
    path('admins/<str:uuid>/', AdminViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='admin-detail'),

    # User
    path('users/login/', TokenObtainPairView.as_view(),
         name='user-login'),

    path('users/', UserViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='user-list'),
    path('users/<str:uuid>/', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='user-detail'),
]
