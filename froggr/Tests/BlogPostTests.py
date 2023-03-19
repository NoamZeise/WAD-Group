from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from froggr.models import BlogPost
from froggr.forms import BlogPostForm
from django.template.defaultfilters import slugify

class BlogPostTest(TestCase):
    def create_user():
        return User.objects.create(username="John",
                           email="john@mail.com",
                           password="mypass")

    def test_make_blog_post_redirects_to_post(self):
        user = BlogPostTest.create_user()
        self.client.force_login(user)
        response = self.client.post(reverse('froggr:create-frogg'),
                                    {'user' : user, 'title': 'my post', 'text' : 'my post'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('froggr:posts') +
                             slugify(user.username) + '-' + slugify('my post') + '/')
