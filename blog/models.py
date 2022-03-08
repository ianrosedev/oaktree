import uuid
from django.conf import settings
from django.urls import reverse
from django.db import models
from autoslug import AutoSlugField
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase
from markdownx.models import MarkdownxField


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    """Customize taggit to accept UUID primary keys"""

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, blank=False)
    body = MarkdownxField(blank=False)
    meta_description = models.CharField(max_length=150, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from="title", unique=True)
    tags = TaggableManager(through=UUIDTaggedItem)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"slug": self.slug})
