from django.test import TestCase
from django.urls import reverse
# import froggr.forms
# import froggr.models
# import froggr.views

REGISTERED_USER = {'username': 'Jsmith', 'password': 'y36xb9j',}
UNREGISTERED_USER = {'username': 'Kate', 'password': '7g3ma7sge',}
FULL_REGISTERED_USER = {'firstname': 'John',
                        'surname': 'Smith',
                        'username': 'Jsmith',
                        'password': 'y36xb9j',
                        'confirm_password': 'y36xb9j'}


class LoginTests(TestCase):


    def test_login_form_exists(self):
        import froggr.forms
        self.assertTrue('LoginForm' in dir(froggr.forms), "The LoginForm class could not be found in forms.py")

    def test_with_invalid_username(self):
        response = self.client.post(reverse(login), UNREGISTERED_USER)
        self.assertEqual(response.status_code, 200)

        self.assertEquals(response.context["error"], "Username not recognised. Please try again.")
        self.assertContains(response, "Username not recognised. Please try again.")

    def test_with_invalid_password(self):
        create_user()
        REGISTERED_USER["password"] = "InvalidPassword"
        response = self.client.post(reverse(login), REGISTERED_USER)
        self.assertEqual(response.status_code, 200)

        error = response.context["error"]
        self.assertEquals(error, "Password is incorrect. Please try again.")
        self.assertContains(response, "Password is incorrect. Please try again.")

    def test_with_correct_data(self):
        create_user()
        response = self.client.post(reverse(login), REGISTERED_USER)
        self.assertRedirects(response, reverse(home))

def create_user():
    register_form = RegisterForm(FULL_REGISTERED_USER)
    user = register_form.save(commit=False)
    user.set_password("y36xb9j")
    user.save()