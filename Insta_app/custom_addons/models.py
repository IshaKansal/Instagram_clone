from django.db import models

class BaseModel(models.Model):
    """
    This class contains fields which are to be added in every app
    """
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
