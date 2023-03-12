from django.test import TestCase
from django.urls import reverse


CORRECT_LOGIN = {'username': 'Jsmith', 'password': 'y36xb9jggg',}
WRONG_PASS = {'username': 'Jsmith', 'password': 'BadPassword',}
WRONG_USERNAME = {'username': 'Johnsmith',
                  'password': 'y36xb9jggg' }
FULL_REGISTERED_USER = {'username': 'Jsmith',
                        'email': 'jsmith@mail.com',
                        'password1': 'y36xb9jggg',
                        'password2': 'y36xb9jggg'}

INVALID_LOGIN_MESSAGE = '<p id="messages">Username OR Password is incorrect</p>'


class LoginTests(TestCase):

    def create_user():
        import froggr.forms
        froggr.forms.UserForm(FULL_REGISTERED_USER).save()

    def check_incorrect(self, details={}):
        request = self.client.post(reverse('froggr:frog-in'), details)
        self.assertEqual(request.status_code, 200)
        content = request.content.decode('utf-8')
        self.assertTrue(INVALID_LOGIN_MESSAGE in content)

    def test_with_invalid_password(self):
        LoginTests.create_user()
        self.check_incorrect(WRONG_PASS)
        
    def test_with_invalid_username(self):
        LoginTests.create_user()
        self.check_incorrect(WRONG_USERNAME)

    def test_with_correct_data(self):
        LoginTests.create_user()
        request = self.client.post(reverse('froggr:frog-in'), CORRECT_LOGIN)
        self.assertRedirects(request, reverse('froggr:home'))

    def test_with_no_input(self):
        LoginTests.create_user()
        self.check_incorrect()

