import jwt
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework.response import Response


def decode_token(request):
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    if not auth:
        return Response({'message': 'You don\'t have permission'})
    parts = auth.split()
    try:
        token = parts[1]
        secret_key = 'mysecretkey'
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
    except Exception:
        raise PermissionDenied

    return decoded_token


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        if decode_token(request)['user_type'] == 'admin':
            return True
        return False


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if decode_token(request)['user_type'] == 'user':
            return True
        return False
