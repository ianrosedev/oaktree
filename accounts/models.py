import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from markdownx.models import MarkdownxField


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    short_bio = models.CharField(max_length=250, blank=True)
    social_image = MarkdownxField(blank=True)
    social_github = models.CharField(max_length=100, blank=True)
    social_linkedin = models.CharField(max_length=100, blank=True)
