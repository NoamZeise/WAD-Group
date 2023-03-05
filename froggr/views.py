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

# Create your views here.

def index(request):
    return HttpResponse("This is the froggr blogging site!")

def posts(request):
    return HttpResponse("Posts!")

def test(request):
    return render(request, 'test_template.html')

def test2(request):
    return render(request, 'test_template_2.html')

def home(request):
    return render(request, 'home.html')

def dog(request):
    return HttpResponse("This is the dog page")


def frogin(request):
    return render(request, 'frog-in.html')

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


