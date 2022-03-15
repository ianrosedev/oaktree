from django.contrib import admin
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from markdownx.widgets import AdminMarkdownxWidget
from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ("username", "email", "is_staff", "is_active")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                    "short_bio",
                    "social_image",
                    "social_github",
                    "social_linkedin",
                    "is_staff",
                    "is_active",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "short_bio",
                    "social_image",
                    "social_github",
                    "social_linkedin",
                    "is_staff",
                    "is_active",
                )
            },
        ),
    )
    formfield_overrides = {
        models.TextField: {"widget": AdminMarkdownxWidget},
    }
