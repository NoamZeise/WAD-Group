from django.test import TestCase
from django.urls import reverse
from django.contrib import messages


CORRECT_LOGIN = {'username': 'Jsmith', 'password': 'y36xb9jggg',}
WRONG_PASS = {'username': 'Jsmith', 'password': 'BadPassword',}
WRONG_USERNAME = {'username': 'Johnsmith',
                  'password': 'y36xb9jggg' }
FULL_REGISTERED_USER = {'username': 'Jsmith',
                        'email': 'jsmith@mail.com',
                        'password1': 'y36xb9jggg',
                        'password2': 'y36xb9jggg'}


class LoginTests(TestCase):

    def create_user():
        import froggr.forms
        froggr.forms.UserForm(FULL_REGISTERED_USER).save()

    def test_with_invalid_password(self):
        LoginTests.create_user()
        response = self.client.post(reverse('froggr:frog-in'), WRONG_PASS)
        content = response.content.decode('utf-8')
        self.assertTrue('<p id="messages">Username OR Password is incorrect</p>' in content)
        
    def test_with_invalid_username(self):
        LoginTests.create_user()
        response = self.client.post(reverse('froggr:frog-in'), WRONG_USERNAME)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertTrue('<p id="messages">Username OR Password is incorrect</p>' in content)

    def test_with_correct_data(self):
        LoginTests.create_user()
        response = self.client.post(reverse('froggr:frog-in'), CORRECT_LOGIN)
        self.assertRedirects(response, reverse('froggr:home'))
