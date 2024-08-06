from rest_framework import serializers
from django.contrib.auth.models import User
from .validators import AuthorsRegisterValidator


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name',
            'last_name', 'email', 'password',
        ]
        id = serializers.IntegerField(read_only=True)
        password = serializers.CharField(write_only=True)
        password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        AuthorsRegisterValidator(
            validated_data, ErrorClass=serializers.ValidationError)
