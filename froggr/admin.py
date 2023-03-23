from django.contrib import admin
from froggr.models import UserProfile, Connection, BlogPost, Comment
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Connection)
admin.site.register(BlogPost)
admin.site.register(Comment)
