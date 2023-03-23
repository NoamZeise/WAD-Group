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

    def test_simple_password(self):
        self.testUser["password1"] = "pass"
        self.testUser["password2"] = "pass"
        response = self.client.post(reverse('froggr:register'), self.testUser)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertTrue("This password is too short. It must contain at least 8 characters." in content)
        self.assertTrue("This password is too common." in content)

    def test_password_different_to_confirm_password(self):
        self.testUser["password2"] = "DifferentPassword"
        self.assertTrue(self.testUser['password1'] != self.testUser['password2'])
        response = self.client.post(reverse('froggr:register'), self.testUser)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertTrue("The two password fields didn’t match." in content)

    def test_register_success(self):
        response = self.client.post(reverse('froggr:register'), self.testUser)
        self.assertRedirects(response, reverse('froggr:home'))

