from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.db import IntegrityError
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.template.defaultfilters import slugify
from froggr_website.settings import MEDIA_URL
from froggr.forms import UserForm, UserProfileForm, CommentForm, BlogPostForm
from froggr.models import BlogPost, User, UserProfile, Comment, Connection
from froggr import forms
from datetime import datetime



# Create your views here.

def missing_page(request, *args, **argv):
    response =  render(request, '404.html')
    response.status_code = 404;
    return response

def register(request):
    form = UserForm()
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if len(slugify(form.data.get("username"))) == 0:
            form.add_error("username", "Username must contain more valid characters url")
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            login(request, user)
            return redirect('froggr:home')
        else:
            context['username'] = form.instance.username
            context['email'] = form.instance.email
    context['form'] =  form
    return render(request, 'register.html', context)

@login_required
def my_frogs(request):
    return render(request, 'my_frogs.html')

def get_user_profile_or_none(user):
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None
    return profile

def checkConnection(user1, user2):
    existing_connection = Connection.objects.filter(user=user1).filter(friend=user2)
    return (len(existing_connection) > 0)

def getProfile(user):
    try:
        userprofile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return None
    except ValueError:
        return None 
    return userprofile 

def getFollowers(user):
    passedFollowers = Connection.objects.filter(friend=user)
    followerList = []
    for follower in passedFollowers:
        followerProfile = getProfile(follower.user)
        followerList.append((follower.user, followerProfile.profile_slug))
    return followerList

def getFollowing(user):
    passedFollowing = Connection.objects.filter(user=user)
    followingList = []
    for following in passedFollowing:
        followingProfile = getProfile(following.friend)
        followingList.append((following.friend, followingProfile.profile_slug))
    return followingList

def profile(request, profile_slug = None):
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
    
    context_dict["logged_in"] = request.user.is_authenticated
    if request.user.is_authenticated:
        context_dict["user_is_following"] = checkConnection(request.user, user)

    context_dict["followers"] = getFollowers(user)
    context_dict["following"] = getFollowing(user)
        
    context_dict["is_logged_in_profile"] = is_logged_in
    context_dict["profile_slug"] = "";
    if profile != None:
        context_dict["profile"] = profile
        context_dict["profile_slug"] = profile.profile_slug;
    context_dict["post_view_title"] = f"{user.username}'s Posts"
    return posts_page(request, BlogPost.objects.filter(user=user), "profile.html", context_dict)

# returns the results of form.save() with image and user filled in
def handle_text_image_form(form, request):
    if form.is_valid():
        form.instance.user = request.user
        if 'image' in request.FILES:
            form.instance.image = request.FILES['image']
            

@login_required
def create_profile(request):
    form = None
    profile = get_user_profile_or_none(request.user)
    if profile != None:
        form = forms.UserProfileForm(
            initial={'text':profile.text,'image':profile.image},
            instance=profile)
    else:
        form = forms.UserProfileForm()
    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, instance=profile)
        handle_text_image_form(form, request)
        form.save()
        return redirect('froggr:create-profile')
        
    return render(request, "create_profile.html", {'profile_form': form})

def new_blogpost_form_old_details(form):
    return forms.BlogPostForm(
                    initial={
                        'title':form.instance.title,
                        'image':form.instance.image,
                        'text':form.instance.text})

@login_required
def create_frogg(request, post_slug=""):
    form = None
    post = None
    try:
        post = BlogPost.objects.get(post_slug=post_slug)
    except BlogPost.DoesNotExist:
        post = None
    if post != None:
        form = forms.BlogPostForm(
            initial={'title':post.title, 'image':post.image, 'text':post.text},
            instance=post)
    else:
        form = forms.BlogPostForm()
    error_message = None
    if request.method == 'POST':
        form = forms.BlogPostForm(request.POST, instance=post)
        handle_text_image_form(form, request)
        if form != None:
            try:
                form.save()
                return redirect('froggr:posts', form.instance.post_slug)
            except IntegrityError:
                # this post already exists, save the inputted info and return form again
                form = new_blogpost_form_old_details(form)
                error_message = "You already have a post with this title!"
            except ValueError:
                form = new_blogpost_form_old_details(form)
                error_message = "This title is invalid!"
                
    return render(request, 'create_frogg.html',
                  {'blog_form': form, 'post_slug' : post_slug, 'error_message': error_message})

