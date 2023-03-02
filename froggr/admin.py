from django.contrib import admin
from froggr.models import User, Connection, BlogPost, Comment, Reaction
# Register your models here.

admin.site.register(User)
admin.site.register(Connection)
admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Reaction)
