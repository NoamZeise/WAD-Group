from django.urls import path

from froggr import views

urlpatterns = [
    path('',  views.index, name='index'),
]
