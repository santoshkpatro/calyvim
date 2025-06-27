from rest_framework import serializers

from calyvim.models.user import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    organization = serializers.CharField(required=True)


class LoggedInUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "full_name",
            "display_name",
        ]
