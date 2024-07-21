from drf_spectacular.utils import extend_schema
from user.serializers import CustomUserSerializer, CustomTokenObtainPairSerializer, CustomUserGetSerializer
from utils.responses import response_schema

login_user_schema = extend_schema(
    summary="login user",
    request=CustomTokenObtainPairSerializer,
    responses={
        200: {"description": "The operation was completed successfully",
              "example": {
                  'refresh': 'refresh_token',
                  'access': 'access_token',
                  'user': {
                      'id': 0,
                      'full_name': 'full_name',
                      'username': 'username',
                  }}
              },
    }
)

create_user_schema = extend_schema(
    summary="create user",
    request=CustomUserSerializer,
    responses={
        200: {"description": "The operation was completed successfully",
              "example": {
                  'refresh': 'refresh_token',
                  'access': 'access_token',
                  'user': {
                      'id': 0,
                      'full_name': 'full_name',
                      'username': 'username',
                  }}
              },
    }
)

update_user_schema = extend_schema(
    summary="update current user",
    request=CustomUserSerializer,
    responses=response_schema
)

get_current_user_schema = extend_schema(
    summary="get current user",
    responses=CustomUserGetSerializer
)
