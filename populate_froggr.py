import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'froggr_website.settings')

import django
django.setup()
from froggr.models import User, UserProfile, Connection, BlogPost, Comment, Reaction

def populate():
    gen_user("John Smith")
    gen_user("EvaSmith")
    gen_user("Jean12")

def gen_user(name):
    u = User.objects.get_or_create(username=name,
                                   email=(name + "@mail.com"))[0]
    u.set_password(name + "@123")
    u.save()

    profile = UserProfile.objects.get_or_create(user=u)[0]
    profile.save()
    
    print("> Added User: " + u.username)
    return (u, profile)

if __name__ == '__main__':
    print("Stating Population Script...")
    populate()
    print("Population Script Complete!")
