from django.urls import path

from froggr import views

app_name = 'froggr'

urlpatterns = [
    path('',  views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('test/', views.test, name='test'),
    path('test2/', views.test2, name='test2'),
    path('dog/', views.dog, name="dog"),
]
