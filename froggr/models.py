from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime

# Peter
from django.db.models import F

# Create your models here.


def user_dir_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


def post_dir_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class UserProfile(models.Model):
    """Represents a User of the website,
    with a profile page, connections, and posts"""
    
    # each user's username, email is unique
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # link to profile should be unique
    profile_slug = models.SlugField(unique=True)

    text = models.TextField(blank=True)
    image = models.ImageField(upload_to=user_dir_path, blank=True)

    def save(self, *args, **kwargs):
        # make user profile url based on username
        self.profile_slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def watchlist_create(sender, instance=None, created=False, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class Connection(models.Model):
    """A link between two users, to show up on each other's connections list,
    there will be two entries for a particular connection"""
    
    # delete the connection if any of the users are deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User")
    friend = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="Friend")

    class Meta:
        # pair (user, friend) is unique for this entity
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'friend'],
                name="only 1 connection to a particular friend")
        ]

    def save(self, *args, **kwargs):
        if self.user == self.friend:
            print("Didn't add Connection: Cannot be friends with yourself")
            return
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username + " -> " + self.friend.username

DEFAULT_DATE = datetime.datetime(1900, 1, 1)
    
class BlogPost(models.Model):
    """ A post on the website. User who posted, and link to page is stored. """

    # delete post if user is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    date = models.DateTimeField(default=DEFAULT_DATE)
    post_slug = models.SlugField(unique=True)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to=post_dir_path, blank=True)
    score = models.IntegerField(default=0)
    users_liked = models.ManyToManyField(User, blank=True, related_name='posts_liked')

    def toggle_like(self, user):
        if user in post.users_liked.all():
            post.score = post.score - 1
            post.users_liked.remove(user)
        else:
            post.score = post.score + 1
            post.users_liked.add(user)
        post.save()


    def save(self, *args, **kwargs):
        # make post url based on username and post title
        if len(self.title.strip()) == 0:
            raise ValueError()
        self.post_slug = slugify(self.user.username + '-' + self.title)
        # if time hasn't been set use current time (will be set for population data)
        if self.date.year == DEFAULT_DATE.date().year:
            self.date = timezone.now()
        super(BlogPost, self).save(*args, **kwargs)

    def sort_blogposts(queryset, field_name, order='ascending'):
        if order.lower() == 'ascending':
            return queryset.order_by(F(field_name).asc())
        elif order.lower() == 'descending':
            return queryset.order_by(F(field_name).desc())
        else:
            raise ValueError(f"Invalid order: {order}. Must be 'ascending' or 'descending'.")
        
    def __str__(self):
        return self.user.username + " -- " + self.title
        

class Comment(models.Model):
    """ A Comment is a text only response to a post made by a user """

    # delete comment if user is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # delete comment if post is deleted
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    #  use text field for comment so we can have more characters than charfield
    text = models.TextField()

    def __str__(self):
        return self.user.username + " -- " + self.post.title
