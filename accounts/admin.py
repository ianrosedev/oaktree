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
                    "groups",
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
                    "groups",
                )
            },
        ),
    )
    formfield_overrides = {
        models.TextField: {"widget": AdminMarkdownxWidget},
    }

    # Limit users to their own profile
    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(id=request.user.id)

    # Limit users to read only certain attributes
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        else:
            return ("is_staff", "is_active", "groups")
