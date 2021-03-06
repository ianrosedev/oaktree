# Generated by Django 4.0.2 on 2022-04-10 15:21

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_alter_post_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="body",
            field=markdownx.models.MarkdownxField(
                help_text="For accessibility use h2 tags for subheadings."
            ),
        ),
    ]
