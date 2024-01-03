from django.db import IntegrityError
from rest_framework.permissions import IsAdminUser
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from TodoAPI.utils import (
    GenericSimpleApiView,
    random_password,
)
from user.serializers import (
    AccountAlterSerializer,
    AccountDetailsSerializer,
    AccountCreateSerializer,
    AccountPasswordSerializer,
    NewPasswordSerializer,
    UserSerializer
)
from user.models import Account
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import authentication_classes, permission_classes


@authentication_classes([])
@permission_classes([])
class AccountView(GenericSimpleApiView):
    def post(self, request, format=None):

        req = AccountCreateSerializer(data=request.data)

        if req.is_valid():
            data = req.data
            try:
                if data["password"] is None:
                    data["password"] = random_password(total=10)

                del data["rpassword"]

                Account.objects.create_user(**data)

                del data["password"]

                return JsonResponse(data=data, status=status.HTTP_201_CREATED)

            except IntegrityError:

                return JsonResponse(
                    data={
                        "error": f"Já existe um usuário com esse email '{data['email']}'"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            except Exception as e:

                return JsonResponse(
                    data={"error": e.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return JsonResponse(
                data={"error": req.errors}, status=status.HTTP_400_BAD_REQUEST
            )

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        if user.is_staff:
            token["group"] = "staff"
        if user.is_admin:
            token["group"] = "admin"
        elif user.is_superuser:
            token["group"] = "super"

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer