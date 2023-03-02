from django.test import TestCase
from django.urls import reverse
from froggr.forms import *
from froggr.models import *
from froggr.views import *
import os


class TemplateTests:

    ## test each template exist

    def test_base_exists(self):
        base_template_exists = os.path.isfile(os.path.join(self.froggr_templates_dir, 'base.html'))
        self.assertTrue(base_template_exists, "The base.html template is missing from the templates directory.")

    def test_first_page_exists(self):
        first_page_template_exists = os.path.isfile(os.path.join(self.froggr_templates_dir, 'first_page.html'))
        self.assertTrue(first_page_template_exists,
                        "The first_page.html template is missing from the templates directory.")

    def test_profile_exists(self):
        profile_template_exists = os.path.isfile(os.path.join(self.froggr_templates_dir, 'profile.html'))
        self.assertTrue(profile_template_exists, "The profile.html template is missing from the templates directory.")

    def test_home_exists(self):
        home_template_exists = os.path.isfile(os.path.join(self.froggr_templates_dir, 'home.html'))
        self.assertTrue(home_template_exists, "The home.html template is missing from the templates directory.")

    def test_login_exists(self):
        login_template_exists = os.path.isfile(os.path.join(self.froggr_templates_dir, 'login.html'))
        self.assertTrue(login_template_exists, "The login.html template is missing from the templates directory.")

    def test_logout_exists(self):
        logout_template_exists = os.path.isfile(os.path.join(self.froggr_templates_dir, 'logout.html'))
        self.assertTrue(logout_template_exists, "The logout.html template is missing from the templates directory.")

    def test_register_exists(self):
        register_template_exists = os.path.isfile(os.path.join(self.froggr_templates_dir, 'register.html'))
        self.assertTrue(register_template_exists, "The register.html template is missing from the templates directory.")

    def test_search_exists(self):
        search_template_exists = os.path.isfile(os.path.join(self.froggr_templates_dir, 'search.html'))
        self.assertTrue(search_template_exists, "The search.html template is missing from the templates directory.")

    def test_upload_exists(self):
        upload_template_exists = os.path.isfile(os.path.join(self.imagenest_templates_dir, 'upload.html'))
        self.assertTrue(upload_template_exists, "The upload.html template is missing from the templates directory.")

    ## test each template maps to the correct view

    def test_home_uses_template(self):
        response = self.client.get(reverse('froggr:home'))
        self.assertTemplateUsed(response, 'froggr/home.html',
                                "The home.html template is not used for the home() view}")

    def test_login_uses_template(self):
        response = self.client.get(reverse('froggr:login'))
        self.assertTemplateUsed(response, 'froggr/login.html',
                                "The login.html template is not used for the login() view}")

    def test_logout_uses_template(self):
        response = self.client.get(reverse('froggr:logout'))
        self.assertTemplateUsed(response, 'froggr/logout.html',
                                "The logout.html template is not used for the logout() view}")

    def test_profile_uses_template(self):
        response = self.client.get(reverse('froggr:profile'))
        self.assertTemplateUsed(response, 'froggr/profile.html',
                                "The profile.html template is not used for the profile() view}")

    def test_register_uses_template(self):
        response = self.client.get(reverse('froggr:register'))
        self.assertTemplateUsed(response, 'froggr/register.html',
                                "The register.html template is not used for the register() view}")

    def test_search_uses_template(self):
        response = self.client.get(reverse('froggr:search'))
        self.assertTemplateUsed(response, 'froggr/search.html',
                                "The search.html template is not used for the search() view}")

    def test_top_frogs_uses_template(self):
        response = self.client.get(reverse('froggr:top_images'))
        self.assertTemplateUsed(response, 'froggr/top_images.html',
                                "The top_images.html template is not used for the top_frogs() view}")

    def test_upload_uses_template(self):
        response = self.client.get(reverse('froggr:add_frog'))
        self.assertTemplateUsed(response, 'froggr/upload.html',
                                "The upload.html template is not used for the add_frog() view}")