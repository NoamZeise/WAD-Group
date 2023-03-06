from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from froggr.forms import UserForm, UserProfileForm
from froggr.models import BlogPost, User, UserProfile
from froggr import forms
from datetime import datetime

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

def frogout(request):
    logout(request)
    return redirect(reverse('froggr:home'))

def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, 'Account created for: ' + username)
            return redirect('froggr:frog-in')
    context = {'form': form}
    return render(request, 'register.html', context)

@login_required
def my_frogs(request):
    return render(request, 'my_frogs.html')

@login_required
def my_profile(request):
    user = request.user
    profile = None
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None
    if profile == None:
        return redirect('/')
    context_dict["username"] = user.username
    context_dict["profile_img"] = profile.image
    context_dict["profile_text"] = profile.text
    
    return render(request, 'my_profile.html')

def search_results(request):
    return render(request, 'search_results.html')

def top_frogs(request):
    return render(request, 'top_frogs.html')

@login_required
def create_frogg(request):
    form = forms.BlogPostForm()
    if request.method == 'POST':
        form = forms.BlogPostForm(request.POST)
        if form.is_valid():
            for i in request.FILES:
                print(request.FILES[i])
            post = form.save(commit=False)
            post.user = request.user
            if 'image' in request.FILES:
                post.image = request.FILES['image']
            post.date = datetime.now().date()
            post.save()
            return redirect('/')
        else:
            print(form.errors)
    
    return render(request, 'create_frogg.html', {'blog_form': form})

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
