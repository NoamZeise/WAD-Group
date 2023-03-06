from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
#from froggr.models import Category
#from froggr.models import Page
#from froggr.forms import CategoryForm
from django.shortcuts import redirect
from django.urls import reverse
#from froggr.forms import PageForm
from froggr.forms import UserForm, UserProfileForm
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from froggr.models import BlogPost, User
from froggr import forms

# Create your views here.

def posts(request):
    return HttpResponse("Posts!")

def test(request):
    return render(request, 'test_template.html')

def test2(request):
    return render(request, 'test_template_2.html')

def home(request):
    posts = BlogPost.objects.all()
    context_dict = {"posts": posts}
    return render(request, 'home.html', context=context_dict)

def frogin(request):
    return render(request, 'frog_in.html')

def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, 'Account created for: ' + username)
            return redirect('froggr:login')
    context = {'form': form}
    return render(request, 'register.html', context)

def my_frogs(request):
    return render(request, 'my_frogs.html')

def my_profile(request): 
    return render(request, 'my_profile.html')

def search_results(request):
    return render(request, 'search_results.html')

def top_frogs(request):
    return render(request, 'top_frogs.html')

def create_frogg(request):
    form = forms.BlogPostForm()
    if request.method == 'POST':
        form = forms.BlogPostForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('')
        else:
            print(form.errors)
    
    return render(request, 'create_frogg.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('froggr:home'))
            else:
                return HttpResponse("Your Froggr account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/frog-in.html')

def user_logout(request):
    logout(request)
    return redirect(reverse('froggr:home'))


