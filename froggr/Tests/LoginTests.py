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


class LoginTests(TestCase):

    def create_user():
        import froggr.forms
        froggr.forms.UserForm(FULL_REGISTERED_USER).save()

    def check_incorrect(self, error_msg, details={}):
        request = self.client.post(reverse('froggr:frog-in'), details)
        self.assertEqual(request.status_code, 200)
        content = request.content.decode('utf-8')
        self.assertTrue(error_msg in content)

    def test_with_invalid_password(self):
        LoginTests.create_user()
        self.check_incorrect("Password was incorrect", WRONG_PASS)
        
    def test_with_invalid_username(self):
        LoginTests.create_user()
        self.check_incorrect("Username does not exist", WRONG_USERNAME)

    def test_with_correct_data(self):
        LoginTests.create_user()
        request = self.client.post(reverse('froggr:frog-in'), CORRECT_LOGIN)
        self.assertRedirects(request, reverse('froggr:home'))

    def test_with_no_input(self):
        LoginTests.create_user()
        self.check_incorrect("Username does not exist")

