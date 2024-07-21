from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user.models import CustomUser


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        ser = CustomUserGetSerializer(self.user)

        data.update({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': ser.data,
        })

        return data


class CustomUserGetSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'username')


class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'username', 'password')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        instance = super().update(instance, validated_data)
        return instance
