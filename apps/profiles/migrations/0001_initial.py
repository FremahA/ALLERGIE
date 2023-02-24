# Generated by Django 4.1.6 on 2023-02-24 13:12

from django.db import migrations, models
import django_countries.fields
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "about_me",
                    models.TextField(
                        default="say something about yourself", verbose_name="About me"
                    ),
                ),
                (
                    "profile_photo",
                    models.ImageField(upload_to="media", verbose_name="Profile Photo"),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("Male", "Male"),
                            ("Female", "Female"),
                            ("Other", "Other"),
                        ],
                        default="Other",
                        max_length=20,
                        verbose_name="Gender",
                    ),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(
                        default="GH", max_length=2, verbose_name="Country"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
