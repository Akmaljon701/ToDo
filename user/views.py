from django.db import transaction
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from user.schemas import create_user_schema, login_user_schema, update_user_schema, get_current_user_schema
from user.serializers import CustomUserSerializer, CustomUserGetSerializer, CustomTokenObtainPairSerializer
from utils.chack_auth import IPThrottle
from utils.responses import success


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @login_user_schema
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'error': str(e)}, 400)

        return Response(serializer.validated_data, 200)


@create_user_schema
@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([IPThrottle])
@transaction.atomic()
def create_user(request):
    serializer = CustomUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save(is_active=True)

    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    user_data = CustomUserGetSerializer(user).data

    return Response({
        'refresh': str(refresh),
        'access': str(access),
        'user': user_data
    })


@update_user_schema
@api_view(['PUT'])
def update_current_user(request):
    serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success


@get_current_user_schema
@api_view(['GET'])
def get_current_user(request):
    serializer = CustomUserGetSerializer(request.user)
    return Response(serializer.data, 200)
