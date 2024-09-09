from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import redis

# Redis client initialization
redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)


class Redis:
    @staticmethod
    def save(key, value, expire_time):
        """Saves a value in Redis with an expiration time."""
        try:
            return redis_client.setex(key, expire_time, value)
        except redis.RedisError as e:
            print(f"Redis save error: {e}")
            return False

    @staticmethod
    def get(key):
        """Gets a value from Redis by key."""
        try:
            return redis_client.get(key)
        except redis.RedisError as e:
            print(f"Redis get error: {e}")
            return None


@extend_schema(
    request=None,  # No full schema for request body, but parameters are included
    parameters=[
        OpenApiParameter(name='key', type=str, description='The key to be saved in Redis', required=True),
        OpenApiParameter(name='value', type=str, description='The value to be saved in Redis', required=True),
        OpenApiParameter(name='expire_time', type=int, description='The expiration time for the key in seconds', required=False, default=3600),
    ],
    responses={
        200: OpenApiResponse(
            description='Data saved and verified successfully',
            response={
                'application/json': {
                    'type': 'object',
                    'properties': {
                        'detail': {'type': 'string'},
                        'saved_value': {'type': 'string'}
                    }
                }
            }
        ),
        400: OpenApiResponse(
            description='Bad Request - Missing key or value',
            response={
                'application/json': {
                    'type': 'object',
                    'properties': {
                        'detail': {'type': 'string'}
                    }
                }
            }
        ),
        500: OpenApiResponse(
            description='Internal Server Error - Failed to save or verify data',
            response={
                'application/json': {
                    'type': 'object',
                    'properties': {
                        'detail': {'type': 'string'}
                    }
                }
            }
        )
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def save_and_check(request):
    """API view to save data in Redis and check the stored value."""
    key = request.query_params.get('key')
    value = request.query_params.get('value')
    expire_time = request.query_params.get('expire_time', 3600)  # default to 3600 seconds (1 hour)

    # Save data in Redis
    if Redis.save(key, value, expire_time):
        # Retrieve the saved value to confirm it was stored correctly
        saved_value = Redis.get(key)

        if saved_value == value:
            return Response({'detail': 'Data saved and verified', 'saved_value': saved_value}, 200)
        else:
            return Response({'detail': 'Data saved but verification failed'}, 500)
    else:
        return Response({'detail': 'Failed to save data'}, 500)
