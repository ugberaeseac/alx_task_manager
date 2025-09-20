from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserRegistrationTest(TestCase):
    def test_registration_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_successful_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password': 'password123',
            'password2': 'password123',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Registration successful. You can now log in.')
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_registration_with_mismatched_passwords(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser2',
            'password': 'password123',
            'password2': 'differentpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', 'The two password fields didn't match.')
        self.assertFalse(User.objects.filter(username='testuser2').exists())

    def test_registration_with_existing_username(self):
        User.objects.create_user(username='existinguser', password='password123')
        response = self.client.post(reverse('register'), {
            'username': 'existinguser',
            'password': 'password123',
            'password2': 'password123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')


class UserLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_successful_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have successfully logged in.')
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_login_with_non_existent_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'nonexistentuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
        self.assertFalse(response.context['user'].is_authenticated)