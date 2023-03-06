from django.urls import path

from froggr import views

app_name = 'froggr'

urlpatterns = [
    path('',  views.home, name='index'),
    path('posts/', views.posts, name='posts'),
    path('test/', views.test, name='test'),
    path('test2/', views.test2, name='test2'),
    path('home/', views.home, name="home"),
    path('frog-in/', views.frogin, name="frog-in"),
    path('frog-out/', views.frogout, name="frog-out"),
    path('register/', views.register, name="register"),
    path('my-frogs/', views.my_frogs, name="my-frogs"),
    path('my-profile/', views.my_profile, name="my-profile"),
    path('search-results/', views.search_results, name="search-results"),
    path('top-frogs/', views.top_frogs, name="top-frogs"),
    path('create-frogg/', views.create_frogg, name="create-frogg"),
]
