import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'froggr_website.settings')
import datetime
import django
django.setup()
from django.core.files import File
from froggr.models import User, UserProfile, Connection, BlogPost, Comment, Reaction
from froggr_website import settings

def populate():
    users = [gen_user("John Smith"),
             gen_user("Eva_Smith"),
             gen_user("Jean12"),
             gen_user("BadRoyRog"),]
    gen_friends(users[0:3])

    blogs = [gen_blog(users[0], "My fav frog",
                      "My favorite is the brazillia greenback.",
                      "example-posts/Frog.webp",
                      datetime.datetime(2020, 5, 6)),
             gen_blog(users[2], "Best Burger",
                      "Had a good burger at the burger shack.",
                      "example-posts/Burger.webp",
                      datetime.datetime(2021, 1, 5)),
             gen_blog(users[2], "Next Best Burger",
                      "Burger at the burger palace was almost as good!",
                      None,
                      datetime.datetime(2021, 2, 6)),
             gen_blog(users[3], "Chicken Tutorial",
                      "This chapter is designed to get you"
                      + " started with CHICKEN programming",
                      "example-posts/ChickenScheme.png", None),
             gen_blog(users[3], "Common Lisp Tutorial",
                      "Common Lisp is a general-purpose, multi-paradigm programming language suited for a wide variety of industry applications. It is frequently referred to as a programmable programming language.",
                      "example-posts/common-lisp.png", None),
             ]
    
    gen_comment(users[0], blogs[1], "a Burger!")
    gen_comment(users[3], blogs[3], "This is my post.")
    gen_comment(users[2], blogs[0], "I prefer the pirenian riceleg!!! :(")
    gen_reaction(users[0], blogs[1], 1)
    gen_reaction(users[0], blogs[3], -1)
    gen_reaction(users[3], blogs[2], -1)
    gen_reaction(users[1], blogs[1], 1)

    # make loads of blogs for testing
    user = gen_user("TestUser")
    for i in range(300):
        gen_blog(user, "Test Post " + str(i),
                 "TEST TEXT.",
                 None,
                 datetime.datetime(2000, 1, 1))
    
 
def gen_user(name):
    u = User.objects.get_or_create(username=name,
                                   email=(name + "@mail.com"))[0]
    u.set_password(name + "@123")
    u.save()

    profile = UserProfile.objects.get_or_create(
        user=u)[0]
    profile.text = f"I'm {name} and this is my profile!"
    profile.save()
  
    print("> Added User: " + u.username)
    return u


def gen_friends(users):
    for u1 in users:
        for u2 in users:
            if u1 == u2:
                continue
            c = Connection.objects.get_or_create(user=u1, friend=u2)[0]
            c.save()
            print("> Added Connection: " + u1.username +
                  " -> "                 + u2.username)

           
def gen_blog(user, title, text, image=None, date=None):
    p = BlogPost.objects.get_or_create(user=user, title=title, text=text)[0]
    if image != None:
        p.image.save(os.path.basename(image),
                     File(open(image, 'rb')))
    if date != None:
        p.date = date.date()
    p.save()
    print(f"> Added Post by {user.username} -- title: \"{title}\"")
    return p


def gen_comment(user, blog, text):
    c = Comment.objects.get_or_create(user=user, post=blog, text=text)[0]
    c.save()
    print(f"> Added Comment by {user.username}" +
          f" on Blog \"{blog.title}\" by {blog.user.username}")
    return c


def gen_reaction(user, blog, value):
    r = Reaction.objects.get_or_create(user=user, post=blog, reaction=value)[0]
    r.save()
    print(f"> Added Reaction '{value}' by {user.username} on post " +
          f"\"{blog.title}\"")
    return r


if __name__ == '__main__':
    print("Stating Population Script...")
    populate()
    print("Population Script Complete!")
