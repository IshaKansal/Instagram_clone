from django.db import models
from custom_addons.models import BaseModel


class UserProfile(BaseModel):
    """
    This class contains the field for user data
    """
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    username = models.CharField(max_length=255, unique=True, null=False, blank=False)
    password = models.CharField(max_length=255, unique=True, null=False, blank=False)


class UserSession(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    session_token = models.CharField(max_length=255)
    is_valid = models.BooleanField(default=True)

    def create_session_token(self):
        from uuid import uuid4
        self.session_token = uuid4()


class PostModel(BaseModel):
    user = models.ForeignKey(UserProfile)
    image = models.FileField(upload_to='user_images')
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=255)
    has_liked = False

    @property
    def like_count(self):
        return len(LikeModel.objects.filter(post=self))

    @property
    def comments(self):
        return CommentModel.objects.filter(post=self).order_by("-created_on")


class LikeModel(BaseModel):
    user = models.ForeignKey(UserProfile)
    post = models.ForeignKey(PostModel)


class CommentModel(BaseModel):
    user = models.ForeignKey(UserProfile)
    post = models.ForeignKey(PostModel)
    comment_text = models.CharField(max_length=1000)

