import uuid
from django.conf import settings
from django.urls import reverse
from django.db import models


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, blank=False)
    body = models.TextField(blank=False)
    meta_description = models.CharField(max_length=150, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"pk": self.pk})
