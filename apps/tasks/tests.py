from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Project, Task
from .forms import TaskForm


class TaskFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.project = Project.objects.create(owner=self.user, title='Test Project')

    def test_task_form_valid_data(self):
        future_date = timezone.now().date() + timedelta(days=7)
        form = TaskForm(data={
            'title': 'New Task',
            'description': 'Task description',
            'due_date': future_date,
            'priority': 'high',
            'status': 'todo',
            'project': self.project.id,
        })
        self.assertTrue(form.is_valid(), form.errors.as_json())

    def test_task_form_due_date_in_past(self):
        past_date = timezone.now().date() - timedelta(days=1)
        form = TaskForm(data={
            'title': 'Past Due Task',
            'description': 'Task description',
            'due_date': past_date,
            'priority': 'medium',
            'status': 'todo',
            'project': self.project.id,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)
        self.assertEqual(form.errors['due_date'], ["Due date cannot be in the past."])

    def test_task_form_empty_due_date(self):
        form = TaskForm(data={
            'title': 'No Due Date Task',
            'description': 'Task description',
            'priority': 'low',
            'status': 'todo',
            'project': self.project.id,
        })
        self.assertTrue(form.is_valid(), form.errors.as_json())

    def test_task_form_priority_normalization(self):
        form = TaskForm(data={
            'title': 'Priority Test',
            'description': 'Task description',
            'due_date': timezone.now().date() + timedelta(days=1),
            'priority': 'HIGH',
            'status': 'todo',
            'project': self.project.id,
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['priority'], 'high')

    def test_task_form_missing_required_fields(self):
        form = TaskForm(data={
            'description': 'Missing title',
            'due_date': timezone.now().date() + timedelta(days=1),
            'priority': 'medium',
            'status': 'todo',
            'project': self.project.id,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)