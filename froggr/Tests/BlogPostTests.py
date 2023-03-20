from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from froggr.models import BlogPost
from froggr.forms import BlogPostForm
from django.template.defaultfilters import slugify

class BlogPostTest(TestCase):
    def setup(self):
        self.post_details = {'user' : None, 'title': 'my post', 'text' : 'my post'};
        
    def create_user():
        return User.objects.create(username="John",
                           email="john@mail.com",
                           password="mypass")

    def create_post(details):
        return BlogPost.objects.create(
            user=details['user'],
            text=details['text'],
            title=details['title'])

    def create_user_and_post(self):
        self.setup()
        user = BlogPostTest.create_user()
        self.client.force_login(user)
        self.post_details['user'] = user

    def test_make_blog_post_redirects_to_post(self):
        self.create_user_and_post()
        response = self.client.post(reverse('froggr:create-frogg'),
                                    self.post_details)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('froggr:posts') +
                             slugify(self.post_details['user'].username)
                             + '-' + slugify('my post') + '/')

    def get_post_response(self):
        response = self.client.post(reverse('froggr:create-frogg'),
                                    self.post_details)
        return response.content.decode('utf-8')

    def check_invalid_title(self):
        content = self.get_post_response()
        self.assertTrue("This title is invalid" in content)
        
    def test_make_blog_post_same_title(self):
        self.create_user_and_post()
        post1 = BlogPostTest.create_post(self.post_details)
        content = self.get_post_response()
        self.assertTrue("You already have a post with this title" in content)

    def test_make_blog_post_no_title(self):
        self.create_user_and_post()
        self.post_details['title'] = ""
        self.check_invalid_title()

    def test_make_blog_post_spaced_title(self):
        self.create_user_and_post()
        self.post_details['title'] = "   "
        self.check_invalid_title()
        
