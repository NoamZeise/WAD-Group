from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("This is the froggr blogging site!")

def posts(request):
    return HttpResponse("Posts!")

def test(request):
    return HttpResponse("test")

def dog(request):
    return HttpResponse("This is the dog page")
