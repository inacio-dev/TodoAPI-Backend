from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from user.models import Account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["email", "name", "surname", "is_active", "id"]
        

class AccountCreateSerializer(serializers.Serializer):

    email = serializers.EmailField(allow_null=False)
    name = serializers.CharField(max_length=30)
    surname = serializers.CharField(max_length=100)
    password = serializers.CharField(allow_null=True, allow_blank=True, max_length=50)
    rpassword = serializers.CharField(allow_null=True, allow_blank=True, max_length=50)

    def validate(self, data):
        if data["password"] and data["password"] != "":
            if data["password"] != data["rpassword"]:
                raise serializers.ValidationError(
                    "O campo 'senha' e 'confirmação de senha' são diferentes."
                )
        return data


class AccountUpdateSerializer(serializers.Serializer):

    email = serializers.EmailField(allow_null=False)
    name = serializers.CharField(max_length=30)
    surname = serializers.CharField(max_length=100)
    password = serializers.CharField(allow_null=True, allow_blank=True, max_length=50)
    rpassword = serializers.CharField(allow_null=True, allow_blank=True, max_length=50)
    is_active = serializers.BooleanField(default=True)

    def validate(self, data):
        if data["password"] != "":
            if data["password"] != data["rpassword"]:
                raise serializers.ValidationError(
                    "O campo 'senha' e 'confirmação de senha' são diferentes."
                )
        return data


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ["password"]


class AccountAlterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["name", "surname"]


class AccountDetailsSerializer(serializers.ModelSerializer):

    group = serializers.SerializerMethodField("list_groups")

    def list_groups(self, obj):
        group = []
        if obj.is_admin is True:
            group.append("admin")
        if obj.is_staff is True:
            group.append("staff")
        if obj.is_superuser is True:
            group.append("super")
        return group

    class Meta:
        model = Account
        fields = ["name", "surname", "email", "group"]


class AccountPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        allow_null=True, allow_blank=True, max_length=50
    )
    password = serializers.CharField(allow_null=True, allow_blank=True, max_length=50)
    rpassword = serializers.CharField(allow_null=True, allow_blank=True, max_length=50)

    def validate(self, data):
        if data["password"] and data["password"] != "":
            if data["password"] != data["rpassword"]:
                raise serializers.ValidationError(
                    "O campo 'senha' e 'confirmação de senha' são diferentes."
                )

        return data


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ["password", "is_admin", "is_staff", "is_superuser"]


class NewPasswordSerializer(serializers.Serializer):

    token = serializers.CharField(allow_null=True, allow_blank=True)

    password = serializers.CharField(allow_null=True, allow_blank=True)
    rpassword = serializers.CharField(allow_null=True, allow_blank=True)

    def validate(self, data):
        if data["password"] and data["password"] != "":
            if data["password"] != data["rpassword"]:
                raise serializers.ValidationError(
                    "O campo 'Nova Senha' e 'Repita a nova Senha' são diferentes."
                )

        try:
            if len(data["token"]) != 250:
                raise ValidationError("Token inválido ou expirado")
        except Exception:
            raise ValidationError("Token inválido ou expirado")

        try:
            if len(data["password"]) < 6:
                raise ValidationError("Informe uma senha com pelo menos 6 caracteres")
        except Exception:
            raise ValidationError("Informe uma senha com pelo menos 6 caracteres")

        return data
