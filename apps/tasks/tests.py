from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch
from django.urls import reverse
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


class ParseCreateTaskTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.project = Project.objects.create(owner=self.user, title='Test Project')

    @patch('apps.tasks.ai_parser.parse_task_text')
    def test_parse_create_task_valid_data(self, mock_parse_task_text):
        mock_parse_task_text.return_value = {
            'title': 'Parsed Task',
            'description': 'Parsed description',
            'due_date': (timezone.now() + timedelta(days=1)).isoformat(),
            'priority': 'high',
            'project': self.project.id,
        }
        response = self.client.post(reverse('tasks:parse_create_task'), {'text': 'Buy groceries tomorrow high priority'})
        self.assertEqual(response.status_code, 302)  # Redirects to task list
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.title, 'Parsed Task')
        self.assertEqual(task.owner, self.user)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Task added successfully!")

    @patch('apps.tasks.ai_parser.parse_task_text')
    def test_parse_create_task_invalid_data(self, mock_parse_task_text):
        mock_parse_task_text.return_value = {
            'title': '',  # Invalid title
            'description': 'Parsed description',
            'due_date': (timezone.now() + timedelta(days=1)).isoformat(),
            'priority': 'high',
            'project': self.project.id,
        }
        response = self.client.post(reverse('tasks:parse_create_task'), {'text': 'Invalid task data'})
        self.assertEqual(response.status_code, 302)  # Still redirects
        self.assertEqual(Task.objects.count(), 0)  # No task created
        messages = list(response.wsgi_request._messages)
        self.assertGreater(len(messages), 0)
        self.assertIn("title: This field cannot be blank.", [str(m) for m in messages])

    def test_parse_create_task_empty_text_input(self):
        response = self.client.post(reverse('tasks:parse_create_task'), {'text': ''})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Task text cannot be empty.")