from django.contrib import admin
from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description')
    ordering = ('title',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'due_date', 'priority', 'project')
    list_filter = ('status', 'priority', 'due_date', 'project')
    search_fields = ('title', 'description', 'owner__username', 'project__title')
    ordering = ('due_date', 'priority')