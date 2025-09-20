from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<uuid:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<uuid:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<uuid:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<uuid:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
]