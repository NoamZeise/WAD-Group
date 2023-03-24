import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'froggr_website.settings')
import datetime
import django
django.setup()
from django.core.files import File
from froggr.models import User, UserProfile, Connection, BlogPost, Comment
from froggr_website import settings

def populate():
    users = [gen_user("John Smith"),
             gen_user("Eva_Smith"),
             gen_user("Jean12"),
             gen_user("BadRoyRog"),
             gen_user("Jack Bean"),
             gen_user("Elyssia-1"),]
    gen_friends(users[0:3])

    blogs = [gen_blog_from_txt(users[0], "example-posts/fav-frog.txt"),
             gen_blog(users[2], "Best Burger",
                      "Had a good burger at the burger shack.",
                      "example-posts/Burger.webp",
                      datetime.datetime(2021, 1, 5)),
             gen_blog(users[2], "Next Best Burger",
                      "Burger at the burger palace was almost as good!",
                      None,
                      datetime.datetime(2021, 2, 6)),
             gen_blog_from_txt(users[3], "example-posts/chicken-tut.txt"),
             gen_blog_from_txt(users[3], "example-posts/cl-post.txt"),
             gen_blog_from_txt(users[4], "example-posts/surprise-proof.txt"),
             gen_blog_from_txt(users[5], "example-posts/emacs-lisp.txt"),
             gen_blog_from_txt(users[5], "example-posts/gnu-prop.txt"),
             gen_blog_from_txt(users[5], "example-posts/free-as-in.txt"),
             gen_blog_from_txt(users[2], "example-posts/chickencopy.txt"),
             ]
    
    gen_comment(users[0], blogs[1], "a Burger!")
    gen_comment(users[0], blogs[1], "I want one of those Burgers!")
    gen_comment(users[2], blogs[1], "It was very tasty")
    gen_comment(users[3], blogs[3], "This is my post.")
    gen_comment(users[2], blogs[0], "I prefer the pirenian riceleg!!! :(")
    gen_comment(users[3], blogs[6], "Chicken Sandwitch")
    gen_comment(users[3], blogs[6], "Salt and Pepper")
    gen_comment(users[0], blogs[4], "Common")
    gen_comment(users[1], blogs[8], "BWOAWOEOAWDOWADOO")
    gen_reaction(users[0], blogs[1])
    gen_reaction(users[0], blogs[3])
    gen_reaction(users[3], blogs[2])
    gen_reaction(users[1], blogs[1])
    gen_reaction(users[1], blogs[4])
    gen_reaction(users[0], blogs[5])
    gen_reaction(users[1], blogs[5])
    gen_reaction(users[1], blogs[6])
    gen_reaction(users[0], blogs[8])

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


def gen_blog_from_txt(user, filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        title = f.readline().strip()
        date = f.readline().strip().split('-')
        image = f.readline().strip()
        text = f.read()
        return gen_blog(user, title, text, image,
                        datetime.datetime(int(date[0]), int(date[1]), int(date[2])))


def gen_comment(user, blog, text):
    c = Comment.objects.get_or_create(user=user, post=blog, text=text)[0]
    c.save()
    print(f"> Added Comment by {user.username}" +
          f" on Blog \"{blog.title}\" by {blog.user.username}")
    return c


def gen_reaction(user, blog):
    blog.toggle_like(user)
    print(f"> Added like by {user.username} on post " +
          f"\"{blog.title}\"")


if __name__ == '__main__':
    print("Stating Population Script...")
    populate()
    print("Population Script Complete!")
