# Generated by Django 4.0.2 on 2022-03-02 17:27

import autoslug.fields
from django.db import migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_rename_published_post_is_published"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ["-date_created"]},
        ),
        migrations.AddField(
            model_name="post",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                default=django.utils.timezone.now,
                editable=False,
                populate_from="title",
                unique=True,
            ),
            preserve_default=False,
        ),
    ]
