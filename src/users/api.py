from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import TokenSerializer


class UserLoginAPIView(TokenObtainPairView):
    serializer_class = TokenSerializer
