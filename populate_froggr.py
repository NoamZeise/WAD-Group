import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'froggr_website.settings')

import django
django.setup()
from froggr.models import User, UserProfile, Connection, BlogPost, Comment, Reaction


def populate():
    gen_friends(
        gen_user("John Smith"),
        gen_user("EvaSmith"),
        gen_user("Jean12"))

    
def gen_user(name):
    u = User.objects.get_or_create(username=name,
                                   email=(name + "@mail.com"))[0]
    u.set_password(name + "@123")
    u.save()

    profile = UserProfile.objects.get_or_create(user=u)[0]
    profile.save()
    
    print("> Added User: " + u.username)
    return (u, profile)


def gen_friends(*users):
    for u1 in users:
        for u2 in users:
            if u1 == u2:
                continue
            c = Connection.objects.get_or_create(user=u1[0], friend=u2[0])[0]
            c.save()
            print("> Added connection: " + u1[0].username +
                  " -> "                 + u2[0].username)
            

if __name__ == '__main__':
    print("Stating Population Script...")
    populate()
    print("Population Script Complete!")
