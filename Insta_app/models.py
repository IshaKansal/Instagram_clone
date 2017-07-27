from django.db import models
from custom_addons.models import BaseModel


class UserProfile(BaseModel):
    """
    This class contains the field for user data
    """
    email = models.EmailField()
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    username = models.CharField(max_length=255)
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
