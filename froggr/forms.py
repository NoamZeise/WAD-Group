from django.db import models
from django.contrib.auth.models import User
from django.forms import TextInput
from froggr.models import UserProfile, BlogPost, Comment
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('text', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'style': 'min-width: 90%'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'style': 'min-width: 90%'}),
            'image': forms.ClearableFileInput(attrs={'class': 'btn'}),
        }


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'text', 'image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'style': 'min-width: 90%'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'style': 'min-width: 90%'}),
            'image': forms.ClearableFileInput(attrs={'class': 'btn'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ('text', )

        widgets = {
            'text': forms.Textarea(attrs={'class' : 'form-control', 'style': 'min-width: 90%'})
        }
