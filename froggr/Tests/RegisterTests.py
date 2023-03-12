from unittest import TestResult
from django.test import TestCase
from django.urls import reverse
from froggr import forms, models, views


class RegisterTests(TestCase):
    def setUp(self):
        self.testUser = {'username': 'Jsmith',
                         'email': 'jsmith@mail.com',
                         'password1': 'y36xb9jggg',
                         'password2': 'y36xb9jggg'}
    
    def test_register_form_exists(self):
        import froggr.forms
        self.assertTrue('UserForm' in dir(froggr.forms),
                        "The UserForm class could not be found in forms.py")

    def form_displays_on_template(self):
        response = self.client.post(reverse('froggr:register'))
        self.assertContains(response.context, "search_form")

    def test_firstname_contains_non_letter(self):
        self.testUser["firstname"] = "John1"
        response = self.client.post(reverse('froggr:register'), self.testUser)
        self.assertEqual(response.status_code, 302)

        self.assertEquals(response.context["error"], "Firstname must contain only alphabetical characters.")
        self.assertContains(response, "Firstname must contain only alphabetical characters.")

        self.testUser["firstname"] = "John"

    def test_surname_contains_non_letter(self):
        self.testUser["surname"] = "Smith1"
        response = self.client.post(reverse('froggr:register'), self.testUser)
        self.assertEqual(response.status_code, 200)

        self.assertEquals(response.context["error"], "Surname must contain only alphabetical characters.")
        self.assertContains(response, "Surname must contain only alphabetical characters.")

        self.testUser["surname"] = "Smith"

    def test_username_contains_space(self):
        self.testUser["username"] = "J smith"
        response = self.client.post(reverse('froggr:register'), self.testUser)
        self.assertEqual(response.status_code, 200)

        self.assertEquals(response.context["error"],
                          "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.")
        self.assertContains(response,
                            "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.")

        self.testUser["username"] = "Jsmith"

    def test_username_less_than_six_chars(self):
        self.testUser["username"] = "John"
        response = self.client.post(reverse('froggr:register'), self.testUser)
        self.assertEqual(response.status_code, 200)

        self.assertEquals(response.context["error"], "Username must be at least 6 characters long. Please try again.")
        self.assertContains(response, "Username must be at least 6 characters long. Please try again.")

        self.testUser["username"] = "Jsmith"

    def test_password_different_to_confirm_password(self):
        self.testUser["confirm_password"] = "DifferentPassword"
        response = self.client.post(reverse('froggr:register'), self.testUser)
        #self.assertEqual(response.status_code, 200)
   
        content = response.content.decode("utf-8")
        print(content)
        self.assertContains(content, "Passwords do not match. Please try again.")

        self.testUser["confirm_password"] = "y36xb9j"

    def test_register_success(self):
        response = self.client.post(reverse('froggr:register'), self.testUser)
        self.assertRedirects(response, reverse('froggr:frog-in'))

