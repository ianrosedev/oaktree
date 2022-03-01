from django.contrib import admin
from .models import Post


@admin.register(Post)
class ProfileAdmin(admin.ModelAdmin):
    model = Post
    list_display = ("title", "author", "publish_date", "is_published")
    list_filter = ("is_published",)
