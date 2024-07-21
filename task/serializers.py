from datetime import datetime
from rest_framework.serializers import ModelSerializer, ValidationError
from task.models import Task


class TaskCreateSerializer(ModelSerializer):

    class Meta:
        model = Task
        exclude = ('completed', 'user')

    def validate_end_date(self, value):
        if value <= datetime.now():
            raise ValidationError("End date must be greater than the current date and time!")
        return value


class TaskUpdateSerializer(ModelSerializer):

    class Meta:
        model = Task
        exclude = ('user',)


class TaskGetSerializer(ModelSerializer):

    class Meta:
        model = Task
        exclude = ('user',)
