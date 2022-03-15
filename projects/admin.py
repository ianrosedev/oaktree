from django.contrib import admin
from django.db import models
from markdownx.widgets import AdminMarkdownxWidget
from .models import Project


@admin.register(Project)
class ProfileAdmin(admin.ModelAdmin):
    model = Project
    list_display = (
        "title",
        "lead",
        "meta_description",
        "is_published",
    )
    readonly_fields = ("slug",)
    list_filter = ("is_published",)
    formfield_overrides = {
        models.TextField: {"widget": AdminMarkdownxWidget},
    }
