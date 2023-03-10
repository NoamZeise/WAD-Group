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

def get_user_profile_or_none(user):
    profile = None
    try:
       profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None
    return profile

def profile(request, profile_slug = None):
    print(profile_slug)
    user = None
    is_logged_in = False
    if request.path == reverse('froggr:profile'):
       user = request.user
    else:
        try:
            user = UserProfile.objects.get(profile_slug=profile_slug)
            user = user.user
        except UserProfile.DoesNotExist:
            user = None
    if user == None:
        return render(request, '404.html')

    if user == request.user:
        is_logged_in = True

    profile = get_user_profile_or_none(user)
    context_dict = {}
    context_dict["username"] = user.username
    context_dict["is_logged_in_profile"] = is_logged_in
    if profile != None:
        context_dict["profile_img"] = profile.image
        context_dict["profile_text"] = profile.text
    
    return render(request, 'profile.html', context_dict)

# returns the results of form.save() with image and user filled in
def handle_text_image_form(form, request):
    if form.is_valid():
        form.instance.user = request.user
        if 'image' in request.FILES:
            form.instance.image = request.FILES['image']
    else:
        print(form.errors)
                
@login_required
def create_profile(request):
    form = None
    profile = get_user_profile_or_none(request.user)
    if profile != None:
        form = forms.UserProfileForm(initial={'text':profile.text,'image':profile.image}, instance=profile)
    else:
        form = forms.UserProfileForm()
    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, instance=profile)
        handle_text_image_form(form, request)
        form.save()
        return redirect('froggr:profile')
        
    return render(request, "create_profile.html", {'profile_form': form})

def search_results(request):
    return render(request, 'search_results.html')

def top_frogs(request):
    return render(request, 'top_frogs.html')

@login_required
def create_frogg(request):
    form = forms.BlogPostForm()
    if request.method == 'POST':
        form = forms.BlogPostForm(request.POST)
        handle_text_image_form(form, request)
        if form != None:
            form.instance.date = datetime.now().date()
            form.save()
            return redirect('/')
    
    return render(request, 'create_frogg.html', {'blog_form': form})

def frogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('froggr:home')
        else:
            messages.info(request, 'Username OR Password is incorrect')
    context = {}
    return render(request, 'frog_in.html', context)


def frogout(request):
    logout(request)
    return redirect(reverse('froggr:home'))


def posts(request, post_slug):
    try:
        post = BlogPost.objects.get(post_slug=post_slug)
    except BlogPost.DoesNotExist:
        return render(request, '404.html')
    print(post.title)
    context_dict = {}
    context_dict['blog_title'] = post.title
    context_dict['blog_img'] = post.image
    context_dict['blog_text'] = post.text
    context_dict['blog_author'] = post.user.username
    return render(request, 'frogg.html', context_dict)
