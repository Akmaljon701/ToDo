from django.db import models
from user.models import CustomUser


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    end_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, related_name='user_tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
