from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.


class User(models.Model):
    """Represents a User of the website,
    with a profile page, connections, and posts"""
    
    # each user's username, email is unique
    username = models.CharField(max_length=25, unique=True)
    email = models.CharField(max_length=25, unique=True)
    # TODO: make more secure at some point
    password = models.CharField(max_length=25)
    # link to profile should be unique
    profile_slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        # make user profile url based on username
        self.profile_slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)

    def delete(self):
        # TODO add code to delete
        # user posts files and profile files from server
        
        super(User, self).delete()
    
    def __str__(self):
        return "User: username=" + self.username


class Connection(models.Model):
    """A link between two users, to show up on each other's connections list,
    there will be two entries for a particular connection"""
    
    # delete the connection if any of the users are deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User")
    friend = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="User_friend")

    class Meta:
        # pair (user, friend) is unique for this entity
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'friend'],
                name="only 1 connection to a particular friend")
        ]

    def __str__(self):
        return "Connection: user=" + self.user + "  friend=" + self.friend


class BlogPost(models.Model):
    """ A post on the website. User who posted, and link to page is stored. """

    # delete post if user is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    post_slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        # make post url based on username and post title
        self.post_slug = slugify(self.user.username + "-" + self.title)
        super(User, self).save(*args, **kwargs)
    
    def __str__(self):
        return "BlogPost: title=" + self.title + "  user=" + self.user
        

class Comment(models.Model):
    """ A Comment is a text only response to a post made by a user """

    # delete comment if user is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # delete comment if post is deleted
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    #  use text field for comment so we can have more characters than charfield
    content = models.TextField()

    def __str__(self):
        return "Comment:  user=" + self.user + " post=" + self.post


class Reaction(models.Model):
    """ A reaction to a blogpost.
    Made by a user and can be positive or negative"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    # should be +1 or -1, so they can all be added together together
    # to get the 'score' of the page
    reacton = models.SmallIntegerField()
    
    class Meta:
        # user can only give one reaction to a post
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name="only 1 reaction per user, per post")
        ]

    def __str__(self):
        return "Reaction: user=" + self.user + "   post=" + self.post
