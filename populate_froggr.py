import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'froggr_website.settings')

import django
django.setup()

from froggr.models import User, Connection, BlogPost, Comment, Reaction

def populate():
    gen_user("John Smith")
    gen_user("EvaSmith")
    gen_user("Jean12")

def gen_user(name):
    u = User.objects.get_or_create(username=name,
                                   email=(name + "@mail.com"),
                                   password=(name+"A123$"))[0]
    u.save()
    print("> Added User: " + u.username)
    return u

if __name__ == '__main__':
    print("Stating Population Script...")
    populate()
    print("Population Script Complete!")
