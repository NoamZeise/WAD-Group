from unittest import TestResult
from django.test import TestCase
from django.urls import reverse
from froggr.forms import *
from froggr.models import *
from froggr.views import *

TEST_USER = {'firstname': 'John',
             'surname': 'Smith',
             'username': 'Jsmith',
             'password': 'y36xb9j',
             'confirm_password': 'y36xb9j'}


class RegisterTests(TestCase):

    def test_register_form_exists(self):
        import froggr.forms
        self.assertTrue('RegisterForm' in dir(froggr.forms), "The RegisterForm class could not be found in forms.py")

    def form_displays_on_template(self):
        response = self.client.post(reverse(register))
        self.assertContains(response.context, "search_form")

    def test_firstname_contains_non_letter(self):
        TEST_USER["firstname"] = "John1"
        response = self.client.post(reverse(register), TEST_USER)
        self.assertEqual(response.status_code, 200)

        self.assertEquals(response.context["error"], "Firstname must contain only alphabetical characters.")
        self.assertContains(response, "Firstname must contain only alphabetical characters.")

        TEST_USER["firstname"] = "John"

    def test_surname_contains_non_letter(self):
        TEST_USER["surname"] = "Smith1"
        response = self.client.post(reverse(register), TEST_USER)
        self.assertEqual(response.status_code, 200)

        self.assertEquals(response.context["error"], "Surname must contain only alphabetical characters.")
        self.assertContains(response, "Surname must contain only alphabetical characters.")

        TEST_USER["surname"] = "Smith"

    def test_username_contains_space(self):
        TEST_USER["username"] = "J smith"
        response = self.client.post(reverse(register), TEST_USER)
        self.assertEqual(response.status_code, 200)

        self.assertEquals(response.context["error"],
                          "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.")
        self.assertContains(response,
                            "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.")

        TEST_USER["username"] = "Jsmith"

    def test_username_less_than_six_chars(self):
        TEST_USER["username"] = "John"
        response = self.client.post(reverse(register), TEST_USER)
        self.assertEqual(response.status_code, 200)

        self.assertEquals(response.context["error"], "Username must be at least 6 characters long. Please try again.")
        self.assertContains(response, "Username must be at least 6 characters long. Please try again.")

        TEST_USER["username"] = "Jsmith"

    def test_password_different_to_confirm_password(self):
        TEST_USER["confirm_password"] = "DifferentPassword"
        response = self.client.post(reverse(register), TEST_USER)
        self.assertEqual(response.status_code, 200)

        self.assertEquals(response.context["error"], "Passwords do not match. Please try again.")
        self.assertContains(response, "Passwords do not match. Please try again.")

        TEST_USER["confirm_password"] = "y36xb9j"


    def test_register_success(self):
        # delete the user in case it already existed
        try:
            user = User.objects.get(username=TEST_USER['username'])
            user.delete()
        except User.DoesNotExist:
            pass

        response = self.client.post(reverse(register), TEST_USER)
        self.assertRedirects(response, reverse(login))

