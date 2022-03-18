import uuid
from django.conf import settings
from django.urls import reverse
from django.db import models
from autoslug import AutoSlugField
from markdownx.models import MarkdownxField


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, blank=False)
    lead = models.CharField(max_length=300, blank=False)
    body = MarkdownxField(
        blank=False, help_text="For accessibility use h2 tags for subheadings."
    )
    web_link = models.CharField(max_length=100, blank=True)
    github_link = models.CharField(max_length=100, blank=True)
    main_image = MarkdownxField(blank=False)
    meta_description = models.CharField(max_length=150, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from="title", unique=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project", kwargs={"slug": self.slug})
