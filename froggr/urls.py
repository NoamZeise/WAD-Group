from django.urls import path

from froggr import views

app_name = 'rango'

urlpatterns = [
    path('',  views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('test/', views.test, name='test'),
    path('dog/', views.dog, name="dog"),
]
