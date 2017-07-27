from django import forms
from models import UserProfile, PostModel


class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields =['email', 'username', 'name', 'password']


class LoginForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'password']


class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['image', 'caption']