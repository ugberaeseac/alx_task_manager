from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib import messages

from ..models import Task, Project
from ..forms import TaskForm, ProjectForm
from .ai_parser import parse_task_text


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().filter(owner=self.request.user)

        # Filtering
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        project_id = self.request.GET.get('project')

        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if project_id:
            queryset = queryset.filter(project__id=project_id)

        # Searching
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', '')
        context['current_priority'] = self.request.GET.get('priority', '')
        context['current_project'] = self.request.GET.get('project', '')
        context['search_query'] = self.request.GET.get('q', '')
        context['projects'] = Project.objects.filter(owner=self.request.user)
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks:task_list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task_list')

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


def parse_create_task(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            parsed_data = parse_task_text(text)
            form = TaskForm(parsed_data)
            if form.is_valid():
                task = form.save(commit=False)
                task.owner = request.user
                task.save()
                messages.success(request, "Task added successfully!")
            else:
                # If form is not valid, display errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        else:
            messages.error(request, "Task text cannot be empty.")
    return redirect('tasks:task_list')


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'tasks/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10  # Projects per page

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user).order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # For each project, get its tasks and apply filters/search
        for project in context['projects']:
            tasks_queryset = project.task_set.filter(owner=self.request.user)

            status = self.request.GET.get('status')
            priority = self.request.GET.get('priority')
            search_query = self.request.GET.get('q')

            if status:
                tasks_queryset = tasks_queryset.filter(status=status)
            if priority:
                tasks_queryset = tasks_queryset.filter(priority=priority)
            if search_query:
                tasks_queryset = tasks_queryset.filter(
                    Q(title__icontains=search_query) | Q(description__icontains=search_query)
                )
            project.tasks = tasks_queryset.order_by('-created_at')

        context['current_status'] = self.request.GET.get('status', '')
        context['current_priority'] = self.request.GET.get('priority', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'tasks/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        tasks_queryset = project.task_set.filter(owner=self.request.user)

        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        search_query = self.request.GET.get('q')

        if status:
            tasks_queryset = tasks_queryset.filter(status=status)
        if priority:
            tasks_queryset = tasks_queryset.filter(priority=priority)
        if search_query:
            tasks_queryset = tasks_queryset.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )
        context['tasks'] = tasks_queryset.order_by('-created_at')

        context['current_status'] = self.request.GET.get('status', '')
        context['current_priority'] = self.request.GET.get('priority', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context