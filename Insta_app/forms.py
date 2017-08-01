from django import forms
from models import UserProfile, PostModel, LikeModel, CommentModel


class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'username', 'name', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)
    fields = ['username', 'password']


class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['image', 'caption']


class LikeForm(forms.ModelForm):
    class Meta:
        model = LikeModel
        fields = ['post']


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['comment_text', 'post']
