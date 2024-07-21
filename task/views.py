from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from task.models import Task
from task.schemas import create_task_schema, update_task_schema, get_tasks_schema, get_task_schema
from task.serializers import TaskCreateSerializer, TaskUpdateSerializer, TaskGetSerializer
from utils.pagination import paginate
from utils.responses import success


@create_task_schema
@api_view(['POST'])
def create_task(request):
    serializer = TaskCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user)
    return success


@update_task_schema
@api_view(['PUT'])
def update_task(request):
    pk = request.query_params.get('pk')
    task = get_object_or_404(Task, id=pk, user=request.user)
    serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success


@get_tasks_schema
@api_view(['GET'])
def get_tasks(request):
    search = request.query_params.get('search')
    status = request.query_params.get('status')
    tasks = Task.objects.filter(user=request.user).order_by('end_date')
    if search:
        tasks = tasks.filter(Q(title__icontains=search) | Q(description__icontains=search))
    if status == 'completed':
        tasks = tasks.filter(completed=True)
    elif status == 'not_completed':
        tasks = tasks.filter(completed=False)
    return paginate(tasks, TaskGetSerializer, request)


@get_task_schema
@api_view(['GET'])
def get_task(request):
    pk = request.query_params.get('pk')
    task = get_object_or_404(Task, id=pk)
    serializer = TaskGetSerializer(task)
    return Response(serializer.data, 200)


@get_task_schema
@api_view(['DELETE'])
def delete_task(request):
    pk = request.query_params.get('pk')
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.delete()
    return success

