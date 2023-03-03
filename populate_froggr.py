import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'froggr_website.settings')

import django
django.setup()
from froggr.models import User, UserProfile, Connection, BlogPost, Comment, Reaction

def populate():
    users = [gen_user("John Smith"),
             gen_user("Eva_Smith"),
             gen_user("Jean12"),
             gen_user("BadRoyRog"),]
    gen_friends(users[0:3])

    blogs = [gen_blog(users[0], "My fav frog",
                      "My favorite is the brazillia greenback."),
             gen_blog(users[2], "Best Burger",
                      "Had a good burger at the burger shack."),
             gen_blog(users[2], "Next Best Burger",
                      "Burger at the burger palace was almost as good!"),
             gen_blog(users[3], "Chicken Tutorial",
                      "This chapter is designed to get you"
                      + "started with CHICKEN programming"),]
    
    gen_comment(users[0], blogs[1], "a Burger!")
    gen_comment(users[3], blogs[3], "This is my post.")
    gen_comment(users[2], blogs[0], "I prefer the pirenian riceleg!!! :(")
    gen_reaction(users[0], blogs[1], 1)
    gen_reaction(users[0], blogs[3], -1)
    gen_reaction(users[3], blogs[2], -1)
    gen_reaction(users[1], blogs[1], 1)
    
 
def gen_user(name):
    u = User.objects.get_or_create(username=name,
                                   email=(name + "@mail.com"))[0]
    u.set_password(name + "@123")
    u.save()

    profile = UserProfile.objects.get_or_create(
        user=u,
        text=f"I'm {name} and this is my profile!")[0]
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

           
def gen_blog(user, title, text):
    p = BlogPost.objects.get_or_create(user=user, title=title, text=text)[0]
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
