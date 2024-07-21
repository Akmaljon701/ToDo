from django.urls import path
from task.views import create_task, update_task, get_tasks, get_task, delete_task

urlpatterns = [
    path('create/', create_task, name='create_task'),
    path('update/', update_task, name='update_task'),
    path('all/', get_tasks, name='get_tasks'),
    path('', get_task, name='get_task'),
    path('delete/', delete_task, name='delete_task'),
]
