# Generated by Django 4.0.2 on 2022-03-15 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="link",
        ),
        migrations.AddField(
            model_name="project",
            name="github_link",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="project",
            name="web_link",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]