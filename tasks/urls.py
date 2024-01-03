from django.urls import path
from .views import TaskListCreateView, TaskDetailView, TaskDataProcessView

urlpatterns = [
    path("", TaskListCreateView.as_view(), name='task_list'),
    path("<int:pk>/", TaskDetailView.as_view(), name='task_detail'),
    path('process/', TaskDataProcessView.as_view(), name='task_process'),
]
