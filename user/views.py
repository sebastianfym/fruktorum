from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from user.serializers import UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from user.models import User
from user.services import get_access_token


class Authentication(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=["POST"], detail=False, url_path="auth")
    def authorization_user(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            # user = User.objects.get(email=email)
            # if user.check_password(password):
            user = User.objects.get(email=email, password=password)
            user_data = self.get_serializer(user).data
            token = get_access_token(user, request)
            return Response({'token': token, 'user': user_data}, 200)



        except ObjectDoesNotExist:
            return Response({'detail': 'Неверный логин или пароль'}, 403)

    @action(methods=["POST"], detail=False, url_path="registration")
    def registration(self, request):
        email, password = request.data.get("email"), request.data.get("password")
        if email is None or password is None:
            return Response({"error": "Вы забыли указать email или пароль"}, status=400)
        if User.objects.filter(email=email).exists():
            return Response({'detail': 'Пользователь с данным email уже зарегистрирован в системе'}, 400)

        try:
            first_name = request.data.get('first_name')
        except KeyError:
            first_name = None

        try:
            last_name = request.data.get('last_name')
        except KeyError:
            last_name = None

        User.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        return Response({"detail": "Вы успешно зарегестрировались"}, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, url_path='logout')
    def logout(self, request):
        try:
            token = get_access_token(request.user, request)
            return Response({"detail": "Вы разлогинились."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Произошла ошибка: {e}."},
                            status=status.HTTP_400_BAD_REQUEST)
