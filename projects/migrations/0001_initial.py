# Generated by Django 4.0.2 on 2022-03-14 18:26

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import markdownx.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("lead", models.CharField(max_length=300)),
                ("body", markdownx.models.MarkdownxField()),
                ("link", models.CharField(max_length=100)),
                ("main_image", markdownx.models.MarkdownxField()),
                ("meta_description", models.CharField(blank=True, max_length=150)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("publish_date", models.DateTimeField(blank=True, null=True)),
                ("is_published", models.BooleanField(default=False)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from="title", unique=True
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-date_created"],
            },
        ),
    ]