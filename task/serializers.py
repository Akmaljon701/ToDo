from rest_framework.serializers import ModelSerializer
from task.models import Task


class TaskCreateSerializer(ModelSerializer):

    class Meta:
        model = Task
        exclude = ('completed', 'user')


class TaskUpdateSerializer(ModelSerializer):

    class Meta:
        model = Task
        exclude = ('user',)


class TaskGetSerializer(ModelSerializer):

    class Meta:
        model = Task
        exclude = ('user',)
