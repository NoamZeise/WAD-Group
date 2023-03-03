from django.db import models
from django.contrib.auth.models import User
from rango.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widgrt=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email'. 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture')
