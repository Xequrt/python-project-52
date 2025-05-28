from django.urls import path
from .views import TasksListView, TasksCreateView, TasksUpdateView, TasksDeleteView

urlpatterns = [
    path('', TasksListView.as_view(), name='tasks_list'),
    path('create/', TasksCreateView.as_view(), name='tasks_create'),
    path('<int:pk>/update/', TasksUpdateView.as_view(), name='tasks_update'),
    path('<int:pk>/delete/', TasksDeleteView.as_view(), name='tasks_delete'),
]