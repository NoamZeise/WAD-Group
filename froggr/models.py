from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime
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
    date = models.DateField(default=DEFAULT_DATE)
    post_slug = models.SlugField(unique=True)
    text = models.TextField(default="My Frogg")
    image = models.ImageField(upload_to=post_dir_path, blank=True)
    score = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # make post url based on username and post title
        self.post_slug = slugify(self.user.username + '-' + self.title)
        print(self.post_slug)
        if self.date == DEFAULT_DATE.date():
            self.date = timezone.now()
        super(BlogPost, self).save(*args, **kwargs)

    class Meta:
        # pair (user, friend) is unique for this entity
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'title'],
                name="only 1 blog with a title per user")
        ]
        
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


class Reaction(models.Model):
    """ A reaction to a blogpost.
    Made by a user and can be positive or negative"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    # should be +1 or -1, so they can all be added together together
    # to get the 'score' of the page
    reaction = models.SmallIntegerField()
    
    class Meta:
        # user can only give one reaction to a post
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name="only 1 reaction per user, per post")
        ]

    def save(self, *args, **kwargs):
        self.post.score += self.reaction
        self.post.save()
        super(Reaction, self).save(*args, **kwargs)

    def delete(self):
        self.post.score -= self.reaction
        self.post.save()
        super(Reaction, self).delete()
        
    def __str__(self):
        return self.user.username + "->" + self.post.title + " : " + str(self.reaction)
