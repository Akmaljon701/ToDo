from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from task.serializers import TaskCreateSerializer, TaskUpdateSerializer, TaskGetSerializer
from utils.responses import response_schema

create_task_schema = extend_schema(
    summary="create task",
    request=TaskCreateSerializer,
    responses=response_schema
)

update_task_schema = extend_schema(
    summary="update task",
    request=TaskUpdateSerializer,
    responses=response_schema,
    parameters=[
        OpenApiParameter(name='pk', description='Task ID', required=True, type=OpenApiTypes.INT),
    ]
)

get_tasks_schema = extend_schema(
    summary="get tasks",
    request=None,
    responses=TaskGetSerializer(many=True),
    parameters=[
        OpenApiParameter(name='search', description='by title or description', required=False, type=OpenApiTypes.STR),
        OpenApiParameter(name='status', description='Task Status', required=False, type=OpenApiTypes.STR,
                         enum=['not_completed', 'completed']),
    ],
)

get_task_schema = extend_schema(
    summary="get task",
    request=None,
    responses=TaskGetSerializer,
    parameters=[
        OpenApiParameter(name='pk', description='Task ID', required=True, type=OpenApiTypes.INT),
    ]
)

delete_task_schema = extend_schema(
    summary="delete task",
    request=None,
    responses=None,
    parameters=[
        OpenApiParameter(name='pk', description='Task ID', required=True, type=OpenApiTypes.INT),
    ]
)
