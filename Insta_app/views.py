from django.shortcuts import render, redirect
from forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm
import datetime
from django.contrib.auth.hashers import make_password, check_password
from models import UserProfile, UserSession, PostModel, LikeModel, CommentModel
from imgurpython import ImgurClient
from InstagramClone.settings import BASE_DIR
from clarifai.rest import ClarifaiApp

api_key = "b4bca6c0c5b94a9ca1ec75dd5e567d27"


def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = UserSession.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user
        else:
            return None
    else:
        return None


def signup_view(request):
    date = datetime.datetime.now()
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            username = signup_form.cleaned_data['username']
            name = signup_form.cleaned_data['name']
            password = signup_form.cleaned_data['password']
            email = signup_form.cleaned_data['email']
            user = UserProfile(name=name, password=make_password(password), username=username, email=email)
            user.save()
            return render(request, 'success.html')
    elif request.method == 'GET':
        signup_form = SignUpForm()
        return render(request, 'index.html', {"Today_date": date, 'form': signup_form})


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = UserProfile.objects.filter(username=login_form.cleaned_data['username']).first()
            if user:
                if check_password(login_form.cleaned_data['password'], user.password):
                    session = UserSession(user=user)
                    session.create_session_token()
                    session.save()
                    response = redirect('/feed/')
                    response.set_cookie(key='session_token', value=session.session_token)
                    return response
                else:
                    print ("Password does not match")
            else:
                print ("user does not exist")
            return render(request, 'index.html')
    elif request.method == 'GET':
        login_form = LoginForm()
    return render(request, 'login.html', {'form': login_form})


def post_view(request):
    user = check_validation(request)
    if user:
        if request.method == "POST":
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                image = post_form.cleaned_data['image']
                caption = post_form.cleaned_data['caption']
                post = PostModel(user=user, image=image, caption=caption)
                post.save()
                path = (BASE_DIR + "\\" + post.image.url)
                client = ImgurClient('f7be8da6b2d2474', '2ec7b8a30028635db5e815fbcc8dab81c45d231a')
                post.image_url = client.upload_from_path(path, anon=True)['link']
                post.save()
                return redirect('/feed/')
        elif request.method == "GET":
            post_form = PostForm()
        return render(request, 'post.html', {'form': post_form})
    else:
        return redirect('/login/')


def like_view(request):
    user = check_validation(request)
    if user and request.method == "POST":
        like_form = LikeForm(request.POST)
        if like_form.is_valid():
            post_id = like_form.cleaned_data.get('post').id
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()
            return redirect('/feed/')
    else:
        return redirect('/login/')


def comment_view(request):
    user = check_validation(request)
    if user and request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            post_id = comment_form.cleaned_data.get('post').id
            comment_text = comment_form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login/')


def feed_view(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by("-created_on")
        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True
        return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect("/login/")
