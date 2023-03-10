# Generated by Django 4.1.6 on 2023-02-24 13:12

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("restaurants", "0001_initial"),
        ("feed", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userallergen",
            name="allergen",
            field=models.ManyToManyField(
                related_name="userallergens", to="restaurants.ingredient"
            ),
        ),
    ]