def frogin(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('froggr:home')
        else:
            try:
                User.objects.get(username=username)
                messages.info(request, 'Password was incorrect')
            except User.DoesNotExist:
                messages.info(request, 'Username does not exist')
            context['username'] = username
    return render(request, 'frog_in.html', context)


def frogout(request):
    logout(request)
    return redirect(reverse('froggr:home'))


def posts(request, post_slug):
    try:
        post = BlogPost.objects.get(post_slug=post_slug)
    except BlogPost.DoesNotExist:
        return render(request, '404.html')
    form = None
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        form.instance.user = request.user;
        form.instance.post = post;
        form.save();
    if request.user.is_authenticated:
        form = CommentForm()
    context_dict = {}
    context_dict['comment_form'] = form
    context_dict['post'] = post
    context_dict['author_url'] = UserProfile.objects.get(user=post.user).profile_slug
    if post.user == request.user:
        context_dict['user_owns_post'] = True
    context_dict['post_url'] = post_slug
    context_dict['comments'] = Comment.objects.filter(post=post)
    return render(request, 'frogg.html', context_dict)

# ---- views that return lists of posts    

INITIAL_POST_LOAD_COUNT = 21
POSTS_PER_LOAD = 6
POST_BOX_CHAR_LIMIT = 102

def delete_post(request,post_slug=None):
    post_to_delete=BlogPost.objects.get(post_slug=post_slug)
    post_to_delete.delete()
    return redirect('froggr:profile')

def render_posts_for_ajax(query, count):
    load_size = POSTS_PER_LOAD
    if count == 0:
        load_size = INITIAL_POST_LOAD_COUNT
    post_data = ""
    for p in query.all()[count:(count + load_size)]:
        text = p.text[:POST_BOX_CHAR_LIMIT] + '[...]' if len(p.text) > POST_BOX_CHAR_LIMIT else p.text
        # insert space so that for very long words the text will not run on past the post box
        halfway = int(POST_BOX_CHAR_LIMIT/2)
        text = text[:halfway] + ' ' + text[halfway:]
        post_data += render_to_string("post_box.html", { 'post' : p, 'MEDIA_URL' : MEDIA_URL,
                                                         'post_text': text})
    return post_data

def posts_page(request, query, base_page, base_context):
    sorting_order = request.GET.get('sorting_order', 'descending')
    sort_by = request.GET.get('sort_by', 'date')
    sorted_queryset = BlogPost.sort_blogposts(query, sort_by, sorting_order)

    count = 0
    first_load = False
    try:
        count = int(request.GET['post_count'])
    except KeyError:
        first_load = True

    if first_load:
        return render(request, base_page, base_context)
    else:
        return HttpResponse(render_posts_for_ajax(sorted_queryset, count))

def home(request):
    return posts_page(request, BlogPost.objects,
                      'post_feed.html', {})

def search_results(request, search_query=None):
    if request.method == "POST":
        searched = request.POST['search-query']
        return redirect(reverse('froggr:search-results') + slugify(searched))
    if search_query == None:
        return posts_page(request, BlogPost.objects.all(),
                   'search_results.html', {'searched':search_query})
    
    search_query = search_query.replace("-", " ")
    return posts_page(request,
                      BlogPost.objects.filter(
                          Q(text__icontains=search_query) | Q(title__icontains=search_query) |
                      Q(user__username__icontains=search_query)),
                      'search_results.html', {'searched':search_query})

@login_required
def following_posts(request):
    return posts_page(request,
                      BlogPost.objects.filter(
                          user__in=Connection.objects.filter(user=request.user).values('friend')),
                      "post_feed.html", {"post_view_title": "Posts by users you are following"})


def no_results(request):
    return render(request, "no_results.html")

def like_post(request):
    post_id = request.GET['post_id']
    user = request.user
    try:
        post = BlogPost.objects.get(post_slug=post_id)
    except BlogPost.DoesNotExist:
        return HttpResponse(-1)
    except ValueError:
        return HttpResponse(-1) 
    post.toggle_like(user)
    return HttpResponse(post.score)

def create_following_list(friend_user):
    following = Connection.objects.filter(friend=friend_user)
    follow_text = ""
    for u in following:
        follow_text += '<a href="/profile/' + slugify(u.user.username) + '/">' + u.user.username + '</a><br/>'
    return follow_text

class follow(View):
    def get(self, request):
        if request.user.is_authenticated:
            followname = request.GET['followname']
            foundFriend = None
            try:
                foundFriend = User.objects.get(username=followname)
            except User.DoesNotExist:
                return HttpResponse("error")
            except ValueError:
                return HttpResponse("error")
            
            existing_connection = Connection.objects.filter(user=request.user).filter(friend=foundFriend)
            if len(existing_connection) == 0:
                new_connection = Connection.objects.create(user=request.user, friend=foundFriend)
                new_connection.save()
                follow_html = create_following_list(foundFriend)
                return HttpResponse("Unfollow " + follow_html)
            else:
                existing_connection[0].delete()
                follow_html = create_following_list(foundFriend)
                return HttpResponse("Follow " + follow_html)
        return HttpResponse("error") 
